exec(open('docs/qa/wood-gate-restoration-378/prepare.py').read().split('assert not S.exists()')[0])
for d,sha in [('gate-245','89f18963d6d66452d584071e5158320c4168a6fb0d908c2ca06375759aaa6579'),('gate-252','867ba2b2e8e15f4d1c2011defebeb2c5fd3cd704722ba10bf2a6b637b765fbd1')]:
 src=R/'docs/qa/stone-fortification-runtime-361/retired-wood-custody/payloads/public/assets/art-v1'/d/'idle.png';assert H(src)==sha;dst=S/'public/assets/art-v1'/d;dst.mkdir(exist_ok=True);shutil.copy2(src,dst/'idle.png')
p=S/'tests/fortification-picking222.test.js';p.write_text(p.read_text().replace('(STONE_WALL_HEIGHT+2)','14'))
b=json.loads((Q/'preservation-before.json').read_text());assert all(inv(R/n)==v for n,v in b['canonical'].items())
(Q/'candidate-source-inventory.json').write_text(json.dumps(inv(S),indent=2));print('PREPARED')
