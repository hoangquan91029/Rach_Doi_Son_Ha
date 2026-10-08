"""Finite NON_ART_TEST_ONLY action packaging checks; temporary outputs deleted."""
import sys,importlib.util,json,copy,tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
sys.dont_write_bytecode=True
O=Path(__file__).parent;s=importlib.util.spec_from_file_location('v3',O/'export-v3.py');a=importlib.util.module_from_spec(s);s.loader.exec_module(a)
class Action(unittest.TestCase):
 def test_shapes_and_rejections(self):
  with tempfile.TemporaryDirectory(prefix='NON_ART_TEST_ONLY-',dir='/tmp') as tmp:
   b=Path(tmp);frames=[]
   for i in range(3):
    p=b/f'F{i}.png';im=Image.new('RGBA',(256,256));ImageDraw.Draw(im).rectangle((70+i,70,180,180),fill=(80+i,110,90,253));im.save(p);source={'path':str(p),'width':256,'height':256,'sha256':a.sha(p.read_bytes()),'rgbaSha256':a.sha(im.tobytes())};r=b/f'R{i}.json';r.write_text(json.dumps({'status':'NON_ART_TEST_ONLY','frameIndex':i,'sourceSha256':source['sha256'],'rgbaSha256':source['rgbaSha256']}));frames.append({'index':i,'phase':f'F{i}','source':source,'selectionStatus':'NON_ART_TEST_ONLY','selectionReceipt':{'path':str(r),'sha256':a.sha(r.read_bytes())},'durationMs':75,'events':[]})
   job=dict(id='NON_ART_TEST_ONLY',family='NON_ART_TEST_ONLY',state='death',loop=False,technicalFixture=True,sourceMethod='NON_ART_TEST_ONLY',sourceCanvas=[256,256],runtimeCell=[128,128],renderSize=[89,89],pivot=[128,230],camera=a.CAMERA,direction=1,wholeCanvasTransform='UNIFORM_LANCZOS_NO_CROP_SHIFT_FIT',contactShadow={'mode':'baked'},frames=frames)
   def run(j,name):p=b/(name+'.json');p.write_text(json.dumps(j));return a.export(p,b/name)
   r=run(job,'three');self.assertEqual(r['frames'],3);self.assertEqual(r['packagingValidation']['packaging'],'PASS');self.assertFalse(json.loads((b/'three/preview.json').read_text())['loop'])
   idle=copy.deepcopy(job);idle.update(state='idle',loop=True,frames=frames[:1]);run(idle,'idle');self.assertEqual(json.loads((b/'idle/manifest.json').read_text())['assets'][0]['runtime']['derivation']['method'],'resize')
   changes=[lambda j:j.update(loop='false'),lambda j:j.update(loop=True),lambda j:j['frames'][0]['source'].update(sha256='0'*64),lambda j:j['frames'][0].update(pivot=[0,0]),lambda j:j.update(runtimeCell=[128,127]),lambda j:j['frames'][0].update(events=[{'name':'bad','offsetMs':100}]),lambda j:j['frames'][0].update(selectionStatus='HELD')]
   for i,change in enumerate(changes):
    j=copy.deepcopy(job);change(j)
    with self.assertRaises((ValueError,KeyError)):run(j,f'bad{i}')
if __name__=='__main__':unittest.main(verbosity=2)
