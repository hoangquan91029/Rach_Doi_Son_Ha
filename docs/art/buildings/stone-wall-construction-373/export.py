from pathlib import Path
from PIL import Image
import shutil,json,hashlib
p=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha/docs/art/buildings/stone-wall-construction-373')
original=Path('/home/kieu-hoang-quan/.codex/generated_images/01a1159b-f20c-75d2-8030-3f4d27119543/exec-442f98c0-adba-4db5-bc47-6644459eebf8.png')
shutil.copy2(original,p/'raw.png');im=Image.open(p/'raw.png');assert im.mode=='RGBA' and im.size==(1254,1254)
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
def record(name):
 f=p/name;i=Image.open(f);return dict(path=name,sha256=sha(f),rgbaSha256=hashlib.sha256(i.tobytes()).hexdigest(),width=i.width,height=i.height)
for name,n in [('runtime.png',128),('working.png',256),('preview42.png',42)]:im.resize((n,n),Image.Resampling.LANCZOS).save(p/name)
source=record('raw.png');runtime=record('runtime.png');runtime['derivation']=dict(method='resize',filter='lanczos',sourceSha256=source['sha256'])
a=json.loads((p.parent/'stone-wall-X-362/candidate.json').read_text());a.update(id='stone-wall-construction-373',state='construction',source=source,runtime=runtime,loop=False,notes='Whole stone construction site, standalone mask0. One static source; no animated progression or runtime/scene acceptance yet. No wood, no PNG transforms.')
(p/'candidate.json').write_text(json.dumps(a,indent=2)+'\n')
alpha=im.getchannel('A');edges=[alpha.crop((0,0,1254,1)),alpha.crop((0,1253,1254,1254)),alpha.crop((0,0,1,1254)),alpha.crop((1253,0,1254,1254))]
receipt=dict(status='RETURNED_CANDIDATE_AWAIT_SCENE',builtinCalls=1,manualRetries=0,toolState='RETURNED_CLOSED',originalToolPath=str(original),source=source,runtime=runtime,working=record('working.png'),preview=record('preview42.png'),alphaExtrema=alpha.getextrema(),edgeAlphaMax=max(e.getextrema()[1] for e in edges),fixedLayout=dict(canvas=[1254,1254],pivot=[627,900],runtimeCell=128,logicalRender=42.3225),derivation='Whole uniform resize only; no fit/crop/shift/warp/mirror/sourcepixelrepair')
(p/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
j=json.loads((p/'work-order.json').read_text());j.update(status='RETURNED_CLOSED',callsCompleted=1,originalToolPath=str(original));(p/'work-order.json').write_text(json.dumps(j,indent=2)+'\n')
print(json.dumps(dict(source=source['sha256'],runtime=runtime['sha256'],edgeAlphaMax=receipt['edgeAlphaMax'])))
