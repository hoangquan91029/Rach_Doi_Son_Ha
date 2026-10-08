#!/usr/bin/env python3
"""Actual8 atlas -> fixed-anchor game-size APNG; technical preview, no approval."""
import argparse,hashlib,json,math,shutil
from pathlib import Path
from PIL import Image,ImageDraw
sha=lambda b:hashlib.sha256(b).hexdigest()
def require(ok,msg):
 if not ok:raise ValueError(msg)
def load_actual(base,meta):
 p=base/meta['path'];require(p.is_file(),'Missing actual runtime image');require(sha(p.read_bytes())==meta['sha256'],'Runtime encoded pin mismatch');im=Image.open(p).convert('RGBA');require(im.size==(meta['width'],meta['height']),'Runtime size mismatch');require(sha(im.tobytes())==meta['rgbaSha256'],'Runtime RGBA pin mismatch');return im

def build(job_path,out):
 job_path=Path(job_path).resolve();job=json.loads(job_path.read_text());base=Path(job['compiledDirectory']).resolve();out=Path(out).resolve();require(not out.exists(),'Refusing existing output');mp=base/'manifest.json';pp=base/'preview.json'
 require(sha(mp.read_bytes())==job['manifestSha256'] and sha(pp.read_bytes())==job['previewSha256'],'Parent supplied compiled metadata pins mismatch')
 manifest=json.loads(mp.read_text());preview=json.loads(pp.read_text());require(manifest.get('schemaVersion')==1 and manifest.get('status')=='CANDIDATE','Existing candidate schema required');assets=[a for a in manifest['assets'] if a.get('state')=='walk'];require(len(assets)==1,'One actual walk atlas required');a=assets[0];frames=a['frames'];require(len(frames)==8 and [f.get('index') for f in frames]==list(range(8)) and preview['frames']==frames,'Actual complete ordered eight frames and matching preview required')
 require(all(f.get('selectionStatus') in ['SELECTED_KEY_CANDIDATE','SELECTED_INBETWEEN_CANDIDATE'] for f in frames),'No held/partial/non-art fixtures as motion preview');require('NON_ART' not in preview['status'],'No synthetic motion proof')
 require(preview['sourceCanvas']==[a['source']['width'],a['source']['height']] and preview['sourcePivot']==[a['pivot']['x'],a['pivot']['y']],'Shared pivot/canvas mismatch')
 require(preview['render']==a['render'] and preview['cell']==a['cell'],'Compiled preview layout mismatch')
 atlas=load_actual(base,a['runtime']);cell=(a['cell']['width'],a['cell']['height']);source=preview['sourceCanvas'];require(cell[0]*source[1]==cell[1]*source[0],'Unequal family scale')
 require(all(isinstance(f['durationMs'],int) and 0<f['durationMs']<=60000 for f in frames),'Integer declared durations required for exact APNG playback')
 nominal=job.get('nominalHeight',80);ref=job.get('referenceHeight',1130);require(nominal in [64,80,96] and ref==1130,'Explicit family1130 reference/64,80,96 nominal required');draw=tuple(round(nominal/ref*n) for n in source);require(draw==tuple(a['render'][k] for k in ['width','height']),'Compile declared full-canvas renderSize to rounded nominal/reference transform first; no hidden scale override')
 shadow=None;shadow_meta=None
 if a['contactShadow']['mode']=='separate':
  matches=[s for s in manifest['assets'] if s['id']==a['contactShadow']['assetId']];require(len(matches)==1,'Missing actual shadow dependency');shadow_meta=matches[0];require(preview.get('shadow')==shadow_meta,'Shadow preview contract mismatch');shadow=load_actual(base,shadow_meta['runtime'])
 elif a['contactShadow']['mode']!='baked':raise ValueError('Honest shadow declaration required')
 size=(280,180);anchor=(140,145);images=[]
 for f in frames:
  x,y,w,h=(f[k] for k in ['x','y','width','height']);require((w,h)==cell and min(x,y)>=0 and x+w<=atlas.width and y+h<=atlas.height,'Invalid exact atlas cell')
  canvas=Image.new('RGBA',size,(86,103,75,255));d=ImageDraw.Draw(canvas);d.line((0,anchor[1],size[0],anchor[1]),fill=(139,156,120,255),width=1)
  if shadow is not None:
   s=shadow_meta;sf=s['frames'][0];rw,rh=[s['render'][k] for k in ['width','height']];sim=shadow.crop((sf['x'],sf['y'],sf['x']+sf['width'],sf['y']+sf['height'])).resize((rw,rh),Image.Resampling.LANCZOS);pos=tuple(round(anchor[i]-s['pivot'][['x','y'][i]]*[rw,rh][i]/s['source'][['width','height'][i]]) for i in range(2));canvas.alpha_composite(sim,pos)
  # Extract exact packed cell only; no source trimming/fitting. Fixed common draw transform.
  im=atlas.crop((x,y,x+w,y+h)).resize(draw,Image.Resampling.LANCZOS);pos=tuple(round(anchor[i]-preview['sourcePivot'][i]*draw[i]/source[i]) for i in range(2));canvas.alpha_composite(im,pos);images.append(canvas)
 out.mkdir(parents=False);images[0].save(out/'actual-eight-frame-loop.png',save_all=True,append_images=images[1:],duration=[f['durationMs'] for f in frames],loop=0,disposal=0,blend=0)
 with Image.open(out/'actual-eight-frame-loop.png') as apng:require(apng.n_frames==8,'APNG did not retain eight declared cells')
 shutil.copyfile(Path(__file__).with_name('preview-v3.html'),out/'preview-v3.html');shutil.copyfile(mp,out/'manifest.json');shutil.copyfile(pp,out/'preview.json');shutil.copyfile(base/a['runtime']['path'],out/a['runtime']['path'])
 if shadow is not None:shutil.copyfile(base/shadow_meta['runtime']['path'],out/shadow_meta['runtime']['path'])
 receipt={'status':'ACTUAL_EIGHT_FRAME_TECHNICAL_PLAYBACK_NOT_APPROVAL','jobSha256':sha(job_path.read_bytes()),'compiledManifestSha256':job['manifestSha256'],'compiledPreviewSha256':job['previewSha256'],'frames':8,'nominalHeight':nominal,'referenceHeight':ref,'drawCanvas':draw,'drawRounding':'round(sourceCanvas*nominal1130ratio); requires exact compiled renderSize match','sharedGroundAnchor':anchor,'sourcePivot':preview['sourcePivot'],'durationsMs':[f['durationMs'] for f in frames],'cycleDurationMs':sum(f['durationMs'] for f in frames),'apngEncodedSha256':sha((out/'actual-eight-frame-loop.png').read_bytes()),'limits':'Actual full8local playback only; no travel/foot-lock/owner/runtime/motion acceptance.'};(out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');return receipt
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('job');p.add_argument('new_output');args=p.parse_args();print(json.dumps(build(args.job,args.new_output),indent=2))
