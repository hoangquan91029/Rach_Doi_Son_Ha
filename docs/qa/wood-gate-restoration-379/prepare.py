from pathlib import Path
import json,shutil,hashlib,subprocess
R=Path.cwd();Q=R/'docs/qa/wood-gate-restoration-379';S=Path('/tmp/rds-gates379-stage');B=Path('/tmp/rds-gates379-build');H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def inv(p):return {str(f.relative_to(p)):H(f) for f in sorted(p.rglob('*')) if f.is_file() and 'node_modules' not in f.parts}
assert not S.exists() and not B.exists();assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()=='e042f0e97e9066c2c25ef7828657631963db593f'
b={'canonical':{n:inv(R/n) for n in ['client','shared','public','dist']},'runtime':inv(Path.home()/'.local/share/rach-doi-son-ha/releases/230/runtime230'),'HEAD':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()};(Q/'preservation-before.json').write_text(json.dumps(b,indent=2))
S.mkdir()
for n in ['client','shared','public','tests']:shutil.copytree(R/n,S/n)
for n in ['index.html','package.json','vite.config.js']:shutil.copy2(R/n,S/n)
(S/'node_modules').symlink_to(R/'node_modules',target_is_directory=True)
for p in (R/'docs/qa/wood-gate-restoration-378/source-copies').rglob('*'):
 if p.is_file():dst=S/p.relative_to(R/'docs/qa/wood-gate-restoration-378/source-copies');dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dst)
p=S/'client/art-routes.js';t=p.read_text();recipe=" food:Object.freeze({manifestUrl:'/assets/art-v1/food-099-manifest.json',world:false}),\n";assert recipe in t;p.write_text(t.replace(recipe,''))
removed=[]
for rel in ['public/assets/art-v1/food-099-manifest.json','public/assets/art-v1/food-099/atlas.png']:
 p=S/rel;assert p.exists();removed.append({'path':rel,'sha256':H(p)});p.unlink()
retained=[]
for p in sorted((R/'dist/assets').glob('index-*')):
 if p.suffix not in ['.js','.css']:continue
 dst=S/'public/assets'/p.name;shutil.copy2(p,dst);retained.append({'path':str(dst.relative_to(S)),'sha256':H(p)})
for name,count in [('stone-361-manifest.json',16),('fort-202-manifest.json',45)]:
 old=json.loads((R/'public/assets/art-v1'/name).read_text());new=json.loads((S/'public/assets/art-v1'/name).read_text());assert new['assets'][:len(old['assets'])]==old['assets'];assert len(new['assets'])==count;assert len([a for a in new['assets'] if a['family']=='building.gate'])==7
 for a in new['assets']:
  if a['family']=='building.gate':assert a['material']=='wood';assert H(S/'public/assets/art-v1'/a['runtime']['path'])==a['runtime']['sha256'];assert H(R/a['source']['path'])==a['source']['sha256']
assert inv(S/'shared')==inv(R/'shared');assert all(inv(R/n)==v for n,v in b['canonical'].items());assert H(S/'vite.config.js')==H(R/'vite.config.js')
(Q/'candidate-source-inventory.json').write_text(json.dumps(inv(S),indent=2));(Q/'preflight.json').write_text(json.dumps({'status':'PASS379_BEFORE_ONE_BUILD','literalCWD':str(S),'absoluteOutDir':str(B),'viteConfigSHA256':H(S/'vite.config.js'),'defaultCount':16,'fortCount':45,'gateRows':7,'gatePNGs':2,'sourceAndRuntimePinsExact':True,'oldRowsPreserved':True,'canonicalPreserved':True,'publicationOnlyExclusions':removed,'retainedCurrent367ChunksCSS':retained,'imageCalls':0},indent=2));print('PASS379_BEFORE_BUILD')
