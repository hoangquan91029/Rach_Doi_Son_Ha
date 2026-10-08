"""Core plus ONE rigid-bone part, partial rest proposal only. No motion export."""
import argparse,copy,hashlib,importlib.util,json,math,pathlib,shutil,sys,tempfile
sys.dont_write_bytecode=True
from PIL import Image,ImageDraw,ImageFont
BASE=pathlib.Path(__file__).resolve().parents[1]
ENGINE_SHA='b5ad84368a091cf1b2643e687fe7a98b7465906a52ede606a7eb89b791d29923'
REVIEW_SHA='f2d304415f809c4de3ae3e00ea901a6a0cbeecb69ac70051eaf90d144e6c2bca'
RIGID_IDS=('arm_right_upper','arm_right_lower_hand','arm_left_upper','arm_left_lower_hand','leg_right_upper','leg_left_upper')
def sha(path):return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()
def engine():
 p=BASE/'tooling-v4/bake_keys.py';review=BASE/'parent-tool-review-v4.json'
 if sha(p)!=ENGINE_SHA or sha(review)!=REVIEW_SHA:raise ValueError('sealed v4 engine/parent review custody mismatch')
 r=json.loads(review.read_text())
 for rel,h in r['pins'].items():
  if sha(BASE/rel)!=h:raise ValueError('sealed parent core dependency changed: '+rel)
 spec=importlib.util.spec_from_file_location('sealed_v4_partial_engine',p);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

def endpoint_similarity(proximal,distal,length):
 """After original inspection only. Returns exact directed uniform fit, no image writes."""
 if not all(isinstance(p,list) and len(p)==2 and all(type(x) in (int,float) and math.isfinite(x) for x in p) for p in (proximal,distal)):raise ValueError('finite inspected endpoint coordinates required')
 if type(length) not in (int,float) or not math.isfinite(length) or length<=0:raise ValueError('positive model length required')
 dx=distal[0]-proximal[0];dy=distal[1]-proximal[1];distance=math.hypot(dx,dy)
 if distance<=1e-6:raise ValueError('distinct original endpoints required')
 s=length/distance;r=math.pi/2-math.atan2(dy,dx);x,y=proximal
 return {'scale':s,'rotationRad':r,'translation':[-s*(math.cos(r)*x-math.sin(r)*y),-s*(math.sin(r)*x+math.cos(r)*y)]}

def rest_reference(plan,pid,b):
 # ONE stationary partial diagnostic: original F0 bone angles, undo only body shift/bob.
 # Persistent plan/world-foot tracks are never edited or used as new final key art.
 f=plan['frames'][0];kind,side,bone,_=b.part_kind(pid)
 b.require(kind=='bone' and pid in RIGID_IDS,'one known rigid limb only; no foot authoring')
 shift=f['lateralWeightShift'];bob=f['pelvisZ']-480
 points={side+'_'+name:[f['points3D'][side+'_'+name][0]-shift,f['points3D'][side+'_'+name][1],f['points3D'][side+'_'+name][2]-bob] for name in bone[:2]}
 return {'points3D':points,'lateralWeightShift':0,'pelvisZ':480,'referenceKey':0,'scope':'Stationary core+onepart rest diagnostic, not F0 key art or a loop.'}

def joint_report(s,plan,pid,b):
 _,side,bone,_=b.part_kind(pid);prox,dist,L=bone
 fit=endpoint_similarity(s['landmarks'][prox]['xy'],s['landmarks'][dist]['xy'],L)
 frame=rest_reference(plan,pid,b)
 def proj(q):return [654+q[0],1140+.5*q[1]-q[2]]
 a,c=[frame['points3D'][side+'_'+x] for x in (prox,dist)];screen=[proj(a),proj(c)]
 records=[]
 for f in plan['frames']:
  a3,c3=[f['points3D'][side+'_'+x] for x in (prox,dist)];a2,c2=proj(a3),proj(c3)
  records.append({'key':f['frame'],'proximalScreenXY':a2,'distalScreenXY':c2,'modelLength':math.dist(a3,c3),'screenLength':math.dist(a2,c2),'screenToModelRatio':math.dist(a2,c2)/L})
 return {'rawInspectedEndpointNames':[prox,dist],'rawEndpointSpan':math.dist(s['landmarks'][prox]['xy'],s['landmarks'][dist]['xy']),'directedUniformEndpointFitProposal':fit,'providedImmutableCalibration':s['calibration'],'providedEndpointRestResidualPx':[math.dist(b.calibration_xy(s['calibration'],s['landmarks'][prox]['xy']),[0,0]),math.dist(b.calibration_xy(s['calibration'],s['landmarks'][dist]['xy']),[0,L])],'unforeshortenedBonePlaneLength':L,'neutralBodyRestScreenEndpoints':screen,'neutralBodyRestScreenLength':math.dist(*screen),'neutralBodyScreenToBoneRatio':math.dist(*screen)/L,'cameraRole':'Fixed2:1 affine camera projection applied ONCE after uniform raw-to-unforeshortened bone-plane calibration. Screen length is not a200px source-calibration target.','allFourJointRecords':records}

def inspect(pid,limb_path,output,order,purpose):
 b=engine();out=pathlib.Path(output);b.require(not out.exists(),'refuse existing partial output')
 b.require(pid in RIGID_IDS,'one known rigid limb required');b.require(order in ([pid,b.PARTS[0]],[b.PARTS[0],pid]),'explicit two-part occlusion order required')
 b.require(purpose in ('ACTUAL_SOURCE_PROPOSAL','NON_ART_TEMPORARY_FIXTURE'),'explicit truthful input purpose required')
 contract,plan=b.locked_inputs();corepath=BASE/'parts/core-head-torso-pelvis-01/sidecar-v3.json';core,craw=b.validate_sidecar(corepath,b.PARTS[0]);b.validate_approved_core(core)
 limb,lraw=b.validate_sidecar(limb_path,pid)
 bounds={b.PARTS[0]:b.validate_pose_geometry(b.PARTS[0],core,plan),pid:b.validate_pose_geometry(pid,limb,plan)}
 report=joint_report(limb,plan,pid,b);frame=rest_reference(plan,pid,b)
 for name,s in [(b.PARTS[0],core),(pid,limb)]:b.validate_pose_geometry(name,s,{'frames':[{'frame':0,**frame}]})
 custody={name:{'rawPath':s['raw']['path'],'rawSha256':s['raw']['sha256'],'rgbaSha256':s['raw']['rgbaSha256'],'sidecarPath':str(p),'sidecarSha256':sha(p)} for name,s,p in [(b.PARTS[0],core,corepath),(pid,limb,limb_path)]}
 b.require(out.parent.exists(),'output parent must already exist');stage=pathlib.Path(tempfile.mkdtemp(prefix='.partial-two-part-',dir=out.parent))
 try:
  image=Image.new('RGBA',(1254,1254));parts={b.PARTS[0]:(core,craw),pid:(limb,lraw)}
  for name in order:s,raw=parts[name];b.draw_part(image,raw,s,frame)
  qa=Image.new('RGBA',(1254,1254),(100,100,100,255));qa.alpha_composite(image);draw=ImageDraw.Draw(qa)
  try:font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
  except OSError:font=ImageFont.load_default()
  status='PARTIAL_REST_INSPECTION_REQUIRES_SOURCE_REVIEW' if purpose=='ACTUAL_SOURCE_PROPOSAL' else 'NON_ART_PARTIAL_DIAGNOSTIC_NOT_QUALIFICATION'
  draw.text((20,15),status+' / core+ONE limb only',font=font,fill='white')
  draw.text((20,45),'Unforeshortened model '+str(report['unforeshortenedBonePlaneLength'])+' -> camera screen '+format(report['neutralBodyRestScreenLength'],'.2f')+'px / no double projection',font=font,fill='white')
  a,c=report['neutralBodyRestScreenEndpoints'];draw.line([tuple(a),tuple(c)],fill=(20,230,255,255),width=2)
  for point,label in zip((a,c),report['rawInspectedEndpointNames']):
   x,y=point;draw.ellipse((x-5,y-5,x+5,y+5),outline=(20,230,255,255),width=2);draw.text((x-170,y-15),label+' diagnostic',font=font,fill=(20,230,255,255))
  draw.line((639,1140,669,1140),fill=(20,255,100,255),width=2);draw.line((654,1125,654,1155),fill=(20,255,100,255),width=2)
  draw.text((20,1190),'Missing7 original parts / no full key, motion, contact or final illustration approval',font=font,fill='white')
  outputs=[]
  for name,im in [('partial-rest.png',image),('partial-rest-QA.png',qa),('partial-rest-whole38.png',image.resize((38,38),Image.Resampling.LANCZOS))]:
   path=stage/name;im.save(path);outputs.append({'path':name,'width':im.width,'height':im.height,'sha256':sha(path),'rgbaSha256':hashlib.sha256(im.tobytes()).hexdigest()})
  for r in custody.values():b.require(sha(r['rawPath'])==r['rawSha256'] and sha(r['sidecarPath'])==r['sidecarSha256'],'source custody changed during inspection')
  b.locked_inputs();engine()
  receipt={'schema':'south-two-part-rest-inspection/v1','status':status,'candidate':False,'fullCharacter':False,'finishedKey':False,'motionQualified':False,'finalArtApproved':False,'imageCalls':0,'runtimeChanges':False,'purpose':purpose,'partId':pid,'coreAndLimbOnly':True,'missingOriginalParts':7,'proposedLayerOrder':order,'orderingApproved':False,'bodyRestReference':frame['scope'],'jointAndCameraReport':report,'allFourPoseGeometryBounds':bounds,'sourceAlphaOutsideEachMesh':0,'sourceCustody':custody,'outputs':outputs,'toolSha256':sha(__file__),'sealedV4EngineSha256':ENGINE_SHA,'parentCoreReviewSha256':REVIEW_SHA,'remainingFootGate':'Actual trailing toe-grounded/heel-rise rigid foot plane must be authored from lower_sandal originals and reviewed BEFORE four finishedkey acceptance; preservedflat12px hypothesis is not contact qualification.'}
  (stage/'inspection.json').write_text(json.dumps(receipt,indent=2)+'\n');b.publish_no_replace(stage,out);return receipt
 finally:
  if stage.exists():shutil.rmtree(stage)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('partId');p.add_argument('sidecar');p.add_argument('output');p.add_argument('--order',required=True,help='comma-separated exact partId and core_head_torso_pelvis');p.add_argument('--purpose',required=True,choices=['ACTUAL_SOURCE_PROPOSAL','NON_ART_TEMPORARY_FIXTURE']);a=p.parse_args()
 try:r=inspect(a.partId,a.sidecar,a.output,a.order.split(','),a.purpose);print(json.dumps({'status':r['status'],'candidate':False,'finishedKey':False,'motionQualified':False}))
 except (ValueError,KeyError,OSError,TypeError) as e:print(json.dumps({'status':'REFUSED_NO_PARTIAL_OUTPUT','reason':str(e),'candidate':False}));raise SystemExit(2)
