import pathlib,json,hashlib
q=pathlib.Path(__file__).parent;h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def inv(p):return {str(f.relative_to(p)):h(f) for f in p.rglob('*') if f.is_file()}
for n,p in [('245',pathlib.Path('docs/art/buildings/gate-x-idle-245')),('239',pathlib.Path('docs/art/buildings/wall-y-idle-239')),('249',pathlib.Path('docs/qa/gate-x-install-249')),('public241',pathlib.Path('dist'))]:q.joinpath(n+'-before.json').write_text(json.dumps(inv(p),indent=2))
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1254" height="1254" viewBox="0 0 1254 1254"><g stroke="#49392b" stroke-width="7" stroke-linejoin="round">']
def pt(t):return 627-800*t,900+400*t
for a,b in [(-.5,-.17),(.17,.5)]:
 x,y=pt(a);u,v=pt(b);svg.append(f'<path d="M{x} {y}L{u} {v}L{u} {v-450}L{x} {y-450}Z" fill="#806447"/>');svg.append(f'<path d="M{x} {y-450}L{x-24} {y-462}L{u-24} {v-462}L{u} {v-450}Z" fill="#b39773"/>')
 for j in range(1,5):
  xx,yy=pt(a+(b-a)*j/5);svg.append(f'<path d="M{xx} {yy-430}L{xx} {yy-30}" stroke="#4c3a29" stroke-width="16"/>')
 for z in [130,290]:svg.append(f'<path d="M{x} {y-z}L{u} {v-z}" stroke="#b08f62" stroke-width="24"/>')
for t in [-.5,-.17,.17,.5]:
 x,y=pt(t);z=475 if abs(t)==.17 else 450;svg.append(f'<path d="M{x-27} {y-10}L{x} {y-24}L{x+27} {y-10}L{x+27} {y+18}L{x} {y+32}L{x-27} {y+18}Z" fill="#988779"/><path d="M{x-18} {y-z}L{x} {y-z-9}L{x+18} {y-z}L{x+18} {y}L{x} {y+9}L{x-18} {y}Z" fill="#a0845e"/>')
x,y=pt(-.17);u,v=pt(.17);svg.append(f'<path d="M{x+18} {y-475}L{u-18} {v-475}L{u-18} {v-435}L{x+18} {y-435}Z" fill="#96774e"/><path d="M{x+18} {y-475}L{x-6} {y-487}L{u-42} {v-487}L{u-18} {v-475}Z" fill="#b69a72"/></g></svg>');q.joinpath('guide.svg').write_text('\n'.join(svg))
prompt='Render ONLY this original complete GateY structural guide as one finished realistic pure2D historical Vietnamese RTS timber/stone gate illustration. Preserve whole down-left worldY silhouette and dimetric camera,1254square transparentcanvas/framing/margins,groundendpoints1027,700→227,1100,fixedpivot627,900. Openpassage footposts763,832→491,968; slenderposts/header475sourcepx abovefeet; sidepanels450sourcepx high reachingcellends. Entire centralopening belowheader throughground MUST be genuinelytransparent: no doorleaves/bars/planks/floorisland/threshold/solidshadow fillingit. Upperleftlight,naturalwarmtimbergrain,mutedstonefeet,painterly realistic handillustratedmaterials. Whole finishedillustration only; nopeople/text/logos/landscape/3D/cutoutseams. Do notmirror/rotate/warp/splice pixels; followthis soleoriginal authoringguide directly. Preservealpha. Intended42.3225logicalpx wholeGateY candidate.'
q.joinpath('prompt.txt').write_text(prompt);q.joinpath('request.json').write_text(json.dumps({'prompt':prompt,'referenced_image_paths':[str((q/'guide.png').resolve())],'transparent_background':True},indent=2));q.joinpath('call-state.json').write_text(json.dumps({'status':'prepared_not_called','call_open':False,'calls':0,'retries':0},indent=2))
