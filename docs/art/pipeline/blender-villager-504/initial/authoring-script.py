"""CANDIDATE ONLY. No execution permitted until separate root render authorization.
Different504 control: two-view constrained garment sections, semantic materials,
source-face-local UV on a curved facial shell, no global image projection.
"""
import math,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
CONTROL=ROOT/'docs/art/pipeline/blender-villager-504/control.json'
def verify():
    record=json.loads(CONTROL.read_text())
    for pin in record['sourcePins']:
        assert hashlib.sha256((ROOT/pin['path']).read_bytes()).hexdigest()==pin['sha256'],pin['path']
    return record

def build_candidate(output,authorization):
    # Caller/root supplies a separate durable finite render decision; no auto-run.
    c=verify()
    assert authorization.get('taskId')=='villager-control504'
    assert authorization.get('decision')=='AUTHOR_NEUTRAL_SCENE'
    assert authorization.get('controlSHA256')==hashlib.sha256(CONTROL.read_bytes()).hexdigest()
    assert authorization.get('renderDirections')==[0,1]
    output=Path(output).resolve();assert not output.exists();output.mkdir()
    import bpy
    from mathutils import Vector
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=32
    scene.render.threads_mode='FIXED';scene.render.threads=2;scene.render.resolution_x=scene.render.resolution_y=256
    scene.render.resolution_percentage=100;scene.render.film_transparent=True
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None'
    bpy.ops.object.empty_add();root=bpy.context.object;root.name='original_Villager_root'
    mats={}
    def principled(material):
        nodes=[node for node in material.node_tree.nodes if node.type=='BSDF_PRINCIPLED']
        assert len(nodes)==1, 'Exactly one Principled node required'
        node=nodes[0]
        assert all(name in node.inputs for name in ['Base Color','Roughness']), 'Required Principled sockets missing'
        return node
    # Region material colors are visual proposals; source-texture never placed on clothes/hands.
    for name,color in c['materials'].items():
        m=bpy.data.materials.new(name);m.use_nodes=True;p=principled(m)
        p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=.9;mats[name]=m
    def surface(name,rings,material,fold=0):
        vertices=[];n=64
        for j,(z,x,y,depth,width) in enumerate(rings):
            for i in range(n):
                a=2*math.pi*i/n;f=1+fold*math.sin(6*a+j*.45)
                vertices.append((x+depth*math.cos(a)*f,y+width*math.sin(a)*f,z))
        faces=[]
        for j in range(len(rings)-1):
            for i in range(n):faces.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
        faces += [tuple(reversed(range(n))),tuple((len(rings)-1)*n+i for i in range(n))]
        mesh=bpy.data.meshes.new(name);mesh.from_pydata(vertices,[],faces);mesh.update()
        o=bpy.data.objects.new(name,mesh);scene.collection.objects.link(o);o.parent=root;o.data.materials.append(mats[material])
        for face in mesh.polygons:face.use_smooth=True
        return o
    # Each section uses manual D1 lateral and D0 oblique garment landmarks.
    # Fit depth from D0 width with D1 lateral halfwidth: w0²=(depth²+width²)/2.
    # Heights are authored from source landmark ordering, not per-frame fitting.
    fitted=[]
    for row in c['torsoSections']:
        w1=row['D1HalfWidthPx']/c['pixelsPerMeter'];w0=row['D0HalfWidthPx']/c['pixelsPerMeter']
        depth=math.sqrt(max(.004,2*w0*w0-w1*w1))
        fitted.append([row['z'],0,0,depth,w1])
    surface('two_view_constrained_cream_tunic',fitted,'cream',.028)
    # Crossover is volumetric solid edge ribbon integrated visually with semantic cloth.
    surface('crossover_lapel',[[1.18,.145,.12,.012,.020],[1.35,.12,0,.014,.022],[1.51,.08,-.10,.012,.020]],'cream')
    surface('waist_sash',[[1.05,0,0,.125,.185],[1.12,0,0,.133,.191],[1.16,0,0,.122,.18]],'sash',.015)
    for side in [-1,1]:
        y=side*.15
        surface('trouser_'+str(side),[[.36,0,y,.067,.070],[.44,0,y,.092,.093],[.57,0,y,.113,.10],[.73,0,y*.95,.105,.093],[.88,0,y*.85,.09,.085]],'trousers',.038)
        surface('calfwrap_'+str(side),[[.10,.018,y,.043,.049],[.22,.005,y,.050,.054],[.36,0,y,.063,.064]],'cream',.020)
        surface('open_sandal_foot_'+str(side),[[.025,.055,y,.095,.048],[.055,.06,y,.098,.047],[.086,.035,y,.060,.045],[.105,.015,y,.038,.043]],'skin')
        surface('sandal_sole_'+str(side),[[.012,.06,y,.103,.055],[.027,.06,y,.103,.055]],'rope')
        surface('sleeve_'+str(side),[[1.13,0,side*.27,.071,.068],[1.22,-.01,side*.28,.087,.080],[1.39,-.015,side*.23,.09,.085],[1.48,-.01,side*.19,.069,.069]],'cream',.028)
        surface('rolled_cuff_'+str(side),[[1.11,.01,side*.27,.073,.075],[1.15,.01,side*.27,.082,.081],[1.18,0,side*.27,.072,.075]],'cream',.01)
        surface('connected_forearm_hand_'+str(side),[[.78,.025,side*.28,.027,.032],[.83,.038,side*.28,.033,.040],[.88,.035,side*.28,.029,.033],[1.02,.018,side*.28,.041,.047],[1.14,.01,side*.27,.044,.044]],'skin')
        surface('sash_tail_'+str(side),[[.75,.128,.095+side*.020,.011,.025],[.93,.137,.105+side*.023,.015,.031],[1.13,.132,.11,.013,.022]],'sash',.02)
    # D1 root -45deg maps local+Y to image-right. Original knot atx700 vscenter635.
    surface('source_offcenter_sash_knot',[[1.055,.130,.110,.016,.021],[1.075,.153,.110,.030,.035],[1.110,.160,.110,.026,.033],[1.145,.132,.110,.014,.020]],'sash',.015)
    surface('neck',[[1.45,0,0,.055,.059],[1.58,0,0,.052,.057]],'skin')
    surface('back_head_hair',[[1.55,-.028,0,.049,.058],[1.65,-.036,0,.075,.08],[1.75,-.038,0,.080,.083],[1.80,-.038,0,.065,.065]],'hair')
    # Macro sourcehead landmarks remain geometric even without facial texture.
    surface('source_jaw_chin',[[1.545,.040,0,.025,.030],[1.58,.037,0,.040,.050],[1.63,.033,0,.040,.069]],'skin')
    surface('source_nose_bridge',[[1.645,.080,0,.019,.024],[1.68,.095,0,.023,.019],[1.72,.065,0,.015,.014]],'skin')
    surface('source_goatee',[[1.535,.064,0,.014,.015],[1.565,.070,0,.019,.024],[1.589,.069,0,.015,.026]],'hair')
    # ONE full originalSouth image, semantic face window only on curved volumetric front.
    # No texture derivative/cutout file; no alpha-driven geometry or material transparency.
    faceverts=[];uvs=[];N=32;M=24;box=c['faceSourceD1Px']
    for j in range(M+1):
        v=j/M;z=1.55+.235*v;half=.058+.024*math.sin(math.pi*v)
        for i in range(N+1):
            u=i/N;y=(u-.5)*2*half;x=.046+.040*math.sqrt(max(0,1-((u-.5)*2)**2))
            faceverts.append((x,y,z));uvs.append(((box[0]+u*(box[2]-box[0]))/1254,1-(box[3]-v*(box[3]-box[1]))/1254))
    faces=[(j*(N+1)+i,j*(N+1)+i+1,(j+1)*(N+1)+i+1,(j+1)*(N+1)+i) for j in range(M) for i in range(N)]
    mesh=bpy.data.meshes.new('curved_source_face');mesh.from_pydata(faceverts,[],faces);mesh.update();o=bpy.data.objects.new('curved_source_face',mesh);scene.collection.objects.link(o);o.parent=root
    layer=mesh.uv_layers.new(name='semantic_face_originalSouth');layer.active_render=True
    for poly in mesh.polygons:
        poly.use_smooth=True
        for li in poly.loop_indices:layer.data[li].uv=uvs[mesh.loops[li].vertex_index]
    m=bpy.data.materials.new('originalSouth_face_only');m.use_nodes=True;n=m.node_tree.nodes;l=m.node_tree.links
    tex=n.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(ROOT/c['sourcePins'][1]['path']));tex.image.pack()
    uv=n.new('ShaderNodeUVMap');uv.uv_map=layer.name;l.new(uv.outputs[0],tex.inputs['Vector']);p=principled(m);l.new(tex.outputs['Color'],p.inputs['Base Color']);p.inputs['Roughness'].default_value=.93;o.data.materials.append(m)
    face_thickness=o.modifiers.new('face_actual_surface_thickness','SOLIDIFY');face_thickness.thickness=.016
    # Open facial exposure is a geometric rule, not a fixed fullhat tilt retry.
    # Front +X brim is lifted locally; back brim keeps source silhouette. Cone shallower than501.
    hat=[];K=64;R=12
    for j in range(R+1):
        t=j/R;r=.273*(1-t);z=1.78+.235*t
        for i in range(K):
            a=2*math.pi*i/K;front=max(0,math.cos(a));hat.append((-.025+r*math.cos(a),r*math.sin(a),z+.105*front*(1-t)**2))
    faces=[(j*K+i,j*K+(i+1)%K,(j+1)*K+(i+1)%K,(j+1)*K+i) for j in range(R) for i in range(K)]
    mesh=bpy.data.meshes.new('source_hat_exposure_surface');mesh.from_pydata(hat,[],faces);mesh.update();o=bpy.data.objects.new('source_hat_exposure_surface',mesh);scene.collection.objects.link(o);o.parent=root;o.data.materials.append(mats['straw'])
    for poly in mesh.polygons:poly.use_smooth=True
    thick=o.modifiers.new('woven_hat_actual_thickness','SOLIDIFY');thick.thickness=.008
    # Camera/root/pivot frozen from family before any render. No per-direction adjustment.
    q=math.sqrt(2);right=Vector((1/q,1/q,0));up=Vector((-.5/q,.5/q,math.sqrt(3)/2));normal=Vector((math.sqrt(3)/2/q,-math.sqrt(3)/2/q,.5))
    pivot=c['pivot'];ppm=c['pixelsPerMeter'];target=right*((128-pivot[0])/ppm)+up*((pivot[1]-128)/ppm)
    bpy.ops.object.camera_add(location=target+normal*6);cam=bpy.context.object;cam.data.type='ORTHO';cam.data.ortho_scale=c['orthoScale'];cam.rotation_euler=(-normal).to_track_quat('-Z','Y').to_euler();scene.camera=cam
    for loc,energy in [((3,-4,5),230),((-3,-1,3),140)]:
        bpy.ops.object.light_add(type='AREA',location=loc);l=bpy.context.object;l.data.energy=energy;l.data.size=5;l.rotation_euler=(Vector((0,0,1))-l.location).to_track_quat('-Z','Y').to_euler()
    scene.world.color=(.2,.2,.2)
    bpy.ops.wm.save_as_mainfile(filepath=str(output/'candidate.blend'))
    # Rendering intentionally separate. This function saves scene, never calls render.
    (output/'candidate-control.json').write_text(json.dumps({'control':c,'rendered':False,'appearance':'UNKNOWN','faceIdentity':'UNKNOWN until actualD0/D1 review','unseenRear':'PROPOSED'},indent=2)+'\n')
    return root,scene
if __name__=='__main__':
    raise SystemExit('504 code is review-only. Root must issue separate finite authoring/render authorization; no automatic Blender execution.')
