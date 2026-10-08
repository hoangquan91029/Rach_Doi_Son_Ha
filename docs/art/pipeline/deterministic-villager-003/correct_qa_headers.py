"""Additive QA title correction only; no geometry/art render or source PNG modification."""
import hashlib,json,pathlib
from PIL import Image,ImageDraw
BASE=pathlib.Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
records=[]
for h in (64,80,96):
 source=BASE/('review-'+str(h)+'-contact-sheet.png');dest=BASE/('review-'+str(h)+'-contact-sheet-corrected48.png')
 if dest.exists():raise ValueError('no overwrite additive QA output')
 im=Image.open(source).convert('RGBA');d=ImageDraw.Draw(im);d.rectangle((0,0,im.width,23),fill=(63,66,60,255));d.text((3,3),str(h)+'px target /48 SAMPLES /stride1.28 hip.84 /CADENCE PENDING',fill='white');im.save(dest)
 records.append({'original':source.name,'originalSha256':sha(source),'corrected':dest.name,'correctedSha256':sha(dest),'change':'QA header rectangle y0..23 only; framepixels retained below title area'})
receipt={'status':'ADDITIVE_QA_HEADER_CORRECTION_ONLY','sourceRenderBuildsAdded':0,'motionChanges':False,'styleChanges':False,'originalSheetsPreserved':True,'scriptSha256':sha(pathlib.Path(__file__)),'outputs':records}
(BASE/'qa-header-correction-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
