from pathlib import Path
import json,hashlib,tarfile,stat,os,subprocess,urllib.request
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');Q=R/'docs/qa/release-prepare-269';B=Path.home()/'.local/share/rach-doi-son-ha/releases/269'
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
for name in ['dist269']:
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
write('candidate-archives.json',archives)

inv=lambda b:{str(f.relative_to(b)):h(f) for f in sorted(b.rglob('*')) if f.is_file()}
assert inv(R/'dist')==json.loads((Q/'public260-before.json').read_text())
service=subprocess.check_output(['systemctl','--user','show','rach-doi-son-ha.service','-p','MainPID','-p','WorkingDirectory','-p','ActiveState'],text=True);assert service==(Q/'service-before.txt').read_text()
health=json.load(urllib.request.urlopen('http://127.0.0.1:3000/health'));assert health=={'ok':True,'rooms':0}
write('receipt.json',{'status':'FROZEN_FORT46_FROZEN266_CANDIDATE_READY_ROOT266B_267B_ACCEPTED_NOT_PROMOTED','candidateArchive':{k:v for k,v in archives['dist269'].items() if k!='inventory'},'buildBinding':json.loads((Q/'build-binding.json').read_text()),'manifestAssets':46,'builds':0,'frozenBuildReused':True,'public260Unchanged':True,'PID':575363,'backendRestarted':False,'productionMutations':0,'health':health,'rollback260SHA256':h(B/'rollback260.tar.gz')})
print(archives['dist269']['sha256'])
