from pathlib import Path
import json,hashlib,subprocess
p=Path(__file__).parent
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1254" height="1254" viewBox="0 0 1254 1254"><g stroke="#493b2d" stroke-width="7" stroke-linejoin="round">']
# Original complete connected three-branch vector drawing, no imported pixels.
branches=[((227,700),(627,900),'#8c7250'),((627,900),(1027,1100),'#796045'),((627,900),(227,1100),'#89704e')]
for (a,b,col) in branches:
 x,y=a;X,Y=b
 parts.append(f'<path d="M{x} {y}L{X} {Y}L{X} {Y-450}L{x} {y-450}Z" fill="{col}"/>')
 for t in [i/7 for i in range(1,7)]:
  q=x+(X-x)*t;r=y+(Y-y)*t
  parts.append(f'<path d="M{q} {r-438}L{q} {r-12}" stroke="#56402d" stroke-width="15"/>')
 for h in [145,305]:
  parts.append(f'<path d="M{x} {y-h}L{X} {Y-h}" fill="none" stroke="#b19064" stroke-width="22"/>')
 parts.append(f'<path d="M{x} {y-450}L{X} {Y-450}" stroke="#ba9a6c" stroke-width="24"/>')
for x,y in [(227,700),(1027,1100),(227,1100),(627,900)]:
 parts.append(f'<path d="M{x-27} {y}L{x} {y-14}L{x+27} {y}L{x+27} {y+22}L{x} {y+36}L{x-27} {y+22}Z" fill="#998b77"/>')
 parts.append(f'<path d="M{x-17} {y-450}L{x} {y-459}L{x+17} {y-450}L{x+17} {y}L{x} {y+9}L{x-17} {y}Z" fill="#a58960"/>')
parts.append('</g></svg>')
svg=''.join(parts);(p/'guide.svg').write_text(svg);subprocess.run(['/home/kieu-hoang-quan/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node','-e','require("/home/kieu-hoang-quan/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp")(process.argv[1]).png().toFile(process.argv[2])',str(p/'guide.svg'),str(p/'guide.png')],check=True)
prompt='''One transparent whole RTS timber wall T junction idle sprite MASK7 (+X,-X,+Y), EXACTLY THREE connected branches and four posts including shared central post. Input is ONLY original whole vector authoring guide; repaint entire connected building as one coherent realistic pure 2D historical illustration. Preserve 1254x1254 canvas, camera, margins, ground center pivot (627,900). Branch ground endpoints +X (1027,1100), -X (227,700), +Y (227,1100). All panels height450: shared center top (627,450), end tops (1027,650), (227,250), (227,650). This is a T: diagonal continuous upper-left through center to lower-right wall plus a third lower-left wing. Absolutely NO fourth upper-right (-Y) branch. Full vertical aged warm-brown timber panels, thin top caps, restrained fine crossbars, modest solid connected timber posts, tiny sandy-grey stone feet. Dimensional hand-painted realistic historical Vietnamese timber palisade family, subtle grain/weathering, warm upper-left light, soft baked olive-earth contact shadow. Genuine transparent alpha. Finished whole pure2D illustration, never 3D or vector placeholder. No extra/missing branch, gate, tower, platform/island, scenery, people, text, props, watermark, detached parts. Do not mirror, rotate, recenter, fit, warp or assemble pieces. Preserve whole composition and branch extents.'''
(p/'prompt.txt').write_text(prompt)
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
(p/'input-pins.json').write_text(json.dumps({f.name:sha(f) for f in [p/'guide.svg',p/'guide.png',p/'prompt.txt']},indent=2))
for name in ['call-state.json','live-handle.json']:(p/name).write_text(json.dumps({'state':'prepared','calls':0,'retries':0,'maxCalls':1,'routing':'gpt-6.1-sol/low'}))
(p/'request.json').write_text(json.dumps({'promptPath':'prompt.txt','referenced_image_paths':[str((p/'guide.png').resolve())],'transparent_background':True,'callsMax':1,'retriesMax':0},indent=2))
