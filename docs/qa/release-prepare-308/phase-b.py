from pathlib import Path
import json,hashlib,shutil,subprocess
R=Path.cwd();Q=R/'docs/qa/release-prepare-308';B=Path.home()/'.local/share/rach-doi-son-ha/releases/308';S=Path('/tmp/rds-registry-public305-stage');D=Path('/tmp/rds-registry-public305-build');T=R/'docs/qa/registry-publicscope-305';A=R/'docs/qa/registry-publicscope-runtime-307'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();inv=lambda p:{str(f.relative_to(p)):h(f) for f in sorted(p.rglob('*')) if f.is_file()};read=lambda p:json.loads(p.read_text());write=lambda n,v:(Q/n).write_text(json.dumps(v,indent=2)+'\n')
subprocess.run(['python3',str(Q/'reverify.py')],check=True)
sb=read(T/'source-bindings.json');bb=read(T/'build-binding.json');pins=read(T/'build-pins.json');rt=read(A/'receipt.json');intake=read(A/'root-intake.json')
assert intake['releasePreparationAuthorized'] and rt['actualBrowserStatus'].startswith('PASS307') and rt['foodRouteDisabled'] and rt['foodPayloadAbsent'] and rt['preservation']=='PASS_EXACT_BEFORE_AFTER';assert rt['cleanup']=={'rooms':0,'serverListening':False,'browserClosed':True}
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==sb['sourceHEAD'];assert {n:inv(R/n) for n in sb['canonical']}==sb['canonical']
assert inv(D)==pins and len(pins)==205
route=(R/'client/art-routes.js').read_text();food=" food:Object.freeze({manifestUrl:'/assets/art-v1/food-099-manifest.json',world:false}),\n";assert route.count(food)==1;assert (S/'client/art-routes.js').read_text()==route.replace(food,'');assert 'food-099-manifest' not in (S/'client/art-routes.js').read_text()
for n in ['assets/art-v1/food-099-manifest.json','assets/art-v1/food-099/atlas.png']:assert n not in pins and not (S/'public'/n).exists()
assert all(h(D/n)==v['sha256'] for n,v in rt['responsePins'].items());assert h(D/bb['bundlePath'])==bb['bundleSHA256'];assert read(T/'receipt.json')['publicationContractsPassed']==4
for n,v in read(R/'docs/qa/public-release-299/current-public-pins.json').items():
 if n!='index.html':assert pins[n]==v
assert not (B/'dist308').exists();shutil.copytree(D,B/'dist308')
for p in (B/'dist308').rglob('*'):
 if not p.is_symlink():p.chmod(0o555 if p.is_dir() else 0o444)
(B/'dist308').chmod(0o555);assert inv(B/'dist308')==pins
write('build-pins.json',pins);write('source-bindings.json',sb);write('build-binding.json',{**bb,'reusedSame305TestedBuild':True,'builds':0,'rootIntakeSHA256':h(A/'root-intake.json'),'actualReceiptSHA256':h(A/'receipt.json'),'strict305ContractsSHA256':h(T/'publication-contracts.mjs'),'strict305ContractResultsSHA256':h(T/'publication-contracts.txt'),'publicationContractsPassed':4})
print('308 same corrected305 candidate copied exact; no rebuild')
