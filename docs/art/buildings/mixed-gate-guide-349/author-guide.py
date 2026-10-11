"""Finite original 2D vector authoring guide; no raster or prior SVG ingestion."""
from pathlib import Path
out=Path(__file__).resolve().parent
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1254" height="1254" viewBox="0 0 1254 1254">','<title>Original Gate completedidle mask5 axisX structural guide349</title>','<desc>Fixed pivot627,900. Open gate retains X endpoints227,700 and1027,1100. Perpendicular wing attaches at left jamb491,832 through elbow91,1032 to Y endpoint227,1100. Authoring only.</desc>','<g stroke="#49392b" stroke-width="7" stroke-linejoin="round">']
def path(points,fill,stroke=None,width=None):
    s.append(f'<path d="{points}" fill="{fill}"'+(f' stroke="{stroke}"' if stroke else '')+(f' stroke-width="{width}"' if width else '')+'/>')
def wing(a,b,face):
    x,y=a; u,v=b
    path(f'M{x} {y}L{u} {v}L{u} {v-450}L{x} {y-450}Z',face)
    path(f'M{x} {y-450}L{x+25} {y-463}L{u+25} {v-463}L{u} {v-450}Z','#b39773')
    for t in [.17,.38,.59,.80]:
        xx=x+(u-x)*t; yy=y+(v-y)*t
        path(f'M{xx:g} {yy-420:g}L{xx:g} {yy-35:g}','none','#4c3a29',18)
    for h in [155,310]:
        path(f'M{x} {y-h}L{u} {v-h}','none','#b08f62',25)
def foot(x,y):
    path(f'M{x-28} {y-10}L{x} {y-24}L{x+28} {y-10}L{x+28} {y+18}L{x} {y+32}L{x-28} {y+18}Z','#988779','#65574a')
def post(x,y,h=450):
    path(f'M{x-18} {y-h}L{x} {y-h-9}L{x+18} {y-h}L{x+18} {y-3}L{x} {y+6}L{x-18} {y-3}Z','#a0845e')
# Entire scene authored directly; wings are drawn, never assembled from input pixels.
wing((227,700),(491,832),'#806447')
foot(227,700)
post(227,700)
wing((763,968),(1027,1100),'#806447')
path('M1027 650L1052 637L1052 1087L1027 1100Z','#594632')
# Offset branch: parallel +Y then short +X return. It terminates at a jamb, not center.
wing((91,1032),(491,832),'#81684b')
wing((91,1032),(227,1100),'#796045')
path('M227 650L252 637L252 1087L227 1100Z','#594632')
for x,y in [(1027,1100),(91,1032),(227,1100),(491,832),(763,968)]: foot(x,y)
for x,y in [(1027,1100),(91,1032),(227,1100)]: post(x,y)
for x,y in [(491,832),(763,968)]: post(x,y,475)
# Same open header proportions and height family as original gate, no ground crosspiece.
path('M474 327L500 314L788 458L762 471Z','#b69a72')
path('M474 327L762 471L762 513L474 369Z','#96774e')
path('M762 471L788 458L788 500L762 513Z','#5b4530')
s.append('</g></svg>')
(out/'guide.svg').write_text('\n'.join(s)+'\n')
