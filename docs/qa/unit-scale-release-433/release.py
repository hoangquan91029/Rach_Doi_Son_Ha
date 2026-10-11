exec(open('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha/docs/qa/unit-scale-public-432/prepare.py').read().split('intake=')[0])
import ctypes,urllib.request
Q=R/'docs/qa/unit-scale-release-433';P=Path.home()/'.local/share/rach-doi-son-ha/releases/433';N=R.parent/'rds-public432-next-dist';RT=P.parent/'230/runtime230';BASE='https://kieu-hoang-quan-loq-15iax9.tail5247a0.ts.net'
ready=json.loads((R/'docs/qa/unit-scale-public-432/receipt.json').read_text());bind=json.loads((R/'docs/qa/unit-scale-runtime-426/binding.json').read_text());meta=json.loads((P.parent/'428/metadata.json').read_text());intake=R/'docs/qa/unit-scale-clear-travel-430/root-intake.json'
assert ready['guards']=='CLOSED' and ready['actualProductionSchemaPASS'] and json.loads(intake.read_text())==ready['rootActualSceneIntake']
assert not P.exists() and not (Q/'attempt.json').exists();assert sha(ready['archive'])==ready['archiveSHA256'];assert sha(ready['rollback'])==ready['rollbackSHA256']
head=cmd('git','rev-parse','HEAD').strip();assert head==ready['sourceHEAD']
canonical={str(p):sha(p) for root in [R/'client',R/'shared',R/'server',R/'public'] if root.exists() for p in root.rglob('*') if p.is_file()};source=inv(B);old=inv(R/'dist');expected=inv(N);assert expected['.']['mode']==0o755;assert {k:v for k,v in expected.items() if k!='.'}=={k:v for k,v in source.items() if k!='.'}
assert sum(v['type']=='file' for v in old.values())==207;assert sum(v['type']=='file' for v in expected.values())==208
for root,key in [(S,'sourcePins'),(B,'buildPins')]:assert {str(p.relative_to(root)):sha(p) for p in root.rglob('*') if p.is_file()}=={k:v['sha256'] for k,v in bind[key].items()}
changed=[k for k,v in old.items() if v['type']=='file' and v!=expected[k]];assert set(changed)==set(ready['modified']);assert sorted(k for k,v in expected.items() if v['type']=='file' and k not in old)==ready['added']
def backend():
 actual=policy();assert actual==ready['policyBeforeAfter']
 for arc,v in meta['sourceEntries'].items():
  if arc.startswith('runtime230'):p=RT/arc.removeprefix('runtime230').lstrip('/')
  elif arc=='node/bin/node':p=Path.home()/'.nvm/versions/node/v24.15.0/bin/node'
  elif arc=='policy/rach-doi-son-ha.service':p=Path.home()/'.config/systemd/user/rach-doi-son-ha.service'
  elif arc.startswith('policy/rach-doi-son-ha.service.d'):p=Path.home()/'.config/systemd/user/rach-doi-son-ha.service.d'/arc.removeprefix('policy/rach-doi-son-ha.service.d').lstrip('/')
  else:continue
  if v['type']=='symlink':assert p.is_symlink() and os.readlink(p)==v['target'];continue
  assert entry(p)==v,arc
 return actual
def preserve():
 assert cmd('git','rev-parse','HEAD').strip()==head
 for p,pin in canonical.items():assert sha(p)==pin,p
 assert inv(B)==source and sha(ready['archive'])==ready['archiveSHA256'] and sha(ready['rollback'])==ready['rollbackSHA256'];backend()
def dump(n,x):(Q/n).write_text(json.dumps(x,indent=2)+'\n')
backend();preserve();P.mkdir(mode=0o700);dump('source-binding.json',{'head':head,'canonicalBaseline':canonical,'sealed426':bind,'archive432':ready['archiveSHA256'],'rootIntakeSHA256':sha(intake),'old423':old,'candidate433':expected})
libc=ctypes.CDLL(None,use_errno=True);exchange=libc.renameat2;exchange.argtypes=[ctypes.c_int,ctypes.c_char_p,ctypes.c_int,ctypes.c_char_p,ctypes.c_uint];exchange.restype=ctypes.c_int
def swap():
 if exchange(-100,os.fsencode(R/'dist'),-100,os.fsencode(N),2):raise OSError(ctypes.get_errno(),'renameat2 exchange failed')
assert inv(R/'dist')==old;preserve();dump('attempt.json',{'order':433,'authorized':True,'scope':'ONE atomic frontend exchange exact sealed426; no restart'});swap()
try:
 assert inv(R/'dist')==expected and inv(N)==old
 pins={k:v['sha256'] for k,v in expected.items() if v['type']=='file' and (k=='index.html' or k.endswith('.css') or k in ['assets/index-8telBS7h.js','assets/index-DOrSNC3u.js'] or k.startswith('assets/art-v1/'))}
 responses={}
 for rel,want in pins.items():
  with urllib.request.urlopen(urllib.request.Request(BASE+'/'+rel,headers={'Cache-Control':'no-cache'}),timeout=30) as response:
   data=response.read();got=hashlib.sha256(data).hexdigest();assert response.status==200 and got==want,rel;responses[rel]={'status':200,'sha256':got,'bytes':len(data)}
 preserve();dump('receipt.json',{'order':433,'status':'PROMOTED_PUBLIC433_SAME_SEALED426_BACKEND230_UNCHANGED','files':208,'assets':50,'default':'fort','world':True,'candidateArchive432SHA256':ready['archiveSHA256'],'pairedRollback428SHA256':ready['rollbackSHA256'],'rollbackStatus':'VERIFIED423_PLUS230_READY','old423Tree':str(N),'normalTLSPins':responses,'backend':backend(),'sourceHEAD':head,'canonicalNewBaselinePreserved':True,'exchanges':1,'buildBrowserImageRestartCalls':0,'preservationPASS':True,'handles':'CLOSED','pending':'Separate434 actual Firefox; narrow static identities only, full goal remains open'});print('PROMOTED433 exact208/defaultfort50; normalTLS pins '+str(len(responses))+' PASS; backend230 unchanged; CLOSED')
except Exception as e:
 dump('failure.json',{'error':repr(e),'postExchange':True});swap();assert inv(R/'dist')==old;preserve();dump('rollback.json',{'restored423':True,'paired230Unchanged':True,'backendRestarted':False,'handles':'CLOSED'});raise
