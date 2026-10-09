"""Future finite145 rollback; restores entire142 tree, no service restart."""
from pathlib import Path
import json,hashlib,urllib.request,subprocess,ctypes,os
out=Path(__file__).resolve().parent; root=out.parents[2]
a=json.loads((out/'dispatch.json').read_text()); assert a['status']=='AUTHORIZED_FINITE_PUBLIC145'
p=json.loads((out/'promotion-receipt.json').read_text()); assert p['status']=='PROMOTED_AWAIT_BROWSER'
assert p['oldSHA']==a['expectedOldSHA']
url='https://kieu-hoang-quan-loq-15iax9.tail5247a0.ts.net'
get=lambda path:urllib.request.urlopen(url+path,timeout=15).read()
assert json.loads(get('/health'))=={'ok':True,'rooms':0}
s=subprocess.check_output(['systemctl','--user','show','rach-doi-son-ha.service','-p','MainPID','-p','ActiveState'],text=True)
assert 'MainPID=157023' in s and 'ActiveState=active' in s
old=out/'dist142-rollback'; assert old.is_dir()
sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha((old/p['oldChunk'].lstrip('/')).read_bytes())==p['oldSHA']
assert sha(get(p['newChunk']))==p['newSHA']
lib=ctypes.CDLL(None,use_errno=True); fn=lib.renameat2
fn.argtypes=[ctypes.c_int,ctypes.c_char_p,ctypes.c_int,ctypes.c_char_p,ctypes.c_uint]; fn.restype=ctypes.c_int
if fn(-100,os.fsencode(root/'dist'),-100,os.fsencode(old),2): raise OSError(ctypes.get_errno(),'renameat2 rollback exchange')
assert sha(get(p['oldChunk']))==p['oldSHA']
assert get('/')==(root/'dist/index.html').read_bytes()
(out/'rollback-receipt.json').write_text(json.dumps({'status':'FULL142_TREE_RESTORED','restart':False,'oldSHA':p['oldSHA'],'failed145Tree':str(old),'service':s},indent=2)+'\n')
