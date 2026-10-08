"""NON_ART_TEST_FIXTURE: numerical/schema checks, never source or art evidence."""
import copy,unittest,tempfile,pathlib
import diagnose_lower as d
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.b=d.p.engine()
 def q(self):
  endpoints={n:{'xy':xy,'method':'observed_original','uncertaintyPx':20,'evidence':'NON_ART synthetic numerical fixture'} for n,xy in [('elbow',[10,20]),('wrist',[70,100])]}
  return {'schema':'south-lower-diagnostic-proposal/v1','status':'UNSEALED_DIAGNOSTIC','purpose':'NON_ART_TEST_FIXTURE','raw':{},'ownershipClarification':{},'endpoints':endpoints,'calibration':d.p.endpoint_similarity([10,20],[70,100],180),'layerOrderProposal':[d.LOW,d.UP,d.CORE]}
 def test_diagonal_uniform_directed_no_mirror(self):
  s,_=d.proposal(self.q(),self.b);self.assertAlmostEqual(s['calibration']['scale'],1.8)
  self.assertTrue(self.b.same(self.b.calibration_xy(s['calibration'],[70,100]),[0,180],1e-6))
  self.assertAlmostEqual(s['calibration']['rotationRad'],0.6435011087932843)
 def test_fullcanvas_fringe_coverage(self):
  s,_=d.proposal(self.q(),self.b);self.assertEqual([v['rawXY'] for v in s['mesh']['vertices']],[[0,0],[1254,0],[1254,1254],[0,1254]])
  self.b.validate_partition(s['mesh']['vertices'],s['mesh']['triangles'])
 def test_duplicate_source_slot(self):
  with self.assertRaises(ValueError):d.verify_unique_sources(['a','a','b'],self.b)
 def test_custody_mismatch(self):
  with tempfile.TemporaryDirectory() as t:
   f=pathlib.Path(t)/'NON_ART';f.write_bytes(b'fixture')
   with self.assertRaises(ValueError):d.verify_bytes(f,'0'*64,self.b)
 def test_anisotropic_forbidden(self):
  q=self.q();q['calibration']['scaleY']=2
  with self.assertRaises(ValueError):d.proposal(q,self.b)
 def test_endpoint_mismatch(self):
  q=self.q();q['endpoints']['wrist']['xy']=[71,100]
  with self.assertRaises(ValueError):d.proposal(q,self.b)
 def test_unsealed_only(self):
  q=self.q();q['status']='SEALED_ORIGINAL_CALIBRATION'
  with self.assertRaises(ValueError):d.proposal(q,self.b)
 def test_existing_output_refused_before_source_read(self):
  with self.assertRaises(ValueError):d.run('/NON_ART_missing_proposal',d.p.BASE/'tooling-v6')
if __name__=='__main__':unittest.main()
