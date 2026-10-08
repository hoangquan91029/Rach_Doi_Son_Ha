"""Finite NON_ART_TEST_ONLY action packaging checks; temporary outputs deleted."""
import sys,importlib.util,json,copy,tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
sys.dont_write_bytecode=True
O=Path(__file__).parent;s=importlib.util.spec_from_file_location('v3',O/'export-v4.py');a=importlib.util.module_from_spec(s);s.loader.exec_module(a)
class Action(unittest.TestCase):
 def test_shapes_and_rejections(self):
  with tempfile.TemporaryDirectory(prefix='NON_ART_TEST_ONLY-',dir='/tmp') as tmp:
   b=Path(tmp);frames=[]
   for i in range(3):
    p=b/f'F{i}.png';im=Image.new('RGBA',(256,256));ImageDraw.Draw(im).rectangle((70+i,70,180,180),fill=(80+i,110,90,253));im.save(p);source={'path':str(p),'width':256,'height':256,'sha256':a.sha(p.read_bytes()),'rgbaSha256':a.sha(im.tobytes())};r=b/f'R{i}.json';r.write_text(json.dumps({'status':'NON_ART_TEST_ONLY','frameIndex':i,'sourceSha256':source['sha256'],'rgbaSha256':source['rgbaSha256']}));frames.append({'index':i,'phase':f'F{i}','source':source,'selectionStatus':'NON_ART_TEST_ONLY','selectionReceipt':{'path':str(r),'sha256':a.sha(r.read_bytes())},'durationMs':75,'events':[]})
   job=dict(id='NON_ART_TEST_ONLY',family='NON_ART_TEST_ONLY',state='carry_wood',loop=True,locomotion={'distancePerCycle':1.26},technicalFixture=True,sourceMethod='NON_ART_TEST_ONLY',sourceCanvas=[256,256],runtimeCell=[128,128],renderSize=[89,89],pivot=[128,230],camera=a.CAMERA,direction=1,wholeCanvasTransform='UNIFORM_LANCZOS_NO_CROP_SHIFT_FIT',contactShadow={'mode':'baked'},frames=frames)
   def run(j,name):p=b/(name+'.json');p.write_text(json.dumps(j));return a.export(p,b/name)
   r=run(job,'carry');self.assertEqual(r['packagingValidation']['packaging'],'PASS');self.assertEqual(json.loads((b/'carry/manifest.json').read_text())['assets'][0]['locomotion'],{'distancePerCycle':1.26})
   for i,(state,distance) in enumerate([('carry_wood',0),('carry',-1),('walk',True),('gather_wood',1.26),('attack',1.26)]):
    j=copy.deepcopy(job);j.update(state=state,locomotion={'distancePerCycle':distance})
    with self.assertRaises(ValueError):run(j,f'bad{i}')
   j=copy.deepcopy(job);j.update(state='gather_wood');j.pop('locomotion');run(j,'generic-gather');self.assertNotIn('locomotion',json.loads((b/'generic-gather/manifest.json').read_text())['assets'][0])
if __name__=='__main__':unittest.main(verbosity=2)
