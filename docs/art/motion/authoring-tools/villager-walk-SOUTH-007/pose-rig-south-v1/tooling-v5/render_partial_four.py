"""Four actual two-part diagnostics. No sidecar seal, finished keys or loop."""
import hashlib,json,pathlib,shutil,tempfile
from PIL import Image,ImageDraw,ImageFont
import inspect_partial as p
import inspect_arm_proposal as a

def run(out):
 b=p.engine();out=pathlib.Path(out);b.require(not out.exists(),'no overwrite')
 qp=p.BASE/'parts/arm-right-upper-01/landmark-fit-proposal-not-sidecar.json';b.require(p.sha(qp)==a.PROPOSAL_SHA,'proposal custody');q=json.loads(qp.read_text());rp=pathlib.Path(q['raw_path']);b.require(p.sha(rp)==q['raw_sha256'],'raw custody')
 raw=Image.open(rp);b.require(raw.mode=='RGBA' and raw.size==(1254,1254),'RGBA1254');b.require(hashlib.sha256(raw.tobytes()).hexdigest()==q['decoded_rgba_sha256'],'RGBA custody')
 cp=p.BASE/'parts/core-head-torso-pelvis-01/sidecar-v3.json';core,craw=b.validate_sidecar(cp,'core_head_torso_pelvis');b.validate_approved_core(core);_,plan=b.locked_inputs();cal={k:q['candidate_uniform_raw_to_bone_rest'][k] for k in ('scale','rotationRad','translation')};cal['tolerancePx']=.01
 verts=[{'rawXY':v,'binding':{'frame':'bone','local':b.calibration_xy(cal,v)}} for v in [[0,0],[1254,0],[1254,1254],[0,1254]]]
 arm={'partId':'arm_right_upper','calibration':cal,'mesh':{'vertices':verts,'triangles':[{'indices':[0,1,2],'region':'bone'},{'indices':[0,2,3],'region':'bone'}]}}
 bounds={'arm_right_upper':b.validate_pose_geometry('arm_right_upper',arm,plan),'core_head_torso_pelvis':b.validate_pose_geometry('core_head_torso_pelvis',core,plan)}
 stage=pathlib.Path(tempfile.mkdtemp(prefix='.partial-four-',dir=out.parent));outputs=[]
 def save(name,im):
  im.save(stage/name);outputs.append({'path':name,'width':im.width,'height':im.height,'sha256':p.sha(stage/name),'rgbaSha256':hashlib.sha256(im.tobytes()).hexdigest()})
 try:
  ims=[]
  for f in plan['frames']:
   im=Image.new('RGBA',(1254,1254));b.draw_part(im,raw,arm,f);b.draw_part(im,craw,core,f);ims.append((f['frame'],im));save('F'+str(f['frame'])+'-PARTIAL.png',im)
  for size in (1254,627,38):
   header=60 if size>38 else 38;sheet=Image.new('RGBA',(size*4,size+header),(90,90,90,255));d=ImageDraw.Draw(sheet)
   for i,(key,im) in enumerate(ims):
    d.text((i*size+2,2),'F'+str(key)+(' PARTIAL' if size>38 else ''),fill='white');d.text((i*size+2,17),'NOT KEY ART' if size>38 else 'PART',fill='white');sheet.alpha_composite(im.resize((size,size),Image.Resampling.LANCZOS),(i*size,header))
   save('PARTIAL_POSE_DIAGNOSTIC-'+str(size)+'-sheet.png',sheet)
  evidence={'status':'FIXED_FIT_ACCEPTED_FOR_AUTHORING_PARTIAL_DIAGNOSTIC_ONLY','sourceProposalSha256':a.PROPOSAL_SHA,'calibration':cal,'landmarks':[{'name':'shoulder','xy':[762,188],'method':'authored_cloth_attachment_convention','uncertaintyRawPx':30,'anatomicalJointMeasured':False},{'name':'elbow','xy':[600,966],'method':'observed_cuff_mouth_center','uncertaintyRawPx':35,'anatomicalJointMeasured':False}],'parentEvidence':'Parent accepted fixed candidate fit after native and38 partial rest review; four-pose diagnostics pending separate review.','sidecarSealAuthorized':False}
  (stage/'candidate-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
  r={'status':'PARTIAL_POSE_DIAGNOSTIC_REQUIRES_PARENT_REVIEW','candidate':False,'finishedKey':False,'motionQualified':False,'sealedSidecarCreated':False,'partCount':2,'missingOriginalParts':7,'keys':[f['frame'] for f in plan['frames']],'sourceProposalSha256':a.PROPOSAL_SHA,'rawSha256':q['raw_sha256'],'rawRgbaSha256':q['decoded_rgba_sha256'],'coreRawSha256':core['raw']['sha256'],'coreSidecarSha256':p.sha(cp),'posePlanSha256':b.PLAN_SHA,'calibration':cal,'allFourPoseGeometryBounds':bounds,'coverage':'Full original arm canvas semantic quad; unchanged sourcebytes/all alpha retained; fixed calibration; no fit/crop/cleanup per pose.','layerOrderProposal':['arm_right_upper','core_head_torso_pelvis'],'fullNinePartOrderingApproved':False,'outputs':outputs,'candidateEvidenceSha256':p.sha(stage/'candidate-evidence.json'),'toolSha256':p.sha(__file__),'remainingGate':'Parent separate four-pose diagnostic review before actual sidecar seal; these are not finished illustrated keys.'}
  b.require(p.sha(qp)==a.PROPOSAL_SHA and p.sha(rp)==q['raw_sha256'],'custody changed');p.engine();b.locked_inputs();(stage/'inspection.json').write_text(json.dumps(r,indent=2)+'\n');b.publish_no_replace(stage,out);return r
 finally:
  if stage.exists():shutil.rmtree(stage)
if __name__=='__main__':
 import sys
 print(json.dumps(run(sys.argv[1]),indent=2))
