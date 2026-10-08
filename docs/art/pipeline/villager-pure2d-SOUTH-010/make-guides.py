#!/usr/bin/env python3
"""Simple hand2D passing guides; no source edit, rendering rig or projection."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageChops
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');O=Path(__file__).parent
sha=lambda b:hashlib.sha256(b).hexdigest()
paths={'canonicalSouth':R/'docs/art/characters/villager-neutral-D01-screen-South-007/raw.png','selectedF0':R/'docs/art/motion/authoring-tools/villager-walk-SOUTH-007/walk/keys/F00-left-contact-01/raw.png','selectedF4':R/'docs/art/pipeline/villager-pure2d-SOUTH-009/F4-trailing-contact-correction-01/raw.png'}
refs={}
for role,p in paths.items():
 im=Image.open(p).convert('RGBA');assert im.size==(1254,1254)
 refs[role]={'path':str(p),'encodedSha256':sha(p.read_bytes()),'rgbaSha256':sha(im.tobytes()),'dimensions':[1254,1254],'role':'identity/material/camera authority' if role=='canonicalSouth' else 'selected key candidate comparison/continuity; no loop approval'}
assert refs['selectedF4']['encodedSha256']=='929b9805f696abf341b8ea9b4df425a753da2c48b1be9ca13282bb5c72e0793f'
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
phases={'F2':{'editTarget':'selectedF0','stanceSide':'LEFT / viewer RIGHT','stance':[[705,820],[720,970],[720,1090],[735,1140]],'swingSide':'RIGHT / viewer LEFT','swing':[[600,820],[580,950],[608,1055],[620,1100]],'stanceSole':[[701,1138],[768,1142]],'swingSole':[[588,1094],[649,1100]],'stanceTrack':[[764,1202],[735,1140],[764,1093]]},'F6':{'editTarget':'selectedF4','stanceSide':'RIGHT / viewer LEFT','stance':[[600,820],[570,970],[550,1090],[565,1140]],'swingSide':'LEFT / viewer RIGHT','swing':[[704,820],[735,950],[685,1055],[695,1100]],'stanceSole':[[533,1138],[596,1142]],'swingSole':[[666,1094],[726,1100]],'stanceTrack':[[530,1193],[565,1140],[552,1084]]}}
for phase,t in phases.items():
 source=Image.open(paths[t['editTarget']]).convert('RGBA');mask=source.getchannel('A').point(lambda v:255 if v>=32 else 0);edge=ImageChops.subtract(mask.filter(ImageFilter.MaxFilter(3)),mask.filter(ImageFilter.MinFilter(3)))
 guide=Image.new('RGB',(1254,1254),'white');guide.paste((190,190,190),(0,0),edge);d=ImageDraw.Draw(guide);d.rectangle((440,910,850,1230),fill='white')
 def text(x,y,s):d.text((x,y),s,font=font,fill='black')
 text(22,20,f'AUTHORING_ONLY {phase} - natural passing pose (hand 2D estimates)');text(22,48,'Gray upper-body context; black leg/foot outlines = pose intent only');text(22,76,'Fixed1254 canvas / pivot654,1140 / referenceHeight1130; no pixel-pass gate')
 # Hand outlines around proposed limb path, not detachable illustrated components.
 for key in ['stance','swing']:
  hip,knee,ankle,sole=t[key]
  outline=[(hip[0]-38,hip[1]),(knee[0]-32,knee[1]),(ankle[0]-18,ankle[1]),(sole[0]-29,sole[1]-17),(sole[0]-32,sole[1]-3),(sole[0]-15,sole[1]+2),(sole[0]+24,sole[1]+2),(sole[0]+33,sole[1]-6),(sole[0]+20,sole[1]-19),(ankle[0]+18,ankle[1]),(knee[0]+32,knee[1]),(hip[0]+38,hip[1])]
  d.line(outline,fill='black',width=3);d.line([tuple(p) for p in t[key]],fill=(110,110,110),width=2)
  d.line([tuple(p) for p in t[key+'Sole']],fill='black',width=4)
  for point in [knee,ankle]:d.ellipse((point[0]-4,point[1]-4,point[0]+4,point[1]+4),outline='black',width=2)
 stance=t['stance'][-1];swing=t['swing'][-1]
 d.line([(stance[0]-55,1140),(stance[0]+55,1140)],fill=(100,100,100),width=1)
 # Label beside each side, with no colored or appearance underlay.
 stx=870 if phase=='F2' else 22;swx=22 if phase=='F2' else 870
 text(stx,950,t['stanceSide']);text(stx,978,'Loaded, nearly straight');text(stx,1006,f'Sole ~{stance[0]},1140');d.line([(stx+110,1045),tuple(stance)],fill='black',width=2)
 text(swx,860,t['swingSide']);text(swx,888,'Bent knee, swings under hip');text(swx,916,f'Lifted sole ~{swing[0]},1090-1110');d.line([(swx+125,956),tuple(swing)],fill='black',width=2)
 text(22,1212,'Small natural bounce + modest arm swing; rich whole illustration, not guide outlines.')
 p=O/f'{phase}-passing-guide.png';guide.save(p)
 t.update(status='AUTHORING_ONLY_ESTIMATES',uncertainty='Approximate hand2D targets, not measured contact/world lock. Natural anatomy and smooth silhouette take precedence over tiny pixel/cloth differences.',canvas=[1254,1254],pivot=[654,1140],referenceHeight=1130,guide={'path':str(p),'sha256':sha(p.read_bytes())})
 (O/f'{phase}-landmarks.json').write_text(json.dumps(t,indent=2)+'\n')
 (O/f'{phase}-prompt-draft.txt').write_text(f'''DRAFT AFTER PARENT BRIEF GUIDE VIEW: exactly one built-in edit for {phase}, zero retries. Edit {t['editTarget']} into a complete richly illustrated passing pose between the selected F0 and F4 contacts (F6 is F4 toward next F0). CanonicalSouth supplies identity/material/light/camera; both selected keys are continuity references, and the monochrome {phase} guide is AUTHORING_ONLY pose intent, never appearance.\n\nAnatomical {t['stanceSide']} is the supporting/loaded leg, nearly straight under the body. Move its sole from the prior front contact toward midstride near {stance}; do not leave it at the old forward footprint. Anatomical {t['swingSide']} passes forward under the hip with a naturally bent knee and clear lifted sandal near {swing}, y1090-1110. Preserve plausible knee/ankle connection and distinct limb ownership. These are approximate hand2D estimates, not rigid pixel pins or projection. Small natural body bounce and modest transitioning counter-swing; no huge arm poses.\n\nKeep1254x1254 canvas, family pivot[654,1140], referenceHeight1130 and whole-frame scale/camera unchanged. Preserve face, hat, LEFT sash ownership, proportions, outfit, rich folds/materials, coherent light/shadow and sandals in a finished whole2D illustration. No mirroring, crop/fit/shift, new isolated limb textures, puppet assembly, 3D dependency, colored guide traces or guide labels in output. Genuine alpha and intact raw output. Aim for natural smooth movement; tiny cloth/pixel differences are not a gate. Return ONLY this one phase. No in-betweens until actual F2/F6 exist and simple key review. Candidate only, no loop/foot-lock/runtime/owner approval.\n''')
order={'status':'DRAFT_READY_PENDING_PARENT_BRIEF_GUIDE_VIEW','profile':{'model':'gpt-6.1-sol','reasoning_effort':'low'},'imageCallsUsed':0,'maxImageCalls':2,'maxCallsPerKey':1,'maxRetriesPerKey':0,'keys':['F2','F6'],'references':refs,'jobs':{phase:{'editTargetRole':t['editTarget'],'requiredReferenceRoles':['canonicalSouth','selectedF0','selectedF4'],'guide':t['guide'],'prompt':{'path':str(O/f'{phase}-prompt-draft.txt'),'sha256':sha((O/f'{phase}-prompt-draft.txt').read_bytes())}} for phase,t in phases.items()},'boundary':'No actual edit authorized by this guide-only package; parent briefly views guides before dispatch. No other keys/in-betweens/retries/source edits. No tiny pixel or cloth-error gate.'}
(O/'WORK_ORDER_DRAFT.json').write_text(json.dumps(order,indent=2)+'\n')
(O/'READY.json').write_text(json.dumps({'status':'GUIDE_ONLY_READY','profile':order['profile'],'imageCalls':0,'sourceEdits':0,'references':refs,'files':{p.name:sha(p.read_bytes()) for p in O.iterdir() if p.is_file() and p.name!='READY.json'},'purpose':'Two estimated passing-key guides only. Natural smooth complete2D loop priority; no grounded-world evidence.'},indent=2)+'\n')
