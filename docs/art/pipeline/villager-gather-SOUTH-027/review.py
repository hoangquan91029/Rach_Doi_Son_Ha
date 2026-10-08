from pathlib import Path
from PIL import Image,ImageDraw
import sys,json
L=Path(__file__).parent;s=int(sys.argv[1]);w=json.loads((L/'WORK_ORDER.json').read_text());refs=w["refs"][str(s)]+[str(L/f'F0{s}-call01/raw.png')];sheet=Image.new('RGBA',(120*len(refs),140),(210,204,184,255));d=ImageDraw.Draw(sheet)
for i,p in enumerate(refs):
 sheet.alpha_composite(Image.open(p).convert('RGBA').resize((89,89),Image.Resampling.LANCZOS),(15+i*120,28));d.text((15+i*120,7),'candidate' if i==len(refs)-1 else 'actualkeyref',fill=(30,30,30))
sheet.save(L/f'F0{s}-call01/review-80.png')
