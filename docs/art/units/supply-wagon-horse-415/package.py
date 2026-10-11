from pathlib import Path
from PIL import Image
import json,hashlib,shutil,sys
p=Path(__file__).resolve().parent
original=Path(sys.argv[1]);shutil.copyfile(original,p/'raw.png')
im=Image.open(p/'raw.png').convert('RGBA')
for name,size in [('working-256.png',256),('runtime-128.png',128),('preview-112.png',112)]: im.resize((size,size),Image.Resampling.LANCZOS).save(p/name)
def record(name):
 q=p/name;i=Image.open(q).convert('RGBA');return dict(path=str(q.relative_to(Path.cwd())),sha256=hashlib.sha256(q.read_bytes()).hexdigest(),rgbaSha256=hashlib.sha256(i.tobytes()).hexdigest(),width=i.width,height=i.height)
s=record('working-256.png');r=record('runtime-128.png');r['path']='wagon-horse-420/idle.png';r['derivation']={'method':'resize','filter':'lanczos','sourceSha256':s['sha256']}
a=dict(id='supply-wagon-horse-idle-d0-415',family='unit.wagon',kind='unit',state='idle',direction=0,candidate=True,review={'status':'CANDIDATE'},source=s,runtime=r,cell={'width':128,'height':128},pivot={'x':654/1254*256,'y':1140/1254*256,'space':'source'},render={'width':112,'height':112},alphaPolicy='transparent',contactShadow={'mode':'baked'},frames=[{'x':0,'y':0,'width':128,'height':128,'durationMs':1000}],loop=True,notes='Whole built-in 2D horse+cart idle D0 static candidate. Logical scale PROVISIONAL; root actual scene required. No motion or eight-direction acceptance.')
(p/'descriptor.json').write_text(json.dumps(a,indent=2))
receipt=dict(status='CLOSED_SOURCE_CANDIDATE_PENDING_ROOT_ACTUAL_SCENE',profile='gpt-6.1-sol/low',calls=1,retries=0,callOpen=False,toolReturnedClosed=True,generatedOriginal=str(original),raw=record('raw.png'),actualCanvas=list(im.size),alphaExtrema=list(im.getchannel('A').getextrema()),alphaBBox=im.getchannel('A').getbbox(),normalizedPivot=[654/1254,1140/1254],transform='uniform whole canvas Lanczos only',scaleAcceptance='PROVISIONAL',installation=False,motionCoverage=False,descriptor='descriptor.json')
(p/'receipt.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2))
