"""One finite authored-shadow dependency validation test, no art export."""
import importlib.util,json,sys,unittest
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).parent;s=importlib.util.spec_from_file_location('adapter_v2',P/'export-v2.py');a=importlib.util.module_from_spec(s);s.loader.exec_module(a)
class Dependency(unittest.TestCase):
 def test_existing_missing_and_mismatch(self):
  dep=json.loads((P/'shadow-dependency-v2.json').read_text());job={'shadowDependency':dep};asset,path,receipt=a.shadow_dependency(job,P);self.assertEqual(receipt['packaging'],'PASS');self.assertEqual(asset['render'],{'width':42,'height':42});self.assertEqual(asset['pivot'],{'x':658,'y':648,'space':'source'})
  bad=dict(dep,manifestPath=str(P/'nonexistent-shadow-manifest.json'))
  with self.assertRaisesRegex(ValueError,'Missing'):a.shadow_dependency({'shadowDependency':bad},P)
  bad=dict(dep,assetSha256='0'*64)
  with self.assertRaisesRegex(ValueError,'contract pin mismatch'):a.shadow_dependency({'shadowDependency':bad},P)
if __name__=='__main__':unittest.main(verbosity=2)
