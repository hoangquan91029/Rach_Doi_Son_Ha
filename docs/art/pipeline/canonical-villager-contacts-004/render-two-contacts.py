from pathlib import Path
import importlib.util,json,hashlib
import numpy as np
from PIL import Image,ImageDraw
BASE=Path(__file__).resolve().parent
MODEL=BASE/'model-appearance-v1.py'
FROZEN=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha/docs/art/pipeline/deterministic-villager-003/model003.py')
REF=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha/docs/art/characters/villager-neutral-D07-screen-East-guided-007/raw.png')
OUT=BASE/'rendered-contacts'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
if OUT.exists():raise SystemExit('render output exists; no retry permitted')
if sha(MODEL)!='421aad76da67de32b3f1c95353c2d5d465d77820e0306ac8c9a9190162651192':raise SystemExit('frozen appearance source mismatch')
if sha(FROZEN)!='2e03d733f742ec60cc046c026fcd2ee13f2413d9bcd8cbeefe652aaeccddbd59':raise SystemExit('frozen motion source mismatch')
if sha(REF)!='45ae1e7a27d3cb9260dc9e5495cf83b4956481b1047ead2975572aff1385aae3':raise SystemExit('canonical ref mismatch')
spec=importlib.util.spec_from_file_location('appearance_model_v1',MODEL);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
OUT.mkdir();(OUT/'aux').mkdir()
records=[];rawframes=[]
# The only complete source renders in this lease: the two frozen opposite contacts.
for name,phase in [('F0',0.0),('F24',0.5)]:
 im,mask,depth,normal,limbid,geo=m.render(m.pose(phase))
 bbox=im.getbbox();height=bbox[3]-bbox[1]
 if not(192<=height<=256):raise SystemExit(f'{name}: source body height {height} outside 192..256; stop without retry')
 if min(geo['geometryBounds'])<0 or geo['geometryBounds'][2]>=256 or geo['geometryBounds'][3]>=256:raise SystemExit(f'{name}: projected geometry outside canvas; stop without retry')
 im.save(OUT/f'{name}.png');im.resize((128,128),Image.Resampling.LANCZOS).save(OUT/f'{name}-runtime128.png')
 for suffix,aux in [('mask',mask),('depth',depth),('normal',normal),('limbID',limbid)]:aux.save(OUT/'aux'/f'{name}-{suffix}.png')
 records.append({'frame':name,'phase':phase,'sourceCanvas':[256,256],'sourcePivot':[128,237],'alphaBounds':list(bbox),'actualAlphaHeight':height,'geometryBounds':geo['geometryBounds'],'vertices':geo['vertices'],'triangles':geo['triangles'],'pngSha256':sha(OUT/f'{name}.png'),'runtime128Sha256':sha(OUT/f'{name}-runtime128.png'),'auxSha256':{s:sha(OUT/'aux'/f'{name}-{s}.png') for s in ['mask','depth','normal','limbID']}})
 rawframes.append(im)
# Contact sheets use fixed whole-canvas scaling and pivots; no fit or per-image crop.
ref=Image.open(REF).convert('RGBA')
for h in (80,96):
 cells=[]; scale=h/233; canvas_size=round(256*scale); pivot=(128*scale,237*scale)
 for label,source in [('Canonical D07 East',ref),('F0 phase 0',rawframes[0]),('F24 phase .5',rawframes[1])]:
  cw=max(126,canvas_size+28); ch=max(126,canvas_size+32); cell=Image.new('RGBA',(cw,ch),(67,75,62,255));draw=ImageDraw.Draw(cell);draw.text((4,3),label,fill=(245,239,216,255))
  if label.startswith('Canonical'):
   # Static identity reference keeps its original canvas; one alpha>=32 body-height measurement only.
   source_pivot=(654,1140);reference_height=1130;ss=h/reference_height;resized=source.resize((round(source.width*ss),round(source.height*ss)),Image.Resampling.LANCZOS);rp=(source_pivot[0]*ss,source_pivot[1]*ss);x=round(cw/2-rp[0]);y=round(ch-7-rp[1]);cell.alpha_composite(resized,(x,y))
  else:
   resized=source.resize((canvas_size,canvas_size),Image.Resampling.LANCZOS);x=round(cw/2-pivot[0]);y=round(ch-7-pivot[1]);cell.alpha_composite(resized,(x,y))
  cells.append(cell)
 sheet=Image.new('RGBA',(sum(c.width for c in cells),max(c.height for c in cells)),(46,52,44,255));x=0
 for cell in cells:sheet.alpha_composite(cell,(x,0));x+=cell.width
 sheet.save(BASE/f'contacts-{h}px.png')
receipt={'schema':'canonical-villager-appearance-two-contact-render-receipt/v1','status':'TWO_CONTACTS_RENDERED_PENDING_PARENT_VISUAL_REVIEW','direction':'D07 Screen East / engine-world NE theta=315','appearanceSourceSha256':sha(MODEL),'frozen003MotionSourceSha256':sha(FROZEN),'canonicalReferenceSha256':sha(REF),'renderBuildCount':1,'completeSourceRenderCount':2,'retries':0,'frames':records,'contactSheets':{str(h):sha(BASE/f'contacts-{h}px.png') for h in (80,96)},'lockedConstants':{'stride':1.28,'hipRest':0.84,'periodMs':649.5793241743906,'worldSpeed':2.1,'sourceCanvas':[256,256],'sourcePivot':[128,237],'runtimeCell':[128,128],'sourceCharacterHeight':233},'limitations':['Two static contacts only; no motion acceptance.','Pelvis-following hem is not knee-aware cloth deformation; collision, self-intersection and leg occlusion are not numerically solved.','Hat and shading changes are not independent identity or owner approval.','No full loop, direction fanout, image transforms or source pixel editing.']}
(OUT/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'status':receipt['status'],'frames':records,'contactSheets':receipt['contactSheets'],'renderBuildCount':1},indent=2))
