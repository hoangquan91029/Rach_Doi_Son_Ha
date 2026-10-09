from pathlib import Path
import json,hashlib
p=Path(__file__).parent
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="512" viewBox="0 0 1024 512"><rect width="1024" height="512" fill="#f5f1e9"/><style>text{font-family:sans-serif;font-size:13px} .bone{fill:none;stroke-linecap:round;stroke-linejoin:round;stroke-width:12}</style><path d="M512 0V512" stroke="#bbb"/>']
for i,label in enumerate(['A: RIGHT / NEAR forward contact','B: LEFT / FAR forward contact']):
 x=i*512
 svg.append(f'<g transform="translate({x} 0)"><text x="20" y="24">{label}</text><text x="20" y="44">Same D0/ESE camera, root and size; MODEL ONLY</text>')
 svg.append('<path d="M267 80V480" stroke="#b7b7b7" stroke-dasharray="5 5"/><path d="M165 426L385 506 M198 407L418 487" stroke="#ccc"/><path d="M394 330L442 350" stroke="#222" stroke-width="2"/><text x="365" y="320">travel ESE</text><ellipse cx="264" cy="126" rx="64" ry="20" fill="none" stroke="#555" stroke-width="3"/><path d="M200 126L264 86L328 126 M250 147L256 177L260 237L267 306" fill="none" stroke="#555" stroke-width="4"/><path d="M236 178L282 164 M245 312L285 302" stroke="#555" stroke-width="4"/><circle cx="267" cy="465" r="6" fill="none" stroke="#222"/><text x="272" y="492">fixed root (267,465)</text>')
 # far first: blue dashed; near orange solid. Ownership anchored at hip, never swapped by screen ordering.
 far=[(285,302),(245,360),(233,425)] if i==0 else [(285,302),(310,383),(343,465)]
 near=[(245,312),(275,385),(310,482)] if i==0 else [(245,312),(215,370),(200,442)]
 for pts,c,dash in [(far,'#2676ad','stroke-dasharray="8 5"'),(near,'#d96b27','')]:
  svg.append(f'<polyline points="'+ ' '.join(f'{a},{b}' for a,b in pts)+f'" class="bone" stroke="{c}" {dash}/>')
  a,b=pts[-1]; svg.append(f'<path d="M{a-9} {b-3}L{a+17} {b+7}" stroke="{c}" stroke-width="6"/>')
 # trailing heel lifts, toe remains; leading foot flat contact.
 trail=far[-1] if i==0 else near[-1]; lead=near[-1] if i==0 else far[-1]
 svg.append(f'<circle cx="{lead[0]}" cy="{lead[1]}" r="13" fill="none" stroke="#398644" stroke-width="2"/><text x="{lead[0]+18}" y="{lead[1]-5}">receiving support</text><path d="M{trail[0]-12} {trail[1]+1}l0 -17" stroke="#555"/><text x="{trail[0]-110}" y="{trail[1]-20}">rear heel releases</text>')
 # counter swing with same shoulder ownership.
 svg.append('<path d="M236 178L'+('217 245L201 283' if i==0 else '277 228L309 254')+'" class="bone" stroke="#d96b27"/><path d="M282 164L'+('317 216L346 246' if i==0 else '270 218L249 254')+'" class="bone" stroke="#2676ad" stroke-dasharray="8 5"/><text x="20" y="65" fill="#d96b27">RIGHT near: solid orange</text><text x="20" y="82" fill="#2676ad">LEFT far / sash side: dashed blue</text></g>')
svg.append('</svg>'); (p/'paired-contact-guide.svg').write_text(''.join(svg))
refs=['docs/art/characters/villager-neutral-D00-screen-ESE/raw.png','docs/art/characters/villager-neutral-D00-screen-Southeast-007/raw.png']
order={'schema':'rds-pure2d-finite-work-order/v1','jobId':p.name,'status':'PREP_ONLY_PARENT_GUIDE_INTAKE_REQUIRED','model':'gpt-6.1-sol','reasoningEffort':'low','callsMade':0,'callOpen':False,'maxCalls':1,'retries':0,'method':'one complete paired-contact illustration; relational opposite-contact control','attachments':[{'path':r,'sha256':hashlib.sha256(Path(r).read_bytes()).hexdigest(),'role':role} for r,role in zip(refs,['canonical appearance only','D0 camera / identity / sash authority'])]+[{'path':str(p/'paired-contact-guide.svg'),'role':'internal pose planning; render to PNG before any authorized call'}],'excludedReferences':'all held F04 and selected033 F00: no pose inertia reference attached','direction':{'engine':0,'world':'E','screen':'ESE'},'requestedSheet':[2508,1254],'equalCells':2,'cellPivotNormalized':[654/1254,1140/1254],'fixedExtraction':{'regions':'left [0,W/2) x [0,H), right [W/2,W) x [0,H); require even W','scale':'s=128/max(W/2,H), same s for BOTH complete cells','padding':'center both resized cells in 128x128 using same offsets; no bbox fit','pivot':'[offsetX+s*(W/2)*(654/1254), offsetY+s*H*(1140/1254)] for BOTH','presentation':'whole 128 canvas displayed89; no per-frame fit/shift/rotation/mirror'},'toolCapability':'aspect ratio is a prompt request only; actual builtin dimensions/control unknown, no pixel-lock guarantee','intake':'one brief fixed89 pair look: genuine opposite forward/support legs, same direction and coherent whole identity; hold if neither pair reverses or clipping/pivot/scale failure is visible','laterGate':'F2/F6/inbetweens/all directions/units/runtime/public remain CLOSED until parent actual pair intake','scope':'no AI/API/key/Git/tests/runtime/topdocs/canonical edits in preparation'}
(p/'work-order.json').write_text(json.dumps(order,indent=2)+'\n')
try:
 import cairosvg
 cairosvg.svg2png(url=str(p/'paired-contact-guide.svg'),write_to=str(p/'paired-contact-guide.png'))
 cairosvg.svg2png(url=str(p/'paired-contact-guide.svg'),write_to=str(p/'guide-game89.png'),output_width=178,output_height=89)
except ImportError: pass
