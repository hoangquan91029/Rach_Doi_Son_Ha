"""Synthetic temporary fixtures validate packing only; never production artwork."""
import copy, importlib.util, json, subprocess, tempfile, unittest
from pathlib import Path
from PIL import Image, ImageDraw
spec=importlib.util.spec_from_file_location('adapter',Path(__file__).with_name('export.py')); adapter=importlib.util.module_from_spec(spec);spec.loader.exec_module(adapter)
class Contracts(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.base=Path(self.temp.name)
  self.job=dict(id='wall-collapse-test',family='building.wall',state='death',direction=None,fortification={'mask':0},loop=False,sourceCanvas=[1254,1254],runtimeCell=[128,128],pivot=[627,900],renderSize=[42.3225,42.3225],sourceMethod='FINISHED_WHOLE_2D_FRAMES',wholeCanvasTransform='UNIFORM_LANCZOS_NO_CROP_SHIFT_FIT',frames=[])
  for i,duration in enumerate([120,150,180,1000]):
   im=Image.new('RGBA',(1254,1254));ImageDraw.Draw(im).rectangle((450+i*20,600,800,900),fill=(100+i*30,70,40,255));path=self.base/f'F{i}.png';im.save(path)
   source=dict(path=str(path),sha256=adapter.sha(path.read_bytes()),rgbaSha256=adapter.sha(im.tobytes()),width=1254,height=1254)
   receipt=self.base/f'selection{i}.json';receipt.write_text(json.dumps(dict(status='SELECTED_FRAME_CANDIDATE',frameIndex=i,sourceSha256=source['sha256'],rgbaSha256=source['rgbaSha256'])))
   tool=self.base/f'tool{i}.json';tool.write_text('{"technicalFixture":true}')
   self.job['frames'].append(dict(index=i,phase=f'F{i}',selectionStatus='SELECTED_FRAME_CANDIDATE',durationMs=duration,source=source,originalRaw=dict(path=str(path),sha256=source['sha256']),toolReceipt=dict(path=str(tool),sha256=adapter.sha(tool.read_bytes())),selectionReceipt=dict(path=str(receipt),sha256=adapter.sha(receipt.read_bytes()))))
 def tearDown(self):self.temp.cleanup()
 def save(self,job=None):
  path=self.base/'job.json';path.write_text(json.dumps(job or self.job));return path
 def test_rejects_missing_family_timing_loop_and_unselected(self):
  mutations=[lambda j:j['frames'].pop(),lambda j:j['frames'][2]['source'].update(width=1024),lambda j:j['frames'][1].update(durationMs=0),lambda j:j.update(loop=True),lambda j:j['frames'][3].update(selectionStatus='HOLD'),lambda j:j['frames'][1].update(offset=[0,0])]
  for mutate in mutations:
   job=copy.deepcopy(self.job);mutate(job)
   with self.assertRaises(ValueError):adapter.preflight(self.save(job))
 def test_exact_pack_terminal_and_real_loader(self):
  output=self.base/'output';ledger=adapter.export(self.save(),output);manifest=json.loads((output/'manifest.json').read_text());asset=manifest['assets'][0]
  self.assertEqual(ledger['totalDurationMs'],1450);self.assertEqual(ledger['terminal']['frame'],3);self.assertFalse(asset['loop'])
  atlas=Image.open(output/'atlas.png').convert('RGBA')
  for i,f in enumerate(asset['frames']):
   source=Image.open(f['source']['path']).convert('RGBA');self.assertEqual(atlas.crop((128*i,0,128*(i+1),128)).tobytes(),source.resize((128,128),Image.Resampling.LANCZOS).tobytes())
   self.assertEqual(adapter.sha(Path(f['source']['path']).read_bytes()),self.job['frames'][i]['source']['sha256'])
  script="import fs from 'node:fs';import {validateAsset,validateManifest} from './client/art-assets.js';import {sampleSpriteAnimation} from './client/sprite-timing.js';const m=JSON.parse(fs.readFileSync(process.argv[1]));validateManifest(m);validateAsset(m.assets[0]);for(const [t,f] of [[0,0],[120,1],[270,2],[450,3],[1450,3],[99999,3]])if(sampleSpriteAnimation(m.assets[0].frames,{timeMs:t,loop:false}).frame!==f)throw Error('Timing/terminal drift');"
  subprocess.run(['node','--input-type=module','-e',script,str(output/'manifest.json')],cwd=adapter.ROOT,check=True)
if __name__=='__main__':unittest.main()
