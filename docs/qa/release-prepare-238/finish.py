from pathlib import Path
import json,hashlib,shutil,tarfile,os,stat,subprocess,urllib.request
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');Q=R/'docs/qa/release-prepare-238';S=Path('/tmp/rds-release238-stage');BUILD=Path('/tmp/rds-release238-build');B=Path.home()/'.local/share/rach-doi-son-ha/releases/238'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();inv=lambda b:{str(f.relative_to(b)):h(f) for f in sorted(b.rglob('*')) if f.is_file()}
def write(n,v):(Q/n).write_text(json.dumps(v,indent=2)+'\n')
old=json.loads((Q/'public230-before.json').read_text());retained=[]
for n,digest in old.items():
 if n.startswith('assets/index-'):
  dest=BUILD/n
  if dest.exists():assert h(dest)==digest
  else:shutil.copy2(R/'dist'/n,dest);retained.append(n)
write('build-pins.json',inv(BUILD));write('build-binding.json',{'cwd':str(S),'config':str(S/'vite.config.js'),'outDir':str(BUILD),'command':'./node_modules/.bin/vite build --config /tmp/rds-release238-stage/vite.config.js --outDir /tmp/rds-release238-build','freshBundle':[(str(f),h(f)) for f in (BUILD/'assets').glob('index-z82FayZ6.js')],'oldChunksRetained':retained,'candidateFiles':len(inv(BUILD))})
def tree(b):
 d={}
 for p in [b,*sorted(b.rglob('*'))]:
  n=str(p.relative_to(b));mode=stat.S_IMODE(p.lstat().st_mode)
  if p.is_symlink():d[n]={'type':'symlink','target':os.readlink(p),'mode':mode}
  elif p.is_dir():d[n]={'type':'directory','mode':mode}
  else:d[n]={'type':'file','sha256':h(p),'bytes':p.stat().st_size,'mode':mode}
 return d
archives={}
for name in ['runtime238','rollback230','dist238']:
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
# Stable publication and service checks; no stop/restart/deploy.
assert inv(R/'dist')==old;write('public230-after.json',inv(R/'dist'));current={n:inv(R/n) for n in ['client','shared','server','public']};assert current==json.loads((Q/'canonical-before.json').read_text());write('canonical-after.json',current)
service=subprocess.check_output(['systemctl','--user','show','rach-doi-son-ha.service','-p','MainPID','-p','WorkingDirectory','-p','ActiveState'],text=True);assert service==(Q/'service-before.txt').read_text();(Q/'service-after.txt').write_text(service);health=json.load(urllib.request.urlopen('http://127.0.0.1:3000/health',timeout=5));write('health-after.json',health)
# Service metadata bytes unchanged, no raw policies printed.
meta=B/'rollback230/service-metadata';assert h(meta/'unit')==h(Path.home()/'.config/systemd/user/rach-doi-son-ha.service');assert inv(meta/'dropins')==inv(Path.home()/'.config/systemd/user/rach-doi-son-ha.service.d')
print('238 archive byte/mode/extraction verified, public186/PID575363/canonical unchanged')
