from pathlib import Path
import json,hashlib,shutil,subprocess,re
from PIL import Image
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');Q=R/'docs/qa/terrain-publicscope-342';S=Path('/tmp/rds-terrain-public342-stage');B=Path('/tmp/rds-terrain-public342-build')
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();inv=lambda p:{str(f.relative_to(p)):h(f) for f in sorted(p.rglob('*')) if f.is_file()};write=lambda n,v:(Q/n).write_text(json.dumps(v,indent=2)+'\n')
assert not S.exists() and not B.exists();assert subprocess.check_output(['git','status','--short'],cwd=R,text=True).strip()=='?? docs/qa/terrain-publicscope-342/'
canonical={n:inv(R/n) for n in ['client','shared','public','server','tests']};oldpublic=inv(R/'dist');assert len(oldpublic)==205;assert oldpublic==json.loads((R/'docs/qa/public-release-309/current-public-pins.json').read_text());old=json.loads((R/'dist/assets/art-v1/fort-202-manifest.json').read_text());assert len(old['assets'])==53;write('before-inventories.json',{'canonical':canonical,'public':oldpublic})
write('work-order.json',{'order':342,'status':'FINITE_PUBLIC_TERRAIN_DERIVATIVE_GO','sourceHEAD':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'maxBuilds':1,'scope':'Exact currentpublic53 plus accepted static rocky338; same terrain340 code. Pending localcollapse321 and food099 excluded; no publicmotion approval inferred. Retain oldchunks. Build/seal only, no productionmutation.'})
S.mkdir()
for n in ['client','shared','public']:shutil.copytree(R/n,S/n)
for n in ['index.html','package.json','package-lock.json','vite.config.js']:shutil.copy2(R/n,S/n)
(S/'node_modules').symlink_to(R/'node_modules',target_is_directory=True)
food=" food:Object.freeze({manifestUrl:'/assets/art-v1/food-099-manifest.json',world:false}),\n";route=(S/'client/art-routes.js').read_text();assert route.count(food)==1;(S/'client/art-routes.js').write_text(route.replace(food,''))
mp=S/'public/assets/art-v1/fort-202-manifest.json';m=json.loads(mp.read_text());assert len(m['assets'])==55 and m['assets'][:53]==old['assets'];rock=m['assets'][54];assert rock['id']=='rocky-ground-338';collapse=m['assets'][53];assert collapse['fortification']['deathSite']=='completed';m['assets']=m['assets'][:53]+[rock];mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
excluded=['assets/art-v1/food-099-manifest.json','assets/art-v1/food-099/atlas.png','assets/art-v1/'+collapse['runtime']['path']]
for n in excluded:(S/'public'/n).unlink()
eclient=canonical['client'].copy();eclient['art-routes.js']=h(S/'client/art-routes.js');epublic={n:v for n,v in canonical['public'].items() if n not in excluded};epublic['assets/art-v1/fort-202-manifest.json']=h(mp)
assert inv(S/'client')==eclient and inv(S/'shared')==canonical['shared'] and inv(S/'public')==epublic
assert S.resolve()==Path('/tmp/rds-terrain-public342-stage') and B.is_absolute() and R not in B.parents;assert h(S/'vite.config.js')==h(R/'vite.config.js')
write('pathassertions.json',{'literalCwd':str(S),'absoluteOutDir':str(B),'exactConfig':str(S/'vite.config.js'),'configSHA256':h(S/'vite.config.js')})
write('source-bindings.json',{'sourceHEAD':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'canonical':canonical,'stage':{n:inv(S/n) for n in ['client','shared','public']},'removedPending':{n:canonical['public'][n] for n in excluded},'removedDescriptor':collapse,'addedDescriptor':rock,'oldPublic':oldpublic,'authorizedDeltas':['client/art-routes.js exact food recipe deletion','fort manifest removes only local pending321 deathSitecompleted descriptor, retains public53 plus static338','three exact pending payload deletions']})
p=subprocess.run([str(S/'node_modules/.bin/vite'),'build','--config','/tmp/rds-terrain-public342-stage/vite.config.js','--outDir','/tmp/rds-terrain-public342-build'],cwd=S,capture_output=True,text=True);(Q/'build.txt').write_text(p.stdout+p.stderr);assert p.returncode==0
for path in (R/'dist/assets').glob('index-*'):
 t=B/'assets'/path.name
 if t.exists():assert h(t)==h(path)
 else:shutil.copy2(path,t)
for a in m['assets']:
 p=B/'assets/art-v1'/a['runtime']['path'];meta=a['runtime'];assert h(p)==meta['sha256'];im=Image.open(p).convert('RGBA');assert list(im.size)==[meta['width'],meta['height']];assert hashlib.sha256(im.tobytes()).hexdigest()==meta['rgbaSha256']
bundle=re.search(r'assets/index-[^" ]+\.js',(B/'index.html').read_text())[0];write('build-binding.json',{'stage':str(S),'build':str(B),'bundlePath':bundle,'bundleSHA256':h(B/bundle),'manifestSHA256':h(B/'assets/art-v1/fort-202-manifest.json'),'indexSHA256':h(B/'index.html')});write('build-pins.json',inv(B));assert {n:inv(R/n) for n in canonical}==canonical and inv(R/'dist')==oldpublic
write('receipt.json',{'status':'SEALED342_PUBLIC_TERRAIN54_NO_PROMOTION','builds':1,'stage':str(S),'build':str(B),'runtimeAssetsEncodedRGBAExact':54,'files':len(inv(B)),'old53RowsUnchanged':True,'pending321And099Absent':True,'canonicalPublicUnchanged':True,'pending':'343 actualFirefox relevant scenes, separate preparation/promotion'})
print(bundle,h(B/bundle))
