"""Append ONLY authorized server after successful native lifecycle proof; CAS + backup."""
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile
import tomllib
import uuid
repo=Path(__file__).resolve().parents[3]
base=repo/'docs/audits/blender-runtime-502/connection'
assignment=json.loads((base/'assignment.json').read_text())
for pin in assignment['inputs']:
 if hashlib.sha256((repo/pin['path']).read_bytes()).hexdigest()!=pin['sha256']:raise ValueError('assignment input drift: '+pin['path'])
proofs=[json.loads(p.read_text()) for p in (base/'runs').glob('*/receipt.json')]
if not any(p['ready'] and p['closed'] and p['failure'] is None and p['serverExit']==0 for p in proofs):raise ValueError('actual ownedlifecycle proof missing')
response=json.loads((base/'sdk-response.json').read_text())
status=json.loads(response['status']['structuredContent']['result'])
if response['status']['isError'] or response['scene']['isError'] or status['telemetry_consent'] is not False:raise ValueError('actual readonly handshake missing')
config=Path(assignment['externalConfiguration'])
if not config.is_file() or config.is_symlink():raise ValueError('regular existingconfig required')
raw=config.read_bytes();before=tomllib.loads(raw.decode());sourceSHA=hashlib.sha256(raw).hexdigest()
mode=stat.S_IMODE(config.stat().st_mode)
if 'rds_blender501' in before.get('mcp_servers',{}):raise ValueError('namedserver alreadyexists; no overwrite')
stanza=(base/'server-stanza.toml').read_bytes()
new=raw+(b'' if raw.endswith(b'\n') else b'\n')+stanza
parsed=tomllib.loads(new.decode());expected=dict(before);expected['mcp_servers']=dict(before.get('mcp_servers',{}));expected['mcp_servers']['rds_blender501']=tomllib.loads(stanza.decode())['mcp_servers']['rds_blender501']
if parsed!=expected or not new.startswith(raw):raise ValueError('otherconfiguration changed')
backupdir=config.parent/'backups'/('blender502-'+uuid.uuid4().hex)
backupdir.mkdir(parents=True,mode=0o700)
backup=backupdir/'config.toml.before'
fd=os.open(backup,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
with os.fdopen(fd,'wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
if hashlib.sha256(config.read_bytes()).hexdigest()!=sourceSHA:raise ValueError('configCASdrift; preservedbackup only')
fd,tmp=tempfile.mkstemp(prefix='.blender502-config-',dir=config.parent)
try:
 with os.fdopen(fd,'wb') as f:
  f.write(new);f.flush();os.fsync(f.fileno());os.fchmod(f.fileno(),mode)
 if config.read_bytes()!=raw:raise ValueError('configCASdrift beforeatomicwrite')
 os.replace(tmp,config)
 directory=os.open(config.parent,os.O_RDONLY)
 try:os.fsync(directory)
 finally:os.close(directory)
finally:
 if Path(tmp).exists():Path(tmp).unlink()
written=config.read_bytes()
if written!=new or stat.S_IMODE(config.stat().st_mode)!=mode:raise ValueError('writtenconfigverification failed')
receipt={'status':'VERIFIED_CONFIGURED_READ_SCOPE','path':str(config),'beforeSHA256':sourceSHA,'afterSHA256':hashlib.sha256(written).hexdigest(),'rawPrefixPreserved':written.startswith(raw),'otherParsedEntriesPreserved':True,'originalMode':oct(mode),'afterMode':oct(stat.S_IMODE(config.stat().st_mode)),'backup':{'path':str(backup),'mode':oct(stat.S_IMODE(backup.stat().st_mode)),'sha256':hashlib.sha256(backup.read_bytes()).hexdigest()},'serverNamesBefore':sorted(before.get('mcp_servers',{})),'serverNamesAfter':sorted(parsed['mcp_servers']),'enabledTools':parsed['mcp_servers']['rds_blender501']['enabled_tools'],'toolExposure':'UNKNOWN currentchat inventory notrefreshed; noapprestart','scope':'Configurationonly; noauthoring/generation/production'}
(base/'config-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'status':receipt['status'],'servers':receipt['serverNamesAfter'],'otherEntriesPreserved':True}))
