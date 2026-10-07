#!/usr/bin/env python3
"""Custody/constant-length preflight and SVG assembly of ORIGINAL painted components.
No pose generation, source alteration, visible skeleton or approval assignment.
"""
import argparse,base64,hashlib,json,math,pathlib
from PIL import Image
PARTS=['core']+[f'{side}_{part}' for side in ['far','near'] for part in ['upper_arm','forearm_hand','thigh','shin','foot']]
def sha(b):return hashlib.sha256(b).hexdigest()
def point(p):return isinstance(p,list) and len(p)==2 and all(isinstance(v,(int,float)) and math.isfinite(v) for v in p)
def require(v,message):
 if not v:raise ValueError(message)
def load(path):return json.loads(path.read_text())
def normalized_sidecar(value):
 value=dict(value);landmarks=value.get('landmarks',{})
 if isinstance(landmarks,list):
  value['landmarkMetadata']={p['name']:dict(p) for p in landmarks}
  value['landmarks']={p['name']:p['xy'] for p in landmarks}
 return value

def preflight(path,partial=False):
 rig=load(path);base=path.parent
 require(rig.get('canvas')==[1254,1254] and rig.get('root')==[650,1140],'Fixed source canvas/root mismatch')
 require(rig.get('direction')=='D00' and rig.get('scale')==38/1254,'Locked direction/full-canvas scale mismatch')
 require(set(rig.get('parts',{}))==set(PARTS) if not partial else bool(rig.get('parts')) and set(rig['parts']).issubset(PARTS),'Exactly eleven original components required' if not partial else 'Partial diagnostic requires actual known components')
 require(set(rig.get('drawOrder',[]))==set(rig['parts']) and len(rig['drawOrder'])==len(rig['parts']),'Explicit stable draw order required')
 originals={}
 for slot,p in rig['parts'].items():
  sidecar=normalized_sidecar(load(base/p['sidecar']));original=base/sidecar['original'];raw=original.read_bytes()
  with Image.open(original) as image:
   require(image.mode=='RGBA','Original must be genuine RGBA: '+slot);rgba=image.tobytes();size=list(image.size)
  require(sha(raw)==sidecar['sha256'] and sha(rgba)==sidecar['rgbaSha256'] and size==sidecar['dimensions'],'Original custody mismatch: '+slot)
  require(sidecar['slot']==slot and sidecar.get('inspection',{}).get('status','').startswith('TECHNICALLY_USABLE'),'Natural-landmark inspection unresolved: '+slot)
  require(sidecar.get('inspection',{}).get('actor') and sidecar.get('inspection',{}).get('method'),'Named inspection actor/method required')
  for landmark in [p['anchor']]+([p['distal']] if p.get('distal') else [])+list(p.get('attachments',{}).values()):
   metadata=sidecar.get('landmarkMetadata',{}).get(landmark,{})
   if metadata:
    require('unresolved' not in metadata.get('status','').lower(),'Unresolved landmark must remain unassigned: '+landmark)
    require(isinstance(metadata.get('uncertainty_px'),(int,float)) and metadata['uncertainty_px']>=0,'Landmark uncertainty required: '+landmark)
    if 'AUTHORED' in metadata.get('status',''):
     require('HYPOTHESIS' in metadata['status'] and sidecar.get('static_transform_proposal',{}).get('status')=='PARENT_ACCEPTED_PRELIMINARY_FOR_PROTOTYPE','Authored hidden pivot needs disclosed hypothesis and parent prototype calibration')
  require(p.get('scale',0)>0 and math.isfinite(p['scale']),'One fixed positive uniform calibration required')
  require(point(sidecar['landmarks'].get(p['anchor'])),'Inspected natural/authored anchor absent: '+slot)
  if p.get('distal'):
   require(point(sidecar['landmarks'].get(p['distal'])) and len(p.get('joints',[]))==2,'Measured endpoints and joint ownership required: '+slot)
   a,b=sidecar['landmarks'][p['anchor']],sidecar['landmarks'][p['distal']]
   length=math.dist(a,b)*p['scale'];require(length>0 and abs(length-p['length'])<.01,'Rest calibration disagrees with locked bone length: '+slot)
  originals[slot]=(raw,size,sidecar)
 frames=rig.get('frames',[])
 if partial:
  require(len(frames)==1 and rig.get('status')=='PARTIAL_NOT_MOTION','Partial diagnostic must be one static explicitly labeled pose')
  return rig,originals
 count=rig.get('frameCount',24);require(isinstance(count,int) and count>=16 and count%8==0,'Frame count must support eight authored phase keys')
 require(len(frames)==count+1,'Rendered frames plus explicit seam closure required')
 require(rig.get('cycleDurationMs',0)>0,'Authored review timing required')
 require(rig.get('strideWorldTiles') is None or rig.get('strideStatus')=='REACHABLE_CONTACT_HYPOTHESIS','Stride cannot be forced before measured reach/contact calibration')
 for index,f in enumerate(frames):
  require(f.get('index')==index and f.get('root')==[650,1140],'Per-frame root fitting forbidden')
  require(f.get('phase')==index/count,'Declared phase must cover full loop')
  for slot,p in rig['parts'].items():
   joints=p['joints'];require(all(point(f['joints'].get(j)) for j in joints),'Missing real authored joint: '+slot)
   if p.get('distal'):require(abs(math.dist(*[f['joints'][j] for j in joints])-p['length'])<.01,'Bone stretch rejected at frame '+str(index)+': '+slot)
  core=rig['parts']['core'];core_sidecar=originals['core'][2];attachments=core.get('attachments',{})
  require(len(attachments)==4,'Core needs both shoulder and hip attachment landmarks')
  require('core' in f.get('angles',{}) and all(side+'_foot' in f.get('angles',{}) for side in ['near','far']),'Authored core/foot rotations required')
  m=matrix(core_sidecar['landmarks'][core['anchor']],f['joints'][core['joints'][0]],core['scale'],f['angles']['core']+core.get('restAngle',0))
  for joint,landmark in attachments.items():
   q=core_sidecar['landmarks'][landmark];transformed=[m[0]*q[0]+m[2]*q[1]+m[4],m[1]*q[0]+m[3]*q[1]+m[5]]
   require(math.dist(transformed,f['joints'][joint])<.01,'Joint drifts away from rigid core attachment: '+joint)
 for slot,angle in frames[0].get('angles',{}).items():require(abs(math.remainder(angle-frames[-1]['angles'][slot],2*math.pi))<.001,'Cyclic rigid-part rotation seam mismatch: '+slot)
 for joint,value in frames[0]['joints'].items():require(math.dist(value,frames[-1]['joints'][joint])<.01,'Cyclic joint seam mismatch: '+joint)
 require(frames[0].get('support')=='near' and frames[count//2].get('support')=='far','Distinct contact ownership required')
 require(frames[count//4].get('phaseName')=='near_support_far_passing' and frames[3*count//4].get('phaseName')=='far_support_near_passing','Actual passing/support keys required')
 return rig,originals

def matrix(raw_anchor,target,scale,angle):
 c=math.cos(angle)*scale;s=math.sin(angle)*scale
 return [c,s,-s,c,target[0]-c*raw_anchor[0]+s*raw_anchor[1],target[1]-s*raw_anchor[0]-c*raw_anchor[1]]
def assemble(path,out,partial=False):
 rig,originals=preflight(path,partial);out.mkdir(parents=True,exist_ok=True)
 for frame in (rig['frames'] if partial else rig['frames'][:-1]):
  elements=[]
  for slot in rig['drawOrder']:
   p=rig['parts'][slot];raw,size,sidecar=originals[slot];a=sidecar['landmarks'][p['anchor']];target=frame['joints'][p['joints'][0]]
   if p.get('distal'):
    b=sidecar['landmarks'][p['distal']];end=frame['joints'][p['joints'][1]]
    angle=math.atan2(end[1]-target[1],end[0]-target[0])-math.atan2(b[1]-a[1],b[0]-a[0])
   else:angle=frame['angles'][slot]+p.get('restAngle',0)
   transform=' '.join(format(v,'.12g') for v in matrix(a,target,p['scale'],angle))
   elements.append(f'<image width="{size[0]}" height="{size[1]}" transform="matrix({transform})" href="data:image/png;base64,{base64.b64encode(raw).decode()}"/>')
  svg='<svg xmlns="http://www.w3.org/2000/svg" width="1254" height="1254" viewBox="0 0 1254 1254">'+''.join(elements)+'</svg>'
  (out/f'{"P" if partial else "F"}{frame["index"]:02}.svg').write_text(svg)
 (out/'render-inputs.json').write_text(json.dumps({'rigSha256':sha(path.read_bytes()),'originalHashes':{slot:sha(raw) for slot,(raw,_,_) in originals.items()},'status':'PARTIAL_NOT_MOTION' if partial else 'REVIEW_ONLY_NOT_MOTION_APPROVED','canvas':rig['canvas'],'root':rig['root'],'scale':rig['scale'],'cycleDurationMs':None if partial else rig['cycleDurationMs'],'frameCount':1 if partial else rig.get('frameCount',24),'originalCustody':{slot:{'sha256':sidecar['sha256'],'rgbaSha256':sidecar['rgbaSha256'],'dimensions':sidecar['dimensions'],'landmarkMetadata':sidecar.get('landmarkMetadata',{}),'inspection':sidecar['inspection']} for slot,(_,_,sidecar) in originals.items()}},indent=2))
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('command',choices=['preflight','assemble','partial-assemble']);parser.add_argument('rig',type=pathlib.Path);parser.add_argument('--out',type=pathlib.Path);args=parser.parse_args()
 if args.command=='preflight':preflight(args.rig);print('CUSTODY_AND_GEOMETRY_ONLY_PASS; motion review remains required')
 else:require(args.out is not None,'--out required');assemble(args.rig,args.out,args.command=='partial-assemble')
