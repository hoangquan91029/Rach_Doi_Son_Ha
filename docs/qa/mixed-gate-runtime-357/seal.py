import pathlib,hashlib,json,sys
root=pathlib.Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha'); out=root/'docs/qa/mixed-gate-runtime-357'; stage=pathlib.Path('/tmp/rds-mixed-gate357-stage'); build=pathlib.Path('/tmp/rds-mixed-gate357-build'); runtime=pathlib.Path('/home/kieu-hoang-quan/.local/share/rach-doi-son-ha/releases/230/runtime230')
def inv(d):return {str(p.relative_to(d)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(d.rglob('*')) if p.is_file() and 'node_modules' not in p.parts}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
mode=sys.argv[1]
if mode=='before':
 pins={str(p.relative_to(root)):sha(p) for folder in ['client','shared','server'] for p in (root/folder).rglob('*') if p.is_file()}
 guard={'public':inv(root/'dist'),'runtime':inv(runtime),'canonical':pins,'baseline342':inv(pathlib.Path('/tmp/rds-terrain-public342-stage'))}
 (out/'preservation-before.json').write_text(json.dumps(guard,indent=2)+'\n')
elif mode=='seal':
 assert stage.resolve()==stage and build.resolve()==build and stage!=root and build!=root/'dist'
 assert sha(stage/'vite.config.js')==json.loads((out/'work-order.json').read_text())['viteConfigSHA256']
 baseline=json.loads((out/'source-inventory.json').read_text()); current=inv(stage)
 changes={p for p in set(baseline)|set(current) if baseline.get(p)!=current.get(p)}
 assert changes=={'public/assets/art-v1/fort-202-manifest.json','public/assets/art-v1/gate-356/runtime.png'},changes
 seal={'status':'SEALED357_SOURCE_BUILD_BEFORE_BROWSER','stage':inv(stage),'build':inv(build),'changedSourceFiles':sorted(changes),'source356':sha(root/'docs/art/buildings/mixed-gate-idle-356/raw.png'),'runtime356':sha(root/'docs/art/buildings/mixed-gate-idle-356/runtime.png')}
 (out/'seal.json').write_text(json.dumps(seal,indent=2)+'\n')
 (out/'root-go.json').write_text(json.dumps({'order':357,'status':'SEALED_SELECTED356_ROOT_GO','rootAuthorization':'Explicit root finite357 GO after356 root intake','sealSHA256':sha(out/'seal.json')},indent=2)+'\n')
elif mode=='after':
 before=json.loads((out/'preservation-before.json').read_text()); after={'public':inv(root/'dist'),'runtime':inv(runtime),'canonical':{p:sha(root/p) for p in before['canonical']},'baseline342':inv(pathlib.Path('/tmp/rds-terrain-public342-stage'))}
 seal=json.loads((out/'seal.json').read_text()); after['stageUnchanged']=inv(stage)==seal['stage']; after['buildUnchanged']=inv(build)==seal['build']; after['preservationPASS']=all(after[k]==before[k] for k in before) and after['stageUnchanged'] and after['buildUnchanged']
 (out/'preservation-after.json').write_text(json.dumps(after,indent=2)+'\n'); assert after['preservationPASS']; print('PRESERVATION PASS')
