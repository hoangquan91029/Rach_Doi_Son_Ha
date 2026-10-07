"""Deterministic web derivatives; does not modify any leadership source."""
from pathlib import Path
from PIL import Image
import hashlib,json,re
ROOT=Path(__file__).resolve().parents[1]
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
manifest={'status':'STATIC_DIRECTIONAL_REFERENCES_NOT_ANIMATION_APPROVAL','directionOrder':['E','SE','S','SW','W','NW','N','NE'],'characters':{}}
for folder in sorted((ROOT/'leadership').iterdir()):
    refs=list(folder.glob('candidates/*/identity-reference/*.png'))
    dirs={}
    for d in range(8):
        candidates=[p for p in refs if re.search(rf'D0{d}(?:[^0-9]|$)',p.name) and 'opaque-pre-research' not in p.name]
        candidates.sort(key=lambda p:('B02' not in str(p),str(p)))
        if not candidates: raise RuntimeError(f'Missing {folder.name} D0{d}')
        source=candidates[0]; out=ROOT/'public/assets/leadership'/folder.name/f'D0{d}.webp';out.parent.mkdir(parents=True,exist_ok=True)
        im=Image.open(source).convert('RGBA'); im.resize((128,192),Image.Resampling.LANCZOS).save(out,'WEBP',quality=90,method=6)
        dirs[f'D0{d}']={'source':str(source.relative_to(ROOT)),'sourceSha256':digest(source),'output':str(out.relative_to(ROOT/'public')),'outputSha256':digest(out),'dimensions':[128,192]}
    # Higher-resolution full-canvas identity card; no art reconstruction/cropping.
    card=out.parent/'portrait.webp';Image.open(ROOT/dirs['D02']['source']).convert('RGBA').resize((256,384),Image.Resampling.LANCZOS).save(card,'WEBP',quality=92,method=6)
    manifest['characters'][folder.name]={'directions':dirs,'portrait':str(card.relative_to(ROOT/'public')),'approval':'source candidate, unaudited; technical packaging only'}
path=ROOT/'public/assets/leadership/manifest.json';path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(f"Packaged {len(manifest['characters'])} characters, 96 static directional frames")
