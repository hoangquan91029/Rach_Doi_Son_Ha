from pathlib import Path
import hashlib,json,subprocess
R=Path.cwd();Q=R/'docs/qa/wood-gate-public-383';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();go=json.loads((Q/'root-go.json').read_text());assert go['status']=='PUBLIC382_PROMOTED_ROOT383_LIVE_GO'
b=json.loads((R/'docs/qa/wood-gate-restoration-379/binding.json').read_text());b['order']=383;b['root']=str(R);b['sourceHEAD']=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();b['installationReceiptSHA256']=H(R/'docs/qa/wood-gate-install-382/installation.json');b['preservationPins']=[]
for root in [R/'client',R/'shared',R/'public',R/'dist',Path.home()/'.local/share/rach-doi-son-ha/releases/230/runtime230']:
 for p in sorted(root.rglob('*')):
  if p.is_file() and 'node_modules' not in p.parts:b['preservationPins'].append({'path':str(p),'sha256':H(p),'mode':p.stat().st_mode&0o777})
for rel,sha in b['buildPins'].items():assert H(R/'dist'/rel)==sha,rel
assert len(json.loads((R/'dist/assets/art-v1/stone-361-manifest.json').read_text())['assets'])==16
assert not (R/'dist/assets/art-v1/food-099/atlas.png').exists()
(Q/'binding.json').write_text(json.dumps(b,indent=2));(Q/'preflight.json').write_text(json.dumps({'status':'PASS383_PUBLIC382_PRESERVATION_BOUND_BEFORE_ONE_FIREFOX','sourceHEAD':b['sourceHEAD'],'installationSHA256':b['installationReceiptSHA256'],'pins':len(b['preservationPins']),'harnessSHA256':H(Q/'browser.mjs'),'browserTrials':1,'builds':0,'images':0},indent=2));print('PASS383',len(b['preservationPins']))
