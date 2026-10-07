from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math
out=Path(__file__).parent
W=H=1254
BG=(29,42,39,255)
INK=(28,33,28,255)
CREAM=(225,215,182,255)
PAPER=(207,193,155,255)
FAR=(242,132,65,255)
NEAR=(65,190,207,255)
MUTED=(149,164,148,255)
im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
def line(points,fill,width): d.line(points,fill=fill,width=width,joint='curve')
def ellipse(box,fill,outline=INK,width=7): d.ellipse(box,fill=fill,outline=outline,width=width)
def poly(points,fill,outline=INK,width=8): d.polygon(points,fill=fill); d.line(points+[points[0]],fill=outline,width=width,joint='curve')
def limb(points,color,width=68,joint_r=35):
    line(points,color,width); line(points,INK,10)
    for x,y in points[1:-1]: ellipse((x-joint_r,y-joint_r,x+joint_r,y+joint_r),CREAM,INK,8)
def foot(heel,toe,color):
    # Sandal-shaped contact patch, with the toe pointing screen ESE.
    x1,y1=heel; x2,y2=toe
    vx=x2-x1; vy=y2-y1; L=math.hypot(vx,vy); px=-vy/L*22; py=vx/L*22
    pts=[(x1+px,y1+py),(x2+px*.72,y2+py*.72),(x2-px*.72,y2-py*.72),(x1-px,y1-py)]
    poly(pts,color,INK,8)
    line([heel,toe],(244,232,198,255),5)
# Root plane, just a diagram mark.
line([(400,1140),(900,1140)],(119,135,123,255),3)
# Far limbs behind torso. Lengths stay close to the master's limb proportions.
limb([(585,735),(670,850),(715,1000)],FAR,60,30)
limb([(715,1000),(740,1070)],FAR,44,22)
foot((740,1070),(790,1110),FAR)
# Far arm swings back while far leg leads.
limb([(525,350),(465,415),(425,500)],FAR,58,29)
# Torso and head mass, schematic only; no internal anatomical details.
poly([(535,325),(603,292),(737,300),(796,355),(772,590),(746,735),(558,735),(529,590)],(220,211,180,255),INK,10)
# Simple wrap/waist band.
line([(548,580),(758,580)],(124,108,82,255),28)
# Head / hat silhouette.
ellipse((602,164,720,300),(157,112,76,255),INK,8)
poly([(505,205),(628,70),(812,202),(785,231),(540,231)],(177,143,93,255),INK,10)
line([(524,207),(790,207)],(238,218,188,255),12)
# Near arm swings forward; same-side near leg trails.
limb([(785,355),(829,430),(860,510)],NEAR,64,31)
# Near leg: modestly flexed knee, upper-left trail; planted trailing sandal.
limb([(704,735),(630,850),(570,1000)],NEAR,62,31)
limb([(570,1000),(535,1068)],NEAR,46,23)
foot((535,1068),(490,1094),NEAR)
# Contact cues: far foot owns the forward lower-right contact, near foot is behind upper-left.
ellipse((773,1093,807,1127),FAR,INK,6)
ellipse((473,1077,507,1111),NEAR,INK,6)
# Ownership labels and arrows, positioned clear of body.
font_path='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
try: font=ImageFont.truetype(font_path,31)
except: font=ImageFont.load_default()
small=ImageFont.truetype(font_path,24) if Path(font_path).exists() else font
d.text((85,900),'NEAR / SCREEN-RIGHT',font=font,fill=NEAR,stroke_width=2,stroke_fill=INK)
d.text((85,938),'TRAILS • ARM FORWARD',font=small,fill=NEAR,stroke_width=2,stroke_fill=INK)
d.text((850,900),'FAR / SCREEN-LEFT',font=font,fill=FAR,stroke_width=2,stroke_fill=INK)
d.text((850,938),'LEADS • ARM BACK',font=small,fill=FAR,stroke_width=2,stroke_fill=INK)
d.text((563,1178),'ROOT (650, 1140)',font=small,fill=CREAM,stroke_width=2,stroke_fill=INK)
im.save(out/'F04-model-guide.png')
# Fixed-scale gameplay-size preview: transform complete 1254 canvas by 38/1254, no alpha fit.
scale=38/1254
small_im=im.resize((38,38),Image.Resampling.LANCZOS)
preview=Image.new('RGBA',(128,110),(82,101,87,255))
preview.alpha_composite(small_im,(28,34))
pd=ImageDraw.Draw(preview)
preview_font=ImageFont.truetype(font_path,10) if Path(font_path).exists() else ImageFont.load_default()
pd.text((3,2),'F04 / actual 38px scale',font=preview_font,fill=(245,245,220,255))
pd.text((3,76),'FAR lead: lower-right',font=preview_font,fill=FAR)
pd.text((3,87),'NEAR trail: upper-left',font=preview_font,fill=NEAR)
pd.text((3,98),'whole canvas; root at (48,68)',font=preview_font,fill=(226,229,209,255))
preview.save(out/'F04-guide-fixed-38px-preview.png')
