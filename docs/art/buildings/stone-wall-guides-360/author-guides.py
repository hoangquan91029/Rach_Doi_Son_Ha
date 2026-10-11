"""Original whole2D stoneWall X/Y structural references; no artwork ingestion."""
from pathlib import Path
OUT=Path(__file__).resolve().parent
HEIGHT=550;THICKNESS=.18

def project(x,y,z=0):return (627+800*(x-y),900+400*(x+y)-z)
def fmt(p):return ' '.join(f'{v:g}' for v in p)
def polygon(points,fill,stroke='#5c605a',width=5):return '<polygon points="'+' '.join(fmt(project(*p)) for p in points)+f'" fill="{fill}" stroke="{stroke}" stroke-width="{width}" stroke-linejoin="round"/>'
def line(a,b):return f'<path d="M{fmt(project(*a))}L{fmt(project(*b))}" fill="none" stroke="#62665f" stroke-width="5"/>'
def make(axis):
    # Both complete wall solids are authored in worldplan, independently projected.
    if axis=='X':
        top=[(-.5,-.09,HEIGHT),(.5,-.09,HEIGHT),(.5,.09,HEIGHT),(-.5,.09,HEIGHT)]
        near=lambda t,z:(t,.09,z);end=lambda t,z:(.5,t,z)
        face=[near(-.5,0),near(.5,0),near(.5,HEIGHT),near(-.5,HEIGHT)]
        butt=[end(.09,0),end(-.09,0),end(-.09,HEIGHT),end(.09,HEIGHT)]
        frontcolor='#92958c';endcolor='#737a72';endpoints=[project(-.5,0),project(.5,0)]
    else:
        top=[(-.09,-.5,HEIGHT),(.09,-.5,HEIGHT),(.09,.5,HEIGHT),(-.09,.5,HEIGHT)]
        near=lambda t,z:(.09,t,z);end=lambda t,z:(t,.5,z)
        face=[near(-.5,0),near(.5,0),near(.5,HEIGHT),near(-.5,HEIGHT)]
        butt=[end(-.09,0),end(.09,0),end(.09,HEIGHT),end(-.09,HEIGHT)]
        frontcolor='#737a72';endcolor='#92958c';endpoints=[project(0,-.5),project(0,.5)]
    parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1254" height="1254" viewBox="0 0 1254 1254">',f'<title>Original whole stoneWall {axis} guide360</title>',f'<desc>Fixed pivot627900; wallheight550; thickness.18; endpointcenters{endpoints}; authoringreference only.</desc>','<g stroke-linecap="butt">',polygon(face,frontcolor),polygon(butt,endcolor)]
    # Five large staggered stone courses; joints stay on the authored faceplanes.
    levels=[0,100,200,300,400,495,550]
    for z in levels[1:-1]:parts.append(line(near(-.5,z),near(.5,z)));parts.append(line(end(-.09,z),end(.09,z)))
    for row,(z0,z1) in enumerate(zip(levels[:-1],levels[1:])):
        if row==len(levels)-2:continue # Flat cutstone capcourse, clean unflared silhouette.
        for t in [-.3,-.1,.1,.3] if row%2==0 else [-.4,-.2,0,.2,.4]:parts.append(line(near(t,z0),near(t,z1)))
        if row%2==0:parts.append(line(end(0,z0),end(0,z1)))
    parts.append(polygon(top,'#bec0b5'))
    # Sparse topcap blocks aligned along length; no protruding posts or railbeam.
    for t in [-.3,-.1,.1,.3]:
        if axis=='X':parts.append(line((t,-.09,HEIGHT),(t,.09,HEIGHT)))
        else:parts.append(line((-.09,t,HEIGHT),(.09,t,HEIGHT)))
    parts+=['</g></svg>'];(OUT/f'guide-{axis}.svg').write_text('\n'.join(parts)+'\n')
for axis in ['X','Y']:make(axis)
