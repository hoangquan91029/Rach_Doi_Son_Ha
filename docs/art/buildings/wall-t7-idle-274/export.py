from pathlib import Path
from PIL import Image
import json,hashlib,shutil,sys
p=Path(__file__).parent;native=Path(sys.argv[1]);shutil.copyfile(native,p/'raw.png')
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
def pin(n):
 f=p/n;im=Image.open(f).convert('RGBA');return {'path':n,'sha256':sha(f),'rgbaSha256':hashlib.sha256(im.tobytes()).hexdigest(),'width':im.width,'height':im.height}
im=Image.open(p/'raw.png').convert('RGBA')
assert im.size==(1254,1254),im.size
for n,size in [('runtime.png',128),('working.png',256),('preview42.png',42)]:im.resize((size,size),Image.Resampling.LANCZOS).save(p/n)
s,r=pin('raw.png'),pin('runtime.png');r['derivation']={'method':'resize','filter':'lanczos','sourceSha256':s['sha256']}
c={'id':'wall-whole-274-mask7','family':'building.wall','kind':'building','state':'idle','direction':None,'candidate':True,'review':{'status':'CANDIDATE'},'source':s,'runtime':r,'cell':{'width':128,'height':128},'pivot':{'x':627,'y':900,'space':'source'},'render':{'width':42.3225,'height':42.3225},'alphaPolicy':'transparent','contactShadow':{'mode':'baked'},'frames':[{'x':0,'y':0,'width':128,'height':128,'durationMs':1000}],'loop':True,'fortification':{'mask':7},'notes':'Whole +X/-X/+Y T junction candidate; mask only, no wallaxis. Living completed idle only. Actual joins and alpha picking unverified.'}
(p/'candidate.json').write_text(json.dumps(c,indent=2))
for n in ['call-state.json','live-handle.json']:(p/n).write_text(json.dumps({'state':'returned_closed','calls':1,'retries':0,'toolNativePath':str(native),'routing':'gpt-6.1-sol/low'},indent=2))
(p/'tool-result.json').write_text(json.dumps({'toolNativePath':str(native),'returned':True,'imageDataOmitted':True},indent=2))
(p/'output-pins.json').write_text(json.dumps({n:pin(n) for n in ['raw.png','runtime.png','working.png','preview42.png']},indent=2))
(p/'receipt.json').write_text(json.dumps({'status':'CANDIDATE_ROOT_INTAKE_PENDING','calls':1,'retries':0,'callState':'returned_closed','source':s,'runtime':r,'working':pin('working.png'),'preview':pin('preview42.png'),'alphaExtrema':im.getchannel('A').getextrema(),'fixedLayout':{'source':[1254,1254],'pivot':[627,900],'cell':[128,128],'logicalRender':42.3225,'fit':False,'shift':False,'mirror':False},'fortification':{'mask':7},'runtimeInstalled':False,'publicPromoted':False,'networkAPIcalls':0,'next':'Root intake then separate finite actual UI T joins/picking trial'},indent=2))
