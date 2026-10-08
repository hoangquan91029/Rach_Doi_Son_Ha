"""Internal three-part authoring projection; proposed lower is NEVER a sealed sidecar."""
import argparse,hashlib,json,math,pathlib,shutil,sys,tempfile
sys.dont_write_bytecode=True
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'tooling-v5'))
import inspect_partial as p
from PIL import Image,ImageDraw
LOW='arm_right_lower_hand';UP='arm_right_upper';CORE='core_head_torso_pelvis'

def proposal(q,b):
 b.require(set(q)=={'schema','status','purpose','raw','endpoints','calibration','layerOrderProposal','ownershipClarification'},'unknown proposal fields')
 b.require(q['schema']=='south-lower-diagnostic-proposal/v1' and q['status']=='UNSEALED_DIAGNOSTIC','unsealed diagnostic required')
 b.require(q['purpose'] in ('ACTUAL_ORIGINAL','NON_ART_TEST_FIXTURE'),'truthful source purpose required')
 b.require(q['layerOrderProposal']==[LOW,UP,CORE],'explicit lower behind upper/core proposal required')
 b.require(set(q['endpoints'])=={'elbow','wrist'},'measured elbow/wrist required')
 for lm in q['endpoints'].values():
  b.require(set(lm)=={'xy','method','uncertaintyPx','evidence'},'endpoint schema')
  b.require(lm['method']=='observed_original' and isinstance(lm['evidence'],str) and bool(lm['evidence'].strip()),'observed original endpoint evidence required')
  b.require(type(lm['uncertaintyPx']) in (int,float) and math.isfinite(lm['uncertaintyPx']) and 0<=lm['uncertaintyPx']<=120,'uncertainty')
  b.require(b.finite(lm['xy'],2) and all(0<=v<=1254 for v in lm['xy']),'endpoint canvas coordinates')
 fit=p.endpoint_similarity(q['endpoints']['elbow']['xy'],q['endpoints']['wrist']['xy'],180)
 cal=q['calibration'];b.require(set(cal)=={'scale','rotationRad','translation'},'only uniform static calibration allowed')
 b.require(type(cal['scale']) in (int,float) and math.isfinite(cal['scale']) and cal['scale']>0,'positive uniform scale')
 b.require(type(cal['rotationRad']) in (int,float) and math.isfinite(cal['rotationRad']) and b.finite(cal['translation'],2),'finite transform')
 for name,target in [('elbow',[0,0]),('wrist',[0,180])]:b.require(b.same(b.calibration_xy(cal,q['endpoints'][name]['xy']),target,1e-6),'measured endpoint residual exceeds 1e-6')
 vertices=[{'rawXY':v,'binding':{'frame':'bone','local':b.calibration_xy(cal,v)}} for v in [[0,0],[1254,0],[1254,1254],[0,1254]]]
 return {'partId':LOW,'calibration':{**cal,'tolerancePx':1e-6},'landmarks':q['endpoints'],'mesh':{'vertices':vertices,'triangles':[{'indices':[0,1,2],'region':'bone'},{'indices':[0,2,3],'region':'bone'}]}},fit

def verify_unique_sources(hashes,b):
 b.require(len(set(hashes))==len(hashes),'duplicate original source slot')

def verify_bytes(path,expected,b):
 b.require(p.sha(path)==expected,'original byte custody')

def run(qpath,out):
 b=p.engine();qpath=pathlib.Path(qpath);out=pathlib.Path(out);b.require(not out.exists() and out.parent.is_dir(),'no overwrite; existing parent required');qh=p.sha(qpath);q=json.loads(qpath.read_text());lower,fit=proposal(q,b);oc=q['ownershipClarification'];b.require(set(oc)=={'path','sha256'},'ownership clarification custody');ocp=pathlib.Path(oc['path']);b.require(ocp.is_absolute(),'absolute clarification path');b.require(ocp==p.BASE/'component-ownership-clarification-v1.json' and oc['sha256']=='9a874ebd63262f54a99df53c84fd4404c354ba0f9290e32ac4888d9dde363076','locked additive ownership clarification required');verify_bytes(ocp,oc['sha256'],b)
 r=q['raw'];b.require(set(r)=={'path','sha256','rgbaSha256','width','height'},'raw custody fields');rp=pathlib.Path(r['path']);b.require(rp.is_absolute(),'absolute original path required');verify_bytes(rp,r['sha256'],b)
 with Image.open(rp) as src:
  b.require(src.mode=='RGBA' and src.size==(1254,1254) and r['width']==1254 and r['height']==1254,'RGBA1254 original required');lraw=src.copy()
 b.require(hashlib.sha256(lraw.tobytes()).hexdigest()==r['rgbaSha256'],'decoded original custody');_,plan=b.locked_inputs();b.require([f['frame'] for f in plan['frames']]==[0,2,4,6],'four locked frames')
 cp=p.BASE/'parts/core-head-torso-pelvis-01/sidecar-v3.json';up=p.BASE/'parts/arm-right-upper-01/sidecar-v1.json';core,craw=b.validate_sidecar(cp,CORE);b.validate_approved_core(core);upper,uraw=b.validate_sidecar(up,UP)
 verify_unique_sources([r['sha256'],core['raw']['sha256'],upper['raw']['sha256']],b);custody={str(x):p.sha(x) for x in [qpath,rp,cp,up,ocp,pathlib.Path(core['raw']['path']),pathlib.Path(upper['raw']['path'])]}
 parts={LOW:(lower,lraw),UP:(upper,uraw),CORE:(core,craw)};rest=p.rest_reference(plan,LOW,b);rest['points3D'].update(p.rest_reference(plan,UP,b)['points3D']);frames=[('REST',{'frame':0,**rest})]+[('F'+str(f['frame']),f) for f in plan['frames']]
 bounds={pid:b.validate_pose_geometry(pid,s,{'frames':[f for _,f in frames]}) for pid,(s,_) in parts.items()};stage=pathlib.Path(tempfile.mkdtemp(prefix='.unsealed-three-',dir=out.parent));outputs=[]
 try:
  for label,f in frames:
   im=Image.new('RGBA',(1254,1254))
   for pid in q['layerOrderProposal']:s,raw=parts[pid];b.draw_part(im,raw,s,f)
   for size in (1254,627,38):
    scaled=im if size==1254 else im.resize((size,size),Image.Resampling.LANCZOS);name=label+'-UNSEALED_DIAGNOSTIC-THREEPARTS-MISSING6-'+str(size)+'.png';scaled.save(stage/name);outputs.append({'path':name,'sha256':p.sha(stage/name),'width':size,'height':size})
   qa=Image.new('RGBA',(1254,1254),(90,90,90,255));qa.alpha_composite(im);ImageDraw.Draw(qa).text((10,10),label+' UNSEALED_DIAGNOSTIC / THREE PARTS / MISSING SIX / NOT FINISHED KEY',fill='white');qa.save(stage/(label+'-UNSEALED-THREEPARTS-MISSING6-QA.png'));outputs.append({'path':label+'-UNSEALED-THREEPARTS-MISSING6-QA.png','sha256':p.sha(stage/(label+'-UNSEALED-THREEPARTS-MISSING6-QA.png'))})
  receipt={'status':'UNSEALED_DIAGNOSTIC','purpose':q['purpose'],'candidate':False,'finishedKey':False,'motionQualified':False,'sealedSidecarCreated':False,'partCount':3,'missingOriginalParts':6,'proposalSha256':qh,'ownershipClarification':oc,'lowerComponent':'bare forearm and hand; upper sleeve owns cuff; additive clarification preserves sealed v3 geometry','sourceCustody':custody,'immutableMeasuredUniformFit':fit,'jointAndCameraReport':p.joint_report(lower,plan,LOW,b),'geometryBounds':bounds,'sourceCoverage':'Full original canvas two-triangle quad retains all alpha; no crop, cleanup, mirror, anisotropic fit or per-pose source fit.','layerOrderProposal':q['layerOrderProposal'],'fullNinePartOrderingApproved':False,'cameraRoot':[654,1140],'wholeCanvasLogicalSize':38,'outputs':outputs,'toolSha256':p.sha(__file__)}
  for path,h in custody.items():b.require(p.sha(path)==h,'source changed during diagnostic')
  b.locked_inputs();p.engine();(stage/'inspection.json').write_text(json.dumps(receipt,indent=2)+'\n');b.publish_no_replace(stage,out);return receipt
 finally:
  if stage.exists():shutil.rmtree(stage)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('proposal');parser.add_argument('output');a=parser.parse_args()
 try:print(json.dumps({'status':run(a.proposal,a.output)['status']}))
 except (ValueError,KeyError,OSError,TypeError) as e:print(json.dumps({'status':'REFUSED_NO_OUTPUT','reason':str(e)}));raise SystemExit(2)
