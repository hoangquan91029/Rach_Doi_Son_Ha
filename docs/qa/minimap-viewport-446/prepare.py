from pathlib import Path
import shutil,hashlib,json,subprocess
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');O=R/'docs/qa/minimap-viewport-446';S=Path('/tmp/rds-minimap446-stage');B=Path('/tmp/rds-minimap446-build')
def inventory(p):return {str(f.relative_to(p)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(p.rglob('*')) if f.is_file() and not f.is_symlink()}
def protected():return {'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'source':{n:inventory(R/n) for n in ['client','shared','server','public']},'dist':inventory(R/'dist'),'backend':inventory(Path('/home/kieu-hoang-quan/.local/share/rach-doi-son-ha/releases/230/runtime230'))}
assert not S.exists() and not B.exists();before=protected();(O/'preservation-before.json').write_text(json.dumps(before,indent=2));S.mkdir()
for n in ['client','shared','server','public']:shutil.copytree(R/n,S/n)
for n in ['index.html','vite.config.js','package.json','package-lock.json']:shutil.copy2(R/n,S/n)
(S/'node_modules').symlink_to(R/'node_modules',target_is_directory=True)
p=S/'client/art-routes.js';s=p.read_text();line=" food:Object.freeze({manifestUrl:'/assets/art-v1/food-099-manifest.json',world:false}),\n";assert line in s;p.write_text(s.replace(line,''))
for n in ['assets/art-v1/food-099-manifest.json','assets/art-v1/food-099/atlas.png']:(S/'public'/n).unlink()
for rel,pin in before['dist'].items():
 if rel=='index.html':continue
 p=S/'public'/rel
 if p.exists():assert hashlib.sha256(p.read_bytes()).hexdigest()==pin,rel
 else:p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/'dist'/rel,p)
assert protected()==before
r={'status':'PASS_PREBUILD','stage':str(S),'build':str(B),'config':str(S/'vite.config.js'),'configSHA':hashlib.sha256((S/'vite.config.js').read_bytes()).hexdigest(),'stagePins':{n:inventory(S/n) for n in ['client','shared','server','public']},'scope':'446 minimap ground footprint only; no image calls/art/simulation changes; public433 retained; local food excluded from stage as current release.'}
(O/'preflight.json').write_text(json.dumps(r,indent=2));print(json.dumps({k:r[k] for k in ['status','stage','build','config','configSHA','scope']}))
