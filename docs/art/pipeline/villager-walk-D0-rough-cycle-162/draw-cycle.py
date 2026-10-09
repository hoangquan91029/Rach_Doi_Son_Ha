from pathlib import Path
import hashlib,json,math

d=Path(__file__).parent
root=Path.cwd()
master=root/'docs/art/characters/villager-neutral-D00-screen-ESE/raw.png'
sha=hashlib.sha256(master.read_bytes()).hexdigest()
assert sha=='145b976ffd1bdf563cb5da78806547e6849424054f2c26fc297e155a0b366e94'
# New original contour authoring from observation of the sole canonical.
# All coordinates are drawn in256space. No imported SVG, raster parts, transforms or source warps.
def fmt(v): return f'{v:.2f}'.rstrip('0').rstrip('.')
def pt(p): return ' '.join(fmt(v) for v in p)
def path(s,fill,stroke='#514338',width=.8):
    return f'<path d="{s}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"/>'

cream='#d9cfb7'; light='#eee6d4'; shade='#b4a78c'; brown='#695746'; darkbrown='#493e35'; skin='#bb895e'; skins='#966b49'; dark='#493c34'

# D0 projected heading is screen(+1,+.5). The authored stance moves backwards along that plane.
# No locomotion length/world-lock claim; these are rough-cycle construction coordinates.
phases=[
 dict(frame='F00',phase='contact A',bob=0,twist=-1.6,pelvis=1.0,near=((118,158),(132,184),(145,223)),far=((145,157),(133,181),(114,207)),nearRoll='heel',farRoll='toe',nearHand=(90,142),farHand=(176,137)),
 dict(frame='F01',phase='down A',bob=2,twist=-.9,pelvis=.7,near=((119,160),(130,187),(136,218.5)),far=((144,159),(132,183),(112,204)),nearRoll='flat',farRoll='toe',nearHand=(96,148),farHand=(170,140)),
 dict(frame='F02',phase='passing A',bob=-.5,twist=.2,pelvis=0,near=((119,157.5),(124,185),(127,214)),far=((143,156.5),(151,182),(135,198)),nearRoll='flat',farRoll='swing',nearHand=(105,148),farHand=(163,146)),
 dict(frame='F03',phase='up A',bob=-2,twist=1.2,pelvis=-.7,near=((120,156),(119,182),(118,209.5)),far=((143,155),(154,178),(153,214)),nearRoll='toe',farRoll='swing',nearHand=(116,143),farHand=(154,144)),
 dict(frame='F04',phase='contact B',bob=0,twist=1.6,pelvis=-1.0,near=((119,158),(111,181),(105,210)),far=((144,157),(153,187),(164,229)),nearRoll='toe',farRoll='heel',nearHand=(125,136),farHand=(147,140)),
 dict(frame='F05',phase='down B',bob=2,twist=.9,pelvis=-.7,near=((120,160),(113,183),(104,204)),far=((144,159),(150,190),(155,224.5)),nearRoll='toe',farRoll='flat',nearHand=(121,142),farHand=(151,146)),
 dict(frame='F06',phase='passing B',bob=-.5,twist=-.2,pelvis=0,near=((119,157.5),(123,180),(120,200)),far=((143,156.5),(146,186),(146,220)),nearRoll='swing',farRoll='flat',nearHand=(111,148),farHand=(160,146)),
 dict(frame='F07',phase='up B',bob=-2,twist=-1.2,pelvis=.7,near=((118,156),(134,180),(134,216)),far=((144,155),(138,184),(137,215.5)),nearRoll='swing',farRoll='toe',nearHand=(99,148),farHand=(170,143)),
]
model=dict(frame='MODEL',phase='canonical-derived neutral model',bob=0,twist=0,pelvis=0,near=((117,159),(112,185),(108,214)),far=((144,160),(151,191),(158,229)),nearRoll='flat',farRoll='flat',nearHand=(91,141),farHand=(162,149))

def leg(pts,roll,far):
    (hx,hy),(kx,ky),(ax,ay)=pts
    # Loose trousers: coherent taper through knee, soft bent support rather than stick shin.
    w=11 if far else 12
    s=f'M{hx-w} {hy-7} Q{hx-9} {hy+10} {kx-w} {ky-8} Q{kx-w-3} {ky+3} {kx-7} {ky+10} L{ax-6} {ay-12} Q{ax+1} {ay-7} {ax+8} {ay-12} L{kx+10} {ky+6} Q{kx+15} {ky-4} {kx+10} {ky-13} Q{hx+10} {hy+3} {hx+w} {hy-7} Z'
    out=path(s,brown if not far else darkbrown)
    out+=path(f'M{hx-5} {hy+4} Q{kx+3} {ky-12} {kx+1} {ky+4} M{kx-9} {ky+4} Q{kx} {ky+11} {kx+8} {ky+5}', 'none', '#8b7660',.65)
    out+=path(f'M{ax-6} {ay-12} Q{ax+1} {ay-8} {ax+8} {ay-12} L{ax+6} {ay+2} Q{ax} {ay+5} {ax-6} {ay+1} Z',cream)
    out+=path(f'M{ax-6} {ay-6} Q{ax} {ay-2} {ax+7} {ay-6} M{ax-5} {ay} L{ax+6} {ay+2}', 'none', '#b4a58a',.65)
    # The foot planes point down-right; heel/toe rolls are newly drawn contours.
    heelY=ay-2 if roll=='toe' else ay+3
    toeY=ay+7 if roll=='heel' else ay+11
    if roll=='swing': heelY=ay+2;toeY=ay+8
    out+=path(f'M{ax-5} {heelY} Q{ax+2} {ay} {ax+8} {ay+4} L{ax+17} {toeY-2} Q{ax+22} {toeY+1} {ax+16} {toeY+4} Q{ax+3} {toeY+5} {ax-8} {heelY+6} Z',skin)
    out+=path(f'M{ax-8} {heelY+6} Q{ax+2} {toeY+7} {ax+17} {toeY+4} L{ax+19} {toeY+6} Q{ax+4} {toeY+11} {ax-9} {heelY+8} Z','#715338')
    out+=path(f'M{ax-3} {ay+3} L{ax+10} {toeY+2} M{ax+4} {ay+2} L{ax+15} {toeY}', 'none','#624d36',1.2)
    return out

def arm(shoulder,hand,far,bob,twist):
    sx,sy=shoulder;hx,hy=hand
    ex=sx+(hx-sx)*.42
    ey=sy+39
    # Continuous cuff/forearm silhouettes. All full images draw both arms with torso overlap.
    out=path(f'M{sx-7} {sy-1} Q{sx+7} {sy+1} {sx+9} {sy+16} L{ex+7} {ey-3} Q{ex} {ey+3} {ex-8} {ey-2} L{sx-10} {sy+20} Q{sx-12} {sy+6} {sx-7} {sy-1} Z',shade if far else cream)
    out+=path(f'M{ex-7} {ey-2} L{ex+6} {ey} Q{hx+5} {hy-10} {hx+4} {hy-5} Q{hx+7} {hy+3} {hx+1} {hy+6} Q{hx-5} {hy+6} {hx-6} {hy} L{hx-5} {hy-9} Q{ex-5} {ey+15} {ex-7} {ey-2} Z',skins if far else skin)
    out+=path(f'M{ex-8} {ey-4} Q{ex} {ey} {ex+8} {ey-3} L{ex+7} {ey+3} Q{ex} {ey+7} {ex-8} {ey+2} Z',light if not far else cream)
    out+=path(f'M{sx-5} {sy+13} Q{sx+1} {sy+25} {ex+5} {ey-9} M{hx-1} {hy-3} L{hx+1} {hy+3}', 'none','#8c765e',.7)
    return out

def draw(p):
    b=p['bob'];t=p['twist'];pel=p['pelvis']
    # Drawn torso/pelvis counterturn preserves widths. Head displacement follows real bob,
    # never a group/canvas stretch or independent fit.
    ns=(101+t,65+b); fs=(152+t*.3,65+b)
    parts=[arm(fs,p['farHand'],True,b,t),leg(p['far'],p['farRoll'],True),leg(p['near'],p['nearRoll'],False)]
    # Whole tunic, broad canonical chest, substantial hem concealing connected thigh roots.
    contour=f'M{114+t} {54+b} Q{101+t} {58+b} {96+t} {73+b} Q{96+t} {87+b} {103+t} {98+b} L{108+pel} {108+b} Q{104+pel} {130+b} {99+pel} {151+b} L{108+pel} {160+b} Q{125+pel} {167+b} {139+pel} {163+b} L{157+pel} {165+b} L{165+pel} {157+b} Q{157+pel} {136+b} {154+pel} {114+b} L{153+t*.3} {105+b} Q{165+t*.3} {88+b} {158+t*.3} {70+b} Q{150+t*.3} {59+b} {137+t} {53+b} Z'
    parts.append(path(contour,cream))
    parts.append(path(f'M{137+t} {55+b} L{146+t} {65+b} Q{138+t} {79+b} {117+t} {96+b} L{110+pel} {107+b} L{104+t} {101+b} Q{120+t} {79+b} {137+t} {55+b} Z',light))
    parts.append(path(f'M{151+t} {71+b} Q{160+t*.3} {86+b} {149+pel} {105+b} L{153+pel} {124+b} L{164+pel} {157+b} L{155+pel} {162+b} Q{147+pel} {136+b} {144+pel} {116+b} L{145+t} {97+b} Z',shade,'none'))
    # Garment overlap and creases respond to pelvis and chest together.
    parts.append(path(f'M{113+pel} {114+b} Q{116+pel} {135+b} {110+pel} {155+b} M{128+pel} {117+b} Q{124+pel} {140+b} {129+pel} {160+b} M{142+pel} {117+b} Q{147+pel} {138+b} {149+pel} {159+b} M{100+t} {86+b} Q{114+t} {98+b} {125+t} {95+b}', 'none','#a39377',.8))
    parts.append(path(f'M{107+pel} {104+b} Q{132+pel} {110+b} {154+pel} {103+b} L{155+pel} {110+b} Q{132+pel} {117+b} {106+pel} {111+b} Z',dark))
    parts.append(path(f'M{109+pel} {108+b} Q{129+pel} {114+b} {148+pel} {107+b} M{110+pel} {105+b} Q{129+pel} {111+b} {150+pel} {105+b}', 'none','#79695a',.75))
    parts.append(path(f'M{146+pel} {107+b} Q{154+pel} {105+b} {153+pel} {115+b} L{150+pel} {119+b} Q{155+pel} {132+b} {159+pel} {145+b} L{150+pel} {148+b} L{147+pel} {137+b} L{144+pel} {157+b} L{135+pel} {153+b} Q{138+pel} {131+b} {141+pel} {116+b} Q{139+pel} {108+b} {146+pel} {107+b} Z','#655346'))
    parts.append(arm(ns,p['nearHand'],False,b,t))
    # Neck, visible ear, face/goatee: observed canonical ESE planes, not old guides.
    parts.append(path(f'M{121+t*.25} {44+b} L{135+t*.25} {43+b} L{138+t*.25} {56+b} L{124+t*.25} {66+b} L{118+t*.25} {58+b} Z',skin))
    parts.append(path(f'M{117+t*.25} {30+b} Q{129+t*.25} {23+b} {140+t*.25} {32+b} L{143+t*.25} {41+b} L{147+t*.25} {45+b} L{142+t*.25} {47+b} L{142+t*.25} {53+b} Q{134+t*.25} {59+b} {126+t*.25} {53+b} L{121+t*.25} {47+b} Q{113+t*.25} {45+b} {114+t*.25} {39+b} Z',skin))
    parts.append(path(f'M{118+t*.25} {37+b} Q{119+t*.25} {33+b} {122+t*.25} {38+b} L{123+t*.25} {43+b} Q{119+t*.25} {47+b} {116+t*.25} {41+b} Z',skins))
    parts.append(path(f'M{126+t*.25} {33+b} Q{133+t*.25} {29+b} {140+t*.25} {33+b} L{142+t*.25} {38+b} L{128+t*.25} {40+b} Z','#d8a578','none'))
    parts.append(path(f'M{133+t*.25} {39+b} L{139+t*.25} {39+b} M{137+t*.25} {47+b} L{142+t*.25} {47+b}', 'none','#45392f',.8))
    parts.append(path(f'M{129+t*.25} {50+b} L{140+t*.25} {49+b} L{140+t*.25} {54+b} L{133+t*.25} {57+b} L{130+t*.25} {53+b} Z','#3e352e'))
    parts.append(path(f'M{116+t*.25} {32+b} Q{125+t*.25} {25+b} {139+t*.25} {29+b} L{142+t*.25} {33+b} L{128+t*.25} {34+b} L{124+t*.25} {39+b} L{119+t*.25} {35+b} L{115+t*.25} {39+b} Z','#332e29'))
    # Slanted woven conicalhat; top/brim retains same mass throughout the sequence.
    h=t*.15
    parts.append(path(f'M{98+h} {44+b} Q{122+h} {36+b} {160+h} {26+b} Q{165+h} {24+b} {163+h} {29+b} Q{151+h} {41+b} {124+h} {47+b} Q{107+h} {52+b} {98+h} {47+b} Z','#775f43'))
    parts.append(path(f'M{98+h} {44+b} L{125+h} {11+b} Q{147+h} {16+b} {161+h} {26+b} Q{132+h} {31+b} {98+h} {44+b} Z','#bea078'))
    parts.append(path(f'M{125+h} {11+b} L{121+h} {36+b} M{125+h} {11+b} L{139+h} {31+b} M{125+h} {11+b} L{153+h} {28+b} M{108+h} {32+b} Q{130+h} {28+b} {152+h} {23+b} M{103+h} {38+b} Q{128+h} {33+b} {159+h} {26+b}', 'none','#947855',.6))
    parts.append(path(f'M{118+t*.25} {42+b} Q{121+t*.25} {50+b} {132+t*.25} {54+b}', 'none','#64513d',.65))
    return '<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256"><title>162 original clothed rough '+p['frame']+' '+p['phase']+'</title>'+''.join(parts)+'</svg>'

for p in [model]+phases: (d/(p['frame']+'-rough.svg')).write_text(draw(p))
landmarks={'source':'canonical ESE observed complete illustration','workingCanvas':[256,256],'pivot':[133.51,232.73],'headHatTop':[125,11],'nearShoulder':[101,65],'farShoulder':[152,65],'chestSpanApprox':[99,160],'waistCenter':[131,108],'pelvisCenter':[131,151],'tunicHemRangeApprox':[99,165],'nearHip':[118,158],'farHip':[144,157],'nearIs':'anatomicalRIGHT viewer-left hip; foreground occlusion','farIs':'anatomicalLEFT viewer-right hip; background occlusion','projectionD0':[1,.5],'note':'coarse observation/authoring controls, not measured anatomy or final camera proof'}
(d/'model-landmarks.json').write_text(json.dumps(landmarks,indent=2)+'\n')
metadata={'job':'162','status':'ORIGINAL_ROUGH_AUTHORING_ONLY_ROOT_INTAKE_REQUIRED','model':'gpt-6.1-sol','reasoningEffort':'low','callsMade':0,'maxCalls':0,'callOpen':False,'workingCanvas':[256,256],'pivot':[133.51,232.73],'uniformPresentation':[89,89],'durationMs':600,'holdMs':75,'frames':phases,'master':{'path':str(master),'sha256':sha,'role':'SOLE identity/proportions/camera observational authority; no sourcepixel sampling/copy'},'authoring':'New original complete clothed SVG contours; no153/158 templates, rejected155 sources, imported raster parts, pixel warp/splice, cutout or3D','projectedGroundSlope':.5,'stancePlan':'near stanceF0-F3, far stanceF4-F7; support samples step(-9,-4.5) in256 authoring space, toe/heel/contact pose changes drawn; no world-lock claim','notEstablished':['finished realistic illustration','root guide intake','natural actual illustrated loop','world foot lock','runtime or fanout']}
(d/'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
