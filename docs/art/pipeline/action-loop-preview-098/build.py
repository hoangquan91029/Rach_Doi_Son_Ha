#!/usr/bin/env python3
"""Thin actual whole-frame preview extension of frozen017; never fills slots."""
import argparse,importlib.util,json,math,sys
from pathlib import Path
from PIL import Image
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[4]
TOOL=ROOT/'docs/art/pipeline/pure2d-action-adapter-017/export-v3.py'
spec=importlib.util.spec_from_file_location('frozen017',TOOL);a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
def build(job,out):
 job=Path(job).resolve();out=Path(out).resolve();j=json.loads(job.read_text());a.check(not j.get('technicalFixture'),'Actual selected whole illustrations only; fixtures forbidden')
 receipt=a.export(job,out) # All custody, distinct frames, canvas, alpha, timing, events and shadow validation remains017.
 manifest=json.loads((out/'manifest.json').read_text());asset=manifest['assets'][0];assets=[asset]
 if asset['contactShadow']['mode']=='separate':assets.insert(0,next(x for x in manifest['assets'] if x['id']==asset['contactShadow']['assetId']))
 bounds=[(-x['pivot']['x']*x['render']['width']/x['source']['width'],-x['pivot']['y']*x['render']['height']/x['source']['height'],x['render']['width'],x['render']['height']) for x in assets]
 left=min(x for x,y,w,h in bounds);top=min(y for x,y,w,h in bounds);right=max(x+w for x,y,w,h in bounds);bottom=max(y+h for x,y,w,h in bounds)
 layout={'width':math.ceil(right-left)+48,'height':math.ceil(bottom-top)+48,'anchor':[24-left,24-top],'background':'#56674b'}
 images={x['id']:Image.open(out/x['runtime']['path']).convert('RGBA') for x in assets};frames=[]
 for f in asset['frames']:
  canvas=Image.new('RGBA',(layout['width'],layout['height']),(86,103,75,255))
  for x,(dx,dy,w,h) in zip(assets,bounds):
   cell=f if x is asset else x['frames'][0];im=images[x['id']].crop((cell['x'],cell['y'],cell['x']+cell['width'],cell['y']+cell['height'])).resize((w,h),Image.Resampling.LANCZOS)
   canvas.alpha_composite(im,(round(layout['anchor'][0]+dx),round(layout['anchor'][1]+dy)))
  frames.append(canvas)
 durations=[f['durationMs'] for f in asset['frames']]
 frames[0].save(out/'actual-action.png',save_all=True,append_images=frames[1:],duration=durations,loop=0 if asset['loop'] else 1,disposal=0,blend=0)
 with Image.open(out/'actual-action.png') as im:
  a.check(im.n_frames==len(frames),'APNG changed declared distinct frame count')
  if len(frames)>1:
   a.check(im.info['loop']==(0 if asset['loop'] else 1),'APNG loop/terminal policy mismatch')
   for i,d in enumerate(durations):im.seek(i);a.check(abs(im.info['duration']-d)<0.01,'APNG timing mismatch')
 (out/'preview-layout.json').write_text(json.dumps(layout,indent=2)+'\n');(out/'loader-preview.html').write_text(Path(__file__).with_name('loader-preview.html').read_text())
 receipt.update(status='ACTUAL_ACTION_TECHNICAL_PREVIEW_ONLY',state=asset['state'],direction=asset['direction'],loop=asset['loop'],frozen017ToolSha256=a.sha(TOOL.read_bytes()),helperSha256=a.sha(Path(__file__).read_bytes()),outputs={p.name:a.sha(p.read_bytes()) for p in out.iterdir() if p.is_file() and p.name not in ['receipt.json','action-preview-receipt.json']},limits='Whole actual selected frames only. No generated slots, gameplay event invention, visual/motion/foot-lock/owner/runtime approval. Nonloop APNG plays once; real loader holds terminal frame.')
 (out/'action-preview-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');return receipt
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('job');p.add_argument('new_output');args=p.parse_args();print(json.dumps(build(args.job,args.new_output),indent=2))
