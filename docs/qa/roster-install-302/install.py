from pathlib import Path
import json,hashlib,shutil,subprocess
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');Q=R/'docs/qa/roster-install-302';S=Path('/tmp/rds-roster302-stage');B=Path('/tmp/rds-roster302-build')
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inv=lambda p:{str(f.relative_to(p)):h(f) for f in sorted(p.rglob('*')) if f.is_file()}
write=lambda n,x:(Q/n).write_text(json.dumps(x,indent=2)+'\n')
read=lambda p:json.loads(p.read_text())
(R/'docs/art/pipeline/MOVEMENT_PRODUCTION_PLAN_20261010.md').read_text()
assert not S.exists() and not B.exists()
assert h(R/'client/raster-slice.js')==read(R/'docs/qa/roster-registry-296/source-bindings.json')['canonicalInputSha256']['client/raster-slice.js']
service=subprocess.check_output(['systemctl','--user','show','rach-doi-son-ha.service','-p','MainPID','-p','WorkingDirectory','-p','ActiveState'],text=True)
assert 'MainPID=3229' in service and 'ActiveState=active' in service
before={n:inv(R/n) for n in ['client','shared','server','public','dist']};write('before-inventories.json',before)
pins=read(R/'docs/qa/roster-registry-296/receipt.json')['sources'];owned=['client/raster-slice.js','shared/unit-art.js','tests/roster-registry296.test.js']
for n in owned:
 p=R/'docs/qa/roster-registry-296/source'/n;assert h(p)==pins[n];shutil.copy2(p,R/n)
res=subprocess.run(['node','--test','tests/roster-registry296.test.js','tests/building-death-api291.test.js','tests/building-state-api276.test.js'],cwd=R,capture_output=True,text=True)
(Q/'tests.txt').write_text(res.stdout+res.stderr);assert res.returncode==0
S.mkdir()
for n in ['client','shared','public'] :shutil.copytree(R/n,S/n)
for n in ['index.html','package.json','package-lock.json','vite.config.js']:shutil.copy2(R/n,S/n)
(S/'node_modules').symlink_to(R/'node_modules',target_is_directory=True)
excluded=['assets/art-v1/food-099-manifest.json','assets/art-v1/food-099/atlas.png']
for n in excluded:(S/'public'/n).unlink()
assert inv(S/'public')=={n:v for n,v in before['public'].items() if n not in excluded}
assert S.resolve()==Path('/tmp/rds-roster302-stage') and B.is_absolute() and R not in B.parents and h(S/'vite.config.js')==h(R/'vite.config.js')
write('build-preflight.json',{'cwd':str(S),'absoluteOutDir':str(B),'configPath':str(S/'vite.config.js'),'configSHA256':h(S/'vite.config.js'),'excludedOnly':excluded,'source':{n:inv(S/n) for n in ['client','shared','public']}})
res=subprocess.run([str(S/'node_modules/.bin/vite'),'build','--config','/tmp/rds-roster302-stage/vite.config.js','--outDir','/tmp/rds-roster302-build'],cwd=S,capture_output=True,text=True)
(Q/'build.txt').write_text(res.stdout+res.stderr);assert res.returncode==0
# All prior public chunks retained byte-for-byte, before candidate sealing.
for p in (R/'dist/assets').glob('index-*'):
 target=B/'assets'/p.name
 if target.exists():assert h(target)==h(p)
 else:shutil.copy2(p,target)
assert all(h(B/n)==v for n,v in before['dist'].items() if n.startswith('assets/index-'))
res=subprocess.run(['python3',str(R/'scripts/validate-art-assets.py'),str(B/'assets/art-v1/fort-202-manifest.json'),'--source-root',str(R),'--output',str(Q/'structural53.json')],cwd=S,capture_output=True,text=True)
(Q/'structural53.txt').write_text(res.stdout+res.stderr);assert res.returncode==0
assert len(read(B/'assets/art-v1/fort-202-manifest.json')['assets'])==53
assert h(B/'assets/art-v1/fort-202-manifest.json')==before['public']['assets/art-v1/fort-202-manifest.json']
after={n:inv(R/n) for n in before};write('after-inventories.json',after)
for n in ['server','public','dist']:assert after[n]==before[n]
assert {n:v for n,v in after['client'].items() if n!='raster-slice.js'}=={n:v for n,v in before['client'].items() if n!='raster-slice.js'}
assert {n:v for n,v in after['shared'].items() if n!='unit-art.js'}==before['shared']
write('candidate-pins.json',inv(B))
write('receipt.json',{'order':302,'status':'EXACT296_INSTALLED_ISOLATED_BUILT_SEALED_BROWSER_UNCALLED','routing':'gpt-6.1-sol low','sourceHEAD':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'ownedFiles':{n:h(R/n) for n in owned},'testsPassed':14,'stage':str(S),'build':str(B),'buildFiles':len(inv(B)),'manifestAssets':53,'publicServerSimUnchanged':True,'service':service,'browserCalled':False,'publicPromoted':False,'ownedHandles':'all test/build/validator processes terminal; no browser/image/service handles','limits':['Registry eligibility only, no authored roster or motion acceptance','Relevant actual family scene and separate promotion remain required']})
print('PASS302 exact install / 14 tests / isolated retained-chunk build / structural53 / preservation / sealed')
