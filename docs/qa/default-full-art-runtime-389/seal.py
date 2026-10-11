from pathlib import Path
import json,hashlib,os
root=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');out=root/'docs/qa/default-full-art-runtime-389';stage=Path('/tmp/rds-fullart389-stage');build=Path('/tmp/rds-fullart389-build')
def inv(base):return {str(p.relative_to(base)):{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'mode':oct(p.stat().st_mode&0o777)} for p in sorted(base.rglob('*')) if p.is_file() and not p.is_symlink()}
assert inv(stage)==json.loads((out/'stage-inventory.json').read_text())
before=json.loads((out/'preservation-before.json').read_text())
for rel,pin in before['public'].items():
 if rel!='index.html':assert inv(build)[rel]==pin,rel
assert len(inv(build))==201
binding={'order':389,'rootAuthorized':True,'stage':str(stage),'build':str(build),'sourcePins':inv(stage),'buildPins':inv(build),'bundle':'assets/index-8telBS7h.js','bundleSHA256':hashlib.sha256((build/'assets/index-8telBS7h.js').read_bytes()).hexdigest(),'focusedContracts':10,'387PassedPreviously':8,'immutableSealed':True}
(out/'binding.json').write_text(json.dumps(binding,indent=2)+'\n')
print(json.dumps({'status':'SEALED389_IMMUTABLE','buildFiles':201,'bundleSHA256':binding['bundleSHA256'],'focusedContracts':10}))
