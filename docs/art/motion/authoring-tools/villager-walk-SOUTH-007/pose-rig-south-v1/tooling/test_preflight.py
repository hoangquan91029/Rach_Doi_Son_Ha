"""NON_ART numerical fixtures only; no art/motion qualification."""
import copy,json,pathlib,tempfile,unittest
import rig_preflight as rig
class GateTests(unittest.TestCase):
 def setUp(self):self.plan=rig.load(rig.BASE.parent/'pose-guides/walk-south-keys-v2/coordinate-plan.json')
 def test_four_key_constant_bones_and_world_contact(self):self.assertEqual(set(rig.geometry(self.plan)),{0,2,4,6})
 def test_changed_bone_rejected(self):
  p=copy.deepcopy(self.plan);p['frames'][0]['points3D']['LEFT_knee'][2]+=10
  with self.assertRaisesRegex(ValueError,'bone length'):rig.geometry(p)
 def test_world_slide_rejected(self):
  p=copy.deepcopy(self.plan);p['frames'][1]['soles']['LEFT']['worldHeel'][1]+=1
  with self.assertRaisesRegex(ValueError,'world support slides'):rig.geometry(p)
 def test_missing_art_no_outputs_or_source_changes(self):
  with tempfile.TemporaryDirectory(prefix='NON_ART_') as t:
   p=pathlib.Path(t);m=p/'NON_ART-empty.json';m.write_text('{"parts":{}}');before=rig.sha(m)
   with self.assertRaisesRegex(ValueError,'missing real parts'):rig.preflight(m,p/'output')
   self.assertEqual(rig.sha(m),before);self.assertFalse((p/'output').exists())
 def test_no_overwrite(self):
  with tempfile.TemporaryDirectory(prefix='NON_ART_') as t:
   p=pathlib.Path(t);out=p/'output';out.mkdir();marker=out/'NON_ART.txt';marker.write_text('preserve')
   with self.assertRaisesRegex(ValueError,'refuse overwrite'):rig.preflight(p/'absent.json',out)
   self.assertEqual(marker.read_text(),'preserve')
 def test_sidecar_custody_rejected_before_raw_decode(self):
  c=rig.load(rig.BASE/'part-contract-v2.json')
  with tempfile.TemporaryDirectory(prefix='NON_ART_') as t:
   p=pathlib.Path(t)/'NON_ART-sidecar.json';p.write_text('{}');before=rig.sha(p)
   m={'parts':{x['id']:{'sidecarPath':str(p),'sidecarSha256':'0'*64} for x in c['parts']}}
   with self.assertRaisesRegex(ValueError,'sidecar custody'):rig.inputs(c,m)
   self.assertEqual(rig.sha(p),before)
 def test_foot_plane_is_independent_of_shin_camera_axis(self):
  matrices=rig.geometry(self.plan)
  self.assertNotEqual(matrices[0]['LEFT_shin'][:4],matrices[2]['LEFT_shin'][:4])
  # Planted endpoints differ locally by root travel; their world endpoints tested above.
  self.assertEqual(matrices[0]['LEFT_foot']['toe'][0],matrices[2]['LEFT_foot']['toe'][0])
  self.assertAlmostEqual(matrices[0]['LEFT_foot']['toe'][1]-matrices[2]['LEFT_foot']['toe'][1],80)
if __name__=='__main__':unittest.main()
