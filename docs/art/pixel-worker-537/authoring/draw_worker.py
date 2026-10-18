#!/usr/bin/env python3
"""Native integer pixel clusters. No input art, transforms, interpolation or mirroring.
Each plan pose supplies independent physical limb keypoints. Anatomy refinements:
hip centers retained; foot toe is broadened forward 2px; rounded knees are drawn
as asymmetric folded trouser clusters. Head/torso share costume vocabulary.
"""
import json, hashlib
from pathlib import Path
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[4]
BASE=ROOT/'docs/art/pixel-worker-537'
PLAN=BASE/'authoring/walk-S-plan.json'
P=json.loads(PLAN.read_text())
C={'ink':'#20232d','hair':'#252b36','hairmid':'#38434d','hairlight':'#52606a','skin0':'#825144','skin1':'#b77b59','skin2':'#d6a071','skin3':'#edbd87','blue0':'#242e49','blue1':'#344365','blue2':'#4b6185','blue3':'#6a7e9c','brown0':'#403136','brown1':'#64493e','brown2':'#85634a','brown3':'#a17c58','gold0':'#765335','gold1':'#b58a44','gold2':'#d2aa61'}

def draw_pose(p):
 im=Image.new('RGBA',(128,128)); d=ImageDraw.Draw(im)
 def poly(points,c): d.polygon(points,fill=C[c])
 def line(points,c,w=1): d.line(points,fill=C[c],width=w)
 def rect(box,c): d.rectangle(box,fill=C[c])
 x=p['torsoWeightX']; b=p['bodyBobY']
 # Trouser legs are articulated volumes rather than strokes. Rear leg first.
 for side in (('rightLeg','leftLeg') if p['leftLeg']['stance'] else ('leftLeg','rightLeg')):
  l=p[side]; hx,hy=l['hip']; kx,ky=l['knee']; ax,ay=l['ankle']; tx,ty=l['toe']; near=l['stance']
  poly([(hx-5,hy-3),(hx+5,hy-3),(kx+5,ky-2),(kx+4,ky+4),(ax+3,ay),(ax+2,ay+2),(ax-3,ay+2),(kx-4,ky+3),(kx-5,ky-2)],'ink')
  poly([(hx-4,hy-2),(hx+3,hy-2),(kx+4,ky-1),(kx+2,ky+3),(ax+2,ay),(ax-2,ay+1),(kx-3,ky+2),(kx-4,ky-2)],'brown1' if near else 'brown0')
  poly([(hx-3,hy),(hx,hy+2),(kx+1,ky-2),(kx-2,ky),(ax-1,ay-1),(ax-2,ay-1),(kx-3,ky+1)],'brown2')
  line([(kx-2,ky),(kx+2,ky+1),(kx+3,ky+3)],'brown3')
  line([(ax-2,ay-2),(ax+2,ay-2)],'gold0')
  # Top of bare foot visible from elevated camera, irregular toe silhouette.
  poly([(ax-3,ay),(ax+2,ay),(tx+3,ty-1),(tx+3,ty+1),(tx+1,ty+2),(tx-3,ty+1),(ax-4,ay+2)],'ink')
  poly([(ax-2,ay),(ax+1,ay),(tx+2,ty),(tx+1,ty+1),(tx-2,ty),(ax-3,ay+1)],'skin1')
  line([(ax-2,ay),(tx-1,ty-1),(tx+1,ty-1)],'skin2')
  d.point((tx+1,ty),fill=C['skin3'])
 # Sleeves swing from stable anatomical shoulders; shoulders and elbows form sewn cloth.
 for side,sx in [('rightHand',53+x),('leftHand',75+x)]:
  tx,ty=p[side]; outward=-1 if side=='rightHand' else 1; ex=sx+outward*3; ey=72+b+(ty-81)//2
  poly([(sx-4,61+b),(sx+4,61+b),(ex+4,ey),(tx+3,ty-3),(tx+2,ty),(tx-4,ty),(ex-4,ey+2)],'ink')
  poly([(sx-3,62+b),(sx+2,63+b),(ex+3,ey),(tx+2,ty-4),(tx-3,ty-3),(ex-3,ey+1)],'blue1')
  poly([(sx-3,63+b),(sx-1,64+b),(ex,ey-1),(tx-2,ty-5),(tx-3,ty-3),(ex-3,ey)],'blue2')
  line([(ex-2,ey+1),(ex+2,ey+2)],'blue0')
  line([(tx-3,ty-3),(tx+2,ty-3)],'blue3')
  poly([(tx-3,ty-2),(tx+2,ty-2),(tx+3,ty+1),(tx+1,ty+4),(tx-2,ty+3),(tx-4,ty+1)],'ink')
  poly([(tx-2,ty-2),(tx+1,ty-2),(tx+2,ty+1),(tx,ty+3),(tx-2,ty+2),(tx-3,ty)],'skin1')
  line([(tx-2,ty-1),(tx,ty-1),(tx+1,ty+1)],'skin3')
  line([(tx-1,ty+1),(tx-1,ty+2)],'skin0')
 # Neck and cross-front tunic; silhouette includes asymmetric side vents.
 poly([(59+x,55+b),(68+x,55+b),(69+x,63+b),(58+x,63+b)],'ink')
 rect((60+x,56+b,66+x,63+b),'skin1'); rect((60+x,56+b,63+x,61+b),'skin2')
 poly([(56+x,60+b),(60+x,59+b),(64+x,63+b),(68+x,59+b),(73+x,61+b),(76+x,70+b),(73+x,79+b),(75+x,89+b),(68+x,91+b),(64+x,89+b),(58+x,91+b),(52+x,88+b),(55+x,77+b),(53+x,68+b)],'ink')
 poly([(56+x,62+b),(60+x,61+b),(65+x,65+b),(69+x,61+b),(72+x,63+b),(73+x,72+b),(71+x,79+b),(73+x,87+b),(67+x,89+b),(63+x,87+b),(57+x,89+b),(54+x,87+b),(57+x,76+b),(55+x,68+b)],'blue1')
 poly([(56+x,63+b),(59+x,62+b),(63+x,66+b),(60+x,75+b),(59+x,82+b),(55+x,86+b),(57+x,74+b)],'blue2')
 poly([(69+x,63+b),(71+x,65+b),(69+x,72+b),(64+x,79+b),(62+x,79+b),(64+x,70+b)],'blue0')
 line([(68+x,61+b),(65+x,67+b),(61+x,75+b),(60+x,79+b)],'blue3')
 line([(59+x,62+b),(63+x,66+b)],'blue3')
 poly([(64+x,82+b),(67+x,84+b),(70+x,88+b),(67+x,89+b)],'blue0')
 line([(57+x,84+b),(56+x,87+b),(59+x,86+b)],'blue3')
 rect((55+x,79+b,72+x,81+b),'gold0'); line([(56+x,79+b),(71+x,79+b)],'gold2'); line([(56+x,80+b),(71+x,80+b)],'gold1')
 rect((63+x,79+b,65+x,82+b),'gold2'); line([(65+x,82+b),(66+x,86+b)],'gold1')
 # Elevated visible headcloth crown and face, ears, jaw, nose and brow.
 poly([(56+x,44+b),(59+x,40+b),(67+x,39+b),(72+x,42+b),(73+x,49+b),(71+x,54+b),(68+x,59+b),(61+x,59+b),(57+x,55+b),(55+x,49+b)],'ink')
 poly([(58+x,47+b),(70+x,47+b),(71+x,51+b),(69+x,56+b),(66+x,58+b),(61+x,56+b),(58+x,53+b)],'skin1')
 poly([(58+x,48+b),(63+x,48+b),(64+x,52+b),(62+x,55+b),(59+x,53+b)],'skin2')
 line([(59+x,49+b),(61+x,49+b)],'skin0'); line([(66+x,49+b),(68+x,49+b)],'skin0')
 d.point((60+x,50+b),fill=C['ink']); d.point((67+x,50+b),fill=C['ink'])
 line([(64+x,50+b),(65+x,53+b),(63+x,53+b)],'skin3'); line([(63+x,55+b),(66+x,55+b)],'skin0')
 rect((56+x,49+b,57+x,52+b),'skin2'); rect((71+x,49+b,72+x,52+b),'skin0')
 poly([(56+x,44+b),(59+x,41+b),(66+x,40+b),(71+x,43+b),(72+x,47+b),(68+x,49+b),(61+x,47+b),(56+x,48+b)],'hair')
 poly([(58+x,43+b),(62+x,41+b),(67+x,41+b),(69+x,43+b),(64+x,44+b),(58+x,46+b)],'hairmid')
 line([(59+x,43+b),(64+x,42+b),(67+x,42+b)],'hairlight')
 line([(57+x,47+b),(62+x,45+b),(69+x,46+b),(71+x,45+b)],'hairlight')
 poly([(71+x,46+b),(74+x,47+b),(75+x,51+b),(73+x,55+b),(72+x,51+b),(70+x,49+b)],'hair')
 line([(73+x,48+b),(74+x,50+b),(73+x,52+b)],'hairmid')
 return im

def main():
 raw=BASE/'raw'; prev=BASE/'preview'; (raw/'S').mkdir(parents=True,exist_ok=True);prev.mkdir(exist_ok=True)
 frames=[draw_pose(p) for p in P['frames']]
 for i,im in enumerate(frames): im.save(raw/'S'/f'F{i}.png')
 strip=Image.new('RGBA',(1024,128))
 for i,im in enumerate(frames):strip.paste(im,(i*128,0))
 strip.save(raw/'worker-walk-S.png')
 sheet=Image.new('RGB',(1024,152),'#d5d0bc'); dr=ImageDraw.Draw(sheet)
 for i,im in enumerate(frames):sheet.paste(im,(128*i,24),im);dr.text((128*i+8,6),f"F{i} {P['frames'][i]['phase'].split('_')[0]}",fill='#20232d')
 sheet.save(prev/'walk-S-contact.png')
 # Palette-index GIF preserves every native pixel; transparent index0 is reserved.
 pal=[(0,0,0)]+[tuple(bytes.fromhex(c[1:])) for c in C.values()]
 gifs=[]
 for im in frames:
  idx=Image.new('P',im.size);idx.putpalette(sum((list(c) for c in pal),[])+[0]*(768-len(pal)*3))
  lut={c:i for i,c in enumerate(pal)};idx.putdata([0 if a==0 else lut[(r,g,b)] for r,g,b,a in im.getdata()]);gifs.append(idx)
 gifs[0].save(prev/'walk-S-native.gif',save_all=True,append_images=gifs[1:],duration=P['durationsMs'],loop=0,transparency=0,disposal=2,optimize=False)
 colors=set(c for im in frames for c in im.getdata() if c[3]); hashes=[hashlib.sha256(im.tobytes()).hexdigest() for im in frames]
 assert len(colors)<=32 and len(set(hashes))==8
 assert all(set(im.getchannel('A').getdata())=={0,255} for im in frames)
 out={'colors':len(colors),'palette':list(C.values()),'framePixelHashes':hashes,'bboxes':[im.getbbox() for im in frames]}
 (prev/'native-check.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
