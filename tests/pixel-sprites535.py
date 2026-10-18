import importlib.util
import tempfile
import unittest
from pathlib import Path
from PIL import Image
spec=importlib.util.spec_from_file_location('pixels',Path(__file__).resolve().parents[1]/'scripts/pixel-sprites.py');p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)

def frames(row=0):
    result=[]
    for f in range(8):
        im=Image.new('RGBA',(128,128));im.putpixel((10+f,10+row),(20,30,40,255));result.append(im)
    return result
class Pixels(unittest.TestCase):
    def test_reject_mutations(self):
        for mutation in ['duplicate','alpha','border','empty','palette']:
            fs=frames()
            if mutation=='duplicate':fs[1]=fs[0].copy()
            if mutation=='alpha':fs[0].putpixel((40,40),(1,2,3,128))
            if mutation=='border':fs[0].putpixel((0,40),(1,2,3,255))
            if mutation=='empty':fs[0]=Image.new('RGBA',(128,128))
            if mutation=='palette':
                for i in range(33):fs[0].putpixel((40+i,40),(i,1,2,255))
            with self.assertRaises(ValueError):p.check_frames(fs)
    def test_cyclic_direction_substitution(self):
        original=frames()
        for mirrored in (False,True):
            row=[p.ImageOps.mirror(f) if mirrored else f.copy() for f in original]
            shifted=row[3:]+row[:3]
            with self.assertRaisesRegex(ValueError,'shifted phases'):
                p.check_direction_rows([original,shifted])
        p.check_direction_rows([frames(0),frames(1)])
    def test_new_source_provenance_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            raw=root/'docs/art/pixel-worker-535/raw/strip.png';raw.parent.mkdir(parents=True);Image.new('RGBA',(128,128)).save(raw)
            provenance={'sources':[{'path':str(raw.relative_to(root)),'sha256':p.sha(raw)}],'callTokens':['consumed-token']}
            p.validate_provenance(provenance,root)
            for bad in ['docs/art/pipeline/old.png','docs/art/pixel-worker-535/references/leader.png','assets/art-v1/old.png']:
                target=root/bad;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw.read_bytes())
                with self.assertRaisesRegex(ValueError,'pixel sources'):
                    p.validate_provenance({'sources':[{'path':bad,'sha256':p.sha(target)}],'callTokens':['token']},root)
            link=raw.parent/'link.png';link.symlink_to(root/'assets/art-v1/old.png')
            with self.assertRaisesRegex(ValueError,'pixel sources'):
                p.validate_provenance({'sources':[{'path':str(link.relative_to(root)),'sha256':p.sha(link)}],'callTokens':['token']},root)
    def test_native_pack_and_gif(self):
        with tempfile.TemporaryDirectory() as tmp:
            strips=[]
            for row in range(8):
                im=Image.new('RGBA',(1024,128))
                for f,frame in enumerate(frames(row)):im.paste(frame,(128*f,0))
                path=Path(tmp)/f'{row}.png';im.save(path);strips.append(path)
            atlas=Path(tmp)/'atlas.png';p.pack(strips,atlas)
            with Image.open(atlas) as image:self.assertEqual(image.size,(1024,1024))
            gif=Path(tmp)/'loop.gif';p.preview(frames(),[100]*8,gif)
            with Image.open(gif) as image:
                self.assertEqual(image.n_frames,8)
                for f in range(8):image.seek(f);self.assertEqual(image.info['duration'],100)
            with self.assertRaises(ValueError):p.pack([strips[0]]*8,Path(tmp)/'bad.png')
            wrong=Path(tmp)/'wrong.png';Image.new('RGBA',(1024,1024)).save(wrong)
            with self.assertRaises(ValueError):p.strip_frames(wrong)
if __name__=='__main__':unittest.main()
