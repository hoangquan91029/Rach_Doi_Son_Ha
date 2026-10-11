exec(open('docs/qa/roster-install-302/install.py').read().split('assert not S.exists()')[0])
from PIL import Image
res=subprocess.run(['node','--input-type=module','-e',"import {validateManifest} from './client/art-assets.js';import fs from 'node:fs';validateManifest(JSON.parse(fs.readFileSync('/tmp/rds-roster302-build/assets/art-v1/fort-202-manifest.json')));console.log('PASS real runtime validateManifest53');"],cwd=S,capture_output=True,text=True)
(Q/'runtime-validator.txt').write_text(res.stdout+res.stderr);assert res.returncode==0
m=read(B/'assets/art-v1/fort-202-manifest.json');assert len(m['assets'])==53
runtime=[]
for a in m['assets']:
 p=B/'assets/art-v1'/a['runtime']['path'];meta=a['runtime'];assert h(p)==meta['sha256']
 im=Image.open(p).convert('RGBA');assert list(im.size)==[meta['width'],meta['height']];assert hashlib.sha256(im.tobytes()).hexdigest()==meta['rgbaSha256'];runtime.append({'id':a['id'],'runtimeSHA256':h(p)})
write('runtime-structural53.json',{'status':'PASS_REAL_VALIDATE_MANIFEST_AND_53_RUNTIME_ENCODED_RGBA','assets':runtime,'historicalSourceValidatorFailureRetained':'structural53.json'})
before=read(Q/'before-inventories.json');after={n:inv(R/n) for n in before};write('after-inventories.json',after)
for n in ['server','public','dist']:assert after[n]==before[n]
assert {n:v for n,v in after['client'].items() if n!='raster-slice.js'}=={n:v for n,v in before['client'].items() if n!='raster-slice.js'}
assert {n:v for n,v in after['shared'].items() if n!='unit-art.js'}==before['shared']
assert h(B/'assets/art-v1/fort-202-manifest.json')==before['public']['assets/art-v1/fort-202-manifest.json']
assert all(h(B/n)==v for n,v in before['dist'].items() if n.startswith('assets/index-'))
write('candidate-pins.json',inv(B))
owned=['client/raster-slice.js','shared/unit-art.js','tests/roster-registry296.test.js']
write('receipt.json',{'order':302,'status':'EXACT296_INSTALLED_ISOLATED_BUILT_SEALED_BROWSER_UNCALLED','routing':'gpt-6.1-sol low','sourceHEAD':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'ownedFiles':{n:h(R/n) for n in owned},'testsPassed':14,'stage':str(S),'build':str(B),'buildFiles':len(inv(B)),'manifestAssets':53,'publicServerSimUnchanged':True,'service':subprocess.check_output(['systemctl','--user','show','rach-doi-son-ha.service','-p','MainPID','-p','WorkingDirectory','-p','ActiveState'],text=True),'browserCalled':False,'publicPromoted':False,'ownedHandles':'all test/build/validator processes terminal; no browser/image/service handles','initialSourceCustodyValidatorFailureRetained':True,'runtimeStructuralValidation':'real validateManifest plus53 encoded/RGBA/dimensions exact','limits':['Registry eligibility only, no authored roster or motion acceptance','Relevant actual family scene and separate promotion remain required']})
print('PASS302 sealed installed candidate runtime53 exact')
