from pathlib import Path
import json,hashlib,shutil,urllib.request,subprocess
R=Path.cwd();Q=R/'docs/qa/wall-t-install-283';B=Path('/tmp/rds-wall-t277-build');h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();inv=lambda p:{str(f.relative_to(R)):h(f) for f in sorted(p.rglob('*')) if f.is_file()};mp=R/'public/assets/art-v1/fort-202-manifest.json';old=json.loads(mp.read_text());assert len(old['assets'])==47;install281=json.loads((R/'docs/qa/wall-construction-install-281/receipt.json').read_text());assert h(mp)==install281['changedFiles']['public/assets/art-v1/fort-202-manifest.json']['afterSHA256']
for n,v in install281['changedFiles'].items():assert h(R/n)==v['afterSHA256']
assert json.loads((R/'docs/qa/wall-t-runtime-277b/root-intake.json').read_text())
before={};
for n in ['client','shared','server','public','dist','tests']:before.update(inv(R/n))
(Q/'preservation-before.json').write_text(json.dumps(before,indent=2));shutil.copy2(mp,Q/'before47-manifest.json');m=json.loads(mp.read_text());tested=json.loads((B/'assets/art-v1/fort-202-manifest.json').read_text());assert len(tested['assets'])==48 and tested['assets'][:46]==old['assets'][:46]
added=[]
for a in tested['assets'][-2:]:
 assert a['fortification'] in [{'mask':7},{'mask':11}];src=B/'assets/art-v1'/a['runtime']['path'];assert h(src)==a['runtime']['sha256'];dest=R/'public/assets/art-v1'/a['runtime']['path'];assert not dest.exists();dest.parent.mkdir();shutil.copy2(src,dest);m['assets'].append(a);added.append(str(dest.relative_to(R)))
assert m['assets'][:47]==old['assets'];assert len(m['assets'])==49;mp.write_text(json.dumps(m,indent=2)+'\n');after={}
for n in ['client','shared','server','public','dist','tests']:after.update(inv(R/n))
allowed={str(mp.relative_to(R)),*added};assert {n for n in set(before)|set(after) if before.get(n)!=after.get(n)}==allowed
(Q/'preservation-after.json').write_text(json.dumps(after,indent=2));(Q/'install-pins.json').write_text(json.dumps({n:after[n] for n in sorted(allowed)},indent=2));print('49 local installed; old47/outsidefiles exact')
