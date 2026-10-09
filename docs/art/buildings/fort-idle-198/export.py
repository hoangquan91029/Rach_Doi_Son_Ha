"""Uniform whole-canvas derivatives only; preserve exact raw/tool custody."""
from pathlib import Path
from PIL import Image
import json,hashlib
p=Path(__file__).resolve().parent
im=Image.open(p/'raw.png').convert('RGBA')
assert im.size==(1254,1254)
for name,size in [('working.png',512),('runtime.png',256),('preview-112.png',112),('preview-default-121.png',121)]:
 im.resize((size,size),Image.Resampling.LANCZOS).save(p/name)
def record(name):
 data=(p/name).read_bytes();a=Image.open(p/name).convert('RGBA')
 return {'path':name,'sha256':hashlib.sha256(data).hexdigest(),'rgbaSha256':hashlib.sha256(a.tobytes()).hexdigest(),'width':a.width,'height':a.height,'bbox':a.getchannel('A').getbbox(),'alphaExtrema':a.getchannel('A').getextrema()}
raw=record('raw.png')
metadata={'schema':'rds-whole-building-candidate/v1','id':'fort-idle-198','family':'building.fort','kind':'building','state':'idle','direction':None,'candidate':True,'review':{'status':'CANDIDATE','visualAccepted':False,'installed':False,'sceneAccepted':False},'source':raw,'working':record('working.png'),'runtime':{**record('runtime.png'),'derivation':{'method':'resize','filter':'lanczos','sourceSha256':raw['sha256'],'wholeCanvas':True,'crop':False,'fit':False}},'cell':{'width':256,'height':256},'pivot':{'x':627,'y':1010,'space':'source','status':'PROVISIONAL_REFERENCE_FAMILY_BASE_CENTER_NEEDS_ACTUAL_SCENE_INTAKE'},'render':{'width':112,'height':112},'contactShadow':{'mode':'baked'},'alphaPolicy':'transparent','frames':[{'x':0,'y':0,'width':256,'height':256,'durationMs':1000}],'loop':True,'preview':[record('preview-112.png'),record('preview-default-121.png')],'layoutReason':'Whole compact defensive fort candidate; same whole1254family transform512working/256runtime/112logicalcell. Idle only, otherstates unresolved.'}
json.dump(metadata,open(p/'candidate.json','w'),indent=2)
print(json.dumps({'rawSHA':raw['sha256'],'runtimeSHA':metadata['runtime']['sha256'],'runtimeRGBABytes':256*256*4,'sourceSize':im.size}))
