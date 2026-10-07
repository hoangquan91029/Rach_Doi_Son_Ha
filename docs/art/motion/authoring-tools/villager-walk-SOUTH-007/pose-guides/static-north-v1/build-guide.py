"""MODEL_ONLY back-facing static pose guide. No source art pixels or motion claim."""
from pathlib import Path
import json, hashlib, math

p=Path(__file__).parent
root=[654,1140]
points={}
for side,x in [('LEFT',541),('RIGHT',767)]:
 for name,y in [('hip',745),('knee',932),('ankle',1092),('heel',1154),('toe',1079)]:
  points[side+'_'+name]=[x,y]
 points[side+'_shoulder']=[x-35 if side=='LEFT' else x+35,345]
 points[side+'_elbow']=[x-55 if side=='LEFT' else x+55,548]
 points[side+'_wrist']=[x-62 if side=='LEFT' else x+62,710]
plan={'status':'MODEL_ONLY_NON_ART_STATIC_GUIDE','canvas':[1254,1254],'root':root,'worldScale':38/1254,
 'direction':{'screen':'NORTH_UP','engine':'D05','world':'NW','worldForward':[-1,-1]},
 'camera':{'projection':'dimetric guide hypothesis','groundDiamondRatio':[2,1],'elevationDegrees':26.565},
 'anatomicalOwnership':'Back-facing: LEFT is viewer-left, RIGHT viewer-right. No mirrored character art.',
 'sourceReference':{'path':'../../identity/south-neutral-reference/raw.png','sha256':'68a7fb9a71ae614f7c01432b1270e7a25071975667cfdf082ae02326d97678db','usage':'Overall proportions only; no traced/copied/extracted pixels'},
 'points':points,'constraints':['Entire head, torso, pelvis and feet face screen-up, back visible','No facial eyes/nose or front tunic wrap neckline','Rear hat, short nape, back sleeves/coat/sash, trouser rear and sandal heels remain recognizable','Both foot longitudinal axes point toward screen-up','Equal authored leg lengths, one6541140ground anchor, no bbox fitting'],
 'footAxes':{side:[0,-75] for side in ['LEFT','RIGHT']},
 'legSegmentLengths':{side:[math.dist(points[side+'_hip'],points[side+'_knee']),math.dist(points[side+'_knee'],points[side+'_ankle'])] for side in ['LEFT','RIGHT']},
 'finishedArt':False,'motionQualified':False,'runtimeIntegrated':False}
(p/'coordinate-plan.json').write_text(json.dumps(plan,indent=2)+'\n')

def svg(qa=False):
 e=['<rect width="1254" height="1254" fill="#f0eee5"/>','<text x="32" y="32" font-size="20" fill="#263c37">MODEL_ONLY / NON_ART — STATIC NORTH BACK — D05 / world NW</text>',
 '<path d="M430 1140L654 1028L878 1140L654 1252Z" fill="none" stroke="#a9b6ad" stroke-dasharray="8 8"/>','<path d="M644 1140h20M654 1130v20" stroke="#617b70" stroke-width="2"/>']
 for side in ['LEFT','RIGHT']:
  for a,b,w in [('hip','knee',86),('knee','ankle',54),('shoulder','elbow',76),('elbow','wrist',43)]:
   pa,pb=points[side+'_'+a],points[side+'_'+b]
   e.append(f'<path d="M{pa[0]} {pa[1]}L{pb[0]} {pb[1]}" stroke="#8fa59b" stroke-width="{w}" stroke-linecap="round"/>')
  x=points[side+'_heel'][0]
  e.append(f'<path d="M{x-34} 1154L{x-28} 1092Q{x} 1066 {x+28} 1092L{x+34} 1154Q{x} 1168 {x-34} 1154Z" fill="#a8b8aa" stroke="#415956" stroke-width="3"/>')
  e.append(f'<path d="M{x-22} 1141Q{x} 1150 {x+22} 1141" fill="none" stroke="#415956" stroke-width="3"/>')
 # Back core: broad shoulders, a continuous plain rear tunic, no front wrap/V neckline.
 e += ['<path d="M512 321Q654 289 796 321L813 423L785 583L808 788Q655 819 499 788L520 583L495 423Z" fill="#bbc8bc" stroke="#405d56" stroke-width="4"/>',
 '<path d="M510 539Q654 557 794 539L791 565Q654 584 516 565Z" fill="#879e91" stroke="#405d56" stroke-width="3"/>',
 '<path d="M654 345L654 538M654 575L654 797" fill="none" stroke="#8a9f92" stroke-width="3"/>',
 '<path d="M591 147Q654 113 717 147L718 247Q711 280 688 290L690 315L619 315L620 290Q593 280 588 247Z" fill="#9daf9f" stroke="#405d56" stroke-width="4"/>',
 '<path d="M594 232Q654 251 713 232L702 275Q654 287 602 275Z" fill="#6c877d"/>',
 '<path d="M476 202L654 53L832 202Q654 260 476 202Z" fill="#c3c9be" stroke="#405d56" stroke-width="4"/>',
 '<path d="M920 425V245l-10 20m10-20l10 20" fill="none" stroke="#426b5c" stroke-width="5"/>',
 '<text x="878" y="450" font-size="18" fill="#294b3d">WHOLE BODY UP / BACK VIEW</text>',
 '<text x="30" y="1200" font-size="17" fill="#263c37">Root (654,1140). Both toes toward −Y. Authored geometry only; no identity/motion qualification.</text>']
 if qa:
  for side,x in [('LEFT',200),('RIGHT',900)]:
   point=points[side+'_ankle'];e.append(f'<text x="{x}" y="1020" font-size="24" fill="#7b3a34">ANATOMICAL {side}</text><path d="M{x} 1030L{point[0]} {point[1]}" stroke="#7b3a34" stroke-width="2"/>')
 return '<svg xmlns="http://www.w3.org/2000/svg" width="1254" height="1254" viewBox="0 0 1254 1254">'+''.join(e)+'</svg>'

(p/'guide.svg').write_text(svg());(p/'guide-qa.svg').write_text(svg(True))
