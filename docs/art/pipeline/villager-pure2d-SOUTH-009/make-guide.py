#!/usr/bin/env python3
"""Hand-authored pixel-space contact annotation; AUTHORING_ONLY, no source edit."""
import hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageChops
ROOT=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha')
OUT=Path(__file__).parent
refs={
 'canonicalSouth':(ROOT/'docs/art/characters/villager-neutral-D01-screen-South-007/raw.png','identity/material/camera authority only'),
 'heldF4EditTarget':(ROOT/'docs/art/pipeline/villager-pure2d-SOUTH-008/F4-right-contact-02/raw.png','held correction target, NOT selected continuity neighbor'),
 'selectedF0Comparison':(Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha-art-lease/villager-walk-SOUTH-007/walk/keys/F00-left-contact-01/raw.png'),'optional comparison only; not edit target; PASS_KEY_CANDIDATE_ONLY')}
def sha(data):return hashlib.sha256(data).hexdigest()
records={}
for role,(p,meaning) in refs.items():
 im=Image.open(p).convert('RGBA')
 assert im.size==(1254,1254)
 records[role]=dict(path=str(p),role=meaning,encodedSha256=sha(p.read_bytes()),rgbaSha256=sha(im.tobytes()),dimensions=list(im.size))
source=Image.open(refs['heldF4EditTarget'][0]).convert('RGBA')
# Grayscale silhouette perimeter only; no source RGB/color underlay or source mutation.
mask=source.getchannel('A').point(lambda p:255 if p>=32 else 0)
edge=ImageChops.subtract(mask.filter(ImageFilter.MaxFilter(3)),mask.filter(ImageFilter.MinFilter(3)))
guide=Image.new('RGB',(1254,1254),'white');guide.paste((195,195,195),(0,0),edge)
d=ImageDraw.Draw(guide)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17)
small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
def text(x,y,s): d.text((x,y),s,fill='black',font=font)
def leader(points,label,xy):d.line(points,fill='black',width=2);text(*xy,label)
text(22,20,'AUTHORING_ONLY - F4 LEFT trailing contact correction')
text(22,46,'Hand 2D estimates (+/-18 px); NOT source art or measured foot-lock')
text(22,72,'1254 canvas | fixed pivot [654,1140] | referenceHeight 1130')
text(22,100,'Gray outline = held F4 context; black foot = proposed correction only')
# Keep receiving RIGHT sole/location unchanged.
d.line([(480,1193),(575,1193)],fill='black',width=3)
leader([(530,1193),(395,1152),(80,1152)],'RIGHT receiving sole ~530,1193: KEEP', (22,1122))
# Rear floor depth is a local authoring contact cue, not a physical projected plane.
for x in range(657,862,18):d.line([(x,1093),(x+10,1093)],fill=(90,90,90),width=2)
leader([(837,1093),(939,1124)],'Rear toe floor depth ~y1093',(907,1130))
# Proposed complete ankle/heel-to-forefoot outline with toe bend at ball.
# Black outlines are deliberately approximate, not detachable limb artwork.
outline=[(710,993),(729,993),(730,1010),(723,1032),(728,1048),(744,1069),(763,1080),(779,1087),(780,1093),(770,1097),(753,1093),(746,1080),(735,1066),(711,1053),(705,1044),(710,1024),(710,993)]
d.line(outline,fill='black',width=3)
d.line([(716,1045),(735,1066),(753,1090),(764,1093)],fill='black',width=4)
d.line([(748,1080),(756,1084),(760,1091)],fill='black',width=2)
for pt in [(720,1008),(716,1045),(764,1093)]:d.ellipse((pt[0]-4,pt[1]-4,pt[0]+4,pt[1]+4),outline='black',width=2)
leader([(720,1008),(920,962)],'LEFT ankle ~720,1008',(932,947))
leader([(716,1045),(920,1007)],'Raised heel ~716,1045',(932,994))
leader([(764,1093),(940,1070)],'Planted toe ~764,1093',(945,1054))
leader([(756,1084),(894,1035)],'Toe/ball bend',(935,1026))
text(22,1220,'Preserve all other placement; this guide contains no appearance authority.')
guide.save(OUT/'F4-left-trailing-contact-guide.png')
landmarks=dict(schema='pure2d-hand-contact-guide/v1',status='AUTHORING_ONLY_READY_PENDING_PARENT_REVIEW',frame='F4',direction={'screen':'South','engine':'D01','world':'SE'},profile={'model':'gpt-6.1-sol','reasoning_effort':'low'},canvas=[1254,1254],pivot=[654,1140],referenceHeight=1130,references=records,
 confidence='Manual visual estimates from actual full held F4/canonical/F0; targets hand-authored, not sealed measurements, projection or contact acceptance.',uncertaintyPx=18,
 observedHeldF4={'trailingAnatomicalLEFTViewerRIGHT':{'toeApprox':[735,1093],'rearHeelApprox':[687,990],'note':'Rear heel estimate refers to high back sandal region; heel center/sole landmark is anatomically uncertain. Heel is already raised in silhouette; toe-ground contact remains ambiguous and no floor/contact is established by raw transparency.'},'receivingAnatomicalRIGHTViewerLEFT':{'soleApprox':[530,1193],'instruction':'preserve exact source placement and shape'}},
 target={'trailingAnatomicalLEFTViewerRIGHT':{'ankleApprox':[720,1008],'raisedHeelApprox':[716,1045],'plantedToeApprox':[764,1093],'ballBendApprox':[756,1084],'authoredRanges':{'ankle':[[710,995],[730,1020]],'heel':[[700,1035],[725,1060]],'toe':[[750,1090],[778,1100]]},'solePathApprox':[[716,1045],[735,1066],[753,1090],[764,1093]],'outlineApprox':outline,'localFloorDepthYApprox':1093,'heelRisePixelsApprox':48,'instruction':'Coherent short toe-grounded push-off: heel behind/up-left of toe; flex toe/forefoot toward local floor. Preserve upper leg/knee and whole frame; allow only local lower wrap/ankle transition needed for coherent sandal.'}},
 priorGuideCorrection='Prior v2 toe[811,1091]/heel[857,1064] was an independent estimate. Actual sandal points toward down/right; placing heel to right of toe risks reversing foot orientation. New target keeps heel up-left of toe. Parent heel7241060/toe7781093/ankle7201045 were starting estimates. Actual calf and independent native review favor ankle995..1020 instead of forcing it45px down; ranges above preserve orientation and reduce broad floating-looking sole. No rigid pixel pins.',
 knownUncertainty='Rear toe depth y1093 is an authored local ground cue consistent with trailing depth, not a global flat baseline; receiving y1193 remains untouched. No floor exists in transparent raw. Visual parent review must judge floor depth, anatomy and contact; no world foot-lock or final acceptance is asserted.',
 sourceMutated=False,imageCalls=0,no3D=True)
(OUT/'F4-contact-landmarks.json').write_text(json.dumps(landmarks,indent=2)+'\n')
