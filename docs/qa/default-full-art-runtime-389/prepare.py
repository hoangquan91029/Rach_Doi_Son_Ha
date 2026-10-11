from pathlib import Path
import shutil,json,hashlib,subprocess,urllib.request,os
root=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');out=root/'docs/qa/default-full-art-runtime-389';stage=Path('/tmp/rds-fullart389-stage');build=Path('/tmp/rds-fullart389-build');runtime=Path('/home/kieu-hoang-quan/.local/share/rach-doi-son-ha/releases/230/runtime230')
def inv(base):
 return {str(p.relative_to(base)):{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'mode':oct(p.stat().st_mode&0o777)} for p in sorted(base.rglob('*')) if p.is_file() and not p.is_symlink()}
def preservation():
 return {'HEAD':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'canonical':{n:inv(root/n) for n in ['client','shared','server','public']},'public':inv(root/'dist'),'runtime':{n:inv(runtime/n) for n in ['server','shared']},'pid3229':Path('/proc/3229/cmdline').read_bytes().decode().replace('\0',' '),'health':json.load(urllib.request.urlopen('http://127.0.0.1:3000/health'))}
assert not stage.exists() and not build.exists()
before=preservation();assert before['HEAD']=='2b16979393716bc056e205f8fc50eaea07db0593';assert before['health']=={'ok':True,'rooms':0};assert len(before['public'])==200
(out/'preservation-before.json').write_text(json.dumps(before,indent=2)+'\n')
stage.mkdir()
for n in ['client','shared','server','public','tests']:shutil.copytree(root/n,stage/n)
for n in ['index.html','vite.config.js','package.json','package-lock.json']:shutil.copy2(root/n,stage/n)
(stage/'node_modules').symlink_to(root/'node_modules',target_is_directory=True)
# Only withheld food recipe/payload excluded from publication source.
routes=stage/'client/art-routes.js';s=routes.read_text();line=" food:Object.freeze({manifestUrl:'/assets/art-v1/food-099-manifest.json',world:false}),\n";assert line in s;routes.write_text(s.replace(line,''))
for n in ['assets/art-v1/food-099-manifest.json','assets/art-v1/food-099/atlas.png']:(stage/'public'/n).unlink()
for rel,data in before['public'].items():
 if rel=='index.html':continue
 target=stage/'public'/rel
 if target.exists():assert hashlib.sha256(target.read_bytes()).hexdigest()==data['sha256'],rel
 else:target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(root/'dist'/rel,target)
assert preservation()==before
m=json.loads((stage/'public/assets/art-v1/fort-202-manifest.json').read_text());assert len(m['assets'])==45
for a in m['assets']:assert hashlib.sha256((stage/'public/assets/art-v1'/a['runtime']['path']).read_bytes()).hexdigest()==a['runtime']['sha256'],a['id']
pre={'status':'PASS389_BEFORE_ONE_BUILD','literalCWD':str(stage),'absoluteOutDir':str(build),'viteConfigSHA256':hashlib.sha256((stage/'vite.config.js').read_bytes()).hexdigest(),'default':'fort','world':True,'assets':45,'public382retained':199,'onlyExclusions':['food route','food-099-manifest.json','food-099/atlas.png'],'sourceRuntimePinsExact':True,'preservationExact':True}
(out/'preflight.json').write_text(json.dumps(pre,indent=2)+'\n')
(out/'stage-inventory.json').write_text(json.dumps(inv(stage),indent=2)+'\n')
print(json.dumps(pre))
