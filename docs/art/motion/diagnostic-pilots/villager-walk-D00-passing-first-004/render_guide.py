from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math
out=Path(__file__).parent
W=H=1254
BG=(29,42,39,255); INK=(28,33,28,255); CLOTH=(220,211,180,255); HAT=(177,143,93,255)
FAR=(242,132,65,255); NEAR=(65,190,207,255); MUTED=(132,151,134,255); LIGHT=(241,231,204,255)
im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
def line(points,fill,width): d.line(points,fill=fill,width=width,joint='curve')
def ell(box,fill,outline=INK,width=7): d.ellipse(box,fill=fill,outline=outline,width=width)
def poly(points,fill,outline=INK,width=8): d.polygon(points,fill=fill); d.line(points+[points[0]],fill=outline,width=width,joint='curve')
def chain(points,color,width=60,joint=27):
    line(points,color,width); line(points,INK,9)
    for x,y in points[1:-1]: ell((x-joint,y-joint,x+joint,y+joint),LIGHT,INK,7)
def sandal(heel,toe,color):
    vx=toe[0]-heel[0]; vy=toe[1]-heel[1]; L=math.hypot(vx,vy); px=-vy/L*18; py=vx/L*18
    pts=[(heel[0]+px,heel[1]+py),(toe[0]+px*.75,toe[1]+py*.75),(toe[0]-px*.75,toe[1]-py*.75),(heel[0]-px,heel[1]-py)]
    poly(pts,color,INK,7); line([heel,toe],LIGHT,4)
# Ground/support plane and root. One compact shadow only under planted near foot.
d.ellipse((594,1127,708,1155),fill=(12,17,15,115))
line([(410,1140),(900,1140)],(119,135,123,255),3)
# Far leg and back-swinging arm, behind torso. The raised sandal is not near the floor line.
chain([(585,735),(705,850),(710,1000)],FAR,56,26)
chain([(710,1000),(730,1008)],FAR,40,20)
sandal((730,1008),(780,1027),FAR)
chain([(525,350),(465,415),(425,500)],FAR,54,26)
# Asymmetric three-quarter body block: shoulders, head and hat angle toward screen-ESE.
poly([(538,326),(607,294),(733,305),(792,360),(769,575),(745,735),(557,735),(529,575)],CLOTH,INK,9)
line([(547,580),(758,580)],(124,108,82,255),26)
ell((610,158,730,296),(157,112,76,255),INK,8)
# Elevated ESE nón lá: off-center apex and elliptical/asymmetric brim, not a front-facing disk.
poly([(503,208),(615,66),(811,191),(788,228),(531,238)],HAT,INK,10)
line([(519,211),(793,211)],(238,218,188,255),10)
# A small forward-facing profile cue points to screen-right while remaining schematic.
poly([(715,232),(745,243),(715,255)],(190,135,92,255),INK,4)
line([(630,350),(705,470),(681,565)],(198,183,151,255),7)
# Near / screen-right leg supports almost straight under the torso and near arm swings forward.
chain([(705,735),(670,865),(650,1040)],NEAR,62,29)
chain([(660,1040),(650,1115)],NEAR,48,23)
sandal((620,1120),(682,1147),NEAR)
chain([(785,355),(830,425),(865,500)],NEAR,56,27)
# Raised far foot at about (740,1018), with no contact shadow or ground mark beneath it.
# Labels clarify roles in this model-only guide. These marks must not appear in generated art.
font_path='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
font=ImageFont.truetype(font_path,30) if Path(font_path).exists() else ImageFont.load_default()
small=ImageFont.truetype(font_path,23) if Path(font_path).exists() else font
d.text((75,910),'NEAR / SCREEN-RIGHT',font=font,fill=NEAR,stroke_width=2,stroke_fill=INK)
d.text((75,948),'PLANTED UNDER BODY',font=small,fill=NEAR,stroke_width=2,stroke_fill=INK)
d.text((845,910),'FAR / SCREEN-LEFT',font=font,fill=FAR,stroke_width=2,stroke_fill=INK)
d.text((845,948),'SWINGING / FOOT AIRBORNE',font=small,fill=FAR,stroke_width=2,stroke_fill=INK)
d.text((518,1180),'ROOT (650,1140)',font=small,fill=LIGHT,stroke_width=2,stroke_fill=INK)
im.save(out/'F02-model-guide.png')
# Fixed 38/1254 full-canvas review preview, with root at the same displayed coordinate (48,68).
small_im=im.resize((38,38),Image.Resampling.LANCZOS)
preview=Image.new('RGBA',(128,110),(82,101,87,255)); preview.alpha_composite(small_im,(28,34))
pd=ImageDraw.Draw(preview); pf=ImageFont.truetype(font_path,10) if Path(font_path).exists() else ImageFont.load_default()
pd.text((3,2),'F02 / true 38px figure',font=pf,fill=(245,244,221,255))
pd.text((3,76),'NEAR foot planted',font=pf,fill=NEAR)
pd.text((3,87),'FAR foot raised',font=pf,fill=FAR)
pd.text((3,98),'root (48,68), fixed canvas',font=pf,fill=(226,229,209,255))
preview.save(out/'F02-guide-fixed-38px-preview.png')
