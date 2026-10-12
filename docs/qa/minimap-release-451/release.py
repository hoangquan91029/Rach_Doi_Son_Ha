exec(open('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha/docs/qa/minimap-candidate-450/prepare.py').read().split('head=')[0])
import ctypes,urllib.request
Q=R/'docs/qa/minimap-release-451';P=Path.home()/'.local/share/rach-doi-son-ha/releases/451';BASE='https://kieu-hoang-quan-loq-15iax9.tail5247a0.ts.net'
ready=json.loads((R/'docs/qa/minimap-candidate-450/receipt.json').read_text());ff=json.loads((R/'docs/qa/minimap-firefox-448/receipt.json').read_text());backup=json.loads((R/'docs/qa/minimap-rollback-449/receipt.json').read_text())
assert ff['workerStatus']=='PASS_FIREFOX448_SAME_SEALED446' and ff['guards']=='CLOSED';assert backup['handles']=='CLOSED';assert sha(backup['rollbackArchive'])==backup['rollbackSHA256'];assert sha(ready['archive'])==ready['archiveSHA']
head=cmd('git','rev-parse','HEAD').strip();assert head==ready['sourceHEAD'];assert not P.exists() and not (Q/'attempt.json').exists()
old=inv(R/'dist');expected=inv(N);sealed=inv(B);assert expected['.']['mode']==0o755;assert {k:v for k,v in expected.items() if k!='.'}=={k:v for k,v in sealed.items() if k!='.'};assert sum(v['type']=='file' for v in old.values())==208
for name,pin in ready['canonicalPins'].items():assert sha(name)==pin
assert policy()==ready['policy'];before=policy();P.mkdir(mode=0o700)
def preserve():
 assert cmd('git','rev-parse','HEAD').strip()==head
 for name,pin in ready['canonicalPins'].items():assert sha(name)==pin
 assert inv(B)==sealed and sha(ready['archive'])==ready['archiveSHA'] and sha(backup['rollbackArchive'])==backup['rollbackSHA256'];assert policy()==before
preserve();dump(Q/'source-binding.json',{'sourceHEAD':head,'old433':old,'new446':expected,'candidateArchive':ready['archiveSHA'],'pairedRollback433230':backup['rollbackSHA256'],'firefoxRequiredPins':ff['requiredPins']})
libc=ctypes.CDLL(None,use_errno=True);exchange=libc.renameat2;exchange.argtypes=[ctypes.c_int,ctypes.c_char_p,ctypes.c_int,ctypes.c_char_p,ctypes.c_uint];exchange.restype=ctypes.c_int
def swap():
 if exchange(-100,os.fsencode(R/'dist'),-100,os.fsencode(N),2):raise OSError(ctypes.get_errno(),'atomic exchange failed')
dump(Q/'attempt.json',{'authorized':True,'scope':'ONE client-only atomic exchange exact446 build; all browser guards closed; no restart/art changes'});swap()
try:
 assert inv(R/'dist')==expected and inv(N)==old
 responses={}
 for rel in ['index.html','assets/index-CU9fIOQr.js','assets/index-Dx0ueiQl.css','assets/art-v1/fort-202-manifest.json']:
  with urllib.request.urlopen(urllib.request.Request(BASE+'/'+rel,headers={'Cache-Control':'no-cache'}),timeout=30) as r:
   data=r.read();pin=hashlib.sha256(data).hexdigest();assert r.status==200 and pin==expected[rel]['sha256'];responses[rel]={'sha256':pin,'status':200,'bytes':len(data)}
 preserve();dump(Q/'receipt.json',{'status':'PROMOTED_PUBLIC451_MINIMAP446_BACKEND230_UNCHANGED','sourceHEAD':head,'files':209,'assets':50,'scope':'Index/newJS only; every old image/manifest/chunk exact; no new art or motion acceptance.','normalTLSPins':responses,'pairedRollback':backup['rollbackArchive'],'pairedRollbackSHA':backup['rollbackSHA256'],'old433Tree':str(N),'policy':before,'canonicalPreserved':True,'exchanges':1,'restartCalls':0,'guards':'CLOSED','pending':'One relevant public browser minimap smoke; full goal INCOMPLETE'});print('PROMOTED451209files;4normalTLSpins;immutable230unchanged;CLOSED')
except Exception as e:
 dump(Q/'failure.json',{'error':repr(e)});swap();assert inv(R/'dist')==old;preserve();dump(Q/'rollback.json',{'restored433':True,'unchangedBackend230':True,'restartCalls':0,'guards':'CLOSED'});raise
