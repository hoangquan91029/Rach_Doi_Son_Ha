"""Synthetic pixels test GIF structure only; no authored artwork or visual approval."""
import importlib.util
from pathlib import Path
import tempfile
from PIL import Image, ImageDraw
spec=importlib.util.spec_from_file_location('pixel_sprites',Path(__file__).resolve().parents[1]/'scripts/pixel-sprites.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
frames=[]
for i in range(8):
    frame=Image.new('RGBA',(128,128),(0,0,0,0))
    ImageDraw.Draw(frame).rectangle((10+i,10,20+i,20),fill=(255,0,0,255));frames.append(frame)
durations=[100,110,120,130,140,150,160,170]
with tempfile.TemporaryDirectory() as directory:
    for loop in (False,True):
        path=Path(directory)/f'{loop}.gif'
        module.preview(frames,durations,path,loop=loop)
        with Image.open(path) as gif:
            assert gif.n_frames==8
            assert (gif.info.get('loop')==0) if loop else ('loop' not in gif.info)
            for i,duration in enumerate(durations):
                gif.seek(i)
                assert gif.info['duration']==duration
                assert gif.convert('RGBA').getpixel((0,0))[3]==0
                assert gif.convert('RGBA').getpixel((10+i,10))==(255,0,0,255)
print('PASS finite/loop GIF metadata, eight frames, timing and transparency')
