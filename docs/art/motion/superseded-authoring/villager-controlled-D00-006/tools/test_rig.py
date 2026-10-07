import unittest,math,json,tempfile,pathlib
from rig import matrix,preflight
class DiagnosticTests(unittest.TestCase):
 def test_uniform_positive_transform_preserves_bone_length_and_anchor(self):
  a=[24,50];target=[650,1140];scale=.8;angle=.75;m=matrix(a,target,scale,angle)
  apply=lambda p:[m[0]*p[0]+m[2]*p[1]+m[4],m[1]*p[0]+m[3]*p[1]+m[5]]
  self.assertAlmostEqual(math.dist(apply(a),target),0);self.assertAlmostEqual(math.dist(apply(a),apply([24,100])),40);self.assertGreater(m[0]*m[3]-m[1]*m[2],0)
 def test_proposal_cannot_render_missing_original_art(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=pathlib.Path(tmp)/'rig.json';p.write_text(json.dumps({'canvas':[1254,1254],'root':[650,1140],'direction':'D00','scale':38/1254,'parts':{}}))
   with self.assertRaisesRegex(ValueError,'eleven original'):preflight(p)
if __name__=='__main__':unittest.main()

from support_tracks import solve_two_bone,contact_track
class TrackDiagnostics(unittest.TestCase):
 def test_ik_preserves_both_actual_lengths_and_refuses_unreachable(self):
  root=[0,0];target=[20,80];knee=solve_two_bone(root,target,50,45,1)
  self.assertAlmostEqual(math.dist(root,knee),50);self.assertAlmostEqual(math.dist(knee,target),45)
  with self.assertRaisesRegex(ValueError,'unreachable'):solve_two_bone(root,[0,100],50,45,1)
 def test_support_alternates_and_track_closes_without_local_stance_motion_error(self):
  self.assertTrue(contact_track(0,'near',100,10)['support']);self.assertTrue(contact_track(.5,'far',100,10)['support'])
  self.assertEqual(contact_track(0,'near',100,10),contact_track(1,'near',100,10))
  a=contact_track(.1,'near',100,10)['offset'];b=contact_track(.2,'near',100,10)['offset'];self.assertAlmostEqual(math.dist(a,b),10)
