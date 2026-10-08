#!/usr/bin/env python3
"""Complete selected actual gather8 only; reuse frozen017 packaging, never fill slots."""
import sys,json,importlib.util,hashlib,shutil,argparse
from pathlib import Path
from PIL import Image
sys.dont_write_bytecode=True
ROOT=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');TOOL=ROOT/'docs/art/pipeline/pure2d-action-adapter-017/export-v3.py';s=importlib.util.spec_from_file_location('action017',TOOL);a=importlib.util.module_from_spec(s);s.loader.exec_module(a)
DURATIONS=[170,130,160,80,100,110,150,180]
def build(job_path,out):
 job_path=Path(job_path).resolve();j=json.loads(job_path.read_text());out=Path(out).resolve();a.check(not out.exists(),'New output only')
 a.check(j.get('state')=='gather_wood' and j.get('direction')==1 and j.get('family')=='unit.villager' and j.get('loop') is True,'Exact gather_wood/D1 looping villager declaration required')
 a.check(j.get('sourceCanvas')==[1254,1254] and j.get('runtimeCell')==[128,128] and j.get('renderSize')==[89,89] and j.get('pivot')==[654,1140],'One declared1254->128/render89 family transform required')
 a.check(not j.get('technicalFixture') and 'locomotion' not in j,'Actual stationary work only, no fixtures/travel metadata')
 a.check(j.get('contactShadow')=={'mode':'separate','assetId':'unit-contact-shadow'},'Existing authored separate shadow required')
 frames=j.get('frames',[]);a.check(len(frames)==8 and [f.get('durationMs') for f in frames]==DURATIONS,'Exactly eight actual selected frames with1080ms timing required')
 a.check(all(f.get('events')==[] for f in frames),'No invented gameplay contact markers; this template declares no events')
 # Existing017 verifies actual RGBA/encoded hashes, selection/status receipts and no duplicate/fitted cells before output.
 r=a.export(job_path,out);manifest=json.loads((out/'manifest.json').read_text());asset=manifest['assets'][0];atlas=Image.open(out/'atlas.png').convert('RGBA');shadow=next(x for x in manifest['assets'] if x['id']==asset['contactShadow']['assetId']);sim=Image.open(out/shadow['runtime']['path']).convert('RGBA');sf=shadow['frames'][0];sim=sim.crop((sf['x'],sf['y'],sf['x']+sf['width'],sf['y']+sf['height'])).resize((shadow['render']['width'],shadow['render']['height']),Image.Resampling.LANCZOS)
 images=[];anchor=(140,145)
 for f in asset['frames']:
  canvas=Image.new('RGBA',(280,180),(86,103,75,255));sp=(round(anchor[0]-shadow['pivot']['x']*shadow['render']['width']/shadow['source']['width']),round(anchor[1]-shadow['pivot']['y']*shadow['render']['height']/shadow['source']['height']));canvas.alpha_composite(sim,sp)
  im=atlas.crop((f['x'],f['y'],f['x']+128,f['y']+128)).resize((89,89),Image.Resampling.LANCZOS);canvas.alpha_composite(im,(round(anchor[0]-654*89/1254),round(anchor[1]-1140*89/1254)));images.append(canvas)
 images[0].save(out/'actual-gather-loop.png',save_all=True,append_images=images[1:],duration=DURATIONS,loop=0,disposal=0,blend=0)
 with Image.open(out/'actual-gather-loop.png') as apng:a.check(apng.n_frames==8,'Eight distinct APNG frames required')
 shutil.copyfile(Path(__file__).with_name('loader-preview.html'),out/'loader-preview.html');r.update(status='ACTUAL_GATHER8_TECHNICAL_PREVIEW_ONLY',frozen017ToolSha256=a.sha(TOOL.read_bytes()),apngSha256=a.sha((out/'actual-gather-loop.png').read_bytes()),cycleMs=1080,limits='No art/motion/gameplay contact/owner/runtime approval. Stationary local preview only.');(out/'gather-receipt.json').write_text(json.dumps(r,indent=2)+'\n');return r
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('job');p.add_argument('new_output');args=p.parse_args();print(json.dumps(build(args.job,args.new_output),indent=2))
