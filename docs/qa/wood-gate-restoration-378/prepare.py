from pathlib import Path
import json,shutil,hashlib,subprocess,difflib
R=Path.cwd();Q=R/'docs/qa/wood-gate-restoration-378';S=Path('/tmp/rds-gates378-stage');B=Path('/tmp/rds-gates378-build');H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def inv(p):return {str(f.relative_to(p)):H(f) for f in sorted(p.rglob('*')) if f.is_file() and 'node_modules' not in f.parts}
assert not S.exists() and not B.exists()
base={n:inv(R/n) for n in ['client','shared','public','dist']};runtime=Path.home()/'.local/share/rach-doi-son-ha/releases/230/runtime230'
(Q/'preservation-before.json').write_text(json.dumps({'canonical':base,'runtime':inv(runtime),'HEAD':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()},indent=2))
S.mkdir()
for n in ['client','shared','public','tests']:shutil.copytree(R/n,S/n)
for n in ['index.html','package.json','vite.config.js']:shutil.copy2(R/n,S/n)
(S/'node_modules').symlink_to(R/'node_modules',target_is_directory=True)
(Q/'originals').mkdir(exist_ok=True)
shutil.copy2(R/'tests/fortification-picking222.test.js',Q/'originals/fortification-picking222.test.js')
old=Path('/tmp/renderer347.js').read_text();body=old.split(' drawFortification(c,e,z,color,trim){',1)[1].split('\n drawBuilding',1)[0];body=body.rsplit('\n }',1)[0].replace('this.','renderer.')
# Exact old gate branch and beams only; wooden wall center-post branch excluded.
body=body.replace("  else{const p=renderer.project(e.x,e.y);c.strokeStyle=color;c.lineWidth=3*z;c.beginPath();c.moveTo(p.x,p.y);c.lineTo(p.x,p.y-13*z);c.stroke();}\n",'')
(S/'client/wood-gate.js').write_text("import {fortificationSpans} from './fortification-topology.js';\n/** Original347 gate-only whole native geometry; walls retain stone presentation. */\nexport function drawWoodGate(renderer,c,e,z,color,trim){"+body+'\n}\n')
p=S/'client/renderer.js';t=p.read_text().replace("import {drawStoneFortification}","import {drawWoodGate} from './wood-gate.js';\nimport {drawStoneFortification}");t=t.replace('drawFortification(c,e,z,color,trim){drawStoneFortification(this,c,e,z);}',"drawFortification(c,e,z,color,trim){if(e.type==='gate')drawWoodGate(this,c,e,z,color,trim);else drawStoneFortification(this,c,e,z);}");p.write_text(t)
p=S/'client/fortification-picking.js';t=p.read_text().replace('STONE_WALL_HEIGHT,STONE_GATE_HEIGHT','STONE_WALL_HEIGHT').replace('const z=renderer.camera.zoom;','const z=renderer.camera.zoom,wallHeight=entity.type===\'gate\'?12:STONE_WALL_HEIGHT;').replace('span.to,STONE_WALL_HEIGHT','span.to,wallHeight').replace('STONE_GATE_HEIGHT,STONE_WALL_HEIGHT','16,12').replace('STONE_GATE_HEIGHT*z','16*z');p.write_text(t)
p=S/'client/stone-fortification.js';t=p.read_text().replace("return !['building.wall','building.gate'].includes(asset?.family)||asset.material==='stone';","return asset?.family==='building.wall'?asset.material==='stone':asset?.family==='building.gate'?asset.material==='wood':true;");p.write_text(t)
rows=[a for a in json.loads((R/'docs/qa/stone-fortification-runtime-361/retired-wood-custody/former-descriptors.json').read_text())['rows'] if a['family']=='building.gate'];assert len(rows)==7
(Q/'original-gate-rows.json').write_text(json.dumps(rows,indent=2))
for a in rows:a['material']='wood'
for name,count in [('stone-361-manifest.json',16),('fort-202-manifest.json',45)]:
 p=S/'public/assets/art-v1'/name;m=json.loads(p.read_text());m['assets']+=rows;assert len(m['assets'])==count;p.write_text(json.dumps(m,indent=2)+'\n')
for d,sha in [('gate-245','89f18963d6d66452d584071e5158320c4168a6fb0d908c2ca06375759aaa6579'),('gate-252','867ba2b2e8e15f4d1c2011defebeb2c5fd3cd704722ba10bf2a6b637b765fbd1')]:
 src=R/'docs/qa/stone-fortification-runtime-361/retired-wood-custody/payloads/public/assets/art-v1'/d/'idle.png';assert H(src)==sha;dst=S/'public/assets/art-v1'/d;dst.mkdir();shutil.copy2(src,dst/'idle.png')
p=S/'tests/fortification-picking222.test.js';p.write_text(p.read_text().replace('(STONE_WALL_HEIGHT+2)','14'))
for n in ['client','shared','public','dist']:assert inv(R/n)==base[n]
(Q/'source-before.json').write_text(json.dumps({k:v for n,x in base.items() if n!='dist' for k,v in [(n+'/'+p,h) for p,h in x.items()]},indent=2))
(Q/'candidate-source-inventory.json').write_text(json.dumps(inv(S),indent=2))
print('PREPARED16/45')
