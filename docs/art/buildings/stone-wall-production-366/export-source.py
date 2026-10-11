"""Custody copy and uniform whole-canvas idle exports; no fitting or pixel repair."""
from PIL import Image
import pathlib,json,hashlib,shutil,sys
p=pathlib.Path(sys.argv[1]);src=pathlib.Path(sys.argv[2]);asset_id=sys.argv[3];mask=int(sys.argv[4]);shutil.copy2(src,p/'raw.png');im=Image.open(p/'raw.png').convert('RGBA')
if im.size!=(1254,1254):raise ValueError('Unexpected family canvas; no fitting permitted')
def record(name):
 f=p/name;i=Image.open(f).convert('RGBA');return dict(path=name,sha256=hashlib.sha256(f.read_bytes()).hexdigest(),rgbaSha256=hashlib.sha256(i.tobytes()).hexdigest(),width=i.width,height=i.height)
for size,name in [(256,'working.png'),(128,'runtime.png'),(42,'preview42.png')]:im.resize((size,size),Image.Resampling.LANCZOS).save(p/name)
source=record('raw.png');runtime=record('runtime.png');runtime['derivation']=dict(method='resize',filter='lanczos',sourceSha256=source['sha256'])
a=im.getchannel('A');border=max(max(a.crop(b).get_flattened_data()) for b in [(0,0,im.width,1),(0,im.height-1,im.width,im.height),(0,0,1,im.height),(im.width-1,0,im.width,im.height)])
r=dict(status='RETURNED_CANDIDATE_AWAIT_SCENE',builtinCalls=1,manualRetries=0,toolState='RETURNED_CLOSED',originalToolPath=str(src),source=source,runtime=runtime,working=record('working.png'),preview=record('preview42.png'),alphaExtrema=a.getextrema(),edgeAlphaMax=border,fixedLayout=dict(canvas=[1254,1254],pivot=[627,900],runtimeCell=128,logicalRender=42.3225),derivation='Whole uniform resize only; no fit/crop/shift/warp/mirror/sourcepixelrepair')
(p/'receipt.json').write_text(json.dumps(r,indent=2)+'\n')
asset=dict(id=asset_id,family='building.wall',kind='building',state='idle',direction=None,material='stone',candidate=True,review=dict(status='CANDIDATE'),source=source,runtime=runtime,cell=dict(width=128,height=128),pivot=dict(x=627,y=900,space='source'),render=dict(width=42.3225,height=42.3225),alphaPolicy='transparent',contactShadow=dict(mode='baked'),frames=[dict(x=0,y=0,width=128,height=128,durationMs=1000)],loop=True,fortification=dict(mask=mask),notes='Whole realistic cutstone illustration, no wood. Only source appearance selected; actual joins trial pending.')
(p/'candidate.json').write_text(json.dumps(asset,indent=2)+'\n');o=json.loads((p/'work-order.json').read_text());o.update(status='RETURNED_CLOSED',callsCompleted=1);(p/'work-order.json').write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'source':source,'runtime':runtime,'edgeAlphaMax':border}))
