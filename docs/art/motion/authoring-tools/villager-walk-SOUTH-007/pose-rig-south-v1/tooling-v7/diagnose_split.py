"""Four-slot unsealed authoring diagnostic. No eleven-part intake or source edits."""
import argparse,hashlib,json,math,pathlib,shutil,sys,tempfile
sys.dont_write_bytecode=True
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'tooling-v5'))
import inspect_partial as p
from PIL import Image,ImageDraw
CORE='core_head_torso_pelvis';UP='arm_right_upper';ARM='arm_right_forearm';HAND='hand_right_palm';PARTS=[CORE,UP,ARM,HAND];LABELS=['REST','F0','F2','F4','F6']
HELD_COMBINED={'1984793eb1fc2c57c1dafac2f454e0f57b6d48d03ead610958a333cf342ebf54','f95457f586608347dd0648abbf769f0c77092f62da425d65de88d1bd1ba36f0c','71e3697c43ea87a7428a5f93716e14621e52be0dbf00e5a66352ac32d8b1e2e8'}
TOPOLOGY_SHA='63859443aad0ec34c44672315b52e45823c03d294bffe74741733f0e43322083'
UPPER_PINS={'sidecar-v1.json':'7e60eb992fb5dfd24b6daa1332c09399cd20197741d5fdd96bc3c52e71bbac7a','parent-calibration-review-v1.json':'93fd995c1cd84746d710735fd92c4e76bff81d9e55b8b820c26e69e4352e5663','calibration-seal-receipt-v1.json':'a9547feb900a8874b85d33c5498cea8d0d03a1d354c222d6fb9b71696b00a6c5'}

def bind(ref,b):
 b.require(set(ref)=={'path','sha256'},'custody reference exact fields');path=pathlib.Path(ref['path']);b.require(path.is_absolute(),'absolute custody path required');b.require(p.sha(path)==ref['sha256'],'custody mismatch');return path

def validate_orders(q,b):
 b.require(set(q)=={'schema','layerOrderByPose','evidenceByPose'} and q['schema']=='south-four-part-orders-proposal/v1','explicit order proposal schema')
 b.require(set(q['layerOrderByPose'])==set(LABELS) and set(q['evidenceByPose'])==set(LABELS),'all five orders/evidence required')
 for label in LABELS:
  order=q['layerOrderByPose'][label];b.require(isinstance(order,list) and len(order)==4 and set(order)==set(PARTS),'exact four unique slots required')
  b.require(isinstance(q['evidenceByPose'][label],str) and bool(q['evidenceByPose'][label].strip()),'order reasoning required; depth ties explicit hypothesis')
 return q['layerOrderByPose']

def proposal(q,pid,b):
 names,length,schema=('elbow','wrist'),180,'south-right-forearm-proposal/v1'
 if pid==HAND:names,length,schema=('wrist','fingertip'),65,'south-right-hand-proposal/v1'
 b.require(pid in (ARM,HAND) and set(q)=={'schema','partId','status','purpose','raw','endpoints','calibration','sourceEvidence'},'new proposal exact fields/slot')
 b.require(q['schema']==schema and q['partId']==pid and q['status']=='UNSEALED_DIAGNOSTIC','new independent unsealed slot required')
 b.require(q['purpose'] in ('ACTUAL_ORIGINAL','NON_ART_TEST_FIXTURE'),'source purpose required');b.require(set(q['endpoints'])==set(names),'natural attachment endpoint names required')
 for name,lm in q['endpoints'].items():
  b.require(set(lm)=={'xy','method','uncertaintyPx','evidence','anatomicalJointMeasured','observableAnatomicalEvidence'},'endpoint exact fields')
  methods=('observed_original','authored_hidden_hypothesis') if name==names[0] else ('observed_original',)
  b.require(lm['method'] in methods and isinstance(lm['evidence'],str) and bool(lm['evidence'].strip()),'truthful natural convention evidence required')
  b.require(type(lm['anatomicalJointMeasured']) is bool,'explicit anatomical flag');ae=lm['observableAnatomicalEvidence']
  b.require((lm['anatomicalJointMeasured'] and lm['method']=='observed_original' and isinstance(ae,str) and bool(ae.strip())) or (not lm['anatomicalJointMeasured'] and ae is None),'anatomical measurement requires explicit observable evidence')
  b.require(type(lm['uncertaintyPx']) in (int,float) and math.isfinite(lm['uncertaintyPx']) and 0<=lm['uncertaintyPx']<=120,'finite uncertainty')
  b.require(b.finite(lm['xy'],2) and all(0<=x<=1254 for x in lm['xy']),'finite canvas coordinates')
 cal=q['calibration'];b.require(set(cal)=={'scale','rotationRad','translation'},'one static uniform calibration only');b.require(type(cal['scale']) in (int,float) and math.isfinite(cal['scale']) and cal['scale']>0,'positive uniform scale');b.require(type(cal['rotationRad']) in (int,float) and math.isfinite(cal['rotationRad']) and b.finite(cal['translation'],2),'finite transform')
 for name,target in zip(names,([0,0],[0,length])):b.require(b.same(b.calibration_xy(cal,q['endpoints'][name]['xy']),target,1e-6),'numeric attachment fit mismatch; not measurement precision')
 vertices=[{'rawXY':v,'binding':{'frame':'bone' if pid==ARM else 'south_wrist_plane','local':b.calibration_xy(cal,v)}} for v in [[0,0],[1254,0],[1254,1254],[0,1254]]]
 return {'partId':pid,'calibration':cal,'landmarks':q['endpoints'],'mesh':{'vertices':vertices,'triangles':[{'indices':[0,1,2],'region':'bone' if pid==ARM else 'hand'},{'indices':[0,2,3],'region':'bone' if pid==ARM else 'hand'}]}}

def unique_sources(sources,b):
 b.require(len({r['sha256'] for r in sources})==len(sources) and len({r['rgbaSha256'] for r in sources})==len(sources),'duplicate source slot bytes/decodedRGBA')

def load_source(q,b):
 r=q['raw'];b.require(r.get('sha256') not in HELD_COMBINED,'held combined lower source forbidden');b.require(set(r)=={'path','sha256','rgbaSha256','width','height'},'raw custody fields');rp=bind({'path':r['path'],'sha256':r['sha256']},b)
 with Image.open(rp) as src:
  b.require(src.mode=='RGBA' and src.size==(1254,1254) and r['width']==1254 and r['height']==1254,'unchanged RGBA1254 required');im=src.copy()
 b.require(hashlib.sha256(im.tobytes()).hexdigest()==r['rgbaSha256'],'decoded RGBA custody')
 evidence=q['sourceEvidence'];b.require(set(evidence)=={'callRecord','rawReview'},'source evidence references required');refs=[bind(evidence[k],b) for k in ('callRecord','rawReview')]
 return im,[rp,*refs]

def project(v,pid,frame,b):
 if pid!=HAND:return b.projected_vertex(v,pid,frame)
 b.require(v['binding']['frame']=='south_wrist_plane','explicit hand plane binding required');x,y=v['binding']['local'];w=frame['points3D']['RIGHT_wrist']
 # Fixed South hypothesis: worldX width and downZ long axis; no forearm-axis foreshortening.
 return [654+w[0]+x,1140+.5*w[1]-w[2]+y]

def targets(s,f,b):
 target=[project(v,s['partId'],f,b) for v in s['mesh']['vertices']];b.require(all(all(math.isfinite(x) and 0<=x<1254 for x in v) for v in target),'projected mesh outside fixed canvas')
 for t in s['mesh']['triangles']:
  src=[s['mesh']['vertices'][i]['rawXY'] for i in t['indices']];dst=[target[i] for i in t['indices']];b.require(b.area(*src)*b.area(*dst)>0,'folded/mirrored triangle');b.affine_inverse(src,dst)
 return target

def draw(canvas,raw,s,f,b):
 # Same sealed-v4 affine_inverse, alpha-aware sampling and indexed partition overwrite.
 dst=targets(s,f,b);layer=Image.new('RGBA',(1254,1254));premult=raw.convert('RGBa')
 for t in s['mesh']['triangles']:
  ids=t['indices'];source=[s['mesh']['vertices'][i]['rawXY'] for i in ids];triangle=[dst[i] for i in ids];coef=b.affine_inverse(source,triangle)
  warped=premult.transform((1254,1254),Image.Transform.AFFINE,coef,Image.Resampling.BILINEAR).convert('RGBA');mask=Image.new('L',(1254,1254));ImageDraw.Draw(mask).polygon([tuple(v) for v in triangle],fill=255);layer.paste(warped,(0,0),mask)
 canvas.alpha_composite(layer)

def neutral(plan):
 f=json.loads(json.dumps(plan['frames'][0]));shift=f['lateralWeightShift'];bob=f['pelvisZ']-480
 for name,q in f['points3D'].items():f['points3D'][name]=[q[0]-shift,q[1],q[2]-bob]
 f['lateralWeightShift']=0;f['pelvisZ']=480;return f

def wrist_report(arm,hand,f,b):
 def vertex(s,name):return {'binding':{'frame':'bone' if s['partId']==ARM else 'south_wrist_plane','local':b.calibration_xy(s['calibration'],s['landmarks'][name]['xy'])}}
 a=project(vertex(arm,'wrist'),ARM,f,b);h=project(vertex(hand,'wrist'),HAND,f,b);tip=project(vertex(hand,'fingertip'),HAND,f,b);w=f['points3D']['RIGHT_wrist'];expected=[654+w[0],1140+.5*w[1]-w[2]]
 b.require(b.same(a,expected,1e-6) and b.same(h,expected,1e-6) and b.same(tip,[expected[0],expected[1]+65],1e-6),'wrist handoff/fixed hand plane mismatch')
 return {'forearmWristScreen':a,'handAttachmentScreen':h,'wristSeamResidualPx':math.dist(a,h),'handTipScreen':tip,'handTipWorld':[w[0],w[1],w[2]-65],'handDepth':w[1],'coreDepthHypothesis':-100,'visibleSeamApproved':False,'handOrientationApproved':False}

def run(ap,hp,op,out):
 b=p.engine();out=pathlib.Path(out);b.require(not out.exists() and out.parent.is_dir(),'no overwrite; existing output parent required');paths=[pathlib.Path(x) for x in (ap,hp,op)];qs=[json.loads(x.read_text()) for x in paths];arm=proposal(qs[0],ARM,b);hand=proposal(qs[1],HAND,b);orders=validate_orders(qs[2],b)
 topology=p.BASE/'part-contract-v4-hand-split.json';b.require(p.sha(topology)==TOPOLOGY_SHA,'hand split contract custody');tc=json.loads(topology.read_text());b.require(tc['originalSlotCount']==11 and tc['forearmBoneLength']==180 and tc['handNominalExtent']==65,'nominal topology hypothesis mismatch')
 for rel,h in tc['preservedPipelinePins'].items():b.require(p.sha(p.BASE/rel)==h,'preserved pipeline pin mismatch')
 araw,arefs=load_source(qs[0],b);hraw,hrefs=load_source(qs[1],b);cp=p.BASE/'parts/core-head-torso-pelvis-01/sidecar-v3.json';up=p.BASE/'parts/arm-right-upper-01/sidecar-v1.json'
 for rel,h in UPPER_PINS.items():b.require(p.sha(up.parent/rel)==h,'sealed upper receipt custody')
 core,craw=b.validate_sidecar(cp,CORE);b.validate_approved_core(core);upper,uraw=b.validate_sidecar(up,UP,UPPER_PINS['sidecar-v1.json']);_,plan=b.locked_inputs();b.require([f['frame'] for f in plan['frames']]==[0,2,4,6],'four locked frames')
 sources=[qs[0]['raw'],qs[1]['raw'],core['raw'],upper['raw']];unique_sources(sources,b)
 custody={str(x):p.sha(x) for x in [*paths,topology,*arefs,*hrefs,cp,*[up.parent/x for x in UPPER_PINS],pathlib.Path(core['raw']['path']),pathlib.Path(upper['raw']['path'])]}
 parts={CORE:(core,craw),UP:(upper,uraw),ARM:(arm,araw),HAND:(hand,hraw)};frames=[('REST',neutral(plan))]+[('F'+str(f['frame']),f) for f in plan['frames']];bounds={};seams={}
 for label,f in frames:
  bounds[label]={}
  for pid,(s,_) in parts.items():v=targets(s,f,b);bounds[label][pid]=[min(x[0] for x in v),min(x[1] for x in v),max(x[0] for x in v),max(x[1] for x in v)]
  seams[label]=wrist_report(arm,hand,f,b)
 stage=pathlib.Path(tempfile.mkdtemp(prefix='.unsealed-four-',dir=out.parent));outputs=[];images=[]
 def save(name,im):im.save(stage/name);outputs.append({'path':name,'sha256':p.sha(stage/name),'rgbaSha256':hashlib.sha256(im.tobytes()).hexdigest(),'width':im.width,'height':im.height})
 try:
  for label,f in frames:
   im=Image.new('RGBA',(1254,1254))
   for pid in orders[label]:s,raw=parts[pid];draw(im,raw,s,f,b)
   images.append((label,im))
   for size in (1254,627,38):save(label+'-UNSEALED-PARTIAL4-MISSING7-'+str(size)+'.png',im if size==1254 else im.resize((size,size),Image.Resampling.LANCZOS))
  for size in (1254,627,38):
   sheet=Image.new('RGBA',(max(5*size,450),size+60),(90,90,90,255));d=ImageDraw.Draw(sheet);d.text((2,2),'UNSEALED_DIAGNOSTIC PARTIAL4 / MISSING7 / NOT KEY',fill='white');d.text((2,17),'Fixed whole canvas '+str(size)+' / hand facing and ordering hypothesis only',fill='white')
   for i,(label,im) in enumerate(images):d.text((i*size+2,36),label,fill='white');sheet.alpha_composite(im.resize((size,size),Image.Resampling.LANCZOS),(i*size,60))
   save('REST-FOURPOSE-UNSEALED-PARTIAL4-MISSING7-'+str(size)+'-sheet.png',sheet)
  receipt={'schema':'south-four-part-split-inspection/v1','status':'UNSEALED_DIAGNOSTIC','partCount':4,'missingOriginalParts':7,'fullContractSlotCount':11,'finishedKey':False,'motionQualified':False,'sealedSidecarCreated':False,'sourcePurposeDeclarations':[q['purpose'] for q in qs[:2]],'sourceEvidenceVerification':'Reference byte custody only; parent separately verifies actual source calls/raw inspections/visual assembly.','topologySha256':TOPOLOGY_SHA,'sourceCustody':custody,'proposedLayerOrderByPose':orders,'orderingEvidenceByPose':qs[2]['evidenceByPose'],'fullElevenPartOrderingApproved':False,'handPlane':'Fixed worldX/downZ65 wrist anchored South hypothesis, not motion approval','wristHandoffReports':seams,'geometryBoundsByPose':bounds,'endpointSemantics':{ARM:qs[0]['endpoints'],HAND:qs[1]['endpoints']},'immutableUniformCalibrations':{ARM:qs[0]['calibration'],HAND:qs[1]['calibration']},'sourceCoverage':'Full unchanged original1254 quad; all alpha retained, no crop/mirror/anisotropic fit/per-pose sourcefit','cameraRoot':[654,1140],'wholeCanvasLogicalSize':38,'numericFitToleranceIsAnatomicalPrecision':False,'outputs':outputs,'toolSha256':p.sha(__file__)}
  for path,h in custody.items():b.require(p.sha(path)==h,'custody changed during diagnostic')
  b.locked_inputs();p.engine();(stage/'inspection.json').write_text(json.dumps(receipt,indent=2)+'\n');b.publish_no_replace(stage,out);return receipt
 finally:
  if stage.exists():shutil.rmtree(stage)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('forearmProposal');parser.add_argument('handProposal');parser.add_argument('ordersProposal');parser.add_argument('output');a=parser.parse_args()
 try:print(json.dumps({'status':run(a.forearmProposal,a.handProposal,a.ordersProposal,a.output)['status']}))
 except (ValueError,KeyError,OSError,TypeError) as e:print(json.dumps({'status':'REFUSED_NO_OUTPUT','reason':str(e)}));raise SystemExit(2)
