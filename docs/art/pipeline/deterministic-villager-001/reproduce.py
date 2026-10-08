"""Reproduce the frozen mesh pilot into a NEW lease; never rewrite originals."""
import argparse, hashlib, json, pathlib, shutil, subprocess, sys
import numpy
from PIL import Image, __version__ as pillow_version

parser=argparse.ArgumentParser()
parser.add_argument('output',type=pathlib.Path)
args=parser.parse_args()
source=pathlib.Path(__file__).resolve().parent
output=args.output.resolve()
if output.exists(): raise SystemExit('Output already exists; choose a new lease.')
script=source/'pilot.py'
script_sha=hashlib.sha256(script.read_bytes()).hexdigest()
if script_sha!='b5c1472cce875cec649e8331b4f91da2bef64a7f57b910109a360ad727fb62e4':
 raise SystemExit('Frozen renderer hash mismatch.')
output.mkdir(parents=True)
shutil.copyfile(script,output/'pilot.py')
subprocess.run([sys.executable,str(output/'pilot.py'),'build'],check=True)
comparisons=[]
for frame in range(8):
 original=source/'frames'/f'F{frame}.png'; reproduced=output/'frames'/f'F{frame}.png'
 a=Image.open(original).convert('RGBA');b=Image.open(reproduced).convert('RGBA')
 comparisons.append({'frame':frame,'pngEqual':original.read_bytes()==reproduced.read_bytes(),
  'rgbaEqual':a.size==b.size and a.tobytes()==b.tobytes(),
  'rgbaSha256':hashlib.sha256(b.tobytes()).hexdigest()})
receipt={'rendererSha256':script_sha,'python':sys.version,'numpy':numpy.__version__,
 'pillow':pillow_version,'comparisons':comparisons,'artApproved':False,
 'reproducibilityPass':all(r['pngEqual'] and r['rgbaEqual'] for r in comparisons)}
(output/'reproduction-comparison.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'output':str(output),'reproducibilityPass':receipt['reproducibilityPass']}))
if not receipt['reproducibilityPass']:raise SystemExit(1)
