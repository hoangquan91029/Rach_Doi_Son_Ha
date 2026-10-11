from pathlib import Path
import shutil,json,hashlib,subprocess,urllib.request
from PIL import Image
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');O=R/'docs/qa/horse-wagon-runtime-420';S=Path('/tmp/rds-horsewagon420-stage');B=Path('/tmp/rds-horsewagon420-build')
def inv(p):return {str(f.relative_to(p)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(p.rglob('*')) if f.is_file() and not f.is_symlink()}
def preserve():return {'HEAD':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'canonical':{n:inv(R/n) for n in ['client','shared','server','public']},'public':inv(R/'dist'),'backend':inv(Path('/home/kieu-hoang-quan/.local/share/rach-doi-son-ha/releases/230/runtime230')),'pid':Path('/proc/3229/cmdline').read_bytes().hex(),'health':json.load(urllib.request.urlopen('http://127.0.0.1:3000/health'))}
p=preserve();assert p['HEAD']=='3a2ab48917d7fb7f3b50858e983037f4dbd44d5f';assert p['health']=={'ok':True,'rooms':0};assert len(p['public'])==206;assert not S.exists() and not B.exists();(O/'preservation-before.json').write_text(json.dumps(p,indent=2))
S.mkdir()
for n in ['client','shared','server','public','tests']:shutil.copytree(R/n,S/n)
for n in ['index.html','vite.config.js','package.json','package-lock.json']:shutil.copy2(R/n,S/n)
(S/'node_modules').symlink_to(R/'node_modules',target_is_directory=True)
f=S/'client/art-routes.js';v=f.read_text();line=" food:Object.freeze({manifestUrl:'/assets/art-v1/food-099-manifest.json',world:false}),\n";assert line in v;f.write_text(v.replace(line,''))
for n in ['assets/art-v1/food-099-manifest.json','assets/art-v1/food-099/atlas.png']:(S/'public'/n).unlink()
for rel,pin in p['public'].items():
 if rel in ['index.html','assets/art-v1/fort-202-manifest.json']:continue
 t=S/'public'/rel
 if t.exists():assert hashlib.sha256(t.read_bytes()).hexdigest()==pin,rel
 else:t.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/'dist'/rel,t)
mf=S/'public/assets/art-v1/fort-202-manifest.json';m=json.loads(mf.read_text());old=json.loads(mf.read_text())['assets'];assert len(old)==50
rows=[]
for family,d,source,runtime,name,size,shadow,candidate in [('wagon','docs/art/units/supply-wagon-horse-415','working-256.png','runtime-128.png','idle.png',112,'baked','descriptor.json')]:
 a=json.loads((R/d/candidate).read_text()) if candidate else {'id':'wagon-idle-d0-398','family':'unit.wagon','kind':'unit','state':'idle','direction':0}
 for key,filename,expected in [('source',source,256),('runtime',runtime,128)]:
  path=R/d/filename;im=Image.open(path);assert im.size==(expected,expected);assert im.mode=='RGBA';a[key]={'path':str(Path(d)/filename) if key=='source' else 'wagon-horse-420/'+name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'rgbaSha256':hashlib.sha256(im.tobytes()).hexdigest(),'width':expected,'height':expected}
 a['runtime']['derivation']={'method':'resize','filter':'lanczos','sourceSha256':a['source']['sha256']}
 a.update(candidate=True,review={'status':'CANDIDATE'},cell={'width':128,'height':128},pivot={'x':654/1254*256,'y':1140/1254*256,'space':'source'},render={'width':size,'height':size},alphaPolicy='transparent',contactShadow={'mode':shadow,**({'assetId':'unit-contact-shadow'} if shadow=='separate' else {})},frames=[{'x':0,'y':0,'width':128,'height':128,'durationMs':1000}],loop=True)
 t=S/'public/assets/art-v1'/a['runtime']['path'];t.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/d/runtime,t);rows.append(a)
indices=[i for i,a in enumerate(old) if a['id']=='wagon-idle-d0-398'];assert len(indices)==1;idx=indices[0];m['assets'][idx]=rows[0];assert all(a==old[i] for i,a in enumerate(m['assets']) if i!=idx);assert len(m['assets'])==50;mf.write_text(json.dumps(m,indent=2)+'\n');(O/'selected-binding.json').write_text(json.dumps({'assets':rows,'staticOnly':True},indent=2)+'\n')
assert preserve()==p
pre={'status':'PASS_PREBUILD420_WAIT_ROOT_BUILD','cwd':str(S),'outDir':str(B),'config':str(S/'vite.config.js'),'configSHA':hashlib.sha256((S/'vite.config.js').read_bytes()).hexdigest(),'assets':50,'other49Verbatim':True,'old398PayloadPreserved':True,'retainedPublicFiles':206,'intendedDataDelta':['fort-202-manifest.json','wagon-horse-420/idle.png'],'foodExcluded':True}
(O/'preflight.json').write_text(json.dumps(pre,indent=2));(O/'stage-inventory.json').write_text(json.dumps(inv(S),indent=2));print(json.dumps(pre))
