from pathlib import Path
import shutil,json,hashlib,subprocess,urllib.request
from PIL import Image
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');O=R/'docs/qa/initial-actors-runtime-399';S=Path('/tmp/rds-actors399-stage');B=Path('/tmp/rds-actors399-build')
def inv(p):return {str(f.relative_to(p)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(p.rglob('*')) if f.is_file() and not f.is_symlink()}
def preserve():return {'HEAD':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'canonical':{n:inv(R/n) for n in ['client','shared','server','public']},'public':inv(R/'dist'),'backend':inv(Path('/home/kieu-hoang-quan/.local/share/rach-doi-son-ha/releases/230/runtime230')),'pid':Path('/proc/3229/cmdline').read_bytes().hex(),'health':json.load(urllib.request.urlopen('http://127.0.0.1:3000/health'))}
p=preserve();assert p['HEAD']=='63705a6c43b0f9e5ad4d18d58157a893cb62a6ab';assert p['health']=={'ok':True,'rooms':0};assert len(p['public'])==201;assert not S.exists() and not B.exists();(O/'preservation-before.json').write_text(json.dumps(p,indent=2))
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
mf=S/'public/assets/art-v1/fort-202-manifest.json';m=json.loads(mf.read_text());old=json.loads(mf.read_text())['assets'];assert len(old)==45
rows=[]
for family,d,source,runtime,name,size,shadow,candidate in [('tran_nhan_tong','docs/art/characters/tran-nhan-tong-idle-396','working256.png','runtime.png','king396.png',42,'baked','candidate.json'),('spearman','docs/art/units/spearman-margin-400','spearman-idle-d0-256.png','spearman-idle-d0-128.png','spearman400.png',42,'separate','asset-candidate.json'),('wagon','docs/art/units/supply-wagon-idle-398','working-256.png','runtime-128.png','wagon398.png',55,'baked',None)]:
 a=json.loads((R/d/candidate).read_text()) if candidate else {'id':'wagon-idle-d0-398','family':'unit.wagon','kind':'unit','state':'idle','direction':0}
 for key,filename,expected in [('source',source,256),('runtime',runtime,128)]:
  path=R/d/filename;im=Image.open(path);assert im.size==(expected,expected);assert im.mode=='RGBA';a[key]={'path':str(Path(d)/filename) if key=='source' else 'initial-actors-399/'+name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'rgbaSha256':hashlib.sha256(im.tobytes()).hexdigest(),'width':expected,'height':expected}
 a.update(candidate=True,review={'status':'CANDIDATE'},cell={'width':128,'height':128},pivot={'x':654/1254*256,'y':1140/1254*256,'space':'source'},render={'width':size,'height':size},alphaPolicy='transparent',contactShadow={'mode':shadow,**({'assetId':'unit-contact-shadow'} if shadow=='separate' else {})},frames=[{'x':0,'y':0,'width':128,'height':128,'durationMs':1000}],loop=True)
 t=S/'public/assets/art-v1'/a['runtime']['path'];t.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/d/runtime,t);rows.append(a)
m['assets']+=rows;assert m['assets'][:45]==old;mf.write_text(json.dumps(m,indent=2)+'\n');(O/'selected-binding.json').write_text(json.dumps({'assets':rows,'held397Selected':False,'staticOnly':True},indent=2)+'\n')
assert preserve()==p
pre={'status':'PASS_PREBUILD399','cwd':str(S),'outDir':str(B),'config':str(S/'vite.config.js'),'configSHA':hashlib.sha256((S/'vite.config.js').read_bytes()).hexdigest(),'assets':48,'old45Verbatim':True,'retainedPublicFiles':201,'intendedDataDelta':['fort-202-manifest.json','king396.png','spearman400.png','wagon398.png'],'foodExcluded':True}
(O/'preflight.json').write_text(json.dumps(pre,indent=2));(O/'stage-inventory.json').write_text(json.dumps(inv(S),indent=2));print(json.dumps(pre))
