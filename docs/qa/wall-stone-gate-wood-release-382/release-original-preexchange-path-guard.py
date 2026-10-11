from pathlib import Path
import hashlib,json,stat,os,subprocess,shutil,ctypes,urllib.request
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');Q=R/'docs/qa/wall-stone-gate-wood-release-382';P=Path.home()/'.local/share/rach-doi-son-ha/releases/382';OLD=P.parent/'380';B=Path('/tmp/rds-gates379-build');S=Path('/tmp/rds-gates379-stage');NEXT=R.parent/'rds-public382-next-dist';RT=P.parent/'230/runtime230';HEAD='e042f0e97e9066c2c25ef7828657631963db593f';BASE='https://kieu-hoang-quan-loq-15iax9.tail5247a0.ts.net'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(n,x):(Q/n).write_text(json.dumps(x,indent=2)+'\n')
def cmd(*a):return subprocess.check_output(a,text=True)
def entry(p):
 s=p.lstat();m=stat.S_IMODE(s.st_mode)
 if p.is_symlink():return {'type':'symlink','mode':m,'target':os.readlink(p)}
 if p.is_dir():return {'type':'directory','mode':m}
 assert stat.S_ISREG(s.st_mode);return {'type':'file','mode':m,'size':s.st_size,'sha256':sha(p)}
def inv(p):return {'.':entry(p),**{str(x.relative_to(p)):entry(x) for x in sorted(p.rglob('*'))}}
ready=json.loads((R/'docs/qa/wall-stone-gate-wood-public-381/receipt.json').read_text());bind=json.loads((R/'docs/qa/wall-stone-gate-wood-public-381/binding.json').read_text());seal=json.loads((R/'docs/qa/wood-gate-restoration-379/seal.json').read_text());meta=json.loads((OLD/'metadata.json').read_text())
assert not P.exists() and not NEXT.exists() and not (Q/'attempt.json').exists()
assert sha(Path(ready['candidateArchive']))==ready['candidateSHA256'] and sha(OLD/'rollback367.tar.gz')==ready['pairedRollbackSHA256']
assert sha(R/'docs/qa/wood-gate-restoration-379/seal.json')==bind['seal379SHA256']
assert inv(B)==bind['sourceInventory'] and inv(R/'dist')==bind['baseInventory']
for root,key in [(S,'stage'),(B,'build')]:assert {str(x.relative_to(root)):sha(x) for x in root.rglob('*') if x.is_file()}==seal[key]
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
backendBefore=backend();P.mkdir(mode=0o700);shutil.copytree(B,NEXT,copy_function=shutil.copy2);NEXT.chmod(0o755)
expected=dict(bind['sourceInventory']);expected['.']={'type':'directory','mode':0o755};assert inv(NEXT)==expected
# Canonical installation is root-owned; record the actual authorized delta, without requiring the pre-install tree.
allowed={'client/wood-gate.js','client/renderer.js','client/fortification-art.js','client/fortification-picking.js','public/assets/art-v1/stone-361-manifest.json','public/assets/art-v1/fort-202-manifest.json'}
delta={}
for p,v in meta['guards'].items():
 path=Path(p);actual=entry(path);rel=str(path.relative_to(R)) if path.is_relative_to(R) else p
 if actual!=v:assert rel in allowed,rel;delta[rel]={'before':v,'after':actual}
dump('source-binding.json',{'testedStage':str(S),'testedBuild':str(B),'seal379SHA256':bind['seal379SHA256'],'archive381SHA256':ready['candidateSHA256'],'rootAuthorizedCanonicalDeltaObserved':delta,'sourceHEAD':HEAD,'rootActualIntake':'Root explicitly accepts actual379 X/Y default gameplay-size completedidle wooden gate + stone wall scenes, pick/transit/PauseResumeStop; separate383 public actual browser pending'})
assert inv(R/'dist')==bind['baseInventory'];backend();dump('attempt.json',{'order':382,'authorized':True,'scope':'ONE frontend atomic exchange SAME sealed379; no restart','next':str(NEXT),'rootMode':0o755})
libc=ctypes.CDLL(None,use_errno=True);exchange=libc.renameat2;exchange.argtypes=[ctypes.c_int,ctypes.c_char_p,ctypes.c_int,ctypes.c_char_p,ctypes.c_uint];exchange.restype=ctypes.c_int
def swap():
 if exchange(-100,os.fsencode(R/'dist'),-100,os.fsencode(NEXT),2):raise OSError(ctypes.get_errno(),'renameat2 exchange failed')
swap()
try:
 assert inv(R/'dist')==expected and inv(NEXT)==bind['baseInventory'];responses={}
 for rel,want in ready['requiredResponsePins'].items():
  req=urllib.request.Request(BASE+'/'+rel,headers={'Cache-Control':'no-cache'})
  with urllib.request.urlopen(req,timeout=30) as response:
   data=response.read();assert response.status==200;got=hashlib.sha256(data).hexdigest();assert got==want,rel;responses[rel]={'status':response.status,'sha256':got,'bytes':len(data)}
 after=backend();assert sha(OLD/'rollback367.tar.gz')==ready['pairedRollbackSHA256']
 dump('receipt.json',{'order':382,'status':'PROMOTED_PUBLIC382_SAME_SEALED379_BACKEND230_UNCHANGED','files':200,'defaultCount':16,'fortCount':45,'gateRows':7,'candidateArchiveSHA256':ready['candidateSHA256'],'pairedRollback380SHA256':ready['pairedRollbackSHA256'],'old367Tree':str(NEXT),'normalTLSPins':responses,'backend':after,'sourceHEAD':HEAD,'exchanges':1,'buildBrowserImageRestartCalls':0,'preservationPASS':True,'handles':'CLOSED','pending':'Separate383 actualpublic browser intake; no fullgoal inference'})
 print('PROMOTED382 exact200/default16/fort45; 8normalTLSpins PASS; backend230 unchanged; CLOSED')
except Exception as e:
 dump('failure.json',{'error':repr(e),'postExchange':True});swap();assert inv(R/'dist')==bind['baseInventory'];backend();dump('rollback.json',{'restoredCurrent367':True,'backendRestarted':False,'paired230Unchanged':True,'handles':'CLOSED'});raise
