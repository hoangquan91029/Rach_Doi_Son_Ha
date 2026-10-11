from pathlib import Path
import json,hashlib
p=Path(__file__).parent
for phase in ['F2','F3']:
 parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1254" height="1254" viewBox="0 0 1254 1254">','<!-- Original whole vector drawing. Authoring guide only. No raster pixels, transforms or PNG assembly. -->']
 def poly(pts,c):parts.append(f'<polygon points="{pts}" fill="{c}"/>')
 # Mathematical original314/234 full foundation planes.
 poly('227,640 1027,1040 1063,1022 263,622','#b3a38a');poly('227,640 1027,1040 1027,1100 227,700','#8c806b');poly('1027,1040 1063,1022 1063,1082 1027,1100','#6c6252')
 # Panel falls to same +x/-y side as314; broad broken planks directly drawn.
 for i in range(10):
  x=270+73*i;y=663+36.5*i
  dx=196+(i%3)*8 if phase=='F2' else 75+(i%4)*23;dy=-88 if phase=='F2' else -32+(i%3)*10
  lift=(i%3)*16 if phase=='F2' else (i%2)*6
  poly(f'{x},{y} {x+dx},{y+dy-lift} {x+dx+55},{y+dy+27-lift} {x+28},{y+15} {x+19},{y+5}', '#a17b4c' if i%2 else '#88603d')
  parts.append(f'<path d="M{x+16},{y+3} L{x+dx+17},{y+dy+7-lift}" stroke="#543c29" stroke-width="5"/>')
 if phase=='F3':
  for i in range(9):
   x=320+79*i;y=637+39.5*i
   poly(f'{x},{y} {x+98},{y+27} {x+117},{y+49} {x+9},{y+18} {x+19},{y+10}', '#b18c58' if i%2 else '#775334')
 # Broken rails spanning fragments across same full structure.
 poly('355,645 374,623 621,747 609,769','#b18c58');poly('751,866 776,842 1014,961 1000,983','#a37b4b')
 if phase=='F2':poly('431,626 450,612 466,622 440,643','#c3a170')
 # Broken low rooted stone ends: exact ends remain represented.
 for x,y in [(227,700),(1027,1100)]:
  h=95 if phase=='F2' else 58
  poly(f'{x},{y-h} {x+22},{y-h-10} {x+48},{y-h+5} {x+48},{y-21} {x},{y}', '#9c8e75')
  poly(f'{x},{y-h} {x+15},{y-h-18} {x+24},{y-h-9} {x+38},{y-h-16} {x+48},{y-h+5} {x+22},{y-h+13}', '#c1b298')
 # Broad rubble fragments spread along original foundation rather than compact292 footprint.
 for i in range(8):
  x=280+94*i;y=695+47*i
  poly(f'{x},{y} {x+18},{y-18} {x+44},{y-7} {x+52},{y+12} {x+20},{y+16}', '#a99b83')
 parts.append('</svg>');(p/(phase+'-guide.svg')).write_text('\n'.join(parts)+'\n')
 prompt=f'''Whole pure2D illustrated wall collapse {phase}, {'ground impact: mostly down with several boards still midfall' if phase=='F2' else 'settled terminal: broken warm timber pile, low broken stone posts, no intact standing panel'}. Guide is original mathematical whole drawing for pose/footprint ONLY, never final art. Canonical234 controls material/identity/camera;292 is material/style only and its compact footprint must NOT be copied. Use actual root-selected315 falling key as neighbor only after binding its actual path and hash; currently PENDING, do not invent. Same fallside as314 (+screenX/-screenY away from original foundation). Full foundation remnants span original anchors227700→10271100,1254squarecanvas,pivot627900,uniform128 export/render42.3225. Preserve both ends and full structure length. One coherent finished illustrated PNG with transparent alpha. No sourcepixel splicing, PNGrotation, warp, mirror, assembly,3D, fire or obscuring dust. {'Few airborne splinters allowed, only slight low dust if essential; retain clearly visible geometry.' if phase=='F2' else 'Resting wood and stone only; no airborne pieces or dust.'}'''
 (p/(phase+'-prompt.txt')).write_text(prompt)
(p/'work-order.json').write_text(json.dumps({'state':'PREP_ONLY','calls':0,'futureOrders':{'F2':{'calls':1,'retries':0,'state':'UNCALLED'},'F3':{'calls':1,'retries':0,'state':'UNCALLED'}},'binding':'PENDING actual root-selected315 neighbor path/hash and root intake; F3 additionally requires selectedF2','pivot':[627,900],'canvas':[1254,1254],'axis':[[227,700],[1027,1100]],'guidesAuthoringOnly':True},indent=2))
