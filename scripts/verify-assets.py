from pathlib import Path
import hashlib,json
from PIL import Image
root=Path(__file__).resolve().parents[1]
locked=json.loads((root/'docs/leadership-source-hashes.json').read_text())
assert all(hashlib.sha256((root/p).read_bytes()).hexdigest()==h for p,h in locked.items()),'Source asset changed'
manifest=json.loads((root/'public/assets/leadership/manifest.json').read_text())
assert len(manifest['characters'])==12
for character,data in manifest['characters'].items():
 assert len(data['directions'])==8
 for direction,row in data['directions'].items():
  p=root/'public'/row['output']; im=Image.open(p)
  assert im.size==(128,192) and im.mode=='RGBA',str(p)
  assert hashlib.sha256(p.read_bytes()).hexdigest()==row['outputSha256']
  assert hashlib.sha256((root/row['source']).read_bytes()).hexdigest()==row['sourceSha256']
print(f'PASS: {len(locked)} source files unchanged; 96 RGBA derivatives and their hashes verified')
