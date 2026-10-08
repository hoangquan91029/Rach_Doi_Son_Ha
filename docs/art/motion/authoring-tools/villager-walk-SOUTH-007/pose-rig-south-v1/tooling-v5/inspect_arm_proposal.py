"""One pinned uncertain cloth-endpoint proposal. Never creates a sealed sidecar."""
import hashlib,json,pathlib,shutil,tempfile
from PIL import Image,ImageDraw
import inspect_partial as p
BASE=p.BASE
PROPOSAL_SHA='56b9f4d1637b24b929cf316abb58328fb00b8f3c62e66903e1be22bcd86636f2'
def run(out):
 b=p.engine();out=pathlib.Path(out);b.require(not out.exists(),'no overwrite');qpath=BASE/'parts/arm-right-upper-01/landmark-fit-proposal-not-sidecar.json';b.require(p.sha(qpath)==PROPOSAL_SHA,'proposal custody');q=json.loads(qpath.read_text());rawpath=pathlib.Path(q['raw_path']);b.require(p.sha(rawpath)==q['raw_sha256'],'raw custody')
 raw=Image.open(rawpath);b.require(raw.mode=='RGBA' and raw.size==(1254,1254),'raw RGBA1254');b.require(hashlib.sha256(raw.tobytes()).hexdigest()==q['decoded_rgba_sha256'],'decoded custody')
 _,plan=b.locked_inputs();core,_=b.validate_sidecar(BASE/'parts/core-head-torso-pelvis-01/sidecar-v3.json','core_head_torso_pelvis');b.validate_approved_core(core);core_raw=Image.open(core['raw']['path'])
 cal={k:q['candidate_uniform_raw_to_bone_rest'][k] for k in ('scale','rotationRad','translation')};cal['tolerancePx']=.01
 # Full original canvas semantic quad; every original alpha is retained. Uniform fit remains unchanged.
 xy=[[0,0],[1254,0],[1254,1254],[0,1254]]
 s={'partId':'arm_right_upper','calibration':cal,'landmarks':{x['name']:{'xy':x['xy_raw_approx']} for x in q['landmark_candidates']},'mesh':{'vertices':[{'rawXY':v,'binding':{'frame':'bone','local':b.calibration_xy(cal,v)}} for v in xy],'triangles':[{'indices':[0,1,2],'region':'bone'},{'indices':[0,2,3],'region':'bone'}]}}
 bounds=b.validate_pose_geometry('arm_right_upper',s,plan);frame=p.rest_reference(plan,'arm_right_upper',b);b.validate_pose_geometry('arm_right_upper',s,{'frames':[{'frame':0,**frame}]});report=p.joint_report(s,plan,'arm_right_upper',b)
 stage=pathlib.Path(tempfile.mkdtemp(prefix='.proposal-only-',dir=out.parent))
 try:
  im=Image.new('RGBA',(1254,1254));b.draw_part(im,raw,s,frame);b.draw_part(im,core_raw,core,frame)
  qa=Image.new('RGBA',im.size,(90,90,90,255));qa.alpha_composite(im);d=ImageDraw.Draw(qa);d.text((20,20),'PROPOSAL_ONLY / TWO REAL PARTS / UNCERTAIN CLOTH ENDPOINTS / NOT ANATOMY',fill='white');d.text((20,40),'NO SEALED SIDECAR / NO FINISHED KEY / NO MOTION QUALIFICATION',fill='white')
  a,c=report['neutralBodyRestScreenEndpoints'];d.line([tuple(a),tuple(c)],fill='cyan',width=2)
  outputs=[]
  for name,img in [('partial-rest.png',im),('partial-rest-QA.png',qa),('partial-rest-whole38.png',im.resize((38,38),Image.Resampling.LANCZOS))]:
   img.save(stage/name);outputs.append({'path':name,'sha256':p.sha(stage/name),'rgbaSha256':hashlib.sha256(img.tobytes()).hexdigest()})
  r={'status':'PROPOSAL_ONLY_UNSEALED_CLOTH_ENDPOINT_PARTIAL_REST','candidate':False,'finishedKey':False,'motionQualified':False,'sealedSidecarCreated':False,'partCount':2,'missingOriginalParts':7,'sourceProposalSha256':PROPOSAL_SHA,'rawSha256':q['raw_sha256'],'rawRgbaSha256':q['decoded_rgba_sha256'],'endpointEvidence':q['landmark_candidates'],'jointAndCameraReport':report,'allFourPoseGeometryBounds':bounds,'sourceCoverage':'Full unchanged1254 canvas quad; all alpha retained; no bbox fit/cleanup/crop.','layerOrderProposal':['arm_right_upper','core_head_torso_pelvis'],'orderingApproved':False,'outputs':outputs,'toolSha256':p.sha(__file__)}
  b.require(p.sha(qpath)==PROPOSAL_SHA and p.sha(rawpath)==q['raw_sha256'],'custody changed');p.engine();(stage/'inspection.json').write_text(json.dumps(r,indent=2)+'\n');b.publish_no_replace(stage,out);return r
 finally:
  if stage.exists():shutil.rmtree(stage)
if __name__=='__main__':
 import sys
 print(json.dumps(run(sys.argv[1]),indent=2))
