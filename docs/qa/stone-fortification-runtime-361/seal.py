from pathlib import Path
import json,hashlib,sys,shutil
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');Q=R/'docs/qa/stone-fortification-runtime-361';S=Path('/tmp/rds-stone361-stage');B=Path('/tmp/rds-stone361-build');L=Path.home()/'.local/share/rach-doi-son-ha/releases/230/runtime230';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def inv(p):return {str(f.relative_to(p)):H(f) for f in sorted(p.rglob('*')) if f.is_file() and 'node_modules' not in f.parts}
def preserved():
 p=json.loads((Q/'preservation-before.json').read_text());return all(inv(R/n)==v for n,v in p['canonical'].items()) and inv(R/'dist')==p['public'] and inv(Path('/tmp/rds-terrain-public342-stage'))==p['base342'] and inv(L)==p['runtime']
mode=sys.argv[1]
if mode=='prebuild':
 assert S.resolve()==S and B.resolve()==B and not B.exists() and S!=R and B!=R/'dist';assert H(S/'vite.config.js')==H(Path('/tmp/rds-terrain-public342-stage/vite.config.js'));assert preserved()
 before=json.loads((Q/'source-inventory.json').read_text());now=inv(S);removed={k for k in before if k not in now};ret=json.loads((Q/'retired-payload-removal.json').read_text());assert removed=={x['stageRelativePath'] for x in ret['files']}
 changed={k for k in set(before)|set(now) if before.get(k)!=now.get(k)};assert changed==removed|{'client/renderer.js','client/stone-fortification.js','client/fortification-picking.js','client/art-routes.js','public/assets/art-v1/stone-361-manifest.json','public/assets/art-v1/fort-202-manifest.json','public/assets/art-v1/stone-wall-X-362/runtime.png','public/assets/art-v1/stone-wall-Y-364/runtime.png','public/assets/art-v1/stone-wall-corner-365/runtime.png'}
 selected=json.loads((Q/'selected-stone366.json').read_text());assert H(Path(selected['bindingPath']))==selected['bindingSHA256']
 for item in selected['sourceBindings']:
  for kind in ['source','runtime']:assert H(R/item['directory']/item[kind]['path'])==item[kind]['sha256']
 (Q/'preflight.json').write_text(json.dumps({'status':'PASS361_PREBUILD_ALL_RETENTION_SOURCEBINDING_CONFIG_PATH_ASSERTIONS','literalCWD':str(S),'absoluteOutDir':str(B),'exactViteConfig':str(S/'vite.config.js'),'viteConfigSHA256':H(S/'vite.config.js'),'changedSourceFiles':sorted(changed),'removedExact15':sorted(removed),'descriptors':37,'sourceBindings':3,'rootFiniteGO':True,'buildsAuthorized':1,'browserCampaignsAuthorized':1,'canonicalPreserved':True},indent=2)+'\n')
 (Q/'candidate-source-inventory.json').write_text(json.dumps(now,indent=2)+'\n')
 for p in ['client/renderer.js','client/stone-fortification.js','client/fortification-picking.js','client/art-routes.js','public/assets/art-v1/stone-361-manifest.json','public/assets/art-v1/fort-202-manifest.json']:
  d=Q/'source-copies'/p;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(S/p,d)
elif mode=='seal':
 assert preserved();assert inv(S)==json.loads((Q/'candidate-source-inventory.json').read_text());assert H(S/'vite.config.js')==json.loads((Q/'preflight.json').read_text())['viteConfigSHA256'];assert len(json.loads((B/'assets/art-v1/fort-202-manifest.json').read_text())['assets'])==37
 seal={'status':'SEALED_STONE361_BEFORE_BROWSER','stage':inv(S),'build':inv(B),'bindingSHA256':H(Q/'selected-stone366.json'),'contractsSHA256':H(Q/'contracts-result.txt'),'browserHarnessSHA256':H(Q/'browser.mjs')};(Q/'seal.json').write_text(json.dumps(seal,indent=2)+'\n');(Q/'root-go.json').write_text(json.dumps({'order':361,'status':'SEALED_STONE361_ROOT_GO','descriptors':37,'defaultDescriptors':8,'sealSHA256':H(Q/'seal.json'),'rootAuthorization':'Explicitroot361code/source/liveGO after366threebindings; ONEscope only; noinstall/promotion'},indent=2)+'\n')
elif mode=='after':
 seal=json.loads((Q/'seal.json').read_text());r={'status':'PASS361_CLOSED_PRESERVATION','canonicalPublicRuntimeBase342Unchanged':preserved(),'sealedStageUnchanged':inv(S)==seal['stage'],'sealedBuildUnchanged':inv(B)==seal['build'],'browserHarnessUnchanged':H(Q/'browser.mjs')==seal['browserHarnessSHA256']};r['preservationPASS']=all(r[k] for k in ['canonicalPublicRuntimeBase342Unchanged','sealedStageUnchanged','sealedBuildUnchanged','browserHarnessUnchanged']);(Q/'preservation-after.json').write_text(json.dumps(r,indent=2)+'\n');assert r['preservationPASS'];print('361PRESERVATIONPASS')
