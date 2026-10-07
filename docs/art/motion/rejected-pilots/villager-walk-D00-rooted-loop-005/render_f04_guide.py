from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math
out=Path(__file__).parent; W=H=1254
INK=(28,33,28,255); CLOTH=(220,211,180,255); HAT=(177,143,93,255); FAR=(242,132,65,255); NEAR=(65,190,207,255); LIGHT=(241,231,204,255)
im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
def line(p,c,w): d.line(p,fill=c,width=w,joint='curve')
def ellipse(box,fill,outline=INK,width=7): d.ellipse(box,fill=fill,outline=outline,width=width)
def poly(points,fill,outline=INK,width=8): d.polygon(points,fill=fill); d.line(points+[points[0]],fill=outline,width=width,joint='curve')
def chain(points,c,w=56,j=25):
 line(points,c,w); line(points,INK,9)
 for x,y in points[1:-1]: ellipse((x-j,y-j,x+j,y+j),LIGHT,INK,7)
def sandal(heel,toe,c):
 vx=toe[0]-heel[0];vy=toe[1]-heel[1];L=math.hypot(vx,vy);px=-vy/L*18;py=vx/L*18
 pts=[(heel[0]+px,heel[1]+py),(toe[0]+.72*px,toe[1]+.72*py),(toe[0]-.72*px,toe[1]-.72*py),(heel[0]-px,heel[1]-py)]
 poly(pts,c,INK,7);line([heel,toe],LIGHT,4)
# Ground/root and one far-foot contact shadow only.
d.ellipse((651,1116,770,1150),fill=(12,17,15,112))
line([(410,1140),(900,1140)],(119,135,123,255),3)
# Far leading leg and rear-swing arm drawn behind the torso.
chain([(585,735),(645,860),(690,1020)],FAR,56,26)
chain([(690,1020),(675,1095)],FAR,42,21)
sandal((675,1095),(745,1138),FAR)
chain([(525,350),(465,415),(425,500)],FAR,54,26)
# Asymmetric elevated three-quarter ESE body silhouette is model-only; master owns appearance.
poly([(538,326),(607,294),(733,305),(792,360),(769,575),(745,735),(557,735),(529,575)],CLOTH,INK,9)
line([(547,580),(758,580)],(124,108,82,255),26)
line([(630,350),(705,470),(681,565)],(198,183,151,255),7)
ellipse((610,158,730,296),(157,112,76,255),INK,8)
poly([(503,208),(615,66),(811,191),(788,228),(531,238)],HAT,INK,10)
line([(519,211),(793,211),(770,229)],(238,218,188,255),10)
poly([(715,232),(745,243),(715,255)],(190,135,92,255),INK,4)
# Near trailing limb: heel lifted, sandal slightly airborne; no contact mark beneath it.
chain([(705,735),(620,855),(555,980)],NEAR,58,27)
chain([(555,980),(530,1038)],NEAR,44,22)
sandal((510,1040),(555,1068),NEAR)
# Near arm swings forward as its leg trails.
chain([(785,355),(830,425),(865,500)],NEAR,56,27)
# Model-only ownership labels; generated frame must contain none of these marks.
fp='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
font=ImageFont.truetype(fp,30) if Path(fp).exists() else ImageFont.load_default(); small=ImageFont.truetype(fp,23) if Path(fp).exists() else font
d.text((75,900),'NEAR / SCREEN-RIGHT',font=font,fill=NEAR,stroke_width=2,stroke_fill=INK)
d.text((75,938),'TRAILS / HEEL LIFTED',font=small,fill=NEAR,stroke_width=2,stroke_fill=INK)
d.text((845,900),'FAR / SCREEN-LEFT',font=font,fill=FAR,stroke_width=2,stroke_fill=INK)
d.text((845,938),'LEADS / SOLE PLANTED',font=small,fill=FAR,stroke_width=2,stroke_fill=INK)
d.text((518,1180),'ROOT (650,1140)',font=small,fill=LIGHT,stroke_width=2,stroke_fill=INK)
im.save(out/'F04-bridge-model-guide.png')
smallim=im.resize((38,38),Image.Resampling.LANCZOS)
prev=Image.new('RGBA',(128,110),(82,101,87,255));prev.alpha_composite(smallim,(28,34));pd=ImageDraw.Draw(prev);pf=ImageFont.truetype(fp,10) if Path(fp).exists() else ImageFont.load_default()
pd.text((3,2),'F04 bridge / true 38px',font=pf,fill=(245,244,221,255));pd.text((3,76),'FAR planted ahead',font=pf,fill=FAR);pd.text((3,87),'NEAR trails / lifts',font=pf,fill=NEAR);pd.text((3,98),'root fixed (48,68)',font=pf,fill=(226,229,209,255));prev.save(out/'F04-bridge-fixed-38px-preview.png')
