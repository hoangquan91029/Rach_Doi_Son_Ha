"""Internal four-key bitmap authoring only. Fixtures never qualify actual art."""
import argparse, ctypes, hashlib, importlib.util, json, math, os, pathlib, shutil, tempfile, sys
sys.dont_write_bytecode=True
from PIL import Image, ImageDraw
BASE=pathlib.Path(__file__).resolve().parents[1]
CONTRACT_SHA='e4715f935a88952a7f6d477d29879641fda6041bf4e783169c6664a386afa7bc'
OLD_SHA='b0c2bb4c040dd3fda22aa11afa6b3381ad13fa4a5ba79b0207e25bf9e8626cb8'
PLAN_SHA='dd685b2b444e8c1b1cdcab04be06d92651c81657cf265489c90cee56203abfcf'
KEYS=(0,2,4,6)
PARTS=('core_head_torso_pelvis','arm_right_upper','arm_right_lower_hand','arm_left_upper','arm_left_lower_hand','leg_right_upper','leg_right_lower_sandal','leg_left_upper','leg_left_lower_sandal')
CORE_POINTS=('actor_left_shoulder_cap','actor_right_shoulder_cap','actor_left_hip_under_hem','actor_right_hip_under_hem')
class Refusal(ValueError):pass
def require(condition,message):
 if not condition:raise Refusal(message)
def digest(path):return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()
def load(path):return json.loads(pathlib.Path(path).read_text())
def finite(v,n):return isinstance(v,list) and len(v)==n and all(type(x) in (int,float) and math.isfinite(x) for x in v)
def same(a,b,tol=1e-7):return math.dist(a,b)<=tol

IDENTITY_VIEWS={'N':(5,'NW'),'NE':(6,'N'),'E':(7,'NE'),'SE':(0,'E'),'S':(1,'SE'),'SW':(2,'S'),'W':(3,'SW'),'NW':(4,'W')}
def validate_identity(lock_path,expected_sha):
 require(digest(lock_path)==expected_sha,'identity lock custody mismatch')
 lock=load(lock_path)
 require(lock.get('schema')=='villager-eight-static-identity/v1' and lock.get('status')=='PASS_STATIC_IDENTITY_LOCK_FOR_SOUTH_AUTHORING_ONLY','unsealed eight-view identity lock')
 require(lock.get('canvas')==[1254,1254] and lock.get('camera')=={'projection':'dimetric','ratio':[2,1],'tile':[54,27],'elevation':26.565},'identity camera/canvas mismatch')
 frames=lock['frames'];require(set(frames)==set(IDENTITY_VIEWS),'exactly eight identity originals required')
 hashes={}
 for view,f in frames.items():
  path=pathlib.Path(f['path']);require(path.is_absolute() and path.is_file(),'missing identity original: '+view)
  require(f.get('fullBodyInspected') is True and f.get('status')=='STATIC_IDENTITY_REFERENCE_CANDIDATE','unreviewed identity original: '+view)
  require((f.get('engineDirection'),f.get('worldDirection'))==IDENTITY_VIEWS[view],'identity direction mismatch: '+view)
  require(digest(path)==f['sha256'],'identity original byte custody mismatch: '+view)
  with Image.open(path) as im:
   require(im.mode=='RGBA' and im.size==(1254,1254),'identity original mode/dimension mismatch: '+view)
   require(hashlib.sha256(im.tobytes()).hexdigest()==f['rgbaSha256'],'identity original decodedRGBA custody mismatch: '+view)
  hashes[view]=f['sha256']
 seal=lock['review'];require(seal.get('frameHashes')==hashes,'identity lock review does not bind eight sources')
 require(digest(seal['receiptPath'])==seal['receiptSha256'],'identity parent review custody mismatch')
 review=load(seal['receiptPath'])
 require(review.get('schema')=='villager-static-identity-review/v1' and review.get('status')==lock['status'],'identity parent review status mismatch')
 require(review.get('frameHashes')==hashes and set(review.get('frames',{}))==set(IDENTITY_VIEWS),'parent review must bind all eight original hashes')
 require(review.get('canvas')==lock['canvas'] and review.get('camera')==lock['camera'] and review.get('sourcePivot')==[654,1140] and review.get('wholeCanvasLogicalSize')==38,'parent identity review camera/root mismatch')
 require(review.get('scope',{}).get('southWalkKeyAuthoring') is True and review['scope'].get('otherAnimationDirections') is False,'identity review authoring scope mismatch')
 for view,f in frames.items():
  rf=review['frames'][view]
  for field in ('sha256','rgbaSha256','fullBodyInspected','engineDirection','worldDirection','status'):
   require(rf.get(field)==f[field],'parent reviewed identity source differs: '+view+'/'+field)
 return lock

def core_targets():return load(BASE/'part-contract-v3.json')['core_rest_adjustment']['attachmentTargets']
def validate_core_model_projection(contract,plan):
 targets=contract['core_rest_adjustment']['attachmentTargets']
 for frame in plan['frames']:
  shift=frame['lateralWeightShift'];bob=frame['pelvisZ']-480
  for side in ('LEFT','RIGHT'):
   for name,joint in [('shoulder_cap','shoulder'),('hip_under_hem','hip')]:
    rest=targets['actor_'+side.lower()+'_'+name]['restScreenXY'];q=frame['points3D'][side+'_'+joint]
    require(same([654+q[0],1140+.5*q[1]-q[2]],[rest[0]+shift,rest[1]-bob],1e-8),'core anchor/3D model projection mismatch')
def validate_approved_core(s):
 a=load(BASE/'part-contract-v3.json')['core_rest_adjustment'];raw=s['raw'];c=s['calibration']
 require(raw['sha256']==a['coreRawSha256'] and raw['rgbaSha256']==a['coreRgbaSha256'],'actual core is not the approved immutable original')
 require({k:c[k] for k in ('scale','rotationRad','translation')}==a['calibration'],'actual core static calibration differs from approved proposal')
 for name,t in a['attachmentTargets'].items():
  lm=s['landmarks'][name]
  require(lm['xy']==t['sourceRawXY'] and lm['method']==t['method'] and lm['uncertaintyPx']==t['uncertaintySourcePx'],'actual core authored attachment convention differs from reviewed proposal')
def validate_pose_geometry(pid,s,plan):
 bounds={}
 for frame in plan['frames']:
  target=[projected_vertex(v,pid,frame) for v in s['mesh']['vertices']]
  require(all(all(math.isfinite(x) and 0<=x<1254 for x in p) for p in target),'projected mesh outside canvas')
  for tri in s['mesh']['triangles']:
   src=[s['mesh']['vertices'][i]['rawXY'] for i in tri['indices']];dst=[target[i] for i in tri['indices']]
   require(area(*src)*area(*dst)>0,'projected triangle folded or mirrored');affine_inverse(src,dst)
  bounds['F'+str(frame['frame'])]=[min(p[0] for p in target),min(p[1] for p in target),max(p[0] for p in target),max(p[1] for p in target)]
 return bounds

def locked_inputs():
 cp=BASE/'part-contract-v3.json';require(digest(cp)==CONTRACT_SHA,'contract custody mismatch')
 c=load(cp);lock=c['identity_lock'];validate_identity(lock['lock_path'],lock['lock_sha256'])
 raw=lock['primary_south_reference'];require(digest(raw['path'])==raw['sha256'],'South identity source custody mismatch')
 pp=BASE.parent/'pose-guides/walk-south-keys-v3/coordinate-plan.json';require(digest(pp)==PLAN_SHA,'pose plan custody mismatch')
 old=BASE/'tooling/rig_preflight.py';require(digest(old)==OLD_SHA,'sealed numeric planner custody mismatch')
 spec=importlib.util.spec_from_file_location('sealed_planner',old);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 plan=load(pp);mod.geometry(plan);validate_core_model_projection(c,plan)
 return c,plan

def calibration_xy(cal,xy):
 s=cal['scale'];r=cal['rotationRad'];x,y=xy;tx,ty=cal['translation']
 return [s*(math.cos(r)*x-math.sin(r)*y)+tx,s*(math.sin(r)*x+math.cos(r)*y)+ty]
def part_kind(pid):
 if pid==PARTS[0]:return 'core',None,None,None
 side='LEFT' if '_left_' in pid else 'RIGHT'
 if pid.startswith('arm_'):return 'bone',side,('shoulder','elbow',200) if pid.endswith('_upper') else ('elbow','wrist',180),None
 if pid.endswith('_upper'):return 'bone',side,('hip','knee',260),None
 return 'lower',side,('knee','ankle',240),None

def rest_xy(binding,kind,L):
 require(set(binding)=={'frame','local'},'unknown binding fields')
 frame=binding['frame'];p=binding['local']
 if frame=='core':require(kind=='core' and finite(p,2),'invalid core binding');return p
 if frame=='bone':require(kind!='core' and finite(p,2),'invalid bone binding');return p
 require(frame=='foot' and kind=='lower' and finite(p,3),'invalid foot binding')
 return [p[0],L+.5*p[1]-p[2]]
def area(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def boundary(tris):
 edges={}
 for tri in tris:
  for a,b in zip(tri,tri[1:]+tri[:1]):
   e=tuple(sorted((a,b)));edges[e]=edges.get(e,0)+1
 require(all(v<=2 for v in edges.values()),'nonmanifold mesh')
 return {e for e,n in edges.items() if n==1}

def validate_partition(vertices,triangles):
 inds=[t['indices'] for t in triangles];boundary(inds)
 signs=[area(*[vertices[i]['rawXY'] for i in t]) for t in inds]
 require(all(x*signs[0]>0 for x in signs),'inconsistent source mesh winding')
 def inside(p,t):
  a,b,c=t;s=[area(a,b,p),area(b,c,p),area(c,a,p)]
  return min(s)>1e-7 or max(s)<-1e-7
 def crosses(a,b,c,d):return area(a,b,c)*area(a,b,d)<-1e-7 and area(c,d,a)*area(c,d,b)<-1e-7
 for n,ta in enumerate(inds):
  a=[vertices[i]['rawXY'] for i in ta]
  for tb in inds[n+1:]:
   b=[vertices[i]['rawXY'] for i in tb]
   require(not any(inside(p,b) for p in a) and not any(inside(p,a) for p in b),'overlapping source triangle interiors')
   require(not any(crosses(x,y,u,v) for x,y in zip(a,a[1:]+a[:1]) for u,v in zip(b,b[1:]+b[:1])),'crossing source mesh edges')

def validate_sidecar(path,expected_pid,expected_sha=None):
 path=pathlib.Path(path)
 if expected_sha:require(digest(path)==expected_sha,'sidecar custody mismatch: '+expected_pid)
 s=load(path);require(set(s)=={'schema','partId','status','raw','calibration','landmarks','mesh'},'unknown sidecar fields');require(s.get('schema')=='south-bitmap-rig-sidecar/v3','unknown sidecar schema')
 require(s.get('partId')==expected_pid and expected_pid in PARTS,'unknown or wrong part identity')
 require(s.get('status')=='SEALED_ORIGINAL_CALIBRATION','unsealed sidecar')
 raw=s['raw'];require(set(raw)=={'path','sha256','rgbaSha256','width','height'},'unknown raw custody fields');rp=pathlib.Path(raw['path']);require(rp.is_absolute(),'absolute original path required')
 require(digest(rp)==raw['sha256'],'raw byte custody mismatch')
 with Image.open(rp) as im:
  require(im.mode=='RGBA' and im.size==(1254,1254),'original must be 1254 RGBA')
  require(raw.get('width')==1254 and raw.get('height')==1254,'source dimensions mismatch')
  require(hashlib.sha256(im.tobytes()).hexdigest()==raw['rgbaSha256'],'raw RGBA custody mismatch')
  image=im.copy()
 cal=s['calibration'];require(set(cal)=={'scale','rotationRad','translation','tolerancePx'},'unknown calibration fields')
 require(type(cal['scale']) in (int,float) and math.isfinite(cal['scale']) and cal['scale']>0,'invalid static uniform scale')
 require(type(cal['rotationRad']) in (int,float) and math.isfinite(cal['rotationRad']) and finite(cal['translation'],2),'invalid static uniform transform')
 require(type(cal['tolerancePx']) in (int,float) and 0<=cal['tolerancePx']<=2,'calibration tolerance must be finite 0..2px')
 kind,side,bone,_=part_kind(expected_pid);L=bone[2] if bone else 0
 landmarks=s['landmarks'];required=set(CORE_POINTS) if kind=='core' else {bone[0],bone[1]}
 if kind=='lower':required|={'heel','toe','solePlane'}
 require(required<=set(landmarks),'missing natural landmarks')
 for name,lm in landmarks.items():
  require(set(lm)=={'xy','method','uncertaintyPx','evidence'},'unknown landmark fields')
  require(finite(lm['xy'],2) and all(0<=x<=1254 for x in lm['xy']),'invalid natural landmark coordinates')
  require(lm['method'] in ('observed_original','authored_hidden_hypothesis','authored_cloth_attachment_convention'),'unknown landmark method')
  require(type(lm['uncertaintyPx']) in (int,float) and math.isfinite(lm['uncertaintyPx']) and 0<=lm['uncertaintyPx']<=120,'invalid uncertainty')
  require(isinstance(lm['evidence'],str) and bool(lm['evidence'].strip()),'landmark evidence missing')
  if lm['method']=='authored_hidden_hypothesis':require('hip' in name,'only hidden hips may use authored hypothesis')
  if lm['method']=='authored_cloth_attachment_convention':require(name in ('shoulder','actor_left_shoulder_cap','actor_right_shoulder_cap'),'cloth attachment convention is shoulder-only')
 for name in required:
  if 'hip' in name:require(landmarks[name]['method']=='authored_hidden_hypothesis','hidden hip must be an authored hypothesis: '+name)
 if kind=='core':
  for name in CORE_POINTS:
   target=core_targets()[name]['restScreenXY']
   if 'shoulder' in name:require(landmarks[name]['method']=='authored_cloth_attachment_convention','core cap must be an authored cloth convention')
   require(same(calibration_xy(cal,landmarks[name]['xy']),target,cal['tolerancePx']),'core attachment rest calibration mismatch: '+name)
 if kind!='core':
  for name,target in [(bone[0],[0,0]),(bone[1],[0,L])]:require(same(calibration_xy(cal,landmarks[name]['xy']),target,cal['tolerancePx']),'natural endpoint calibration mismatch: '+name)
 if kind=='lower':
  for name,target in [('heel',[0,L+35]),('toe',[0,L+115]),('solePlane',[0,L+75])]:
   require(landmarks[name]['method']=='observed_original','foot landmark must be observed')
   require(same(calibration_xy(cal,landmarks[name]['xy']),target,cal['tolerancePx']),'rigid foot rest correspondence mismatch: '+name)
 mesh=s['mesh'];require(set(mesh)=={'vertices','triangles','sharedAnkleSeam'},'unknown mesh fields')
 vertices=mesh['vertices'];require(isinstance(vertices,list) and 3<=len(vertices)<=128,'bounded mesh vertices required')
 for v in vertices:
  require(set(v)=={'rawXY','binding'} and finite(v['rawXY'],2) and all(0<=x<=1254 for x in v['rawXY']),'invalid source mesh vertex')
  rest=rest_xy(v['binding'],kind,L)
  require(same(calibration_xy(cal,v['rawXY']),rest,cal['tolerancePx']),'immutable raw/rest mesh correspondence mismatch')
 require(len({tuple(v['rawXY']) for v in vertices})==len(vertices),'duplicate rawXY mesh vertices; shared seam must reuse indices')
 triangles=mesh['triangles'];require(isinstance(triangles,list) and 1<=len(triangles)<=256,'bounded triangle mesh required')
 regions={'core'} if kind=='core' else {'shin','foot'} if kind=='lower' else {'bone'}
 grouped={r:[] for r in regions};seen=set()
 for t in triangles:
  require(set(t)=={'indices','region'} and t['region'] in regions,'unknown semantic mesh region')
  inds=t['indices'];require(isinstance(inds,list) and len(inds)==3 and all(type(i)==int and 0<=i<len(vertices) for i in inds) and len(set(inds))==3,'invalid triangle indices')
  require(tuple(sorted(inds)) not in seen,'duplicate triangle');seen.add(tuple(sorted(inds)))
  require(abs(area(*[vertices[i]['rawXY'] for i in inds]))>1e-6,'degenerate source triangle')
  if t['region']=='foot':require(all(vertices[i]['binding']['frame']=='foot' for i in inds),'sole must remain independently rigid')
  elif kind!='lower':require(all(vertices[i]['binding']['frame']==('core' if kind=='core' else 'bone') for i in inds),'invalid rigid region binding')
  grouped[t['region']].append(inds)
 require(all(grouped.values()),'missing semantic region')
 validate_partition(vertices,triangles)
 coverage=Image.new('L',(1254,1254));coverage_draw=ImageDraw.Draw(coverage)
 for t in triangles:coverage_draw.polygon([tuple(vertices[i]['rawXY']) for i in t['indices']],fill=255)
 # An explicit semantic mesh may partition art, never silently erase alpha/fringes.
 from PIL import ImageChops
 omitted=ImageChops.multiply(image.getchannel('A'),ImageChops.invert(coverage))
 require(omitted.getbbox() is None,'source alpha outside authored mesh; no cleanup/cutting permitted')
 seam=mesh['sharedAnkleSeam']
 if kind=='lower':
  require(isinstance(seam,list) and 2<=len(seam)<=16 and len(set(seam))==len(seam),'shared ankle seam required')
  require(all(type(i)==int and 0<=i<len(vertices) for i in seam),'unknown ankle seam index')
  edges={tuple(sorted(e)) for e in zip(seam,seam[1:])}
  require(boundary(grouped['shin'])&boundary(grouped['foot'])==edges,'shin/foot polygons do not share exact ankle boundary')
  for i in seam:
   b=vertices[i]['binding'];require(b['frame']=='foot' and abs(b['local'][1])+abs(b['local'][2])<1e-8,'shared seam must use same rigid ankle plane')
  for t in grouped['shin']:
   for i in t:require(vertices[i]['binding']['frame']=='bone' or i in seam,'shin foot binding outside shared seam')
 else:require(seam==[],'unexpected ankle seam')
 return s,image

def projected_vertex(v,pid,frame):
 kind,side,bone,_=part_kind(pid);binding=v['binding'];local=binding['local'];p=frame['points3D']
 if kind=='core':return [local[0]+frame['lateralWeightShift'],local[1]-(frame['pelvisZ']-480)]
 if binding['frame']=='foot':
  a=p[side+'_ankle'];return [654+a[0]+local[0],1140+.5*(a[1]+local[1])-(a[2]+local[2])]
 a,b=p[side+'_'+bone[0]],p[side+'_'+bone[1]];L=bone[2]
 axis=[(b[i]-a[i])/L for i in range(3)]
 width=[(1 if i==0 else 0)-axis[0]*axis[i] for i in range(3)];n=math.sqrt(sum(x*x for x in width));require(n>1e-6,'singular camera bone plane');width=[x/n for x in width]
 pt=[a[i]+width[i]*local[0]+axis[i]*local[1] for i in range(3)]
 return [654+pt[0],1140+.5*pt[1]-pt[2]]

def affine_inverse(src,dst):
 # Solve two 3x3 systems explicitly: destination -> immutable source pixels.
 den=area(*dst);require(abs(den)>1e-5,'singular projected triangle')
 x0,y0=dst[0];x1,y1=dst[1];x2,y2=dst[2]
 def solve(vals):
  v0,v1,v2=vals
  a=((v1-v0)*(y2-y0)-(v2-v0)*(y1-y0))/den
  b=((x1-x0)*(v2-v0)-(x2-x0)*(v1-v0))/den
  return [a,b,v0-a*x0-b*y0]
 return tuple(solve([p[0] for p in src])+solve([p[1] for p in src]))
def draw_part(canvas,image,sidecar,frame):
 verts=sidecar['mesh']['vertices'];target=[projected_vertex(v,sidecar['partId'],frame) for v in verts]
 # Shared indexed vertices have ONE target; they cannot split at the ankle seam.
 for p in target:require(all(math.isfinite(x) and 0<=x<1254 for x in p),'projected art mesh exceeds fixed whole canvas')
 layer=Image.new('RGBA',(1254,1254))
 premult=image.convert('RGBa') # Standard alpha-aware sampling; never edits original bytes.
 for tri in sidecar['mesh']['triangles']:
  inds=tri['indices'];src=[verts[i]['rawXY'] for i in inds];dst=[target[i] for i in inds]
  require(area(*src)*area(*dst)>0,'projected triangle folded or mirrored')
  coef=affine_inverse(src,dst)
  warped=premult.transform((1254,1254),Image.Transform.AFFINE,coef,Image.Resampling.BILINEAR).convert('RGBA')
  mask=Image.new('L',(1254,1254));ImageDraw.Draw(mask).polygon([tuple(p) for p in dst],fill=255)
  # Replace within each partition, rather than doubling semitransparent shared edges.
  layer.paste(warped,(0,0),mask)
 canvas.alpha_composite(layer)
 return target

def validate_manifest(manifest,contract,plan):
 require(set(manifest)=={'schema','purpose','parts','layerOrderByKey','reviewReceipt'},'unknown manifest fields')
 require(manifest['schema']=='south-four-key-bake/v3','unknown manifest schema')
 require(manifest['purpose'] in ('ACTUAL_ORIGINAL_PARTS','NON_ART_TEMPORARY_FIXTURE'),'unknown input purpose')
 require(set(manifest['parts'])==set(PARTS),'missing or unknown original parts; all nine required')
 rr=manifest['reviewReceipt'];require(set(rr)=={'path','sha256'},'review receipt required')
 require(digest(rr['path'])==rr['sha256'],'review receipt custody mismatch')
 review=load(rr['path']);expected='SEALED_PART_CALIBRATIONS_FOR_FOUR_KEY_AUTHORING' if manifest['purpose']=='ACTUAL_ORIGINAL_PARTS' else 'NON_ART_TECHNICAL_FIXTURE_ONLY'
 require(review.get('status')==expected,'part/calibration authoring review missing')
 require(review.get('contractSha256')==CONTRACT_SHA and review.get('posePlanSha256')==PLAN_SHA,'review camera/topology mismatch')
 require(review.get('sidecarHashes')=={pid:r['sha256'] for pid,r in manifest['parts'].items()},'review does not bind all nine calibrations')
 loaded={}
 for pid,r in manifest['parts'].items():
  require(set(r)=={'path','sha256'},'unknown source record fields')
  loaded[pid]=validate_sidecar(r['path'],pid,r['sha256'])
 require(set(manifest['layerOrderByKey'])=={'F'+str(k) for k in KEYS},'only four explicit key layer orders allowed')
 for k in KEYS:
  order=manifest['layerOrderByKey']['F'+str(k)]
  require(len(order)==9 and set(order)==set(PARTS),'explicit per-pose layer order must contain each original once')
 require(review.get('layerOrderByKey')==manifest['layerOrderByKey'],'occlusion order is not review-bound')
 # All rendering geometry must validate BEFORE any output directory exists.
 for pid,(s,_) in loaded.items():validate_pose_geometry(pid,s,plan)
 if manifest['purpose']=='ACTUAL_ORIGINAL_PARTS':validate_approved_core(loaded[PARTS[0]][0])
 return loaded

def publish_no_replace(stage,out):
 # Linux atomic directory publication with an explicit NOREPLACE guarantee.
 libc=ctypes.CDLL(None,use_errno=True);rename=getattr(libc,'renameat2',None)
 require(rename is not None,'atomic no-overwrite publication unsupported on this platform')
 rename.argtypes=[ctypes.c_int,ctypes.c_char_p,ctypes.c_int,ctypes.c_char_p,ctypes.c_uint];rename.restype=ctypes.c_int
 if rename(-100,os.fsencode(stage),-100,os.fsencode(out),1)!=0:
  err=ctypes.get_errno()
  raise Refusal('atomic publication refused: '+os.strerror(err))

def bake(manifest_path,output):
 out=pathlib.Path(output);require(not out.exists(),'refuse existing output; never overwrite')
 manifest_sha=digest(manifest_path)
 contract,plan=locked_inputs();manifest=load(manifest_path);loaded=validate_manifest(manifest,contract,plan)
 sources={pid:{'sidecarSha256':digest(manifest['parts'][pid]['path']),'byteSha256':s['raw']['sha256'],'rgbaSha256':s['raw']['rgbaSha256']} for pid,(s,_) in loaded.items()}
 require(out.parent.exists(),'output parent must already exist')
 stage=pathlib.Path(tempfile.mkdtemp(prefix='.four-key-stage-',dir=out.parent));outputs=[]
 try:
  for frame in plan['frames']:
   k=frame['frame'];im=Image.new('RGBA',(1254,1254));targets={}
   for pid in manifest['layerOrderByKey']['F'+str(k)]:
    s,raw=loaded[pid];targets[pid]=draw_part(im,raw,s,frame)
   path=stage/('F'+str(k)+'.png');im.save(path)
   outputs.append({'key':k,'timeMs':frame['timeMs'],'support':frame['support'],'swing':frame['swing'],'path':path.name,'width':1254,'height':1254,'pivot':[654,1140],'wholeCanvasLogicalSize':38,'sha256':digest(path),'rgbaSha256':hashlib.sha256(im.tobytes()).hexdigest(),'projectedMeshVertices':targets})
  # Detect changed original/sidecar bytes during rendering; do not publish partial results.
  for pid,(s,_) in loaded.items():
   require(digest(s['raw']['path'])==s['raw']['sha256'],'source changed during baking')
   require(digest(manifest['parts'][pid]['path'])==manifest['parts'][pid]['sha256'],'sidecar changed during baking')
  require(digest(manifest_path)==manifest_sha,'manifest changed during baking')
  require(digest(manifest['reviewReceipt']['path'])==manifest['reviewReceipt']['sha256'],'review changed during baking')
  locked_inputs()
  status='SOURCE_BAKED_RIG_REQUIRES_FINISHED_ILLUSTRATION_REVIEW' if manifest['purpose']=='ACTUAL_ORIGINAL_PARTS' else 'NON_ART_AUTHORING_DIAGNOSTIC_NOT_QUALIFICATION'
  receipt={'schema':'south-four-key-bake-receipt/v3','status':status,'candidate':False,'motionQualified':False,'finalArtApproved':False,'imageCalls':0,'runtimeIntegrated':False,'manifestSha256':manifest_sha,'reviewReceiptSha256':manifest['reviewReceipt']['sha256'],'toolSha256':digest(__file__),'contractSha256':CONTRACT_SHA,'posePlanSha256':PLAN_SHA,'sourceCustody':sources,'outputs':outputs,'nominalReviewPeriodMs':600,'strideHypothesis':plan['strideHypothesis'],'scope':'Four discrete keys only; no atlas, in-betweens or loop qualification. Numeric contact and mesh continuity do not establish illustrated quality.'}
  (stage/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
  require(not out.exists(),'output appeared during bake; refuse overwrite')
  publish_no_replace(stage,out)
  return receipt
 finally:
  if stage.exists():shutil.rmtree(stage)

def main():
 parser=argparse.ArgumentParser();sub=parser.add_subparsers(dest='command',required=True)
 b=sub.add_parser('bake');b.add_argument('manifest');b.add_argument('output')
 i=sub.add_parser('inspect-sidecar');i.add_argument('partId');i.add_argument('path')
 args=parser.parse_args()
 try:
  if args.command=='bake':r=bake(args.manifest,args.output);print(json.dumps({'status':r['status'],'candidate':False,'outputs':len(r['outputs'])}))
  else:
   contract,plan=locked_inputs();s,_=validate_sidecar(args.path,args.partId)
   if args.partId==PARTS[0]:validate_approved_core(s)
   bounds=validate_pose_geometry(args.partId,s,plan)
   print(json.dumps({'status':'PARTIAL_REST_INSPECTION_ONLY','partId':s['partId'],'candidate':False,'outputsWritten':0,'canvas':[1254,1254],'pivot':[654,1140],'sourceByteSha256':s['raw']['sha256'],'sourceRgbaSha256':s['raw']['rgbaSha256'],'calibration':s['calibration'],'fullCharacter':False,'animationKey':False,'allFourPoseGeometryChecked':True,'projectedMeshBounds':bounds,'sourceAlphaOutsideMesh':0}))
 except (Refusal,KeyError,OSError,TypeError,ValueError) as e:
  print(json.dumps({'status':'REFUSED_NO_PUBLISHED_OUTPUT','candidate':False,'reason':str(e),'imageCalls':0}));return 2
 return 0
if __name__=='__main__':raise SystemExit(main())
