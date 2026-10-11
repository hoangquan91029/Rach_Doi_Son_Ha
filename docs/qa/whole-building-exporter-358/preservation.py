from pathlib import Path
import json,hashlib,sys
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');O=R/'docs/qa/whole-building-exporter-358'
paths=['scripts','client','shared','server','public','dist','docs/qa/wall-collapse-adapter-313','docs/art/buildings/wall-collapse-preview-321','docs/art/buildings/mixed-gate-idle-356']
backend=Path('/home/kieu-hoang-quan/.local/share/rach-doi-son-ha/releases/230/runtime230')
def inv(root):return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob('*')) if p.is_file() and 'node_modules' not in p.parts and '__pycache__' not in p.parts}
current={p:inv(R/p) for p in paths};current['immutable230']=inv(backend)
if sys.argv[1]=='before':(O/'preservation-before.json').write_text(json.dumps(current,indent=2)+'\n')
else:
 before=json.loads((O/'preservation-before.json').read_text());assert current==before,'Preservation drift';(O/'preservation-after.json').write_text(json.dumps({'status':'PASS_UNCHANGED313321356_CANONICAL_PUBLIC_BACKEND','inventories':current},indent=2)+'\n');print('PRESERVATION PASS')
