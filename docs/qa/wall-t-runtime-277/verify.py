from pathlib import Path
import json,hashlib
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');Q=R/'docs/qa/wall-t-runtime-277';S=Path('/tmp/rds-wall-t277-stage');B=Path('/tmp/rds-wall-t277-build');h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();binding=json.loads((Q/'binding.json').read_text());prior=json.loads((Q/'prior46.json').read_text());m=json.loads((B/'assets/art-v1/fort-202-manifest.json').read_text());assert len(m['assets'])==48 and m['assets'][:46]==prior['assets'];assert h(B/'assets/index-z82FayZ6.js')==binding['bundleSHA256'];assert h(B/'assets/art-v1/fort-202-manifest.json')==binding['manifestSHA256'];assert len([f for f in B.rglob('*') if f.is_file()])==197
for a in prior['assets']:
 assert h(S/'public/assets/art-v1'/a['runtime']['path'])==h(R/'public/assets/art-v1'/a['runtime']['path'])
for a in m['assets'][-2:]:assert set(a['fortification'])=={'mask'} and a['fortification']['mask'] in [7,11] and h(B/'assets/art-v1'/a['runtime']['path'])==a['runtime']['sha256']
assert not (B/'assets/art-v1/food-099-manifest.json').exists() and not (B/'assets/art-v1/food-099/atlas.png').exists()
(Q/'contracts.json').write_text(json.dumps({'status':'PASS_TECHNICAL_ONLY','assets':48,'files':197,'old46Preserved':True,'newMaskOnly':[7,11],'bundleSHA256':binding['bundleSHA256'],'noVisualAcceptance':True},indent=2))
(Q/'build-pins.json').write_text(json.dumps({str(f.relative_to(B)):h(f) for f in sorted(B.rglob('*')) if f.is_file()},indent=2))
print('48 descriptor/197file/staticbundle/custody contracts PASS technical only')
