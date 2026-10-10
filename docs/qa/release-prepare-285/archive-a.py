from pathlib import Path
import json,hashlib,tarfile,stat,os,subprocess,urllib.request
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');Q=R/'docs/qa/release-prepare-285';B=Path.home()/'.local/share/rach-doi-son-ha/releases/285'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,v):(Q/n).write_text(json.dumps(v,indent=2)+'\n')
def tree(b):
 d={}
 for p in [b,*sorted(b.rglob('*'))]:
  n=str(p.relative_to(b));mode=stat.S_IMODE(p.lstat().st_mode)
  if p.is_symlink():d[n]={'type':'symlink','target':os.readlink(p),'mode':mode}
  elif p.is_dir():d[n]={'type':'directory','mode':mode}
  else:d[n]={'type':'file','sha256':h(p),'bytes':p.stat().st_size,'mode':mode}
 return d
archives={}
for name in ['rollback270']:
 source=B/name;expected=tree(source);archive=B/(name+'.tar.gz')
 if not archive.exists():
  with tarfile.open(archive,'w:gz') as t:t.add(source,arcname=name,recursive=True)
 archive.chmod(0o400)
 with tarfile.open(archive) as t:
  entries={str(Path(m.name).relative_to(name)):m for m in t.getmembers()};assert set(entries)==set(expected)
  for n,v in expected.items():
   m=entries[n];assert m.mode==v['mode']
   if v['type']=='file':assert hashlib.sha256(t.extractfile(m).read()).hexdigest()==v['sha256']
   if v['type']=='symlink':assert m.linkname==v['target']
 # Python data filter can restore writable owner modes; restore exact archive modes only in private extraction, then verify.
 extraction=B/('verify-'+name);extraction.mkdir(mode=0o700,exist_ok=True)
 if not (extraction/name).exists():
  with tarfile.open(archive) as t:
   t.extractall(extraction,filter='data')
   members=t.getmembers()
   for m in members:
    p=extraction/m.name
    if m.isfile():p.chmod(m.mode)
   for m in sorted(members,key=lambda x:len(Path(x.name).parts),reverse=True):
    if m.isdir():(extraction/m.name).chmod(m.mode)
 assert tree(extraction/name)==expected
 archives[name]={'path':str(archive),'sha256':h(archive),'entries':len(expected),'archiveBytesModesInventoryVerified':True,'dataFilterExtractionThenExactModeRepairVerified':True,'inventory':expected}
write('archives.json',archives)

