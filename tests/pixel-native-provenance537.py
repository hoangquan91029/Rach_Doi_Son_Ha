import importlib.util
import tempfile
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('pixel',Path(__file__).resolve().parents[1]/'scripts/pixel-sprites.py')
pixel=importlib.util.module_from_spec(spec);spec.loader.exec_module(pixel)

class Provenance(unittest.TestCase):
 def test_resolved_union_and_negative_pins(self):
  with tempfile.TemporaryDirectory() as temporary:
   root=Path(temporary)
   def pin(path):
    file=root/path;file.parent.mkdir(parents=True,exist_ok=True);file.write_bytes(b'fixture bytes only')
    return {'path':path,'sha256':pixel.sha(file)}
   source=pin('docs/art/pixel-test/raw/S.png');recipe=pin('docs/art/pixel-test/authoring/draw.py');plan=pin('docs/art/pixel-test/authoring/plan.json')
   native={'kind':'native-raster','sources':[source],'recipe':recipe,'framePlan':plan}
   pixel.validate_provenance(native,root)
   pixel.validate_provenance({'sources':[source],'callTokens':['actual']},root)
   invalid=[{**native,'kind':'unknown'},{**native,'callTokens':['fake']},{**native,'sources':[]},{**native,'extra':True},{**native,'recipe':{**recipe,'sha256':'0'*64}},{**native,'recipe':pin('docs/art/pixel-other/authoring/draw.py')},{**native,'sources':[pin('docs/art/pipeline/old.png')]},{**native,'framePlan':{**plan,'path':'../outside.json'}},{**native,'recipe':{**recipe,'extra':1}},{'sources':[source],'callTokens':[]},{'sources':[source],'callTokens':['a','a']}]
   for value in invalid:
    with self.subTest(value=value),self.assertRaises(ValueError):pixel.validate_provenance(value,root)
   # Both in-root file symlinks and directory symlinks are forbidden.
   original=root/source['path'];target=original.with_name('original.png');original.rename(target);original.symlink_to(target)
   with self.assertRaises(ValueError):pixel.validate_provenance(native,root)
   original.unlink();target.rename(original)
   authoring=root/'docs/art/pixel-test/authoring';real=authoring.with_name('actual');authoring.rename(real);authoring.symlink_to(real,target_is_directory=True)
   with self.assertRaises(ValueError):pixel.validate_provenance(native,root)
if __name__=='__main__':unittest.main()
