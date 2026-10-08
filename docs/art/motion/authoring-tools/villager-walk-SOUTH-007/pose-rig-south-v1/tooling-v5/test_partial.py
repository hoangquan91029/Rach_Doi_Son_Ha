"""Temporary NON_ART textures only. No artist-output or motion qualification."""
import copy,hashlib,json,math,pathlib,tempfile,unittest
from PIL import Image,ImageDraw
import inspect_partial as p
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.tmp=tempfile.TemporaryDirectory(prefix='NON_ART_partial_');c.root=pathlib.Path(c.tmp.name);c.b=p.engine();_,c.plan=c.b.locked_inputs()
  im=Image.new('RGBA',(1254,1254));ImageDraw.Draw(im).rectangle((488,300,512,500),fill=(40,80,220,255));raw=c.root/'NON_ART.png';im.save(raw)
  lm=lambda xy:{'xy':xy,'method':'observed_original','uncertaintyPx':1,'evidence':'NON_ART temporary numeric texture only'}
  c.s={'schema':'south-bitmap-rig-sidecar/v3','partId':'arm_right_upper','status':'SEALED_ORIGINAL_CALIBRATION','raw':{'path':str(raw),'sha256':p.sha(raw),'rgbaSha256':hashlib.sha256(im.tobytes()).hexdigest(),'width':1254,'height':1254},'calibration':{'scale':1,'rotationRad':0,'translation':[-500,-300],'tolerancePx':.01},'landmarks':{'shoulder':lm([500,300]),'elbow':lm([500,500])},'mesh':{'vertices':[{'rawXY':[500+x,300+y],'binding':{'frame':'bone','local':[x,y]}} for x,y in [(-12,0),(12,0),(12,200),(-12,200)]],'triangles':[{'indices':[0,1,2],'region':'bone'},{'indices':[0,2,3],'region':'bone'}],'sharedAnkleSeam':[]}}
  c.side=c.root/'NON_ART.json';c.side.write_text(json.dumps(c.s));c.rawhash=p.sha(raw);c.planhash=p.sha(p.BASE/'../pose-guides/walk-south-keys-v3/coordinate-plan.json')
  c.out=c.root/'partial';c.r=p.inspect('arm_right_upper',c.side,c.out,['arm_right_upper','core_head_torso_pelvis'],'NON_ART_TEMPORARY_FIXTURE')
 @classmethod
 def tearDownClass(c):c.tmp.cleanup()
 def test_output_custody_and_source_preservation(self):
  self.assertFalse(self.r['finishedKey']);self.assertIn('NON_ART',self.r['status'])
  for o in self.r['outputs']:
   f=self.out/o['path'];self.assertEqual(p.sha(f),o['sha256'])
   with Image.open(f) as im:self.assertEqual(im.mode,'RGBA');self.assertEqual(hashlib.sha256(im.tobytes()).hexdigest(),o['rgbaSha256']);self.assertEqual(im.size,(o['width'],o['height']))
  self.assertEqual(p.sha(self.s['raw']['path']),self.rawhash);self.assertEqual(p.sha(p.BASE/'../pose-guides/walk-south-keys-v3/coordinate-plan.json'),self.planhash)
 def test_camera_once_and_constant_all_four_bones(self):
  r=self.r['jointAndCameraReport'];self.assertEqual(r['unforeshortenedBonePlaneLength'],200);self.assertAlmostEqual(r['neutralBodyRestScreenLength'],173.328261,places=3)
  for f in r['allFourJointRecords']:self.assertAlmostEqual(f['modelLength'],200,places=7)
 def test_directed_uniform_fit(self):
  fit=p.endpoint_similarity([600,300],[600,1100],200);self.assertEqual(fit['scale'],.25)
  for xy,target in [([600,300],[0,0]),([600,1100],[0,200])]:self.assertLess(math.dist(self.b.calibration_xy(fit,xy),target),1e-8)
  for a,c in [([0,0],[0,0]),([float('nan'),0],[0,1])]:
   with self.assertRaises(ValueError):p.endpoint_similarity(a,c,200)
 def test_missing_unknown_order_and_nooverwrite(self):
  before=p.sha(self.out/'inspection.json')
  with self.assertRaises(ValueError):p.inspect('arm_right_upper',self.side,self.out,['arm_right_upper','core_head_torso_pelvis'],'NON_ART_TEMPORARY_FIXTURE')
  self.assertEqual(before,p.sha(self.out/'inspection.json'))
  for pid,side,order in [('unknown',self.side,['unknown','core_head_torso_pelvis']),('arm_right_upper',self.root/'missing.json',['arm_right_upper','core_head_torso_pelvis']),('arm_right_upper',self.side,[])]:
   out=self.root/'refused'
   with self.assertRaises((ValueError,OSError)):p.inspect(pid,side,out,order,'NON_ART_TEMPORARY_FIXTURE')
   self.assertFalse(out.exists())
 def test_custody_projection_and_alpha_refusals(self):
  variants=[]
  q=copy.deepcopy(self.s);q['raw']['sha256']='0'*64;variants.append(q)
  q=copy.deepcopy(self.s);q['raw']['rgbaSha256']='0'*64;variants.append(q)
  q=copy.deepcopy(self.s);q['calibration']['scale']=173.33/200;variants.append(q)
  q=copy.deepcopy(self.s);q['mesh']['vertices'][0]['rawXY']=[499,300];variants.append(q)
  for q in variants:
   f=self.root/'bad.json';f.write_text(json.dumps(q));out=self.root/'bad-output'
   with self.assertRaises(ValueError):p.inspect('arm_right_upper',f,out,['arm_right_upper','core_head_torso_pelvis'],'NON_ART_TEMPORARY_FIXTURE')
   self.assertFalse(out.exists())
if __name__=='__main__':unittest.main()
