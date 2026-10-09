from pathlib import Path
import json, hashlib

d = Path(__file__).parent
r = Path.cwd()
base = (r/'docs/art/pipeline/villager-walk-D0-passing-keys-153/F02-clothed-guide.svg').read_text()
# Original vector contours only. No raster extraction or raster alteration.
def leg(hip, knee, ankle, heel_up=False, raised=False):
    hx,hy=hip; kx,ky=knee; ax,ay=ankle
    trouser=f'<path d="M{hx-35} {hy}Q{kx-37} {ky-55} {kx-28} {ky}L{ax-24} {ay-62}Q{ax} {ay-43} {ax+25} {ay-62}L{kx+30} {ky}Q{kx+37} {ky-65} {hx+34} {hy}Z" fill="url(#brown)"/>'
    wrap=f'<path d="M{ax-24} {ay-62}Q{ax} {ay-48} {ax+25} {ay-62}L{ax+24} {ay}Q{ax} {ay+10} {ax-22} {ay}Z" fill="url(#cream)"/>'
    # Heel roll is authored into the sandal contour, never a rotated raster.
    heel=ay-3 if heel_up else ay+22; toe=ay+40 if not raised else ay+28
    shoe=f'<path d="M{ax-23} {heel}L{ax+17} {ay-3}Q{ax+45} {ay+12} {ax+80} {toe-8}Q{ax+90} {toe+5} {ax+72} {toe+10}L{ax+14} {toe+8}L{ax-29} {heel+10}Z" fill="#b5865d"/><path d="M{ax-29} {heel+10}L{ax+14} {toe+8}L{ax+77} {toe+5}L{ax+84} {toe+12}Q{ax+50} {toe+22} {ax+8} {toe+15}L{ax-32} {heel+19}Z" fill="#6b4b30"/><path d="M{ax-5} {ay+5}L{ax+42} {toe+5}M{ax+17} {ay+5}L{ax+60} {toe}" stroke="#493626" stroke-width="8" fill="none"/>'
    return trouser+wrap+shoe

poses={
 'F01':{'near':((465,595),(510,751),(538,910),False,False),'far':((539,595),(452,746),(367,910),True,False),'description':'nearRIGHT weight transfer; farLEFT rear heel rolls upward, toe remains low'},
 'F03':{'near':((465,595),(480,750),(448,910),True,False),'far':((539,595),(581,724),(600,862),False,True),'description':'nearRIGHT rear push-off; farLEFT swing advances and lowers toward F04'},
 'F05':{'near':((465,595),(418,754),(352,910),True,False),'far':((539,595),(572,748),(608,910),False,False),'description':'farLEFT weight transfer; nearRIGHT rear heel rolls upward'},
 'F07':{'near':((465,595),(538,716),(583,862),False,True),'far':((539,595),(528,748),(491,910),True,False),'description':'farLEFT rear push-off; nearRIGHT swing advances and lowers toward F00'},
}
for frame,p in poses.items():
    start=base.index('<!-- FAR LEFT flexed');end=base.index(' <!-- One whole tunic')
    legs='<!-- '+p['description']+' -->\n'+leg(*p['far'])+leg(*p['near'])
    out=base[:start]+legs+base[end:]
    # Whole drawn sleeve/forearm positions interpolate the contact-to-passing offset.
    offsets={'F01':-18,'F03':42,'F05':58,'F07':-30};dx=offsets[frame]
    out=out.replace('L415 491L427 543Q428 559 413 561L402 548L398 519',f'L{415+dx} 491L{427+dx} 543Q{428+dx} 559 {413+dx} 561L{402+dx} 548L{398+dx} 519')
    (d/f'{frame}-clothed-guide.svg').write_text(out)
sel=json.loads((r/'docs/art/pipeline/villager-walk-D0-passing-keys-155/parent-selection.json').read_text())
keys={f:sel['sources'][i] for i,f in enumerate(['F00','F02','F04','F06'])}
neighbors={'F01':('F00','F02'),'F03':('F02','F04'),'F05':('F04','F06'),'F07':('F06','F00')}
slots=[]
for frame,(prev,nxt) in neighbors.items():
    slots.append({'frame':frame,'status':'UNCALLED','primaryGuide':f'{frame}-clothed-guide.png','pose':poses[frame]['description'],'predecessor':keys[prev],'nextKey':keys[nxt],'callRequest':f'{frame}-call-request.json'})
    refs=[str((d/f'{frame}-clothed-guide.png').resolve()),str(r/keys[prev]['path']),str(r/keys[nxt]['path'])]
    prompt=f'Use case: identity-preserve. Produce ONE pure2D realistic illustrated Vietnamese villager wholeframe {frame}. Image1 is PRIMARY original complete clothed guide for the requested pose: {poses[frame]["description"]}. Image2 is selected predecessor {prev}; Image3 is selected next key {nxt}. These actual keys bind face, ivory tunic, loose brown trousers, dark farLEFT sash, woven conicalhat, wraps/sandals, proportions, ESE camera and material continuity. Advance physically between these keys, do not copy their contact or passing pose. Preserve near/far hip linkage; whole coherent illustration with natural clothing overlap. Transparent1254 square canvas, sourcepivot6541140, same family framing. No text, ground, props, guide marks, new identity, mirrored limbs, parts, cutout, splice, warp,3D or perframe fit. Guide flat colors are authoring cues only; restore realistic selected-key shading and detail.'
    (d/f'{frame}-call-request.json').write_text(json.dumps({'prompt':prompt,'referenced_image_paths':refs,'transparent_background':True},indent=2)+'\n')
order={'jobId':d.name,'status':'PREP_ONLY_ROOT_GUIDE_INTAKE_AND_NEW_DISPATCH_REQUIRED','model':'gpt-6.1-sol','reasoningEffort':'low','callsMade':0,'callOpen':False,'maxCalls':4,'retries':0,'slots':slots,'selectedKeysAuthority':'docs/art/pipeline/villager-walk-D0-passing-keys-155/parent-selection.json','canvas':[1254,1254],'pivot':[654,1140],'guideAuthoringFamilyTransform':'same153 original vector yNew=1.08*y-74.4727272727, x unchanged','export':'whole1254 to128 uniformLanczos; review89 wholecanvas; nofit/shift/mirror','gate':'Zero calls until root brief guide intake and new finite dispatch; full8actualframe loop intake before runtime/fanout','notEstablished':['returned illustrations','complete motion','world foot lock','runtime','owner acceptance']}
(d/'work-order.json').write_text(json.dumps(order,indent=2)+'\n')
