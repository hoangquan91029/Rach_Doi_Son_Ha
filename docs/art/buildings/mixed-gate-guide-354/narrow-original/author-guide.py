"""One complete original2D corner Gate guide. No raster/SVG input or transforms."""
from pathlib import Path
out=Path(__file__).resolve().parent
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1254" height="1254" viewBox="0 0 1254 1254">','<title>Original whole northwest portal Gate mask5 guide354</title>','<desc>Dimetric2:1 fixed pivot627,900. Jambs491,832 and763,832. +Xendpoint1027,1100; +Yendpoint227,1100. Complete authoring geometry only.</desc>','<g stroke="#49392b" stroke-width="7" stroke-linejoin="round">']
def path(d,fill,stroke=None,width=None):
    svg.append(f'<path d="{d}" fill="{fill}"'+(f' stroke="{stroke}"' if stroke else '')+(f' stroke-width="{width}"' if width else '')+'/>')
def panel(a,b,color):
    x,y=a;u,v=b
    path(f'M{x} {y}L{u} {v}L{u} {v-450}L{x} {y-450}Z',color)
    path(f'M{x} {y-450}L{x+25} {y-463}L{u+25} {v-463}L{u} {v-450}Z','#b39773')
    n=4 if abs(u-x)>200 else 2
    for k in range(1,n+1):
        t=k/(n+1);xx=x+(u-x)*t;yy=y+(v-y)*t
        path(f'M{xx:g} {yy-420:g}L{xx:g} {yy-35:g}','none','#4c3a29',18)
    for h in [155,310]:path(f'M{x} {y-h}L{u} {v-h}','none','#b08f62',25)
def foot(x,y):path(f'M{x-28} {y-10}L{x} {y-24}L{x+28} {y-10}L{x+28} {y+18}L{x} {y+32}L{x-28} {y+18}Z','#988779','#65574a')
def post(x,y,h=450):path(f'M{x-18} {y-h}L{x} {y-h-9}L{x+18} {y-h}L{x+18} {y-3}L{x} {y+6}L{x-18} {y-3}Z','#a0845e')
# Coherent orthogonal wings: no center spur, no missing-neighbor negativeX wing.
panel((91,1032),(491,832),'#81684b')
panel((763,832),(1163,1032),'#796045')
# Foreground short returns attach each exact positive-axis neighbor endpoint.
panel((91,1032),(227,1100),'#796045')
panel((1027,1100),(1163,1032),'#81684b')
path('M227 650L252 637L252 1087L227 1100Z','#594632')
path('M1163 582L1188 569L1188 1019L1163 1032Z','#594632')
for x,y in [(91,1032),(227,1100),(1163,1032),(1027,1100),(491,832),(763,832)]:foot(x,y)
for x,y in [(91,1032),(227,1100),(1163,1032),(1027,1100)]:post(x,y)
for x,y in [(491,832),(763,832)]:post(x,y,475)
# A single original raised horizontal-in-screen lintel over diagonal NW portal.
path('M474 327L500 314L788 314L762 327Z','#b69a72')
path('M474 327L762 327L762 369L474 369Z','#96774e')
path('M762 327L788 314L788 356L762 369Z','#5b4530')
svg.append('</g></svg>');(out/'guide.svg').write_text('\n'.join(svg)+'\n')
