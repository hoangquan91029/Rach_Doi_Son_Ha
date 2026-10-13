"""One source-bound neutral Villager scene. Initial D0/D1 only; no rig/action."""
import bpy, math, json, hashlib, sys, time
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/art/pipeline/blender-villager-501/initial'
assert not OUT.exists(), 'Never overwrite or automatically retry initial renders'
assignment=json.loads((OUT.parent/'assignment.json').read_text())
for pin in assignment['inputs']:
    assert hashlib.sha256((ROOT/pin['path']).read_bytes()).hexdigest()==pin['sha256'],pin['path']
OUT.mkdir();start=time.monotonic()
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=32
scene.render.threads_mode='FIXED';scene.render.threads=2
scene.render.resolution_x=256;scene.render.resolution_y=256;scene.render.resolution_percentage=100
scene.render.film_transparent=True;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.image_settings.color_depth='8'
scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
scene.world.color=(.22,.22,.22)
# Fixed calibration chosen once from original full-canvas hat/root landmarks, before either render.
ORTHO=2.0;PIVOT=(654*256/1254,1140*256/1254);PPM=256/ORTHO
right=Vector((1/math.sqrt(2),1/math.sqrt(2),0));up=Vector((-.5/math.sqrt(2),.5/math.sqrt(2),math.sqrt(3)/2))
normal=Vector((math.sqrt(3)/2/math.sqrt(2),-math.sqrt(3)/2/math.sqrt(2),.5))
target=right*((128-PIVOT[0])/PPM)+up*((PIVOT[1]-128)/PPM)
bpy.ops.object.camera_add(location=target+normal*6);cam=bpy.context.object;cam.name='fixed_engine30_camera';cam.rotation_euler=(-normal).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=ORTHO;scene.camera=cam
bpy.ops.object.empty_add(type='PLAIN_AXES',location=(0,0,0));body=bpy.context.object;body.name='Villager_ground_root';body['source_identity']='villager';body['not_qualified']='neutral candidate only; no rig or motion'
source=bpy.data.images.load(str(ROOT/'docs/art/characters/villager-neutral-D00-screen-ESE/raw.png'));source.name='WHOLE_ORIGINAL_D0_NO_LIMB_TEXTURES';source.pack()
materials={}
def material(name,color,project=.72):
    if name in materials:return materials[name]
    m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;l=m.node_tree.links;n.clear()
    tex=n.new('ShaderNodeTexImage');tex.image=source;tex.interpolation='Linear';tex.extension='CLIP'
    blend=n.new('ShaderNodeMixRGB');blend.blend_type='MIX';blend.inputs[1].default_value=(*color,1)
    mul=n.new('ShaderNodeMath');mul.operation='MULTIPLY';mul.inputs[1].default_value=project;l.new(tex.outputs['Alpha'],mul.inputs[0]);l.new(mul.outputs[0],blend.inputs[0]);l.new(tex.outputs['Color'],blend.inputs[2])
    diffuse=n.new('ShaderNodeBsdfPrincipled');diffuse.inputs['Roughness'].default_value=.86;l.new(blend.outputs[0],diffuse.inputs['Base Color'])
    emission=n.new('ShaderNodeEmission');emission.inputs['Strength'].default_value=.85;l.new(blend.outputs[0],emission.inputs['Color'])
    mix=n.new('ShaderNodeMixShader');mix.inputs[0].default_value=.68;l.new(diffuse.outputs[0],mix.inputs[1]);l.new(emission.outputs[0],mix.inputs[2]);o=n.new('ShaderNodeOutputMaterial');l.new(mix.outputs[0],o.inputs[0]);materials[name]=m;return m
cream=material('cream_woven_crossover',(.63,.55,.40));dark=material('brown_baggy_trousers',(.12,.085,.059));sash=material('dark_wrapped_sash',(.10,.077,.062));skin=material('warm_matte_skin',(.47,.26,.12),.82);hair=material('black_hair_beard',(.025,.018,.012),.15);straw=material('woven_straw_hat',(.50,.34,.15),.80);rope=material('brown_sandal_rope',(.20,.105,.04),.25)
objects=[]
def finish(o,mat):
    o.parent=body;o.data.materials.append(mat);objects.append(o)
    for f in o.data.polygons:f.use_smooth=True
    return o

def uv_project(o):
    if o.type!='MESH':return
    layer=o.data.uv_layers.new(name='whole_original_D0_camera_projection')
    for face in o.data.polygons:
        for i in face.loop_indices:
            v=o.matrix_world@o.data.vertices[o.data.loops[i].vertex_index].co
            x=PIVOT[0]+v.dot(right)*PPM;y=PIVOT[1]-v.dot(up)*PPM
            layer.data[i].uv=(x/256,1-y/256)

def mesh(name,verts,faces,mat):
    d=bpy.data.meshes.new(name);d.from_pydata(verts,[],faces);d.update();o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);return finish(o,mat)

def loft(name,rings,mat,fold=.0):
    # Closed connected curved garment surface; broad folds in actual volume.
    N=64;verts=[]
    for j,(z,x,y,rx,ry) in enumerate(rings):
        for i in range(N):
            a=2*math.pi*i/N;f=1+fold*(math.sin(a*7+j*.63)+.35*math.sin(a*11-j*.7))
            verts.append((x+rx*math.cos(a)*f,y+ry*math.sin(a)*f,z))
    faces=[]
    for j in range(len(rings)-1):
        for i in range(N):faces.append((j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i))
    faces.extend([tuple(reversed(range(N))),tuple((len(rings)-1)*N+i for i in range(N))]);return mesh(name,verts,faces,mat)

def ellipsoid(name,loc,scale,mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48,ring_count=24,location=loc);o=bpy.context.object;o.name=name;o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);return finish(o,mat)

def tube(name,points,radii,mat,sides=16):
    pts=[Vector(v) for v in points];verts=[]
    for j,p in enumerate(pts):
        tangent=(pts[min(j+1,len(pts)-1)]-pts[max(0,j-1)]).normalized();a=tangent.cross(Vector((0,0,1)))
        if a.length<.01:a=tangent.cross(Vector((1,0,0)))
        a.normalize();b=tangent.cross(a).normalized()
        for i in range(sides):verts.append(tuple(p+radii[j]*(a*math.cos(i*2*math.pi/sides)+b*math.sin(i*2*math.pi/sides))))
    faces=[]
    for j in range(len(pts)-1):
        for i in range(sides):faces.append((j*sides+i,j*sides+(i+1)%sides,(j+1)*sides+(i+1)%sides,(j+1)*sides+i))
    faces.extend([tuple(reversed(range(sides))),tuple((len(pts)-1)*sides+i for i in range(sides))]);return mesh(name,verts,faces,mat)

# Full body volume, broad crossover garment and dark sash; model front +BlenderX.
loft('connected_torso_tunic',[(.62,-.025,0,.19,.27),(.68,-.025,0,.20,.265),(.79,-.02,0,.165,.22),(.94,-.01,0,.14,.21),(1.05,-.025,0,.155,.235),(1.22,-.045,0,.155,.27),(1.37,-.04,0,.14,.28),(1.45,-.04,0,.105,.22),(1.48,-.04,0,.085,.135)],cream,.04)
loft('wrapped_waist_sash',[(.98,-.01,0,.163,.219),(1.0,-.01,0,.167,.227),(1.035,-.01,0,.169,.231),(1.065,-.01,0,.157,.218)],sash,.015)
# Broad overlapping collar is curved solid geometry along diagonal front.
tube('crossover_lapel',[(.070,-.12,1.47),(.13,-.05,1.36),(.14,.05,1.24),(.155,.15,1.10)], [.024,.023,.022,.017],cream)
ellipsoid('sash_knot',(.16,-.12,1.015),(.038,.055,.045),sash)
loft('sash_tail_A',[(.70,.165,-.13,.025,.046),(.82,.17,-.13,.027,.040),(.98,.17,-.125,.02,.035),(1.025,.15,-.12,.020,.025)],sash,.025)
loft('sash_tail_B',[(.64,.13,-.18,.018,.035),(.76,.14,-.17,.024,.040),(.96,.15,-.15,.020,.031)],sash,.025)
# Physical leg IDs retained; cuffs never projected separate texture files.
for side in [-1,1]:
    y=side*.195
    loft(f'baggy_trouser_{side}',[(.36,-.015,y*1.12,.08,.080),(.42,-.025,y*1.14,.13,.115),(.51,-.035,y*1.10,.155,.13),(.64,-.035,y,.145,.125),(.77,-.04,y*.88,.125,.125),(.91,-.03,y*.72,.115,.13)],dark,.08)
    loft(f'calf_wrap_{side}',[(.085,.0,y*1.2,.052,.054),(.13,-.01,y*1.2,.062,.060),(.22,-.02,y*1.18,.059,.065),(.31,-.01,y*1.16,.071,.070),(.375,-.012,y*1.14,.082,.075)],cream,.025)
    for z in [.12,.18,.25,.33]:
        points=[(.06*math.cos(a),y*1.17+.068*math.sin(a),z+.01*math.sin(a)) for a in [2*math.pi*i/48 for i in range(49)]];tube(f'calf_tie_{side}_{z}',points,[.006]*49,rope,8)
    ellipsoid(f'foot_{side}',(.08,y*1.2,.065),(.14,.060,.055),skin)
    ellipsoid(f'sandal_sole_{side}',(.08,y*1.2,.025),(.155,.075,.02),rope)
    for j in range(5):ellipsoid(f'toe_{side}_{j}',(.20+.013*math.sin(j),y*1.2+(j-2)*.018,.042),(.034,.013,.021),skin)
    tube(f'sandal_front_strap_{side}',[(.15,y*1.2-.06,.044),(.15,y*1.2-.035,.087),(.135,y*1.2,.105),(.15,y*1.2+.035,.087),(.15,y*1.2+.06,.044)],[.009]*5,rope)
    tube(f'sandal_heel_strap_{side}',[(-.05,y*1.2-.055,.03),(-.04,y*1.2-.042,.10),(-.02,y*1.2,.12),(-.04,y*1.2+.042,.10),(-.05,y*1.2+.055,.03)],[.009]*5,rope)
    # Connected upper sleeve/cuff, warm forearm and gently curled hands.
    loft(f'rolled_sleeve_{side}',[(1.04,.01,side*.335,.075,.075),(1.10,-.02,side*.34,.085,.10),(1.22,-.04,side*.335,.097,.09),(1.35,-.045,side*.29,.10,.115),(1.425,-.045,side*.245,.095,.095)],cream,.045)
    loft(f'rolled_cuff_{side}',[(1.02,.025,side*.34,.082,.080),(1.045,.025,side*.34,.091,.09),(1.077,.015,side*.34,.084,.085)],cream,.025)
    tube(f'forearm_{side}',[(.022,side*.335,1.045),(.035,side*.35,.955),(.05,side*.345,.845),(.07,side*.34,.77)],[.054,.059,.049,.037],skin,32)
    ellipsoid(f'palm_{side}',(.07,side*.34,.735),(.042,.049,.060),skin)
    for j in range(4):tube(f'curved_finger_{side}_{j}',[(.085,side*.34+(j-1.5)*.018,.735),(.095,side*.34+(j-1.5)*.018,.699),(.077,side*.34+(j-1.5)*.018,.678)],[.013,.012,.008],skin)
    tube(f'thumb_{side}',[(.085,side*.34-side*.05,.755),(.11,side*.34-side*.06,.725),(.099,side*.34-side*.056,.706)],[.018,.015,.01],skin)
# Neck and sculpted head: rounded jaw/cheeks plus nose, eye sockets, brow/beard volumes.
loft('neck',[(1.40,-.02,0,.068,.072),(1.50,-.02,0,.065,.069),(1.57,-.025,0,.060,.073)],skin)
ellipsoid('organic_head',(-.035,0,1.645),(.105,.095,.155),skin)
ellipsoid('jaw',(.014,0,1.558),(.09,.080,.062),skin)
ellipsoid('nose_bridge',(.064,0,1.660),(.065,.021,.039),skin)
ellipsoid('nose_tip',(.108,0,1.631),(.024,.030,.023),skin)
for side in [-1,1]:
    ellipsoid(f'ear_{side}',(-.028,side*.092,1.65),(.026,.024,.049),skin)
    ellipsoid(f'eye_socket_{side}',(.052,side*.044,1.691),(.026,.028,.018),skin)
    tube(f'brow_{side}',[(.081,side*.016,1.718),(.075,side*.046,1.724),(.06,side*.069,1.717)],[.008,.009,.005],hair)
    ellipsoid(f'eye_{side}',(.078,side*.043,1.689),(.010,.015,.006),hair)
    tube(f'moustache_{side}',[(.091,side*.002,1.608),(.080,side*.020,1.610),(.06,side*.041,1.596)],[.009,.012,.006],hair)
ellipsoid('short_pointed_chin_beard',(.066,0,1.551),(.035,.039,.04),hair)
ellipsoid('hair_back',(-.070,0,1.73),(.087,.102,.090),hair)
# Straw hat is curved conical volume, brim binding, visible underside/ribs, chin cords.
loft('whole_woven_conical_hat',[(1.76,-.045,0,.375,.375),(1.775,-.045,0,.366,.366),(1.83,-.045,0,.276,.276),(1.89,-.045,0,.191,.191),(1.945,-.045,0,.103,.103),(1.993,-.045,0,.016,.016),(2.0,-.045,0,.001,.001)],straw,.0)
for rad,z in [(.374,1.765),(.28,1.83),(.19,1.891),(.103,1.946)]:
    pts=[(-.045+rad*math.cos(a),rad*math.sin(a),z) for a in [2*math.pi*i/96 for i in range(97)]];tube('hat_ring_'+str(rad),pts,[.005]*97,straw,8)
for i in range(24):
    a=2*math.pi*i/24;tube('straw_radial_rib_'+str(i),[(-.045+.012*math.cos(a),.012*math.sin(a),1.996),(-.045+.10*math.cos(a),.10*math.sin(a),1.95),(-.045+.25*math.cos(a),.25*math.sin(a),1.85),(-.045+.372*math.cos(a),.372*math.sin(a),1.772)],[.004]*4,straw,8)
for side in [-1,1]:tube('chin_hat_cord_'+str(side),[(.015,side*.1,1.755),(.04,side*.08,1.62),(.06,side*.025,1.55)],[.004]*3,rope,8)
# One whole original projection evaluated once in neutral D0 object coordinates.
bpy.context.view_layer.update()
for o in objects:
    if o.type=='MESH':uv_project(o)
for name,loc,energy,size in [('soft_key',(3,-4,5),120,5),('soft_fill',(-3,-1,3),65,5)]:
    bpy.ops.object.light_add(type='AREA',location=loc);l=bpy.context.object;l.name=name;l.data.energy=energy;l.data.size=size;l.rotation_euler=(Vector((0,0,1))-l.location).to_track_quat('-Z','Y').to_euler()
body.rotation_euler.z=0
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'villager-neutral501.blend'))
meta={'status':'UNREVIEWED_NEUTRAL_CANDIDATE','blender':bpy.app.version_string,'python':sys.version,'device':'CPU','samples':32,'threads':2,'canvas':[256,256],'pivot':PIVOT,'render':[42,42],'defaultZoom':1.68,'orthoScale':ORTHO,'gameUnitsPerBlenderMeter':42/(27*math.sqrt(2)*ORTHO),'elevationDegrees':30,'cameraLocation':list(cam.location),'cameraQuaternion':list(cam.rotation_euler.to_quaternion()),'cameraTarget':list(target),'engineXYtoBlender':'(x,-y,z)','physicalModelHeightMeters':2.0,'scaleCalibration':'One original root/hat landmark estimate before render; no per-direction or per-frame fit. Independent appearance match UNKNOWN.','source':assignment['inputs'][-2:],'wholeTexture':'packed canonicalD0 only; no separate limb files; sourcealpha ignored for opacity (solidgeometry), sourcecolor mixed with organic material','shadow':'body selfshading only; no groundplane or newshadowart. Candidate separate unit-contact-shadow policy','objects':len(objects),'meshVertices':sum(len(o.data.vertices) for o in objects),'meshFaces':sum(len(o.data.polygons) for o in objects),'rig':None,'motion':None,'appearanceApproval':False,'unseenRear':'PROPOSED reconstruction only'}
for d in [0,1]:
    body.rotation_euler.z=-d*math.pi/4;scene.render.filepath=str(OUT/f'neutral-D{d}.png');bpy.ops.render.render(write_still=True)
body.rotation_euler.z=0;bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'villager-neutral501.blend'));meta['elapsedSeconds']=time.monotonic()-start
(OUT/'scene-receipt.json').write_text(json.dumps(meta,indent=2)+'\n')
print('DONE',json.dumps({'outputs':str(OUT),'seconds':meta['elapsedSeconds'],'objects':meta['objects']}),flush=True)
