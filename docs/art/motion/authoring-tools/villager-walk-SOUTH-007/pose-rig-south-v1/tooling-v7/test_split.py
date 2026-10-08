"""NON_ART numerical/schema/raster fixtures, not original art evidence."""
import copy,hashlib,json,pathlib,tempfile,unittest
from PIL import Image
import diagnose_split as d
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.b=d.p.engine();_,cls.plan=cls.b.locked_inputs()
 def q(self,pid):
  names,length,schema=(('elbow','wrist'),180,'south-right-forearm-proposal/v1') if pid==d.ARM else (('wrist','fingertip'),65,'south-right-hand-proposal/v1')
  points=[[500,100],[500,1000 if pid==d.ARM else 750]]
  landmarks={name:{'xy':point,'method':'authored_hidden_hypothesis' if i==0 else 'observed_original','uncertaintyPx':30,'evidence':'NON_ART attachment convention; not anatomy','anatomicalJointMeasured':False,'observableAnatomicalEvidence':None} for i,(name,point) in enumerate(zip(names,points))}
  return {'schema':schema,'partId':pid,'status':'UNSEALED_DIAGNOSTIC','purpose':'NON_ART_TEST_FIXTURE','raw':{},'endpoints':landmarks,'calibration':d.p.endpoint_similarity(*points,length),'sourceEvidence':{}}
 def orders(self):return {'schema':'south-four-part-orders-proposal/v1','layerOrderByPose':{k:list(d.PARTS) for k in d.LABELS},'evidenceByPose':{k:'NON_ART permutation only; not ordering approval' for k in d.LABELS}}
 def test_distinct_slot_schemas(self):
  for pid in (d.ARM,d.HAND):self.assertEqual(d.proposal(self.q(pid),pid,self.b)['partId'],pid)
  with self.assertRaises(ValueError):d.proposal(self.q(d.ARM),d.HAND,self.b)
 def test_held_combined_not_new_original(self):
  q=self.q(d.ARM);q['raw']={'sha256':next(iter(d.HELD_COMBINED))}
  with self.assertRaises(ValueError):d.load_source(q,self.b)
 def test_duplicate_raw_and_decoded_slots(self):
  for sources in [[{'sha256':'a','rgbaSha256':'x'},{'sha256':'a','rgbaSha256':'y'}],[{'sha256':'a','rgbaSha256':'x'},{'sha256':'b','rgbaSha256':'x'}]]:
   with self.assertRaises(ValueError):d.unique_sources(sources,self.b)
 def test_no_old_slot_alias(self):
  q=self.q(d.ARM);q['partId']='arm_right_lower_hand'
  with self.assertRaises(ValueError):d.proposal(q,d.ARM,self.b)
 def test_numeric_calibration(self):
  for pid,scale in [(d.ARM,.2),(d.HAND,.1)]:self.assertAlmostEqual(d.proposal(self.q(pid),pid,self.b)['calibration']['scale'],scale)
 def test_oblique_uniform_fit(self):
  q=self.q(d.HAND);q['endpoints']['wrist']['xy']=[100,200];q['endpoints']['fingertip']['xy']=[160,280];q['calibration']={'scale':.65,'rotationRad':.6435011087932843,'translation':[-.65*(.8*100-.6*200),-.65*(.6*100+.8*200)]};d.proposal(q,d.HAND,self.b)
 def test_anisotropic_and_mirror_refused(self):
  for edit in [{'scaleY':2},{'scale':-1}]:
   q=self.q(d.HAND);q['calibration'].update(edit)
   with self.assertRaises(ValueError):d.proposal(q,d.HAND,self.b)
 def test_endpoint_mismatch(self):
  q=self.q(d.HAND);q['endpoints']['fingertip']['xy'][1]+=1
  with self.assertRaises(ValueError):d.proposal(q,d.HAND,self.b)
 def test_hidden_not_measured_anatomy(self):
  q=self.q(d.ARM);q['endpoints']['elbow']['anatomicalJointMeasured']=True
  with self.assertRaises(ValueError):d.proposal(q,d.ARM,self.b)
 def test_fullcanvas_no_crop_override(self):
  q=self.q(d.HAND);s=d.proposal(q,d.HAND,self.b);self.assertEqual([v['rawXY'] for v in s['mesh']['vertices']],[[0,0],[1254,0],[1254,1254],[0,1254]]);self.b.validate_partition(s['mesh']['vertices'],s['mesh']['triangles']);q['crop']=[1,1,1253,1253]
  with self.assertRaises(ValueError):d.proposal(q,d.HAND,self.b)
 def test_explicit_order_allposes(self):
  d.validate_orders(self.orders(),self.b)
  for label in d.LABELS:
   q=self.orders();del q['layerOrderByPose'][label]
   with self.assertRaises(ValueError):d.validate_orders(q,self.b)
 def test_duplicate_order_slot(self):
  q=self.orders();q['layerOrderByPose']['F0']=[d.CORE,d.UP,d.ARM,d.ARM]
  with self.assertRaises(ValueError):d.validate_orders(q,self.b)
 def test_missing_input(self):
  with self.assertRaises(ValueError):d.proposal({},d.ARM,self.b)
 def test_no_overwrite(self):
  with self.assertRaises(ValueError):d.run('/missing','/missing','/missing',d.p.BASE/'tooling-v7')
 def test_wrist_attachment_and_fixed_facing_allposes(self):
  a=d.proposal(self.q(d.ARM),d.ARM,self.b);h=d.proposal(self.q(d.HAND),d.HAND,self.b)
  for f in [d.neutral(self.plan),*self.plan['frames']]:
   report=d.wrist_report(a,h,f,self.b);self.assertAlmostEqual(report['wristSeamResidualPx'],0);self.assertAlmostEqual(report['handTipScreen'][1]-report['handAttachmentScreen'][1],65);self.assertAlmostEqual(report['handTipScreen'][0],report['handAttachmentScreen'][0]);self.assertEqual(report['handTipWorld'][1],f['points3D']['RIGHT_wrist'][1])
 def test_forearm_exact_sealed_projection(self):
  s=d.proposal(self.q(d.ARM),d.ARM,self.b)
  for f in self.plan['frames']:
   for v in s['mesh']['vertices']:self.assertEqual(d.project(v,d.ARM,f,self.b),self.b.projected_vertex(v,d.ARM,f))
 def test_bounds_fail_before_raster(self):
  s=d.proposal(self.q(d.HAND),d.HAND,self.b);f=copy.deepcopy(self.plan['frames'][0]);f['points3D']['RIGHT_wrist'][0]=5000
  with self.assertRaises(ValueError):d.targets(s,f,self.b)
 def test_source_custody_and_rgba_fixture(self):
  with tempfile.TemporaryDirectory() as tmp:
   base=pathlib.Path(tmp);raw=base/'NON_ART.png';Image.new('RGBA',(1254,1254),(1,2,3,4)).save(raw);e=base/'NON_ART-evidence.json';e.write_text('{"NON_ART":true}');q=self.q(d.HAND);q['raw']={'path':str(raw),'sha256':d.p.sha(raw),'rgbaSha256':hashlib.sha256(Image.open(raw).tobytes()).hexdigest(),'width':1254,'height':1254};q['sourceEvidence']={k:{'path':str(e),'sha256':d.p.sha(e)} for k in ('callRecord','rawReview')};d.load_source(q,self.b);q['raw']['rgbaSha256']='0'*64
   with self.assertRaises(ValueError):d.load_source(q,self.b)
   q['raw']['sha256']='0'*64
   with self.assertRaises(ValueError):d.load_source(q,self.b)
 def test_full_non_art_pipeline_receipt(self):
  with tempfile.TemporaryDirectory() as tmp:
   base=pathlib.Path(tmp);e=base/'NON_ART-evidence.json';e.write_text('{"NON_ART":true}');paths=[]
   for i,pid in enumerate((d.ARM,d.HAND)):
    im=Image.new('RGBA',(1254,1254));im.putpixel((500,500),(40+i,70,90,255));im.putpixel((0,0),(120+i,30,10,60));raw=base/(pid+'-NON_ART.png');im.save(raw);q=self.q(pid);q['raw']={'path':str(raw),'sha256':d.p.sha(raw),'rgbaSha256':hashlib.sha256(im.tobytes()).hexdigest(),'width':1254,'height':1254};q['sourceEvidence']={k:{'path':str(e),'sha256':d.p.sha(e)} for k in ('callRecord','rawReview')};qp=base/(pid+'-NON_ART.json');qp.write_text(json.dumps(q));paths.append(qp)
   op=base/'NON_ART-orders.json';op.write_text(json.dumps(self.orders()));out=base/'NON_ART-output';r=d.run(*paths,op,out);self.assertEqual(r['missingOriginalParts'],7);self.assertEqual(set(r['geometryBoundsByPose']),set(d.LABELS));self.assertFalse(r['finishedKey']);self.assertFalse(r['sealedSidecarCreated']);self.assertEqual(r['sourcePurposeDeclarations'],['NON_ART_TEST_FIXTURE']*2);self.assertEqual(len(r['outputs']),18);self.assertTrue((out/'inspection.json').is_file())
   with self.assertRaises(ValueError):d.run(*paths,op,out)
 def test_raster_fringe_identical_sampling(self):
  raw=Image.new('RGBA',(1254,1254));raw.putpixel((0,0),(200,50,10,80));raw.putpixel((500,700),(80,90,100,255));s=d.proposal(self.q(d.ARM),d.ARM,self.b);f=self.plan['frames'][0];a=Image.new('RGBA',raw.size);z=a.copy();d.draw(a,raw,s,f,self.b);self.b.draw_part(z,raw,s,f);self.assertEqual(a.tobytes(),z.tobytes())
if __name__=='__main__':unittest.main()
