"""Original whole2D continuous L masonry guide, mask5 +X/+Y; no artwork ingestion."""
from pathlib import Path
OUT=Path(__file__).resolve().parent;HEIGHT=550

def p(x,y,height=0):return (627+800*(x-y),900+400*(x+y)-height)
def fmt(point):return ' '.join(f'{n:g}' for n in point)
def polygon(points,color):return '<polygon points="'+' '.join(fmt(p(*q)) for q in points)+f'" fill="{color}" stroke="#5c605a" stroke-width="5" stroke-linejoin="round"/>'
def line(a,b):return f'<path d="M{fmt(p(*a))}L{fmt(p(*b))}" fill="none" stroke="#62665f" stroke-width="5"/>'
# Single connected concave footprint with a full filled corner core, exactflushends.
footprint=[(-.09,-.09),(.5,-.09),(.5,.09),(.09,.09),(.09,.5),(-.09,.5)]
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1254" height="1254" viewBox="0 0 1254 1254">','<title>Original continuous whole stoneWall corner mask5 guide363</title>','<desc>Fixed1254 pivot627900 height550 thickness.18; +Xendpoint10271100 and+Y2271100; authoringreference only.</desc>','<g stroke-linecap="butt">']
xface=lambda t,h:(t,.09,h);yface=lambda t,h:(.09,t,h);xend=lambda t,h:(.5,t,h);yend=lambda t,h:(t,.5,h)
s += [polygon([xface(.09,0),xface(.5,0),xface(.5,HEIGHT),xface(.09,HEIGHT)],'#92958c'),polygon([yface(.09,0),yface(.5,0),yface(.5,HEIGHT),yface(.09,HEIGHT)],'#737a72'),polygon([xend(.09,0),xend(-.09,0),xend(-.09,HEIGHT),xend(.09,HEIGHT)],'#737a72'),polygon([yend(-.09,0),yend(.09,0),yend(.09,HEIGHT),yend(-.09,HEIGHT)],'#92958c')]
levels=[0,100,200,300,400,495,550]
for h in levels[1:-1]:
    # Continuous horizontal stone courses follow both wings through samecorner.
    for face in [xface,yface]:s.append(line(face(.09,h),face(.5,h)))
    for end in [xend,yend]:s.append(line(end(-.09,h),end(.09,h)))
for row,(lo,hi) in enumerate(zip(levels[:-1],levels[1:])):
    if row==len(levels)-2:continue
    for t in ([.2,.4] if row%2==0 else [.3]):
        for face in [xface,yface]:s.append(line(face(t,lo),face(t,hi)))
    if row%2==0:
        for end in [xend,yend]:s.append(line(end(0,lo),end(0,hi)))
# One continuous flat L top cap, not separate overlapping wall pictures.
s.append(polygon([(x,y,HEIGHT) for x,y in footprint],'#bec0b5'))
for t in [.2,.4]:s.append(line((t,-.09,HEIGHT),(t,.09,HEIGHT)));s.append(line((-.09,t,HEIGHT),(.09,t,HEIGHT)))
# Core is one modest cornercap block; no tall pillar or flaredfoot.
s+=['</g></svg>'];(OUT/'guide.svg').write_text('\n'.join(s)+'\n')
