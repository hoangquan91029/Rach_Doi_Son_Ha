#!/usr/bin/env python3
"""Hand2D local silhouette correction; no original/source-art mutation."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageChops
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');O=Path(__file__).parent;sha=lambda b:hashlib.sha256(b).hexdigest()
paths={'canonicalSouth':R/'docs/art/characters/villager-neutral-D01-screen-South-007/raw.png','currentF7CorrectionTarget':R/'docs/art/pipeline/villager-pure2d-SOUTH-011/F7-inbetween-01/raw.png','selectedF6':R/'docs/art/pipeline/villager-pure2d-SOUTH-010/F6-left-passing-01/raw.png','selectedF0':R/'docs/art/motion/authoring-tools/villager-walk-SOUTH-007/walk/keys/F00-left-contact-01/raw.png'}
refs={}
for role,p in paths.items():
 im=Image.open(p).convert('RGBA');assert im.size==(1254,1254);refs[role]={'path':str(p),'encodedSha256':sha(p.read_bytes()),'rgbaSha256':sha(im.tobytes()),'dimensions':[1254,1254],'role':('local correction edit target; preserve upper-body art' if role=='currentF7CorrectionTarget' else 'identity/material/light authority' if role=='canonicalSouth' else 'actual selected neighboring key continuity reference')}
im=Image.open(paths['currentF7CorrectionTarget']).convert('RGBA');m=im.getchannel('A').point(lambda v:255 if v>=32 else 0);edge=ImageChops.subtract(m.filter(ImageFilter.MaxFilter(3)),m.filter(ImageFilter.MinFilter(3)));guide=Image.new('RGB',(1254,1254),'white');guide.paste((190,190,190),(0,0),edge);d=ImageDraw.Draw(guide);d.rectangle((435,820,850,1230),fill='white');font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
def text(x,y,s):d.text((x,y),s,font=font,fill='black')
text(22,20,'AUTHORING_ONLY F7 correction: clearly separated natural calves');text(22,48,'Gray upper-body context; black lower silhouette = hand2D intent only');text(22,76,'Natural spacing first; toe estimates are not rigid pins / no pixel microgate')
# Simple separate leg outlines. No color underlay, projection or limb textures.
right=[(538,820),(520,886),(527,940),(520,994),(511,1055),(522,1094),(529,1118),(530,1130),(549,1136),(583,1131),(588,1122),(573,1107),(558,1080),(557,1054),(576,1007),(597,966),(609,919),(620,856)]
left=[(674,820),(665,874),(676,933),(685,979),(697,1034),(704,1083),(710,1115),(706,1136),(715,1151),(742,1155),(770,1150),(779,1141),(766,1130),(750,1111),(746,1084),(752,1041),(754,993),(748,938),(753,872),(748,820)]
d.line(right,fill='black',width=3);d.line(left,fill='black',width=3)
d.line([(529,1130),(580,1130)],fill='black',width=4);d.line([(715,1150),(770,1150)],fill='black',width=4)
text(22,930,'RIGHT / viewer LEFT');text(22,958,'Trailing, pushing off after F6');text(22,986,'Toe region ~560,1130');d.line([(180,1028),(560,1130)],fill='black',width=2)
text(865,930,'LEFT / viewer RIGHT');text(865,958,'Reaches naturally toward F0');text(865,986,'Toe region ~740,1150');d.line([(997,1028),(740,1150)],fill='black',width=2)
text(847,1075,'Keep visible calf gap');d.line([(840,1108),(630,1014)],fill='black',width=2)
text(22,1215,'Same1254 canvas / pivot654,1140 / ref1130. Preserve identity/camera/whole-frame scale.')
p=O/'F7-separated-calves-guide.png';guide.save(p)
(O/'references.json').write_text(json.dumps(refs,indent=2)+'\n')
(O/'F7-landmarks.json').write_text(json.dumps({'status':'AUTHORING_ONLY_ESTIMATES','frame':'F7','canvas':[1254,1254],'pivot':[654,1140],'referenceHeight':1130,'RIGHTTrailingToeApprox':[560,1130],'LEFTApproachingToeApprox':[740,1150],'priority':'Uncrossed naturally connected knees/calves and visible separation at gameplay size; preserve whole-image scale and identity. Toe coordinates/outline are flexible hand2D intent, not sealed measurements or hard pixels.','guide':{'path':str(p),'sha256':sha(p.read_bytes())}},indent=2)+'\n')
