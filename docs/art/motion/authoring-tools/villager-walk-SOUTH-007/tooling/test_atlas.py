"""NON_ART numeric PNG fixtures only. Tests do not qualify identity, anatomy or motion."""
import unittest,json,pathlib,tempfile,hashlib
from PIL import Image,ImageDraw
from atlas import frame_at,DURATIONS,preflight,compile_atlas,sha

def fixture(directory):
 job={'technicalFixture':True,'direction':{'name':'SOUTH','screen':'down','engine':'D01','world':'SE'},'canvas':[1254,1254],'worldScale':38/1254,'groundPivot':[654,1140],'pivotStatus':'SEALED_FROM_SOUTH_REFERENCE','sourceMethod':'CONTROLLED_FINISHED_ILLUSTRATED_FRAMES','qaStrideWorldTiles':None}
 identity={};frames=[]
 for index,label in enumerate(['N','NE','E','SE','S','SW','W','NW']):
  image=Image.new('RGBA',(1254,1254),(20+index*20,40,70,255));ImageDraw.Draw(image).text((100,100),'NON_ART NUMERIC STATIC FIXTURE '+label,fill='white');path=directory/f'static-{label}.png';image.save(path);identity[label]={'path':path.name,'sha256':sha(path.read_bytes()),'fullBodyInspected':True}
 for index in range(8):
  image=Image.new('RGBA',(1254,1254),(index*25,70,90,255));ImageDraw.Draw(image).text((100,100),'NON_ART NUMERIC FRAME '+str(index),fill='white');path=directory/f'F{index}.png';image.save(path);frames.append({'index':index,'path':path.name,'originalSha256':sha(path.read_bytes()),'custodyReceipt':'NON_ART_FIXTURE_ONLY','support':'LEFT' if index<4 else 'RIGHT','swing':'RIGHT' if index<4 else 'LEFT','durationMs':DURATIONS[index]})
 receipt=directory/'NON_ART-test-receipt.json';receipt.write_text(json.dumps({'status':'NON_ART_NO_VISUAL_APPROVAL'}));review={'reviewer':'NON_ART_TECHNICAL_TEST_NOT_A_VISUAL_REVIEW','receiptPath':receipt.name,'receiptSha256':sha(receipt.read_bytes())}
 job['identityTurnaround']={'canvas':[1254,1254],'camera':{'projection':'dimetric','ratio':[2,1],'tile':[54,27],'elevation':26.565},'frames':identity,'review':{**review,'frameHashes':{k:v['sha256'] for k,v in identity.items()}}}
 job['southReference']={**identity['S'],'viewReviewReceipt':receipt.name};job['keyPoseReview']={**review,'supportGatePass':True,'frameHashes':{str(i):frames[i]['originalSha256'] for i in [0,2,4,6]}};job['frames']=frames
 path=directory/'job.json';path.write_text(json.dumps(job));return path,job

class Tests(unittest.TestCase):
 def test_variable_clock_boundaries_and_loop_are_exact(self):
  self.assertEqual(sum(DURATIONS),600)
  self.assertEqual([frame_at(DURATIONS,t) for t in [0,79,80,149,150,229,230,299,300,599,600,680]],[0,0,1,1,2,2,3,3,4,7,0,1])
 def test_d00_alias_refused_before_loading_art(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=pathlib.Path(tmp)/'job.json';p.write_text(json.dumps({'direction':{'name':'SOUTH','engine':'D00'}}))
   with self.assertRaisesRegex(ValueError,'D00 is not South'):preflight(p)
 def test_missing_static_identity_gate_refuses_animation(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=pathlib.Path(tmp)/'job.json';p.write_text(json.dumps({'direction':{'name':'SOUTH','screen':'down','engine':'D01','world':'SE'},'canvas':[1254,1254],'worldScale':38/1254}))
   with self.assertRaisesRegex(ValueError,'eight-direction static identity lock'):preflight(p)
 def test_numeric_fixture_preserves_sources_and_fixed_cells_custody(self):
  with tempfile.TemporaryDirectory() as tmp:
   directory=pathlib.Path(tmp);path,job=fixture(directory);before={p.name:p.read_bytes() for p in directory.glob('*.png')};out=directory/'compiled';compile_atlas(path,out)
   self.assertEqual(before,{p.name:p.read_bytes() for p in directory.glob('*.png')})
   metadata=json.loads((out/'animation.json').read_text());self.assertEqual(metadata['status'],'NON_ART_TECHNICAL_FIXTURE');self.assertFalse(metadata['runtimeIntegrated']);self.assertEqual(metadata['cycleDurationMs'],600)
   with Image.open(out/'villager-walk-SOUTH.png') as atlas:
    self.assertEqual(atlas.size,(1024,512))
    for index,frame in enumerate(metadata['frames']):
     self.assertEqual((frame['x'],frame['y'],frame['width'],frame['height']),(index%4*256,index//4*256,256,256))
     self.assertEqual(atlas.getpixel((frame['x']+128,frame['y']+128)),(index*25,70,90,255));self.assertEqual(frame['pivot'],{'x':654,'y':1140,'space':'source'})
     self.assertEqual(frame['source']['sha256'],job['frames'][index]['originalSha256'])
   self.assertEqual(metadata['frames'][0]['events'],[{'name':'FOOT_CONTACT_LEFT','offsetMs':0}]);self.assertEqual(metadata['frames'][4]['events'],[{'name':'FOOT_CONTACT_RIGHT','offsetMs':0}])
   with self.assertRaisesRegex(ValueError,'must not be overwritten'):compile_atlas(path,out)
 def test_tampered_original_and_identity_binding_are_refused(self):
  with tempfile.TemporaryDirectory() as tmp:
   directory=pathlib.Path(tmp);path,job=fixture(directory);(directory/'F3.png').write_bytes((directory/'F2.png').read_bytes())
   with self.assertRaisesRegex(ValueError,'Original byte custody mismatch'):preflight(path)
   job['identityTurnaround']['review']['frameHashes']['N']='0'*64;path.write_text(json.dumps(job))
   with self.assertRaisesRegex(ValueError,'Identity review must bind'):preflight(path)
 def test_invalid_grid_stride_does_not_write_outputs(self):
  with tempfile.TemporaryDirectory() as tmp:
   directory=pathlib.Path(tmp);path,job=fixture(directory);job['qaStrideWorldTiles']=float('nan');path.write_text(json.dumps(job));out=directory/'output'
   with self.assertRaisesRegex(ValueError,'Grid travel requires'):compile_atlas(path,out)
   self.assertFalse(out.exists())
if __name__=='__main__':unittest.main()
