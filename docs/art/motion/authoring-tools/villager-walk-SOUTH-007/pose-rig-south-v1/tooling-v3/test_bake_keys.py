"""Temporary NON_ART bitmap fixtures. These checks never qualify artist output."""
import copy,hashlib,json,pathlib,tempfile,unittest
from PIL import Image,ImageDraw
import bake_keys as b

def write_json(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def lm(xy,hidden=False):return {'xy':xy,'method':'authored_hidden_hypothesis' if hidden else 'observed_original','uncertaintyPx':1,'evidence':'NON_ART temporary numeric fixture, not an anatomical measurement'}
def fixture(root):
 records={};originals={}
 for pid in b.PARTS:
  kind,side,bone,_=b.part_kind(pid);L=bone[2] if bone else 0
  raw=root/(pid+'-NON_ART.png');sidecar=root/(pid+'-NON_ART.json');im=Image.new('RGBA',(1254,1254));draw=ImageDraw.Draw(im)
  cal={'scale':1,'rotationRad':0,'translation':[0,0] if kind=='core' else [-500,-300],'tolerancePx':0.01}
  if kind=='core':
   coords=[[520,130],[788,130],[788,640],[520,640]]
   vertices=[{'rawXY':p,'binding':{'frame':'core','local':p}} for p in coords]
   triangles=[{'indices':[0,1,2],'region':'core'},{'indices':[0,2,3],'region':'core'}];seam=[]
   landmarks={n:lm(p,'hip' in n) for n,p in zip(b.CORE_POINTS,[[834,300],[474,300],[754,610],[554,610]])}
   draw.polygon([tuple(p) for p in coords],fill=(170,110,50,255))
  else:
   coords=[[-12,0],[12,0],[12,L],[-12,L]]
   vertices=[{'rawXY':[500+x,300+y],'binding':{'frame':'bone','local':[x,y]}} for x,y in coords]
   triangles=[{'indices':[0,1,2],'region':'shin' if kind=='lower' else 'bone'},{'indices':[0,2,3],'region':'shin' if kind=='lower' else 'bone'}];seam=[]
   landmarks={bone[0]:lm([500,300],bone[0]=='hip'),bone[1]:lm([500,300+L])}
   draw.polygon([(500+x,300+y) for x,y in coords],fill=(50,70,220,255))
   if kind=='lower':
    for i in (2,3):vertices[i]['binding']={'frame':'foot','local':[coords[i][0],0,0]}
    vertices += [{'rawXY':[532,300+L+125],'binding':{'frame':'foot','local':[32,130,-60]}},{'rawXY':[468,300+L+125],'binding':{'frame':'foot','local':[-32,130,-60]}}]
    triangles += [{'indices':[3,2,4],'region':'foot'},{'indices':[3,4,5],'region':'foot'}];seam=[3,2]
    draw.polygon([(488,300+L),(512,300+L),(532,300+L+125),(468,300+L+125)],fill=(30,160,70,255))
    for name,y,color in [('heel',L+35,(255,0,0,255)),('toe',L+115,(255,0,255,255)),('solePlane',L+75,None)]:
     landmarks[name]=lm([500,300+y])
     if color:draw.rectangle((497,300+y-3,503,300+y+3),fill=color)
  im.save(raw);originals[pid]=b.digest(raw)
  s={'schema':'south-bitmap-rig-sidecar/v2','partId':pid,'status':'SEALED_ORIGINAL_CALIBRATION','raw':{'path':str(raw),'sha256':b.digest(raw),'rgbaSha256':hashlib.sha256(im.tobytes()).hexdigest(),'width':1254,'height':1254},'calibration':cal,'landmarks':landmarks,'mesh':{'vertices':vertices,'triangles':triangles,'sharedAnkleSeam':seam}}
  write_json(sidecar,s);records[pid]={'path':str(sidecar),'sha256':b.digest(sidecar)}
 order={ 'F'+str(k):list(b.PARTS) for k in b.KEYS }
 review=root/'NON_ART-review.json';write_json(review,{'status':'NON_ART_TECHNICAL_FIXTURE_ONLY','contractSha256':b.CONTRACT_SHA,'posePlanSha256':b.PLAN_SHA,'sidecarHashes':{p:r['sha256'] for p,r in records.items()},'layerOrderByKey':order})
 manifest={'schema':'south-four-key-bake/v2','purpose':'NON_ART_TEMPORARY_FIXTURE','parts':records,'layerOrderByKey':order,'reviewReceipt':{'path':str(review),'sha256':b.digest(review)}}
 mp=root/'NON_ART-manifest.json';write_json(mp,manifest)
 return mp,manifest,originals

class BakeTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tmp=tempfile.TemporaryDirectory(prefix='NON_ART_bitmap_rig_');cls.root=pathlib.Path(cls.tmp.name);cls.mp,cls.manifest,cls.originals=fixture(cls.root)
  cls.contract,cls.plan=b.locked_inputs();cls.receipt=b.bake(cls.mp,cls.root/'output')
 @classmethod
 def tearDownClass(cls):cls.tmp.cleanup()
 def test_four_whole_rgba_with_custody_and_sources_preserved(self):
  self.assertEqual(len(self.receipt['outputs']),4);self.assertFalse(self.receipt['candidate']);self.assertIn('NON_ART',self.receipt['status'])
  for out in self.receipt['outputs']:
   path=self.root/'output'/out['path'];self.assertEqual(b.digest(path),out['sha256'])
   with Image.open(path) as im:self.assertEqual(im.mode,'RGBA');self.assertEqual(im.size,(1254,1254));self.assertEqual(hashlib.sha256(im.tobytes()).hexdigest(),out['rgbaSha256'])
  for pid,h in self.originals.items():self.assertEqual(b.digest(self.root/(pid+'-NON_ART.png')),h)
 def test_actual_raster_support_markers_world_planting(self):
  outputs={o['key']:o for o in self.receipt['outputs']};raster_world={}
  for a,c,side in [(0,2,'LEFT'),(4,6,'RIGHT')]:
   pid='leg_'+side.lower()+'_lower_sandal'
   for key in (a,c):
    frame=next(f for f in self.plan['frames'] if f['frame']==key);s,_=b.validate_sidecar(self.manifest['parts'][pid]['path'],pid)
    with Image.open(self.root/'output'/('F'+str(key)+'.png')) as im:
     for name,color,offset in [('heel',(255,0,0),[-0.0,-50,-60]),('toe',(255,0,255),[0,110,-60])]:
      q=b.projected_vertex({'binding':{'frame':'foot','local':offset}},pid,frame);x,y=map(round,q)
      # Inspect actual resampled bitmap neighborhood, not merely target metadata.
      pixels=[im.getpixel((x+dx,y+dy)) for dx in range(-2,3) for dy in range(-2,3)]
      self.assertTrue(any(p[:3]==color and p[3]>240 for p in pixels),(key,name,q))
      cluster=[(x+dx,y+dy) for dx in range(-8,9) for dy in range(-8,9) if im.getpixel((x+dx,y+dy))[:3]==color and im.getpixel((x+dx,y+dy))[3]>240]
      self.assertTrue(cluster)
      centroid=[sum(p[j] for p in cluster)/len(cluster) for j in (0,1)]
      raster_world[(key,name)]=[centroid[0],centroid[1]+.5*frame['bodyTravelDepth']]
      world=frame['points3D'][side+'_'+name];world=[world[0],world[1]+frame['bodyTravelDepth'],world[2]]
      other=next(f for f in self.plan['frames'] if f['frame']==(c if key==a else a));ow=other['soles'][side]['world'+name.title()]
      self.assertLess(math_distance(world,ow),1e-8)
   for name in ('heel','toe'):self.assertLess(math_distance_2(raster_world[(a,name)],raster_world[(c,name)]),1.5)
 def test_shared_ankle_seam_raster_has_no_transparent_crack(self):
  for key in b.KEYS:
   frame=next(f for f in self.plan['frames'] if f['frame']==key)
   for side in ('left','right'):
    pid='leg_'+side+'_lower_sandal';s,raw=b.validate_sidecar(self.manifest['parts'][pid]['path'],pid)
    canvas=Image.new('RGBA',(1254,1254));target=b.draw_part(canvas,raw,s,frame);a,c=[target[i] for i in s['mesh']['sharedAnkleSeam']]
    for t in (.2,.4,.6,.8):
     x,y=[round(a[j]+t*(c[j]-a[j])) for j in (0,1)]
     self.assertGreater(canvas.getpixel((x,y))[3],200)
 def test_missing_unknown_parts_no_output(self):
  for bad in ({}, {**self.manifest['parts'],'unknown':next(iter(self.manifest['parts'].values()))}):
   m=copy.deepcopy(self.manifest);m['parts']=bad;p=self.root/'bad.json';write_json(p,m);out=self.root/'forbidden'
   with self.assertRaisesRegex(b.Refusal,'missing or unknown'):b.bake(p,out)
   self.assertFalse(out.exists())
 def test_no_overwrite_preserves_existing(self):
  before=b.digest(self.root/'output/receipt.json')
  with self.assertRaisesRegex(b.Refusal,'never overwrite'):b.bake(self.mp,self.root/'output')
  self.assertEqual(before,b.digest(self.root/'output/receipt.json'))
 def test_source_and_sidecar_custody_fail(self):
  r=self.manifest['parts']['arm_left_upper']
  with self.assertRaisesRegex(b.Refusal,'sidecar custody'):b.validate_sidecar(r['path'],'arm_left_upper','0'*64)
  s=b.load(r['path']);s['raw']['sha256']='0'*64;p=self.root/'wrong-source.json';write_json(p,s)
  with self.assertRaisesRegex(b.Refusal,'raw byte custody'):b.validate_sidecar(p,'arm_left_upper')
  s=b.load(r['path']);s['raw']['rgbaSha256']='0'*64;write_json(p,s)
  with self.assertRaisesRegex(b.Refusal,'raw RGBA custody'):b.validate_sidecar(p,'arm_left_upper')
 def test_unknown_nonfinite_landmarks_calibration_and_seam_refused(self):
  pid='leg_left_lower_sandal';s=b.load(self.manifest['parts'][pid]['path']);p=self.root/'bad-sidecar.json'
  variants=[]
  q=copy.deepcopy(s);q['landmarks']['toe']['xy'][0]=float('nan');variants.append(q)
  q=copy.deepcopy(s);q['calibration']['scale']=float('inf');variants.append(q)
  q=copy.deepcopy(s);q['landmarks']['heel']['method']='inferred';variants.append(q)
  q=copy.deepcopy(s);q['mesh']['sharedAnkleSeam']=[0,1];variants.append(q)
  q=copy.deepcopy(s);q['mesh']['vertices'][2]['binding']['frame']='bone';variants.append(q)
  q=copy.deepcopy(s);q['calibration']['translation'][0]+=10;variants.append(q)
  for q in variants:
   write_json(p,q)
   with self.assertRaises(b.Refusal):b.validate_sidecar(p,pid)
 def test_mesh_source_coverage_winding_and_core_rest_fit(self):
  pid='leg_left_lower_sandal';original=b.load(self.manifest['parts'][pid]['path']);p=self.root/'invalid-mesh.json'
  q=copy.deepcopy(original);q['mesh']['triangles'][0]['indices'].reverse();write_json(p,q)
  with self.assertRaisesRegex(b.Refusal,'winding'):b.validate_sidecar(p,pid)
  q=copy.deepcopy(original);raw=self.root/'NON_ART-stray-pixel.png'
  with Image.open(q['raw']['path']) as image:
   image.putpixel((10,10),(1,2,3,1));image.save(raw);q['raw'].update(path=str(raw),sha256=b.digest(raw),rgbaSha256=hashlib.sha256(image.tobytes()).hexdigest())
  write_json(p,q)
  with self.assertRaisesRegex(b.Refusal,'source alpha outside'):b.validate_sidecar(p,pid)
  core=b.load(self.manifest['parts'][b.PARTS[0]]['path']);core['landmarks']['actor_left_shoulder_cap']['xy'][0]+=10;write_json(p,core)
  with self.assertRaisesRegex(b.Refusal,'core attachment'):b.validate_sidecar(p,b.PARTS[0])
 def test_atomic_publication_refuses_even_empty_existing_output(self):
  source=self.root/'NON_ART-stage';dest=self.root/'NON_ART-existing';source.mkdir();dest.mkdir();(source/'marker').write_text('keep')
  with self.assertRaisesRegex(b.Refusal,'atomic publication refused'):b.publish_no_replace(source,dest)
  self.assertTrue((source/'marker').exists());self.assertEqual(list(dest.iterdir()),[])
 def test_hidden_core_and_leg_hips_must_be_authored_hypotheses(self):
  for pid,name in [(b.PARTS[0],'actor_left_hip_under_hem'),('leg_left_upper','hip')]:
   s=b.load(self.manifest['parts'][pid]['path']);s['landmarks'][name]['method']='observed_original';p=self.root/'NON_ART-invalid-hip.json';write_json(p,s)
   with self.assertRaisesRegex(b.Refusal,'hidden hip must be an authored hypothesis'):b.validate_sidecar(p,pid)
 def test_duplicate_source_mesh_coordinates_rejected(self):
  pid='leg_left_lower_sandal';s=b.load(self.manifest['parts'][pid]['path']);s['mesh']['vertices'].append(copy.deepcopy(s['mesh']['vertices'][2]));p=self.root/'NON_ART-duplicate-vertex.json';write_json(p,s)
  with self.assertRaisesRegex(b.Refusal,'duplicate rawXY'):b.validate_sidecar(p,pid)
 def test_bone_length_change_refused(self):
  p=copy.deepcopy(self.plan);p['frames'][0]['points3D']['LEFT_knee'][2]+=5
  old=b.BASE/'tooling/rig_preflight.py';spec=b.importlib.util.spec_from_file_location('old',old);mod=b.importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
  with self.assertRaisesRegex(ValueError,'bone length'):mod.geometry(p)

def math_distance_2(a,c):return sum((a[i]-c[i])**2 for i in range(2))**.5
def math_distance(a,c):return sum((a[i]-c[i])**2 for i in range(3))**.5

class CompleteIdentityGateTests(unittest.TestCase):
 """Temporary NON_ART static numeric rasters, never an actual identity review."""
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(prefix='NON_ART_identity_gate_');self.root=pathlib.Path(self.tmp.name)
  camera={'projection':'dimetric','ratio':[2,1],'tile':[54,27],'elevation':26.565};frames={}
  for n,(view,(direction,world)) in enumerate(b.IDENTITY_VIEWS.items()):
   p=self.root/(view+'-NON_ART.png');im=Image.new('RGBA',(1254,1254),(n*20,1,2,255));im.save(p)
   frames[view]={'path':str(p),'sha256':b.digest(p),'rgbaSha256':hashlib.sha256(im.tobytes()).hexdigest(),'fullBodyInspected':True,'engineDirection':direction,'worldDirection':world,'status':'STATIC_IDENTITY_REFERENCE_CANDIDATE'}
  self.review={'schema':'villager-static-identity-review/v1','status':'PASS_STATIC_IDENTITY_LOCK_FOR_SOUTH_AUTHORING_ONLY','frames':copy.deepcopy(frames),'frameHashes':{v:f['sha256'] for v,f in frames.items()},'canvas':[1254,1254],'camera':camera,'sourcePivot':[654,1140],'wholeCanvasLogicalSize':38,'scope':{'southWalkKeyAuthoring':True,'otherAnimationDirections':False},'fixturePurpose':'NON_ART_TEMPORARY_NUMERIC_NOT_IDENTITY_QUALIFICATION'}
  self.review_path=self.root/'NON_ART-review.json';write_json(self.review_path,self.review)
  self.lock={'schema':'villager-eight-static-identity/v1','status':self.review['status'],'frames':frames,'canvas':[1254,1254],'camera':camera,'review':{'receiptPath':str(self.review_path),'receiptSha256':b.digest(self.review_path),'frameHashes':copy.deepcopy(self.review['frameHashes'])},'fixturePurpose':'NON_ART_TEMPORARY_NUMERIC_NOT_IDENTITY_QUALIFICATION'}
  self.lock_path=self.root/'NON_ART-lock.json';write_json(self.lock_path,self.lock)
 def tearDown(self):self.tmp.cleanup()
 def seal_fixture_records(self):
  write_json(self.review_path,self.review);self.lock['review']['receiptSha256']=b.digest(self.review_path);write_json(self.lock_path,self.lock)
 def test_all_eight_sources_checked_and_reader_preserves_bytes(self):
  before={p.name:b.digest(p) for p in self.root.iterdir()}
  self.assertEqual(set(b.validate_identity(self.lock_path,b.digest(self.lock_path))['frames']),set(b.IDENTITY_VIEWS))
  self.assertEqual(before,{p.name:b.digest(p) for p in self.root.iterdir()})
 def test_corrupted_non_south_source_rejected(self):
  p=pathlib.Path(self.lock['frames']['N']['path'])
  with Image.open(p) as im:im.putpixel((4,4),(3,4,5,255));im.save(p)
  with self.assertRaisesRegex(b.Refusal,'byte custody mismatch: N'):b.validate_identity(self.lock_path,b.digest(self.lock_path))
 def test_decoded_rgba_hash_rejected_even_with_byte_hash_correct(self):
  self.lock['frames']['NE']['rgbaSha256']='0'*64;self.review['frames']['NE']['rgbaSha256']='0'*64;self.seal_fixture_records()
  with self.assertRaisesRegex(b.Refusal,'decodedRGBA custody mismatch: NE'):b.validate_identity(self.lock_path,b.digest(self.lock_path))
 def test_missing_non_south_original_rejected(self):
  pathlib.Path(self.lock['frames']['W']['path']).unlink()
  with self.assertRaisesRegex(b.Refusal,'missing identity original: W'):b.validate_identity(self.lock_path,b.digest(self.lock_path))
 def test_review_digest_and_all_eight_binding_rejected(self):
  self.review_path.write_text(self.review_path.read_text()+' ')
  with self.assertRaisesRegex(b.Refusal,'parent review custody mismatch'):b.validate_identity(self.lock_path,b.digest(self.lock_path))
  del self.review['frameHashes']['NW'];self.seal_fixture_records()
  with self.assertRaisesRegex(b.Refusal,'parent review must bind all eight'):b.validate_identity(self.lock_path,b.digest(self.lock_path))
 def test_parent_review_rgba_and_camera_binding_rejected(self):
  self.review['frames']['E']['rgbaSha256']='0'*64;self.seal_fixture_records()
  with self.assertRaisesRegex(b.Refusal,'reviewed identity source differs'):b.validate_identity(self.lock_path,b.digest(self.lock_path))
  self.review['frames']['E']['rgbaSha256']=self.lock['frames']['E']['rgbaSha256'];self.review['sourcePivot']=[650,1140];self.seal_fixture_records()
  with self.assertRaisesRegex(b.Refusal,'camera/root mismatch'):b.validate_identity(self.lock_path,b.digest(self.lock_path))

if __name__=='__main__':unittest.main()
