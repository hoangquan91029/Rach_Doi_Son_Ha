import importlib.util,json,hashlib,math,time,sys
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[4];base=ROOT/'docs/art/pipeline/blender-villager-504'
pins=json.loads((base/'render-inputs.json').read_text())
for p in pins:assert hashlib.sha256((ROOT/p['path']).read_bytes()).hexdigest()==p['sha256'],p['path']
auth=json.loads((ROOT/'docs/audits/continuation-504/root/render-authorization.json').read_text());out=ROOT/auth['output'];assert not out.exists()
spec=importlib.util.spec_from_file_location('villager504_candidate',ROOT/auth['script']['path']);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
start=time.monotonic();root,scene=module.build_candidate(out,auth)
(out/'authoring-script.py').write_bytes((ROOT/auth['script']['path']).read_bytes())
(out/'root-authorization.json').write_text(json.dumps(auth,indent=2)+'\n')
scene.render.resolution_x=scene.render.resolution_y=256;scene.render.resolution_percentage=100
assert scene.cycles.device=='CPU' and scene.cycles.samples==32 and scene.render.threads==2
metadata={'blender':bpy.app.version_string,'python':sys.version,'device':scene.cycles.device,'samples':scene.cycles.samples,'threads':scene.render.threads,'cameraLocation':list(scene.camera.location),'cameraRotation':list(scene.camera.rotation_euler),'orthoScale':scene.camera.data.ortho_scale,'pivot':module.verify()['pivot'],'render':[42,42],'resolution':[256,256],'objectCount':len(scene.objects),'sceneBuilds':1,'renderCount':0,'correctionCap':0,'appearanceApproval':False,'rig':None,'sourcePins':pins}
for d in [0,1]:
 root.rotation_euler.z=-d*math.pi/4;bpy.context.view_layer.update();scene.render.filepath=str(out/f'neutral-D{d}.png');bpy.ops.render.render(write_still=True);metadata['renderCount']+=1
root.rotation_euler.z=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'candidate.blend'));metadata['elapsedSeconds']=time.monotonic()-start
(out/'actual-render.json').write_text(json.dumps(metadata,indent=2)+'\n');print('DONE',json.dumps(metadata),flush=True)
