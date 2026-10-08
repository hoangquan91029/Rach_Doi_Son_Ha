from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
B=Path(__file__).resolve().parent
src=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha-art-lease/villager-walk-SOUTH-007/walk/keys/F00-left-contact-01/raw.png')
im=Image.open(src).convert('RGBA')
im.putalpha(im.getchannel('A').point(lambda a: round(a*.20)))
layer=Image.new('RGBA',(1254,1254),(0,0,0,0));d=ImageDraw.Draw(layer)
try: font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',19); small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
except: font=small=None
white=(255,255,255,255);blue=(40,150,255,255);bluefill=(35,145,255,150);orange=(255,150,35,255);orangefill=(255,140,25,150);yellow=(255,245,70,255);green=(80,255,120,255);muted=(205,215,225,255)
def label(box,lines,color):
 d.rounded_rectangle(box,radius=8,fill=(12,19,28,225),outline=color,width=2)
 x,y=box[0]+8,box[1]+6
 for line in lines:
  d.text((x,y),line,font=small,fill=color,stroke_width=1,stroke_fill=(8,8,8,220));y+=19
# Title lives in blank upper-left space and does not cover the character's hat.
label((16,18,420,112),['2D MODEL GUIDE: F4 OPPOSITE CONTACT','Ghosted illustration = selected F0 continuity','Blue = RIGHT/viewer-left receives; orange = LEFT trails'],white)
# Light source-coordinate grid for contact and pivot alignment.
for y in (1000,1100,1140,1200):d.line((300,y,930,y),fill=(255,255,255,45),width=1)
d.line((654,750,654,1230),fill=(255,255,255,55),width=1)
d.ellipse((646,1132,662,1148),fill=yellow,outline=(20,20,20,255),width=2)
# F0 measurements from inspected raw PNG. These marks are historical reference landmarks, not output targets.
d.rounded_rectangle((760,1177,872,1211),radius=11,outline=green,width=4)
d.ellipse((806,1193,822,1209),fill=green,outline=(15,50,20,255),width=2)
label((878,1150,1235,1231),['MEASURED F0 support:', 'LEFT / viewer-right, flat sole', 'contact center ≈ (814,1201)'],green)
d.ellipse((438,1048,462,1072),outline=muted,width=3)
d.ellipse((515,1075,537,1097),outline=muted,width=3)
label((16,930,342,1010),['MEASURED F0 RIGHT trailing:', 'toe ≈ (450,1060); heel ≈ (526,1086)', 'manual estimate ±10 px'],muted)
# F4 opposite support: target coordinates derive from the observed F0 stride baseline/depth delta.
d.line((652,435,638,696),fill=yellow,width=7)
label((16,744,386,805),['F4 torso settles subtly LEFT', 'toward the receiving RIGHT leg;', 'keep the full-canvas anchor fixed'],yellow)
# RIGHT / viewer-left leg extends to receive weight on a flat whole sandal.
d.line([(600,820),(574,948),(528,1085)],fill=blue,width=20,joint='curve')
d.ellipse((515,1072,541,1098),fill=blue)
d.line((528,1085,498,1189),fill=blue,width=18)
d.rounded_rectangle((438,1184,553,1210),radius=12,fill=bluefill,outline=blue,width=5)
d.line((446,1199,548,1199),fill=white,width=4)
d.ellipse((490,1182,506,1198),fill=white,outline=blue,width=2)
label((16,1065,332,1143),['F4 RIGHT / viewer-left:', 'forward, low, flat, receiving', 'sole center target ≈ (496,1197)'],blue)
# LEFT / viewer-right leg trails. Toe is low/down; heel is visibly raised.
d.line([(704,820),(768,946),(820,1070)],fill=orange,width=20,joint='curve')
d.ellipse((807,1058,833,1084),fill=orange)
d.line((820,1070,812,1092),fill=orange,width=18)
d.polygon([(785,1088),(815,1092),(842,1080),(864,1064),(851,1058),(827,1073),(803,1077)],fill=orangefill,outline=orange)
d.ellipse((803,1083,819,1099),fill=white,outline=orange,width=2)
label((878,1008,1235,1090),['F4 LEFT / viewer-right:', 'trailing; toe-down, heel raised', 'toe target ≈ (811,1091)'],orange)
# Opposite arm counter-swing, kept attached to the continuous torso.
d.line([(565,472),(515,577),(465,693)],fill=blue,width=16,joint='curve');d.ellipse((455,682,475,702),fill=blue)
d.line([(725,470),(770,560),(818,650)],fill=orange,width=16,joint='curve');d.ellipse((808,640,828,660),fill=orange)
label((16,820,325,891),['RIGHT arm moves back', 'to counter the forward RIGHT leg'],blue)
label((900,690,1235,761),['LEFT arm moves forward', 'to counter the support leg'],orange)
# The pivot marker is numerically defined in the companion landmark JSON.
d.text((666,1127),'PIVOT [654,1140]',font=small,fill=yellow,stroke_width=2,stroke_fill=(10,10,10,230))
im.alpha_composite(layer)
im.save(B/'F4-opposite-contact-guide.png')
