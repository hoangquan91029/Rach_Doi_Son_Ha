"""ONE authorized actual-core-driven model adjustment; no source/art calls."""
import copy,hashlib,json,math,pathlib,sys
sys.dont_write_bytecode=True
from PIL import Image
BASE=pathlib.Path(__file__).resolve().parents[1]
PROPOSAL_SHA='66b568178639b52214da1e3514b161e85decdfe6e7429c631280c01df0840cdc'
OLD_CONTRACT_SHA='52202bc716ce0d82bc3cdef3c2e18c4cdba094f7a58dc5b6c75e5c7ccf883421'
OLD_PLAN_SHA='c6499aebde1287abe2066de1dfcc3f6fc74bae9b0952452a34024e3da27c87bf'
SCALE=.672919808;ROTATION=-.000318866;TRANSLATION=[206.170592,16.511619]
DEFS={'actor_right_shoulder_cap':([430,484],'authored_cloth_attachment_convention',14),'actor_left_shoulder_cap':([820,484],'authored_cloth_attachment_convention',14),'actor_right_hip_under_hem':([510,870],'authored_hidden_hypothesis',45),'actor_left_hip_under_hem':([785,870],'authored_hidden_hypothesis',45)}
def digest(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(pathlib.Path(p).read_text())
def encoded(d):return (json.dumps(d,indent=2)+'\n').encode()
def project(p):return [654+p[0],1140+.5*p[1]-p[2]]
def mapped(xy):
 x,y=xy;return [SCALE*(math.cos(ROTATION)*x-math.sin(ROTATION)*y)+TRANSLATION[0],SCALE*(math.sin(ROTATION)*x+math.cos(ROTATION)*y)+TRANSLATION[1]]
def ik(a,c,L1,L2,pole):
 delta=[c[i]-a[i] for i in range(3)];r=math.sqrt(sum(v*v for v in delta))
 if not abs(L1-L2)<r<L1+L2:raise ValueError('UNREACHABLE; no bone stretch allowed: '+str(r))
 u=[v/r for v in delta];along=(L1*L1-L2*L2+r*r)/(2*r);h=math.sqrt(L1*L1-along*along)
 desired=[0,pole,0];dot=sum(desired[i]*u[i] for i in range(3));v=[desired[i]-dot*u[i] for i in range(3)];n=math.sqrt(sum(x*x for x in v))
 if n<1e-9:raise ValueError('singular IK pole')
 return [a[i]+u[i]*along+v[i]/n*h for i in range(3)]
def build():
 pp=BASE/'core-rest-proposal-v1/proposal.json';assert digest(pp)==PROPOSAL_SHA
 proposal=load(pp);assert proposal['calibration']['scale']==SCALE and proposal['calibration']['rotation_rad']==ROTATION and proposal['calibration']['translation_xy']==TRANSLATION
 oldc=BASE/'part-contract-v2.json';oldp=BASE.parent/'pose-guides/walk-south-keys-v2/coordinate-plan.json';assert digest(oldc)==OLD_CONTRACT_SHA and digest(oldp)==OLD_PLAN_SHA
 raw=proposal['sources']['core_raw'];assert digest(raw['path'])==raw['sha256']
 with Image.open(raw['path']) as im:
  assert im.mode=='RGBA' and im.size==(1254,1254);assert hashlib.sha256(im.tobytes()).hexdigest()==raw['decoded_rgba_sha256']
  bounds=im.getchannel('A').getbbox();assert bounds==(73,42,1194,1222)
  anchors={name:{'sourceRawXY':xy,'restScreenXY':mapped(xy),'modelRest3D':[mapped(xy)[0]-654,-100,1090-mapped(xy)[1]],'method':method,'uncertaintySourcePx':unc,'sourceAlpha':im.getpixel(tuple(xy))[3]} for name,(xy,method,unc) in DEFS.items()}
  assert all(a['sourceAlpha']==253 for a in anchors.values())
 plan=copy.deepcopy(load(oldp));oldplan=load(oldp);reach=[]
 for f,old in zip(plan['frames'],oldplan['frames']):
  shift=f['lateralWeightShift'];bob=f['pelvisZ']-480;p=f['points3D']
  for side in ('LEFT','RIGHT'):
   hip=anchors['actor_'+side.lower()+'_hip_under_hem']['modelRest3D'];shoulder=anchors['actor_'+side.lower()+'_shoulder_cap']['modelRest3D']
   p[side+'_hip']=[hip[0]+shift,hip[1],hip[2]+bob];p[side+'_shoulder']=[shoulder[0]+shift,shoulder[1],shoulder[2]+bob]
   p[side+'_knee']=ik(p[side+'_hip'],p[side+'_ankle'],260,240,1)
   arm_sign=-1 if side==f['support'] else 1;p[side+'_elbow']=ik(p[side+'_shoulder'],p[side+'_wrist'],200,180,-arm_sign)
   for joint in ('ankle','heel','toe','wrist'):assert p[side+'_'+joint]==old['points3D'][side+'_'+joint]
   f['lengths'][side]={name:math.dist(p[side+'_'+a],p[side+'_'+b]) for name,a,b in [('thigh','hip','knee'),('shin','knee','ankle'),('upperArm','shoulder','elbow'),('forearm','elbow','wrist')]}
   assert all(abs(f['lengths'][side][k]-L)<1e-8 for k,L in [('thigh',260),('shin',240),('upperArm',200),('forearm',180)])
   reach.append({'key':f['frame'],'side':side,'hipAnkleDistance':math.dist(p[side+'_hip'],p[side+'_ankle']),'shoulderWristDistance':math.dist(p[side+'_shoulder'],p[side+'_wrist'])})
   for joint,label in [('hip','actor_'+side.lower()+'_hip_under_hem'),('shoulder','actor_'+side.lower()+'_shoulder_cap')]:
    rest=anchors[label]['restScreenXY'];assert math.dist(project(p[side+'_'+joint]),[rest[0]+shift,rest[1]-bob])<1e-9
  f['points2D']={k:project(v) for k,v in p.items()};f['bodyCenterSourceX']=(anchors['actor_left_hip_under_hem']['restScreenXY'][0]+anchors['actor_right_hip_under_hem']['restScreenXY'][0])*.5+shift
  assert f['soles']==old['soles'] and all(f[k]==old[k] for k in ('timeMs','support','swing','passing','pelvisZ','lateralWeightShift','bodyTravelDepth'))
 assert plan['contactTable']==oldplan['contactTable'] and plan['strideHypothesis']==oldplan['strideHypothesis']
 plan['hiddenJoints']['hipSourceApprox']=[*anchors['actor_right_hip_under_hem']['restScreenXY'],*anchors['actor_left_hip_under_hem']['restScreenXY']]
 plan['hiddenJoints']['uncertaintySourcePx']=45;plan['hiddenJoints']['hipSourceApproxMeaning']='Exact projected authored hidden-pivot conventions from accepted actual core; uncertainty45 RAWsource px, not measured anatomy.';plan['hiddenJoints']['coreAttachments']=anchors
 plan['eightStaticIdentityGate']='PASS_STATIC_IDENTITY_LOCK_FOR_SOUTH_AUTHORING_ONLY'
 plan['sourceDrivenAdjustment']={'status':'ONE_AUTHORIZED_ATTACHMENT_ADJUSTMENT_NOT_ART_APPROVAL','proposalPath':str(pp),'proposalSha256':PROPOSAL_SHA,'previousPlanSha256':OLD_PLAN_SHA,'staticCoreCalibration':{'scale':SCALE,'rotationRad':ROTATION,'translation':TRANSLATION},'frameRule':'Each core anchor translates by original lateral shift and bob; baseline depth−100 is a model hypothesis. Constantbones solved by full3DIK; original wrist/ankle/heel/toe/contact/world tracks unchanged.','numericalMappingTolerancePx':2,'visibleFeatureFitResidualPx':[2.96,6.40],'attachmentUncertaintyMeaning':'14px cloth seam /45px hidden hip uncertainty in RAWsource coordinates; not a2px measurement claim.'}
 plan['reach']={'checkedAll4Keys':True,'legMaxReach':500,'armMaxReach':380,'maxActualHipAnkleDistance':max(r['hipAnkleDistance'] for r in reach),'maxActualShoulderWristDistance':max(r['shoulderWristDistance'] for r in reach),'records':reach,'noStretch':True}
 contract=copy.deepcopy(load(oldc));contract['schema']='south-illustrated-bitmap-rig-part-contract/v3';contract['status']='ONE_PARENT_AUTHORIZED_SOURCE_DRIVEN_ATTACHMENT_ADJUSTMENT_REQUIRES_WHOLE_KEY_REVIEW'
 contract['core_rest_adjustment']={'proposalPath':str(pp),'proposalSha256':PROPOSAL_SHA,'previousContractSha256':OLD_CONTRACT_SHA,'coreRawSha256':raw['sha256'],'coreRgbaSha256':raw['decoded_rgba_sha256'],'calibration':{'scale':SCALE,'rotationRad':ROTATION,'translation':TRANSLATION},'attachmentTargets':anchors,'semanticCoverageQuadRaw':[[70,40],[1197,40],[1197,1224],[70,1224]],'sourceNonzeroAlphaBounds':list(bounds),'coverageRule':'ONE immutable padded alpha-coverage domain, with no nonzeroalpha outside; original1254RGBA remains unchanged. This domain is not a scale/bbox fit.','numericalMappingTolerancePx':2,'visibleFeatureFitResidualPx':[2.96,6.4],'cameraDepthHypothesis':-100,'wholeKeyArtApproval':False,'remainingOriginalParts':8}
 contract['parts'][0]['landmarks']='Actual shoulder cloth attachment conventions ±14RAWpx; hips authored hidden hypotheses ±45RAWpx; exact rest mapping from one approved immutable static calibration. No measured shoulder/hip anatomical centers claimed.'
 contract['component_policy']['landmarks']='Observed natural landmarks recorded after original inspection. Shoulder-only authored_cloth_attachment_convention permitted; hiddenhip pivots REQUIRE authored_hidden_hypothesis. All uncertainty is distinct from numerical mapping tolerance.'
 contract['model_pose_plan']={'path':str(BASE.parent/'pose-guides/walk-south-keys-v3/coordinate-plan.json'),'sha256':hashlib.sha256(encoded(plan)).hexdigest(),'keys':[0,2,4,6]}
 evidence={x['id']:x['evidence'] for x in proposal['attachment_proposals']};evidence.update({x['id'].replace('_under_tunic','_under_hem'):x['evidence'] for x in proposal['hip_pivot_hypotheses']})
 cal={'scale':SCALE,'rotationRad':ROTATION,'translation':TRANSLATION,'tolerancePx':2};corners=contract['core_rest_adjustment']['semanticCoverageQuadRaw']
 sidecar={'schema':'south-bitmap-rig-sidecar/v3','partId':'core_head_torso_pelvis','status':'SEALED_ORIGINAL_CALIBRATION','raw':{'path':raw['path'],'sha256':raw['sha256'],'rgbaSha256':raw['decoded_rgba_sha256'],'width':1254,'height':1254},'calibration':cal,'landmarks':{k:{'xy':v['sourceRawXY'],'method':v['method'],'uncertaintyPx':v['uncertaintySourcePx'],'evidence':evidence[k]} for k,v in anchors.items()},'mesh':{'vertices':[{'rawXY':xy,'binding':{'frame':'core','local':mapped(xy)}} for xy in corners],'triangles':[{'indices':[0,1,2],'region':'core'},{'indices':[0,2,3],'region':'core'}],'sharedAnkleSeam':[]}}
 output={BASE/'part-contract-v3.json':contract,BASE.parent/'pose-guides/walk-south-keys-v3/coordinate-plan.json':plan,BASE/'parts/core-head-torso-pelvis-01/sidecar-v3.json':sidecar}
 assert all(not path.exists() for path in output),'refuse overwrite adjustment outputs'
 for path,data in output.items():path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(encoded(data))
 print(json.dumps({'status':'NUMERICAL_SOURCE_DRIVEN_ADJUSTMENT_REQUIRES_PARENT_REVIEW','candidate':False,'coreTargets':anchors,'reach':plan['reach'],'outputs':{str(p):digest(p) for p in output}},indent=2))
if __name__=='__main__':build()
