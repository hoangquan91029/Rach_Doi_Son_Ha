from pathlib import Path
import json,hashlib,shutil,subprocess,re
from PIL import Image
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');Q=R/'docs/qa/wall-collapse-trial-318';S=Path('/tmp/rds-wall-collapse318-stage');B=Path('/tmp/rds-wall-collapse318-build');A=R/'docs/art/buildings/wall-collapse-preview-321/export'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inv=lambda p:{str(f.relative_to(p)):h(f) for f in sorted(p.rglob('*')) if f.is_file()}
write=lambda n,v:(Q/n).write_text(json.dumps(v,indent=2)+'\n')
assert not S.exists() and not B.exists()
canonical={n:inv(R/n) for n in ['client','shared','public','server','tests']};public=inv(R/'dist');preserved317=inv(R/'docs/qa/wall-collapse-combat-prep-317');write('before-inventories.json',dict(canonical=canonical,public=public,preserved317=preserved317))
old=json.loads((R/'public/assets/art-v1/fort-202-manifest.json').read_text());assert len(old['assets'])==53;assert old==json.loads((R/'dist/assets/art-v1/fort-202-manifest.json').read_text())
write('baseline-manifest.json',old)
S.mkdir()
for n in ['client','shared','public']:shutil.copytree(R/n,S/n)
for n in ['index.html','package.json','package-lock.json','vite.config.js']:shutil.copy2(R/n,S/n)
(S/'node_modules').symlink_to(R/'node_modules',target_is_directory=True)
food=" food:Object.freeze({manifestUrl:'/assets/art-v1/food-099-manifest.json',world:false}),\n";route=(S/'client/art-routes.js').read_text();assert route.count(food)==1;(S/'client/art-routes.js').write_text(route.replace(food,''))
excluded=['assets/art-v1/food-099-manifest.json','assets/art-v1/food-099/atlas.png']
for n in excluded:(S/'public'/n).unlink()
a=json.loads((A/'manifest.json').read_text())['assets'][0];a['runtime']['path']='runtime/wall-collapse-321-atlas.png';shutil.copy2(A/'atlas.png',S/'public/assets/art-v1'/a['runtime']['path'])
rows=[i for i,v in enumerate(old['assets']) if v.get('family')=='building.wall' and v.get('state')=='death' and v.get('fortification')=={'mask':0}];assert len(rows)==1;idx=rows[0];candidate=json.loads(json.dumps(old));candidate['assets'][idx]=a
(S/'public/assets/art-v1/fort-202-manifest.json').write_text(json.dumps(candidate,indent=2)+'\n');assert len(candidate['assets'])==53 and [v for i,v in enumerate(candidate['assets']) if i!=idx]==[v for i,v in enumerate(old['assets']) if i!=idx]
expectedclient=canonical['client'].copy();expectedclient['art-routes.js']=h(S/'client/art-routes.js');assert inv(S/'client')==expectedclient and inv(S/'shared')==canonical['shared']
expectedpublic={n:v for n,v in canonical['public'].items() if n not in excluded};expectedpublic['assets/art-v1/fort-202-manifest.json']=h(S/'public/assets/art-v1/fort-202-manifest.json');expectedpublic['assets/art-v1/'+a['runtime']['path']]=h(S/'public/assets/art-v1'/a['runtime']['path']);assert inv(S/'public')==expectedpublic
assert S.resolve()==Path('/tmp/rds-wall-collapse318-stage') and B==Path('/tmp/rds-wall-collapse318-build') and B.is_absolute() and R not in B.parents and S not in B.parents;assert h(S/'vite.config.js')==h(R/'vite.config.js')
write('prebuild-pathassertions.json',dict(literalCwd=str(S),absoluteOutDir=str(B),exactConfig=str(S/'vite.config.js'),configSHA256=h(S/'vite.config.js')))
p=subprocess.run([str(S/'node_modules/.bin/vite'),'build','--config','/tmp/rds-wall-collapse318-stage/vite.config.js','--outDir','/tmp/rds-wall-collapse318-build'],cwd='/tmp/rds-wall-collapse318-stage',capture_output=True,text=True);(Q/'build.txt').write_text(p.stdout+p.stderr);assert p.returncode==0
for file in (R/'dist/assets').glob('index-*'):
 dest=B/'assets'/file.name
 if dest.exists():assert h(dest)==h(file)
 else:shutil.copy2(file,dest)
for v in candidate['assets']:
 file=B/'assets/art-v1'/v['runtime']['path'];assert h(file)==v['runtime']['sha256'];im=Image.open(file).convert('RGBA');assert list(im.size)==[v['runtime']['width'],v['runtime']['height']];assert hashlib.sha256(im.tobytes()).hexdigest()==v['runtime']['rgbaSha256']
for n,v in public.items():
 if n.startswith('assets/index-') or n.startswith('assets/art-v1/') and n not in excluded and n!='assets/art-v1/fort-202-manifest.json':assert h(B/n)==v
for n in excluded:assert not (B/n).exists()
ledger=json.loads((A/'frame-source-ledger.json').read_text());custody=[]
for record in ledger['frames']:
 for key in ['source','originalRaw','toolReceipt','selectionReceipt']:
  v=record[key];assert h(Path(v['path']))==v['sha256'];custody.append(dict(path=v['path'],sha256=v['sha256']))
for file in [A/'manifest.json',A/'atlas.png',A/'frame-source-ledger.json',R/'docs/art/buildings/wall-collapse-preview-321/receipt.json']:
 assert file.is_file();custody.append(dict(path=str(file),sha256=h(file)))
sourcepins={}
for n in ['client','shared','public']:
 sourcepins.update({n+'/'+p:v for p,v in inv(S/n).items()})
for n in ['index.html','package.json','package-lock.json','vite.config.js']:sourcepins[n]=h(S/n)
bundle=re.search(r'assets/index-[^" ]+\.js',(B/'index.html').read_text())[0]
binding=json.loads((R/'docs/qa/wall-collapse-combat-prep-317/binding.json').read_text());binding.update(status='SEALED_PREFLIGHT_WAIT_ROOT_LAUNCH_GO',rootAuthorized=True,runGO=False,sourcePins=sourcepins,buildPins=inv(B),baselineManifestPath=str(Q/'baseline-manifest.json'),baselineManifestSHA256=h(Q/'baseline-manifest.json'),candidateManifestPath=str(B/'assets/art-v1/fort-202-manifest.json'),candidateManifestSHA256=h(B/'assets/art-v1/fort-202-manifest.json'),oldDeathAssetId=old['assets'][idx]['id'],deathAssetId=a['id'],frameSourcePins=[dict(path=f['source']['path'],sha256=f['source']['sha256']) for f in a['frames']],adapterLedgerPath=str(A/'frame-source-ledger.json'),adapterLedgerSHA256=h(A/'frame-source-ledger.json'),custodyPins=custody,bundlePath=bundle)
write('binding.json',binding);assert {n:inv(R/n) for n in canonical}==canonical and inv(R/'dist')==public and inv(R/'docs/qa/wall-collapse-combat-prep-317')==preserved317
write('preflight.json',dict(status='PASS_SEALED_WAIT_ROOT_LAUNCH_GO',builds=1,descriptors=53,unchangedRows=52,exactEncodedDecodedAssets=53,retainedOldChunks=True,retainedOld292=True,foodExcludedOnly=excluded,bundlePath=bundle,bundleSHA256=h(B/bundle),manifestSHA256=h(B/'assets/art-v1/fort-202-manifest.json'),indexSHA256=h(B/'index.html'),sourceInventorySHA256=h(Q/'binding.json'),canonicalPublicBackendFilesUnchanged=True,original317Preserved=True,browserCalls=0,serverStarted=False))
print(json.dumps(json.loads((Q/'preflight.json').read_text()),indent=2))
