"""New integer-grid raster study538. No source images, resampling or animation.
Contours, material planes, garment seams and native clusters are editable here.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import hashlib, json, math, random

ROOT = Path(__file__).resolve().parents[4]
BASE = ROOT / 'docs/art/pixel-village-538'
OUT = ROOT / 'public/assets/art-direction-538'
P = dict(ink='#202c30', deep='#403c35', navy='#574b3f', blue='#75624d',
         mid='#927d5d', lit='#ac9570', seam='#bba681', hair='#242e30',
         wrap='#394344', wraplit='#596260', skin='#ac744e', shade='#7d513c',
         warm='#cc9464', skinlit='#e1b17b', eye='#303238',
         pant='#5b4a39', pantmid='#786047', pantlit='#958062',
         sash='#b18a48', sashlit='#d1ae63', sashdark='#86643a',
         cuff='#8d9f94', metal='#9caeab', wood='#99734c')

def canvas(size):
    im = Image.new('RGBA', size); return im, ImageDraw.Draw(im)
def poly(d, pts, c): d.polygon(pts, fill=P.get(c,c))
def box(d, xy, c): d.rectangle(xy, fill=P.get(c,c))
def line(d, pts, c, w=1): d.line(pts, fill=P.get(c,c), width=w)

def worker(view):
    im,d=canvas((128,128))
    if view=='S':
        # Legs separately shaped: knee and ankle taper, separate bare feet.
        poly(d,[(56,73),(65,74),(65,89),(63,99),(63,108),(59,110),(55,108),(57,94),(55,84)],'ink')
        poly(d,[(66,74),(75,73),(77,84),(75,94),(75,108),(71,110),(67,108),(68,96),(66,87)],'ink')
        poly(d,[(57,77),(63,77),(63,90),(61,99),(61,107),(57,107),(59,93)],'pantmid')
        poly(d,[(68,77),(74,76),(75,84),(73,96),(73,108),(69,108),(70,93)],'pant')
        line(d,[(58,81),(60,88),(59,97)],'pantlit',2)
        line(d,[(69,80),(72,88),(71,98)],'pantmid',2)
        box(d,(57,105,61,109),'skin');box(d,(69,106,73,110),'shade')
        poly(d,[(57,108),(61,108),(63,110),(63,112),(54,112),(54,110)],'shade')
        box(d,(55,110,61,111),'warm');box(d,(55,112,61,112),'skin')
        poly(d,[(69,109),(73,108),(76,111),(76,112),(68,112),(68,110)],'shade')
        box(d,(69,110,74,111),'skin');box(d,(70,110,73,110),'warm')
        # Far/near sleeves, elbows and cuffs, then torso overlays shoulder joins.
        poly(d,[(54,44),(60,46),(57,56),(53,65),(52,76),(46,78),(45,74),(46,61),(49,50)],'ink')
        poly(d,[(51,48),(56,47),(54,57),(50,65),(50,74),(47,75),(48,61)],'blue')
        line(d,[(51,49),(50,56),(48,62),(48,70)],'mid',2)
        box(d,(47,73,51,76),'cuff')
        poly(d,[(47,77),(51,77),(52,81),(51,85),(48,86),(46,83)],'shade')
        box(d,(47,78,50,82),'warm');line(d,[(48,83),(50,83)],'skinlit')
        poly(d,[(73,45),(78,47),(81,56),(84,65),(83,78),(78,80),(76,76),(77,65),(74,57)],'ink')
        poly(d,[(75,48),(78,50),(79,57),(82,65),(81,76),(78,76),(79,64)],'navy')
        line(d,[(76,50),(77,56),(80,64)],'blue',2);box(d,(78,75,82,78),'mid')
        poly(d,[(78,79),(82,79),(83,83),(81,87),(78,86),(77,83)],'shade')
        box(d,(78,80,81,83),'skin');line(d,[(78,80),(80,80)],'warm')
        poly(d,[(59,43),(68,42),(75,46),(76,59),(74,66),(77,79),(70,82),(65,79),(60,82),(53,79),(55,65),(53,53),(54,47)],'ink')
        poly(d,[(58,46),(65,45),(71,46),(73,53),(72,64),(74,77),(68,79),(64,76),(58,79),(55,77),(57,64),(55,53)],'blue')
        poly(d,[(57,49),(61,47),(64,53),(62,63),(59,69),(57,73),(58,62)],'mid')
        poly(d,[(65,49),(70,47),(72,54),(70,64),(73,76),(68,78),(65,74)],'navy')
        line(d,[(60,46),(65,53),(61,62),(58,65)],'seam')
        line(d,[(68,46),(65,53),(67,58)],'deep')
        line(d,[(59,70),(57,76),(61,75)],'mid')
        line(d,[(66,69),(69,74),(70,77)],'blue')
        poly(d,[(55,64),(63,65),(73,64),(74,68),(64,70),(55,68)],'sashdark')
        line(d,[(56,65),(64,66),(72,65)],'sashlit',2)
        box(d,(62,66,65,69),'sash');poly(d,[(64,69),(67,69),(69,77),(66,76)],'sash')
        line(d,[(66,70),(67,74)],'sashlit')
        # Neck emerges from open crossover, not a head pasted on a rectangle.
        poly(d,[(61,39),(67,39),(68,45),(65,49),(61,46)],'shade')
        poly(d,[(62,40),(66,40),(66,45),(64,47),(62,45)],'skin')
        poly(d,[(59,31),(60,29),(67,29),(70,31),(70,35),(68,38),(64,40),(60,38),(58,35)],'shade')
        poly(d,[(60,32),(67,31),(69,33),(68,37),(65,39),(61,37)],'warm')
        box(d,(59,34,60,36),'skin');box(d,(69,34,70,36),'skin')
        box(d,(62,34,62,34),'eye');box(d,(67,34,67,34),'eye')
        line(d,[(65,34),(65,36),(66,36)],'skinlit');line(d,[(63,37),(66,37)],'shade')
        poly(d,[(58,31),(59,29),(62,28),(67,29),(70,30),(70,33),(65,32),(60,33)],'hair')
        poly(d,[(59,30),(62,29),(67,30),(69,31),(63,30),(59,32)],'wrap')
        line(d,[(60,29),(64,29),(67,30)],'wraplit')
    elif view=='SE':
        # Independent oblique contours and occlusion. No transformed S pixels.
        poly(d,[(58,73),(67,73),(68,88),(64,99),(62,108),(56,110),(54,108),(58,94)],'ink')
        poly(d,[(60,78),(65,77),(65,88),(61,100),(60,107),(56,108),(60,92)],'pant')
        line(d,[(62,80),(63,89),(59,101)],'pantmid',2)
        poly(d,[(67,74),(76,73),(78,84),(75,96),(75,108),(71,111),(67,109),(68,96)],'ink')
        poly(d,[(68,77),(74,76),(76,85),(73,97),(73,108),(69,108),(70,94)],'pantmid')
        line(d,[(69,79),(72,88),(70,99)],'pantlit',2)
        poly(d,[(56,107),(61,107),(65,109),(66,111),(56,111),(54,110)],'shade')
        line(d,[(56,109),(63,110)],'skin',2)
        poly(d,[(69,108),(73,108),(79,111),(79,113),(69,113),(67,111)],'shade')
        poly(d,[(69,109),(73,110),(77,112),(69,112)],'warm')
        poly(d,[(54,45),(60,45),(59,57),(55,65),(56,77),(51,80),(48,77),(49,63),(50,52)],'ink')
        poly(d,[(53,49),(57,48),(55,60),(52,65),(53,75),(50,76),(51,62)],'navy')
        box(d,(50,75,54,78),'mid');poly(d,[(50,79),(54,79),(56,82),(55,86),(51,86),(49,83)],'shade')
        box(d,(51,80,54,83),'skin')
        poly(d,[(58,43),(66,42),(75,46),(77,54),(74,65),(77,78),(70,81),(61,80),(55,77),(56,65),(53,53)],'ink')
        poly(d,[(58,47),(65,45),(72,47),(74,53),(71,64),(74,76),(69,79),(62,78),(57,76),(59,64),(56,53)],'blue')
        poly(d,[(58,48),(63,46),(66,49),(63,61),(59,65),(59,56)],'mid')
        poly(d,[(69,48),(73,50),(73,55),(70,65),(73,76),(68,78),(66,69),(67,59)],'navy')
        line(d,[(64,46),(68,51),(64,60),(61,64)],'seam')
        line(d,[(60,69),(59,75),(63,76)],'mid');line(d,[(67,71),(70,76)],'blue')
        poly(d,[(57,64),(66,66),(74,64),(75,68),(66,70),(57,68)],'sashdark')
        line(d,[(58,65),(66,67),(73,65)],'sashlit',2)
        box(d,(69,66,72,69),'sash');poly(d,[(71,69),(73,69),(75,76),(72,76)],'sash')
        # Near shoulder overlaps the side seam, natural bent elbow.
        poly(d,[(71,47),(76,48),(80,54),(81,62),(79,70),(79,79),(74,81),(72,78),(74,68),(74,60),(70,54)],'ink')
        poly(d,[(73,49),(76,51),(78,56),(79,62),(76,70),(77,77),(74,78),(75,68),(75,59),(72,54)],'blue')
        line(d,[(73,50),(75,53),(76,58),(77,62)],'mid',2)
        line(d,[(77,65),(75,70),(75,74)],'navy',2);box(d,(74,77,78,79),'cuff')
        poly(d,[(74,80),(78,80),(80,83),(78,87),(75,87),(73,84)],'shade')
        box(d,(74,81,77,84),'warm');box(d,(75,85,77,85),'skin')
        poly(d,[(62,39),(68,38),(71,44),(67,48),(63,45)],'shade')
        poly(d,[(65,40),(68,40),(69,44),(67,46),(65,44)],'skin')
        poly(d,[(60,31),(64,29),(69,30),(72,32),(72,34),(73,36),(72,37),(71,39),(67,40),(63,38),(60,35)],'shade')
        poly(d,[(64,32),(69,32),(71,34),(73,36),(71,37),(70,38),(67,39),(64,36)],'warm')
        box(d,(62,34,63,36),'skin');box(d,(66,34,66,34),'eye');box(d,(70,34,70,34),'eye');box(d,(71,36,72,36),'skinlit')
        line(d,[(67,38),(70,38)],'shade')
        poly(d,[(59,31),(61,29),(64,28),(69,29),(72,31),(72,33),(67,32),(65,34),(61,34)],'hair')
        poly(d,[(60,30),(63,28),(68,29),(70,31),(65,31),(61,33)],'wrap')
        line(d,[(62,29),(66,29),(69,30)],'wraplit');box(d,(59,32,61,35),'wrap')
    else:
        poly(d,[(55,74),(64,75),(65,90),(62,103),(62,111),(56,112),(54,110),(56,96)],'ink')
        poly(d,[(66,75),(75,74),(77,88),(74,100),(75,110),(69,112),(67,110),(68,95)],'ink')
        poly(d,[(57,78),(62,79),(63,89),(60,102),(60,109),(56,109),(58,96)],'pantmid')
        poly(d,[(68,79),(74,78),(75,88),(72,100),(73,109),(69,110),(70,94)],'pant')
        line(d,[(58,83),(60,89),(58,101)],'pantlit',2);line(d,[(70,84),(72,89),(71,101)],'pantmid',2)
        box(d,(56,109,61,111),'skin');box(d,(69,109,74,111),'shade')
        line(d,[(56,112),(61,112)],'shade');line(d,[(69,112),(74,112)],'shade')
        poly(d,[(54,44),(60,45),(57,57),(52,64),(51,77),(46,79),(44,75),(46,60),(49,49)],'ink')
        poly(d,[(51,48),(56,47),(54,57),(49,64),(49,75),(46,76),(48,61)],'blue')
        line(d,[(51,49),(50,56),(47,64),(47,71)],'mid',2);box(d,(46,75,50,78),'cuff')
        poly(d,[(46,79),(50,78),(52,82),(50,86),(47,86),(45,83)],'shade');box(d,(46,79,49,83),'skin')
        poly(d,[(73,44),(78,47),(81,58),(84,65),(83,77),(78,80),(76,77),(78,65),(74,57)],'ink')
        poly(d,[(75,48),(78,51),(79,59),(82,65),(81,76),(78,77),(80,64)],'navy')
        line(d,[(76,51),(77,58),(80,64)],'blue',2);box(d,(78,76,82,79),'mid')
        poly(d,[(78,80),(82,80),(83,83),(81,87),(78,86),(77,83)],'shade');box(d,(78,80,81,83),'skin')
        poly(d,[(59,42),(68,42),(75,45),(77,54),(74,66),(77,79),(69,82),(63,80),(57,82),(53,78),(55,65),(53,54),(54,46)],'ink')
        poly(d,[(58,45),(65,44),(71,45),(74,49),(73,57),(71,65),(74,77),(68,79),(63,77),(58,79),(55,76),(58,64),(56,54),(55,49)],'blue')
        poly(d,[(57,48),(61,46),(65,48),(68,46),(72,47),(72,51),(65,53),(58,51)],'mid')
        poly(d,[(66,53),(71,51),(72,58),(70,65),(72,76),(68,78),(65,74)],'navy')
        line(d,[(57,52),(62,54),(64,61)],'lit');line(d,[(64,54),(65,62)],'navy')
        line(d,[(59,69),(57,75),(60,76)],'mid');line(d,[(65,69),(68,76)],'blue')
        poly(d,[(56,64),(64,66),(73,64),(74,68),(64,70),(55,68)],'sashdark')
        line(d,[(57,65),(64,67),(72,65)],'sashlit',2)
        poly(d,[(61,38),(68,38),(69,43),(65,46),(61,43)],'shade')
        poly(d,[(59,31),(61,29),(67,29),(70,31),(70,36),(68,39),(61,39),(58,36)],'hair')
        poly(d,[(60,30),(63,28),(67,29),(69,31),(69,34),(63,35),(59,33)],'wrap')
        line(d,[(61,29),(65,28),(68,30)],'wraplit')
        poly(d,[(60,35),(67,35),(70,36),(68,39),(64,38),(61,40),(59,38)],'deep')
        box(d,(63,37,66,40),'wrap');line(d,[(64,40),(62,45),(60,46)],'wrap',2)
        line(d,[(65,41),(67,45)],'wraplit')
        box(d,(58,35,59,37),'skin');box(d,(69,35,70,37),'shade')
    return im

def house():
    im,d=canvas((520,430));r=random.Random(538)
    # Native 2:1 wall axes. Person84px, door87px, same overhead light.
    poly(d,[(47,283),(270,171),(477,275),(270,392)],'#53614b')
    poly(d,[(56,280),(267,178),(466,276),(270,385)],'#a69b77')
    poly(d,[(56,280),(270,385),(270,395),(56,290)],'#776d52')
    poly(d,[(270,385),(466,276),(466,287),(270,395)],'#615b47')
    # Front wall and side, full fill before joinery. Never bare vector outlines.
    front=[(65,180),(270,282),(270,371),(65,269)]
    side=[(270,282),(453,190),(453,280),(270,371)]
    poly(d,front,'#ac986b');poly(d,side,'#7d7252')
    # Fine woven bamboo panels in local perspective with exact clipping.
    for pts,base,shade,light in [(front,'#ac986b','#958057','#bfac7d'),(side,'#7d7252','#706344','#998965')]:
        mask=Image.new('1',im.size);ImageDraw.Draw(mask).polygon(pts,fill=1)
        layer=Image.new('RGBA',im.size);ld=ImageDraw.Draw(layer)
        for x in range(60,460,7):line(ld,[(x,140),(x,390)],shade)
        for y in range(140,400,5):line(ld,[(50,y),(460,y+205 if pts==front else y-205)],light)
        im.alpha_composite(Image.composite(layer,Image.new('RGBA',im.size),mask))
    d=ImageDraw.Draw(im)
    # Main dark entrance reads at actual size, modest wood plank doors.
    poly(d,[(147,238),(195,262),(195,331),(147,308)],'#34352b')
    poly(d,[(151,243),(169,252),(169,316),(151,307)],'#66553b')
    for x in range(153,170,5):line(d,[(x,245+(x-153)//2),(x,307+(x-153)//2)],'#927346')
    poly(d,[(149,235),(198,260),(198,334),(193,331),(193,264),(149,242)],'#54432f')
    line(d,[(149,238),(194,261)],'#c0a26a',2)
    box(d,(166,284,167,286),'#c6ad70')
    # Side window, slats use the wall's NE axis.
    poly(d,[(333,274),(406,237),(406,273),(333,310)],'#374035')
    for x in range(338,406,9):line(d,[(x,275-(x-338)//2),(x,304-(x-338)//2)],'#b09a6d',2)
    line(d,[(333,274),(406,237)],'#bba372',3)
    # Posts, sill, lintel, brackets: structural detail and material volume.
    for x,y in [(65,180),(128,211),(206,250),(270,282),(453,190)]:
        poly(d,[(x-3,y),(x+3,y+2),(x+3,y+90),(x-3,y+88)],'#54452e')
        line(d,[(x-2,y+3),(x-2,y+86)],'#c19e61',2)
    line(d,[(65,267),(270,370),(453,278)],'#4b442f',4)
    line(d,[(67,265),(270,367),(451,276)],'#baa071')
    # Right gable: vertical woven plane below roof, not a second roof slope.
    poly(d,[(270,287),(375,148),(467,191)],'#8f7c50')
    for x in range(300,455,6):
        top=150+(375-x)*145/105 if x<375 else 150+(x-375)*40/105
        bottom=287-(x-270)/2
        if top<bottom:line(d,[(x,int(top)+4),(x,int(bottom)-3)],'#7b6944')
    line(d,[(375,153),(375,231)],'#5a4e32',4)
    line(d,[(328,210),(422,211)],'#6d5c3a',3)
    # Two thatch slopes plus clean angular ridge; bundles clipped to roof mask.
    near=[(40,180),(145,35),(375,150),(270,295)]
    far=[(145,35),(250,75),(480,190),(375,150)]
    poly(d,far,'#99814b');poly(d,near,'#b19557')
    mask=Image.new('1',im.size);ImageDraw.Draw(mask).polygon(near,fill=1)
    layer=Image.new('RGBA',im.size);ld=ImageDraw.Draw(layer)
    # Rows of staggered straw bundles: downhill(-105,+145), ridge(+230,+115).
    for band in range(12):
        for k in range(72):
            x=145+k*4-band*9+r.choice([-1,0,1]);y=36+k*2+band*12+r.randrange(-3,4)
            c=['#c3a568','#b89b5e','#cdb176','#a88c50','#967b42'][(k+3*band)%5]
            length=r.choice([7,11,15,19]);line(ld,[(x,y),(x-length//2,y+length)],c)
            if (k+band)%4==0:line(ld,[(x+1,y),(x+1-length//2,y+length-2)],'#d1b674')
    im.alpha_composite(Image.composite(layer,Image.new('RGBA',im.size),mask));d=ImageDraw.Draw(im)
    line(d,[(144,34),(375,149)],'#ddbd79',5)
    line(d,[(145,33),(375,148)],'#7e693b',2)
    line(d,[(39,180),(270,297),(481,191)],'#695633',5)
    line(d,[(41,178),(270,293),(479,189)],'#dfbc74',2)
    for k in range(35):
        x=43+k*6;y=183+k*3;line(d,[(x,y),(x-2,y+r.choice([3,4,6]))],'#9d8249')
    for k in range(34):
        x=278+k*6;y=294-k*3;line(d,[(x,y),(x,y+3)],'#a58b51')
    # Porch step, threshold and jar complement readable dwelling scale.
    poly(d,[(143,311),(196,337),(212,329),(160,303)],'#c8b590')
    poly(d,[(143,311),(196,337),(196,344),(143,317)],'#897d5b')
    poly(d,[(196,337),(212,329),(212,335),(196,344)],'#70694c')
    poly(d,[(405,300),(411,294),(422,293),(430,300),(433,314),(428,327),(415,331),(406,324),(402,311)],'#574b34')
    poly(d,[(407,302),(412,298),(421,298),(427,303),(429,314),(425,323),(415,327),(409,320),(406,311)],'#99724a')
    line(d,[(409,305),(409,314),(413,320)],'#bd925c',2)
    poly(d,[(411,294),(416,291),(424,293),(427,296),(420,300),(412,298)],'#c6aa78')
    poly(d,[(414,294),(420,293),(424,296),(419,298),(414,297)],'#494130')
    return im

def tree():
    im,d=canvas((280,290));r=random.Random(901)
    # Root buttresses and a crooked, lit trunk under several leaf masses.
    poly(d,[(131,144),(154,140),(160,217),(157,247),(171,265),(158,270),(146,257),(135,271),(123,268),(134,249),(130,216)],'#354739')
    poly(d,[(137,145),(148,145),(153,217),(149,247),(157,261),(148,256),(139,263),(142,244),(137,217)],'#806b45')
    line(d,[(139,160),(140,211),(145,241)],'#aa8a53',3)
    line(d,[(153,224),(156,248),(165,263)],'#514e37',3)
    poly(d,[(139,199),(113,167),(104,127),(111,123),(126,157),(145,178)],'#645b3b')
    poly(d,[(151,187),(173,151),(190,139),(193,146),(178,164),(158,207)],'#625b3d')
    # Hand-directed crown silhouette; clusters describe layered planes rather than circles.
    shape=[(25,119),(19,105),(28,95),(25,80),(38,72),(38,57),(55,51),(66,36),(86,36),(98,22),(120,26),(138,16),(155,22),(174,22),(187,34),(207,36),(211,48),(233,55),(230,69),(249,83),(245,99),(258,110),(248,129),(253,142),(236,155),(221,153),(211,170),(189,170),(176,181),(157,174),(137,184),(119,176),(98,179),(85,165),(65,164),(57,151),(39,151),(39,135)]
    poly(d,shape,'#304d3e')
    planes=[([(29,100),(42,78),(64,75),(69,59),(91,53),(111,44),(139,48),(147,70),(125,88),(106,93),(94,118),(64,127),(45,119)],'#618052'), ([(106,40),(123,30),(144,24),(164,30),(182,29),(198,43),(198,58),(178,70),(156,70),(141,58)],'#789059'), ([(136,89),(156,72),(185,67),(204,53),(223,64),(224,82),(242,91),(232,112),(211,120),(202,136),(176,138),(163,120)],'#4d714a'), ([(57,129),(85,117),(106,100),(129,102),(145,125),(136,150),(119,163),(92,158),(78,146),(61,148)],'#486a45'), ([(143,145),(163,129),(184,139),(209,135),(226,129),(239,140),(225,151),(210,151),(202,166),(182,161),(173,172),(153,163)],'#3d6044')]
    for pts,c in planes:poly(d,pts,c)
    # Leaf clusters placed on lit upper edges and shaded lower branches.
    for x,y in [(48,86),(61,68),(83,58),(101,53),(124,35),(148,32),(174,36),(191,48),(156,81),(180,79),(207,71),(218,90),(224,112),(175,104),(108,111),(89,132),(112,137),(151,144),(190,147),(63,110)]:
        c='#95a365' if y<65 else '#749056'
        poly(d,[(x-7,y),(x-4,y-3),(x+2,y-3),(x+5,y),(x+1,y+2),(x-5,y+2)],c)
        line(d,[(x-3,y-2),(x+1,y-2)],'#a2ae72' if y<65 else '#839b5e')
        for dx,dy in [(6,4),(-8,7),(1,10)]:
            line(d,[(x+dx,y+dy),(x+dx+3,y+dy-1)],'#5c7e4d')
    crown=im.copy()
    for cx,cy in [(44,97),(62,71),(86,53),(115,46),(145,36),(173,40),(194,52),(214,72),(233,97),(217,120),(192,135),(174,153),(151,156),(127,157),(103,143),(81,143),(57,131),(95,96),(126,82),(151,98),(178,88),(182,116),(126,125)]:
        for j in range(16):
            dx=r.randrange(-16,17);dy=r.randrange(-9,12);x=cx+dx;y=cy+dy
            if crown.getpixel((x,y))[3]==0:continue
            c=['#6b8753','#76915a','#87a064','#597c4e','#4d714a'][j%5]
            poly(d,[(x-3,y),(x-1,y-2),(x+3,y-2),(x+5,y),(x+2,y+2),(x-2,y+2)],c)
            if j%3==0:line(d,[(x-1,y-2),(x+2,y-2)],'#9baa6e')
    return im

def tools():
    im,d=canvas((128,128))
    line(d,[(32,101),(53,45)],'#3b3c32',5);line(d,[(32,101),(53,45)],'#987349',3)
    line(d,[(32,99),(51,47)],'#c0a06a')
    poly(d,[(48,44),(54,43),(68,47),(69,56),(61,59),(53,52),(48,51)],'#2b3c3c')
    poly(d,[(55,45),(66,49),(67,55),(61,57),(54,51)],'#91a7a5')
    line(d,[(66,49),(67,55),(62,57)],'#c3ccba')
    poly(d,[(73,84),(82,79),(96,82),(101,92),(97,107),(84,113),(75,108),(71,96)],'#554d34')
    poly(d,[(74,89),(82,84),(95,86),(98,94),(95,104),(84,110),(77,106)],'#ac8b50')
    for y in [91,96,101,106]:line(d,[(76,y),(84,y+3),(97,y-4)],'#d2b36c')
    for x in [78,83,89,94]:line(d,[(x,87),(x+1,105)],'#82653c')
    line(d,[(76,89),(76,83),(81,77),(91,78),(96,84)],'#c0a064',2)
    return im

def ground():
    # Native1680x940 landscape; camera crops at1:1 for both review resolutions.
    im=Image.new('RGBA',(2000,1200),'#748363');d=ImageDraw.Draw(im);r=random.Random(538)
    # Muted broad grass planes give terrain relief without tiling outlines.
    for pts,c in [([(0,0),(790,0),(1070,210),(711,399),(286,339),(0,456)],'#7c8966'), ([(0,625),(376,462),(727,588),(936,910),(371,1200),(0,1200)],'#7b8966'), ([(860,0),(2000,0),(2000,1200),(1540,1200),(1180,730),(1270,370)],'#6b7c5d')]:poly(d,pts,c)
    # Stream has a true irregular bank with sediment, wet soil and inset water.
    shore=[(1458,-10),(1460,112),(1424,217),(1439,319),(1376,416),(1393,503),(1341,584),(1348,687),(1273,792),(1250,900),(1181,1021),(1202,1200),(2000,1200),(2000,-10)]
    poly(d,shore,'#9c976f')
    wet=[(1479,-10),(1480,117),(1445,217),(1461,322),(1397,422),(1417,503),(1363,592),(1372,694),(1296,802),(1278,910),(1207,1026),(1228,1200),(2000,1200),(2000,-10)]
    poly(d,wet,'#617f72')
    water=[(1490,-10),(1493,120),(1458,218),(1475,322),(1410,425),(1430,505),(1377,594),(1387,699),(1311,809),(1294,916),(1224,1028),(1245,1200),(2000,1200),(2000,-10)]
    poly(d,water,'#477c7b')
    poly(d,[(1641,0),(1570,207),(1613,408),(1488,611),(1501,792),(1398,1045),(1451,1200),(2000,1200),(2000,0)],'#407373')
    for i in range(420):
        x=r.randrange(1240,2000);y=r.randrange(1200)
        if im.getpixel((x,y))[:3] in [(71,124,123),(64,115,115)]:
            c=r.choice(['#558a84','#5b9189','#3b6e70']);line(d,[(x,y),(x+10,y),(x+13,y-1),(x+21,y-1)],c)
    # Winding compacted path connecting the house and riverside.
    path=[(-10,834),(225,746),(406,652),(562,588),(691,569),(815,584),(984,653),(1174,726),(1332,755),(1320,789),(1163,779),(964,706),(800,640),(683,628),(580,640),(426,703),(250,796),(-10,893)]
    poly(d,path,'#9b9670')
    poly(d,[(-10,846),(233,757),(414,666),(570,604),(687,585),(811,602),(979,670),(1172,746),(1324,768),(1319,779),(1166,764),(972,693),(805,625),(685,614),(576,627),(421,689),(243,783),(-10,880)],'#b1a17b')
    for i in range(11000):
        x=r.randrange(2000);y=r.randrange(1200);base=im.getpixel((x,y))[:3]
        if base in [(116,131,99),(124,137,102),(123,137,102),(107,124,93)]:
            c=r.choice(['#7d8d68','#687b5a','#8c966e','#71835d'])
            if i%5==0:
                line(d,[(x-2,y),(x,y-4),(x,y+1),(x+3,y-2)],c)
            else:line(d,[(x,y),(x+r.choice([2,3,4]),y)],c)
        elif base==(177,161,123) and i%3==0:
            line(d,[(x,y),(x+3,y)],r.choice(['#a29370','#c0af88','#998c69']))
    # Hand-placed river margin reeds, bank stones and small flowers.
    for x,y in [(1430,342),(1385,460),(1350,631),(1283,830),(1240,953),(1328,747)]:
        for dx,dy in [(-8,0),(-4,-2),(0,0),(5,2),(9,-1)]:
            line(d,[(x+dx,y),(x+dx-3,y-17+dy)],'#4d6d4b',2)
            line(d,[(x+dx,y),(x+dx+4,y-13+dy)],'#94a16b')
    for x,y in [(1264,811),(1347,711),(1365,564),(1419,389),(1437,245),(1215,1050)]:
        poly(d,[(x-9,y),(x-7,y-5),(x,y-8),(x+8,y-3),(x+9,y+2),(x+1,y+5)],'#6c7762')
        poly(d,[(x-7,y-5),(x,y-8),(x+8,y-3),(x,y)],'#a7aa83')
    for x,y in [(521,719),(488,694),(1191,570),(1046,464),(733,850),(323,521)]:
        for dx,dy in [(0,0),(5,3),(-4,5)]:
            line(d,[(x+dx,y+dy+4),(x+dx,y+dy-2)],'#647d52');box(d,(x+dx-1,y+dy-3,x+dx+1,y+dy-2),'#cebc79')
    return im

def save(im,name):
    (BASE/'raw').mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    im.save(BASE/'raw'/name);im.save(OUT/name)

def main():
    for v in ['S','SE','N']:save(worker(v),'worker-'+v+'.png')
    for n,fn in [('house',house),('tree',tree),('tools',tools),('ground',ground)]:save(fn(),n+'.png')
    sheet,d=canvas((768,300));d.rectangle((0,0,767,299),fill='#e1d5b5')
    for i,v in enumerate(['S','SE','N']):
        w=worker(v);sheet.alpha_composite(w,(i*256+22,10))
        # Explicit nearest-neighbor viewing derivative, never a source frame.
        silhouette=Image.new('RGBA',w.size,'#263d39');silhouette.putalpha(w.getchannel('A'));sheet.alpha_composite(silhouette,(i*256+130,10))
    sheet=sheet.crop((0,0,768,148));save(sheet,'worker-study.png')
    close=Image.new('RGBA',(768,256),'#e1d5b5')
    for i,v in enumerate(['S','SE','N']):close.alpha_composite(worker(v).resize((256,256),Image.Resampling.NEAREST),(i*256,0))
    save(close,'worker-closeup-2x.png')
    files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (BASE/'raw').glob('*.png')}
    manifest={'schema':'rds-native-scene-study/v1','status':'OWNER_REVIEW_PENDING','provenance':{'kind':'native-raster','recipe':{'path':str(Path(__file__).relative_to(ROOT)),'sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},'framePlan':{'path':str((BASE/'authoring/frame-plan.json').relative_to(ROOT)),'sha256':hashlib.sha256((BASE/'authoring/frame-plan.json').read_bytes()).hexdigest()},'providerCalls':0,'callTokens':None,'sources':[{'path':str((BASE/'raw'/n).relative_to(ROOT)),'sha256':s} for n,s in sorted(files.items())]},'worker':{'cellSize':128,'renderSize':[128,128],'anchor':[64,112],'directions':['S','SE','N'],'frameCount':3,'animation':False,'palette':list(P.values())},'review':{'visual':'UNKNOWN','motion':'NOT_STARTED','runtime':'UNKNOWN','owner':'PENDING','release':'NOT_REQUESTED'}}
    (BASE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'outputs':len(files),'sourceMethod':'native-raster','providerCalls':0,'workerPalette':len(P)}))
if __name__=='__main__':main()
