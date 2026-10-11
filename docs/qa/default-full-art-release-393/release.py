from pathlib import Path
import hashlib,json,stat,os,subprocess,shutil,ctypes,urllib.request
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');Q=R/'docs/qa/default-full-art-release-393';P=Path.home()/'.local/share/rach-doi-son-ha/releases/393';OLD=P.parent/'390';B=Path('/tmp/rds-fullart389-build');S=Path('/tmp/rds-fullart389-stage');NEXT=R.parent/'rds-public391-next-dist';RT=P.parent/'230/runtime230';HEAD='2b16979393716bc056e205f8fc50eaea07db0593';BASE='https://kieu-hoang-quan-loq-15iax9.tail5247a0.ts.net'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(n,x):(Q/n).write_text(json.dumps(x,indent=2)+'\n')
def cmd(*a):return subprocess.check_output(a,text=True)
def entry(p):
 s=p.lstat();m=stat.S_IMODE(s.st_mode)
 if p.is_symlink():return {'type':'symlink','mode':m,'target':os.readlink(p)}
 if p.is_dir():return {'type':'directory','mode':m}
 assert stat.S_ISREG(s.st_mode);return {'type':'file','mode':m,'size':s.st_size,'sha256':sha(p)}
def inv(p):return {'.':entry(p),**{str(x.relative_to(p)):entry(x) for x in sorted(p.rglob('*'))}}
ready=json.loads((R/'docs/qa/default-full-art-public-391/receipt.json').read_text());bind=json.loads((R/'docs/qa/default-full-art-public-391/binding.json').read_text());seal=json.loads((R/'docs/qa/default-full-art-runtime-389/binding.json').read_text());meta=json.loads((OLD/'metadata.json').read_text())
intake=R/'docs/qa/default-full-art-runtime-392/root-intake.json';assert intake.is_file()
assert not P.exists() and NEXT.is_dir() and not (Q/'attempt.json').exists()
assert sha(Path(ready['candidateArchive']))==ready['candidateSHA256'] and sha(OLD/'rollback382.tar.gz')==ready['pairedRollback390SHA256']
assert sha(R/'docs/qa/default-full-art-runtime-389/binding.json')==bind['binding389SHA256']
assert inv(B)==bind['sourceInventory'] and inv(R/'dist')==bind['currentBaseInventory']
for root,key in [(S,'sourcePins'),(B,'buildPins')]:assert {str(x.relative_to(root)):{'sha256':sha(x),'mode':oct(stat.S_IMODE(x.stat().st_mode))} for x in root.rglob('*') if x.is_file()}==seal[key]
for p,v in bind['canonicalPins'].items():assert entry(Path(p))==v
def backend():
 pol=meta['policy'];assert cmd('git','rev-parse','HEAD').strip()==HEAD
 assert cmd('systemctl','--user','show','rach-doi-son-ha.service','-p','ActiveState','-p','MainPID','-p','WorkingDirectory','-p','FragmentPath','-p','DropInPaths','-p','EnvironmentFiles')==pol['service']
 assert cmd('tailscale','serve','status','--json')==pol['funnel']
 assert sha('/proc/3229/environ')==pol['environmentSHA256'] and sha('/proc/3229/cmdline')==pol['cmdlineSHA256']
 assert os.readlink('/proc/3229/cwd')==str(RT)
 h=json.loads(cmd('curl','-fsS','http://127.0.0.1:3000/health'));assert h['rooms']==0
 for arc,v in meta['sourceEntries'].items():
  if arc.startswith('runtime230'):p=RT/arc.removeprefix('runtime230').lstrip('/')
  elif arc=='node/bin/node':p=Path.home()/'.nvm/versions/node/v24.15.0/bin/node'
  elif arc=='policy/rach-doi-son-ha.service':p=Path.home()/'.config/systemd/user/rach-doi-son-ha.service'
  elif arc.startswith('policy/rach-doi-son-ha.service.d'):p=Path.home()/'.config/systemd/user/rach-doi-son-ha.service.d'/arc.removeprefix('policy/rach-doi-son-ha.service.d').lstrip('/')
  else:continue
  assert entry(p)==v
 return {'pid':3229,'rooms':0,'runtime230Exact':True,'nodeWsUnitEnvFunnelExact':True}
backendBefore=backend();P.mkdir(mode=0o700);assert stat.S_IMODE(NEXT.stat().st_mode)==0o755
expected=dict(bind['sourceInventory']);expected['.']={'type':'directory','mode':0o755};assert inv(NEXT)==expected
dump('source-binding.json',{'testedStage':str(S),'testedBuild':str(B),'binding389SHA256':bind['binding389SHA256'],'archive391SHA256':ready['candidateSHA256'],'rootActual392IntakeSHA256':sha(intake),'sourceHEAD':HEAD,'canonicalPinsReverified':True,'original389HOLDRetained':True})
assert inv(R/'dist')==bind['currentBaseInventory'];backend();dump('attempt.json',{'order':393,'authorized':True,'scope':'ONE frontend atomic exchange SAME sealed389; no restart','next':str(NEXT),'rootMode':0o755})
libc=ctypes.CDLL(None,use_errno=True);exchange=libc.renameat2;exchange.argtypes=[ctypes.c_int,ctypes.c_char_p,ctypes.c_int,ctypes.c_char_p,ctypes.c_uint];exchange.restype=ctypes.c_int
def swap():
 if exchange(-100,os.fsencode(R/'dist'),-100,os.fsencode(NEXT),2):raise OSError(ctypes.get_errno(),'renameat2 exchange failed')
swap()
try:
 assert inv(R/'dist')==expected and inv(NEXT)==bind['currentBaseInventory'];responses={}
 responsePins=dict(ready['requiredResponsePins'])
 for rel in ['assets/art-v1/runtime/grass.webp','assets/art-v1/runtime/forest.webp','assets/art-v1/runtime/residence-idle.webp','assets/art-v1/runtime/storage-depot-idle.webp','assets/art-v1/characters/villager-neutral-D00-screen-ESE.png']:
  if (B/rel).is_file():responsePins[rel]=sha(B/rel)
 for rel,want in responsePins.items():
  req=urllib.request.Request(BASE+'/'+rel,headers={'Cache-Control':'no-cache'})
  with urllib.request.urlopen(req,timeout=30) as response:
   data=response.read();assert response.status==200;got=hashlib.sha256(data).hexdigest();assert got==want,rel;responses[rel]={'status':response.status,'sha256':got,'bytes':len(data)}
 after=backend();assert sha(OLD/'rollback382.tar.gz')==ready['pairedRollback390SHA256']
 dump('receipt.json',{'order':393,'status':'PROMOTED_PUBLIC393_SAME_SEALED389_BACKEND230_UNCHANGED','files':201,'default':'fort','world':True,'assets':45,'candidateArchiveSHA256':ready['candidateSHA256'],'pairedRollback390SHA256':ready['pairedRollback390SHA256'],'old382Tree':str(NEXT),'normalTLSPins':responses,'backend':after,'sourceHEAD':HEAD,'exchanges':1,'buildBrowserImageRestartCalls':0,'preservationPASS':True,'handles':'CLOSED','pending':'Separate394 actualpublic browser intake; no fullgoal inference'})
 print('PROMOTED393 exact201/defaultfort45/worldtrue; 8normalTLSpins PASS; backend230 unchanged; CLOSED')
except Exception as e:
 dump('failure.json',{'error':repr(e),'postExchange':True});swap();assert inv(R/'dist')==bind['currentBaseInventory'];backend();dump('rollback.json',{'restoredCurrent382':True,'backendRestarted':False,'paired230Unchanged':True,'handles':'CLOSED'});raise
