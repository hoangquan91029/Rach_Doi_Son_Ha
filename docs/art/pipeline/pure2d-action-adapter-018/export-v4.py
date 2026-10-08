#!/usr/bin/env python3
"""Selected ordered whole-canvas action frames -> candidate exact-cell atlas; no approval."""
import argparse, hashlib, importlib.util, json, math, re, sys, copy, shutil
sys.dont_write_bytecode=True
from pathlib import Path
from PIL import Image, ImageDraw
CONTRACT=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha/scripts/validate-art-assets.py')
spec=importlib.util.spec_from_file_location('raster_contract',CONTRACT); contract=importlib.util.module_from_spec(spec);spec.loader.exec_module(contract)
check=contract.check; sha=contract.sha
CAMERA={'projection':'dimetric','ratio':[2,1],'tile':[54,27],'elevation':26.565}
def dims(v,label):
 check(isinstance(v,list) and len(v)==2,label+' requires [width,height]')
 contract.dimensions(dict(zip(['width','height'],v)),label);return tuple(v)
def resolved(base,path):
 check(isinstance(path,str) and bool(path),'Missing custody path');p=Path(path);return p.resolve() if p.is_absolute() else (base/p).resolve()
def pin(path,expected):
 check(path.is_file(),'Missing custody file '+str(path));check(isinstance(expected,str) and contract.SHA.fullmatch(expected) and sha(path.read_bytes())==expected.lower(),'Custody hash mismatch '+str(path))
def shadow_dependency(job,base):
 dep=job.get('shadowDependency',{});mp=resolved(base,dep.get('manifestPath'));pin(mp,dep.get('manifestSha256'));m=json.loads(mp.read_text());check(m.get('schemaVersion')==1,'Shadow manifest schema mismatch')
 matches=[a for a in m.get('assets',[]) if a.get('id')=='unit-contact-shadow'];check(len(matches)==1,'Missing unique authored shadow dependency');a=copy.deepcopy(matches[0])
 check(sha(json.dumps(a,sort_keys=True,separators=(',',':')).encode())==dep.get('assetSha256'),'Shadow asset contract pin mismatch')
 check(a.get('kind')=='vfx' and a.get('state')=='static' and a.get('direction') is None and a.get('contactShadow')=={'mode':'none'} and a.get('candidate') is True and a.get('review')=={'status':'CANDIDATE'},'Authored candidate shadow contract mismatch')
 validation=contract.validate_asset(a,mp.parent,mp.parent,False)
 custody=dep.get('sourceReceipt',{});cp=resolved(base,custody.get('path'));pin(cp,custody.get('sha256'));c=json.loads(cp.read_text());check(c.get('status')=='CANDIDATE' and c.get('source')==a['source'],'Authored shadow original receipt mismatch')
 a['source']['path']=str(resolved(mp.parent,a['source']['path']));runtime_path=resolved(mp.parent,a['runtime']['path'])
 return a,runtime_path,validation

def preflight(job_path):
 job_path=Path(job_path).resolve();job=json.loads(job_path.read_text());base=job_path.parent
 check(isinstance(job.get('state'),str) and re.fullmatch(r'[a-z][a-z0-9_]{0,63}',job['state']),'Explicit action state string required')
 check(isinstance(job.get('loop'),bool),'Explicit loop boolean required')
 check(job['state']!='death' or job['loop'] is False,'Death must hold terminal frame')
 if 'locomotion' in job:check((job['state']=='walk' or job['state']=='carry' or job['state'].startswith('carry_')) and isinstance(job['locomotion'],dict) and contract.number(job['locomotion'].get('distancePerCycle')) and job['locomotion']['distancePerCycle']>0,'Invalid movement locomotion')
 check(job.get('wholeCanvasTransform')=='UNIFORM_LANCZOS_NO_CROP_SHIFT_FIT','Explicit whole-canvas transform required')
 canvas=dims(job['sourceCanvas'],'sourceCanvas');cell=dims(job['runtimeCell'],'runtimeCell');render=dims(job['renderSize'],'renderSize')
 check(cell[0]*canvas[1]==cell[1]*canvas[0],'Unequal uniform rescale');check(render[0]*cell[1]==render[1]*cell[0],'Distorted render size')
 check(cell[0]<=canvas[0] and cell[1]<=canvas[1],'Do not invent source detail by upscaling')
 pivot=job['pivot'];check(isinstance(pivot,list) and len(pivot)==2 and all(contract.number(n) and 0<=n<=canvas[i] for i,n in enumerate(pivot)),'Invalid shared source pivot')
 check(job.get('camera')==CAMERA,'Declare existing runtime camera metadata; no physical3D production dependency')
 check(contract.integer(job.get('direction')) and 0<=job['direction']<=7,'Explicit engine direction required')
 check(isinstance(job.get('id'),str) and re.fullmatch(r'[A-Za-z0-9_.-]{1,120}',job['id']),'Invalid id')
 check(isinstance(job.get('family'),str) and job['family'],'Explicit family required')
 check(job.get('contactShadow') in [{'mode':'baked'},{'mode':'separate','assetId':'unit-contact-shadow'}],'Declare honest baked shadow or existing unit-contact-shadow dependency')
 if job['contactShadow']['mode']=='separate': shadow_dependency(job,base)
 fixture=job.get('technicalFixture',False);check(isinstance(fixture,bool),'technicalFixture must be boolean')
 check(job.get('sourceMethod')==('NON_ART_TEST_ONLY' if fixture else 'FINISHED_WHOLE_2D_FRAMES'),'Finished whole2D frames required; no proxy or assembly')
 frames=job.get('frames');check(isinstance(frames,list) and 1<=len(frames)<=256,'Require1..256 complete ordered frames')
 images=[];records=[];seen=set()
 for i,f in enumerate(frames):
  check(f.get('index')==i and f.get('phase',f'F{i}')==f'F{i}','Ordered F0..Fn required')
  check(f.get('selectionStatus') in (['NON_ART_TEST_ONLY'] if fixture else ['SELECTED_FRAME_CANDIDATE','SELECTED_KEY_CANDIDATE','SELECTED_INBETWEEN_CANDIDATE']),'Held/missing/rejected/unselected frame forbidden')
  if not fixture and f['selectionStatus']!='SELECTED_FRAME_CANDIDATE':check(job['state']=='walk' and len(frames)==8 and f['selectionStatus']==('SELECTED_KEY_CANDIDATE' if i in [0,2,4,6] else 'SELECTED_INBETWEEN_CANDIDATE'),'Legacy selection statuses require actual eight-frame walk')
  check(not any(k in f for k in ['crop','trim','scale','renderSize','runtimeCell','transform','offset']),'Per-frame fitting/transform forbidden')
  check(f.get('pivot',pivot)==pivot,'Per-frame pivot fitting forbidden')
  check(contract.number(f.get('durationMs')) and 0<f['durationMs']<=60000,'Invalid duration')
  events=f.get('events');check(isinstance(events,list) and len(events)<=32,'Explicit events list required')
  for e in events:check(isinstance(e,dict) and isinstance(e.get('name'),str) and re.fullmatch(r'[A-Z][A-Z0-9_]{0,63}',e['name']) and contract.integer(e.get('offsetMs')) and 0<=e['offsetMs']<f['durationMs'],'Invalid event')
  source=dict(f['source']);p=resolved(base,source['path']);source['path']=str(p)
  check((source.get('width'),source.get('height'))==canvas,'Inconsistent source canvas')
  im,receipt=contract.image_file(source,base,f'F{i}','transparent',True)
  check(receipt['rgbaSha256'] not in seen,'Duplicate source frame is not a distinct completed phase');seen.add(receipt['rgbaSha256'])
  custody=f['selectionReceipt'];rp=resolved(base,custody['path']);pin(rp,custody['sha256']);r=json.loads(rp.read_text())
  check(r.get('status')==f['selectionStatus'] and r.get('frameIndex')==i and r.get('sourceSha256')==source['sha256'] and r.get('rgbaSha256')==source['rgbaSha256'],'Selection receipt must bind exact frame/status')
  images.append(im);records.append(source)
 cols=job.get('columns',min(4,len(frames)));g=job.get('gutter',0)
 if len(frames)==1:check(cols==1 and g==0,'Single frame requires one exact cell without gutters')
 check(contract.integer(cols) and 1<=cols<=8 and contract.integer(g) and 0<=g<=64,'Invalid columns/gutter')
 rows=math.ceil(len(frames)/cols);atlas_size=(cols*(cell[0]+2*g),rows*(cell[1]+2*g));dims(list(atlas_size),'atlas')
 return job,images,records,atlas_size

def export(job_path,out):
 out=Path(out).resolve();check(not out.exists(),'Refusing existing output directory')
 job,images,records,size=preflight(job_path);cell=job['runtimeCell'];g=job.get('gutter',0);cols=job.get('columns',min(4,len(images)))
 atlas=Image.new('RGBA',size);frames=[];time=0
 for i,(im,source) in enumerate(zip(images,records)):
  runtime=im if im.size==tuple(cell) else im.resize(tuple(cell),Image.Resampling.LANCZOS)
  x=i%cols*(cell[0]+2*g)+g;y=i//cols*(cell[1]+2*g)+g;atlas.paste(runtime,(x,y))
  frames.append(dict(index=i,phase=f'F{i}',x=x,y=y,width=cell[0],height=cell[1],durationMs=job['frames'][i]['durationMs'],events=job['frames'][i]['events'],source=source,pivot={'x':job['pivot'][0],'y':job['pivot'][1],'space':'source'},timeMs=time,selectionStatus=job['frames'][i]['selectionStatus'],selectionReceipt=job['frames'][i]['selectionReceipt']));time+=frames[-1]['durationMs']
 out.mkdir(parents=False);atlas.save(out/'atlas.png')
 runtime={'path':'atlas.png','sha256':sha((out/'atlas.png').read_bytes()),'rgbaSha256':sha(atlas.tobytes()),'width':size[0],'height':size[1],'derivation':{'method':'atlas','filter':'lanczos','sourceSha256':records[0]['sha256']}}
 asset=dict(id=job['id'],family=job['family'],kind='unit',state=job['state'],direction=job['direction'],source=records[0],runtime=runtime,cell=dict(zip(['width','height'],cell)),render=dict(zip(['width','height'],job['renderSize'])),pivot={'x':job['pivot'][0],'y':job['pivot'][1],'space':'source'},alphaPolicy='transparent',contactShadow=job['contactShadow'],candidate=True,review={'status':'CANDIDATE'},loop=job['loop'],frames=frames)
 if 'locomotion' in job:asset['locomotion']=job['locomotion']
 if len(frames)==1 and g==0:
  asset['runtime']['derivation']['method']='copy' if tuple(cell)==images[0].size else 'resize'
 label='NON_ART_TEST_ONLY' if job.get('technicalFixture') else 'CANDIDATE_TECHNICAL_CUSTODY_ONLY'
 manifest={'schemaVersion':1,'status':'CANDIDATE','camera':job['camera'],'notes':label+'; no visual/motion/owner/runtime/production approval','assets':[asset]}
 shadow_preview=None
 if job['contactShadow']['mode']=='separate':
  shadow,shadow_path,shadow_validation=shadow_dependency(job,Path(job_path).resolve().parent);dest='unit-contact-shadow'+shadow_path.suffix;shutil.copyfile(shadow_path,out/dest);shadow['runtime']['path']=dest;manifest['assets'].append(shadow);shadow_preview=shadow
 (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 # Reuse authoritative validator: exact decoded cells + transparent unused gutters.
 validation=contract.validate_manifest(out/'manifest.json')
 check(validation.get('packaging')=='PASS','Existing packaging validator failed: '+json.dumps(validation))
 rw,rh=job['renderSize'];slot=max(rw,180);sheet=Image.new('RGBA',(cols*slot,math.ceil(len(frames)/cols)*(rh+36)),(45,55,48,255));draw=ImageDraw.Draw(sheet)
 for f in frames:
  im=atlas.crop((f['x'],f['y'],f['x']+cell[0],f['y']+cell[1])).resize((rw,rh),Image.Resampling.LANCZOS);x=f['index']%cols*slot;y=f['index']//cols*(rh+36);sheet.alpha_composite(im,(x+(slot-rw)//2,y));draw.text((x,y+rh),f"F{f['index']} {f['durationMs']}ms",fill='white')
 sheet.save(out/'contact-sheet.png')
 (out/'preview.json').write_text(json.dumps({'status':label,'render':asset['render'],'cell':asset['cell'],'sourceCanvas':job['sourceCanvas'],'sourcePivot':job['pivot'],'frames':frames,'loop':job['loop'],'cycleDurationMs':time,'shadow':shadow_preview},indent=2)+'\n')
 (out/'preview.html').write_text(Path(__file__).with_name('preview-v4.html').read_text())
 receipt={'status':label,'jobSha256':sha(Path(job_path).read_bytes()),'contractValidatorSha256':sha(CONTRACT.read_bytes()),'packagingValidation':validation,'runtimePivot':[job['pivot'][i]*cell[i]/job['sourceCanvas'][i] for i in range(2)],'uniformScale':cell[0]/job['sourceCanvas'][0],'gutter':g,'gutterPolicy':'transparent zero padding only; no extrusion/trim','cycleDurationMs':time,'frames':len(frames),'outputs':{p.name:sha(p.read_bytes()) for p in out.iterdir() if p.is_file()},'limits':'Technical packaging only. Preview is actual declared-frame local playback; no travel/foot-lock/cadence/identity/owner/runtime approval.'}
 (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');return receipt
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('job',type=Path);p.add_argument('output',type=Path);a=p.parse_args();print(json.dumps(export(a.job,a.output),indent=2))
