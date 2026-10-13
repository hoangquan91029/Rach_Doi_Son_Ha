#!/usr/bin/env python3
"""Candidate whole-frame export. Validation does not authenticate qualification prose."""
import argparse
import hashlib
import json
import math
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

def require(ok, message):
    if not ok:
        raise ValueError(message)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def path_in(root, value):
    require(isinstance(value, str) and value and not Path(value).is_absolute(), 'relative path required')
    path = (root / value).resolve()
    require(path.is_relative_to(root.resolve()) and '..' not in Path(value).parts, 'path escape')
    return path

def pin(root, value):
    require(isinstance(value, dict) and set(value) == {'path', 'sha256'}, 'exact pin required')
    path = path_in(root, value['path'])
    require(path.is_file() and re.fullmatch('[a-f0-9]{64}', value['sha256']) and digest(path) == value['sha256'], 'input pin mismatch')
    return path

def number(n):
    return type(n) in (int, float) and math.isfinite(n)

def world_signature(matrix):
    """Pure matrix gate; evaluated parent transforms included, bone poses excluded."""
    require(len(matrix) == 4 and all(len(row) == 4 for row in matrix) and all(number(v) for row in matrix for v in row), 'invalid evaluated world matrix')
    a,b,c = [row[:3] for row in matrix[:3]]
    det = a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])
    require(det > 0, 'mirrored or singular evaluated world transform')
    return tuple(math.sqrt(sum(matrix[row][col]**2 for row in range(3))) for col in range(3))

def fixed_world_signature(matrix, baseline):
    actual = world_signature(matrix)
    require(all(abs(a-b) <= 1e-6*max(1,abs(b)) for a,b in zip(actual,baseline)), 'animated evaluated world scale forbidden')
    return actual

def render_members(visible_names, allowlist, collection_names):
    require(set(allowlist).issubset(set(collection_names)), 'allowlisted mesh outside selected collection')
    require(set(visible_names) == set(allowlist), 'render-visible mesh allowlist mismatch')

def validate(job, root):
    fields = {'schema','id','identity','action','direction','original','view','blend','selection','qualification','layout','frames','loop','output','candidate'}
    require(isinstance(job, dict) and set(job) == fields and job['schema'] == 'rds-blender-job/v1', 'exact job schema required')
    require(re.fullmatch('[A-Za-z0-9_.-]{1,120}', job['id']) is not None and job['candidate'] is True, 'candidate ID required')
    require(type(job['direction']) is int and 0 <= job['direction'] <= 7, 'engine direction required')
    require(isinstance(job['identity'], str) and isinstance(job['action'], str), 'identity/action required')
    code = "import {actionSpec} from './shared/unit-action-spec.js';import {TILE_WIDTH,TILE_HEIGHT,CAMERA_ELEVATION} from './client/world-presentation.js';console.log(JSON.stringify({spec:actionSpec(...JSON.parse(process.argv[1])),camera:{tile:[TILE_WIDTH,TILE_HEIGHT],elevation:CAMERA_ELEVATION}}));"
    actual = json.loads(subprocess.check_output(['node','--input-type=module','-e',code,json.dumps([job['identity'],job['action']])], cwd=REPO, text=True))
    spec = actual['spec']
    require(spec['applicable'] and not spec['alias'], 'known canonical applicable action required')
    paths = {name: pin(root, job[name]) for name in ('original','view','blend','qualification')}
    require(paths['blend'].suffix == '.blend', 'blend file required')
    selection = job['selection']
    require(set(selection) == {'scene','model','rig','camera','action','renderCollection','renderMeshes'} and all(isinstance(selection[k],str) and re.fullmatch('[A-Za-z0-9_. -]{1,120}',selection[k]) for k in ('scene','model','rig','camera','action','renderCollection')) and isinstance(selection['renderMeshes'],list) and 1 <= len(selection['renderMeshes']) <= 128 and all(isinstance(v,str) and re.fullmatch('[A-Za-z0-9_. -]{1,120}',v) for v in selection['renderMeshes']) and len(set(selection['renderMeshes'])) == len(selection['renderMeshes']) and selection['model'] in selection['renderMeshes'], 'exact selected Blender names required')
    layout = job['layout']
    require(set(layout) == {'fixedCanvas','cell','pivot','render','contactShadow','camera'}, 'exact layout required')
    size = layout['fixedCanvas']
    require(set(size) == {'width','height'} and all(type(v) is int and 1 <= v <= 16384 for v in size.values()) and size['width'] == size['height'] and size['width']**2 <= 32*1024*1024, 'square fixed canvas required')
    require(size == {'width':256,'height':256}, 'v1 fixed source canvas must be 256 square')
    require(layout['cell'] == {'width':128,'height':128}, 'compiler cell mismatch')
    pivot = layout['pivot']
    require(set(pivot) == {'space','x','y'} and pivot['space'] == 'source' and all(number(pivot[k]) and 0 <= pivot[k] <= size['width'] for k in ('x','y')), 'fixed pivot required')
    render = layout['render']
    require(set(render) == {'width','height'} and all(number(v) and v > 0 for v in render.values()) and render['width'] == render['height'], 'fixed logical scale required')
    shadow = layout['contactShadow']
    require(shadow == {'mode':'baked'} or set(shadow) == {'mode','assetId'} and shadow['mode'] == 'separate' and isinstance(shadow['assetId'],str) and shadow['assetId'], 'shadow required')
    require(layout['camera'] == {'projection':'dimetric','ratio':[2,1],**actual['camera']}, 'engine projection mismatch')
    frames = job['frames']
    require(isinstance(frames,list) and len(frames) == spec['frames'], 'action frame slots mismatch')
    require(type(job['loop']) is bool and job['loop'] == (job['action'] in ('idle','walk','gather_wood','gather_food','gather_iron','build')), 'action loop policy mismatch')
    for i,f in enumerate(frames):
        require(set(f) == {'slot','blenderFrame','phase','durationMs','status'} and f['slot'] == i and type(f['slot']) is int and type(f['blenderFrame']) is int and 0 <= f['blenderFrame'] <= 100000 and f['phase'] == i/len(frames) and number(f['durationMs']) and 0 < f['durationMs'] <= 60000 and f['status'] == 'candidate', 'exact candidate frame slot/timing required')
    require(len({f['blenderFrame'] for f in frames}) == len(frames), 'duplicate Blender frames')
    require(job['action'] != 'death' or sum(f['durationMs'] for f in frames) <= 4000, 'death exceeds corpse window')
    q = json.loads(paths['qualification'].read_text())
    bindings = {k:job[k] for k in ('identity','action','direction','original','view','blend','selection','layout','frames','loop')}
    require(q.get('schema') == 'rds-blender-selection/v1' and q.get('status') == 'qualified' and q.get('bindings') == bindings and all(q.get(k) == 'VERIFIED' for k in ('identityReview','modelReview','rigReview','cameraReview')), 'source-bound selected model/rig/camera qualification required')
    out = path_in(root, job['output'])
    require(not out.exists() and not any(p == out or p.is_relative_to(out) for p in paths.values()), 'output exists or overlaps input')
    angle = job['direction']*math.pi/4
    return {'schema':'rds-blender-plan/v1','job':job,'inputHashes':{k:digest(v) for k,v in paths.items()},'mapping':[{'slot':f['slot'],'path':f"F{f['slot']}.png",'blenderFrame':f['blenderFrame']} for f in frames], 'groundVector':[math.cos(angle),math.sin(angle)],'screenVector':[math.cos(angle)-math.sin(angle),(math.cos(angle)+math.sin(angle))/2], 'acceptance':{k:'UNKNOWN' for k in ('blenderExecution','visual','motion','runtime','owner','release')},'compilerIntegration':'UNKNOWN','orthographicBasis':{'right':[2**-.5,-2**-.5,0],'up':[-.5*2**-.5,-.5*2**-.5,math.sqrt(3)/2],'view':[math.sqrt(3/8),math.sqrt(3/8),.5],'worldPixelScale':27*math.sqrt(2),'physicalElevationDegrees':30,'engineElevationLabel':actual['camera']['elevation'],'engineToBlender':'(x,y,z) -> (x,-y,z)'}}

def saved_background_state(bpy, expected):
    """Blender 5 marks freshly loaded files dirty; reload disk in background only.

    Reload discards all in-memory changes. Never save or bless interactive state.
    """
    require(Path(bpy.data.filepath).resolve() == expected, 'opened blend mismatch')
    if bpy.data.is_dirty:
        require(bpy.app.background, 'unsaved Blender data forbidden')
        bpy.ops.wm.open_mainfile(filepath=str(expected), use_scripts=False)
        require(Path(bpy.data.filepath).resolve() == expected, 'opened blend mismatch')

def export(job, root):
    plan = validate(job, root)
    import bpy  # only Blender execution requires this dependency
    require(not bpy.context.preferences.filepaths.use_scripts_auto_execute, 'disable Blender auto-execution required')
    saved_background_state(bpy, pin(root,job['blend']))
    selection = job['selection']
    scene = bpy.data.scenes.get(selection['scene'])
    require(scene is not None and bpy.context.scene == scene, 'selected active scene missing')
    model,rig,camera = [scene.objects.get(selection[k]) for k in ('model','rig','camera')]
    require(model is not None and model.type == 'MESH' and rig is not None and rig.type == 'ARMATURE' and camera is not None and camera.type == 'CAMERA' and camera.data.type == 'ORTHO', 'selected objects/types mismatch')
    require(any(m.type == 'ARMATURE' and m.object == rig for m in model.modifiers), 'selected mesh rig binding missing')
    require(rig.animation_data is not None and rig.animation_data.action is not None and rig.animation_data.action.name == selection['action'], 'selected rig action mismatch')
    require(scene.camera == camera, 'selected scene camera mismatch')
    basis = camera.matrix_world.to_3x3()
    expected = [(2**-.5,2**-.5,0),(-.5*2**-.5,.5*2**-.5,math.sqrt(3)/2),(math.sqrt(3/8),-math.sqrt(3/8),.5)]
    require(all(abs(basis[row][col]-expected[col][row]) < 1e-5 for row in range(3) for col in range(3)), 'camera basis differs from engine projection; no automatic adjustment')
    require(all(v > 0 for v in model.scale) and all(v > 0 for v in rig.scale), 'mirrored model/rig forbidden')
    collection = bpy.data.collections.get(selection['renderCollection'])
    require(collection is not None and any(collection.name == c.name for c in scene.collection.children) , 'selected render collection missing')
    render_members([o.name for o in scene.objects if o.type == 'MESH' and not o.hide_render], selection['renderMeshes'], [o.name for o in collection.all_objects])
    require(all(o.type in ('MESH','ARMATURE','CAMERA','LIGHT','EMPTY') or o.hide_render for o in scene.objects), 'unlisted renderable object type')
    depsgraph = bpy.context.evaluated_depsgraph_get()
    scales = {o.name:world_signature([list(row) for row in o.evaluated_get(depsgraph).matrix_world]) for o in [rig]+[scene.objects[name] for name in selection['renderMeshes']]}
    camera_matrix = tuple(v for row in camera.matrix_world for v in row)
    camera_scale = camera.data.ortho_scale
    model_scale = tuple(model.scale)
    rig_scale = tuple(rig.scale)
    # Camera/world/model transforms are authored and qualified, never auto-fit per frame.
    out = path_in(root,job['output']); out.mkdir(parents=True,exist_ok=False)
    scene.render.resolution_x = job['layout']['fixedCanvas']['width']
    scene.render.resolution_y = job['layout']['fixedCanvas']['height']
    scene.render.resolution_percentage = 100
    scene.render.film_transparent = True
    scene.render.use_border = False
    scene.render.use_crop_to_border = False
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.image_settings.color_depth = '8'
    for entry in plan['mapping']:
        scene.frame_set(entry['blenderFrame'])
        depsgraph = bpy.context.evaluated_depsgraph_get()
        render_members([o.name for o in scene.objects if o.type == 'MESH' and not o.hide_render], selection['renderMeshes'], [o.name for o in collection.all_objects])
        for name, baseline in scales.items():
            fixed_world_signature([list(row) for row in scene.objects[name].evaluated_get(depsgraph).matrix_world],baseline)
        require(tuple(v for row in camera.matrix_world for v in row) == camera_matrix and camera.data.ortho_scale == camera_scale and tuple(model.scale) == model_scale and tuple(rig.scale) == rig_scale, 'animated camera or scale fitting forbidden')
        scene.render.filepath = str(out/entry['path'])
        bpy.ops.render.render(write_still=True,scene=scene.name)
        entry['sha256'] = digest(out/entry['path'])
    require(digest(pin(root,job['blend'])) == plan['inputHashes']['blend'], 'blend changed during export')
    plan['blenderVersion'] = bpy.app.version_string
    plan['acceptance']['blenderExecution'] = 'VERIFIED'
    (out/'receipt.json').write_text(json.dumps(plan,indent=2)+'\n')
    return plan

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('job',type=Path)
    parser.add_argument('--render',action='store_true')
    argv = sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:]
    args = parser.parse_args(argv)
    source = args.job.resolve()
    job = json.loads(source.read_text())
    print(json.dumps((export if args.render else validate)(job,source.parent),indent=2))
