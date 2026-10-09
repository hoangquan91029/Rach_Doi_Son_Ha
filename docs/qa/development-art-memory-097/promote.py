from pathlib import Path
import urllib.request,re,hashlib,json,tarfile,shutil,ctypes,os,datetime,subprocess
root=Path.cwd(); out=root/'docs/qa/development-art-memory-097'; stage=Path('/tmp/rdsh-asset-memory-093-hkxkUR');url='https://kieu-hoang-quan-loq-15iax9.tail5247a0.ts.net';sha=lambda b:hashlib.sha256(b).hexdigest()
get=lambda path:urllib.request.urlopen(url+path,timeout=15).read()
health=json.loads(get('/health'));assert health=={'ok':True,'rooms':0},health
service=(out/'service-before.txt').read_text();assert 'MainPID=157023' in service and 'ActiveState=active' in service,service
html=get('/').decode();chunk=re.search(r'/assets/index-[^" ]+\.js',html).group();before=sha(get(chunk));assert before=='f85cdd520aa1fc133fe98eb2542a917600206fa27fa9dd16ca1e591fef3ea3e7',before
assert sha((root/('dist'+chunk)).read_bytes())==before
archive=out/'rollback-dist088-before097.tar.gz'
with tarfile.open(archive,'w:gz') as t:t.add(root/'dist',arcname='dist')
archive.chmod(0o444)
prepared=out/'dist-097-prepared';shutil.copytree(stage/'dist',prepared)
old=[]
for p in (root/'dist').rglob('*'):
 if not p.is_file():continue
 q=prepared/p.relative_to(root/'dist')
 if p.relative_to(root/'dist').parts[0]!='assets':continue
 if q.exists():assert sha(q.read_bytes())==sha(p.read_bytes()),str(q)
 else:q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);old.append(str(p.relative_to(root/'dist')))
rows=[{'path':str(p.relative_to(root/'dist')),'sha256':sha(p.read_bytes())} for p in sorted((root/'dist').rglob('*')) if p.is_file()]
(out/'dist088-pins.json').write_text(json.dumps(rows,indent=2))
assert json.loads(get('/health'))=={'ok':True,'rooms':0}
# Linux renameat2 RENAME_EXCHANGE swaps complete directories without a missing-dist interval.
libc=ctypes.CDLL(None,use_errno=True);fn=libc.renameat2;fn.argtypes=[ctypes.c_int,ctypes.c_char_p,ctypes.c_int,ctypes.c_char_p,ctypes.c_uint];fn.restype=ctypes.c_int
ret=fn(-100,os.fsencode(root/'dist'),-100,os.fsencode(prepared),2)
if ret:raise OSError(ctypes.get_errno(),'renameat2 exchange failed')
prepared.rename(out/'dist088-rollback')
html2=get('/').decode();chunk2=re.search(r'/assets/index-[^" ]+\.js',html2).group();after=sha(get(chunk2));assert after=='e2645a906c9bcceaf0a0882afe9701f6bffaf225d38375e45ebdb7965f3e9d63',after
assert sha(get(chunk))==before
receipt={'status':'PROMOTED_AWAIT_BROWSER','timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'publicURL':url,'beforeChunk':chunk,'beforeSHA':before,'afterChunk':chunk2,'afterSHA':after,'oldAssetsRetained':old,'archiveSHA':sha(archive.read_bytes()),'health':json.loads(get('/health')),'atomic':'renameat2 RENAME_EXCHANGE','restart':False,'service':subprocess.check_output(['systemctl','--user','show','rach-doi-son-ha.service','-p','MainPID','-p','ActiveState','-p','ActiveEnterTimestamp'],text=True)}
(out/'promotion-receipt.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt))
