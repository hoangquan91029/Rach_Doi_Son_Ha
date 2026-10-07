"""Finalize PNG decoded custody and fixed whole-canvas preview only after real rendering."""
import pathlib,json,hashlib,sys
from PIL import Image
p=pathlib.Path(sys.argv[1]);receipt=json.load(open(p/'render-receipt.json'));frames=[];count=len(receipt['frames']);duration=receipt.get('cycleDurationMs');images=[]
for index,row in enumerate(receipt['frames']):
 file=p/row['file'];raw=file.read_bytes()
 with Image.open(file) as original:
  image=original.convert('RGBA');assert image.size==(1254,1254);rgba=image.tobytes();bounds=image.getchannel('A').point(lambda a:255 if a>16 else 0).getbbox()
  frames.append({**row,'sha256':hashlib.sha256(raw).hexdigest(),'rgbaSha256':hashlib.sha256(rgba).hexdigest(),'dimensions':[1254,1254],'timeMs':None if duration is None else index*duration/count,'durationMs':None if duration is None else duration/count,'root':receipt['root'],'presentationScale':receipt['scale'],'alphaGreater16Bounds':bounds})
  images.append(image.resize((38,38),Image.Resampling.LANCZOS))
receipt['frames']=frames;receipt['independentMotionReview']='PENDING';receipt['runtimeIntegrated']=False
if duration and count>1:
 images[0].save(p/'loop-fixed-38.gif',save_all=True,append_images=images[1:],duration=round(duration/count),loop=0,disposal=2)
 receipt['gifNote']='Fixed whole-canvas38 preview; GIF integer-ms timing quantizes nominal frame duration, PNG sidecar timing is authoritative.'
else:images[0].save(p/'partial-fixed-38.png')
(p/'render-receipt.json').write_text(json.dumps(receipt,indent=2))
