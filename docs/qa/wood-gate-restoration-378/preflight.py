exec(open('docs/qa/wood-gate-restoration-378/prepare.py').read().split('assert not S.exists()')[0])
b=json.loads((Q/'preservation-before.json').read_text());assert all(inv(R/n)==v for n,v in b['canonical'].items());assert inv(Path.home()/'.local/share/rach-doi-son-ha/releases/230/runtime230')==b['runtime'];assert H(S/'vite.config.js')==H(R/'vite.config.js')
p=S/'client/art-routes.js';t=p.read_text();assert " food:Object.freeze({manifestUrl:'/assets/art-v1/food-099-manifest.json',world:false}),\n" in t;p.write_text(t.replace(" food:Object.freeze({manifestUrl:'/assets/art-v1/food-099-manifest.json',world:false}),\n",''))
removed=[]
for rel in ['public/assets/art-v1/food-099-manifest.json','public/assets/art-v1/villager-food-101/atlas.png']:
 p=S/rel;assert p.exists();removed.append({'path':rel,'sha256':H(p)});p.unlink()
retained=[]
for p in sorted((R/'dist/assets').glob('index-*')):
 if p.suffix not in ['.js','.css']:continue
 dst=S/'public/assets'/p.name;shutil.copy2(p,dst);retained.append({'path':str(dst.relative_to(S)),'sha256':H(p)})
for name,count in [('stone-361-manifest.json',16),('fort-202-manifest.json',45)]:
 old=json.loads((R/'public/assets/art-v1'/name).read_text());new=json.loads((S/'public/assets/art-v1'/name).read_text());assert new['assets'][:len(old['assets'])]==old['assets'];assert len(new['assets'])==count;assert len([a for a in new['assets'] if a['family']=='building.gate'])==7
 for a in new['assets']:
  if a['family']=='building.gate':assert a['material']=='wood';assert H(S/'public/assets/art-v1'/a['runtime']['path'])==a['runtime']['sha256'];assert H(R/a['source']['path'])==a['source']['sha256']
assert inv(S/'shared')==inv(R/'shared')
(Q/'candidate-source-inventory.json').write_text(json.dumps(inv(S),indent=2));(Q/'preflight.json').write_text(json.dumps({'status':'PASS378_BEFORE_ONE_BUILD','literalCWD':str(S),'absoluteOutDir':str(B),'viteConfigSHA256':H(S/'vite.config.js'),'defaultCount':16,'fortCount':45,'gateRows':7,'gatePNGs':2,'sourceAndRuntimePinsExact':True,'oldRowsPreserved':True,'canonicalPreserved':True,'publicationOnlyExclusions':removed,'retainedCurrent367ChunksCSS':retained,'contractsPass':16,'imageCalls':0},indent=2))
