"""Focused real-source packaging/custody tests. No synthetic or visual acceptance."""
import copy,importlib.util,json,sys,unittest,subprocess,os
from pathlib import Path
from PIL import Image
sys.dont_write_bytecode=True
ROOT=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');OUT=ROOT/'docs/qa/whole-building-exporter-358';STAGE=Path(os.environ.get('BUILDING358_TEST_STAGE','/tmp/rds-building-export358-stage/final-suite'));STAGE.mkdir(parents=True,exist_ok=True)
spec=importlib.util.spec_from_file_location('exporter',OUT/'export-whole2d-building-atlas.py');adapter=importlib.util.module_from_spec(spec);spec.loader.exec_module(adapter)
def pin(p):return {'path':str(p),'sha256':adapter.sha(p.read_bytes())}
def job321():
 j=json.loads((ROOT/'docs/art/buildings/wall-collapse-preview-321/selected-job.json').read_text());j['expectedFrameCount']=4;return j

def job356():
 a=ROOT/'docs/art/buildings/mixed-gate-idle-356';candidate=json.loads((a/'candidate.json').read_text());source=dict(candidate['source'],path=str(a/'raw.png'))
 return dict(id='gate-whole-356-X-mask5-packaging358',family='building.gate',kind='building',state='idle',direction=None,fortification={'mask':5,'axis':'X'},loop=True,sourceCanvas=[1254,1254],runtimeCell=[128,128],pivot=[627,900],renderSize=[42.3225,42.3225],sourceMethod='FINISHED_WHOLE_2D_FRAMES',wholeCanvasTransform='UNIFORM_LANCZOS_NO_CROP_SHIFT_FIT',expectedFrameCount=1,frames=[dict(index=0,phase='F0',selectionStatus='SELECTED_FRAME_CANDIDATE',durationMs=1000,source=source,originalRaw=pin(a/'raw.png'),toolReceipt=pin(a/'tool-result.json'),selectionReceipt=pin(a/'root-intake.json'),provenance=[pin(a/'work-order.json'),pin(a/'receipt.json')])])
def job245():
 a=ROOT/'docs/art/buildings/gate-x-idle-245';candidate=json.loads((a/'candidate.json').read_text());j=job356();j['id']='gate-whole-245-X-mask3-packaging358';j['fortification']={'mask':3,'axis':'X'};source=dict(candidate['source'],path=str(a/'raw.png'));j['frames'][0].update(source=source,originalRaw=pin(a/'raw.png'),toolReceipt=pin(a/'tool-result.json'),selectionReceipt=pin(a/'root-intake.json'),provenance=[pin(a/'receipt.json'),pin(a/'candidate.json')]);return j
class RealPackaging(unittest.TestCase):
 def write(self,j,name):
  p=STAGE/(name+'.json');p.write_text(json.dumps(j,indent=2)+'\n');return p
 def test_real321_exactatlas_pixels_durations_terminal(self):
  j=job321();out=STAGE/'real321';ledger=adapter.export(self.write(j,'job321'),out,ROOT);a=json.loads((out/'manifest.json').read_text())['assets'][0]
  actual=Image.open(out/'atlas.png').convert('RGBA');original=Image.open(ROOT/'docs/art/buildings/wall-collapse-preview-321/export/atlas.png').convert('RGBA');self.assertEqual(actual.tobytes(),original.tobytes());self.assertEqual(actual.size,(512,128));self.assertEqual(ledger['timingMs'],[120,150,180,1000]);self.assertEqual(ledger['terminal']['frame'],3);self.assertIs(a['loop'],False)
  for i,f in enumerate(a['frames']):
   source=Image.open(f['source']['path']).convert('RGBA');self.assertEqual(actual.crop((i*128,0,(i+1)*128,128)).tobytes(),source.resize((128,128),Image.Resampling.LANCZOS).tobytes());self.assertEqual(adapter.sha(Path(f['source']['path']).read_bytes()),j['frames'][i]['source']['sha256'])
  (OUT/'actual321-pixel-result.json').write_text(json.dumps({'status':'PASS_REAL4FRAME_WHOLEPIXEL_PARITY','decodedAtlasSHA256':adapter.sha(actual.tobytes()),'originalAtlasSHA256':adapter.sha(original.tobytes()),'encodedNewAtlasSHA256':adapter.sha((out/'atlas.png').read_bytes()),'cellWholePixelParity':[True]*4,'durationsMs':ledger['timingMs'],'terminalFrame':3,'validators':ledger['validators']},indent=2)+'\n')
 def test_real245_selected_static_wholepixel_parity(self):
  j=job245();out=STAGE/'real245';ledger=adapter.export(self.write(j,'job245'),out,ROOT);a=json.loads((out/'manifest.json').read_text())['assets'][0];actual=Image.open(out/'atlas.png').convert('RGBA');original=Image.open(ROOT/'docs/art/buildings/gate-x-idle-245/runtime.png').convert('RGBA');self.assertEqual(actual.tobytes(),original.tobytes());self.assertEqual(a['frames'][0]['durationMs'],1000);self.assertIs(a['loop'],True);self.assertEqual(a['fortification'],{'mask':3,'axis':'X'})
  for rec in ledger['copiedCustody'][0]['provenance']:self.assertEqual(adapter.sha(Path(rec['path']).read_bytes()),rec['sha256'])
  (OUT/'actual245-packaging-result.json').write_text(json.dumps({'status':'PASS_REAL_SELECTED_SINGLE_IDLE_WHOLEPIXEL_PARITY','sourceSHA256':j['frames'][0]['source']['sha256'],'runtimeDecodedSHA256':adapter.sha(actual.tobytes()),'existingRuntimeDecodedSHA256':adapter.sha(original.tobytes()),'wholeRuntimePixelParity':True,'durationMs':1000,'loop':True,'validators':ledger['validators'],'visualApprovalGranted':False},indent=2)+'\n')
 def test_real356_static_candidate_fails_closed_runtime_margin(self):
  j=job356();out=STAGE/'real356';source=Image.open(j['frames'][0]['source']['path']).convert('RGBA');expected=source.resize((128,128),Image.Resampling.LANCZOS);existing=Image.open(ROOT/'docs/art/buildings/mixed-gate-idle-356/runtime.png').convert('RGBA');self.assertEqual(expected.tobytes(),existing.tobytes())
  with self.assertRaisesRegex(ValueError,'runtime: clipped/opaque cutout or nontransparent canvas edge'):adapter.export(self.write(j,'job356'),out,ROOT)
  self.assertFalse(out.exists())
  (OUT/'actual356-packaging-result.json').write_text(json.dumps({'status':'HOLD_REAL_SELECTED_STATIC_RUNTIME_MARGIN','sourceSHA256':j['frames'][0]['source']['sha256'],'whole128PixelParityWithExisting356':True,'runtimeDecodedSHA256':adapter.sha(expected.tobytes()),'reason':'Existing authoritative runtime margin rejects edge alpha111/165. No crop/fit/shift or contract relaxation.','destinationCreated':False,'visualAcceptance':False,'runtimeInstalled':False},indent=2)+'\n')
 def test_custody_fails_closed_without_destination(self):
  mutations={'bad-source-hash':lambda j:j['frames'][0]['source'].update(sha256='0'*64),'held-frame':lambda j:j['frames'][0].update(selectionStatus='HOLD'),'perframe-shift':lambda j:j['frames'][0].update(offset=[0,0]),'missing-loop':lambda j:j.pop('loop'),'disallowed-kind':lambda j:j.update(kind='unit'),'missing-phase':lambda j:j['frames'].pop(),'duplicate-phase':lambda j:j['frames'][1].update(index=0,phase='F0'),'duplicate-whole':lambda j:j['frames'][1].update(source=copy.deepcopy(j['frames'][0]['source'])),'death-loop':lambda j:j.update(loop=True)}
  held=STAGE/'held-receipt.json';receipt=json.loads((ROOT/'docs/art/buildings/wall-collapse-key-312/root-selection.json').read_text());receipt['status']='HOLD';held.write_text(json.dumps(receipt));mutations['held-pinned-selection']=lambda j:j['frames'][0].update(selectionReceipt=pin(held))
  results=[]
  for name,mutate in mutations.items():
   j=job321();mutate(j);dest=STAGE/('reject-'+name)
   with self.subTest(name=name):
    with self.assertRaises(ValueError):adapter.export(self.write(j,'bad-'+name),dest,ROOT)
    self.assertFalse(dest.exists());results.append(name)
  j=job321();j['fortification']['axis']='X';dest=STAGE/'reject-invalidfortification'
  with self.assertRaises(subprocess.CalledProcessError):adapter.export(self.write(j,'bad-fortification'),dest,ROOT)
  self.assertFalse(dest.exists());results.append('authoritative-invalid-fortification')
  (OUT/'rejection-results.json').write_text(json.dumps({'status':'PASS_FAIL_CLOSED','rejected':results,'destinationCreated':False},indent=2)+'\n')
if __name__=='__main__':unittest.main()
