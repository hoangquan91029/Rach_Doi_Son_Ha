"""MODEL_ONLY static pose projections, corrected anatomical ownership v2. Never character pixels or animation evidence."""
from pathlib import Path
import json,math,shutil

base=Path(__file__).parent
views={'southeast':('SE',0,'E',1,1),'southwest':('SW',2,'S',-1,1),'northeast':('NE',6,'N',1,-1),'northwest':('NW',4,'W',-1,-1)}
for name,(screen,engine,world,sx,sy) in views.items():
 p=base/f'static-{name}-v2';p.mkdir(exist_ok=True)
 f=(sx/math.sqrt(2),sy/math.sqrt(2));left=(f[1],-f[0]);front=sy>0
 def project(longitudinal,lateral,h):
  x=f[0]*longitudinal+left[0]*lateral
  d=f[1]*longitudinal+left[1]*lateral
  return [round(654+x,3),round(1140+.5*d-h,3)]
 points={}
 for side,lat in [('LEFT',113),('RIGHT',-113)]:
  for joint,along,h in [('shoulder',0,817),('elbow',12,612),('wrist',22,447),('hip',0,405),('knee',-4,222),('ankle',0,24),('heel',-35,0),('toe',115,0)]:points[side+'_'+joint]=project(along,lat,h)
 near='LEFT' if left[1]>0 else 'RIGHT';far='RIGHT' if near=='LEFT' else 'LEFT'
 plan={'status':'MODEL_ONLY_NON_ART_STATIC_GUIDE','canvas':[1254,1254],'root':[654,1140],'worldScale':38/1254,
  'direction':{'screen':screen,'engine':f'D{engine:02}','world':world,'bodyPlaneForward':f,'screenForward':[f[0],.5*f[1]]},
  'camera':{'projection':'orthographic dimetric geometry hypothesis','groundDiamondRatio':[2,1],'elevationDegrees':26.565},
  'projectionFormula':'screen=(654+forward.x*longitudinal+left.x*lateral,1140+0.5*(forward.depth*longitudinal+left.depth*lateral)-projectedHeight)',
  'anatomicalOwnership':{'near':near,'far':far,'leftBodyAxis':left,'note':'Labels are anatomical. Reflection only in authored mannequin coordinates, never painted character artwork.'},
  'points':points,'footAxes':{s:[round(f[0]*150,3),round(f[1]*75,3)] for s in ['LEFT','RIGHT']},
  'constraints':['All head, chest/back, pelvis and both sandal longitudinal axes share the diagonal heading','Front three-quarter visible' if front else 'Back three-quarter visible; no full front chest or face','Exactly one fixed root6541140; no image crop, bbox fit or large translation','Neutral weight balanced across feet, not a walking pose','Canonical illustrated identity supplied separately; guide geometry may not leak into final image'],
  'finishedArt':False,'motionQualified':False,'runtimeIntegrated':False,'imageCalls':0}
 (p/'coordinate-plan.json').write_text(json.dumps(plan,indent=2)+'\n')
 def path(a,b,width,color):return f'<path d="M{a[0]} {a[1]}L{b[0]} {b[1]}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>'
 def svg(qa=False):
  e=['<rect width="1254" height="1254" fill="#f0eee5"/>',f'<text x="30" y="32" font-size="20" fill="#263c37">MODEL_ONLY / NON_ART — STATIC {screen} — D{engine:02} / world {world}</text>','<path d="M430 1140L654 1028L878 1140L654 1252Z" fill="none" stroke="#a9b6ad" stroke-dasharray="8 8"/>','<path d="M644 1140h20M654 1130v20" stroke="#617b70" stroke-width="2"/>']
  for side in [far,near]:
   color='#a7b5b2' if side==far else '#718c84';lat=113 if side=='LEFT' else -113
   for a,b,w in [('shoulder','elbow',65),('elbow','wrist',37),('hip','knee',80),('knee','ankle',52)]:e.append(path(points[side+'_'+a],points[side+'_'+b],w,color))
   polygon=[project(-35,lat-30,0),project(110,lat-27,0),project(120,lat,0),project(110,lat+27,0),project(-35,lat+30,0)]
   e.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in polygon)+f'" fill="{color}" stroke="#405d56" stroke-width="3"/>')
   e.append(path(project(-20,lat,14),project(100,lat,14),9,'#546e65'))
  radius=math.sqrt((170*left[0])**2+(85*f[0])**2)
  e += [f'<path d="M{654-radius} 328Q654 190 {654+radius} 328L{660+radius} 444L{642+radius} 585L{663+radius} 783Q654 815 {645-radius} 783L{666-radius} 585L{645-radius} 444Z" fill="#bbc8bc" stroke="#405d56" stroke-width="4"/>',f'<path d="M{654-radius} 541Q654 566 {654+radius} 541L{650+radius} 572Q654 595 {658-radius} 572Z" fill="#879e91" stroke="#405d56" stroke-width="3"/>']
  if front:
   a=project(70,55,817);b=project(70,0,695);c=project(70,-55,817);e.append(f'<path d="M{a[0]} {a[1]}L{b[0]} {b[1]}L{c[0]} {c[1]}" fill="none" stroke="#546e65" stroke-width="7"/>')
  else:e.append(path(project(-70,0,817),project(-70,0,562),3,'#8a9f92'))
  for a,b,w in [('shoulder','elbow',65),('elbow','wrist',37)]:e.append(path(points[near+'_'+a],points[near+'_'+b],w,'#718c84'))
  hand=points[near+'_wrist'];e.append(f'<ellipse cx="{hand[0]}" cy="{hand[1]+20}" rx="18" ry="25" fill="#718c84" stroke="#405d56" stroke-width="2"/>')
  # Simple mannequin head with either front-plane features or rear hair. No copied face.
  e.append('<path d="M594 150Q654 109 714 150L722 238Q713 277 684 287L682 315L624 315L625 287Q595 272 588 238Z" fill="#a4b8b3" stroke="#405d56" stroke-width="4"/>')
  if front:
   x=654+f[0]*64;e += [f'<path d="M{x} 226l{sx*20} 12l{-sx*18} 6" fill="none" stroke="#385951" stroke-width="5"/>',f'<circle cx="{x-25}" cy="217" r="4" fill="#263f37"/><circle cx="{x+19}" cy="211" r="3" fill="#263f37"/>',f'<path d="M{x-17} 263q20 6 35 -5" fill="none" stroke="#385951" stroke-width="4"/>']
  else:e.append('<path d="M592 206Q654 231 717 206L701 268Q655 290 606 267Z" fill="#6c877d"/>')
  e.append(f'<path d="M466 192L{654+f[0]*12} 53L842 192Q654 244 466 192Z" fill="#c3c9be" stroke="#405d56" stroke-width="4"/>')
  a=[920,420];b=[a[0]+f[0]*130,a[1]+f[1]*65];e += [path(a,b,5,'#426b5c'),f'<circle cx="{b[0]}" cy="{b[1]}" r="7" fill="#426b5c"/>',f'<text x="860" y="490" font-size="18" fill="#294b3d">{screen} WHOLE BODY / BOTH FEET</text>',f'<text x="30" y="1202" font-size="16" fill="#263c37">Root6541140. {"Front" if front else "Back"} three-quarter. Anatomical {near} near. Geometry guide only, not motion or finished art.</text>']
  if qa:
   for side,x in [('LEFT',160),('RIGHT',920)]:
    e.append(f'<text x="{x}" y="960" font-size="23" fill="#7b3a34">{side} / {"NEAR" if side==near else "FAR"}</text>');e.append(path([x,970],points[side+'_ankle'],2,'#7b3a34'))
  return '<svg xmlns="http://www.w3.org/2000/svg" width="1254" height="1254" viewBox="0 0 1254 1254">'+''.join(e)+'</svg>'
 (p/'guide.svg').write_text(svg());(p/'guide-qa.svg').write_text(svg(True))
 shutil.copyfile(base/'static-east-v1/render-guide.mjs',p/'render-guide.mjs')
 print(name,plan['footAxes']['LEFT'],near)
