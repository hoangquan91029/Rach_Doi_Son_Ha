"""Finite NON_ART_TEST_ONLY packaging checks; no actual project art consumed."""
import copy,json,tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
import export as adapter
class Checks(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(prefix='NON_ART_TEST_ONLY-',dir=Path(__file__).parent);self.base=Path(self.tmp.name);self.job=self.fixture(256)
 def tearDown(self):self.tmp.cleanup()
 def fixture(self,size):
  frames=[]
  for i in range(8):
   p=self.base/f'NON_ART_TEST_ONLY-{size}-F{i}.png';im=Image.new('RGBA',(size,size));d=ImageDraw.Draw(im);d.rectangle((size//3+i,size//3,size*2//3,size*2//3+i),fill=(40+i*15,80,120,253));im.save(p)
   source={'path':str(p),'width':size,'height':size,'sha256':adapter.sha(p.read_bytes()),'rgbaSha256':adapter.sha(im.tobytes())};rp=self.base/f'selection-{size}-{i}.json';rp.write_text(json.dumps({'status':'NON_ART_TEST_ONLY','frameIndex':i,'sourceSha256':source['sha256'],'rgbaSha256':source['rgbaSha256']}))
   frames.append({'index':i,'phase':f'F{i}','source':source,'selectionStatus':'NON_ART_TEST_ONLY','selectionReceipt':{'path':str(rp),'sha256':adapter.sha(rp.read_bytes())},'durationMs':73+i,'events':[{'name':'TEST_ONLY','offsetMs':0}]})
  return dict(id='NON_ART_TEST_ONLY',family='NON_ART_TEST_ONLY',state='walk',sourceCanvas=[size,size],runtimeCell=[128,128],renderSize=[96,96],pivot=[size*.52,size*.91],camera=adapter.CAMERA,direction=1,wholeCanvasTransform='UNIFORM_LANCZOS_NO_CROP_SHIFT_FIT',contactShadow={'mode':'baked'},technicalFixture=True,sourceMethod='NON_ART_TEST_ONLY',columns=4,gutter=2,frames=frames)
 def save(self,job):p=self.base/'job.json';p.write_text(json.dumps(job));return p
 def reject(self,job,reason):
  output=self.base/'must-not-exist'
  with self.assertRaisesRegex((ValueError,OSError),reason):adapter.export(self.save(job),output)
  self.assertFalse(output.exists())
 def test_rejections(self):
  cases=[]
  j=copy.deepcopy(self.job);j['frames'][4]['selectionStatus']='HELD';cases.append((j,'Held'))
  j=copy.deepcopy(self.job);j['frames']=j['frames'][:2];cases.append((j,'eight'))
  j=copy.deepcopy(self.job);j['frames'][0]['source']['path']=str(self.base/'missing.png');cases.append((j,'missing'))
  j=copy.deepcopy(self.job);j['frames'][0]['source']['sha256']='0'*64;cases.append((j,'SHA256 mismatch'))
  j=copy.deepcopy(self.job);j['frames'][0]['source']['width']=1254;cases.append((j,'Inconsistent'))
  j=copy.deepcopy(self.job);j['runtimeCell']=[128,127];cases.append((j,'Unequal'))
  j=copy.deepcopy(self.job);j['frames'][0]['pivot']=[0,0];cases.append((j,'pivot'))
  j=copy.deepcopy(self.job);j['frames'][0]['trim']=[0,0,10,10];cases.append((j,'fitting'))
  j=copy.deepcopy(self.job);j['runtimeCell']=[0,0];cases.append((j,'dimensions'))
  j=copy.deepcopy(self.job);j['frames'][0]['selectionReceipt']['sha256']='0'*64;cases.append((j,'Custody'))
  for job,reason in cases:
   with self.subTest(reason=reason):self.reject(job,reason)
 def test_bad_alpha(self):
  p=self.base/'opaque.png';im=Image.new('RGBA',(256,256),(90,80,70,255));im.save(p);j=copy.deepcopy(self.job);j['frames'][0]['source'].update(path=str(p),sha256=adapter.sha(p.read_bytes()),rgbaSha256=adapter.sha(im.tobytes()));self.reject(j,'actual alpha-zero')
 def test_success_256_and_1254(self):
  for size in [256,1254]:
   with self.subTest(size=size):
    job=self.fixture(size);before={f['source']['path']:Path(f['source']['path']).read_bytes() for f in job['frames']};out=self.base/f'NON_ART_TEST_ONLY-output-{size}';r=adapter.export(self.save(job),out);self.assertEqual(r['status'],'NON_ART_TEST_ONLY');self.assertEqual(r['packagingValidation']['packaging'],'PASS');self.assertEqual(r['runtimePivot'],[66.56,116.48]);a=json.loads((out/'manifest.json').read_text())['assets'][0];atlas=Image.open(out/'atlas.png').convert('RGBA');self.assertEqual(atlas.size,(528,264));self.assertEqual(a['pivot'],{'x':size*.52,'y':size*.91,'space':'source'})
    for i,f in enumerate(a['frames']):
     self.assertEqual((f['x'],f['y'],f['width'],f['height']),(i%4*132+2,i//4*132+2,128,128));expected=Image.open(f['source']['path']).resize((128,128),Image.Resampling.LANCZOS);self.assertEqual(atlas.crop((f['x'],f['y'],f['x']+128,f['y']+128)).tobytes(),expected.tobytes());self.assertEqual(Path(f['source']['path']).read_bytes(),before[f['source']['path']])
    with self.assertRaisesRegex(ValueError,'existing'):adapter.export(self.save(job),out)
if __name__=='__main__':unittest.main(verbosity=2)
