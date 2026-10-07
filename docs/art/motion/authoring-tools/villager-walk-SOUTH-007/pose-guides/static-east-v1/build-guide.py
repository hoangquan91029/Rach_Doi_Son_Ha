"""One static MODEL_ONLY mannequin, never a painted identity or motion proof."""
import json,pathlib,hashlib,math
p=pathlib.Path(__file__).parent
root=[654,1140]
# Model-local longitudinal x, camera-depth d and projected vertical h.
# Exact game affine ground ratio2:1. No perspective camera or source-image pixels.
def project(x,d,h):return [root[0]+x,root[1]+.5*d-h]
points={}
for side,d in [('LEFT',-28),('RIGHT',28)]:
 for joint,x,h in [('shoulder',0,817),('elbow',20,612),('wrist',26,447),('hip',0,405),('knee',-4,222),('ankle',0,62),('heel',-35,0),('toe',115,0)]:points[side+'_'+joint]=project(x,d,h)
plan={'status':'MODEL_ONLY_NON_ART_NOT_ANIMATION','canvas':[1254,1254],'root':root,'worldScale':38/1254,'direction':{'screen':'EAST_RIGHT','engine':'D07','world':'NE','worldForward':[1,-1]},'camera':{'elevationDegrees':26.565,'projection':'locked game orthographic dimetric affine','groundDiamondRatio':[2,1]},'projectionFormula':'screen=(654+x,1140+0.5*depth-projectedHeight), axis aligned local heading NE; preserves game2:1 affine ground','proportions':'Visual South reference used for overall height and body segment proportions only; coordinate anatomy is MODEL_ONLY authored hypothesis, not exact measured body landmarks','sourceReference':{'path':'../../identity/south-neutral-reference/raw.png','sha256':'68a7fb9a71ae614f7c01432b1270e7a25071975667cfdf082ae02326d97678db','usage':'inspected proportions only; no copied pixels, traces, cutouts or image edits'},'anatomicalOwnership':'RIGHT side near(camera SE); LEFT side far(NW) for actor heading worldNE. Labels are QA only.','points':points,'constraints':['Head face, sternum, pelvis and both feet point screen right, not only the head','One visible side eye/nose silhouette; no full front face','Shoulder/hip pair overlap horizontally; narrow profile chest/pelvis','Both sole longitudinal axes have positiveX and zeroY; minor toe-out only if later illustration remains clearly profile','Fixed root and equal corresponding limb segment lengths; ground support sole points remain on their own projected depth plane'],'legSegmentLengthsSource':{side:[math.dist(points[side+'_hip'],points[side+'_knee']),math.dist(points[side+'_knee'],points[side+'_ankle'])] for side in ['LEFT','RIGHT']},'footAxes':{side:[points[side+'_toe'][0]-points[side+'_heel'][0],points[side+'_toe'][1]-points[side+'_heel'][1]] for side in ['LEFT','RIGHT']},'finishedArt':False,'motionQualified':False,'runtimeIntegrated':False}
for side in ['LEFT','RIGHT']:
 assert plan['footAxes'][side][0]>0 and abs(plan['footAxes'][side][1])<1e-9
assert abs(plan['legSegmentLengthsSource']['LEFT'][0]-plan['legSegmentLengthsSource']['RIGHT'][0])<1e-9
assert abs(plan['legSegmentLengthsSource']['LEFT'][1]-plan['legSegmentLengthsSource']['RIGHT'][1])<1e-9
(p/'coordinate-plan.json').write_text(json.dumps(plan,indent=2))

def svg(qa=False):
 elems=['<rect width="1254" height="1254" fill="#f0eee5"/>','<text x="32" y="32" font-size="20" fill="#263c37">MODEL_ONLY / NON_ART — STATIC EAST PROFILE — D07 / world NE</text>']
 # Ground guide and root, never final game art.
 elems+=['<path d="M430 1140 L654 1028 L878 1140 L654 1252 Z" fill="none" stroke="#a9b6ad" stroke-dasharray="8 8"/>','<path d="M644 1140h20 M654 1130v20" stroke="#617b70" stroke-width="2"/>']
 for side,color in [('LEFT','#a7b5b2'),('RIGHT','#647c79')]:
  for a,b,w in [('shoulder','elbow',44),('elbow','wrist',28),('hip','knee',57),('knee','ankle',37)]:
   pa=points[side+'_'+a];pb=points[side+'_'+b];elems.append(f'<path d="M{pa[0]} {pa[1]}L{pb[0]} {pb[1]}" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>')
  heel=points[side+'_heel'];toe=points[side+'_toe'];y=heel[1]
  elems.append(f'<path d="M{heel[0]} {y} L{heel[0]} {y-19} Q660 {y-46} 691 {y-19} L{toe[0]-15} {y-16} Q{toe[0]+8} {y-12} {toe[0]} {y} Z" fill="{color}" stroke="#415956" stroke-width="2"/>')
 # Profile core: front plane consistently at positiveX. Both shoulder caps align in x.
 elems+=['<path d="M601 320 Q638 305 686 318 L724 368 Q738 445 723 530 L709 641 L721 756 Q667 781 607 751 L591 621 L590 439 Z" fill="#bcc8c3" stroke="#405d56" stroke-width="4"/>','<path d="M710 365L724 446L711 640 M608 745L715 745" fill="none" stroke="#607c70" stroke-width="3"/>']
 # Near anatomical RIGHT arm drawn over the profile core; far LEFT remains partly occluded.
 for a,b,w in [('shoulder','elbow',44),('elbow','wrist',28)]:
  pa=points['RIGHT_'+a];pb=points['RIGHT_'+b];elems.append(f'<path d="M{pa[0]} {pa[1]}L{pb[0]} {pb[1]}" stroke="#718c84" stroke-width="{w}" stroke-linecap="round"/>')
 hand=points['RIGHT_wrist'];elems.append(f'<ellipse cx="{hand[0]}" cy="{hand[1]+22}" rx="15" ry="25" fill="#718c84" stroke="#405d56" stroke-width="2"/>')
 # One side-face eye, nose and mouth in the same screen-right profile.
 elems+=['<path d="M610 138 Q659 107 695 130 Q718 151 711 182 L734 191 L748 207 L727 216 L729 229 L720 238 L720 256 Q704 276 677 278 L669 310 L627 315 L628 268 Q600 245 596 205 Q588 166 610 138 Z" fill="#a4b8b3" stroke="#385951" stroke-width="4"/>','<ellipse cx="623" cy="211" rx="11" ry="18" fill="none" stroke="#46665e" stroke-width="3"/>','<path d="M696 182l15 3 M722 233l-13 2" stroke="#263f37" stroke-width="4"/>','<circle cx="704" cy="187" r="4" fill="#263f37"/>','<path d="M485 150L644 53L807 150Q686 179 485 150 Z" fill="#c3c9be" stroke="#405d56" stroke-width="4"/>']
 elems+=['<path d="M858 440h180l-20 -10m20 10l-20 10" fill="none" stroke="#426b5c" stroke-width="5"/>','<text x="858" y="425" font-size="18" fill="#294b3d">WHOLE BODY +X</text>','<text x="30" y="1200" font-size="17" fill="#263c37">Root (654,1140). Both toes +X. Profile overlap. Proportion guide only; no identity or direction approval.</text>']
 if qa:
  for side,x,y in [('LEFT',250,975),('RIGHT',955,1080)]:
   point=points[side+'_ankle'];elems.append(f'<text x="{x}" y="{y}" font-size="24" fill="#7b3a34">{side} / {"FAR" if side=="LEFT" else "NEAR"}</text><path d="M{x} {y+10}L{point[0]} {point[1]}" stroke="#7b3a34" stroke-width="2" fill="none"/>')
 return '<svg xmlns="http://www.w3.org/2000/svg" width="1254" height="1254" viewBox="0 0 1254 1254">'+''.join(elems)+'</svg>'
(p/'guide.svg').write_text(svg());(p/'guide-qa.svg').write_text(svg(True))
