#!/usr/bin/env python3
"""Compile complete illustrated originals; preserves full source canvas, never fits bounds.
Metadata checks do not establish visible motion/contact/identity acceptance.
"""
import argparse,hashlib,json,math,pathlib
from PIL import Image,ImageDraw
DURATIONS=[80,70,80,70,80,70,80,70]
SUPPORT=['LEFT']*4+['RIGHT']*4
PHASES=['LEFT_CONTACT','LEFT_DOWN','RIGHT_PASSING','LEFT_PUSH','RIGHT_CONTACT','RIGHT_DOWN','LEFT_PASSING','RIGHT_PUSH']
KEYS=[0,2,4,6]
def sha(data):return hashlib.sha256(data).hexdigest()
def require(ok,text):
 if not ok:raise ValueError(text)
def frame_at(durations,time_ms):
 cycle=sum(durations);t=time_ms%cycle
 for i,duration in enumerate(durations):
  if t<duration:return i
  t-=duration
 raise AssertionError('invalid timing')
def checked_image(path,expected=None):
 raw=path.read_bytes();image=Image.open(path);require(image.mode=='RGBA','Original must be RGBA');image.load()
 if expected:require(sha(raw)==expected,'Original byte custody mismatch: '+str(path))
 return image,{'sha256':sha(raw),'rgbaSha256':sha(image.tobytes()),'dimensions':list(image.size),'width':image.width,'height':image.height}
def preflight(path):
 job=json.loads(path.read_text());base=path.parent
 require(job.get('direction')=={'name':'SOUTH','screen':'down','engine':'D01','world':'SE'},'South must explicitly remain screen-down D01/worldSE; D00 is not South')
 require(job.get('canvas')==[1254,1254] and job.get('worldScale')==38/1254,'One fixed whole-canvas presentation scale required')
 identity=job.get('identityTurnaround',{});directions=['N','NE','E','SE','S','SW','W','NW'];lock_frames=identity.get('frames',{})
 require(set(lock_frames)==set(directions),'Actual eight-direction static identity lock required BEFORE animation authoring')
 require(identity.get('canvas')==[1254,1254] and identity.get('camera')=={'projection':'dimetric','ratio':[2,1],'tile':[54,27],'elevation':26.565},'Static identity camera/canvas mismatch')
 lock_review=identity.get('review',{})
 require(lock_review.get('reviewer') and lock_review.get('receiptPath') and lock_review.get('receiptSha256'),'Sealed static identity review receipt required')
 require(sha((base/lock_review['receiptPath']).read_bytes())==lock_review['receiptSha256'],'Static identity review receipt custody mismatch')
 for direction in directions:
  original=lock_frames[direction];require(original.get('path') and original.get('sha256') and original.get('fullBodyInspected') is True,'Actual inspected full-body static original required: '+direction)
  static,record=checked_image(base/original['path'],original['sha256']);require(static.size==(1254,1254),'Static identity canvas mismatch: '+direction)
  require(lock_review.get('frameHashes',{}).get(direction)==record['sha256'],'Identity review must bind actual static original: '+direction)
 stride=job.get('qaStrideWorldTiles')
 if stride is not None:require(isinstance(stride,(int,float)) and math.isfinite(stride) and 0<stride<4 and job.get('qaStrideStatus')=='REACHABLE_CONTACT_HYPOTHESIS','Grid travel requires disclosed measured reachable-stride hypothesis')
 require(job.get('sourceMethod') in ['CONTROLLED_FINISHED_ILLUSTRATED_FRAMES','CONTROLLED_BAKED_AND_FINISHED_FRAMES'],'Finished whole-character frames only, not runtime rig parts')
 require(job.get('groundPivot') and len(job['groundPivot'])==2 and all(isinstance(n,(int,float)) and math.isfinite(n) and 0<=n<=1254 for n in job['groundPivot']),'Explicit shared source ground pivot required')
 ref=job.get('southReference',{});require(ref.get('path') and ref.get('sha256') and ref.get('viewReviewReceipt'),'Inspected real South directional reference required')
 reference,_=checked_image(base/ref['path'],ref['sha256']);require(reference.size==(1254,1254),'South reference canvas mismatch')
 require(job.get('pivotStatus')=='SEALED_FROM_SOUTH_REFERENCE','Proposed pivot must be confirmed and sealed on real South reference')
 require(ref['sha256']==lock_frames['S']['sha256'],'South directional reference must be the sealed S turnaround original')
 require(ref['sha256']!='145b976ffd1bdf563cb5da78806547e6849424054f2c26fc297e155a0b366e94','D00 master cannot be relabeled South directional art')
 review=job.get('keyPoseReview',{});require(review.get('reviewer') and review.get('supportGatePass') is True and review.get('receiptPath') and review.get('receiptSha256'),'Four real key-pose review receipt required before in-between compilation')
 require(sha((base/review['receiptPath']).read_bytes())==review['receiptSha256'],'Key review receipt byte binding mismatch')
 frames=job.get('frames',[]);require(len(frames)==8,'Exactly eight finished walk frames required');images=[];custody=[]
 for index,f in enumerate(frames):
  require(f.get('index')==index and f.get('support')==SUPPORT[index] and f.get('swing')==('RIGHT' if index<4 else 'LEFT'),'Binary LEFT/RIGHT contact declaration failed')
  require(f.get('durationMs')==DURATIONS[index],'Initial reviewed variable timing80/70/80/70x2 required')
  require(f.get('pivot',job['groundPivot'])==job['groundPivot'],'Per-frame pivot fit forbidden')
  require(f.get('originalSha256') and f.get('custodyReceipt'),'Original frame/authoring custody missing')
  image,record=checked_image(base/f['path'],f['originalSha256']);require(image.size==(1254,1254),'Source canvas change forbidden')
  if index in KEYS:require(review.get('frameHashes',{}).get(str(index))==record['sha256'],'Key receipt must bind actual selected frame '+str(index))
  require(f.get('method')!='PAPER_PUPPET_PROXY','Geometry/part proxy is not a finished frame')
  images.append(image);custody.append({**record,'path':f['path'],'originalPath':f['path'],'custodyReceipt':f['custodyReceipt']})
 return job,images,custody

def compile_atlas(path,out,cell=256):
 require(isinstance(cell,int) and cell>=256 and cell<=1254,'Runtime whole-canvas cell must be256..1254')
 require(not out.exists() or not any(out.iterdir()),'Existing compilation output must not be overwritten')
 job,images,custody=preflight(path);out.mkdir(parents=True,exist_ok=True)
 atlas=Image.new('RGBA',(4*cell,2*cell));frames=[];time=0
 for index,image in enumerate(images):
  runtime=image if cell==1254 else image.resize((cell,cell),Image.Resampling.LANCZOS)
  x=index%4*cell;y=index//4*cell;atlas.paste(runtime,(x,y));events=[{'name':'FOOT_CONTACT_'+SUPPORT[index],'offsetMs':0}] if index in [0,4] else []
  frames.append({'index':index,'x':x,'y':y,'width':cell,'height':cell,'rectangle':{'x':x,'y':y,'width':cell,'height':cell},'pivot':{'x':job['groundPivot'][0],'y':job['groundPivot'][1],'space':'source'},'cellPivot':{'x':job['groundPivot'][0]*cell/1254,'y':job['groundPivot'][1]*cell/1254,'space':'cell'},'sourcePivot':job['groundPivot'],'durationMs':DURATIONS[index],'timeMs':time,'phase':PHASES[index],'support':SUPPORT[index],'swing':'RIGHT' if index<4 else 'LEFT','events':events,'source':custody[index]});time+=DURATIONS[index]
 atlas.save(out/'villager-walk-SOUTH.png');raw=(out/'villager-walk-SOUTH.png').read_bytes()
 metadata={'schema':'illustrated-animation-atlas/v1','animation':'walk','state':'walk','unit':'villager','direction':1,'directionName':'SOUTH','directionMapping':job['direction'],'cell':{'width':cell,'height':cell},'render':{'width':38,'height':38},'pivot':{'x':job['groundPivot'][0],'y':job['groundPivot'][1],'space':'source'},'status':'NON_ART_TECHNICAL_FIXTURE' if job.get('technicalFixture') is True else 'CANDIDATE_REVIEW_ONLY','loop':True,'cycleDurationMs':time,'runtimeAtlas':{'path':'villager-walk-SOUTH.png','sha256':sha(raw),'rgbaSha256':sha(atlas.tobytes()),'dimensions':list(atlas.size),'derivation':'uniform whole-canvas Lanczos resize then unmodified cell packing' if cell!=1254 else 'pixel-preserving complete source cell packing'},'frames':frames,'sourceCanvas':[1254,1254],'worldScale':38/1254,'identityTurnaroundReview':job['identityTurnaround']['review'],'keyPoseReview':job['keyPoseReview'],'independentMotionReview':'PENDING','runtimeIntegrated':False,'gameplayAuthority':'Fixed-tick simulation only; browser events never deal damage or transfer resources'}
 (out/'animation.json').write_text(json.dumps(metadata,indent=2));qa(images,job,out)

def qa(images,job,out):
 for size,label in [(1254,'native'),(627,'half'),(38,'gameplay')]:
  pad=8;text_height=36;slot=max(size,180);sheet=Image.new('RGBA',(4*(slot+pad),2*(size+text_height+pad)),(29,44,36,255));draw=ImageDraw.Draw(sheet)
  for index,image in enumerate(images):
   x=index%4*(slot+pad);y=index//4*(size+text_height+pad);sheet.alpha_composite(image.resize((size,size),Image.Resampling.LANCZOS),(x+(slot-size)//2,y));draw.text((x,y+size),f'F{index} SUPPORT:{SUPPORT[index]}',fill='white');draw.text((x,y+size+14),f'SWING:{"RIGHT" if index<4 else "LEFT"}',fill='white')
  sheet.save(out/f'contact-sheet-{label}.png')
 preview=[image.resize((38,38),Image.Resampling.LANCZOS) for image in images];preview[0].save(out/'loop-fixed-38.gif',save_all=True,append_images=preview[1:],duration=DURATIONS,loop=0,disposal=2)
 # Authoring grid diagnostic: supplied reachable stride only, never fabricated gameplay motion.
 stride=job.get('qaStrideWorldTiles')
 if stride is not None:
  require(isinstance(stride,(int,float)) and 0<stride<4 and job.get('qaStrideStatus')=='REACHABLE_CONTACT_HYPOTHESIS','Grid travel requires disclosed measured reachable-stride hypothesis')
  grid=[];cycle=sum(DURATIONS);timeline=range(0,cycle*2,10)
  for time in timeline:
   canvas=Image.new('RGBA',(240,130),(31,46,38,255));draw=ImageDraw.Draw(canvas)
   for x in range(0,240,27):draw.line((x,18,x,130),fill=(87,104,81,255))
   for y in range(22,130,14):draw.line((0,y,240,y),fill=(87,104,81,255))
   draw.text((4,2),'QA GRID / REACHABLE STRIDE HYPOTHESIS',fill='white')
   image=preview[frame_at(DURATIONS,time)];ground_y=45+time/cycle*stride*27/math.sqrt(2)
   x=round(120-job['groundPivot'][0]*38/1254);y=round(ground_y-job['groundPivot'][1]*38/1254);canvas.alpha_composite(image,(x,y));grid.append(canvas)
  grid[0].save(out/'grid-review.gif',save_all=True,append_images=grid[1:],duration=10,loop=0,disposal=2)
 else:(out/'grid-review-pending.json').write_text(json.dumps({'status':'PENDING_REAL_REACHABLE_STRIDE_AND_CONTACT_LANDMARKS','reason':'No invented travel speed or foot-slide approval'},indent=2))
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('command',choices=['preflight','compile']);parser.add_argument('job',type=pathlib.Path);parser.add_argument('--out',type=pathlib.Path);parser.add_argument('--cell',type=int,default=256);args=parser.parse_args()
 if args.command=='preflight':preflight(args.job);print('CUSTODY_AND_DECLARATIONS_PASS; visual review still required')
 else:require(args.out is not None,'--out required');compile_atlas(args.job,args.out,args.cell)
