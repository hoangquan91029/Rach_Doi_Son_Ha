from pathlib import Path
import json,hashlib,urllib.request,re,subprocess,tarfile,shutil,ctypes,os,datetime
out=Path(__file__).resolve().parent; root=out.parents[2]; stage=out/'source-stage'; url='https://kieu-hoang-quan-loq-15iax9.tail5247a0.ts.net'
a=json.loads((out/'dispatch.json').read_text()); assert a['status']=='AUTHORIZED_FINITE_PUBLIC142'
assert a['rootSceneIntakeStatus']=='ACCEPTED_TERMINAL137'
assert a['localProofStatus']=='PASS_ACTUAL_D1_EPISODE_20IRON_DEPOSIT'
assert a['expectedOldSHA']=='e101219382588201783f2a7afef1a83a0286a66cb22a80b360a92c9e7abcf518'
assert a['expectedIronAssets']==24
pins=json.loads((out/'build-pins.json').read_text()); sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert pins
for rel,h in pins.items(): assert sha(stage/'dist'/rel)==h,(rel,h)
assert not (stage/'dist/assets/art-v1/food-099-manifest.json').exists()
assert not (stage/'dist/assets/art-v1/food-099/atlas.png').exists()
get=lambda path:urllib.request.urlopen(url+path,timeout=15).read()
health=lambda:json.loads(get('/health'))
service=lambda:subprocess.check_output(['systemctl','--user','show','rach-doi-son-ha.service','-p','MainPID','-p','ActiveState'],text=True)
assert health()=={'ok':True,'rooms':0}; s=service(); assert 'MainPID=157023' in s and 'ActiveState=active' in s
chunk=lambda b:re.search(r'/assets/index-[^" ]+\.js',b.decode()).group()
oldchunk=chunk(get('/')); oldsha=hashlib.sha256(get(oldchunk)).hexdigest(); assert oldsha==a['expectedOldSHA']
assert sha(root/('dist'+oldchunk))==oldsha
prepared=out/'dist-prepared'; rollback=out/'dist129-rollback'; archive=out/'rollback-dist129.tar.gz'; assert not any(q.exists() for q in [prepared,rollback,archive])
with tarfile.open(archive,'w:gz') as t:t.add(root/'dist',arcname='dist')
archive.chmod(0o444);shutil.copytree(stage/'dist',prepared);retained=[]
for f in (root/'dist/assets').rglob('*'):
 if f.is_file():
  rel=f.relative_to(root/'dist'); q=prepared/rel
  if q.exists(): assert sha(f)==sha(q),str(rel)
  else:q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,q);retained.append(str(rel))
# Old129 has no pending food-character assets; forbid accidentally retaining them.
assert not (prepared/'assets/art-v1/food-099-manifest.json').exists(); assert not (prepared/'assets/art-v1/food-099/atlas.png').exists()
assert health()=={'ok':True,'rooms':0} and service()==s
lib=ctypes.CDLL(None,use_errno=True); fn=lib.renameat2;fn.argtypes=[ctypes.c_int,ctypes.c_char_p,ctypes.c_int,ctypes.c_char_p,ctypes.c_uint];fn.restype=ctypes.c_int
def exchange():
 if fn(-100,os.fsencode(root/'dist'),-100,os.fsencode(prepared),2): raise OSError(ctypes.get_errno(),'renameat2 exchange')
exchange();status='PROMOTED_AWAIT_BROWSER'
try:
 newchunk=chunk(get('/')); assert newchunk==chunk((stage/'dist/index.html').read_bytes());assert hashlib.sha256(get(newchunk)).hexdigest()==sha(stage/('dist'+newchunk));assert hashlib.sha256(get(oldchunk)).hexdigest()==oldsha;assert service()==s
except BaseException as error:
 exchange(); (out/'promotion-failure.json').write_text(json.dumps({'status':'ROLLED_BACK_HTTP_CHECK_FAILURE','error':repr(error)},indent=2));raise
prepared.rename(rollback)
for q in rollback.rglob('*'):q.chmod(0o555 if q.is_dir() else 0o444)
rollback.chmod(0o555)
(out/'promotion-receipt.json').write_text(json.dumps({'status':status,'oldChunk':oldchunk,'oldSHA':oldsha,'newChunk':newchunk,'newSHA':sha(stage/('dist'+newchunk)),'archiveSHA':sha(archive),'retained':retained,'rooms':health(),'service':s,'restart':False,'atomic':'renameat2 RENAME_EXCHANGE'},indent=2)+'\n')
