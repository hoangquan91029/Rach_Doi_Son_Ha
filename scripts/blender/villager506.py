"""506 SOURCE GARMENT CODE ONLY. No bpy imported or executed at module import.
Actual sewn-panel geometry and canonical corresponding-region UV; NOT global
camera projection, plain palette mannequin, alpha card or old501/504 retry.
"""
from pathlib import Path
import json,hashlib,math
ROOT=Path(__file__).resolve().parents[2]
CONTROL=ROOT/'docs/art/pipeline/blender-villager-506/control.json'
def source_controls():
    c=json.loads(CONTROL.read_text())
    for p in c['inputPins']:
        assert hashlib.sha256((ROOT/p['path']).read_bytes()).hexdigest()==p['sha256'],p['path']
    return c

def author_scene(output,authorization):
    c=source_controls()
    assert authorization.get('taskId')=='source-garment506'
    assert authorization.get('decision')=='AUTHOR_SOURCE_GARMENT'
    assert authorization.get('controlSHA256')==hashlib.sha256(CONTROL.read_bytes()).hexdigest()
    out=Path(output).resolve();assert not out.exists();out.mkdir()
    import bpy
    from mathutils import Vector
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    scene=bpy.context.scene
    bpy.ops.object.empty_add();root=bpy.context.object;root.name='source_Villager_groundroot'
    whole=bpy.data.images.load(str(ROOT/c['canonicalD1']['path']));whole.pack();whole.name='ONE_WHOLE_CANONICAL_D1'
    def node_principled(m):
        nodes=[n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'];assert len(nodes)==1
        p=nodes[0];assert all(k in p.inputs for k in ['Base Color','Roughness']);return p
    mats={}
    for name,color in c['fallbackRegionColors'].items():
        m=bpy.data.materials.new(name);m.use_nodes=True;p=node_principled(m);p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=.9
        if name in c['texturedRegions']:
            tex=m.node_tree.nodes.new('ShaderNodeTexImage');tex.image=whole;tex.extension='EXTEND';tex.interpolation='Linear'
            uv=m.node_tree.nodes.new('ShaderNodeUVMap');uv.uv_map='source_correspondence_'+name
            m.node_tree.links.new(uv.outputs['UV'],tex.inputs['Vector']);m.node_tree.links.new(tex.outputs['Color'],p.inputs['Base Color'])
            # Source already painted realistic values: preserve most without plastic lighting.
            emission=m.node_tree.nodes.new('ShaderNodeEmission');emission.inputs['Strength'].default_value=.8;m.node_tree.links.new(tex.outputs['Color'],emission.inputs['Color'])
            mix=m.node_tree.nodes.new('ShaderNodeMixShader');mix.inputs[0].default_value=.45;m.node_tree.links.new(p.outputs[0],mix.inputs[1]);m.node_tree.links.new(emission.outputs[0],mix.inputs[2]);m.node_tree.links.new(mix.outputs[0],m.node_tree.nodes.get('Material Output').inputs['Surface'])
        mats[name]=m
    def sewn(name,verts,faces,uvs,region,thickness=.012):
        data=bpy.data.meshes.new(name);data.from_pydata(verts,[],faces);data.update();obj=bpy.data.objects.new(name,data);scene.collection.objects.link(obj);obj.parent=root;data.materials.append(mats[region])
        if uvs:
            layer=data.uv_layers.new(name='source_correspondence_'+region);layer.active_render=True;data.uv_layers.active=layer
            for poly in data.polygons:
                for li in poly.loop_indices:
                    u,v=uvs[data.loops[li].vertex_index];layer.data[li].uv=(u/1254,1-v/1254)
        for poly in data.polygons:poly.use_smooth=True
        if thickness:
            mod=obj.modifiers.new('actual_fabric_thickness','SOLIDIFY');mod.thickness=thickness
        return obj
    def panel(name,rows,region):
        # Each row has explicit modelZ,left/rightY,frontDepth and corresponding
        # original left/right pixels. Rows differ at Vneck and flaring hem.
        N=48;verts=[];uvs=[]
        for j,row in enumerate(rows):
            z,yl,yr,depth,pxl,pxr,py=row
            for i in range(N+1):
                u=i/N;y=yl+(yr-yl)*u
                # actual panel curvature wraps around torso; broad drape folds.
                edge=(2*u-1);x=depth-.07*edge*edge+.009*math.sin(4*math.pi*u+j*.8)
                verts.append((x,y,z+.004*math.sin(3*math.pi*u+j*.4)));uvs.append((pxl+(pxr-pxl)*u,py))
        faces=[(j*(N+1)+i,j*(N+1)+i+1,(j+1)*(N+1)+i+1,(j+1)*(N+1)+i) for j in range(len(rows)-1) for i in range(N)]
        return sewn(name,verts,faces,uvs,region)
    # TWO independent thick sewn front panels create actual V opening, overlap
    # beneath diagonal lapel, drape flare and unequal physical hems.
    for name in ['under_front','over_front','lapel_under','lapel_over']:
        panel(name,c['panels'][name],'cream')
    # Continuous back/side garment wraps sewnfront edges; source rear unknown,
    # neutral fabric source patch only, never claim original rear artwork.
    def volume(name,rings,region,box,fold=.02):
        N=64;verts=[];uvs=[]
        for j,(z,cx,cy,rx,ry) in enumerate(rings):
            for i in range(N):
                a=2*math.pi*i/N;f=1+fold*math.sin(6*a+j*.6)
                verts.append((cx+rx*math.cos(a)*f,cy+ry*math.sin(a)*f,z))
                # Region correspondence by physical horizontal lane and garment
                # axial coordinate; one wholeimage, not separatepartimage.
                u=(math.sin(a)+1)/2;v=j/(len(rings)-1)
                uvs.append((box[0]+u*(box[2]-box[0]),box[3]-v*(box[3]-box[1])))
        faces=[(j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i) for j in range(len(rings)-1) for i in range(N)]
        faces += [tuple(reversed(range(N))),tuple((len(rings)-1)*N+i for i in range(N))]
        return sewn(name,verts,faces,uvs,region,0)
    # Back is halfshell so it cannot fill the openfrontV or cover real lapels.
    N=48;verts=[];uvs=[]
    for j,(z,depth,width,py) in enumerate(c['backShellRows']):
        for i in range(N+1):
            a=math.pi/2+math.pi*i/N;verts.append((depth*math.cos(a),width*math.sin(a),z));uvs.append((500+200*i/N,py))
    faces=[(j*(N+1)+i,j*(N+1)+i+1,(j+1)*(N+1)+i+1,(j+1)*(N+1)+i) for j in range(len(c['backShellRows'])-1) for i in range(N)]
    sewn('continuous_side_back_tunic',verts,faces,uvs,'cream')
    # Bare chest extends above actualVneck; cloth never paints chestclosed.
    volume('bare_neck_chest',[[1.38,0,0,.061,.075],[1.48,0,0,.068,.083],[1.57,0,0,.052,.055]],'skin',c['regions']['chest'],0)
    # Wrapped sash has layered wrap offsets and actualoffcenterknot, notdarkstripe.
    for i in range(3):
        z=1.025+i*.031;volume('sash_wrap_'+str(i),[[z,0,0,.151,.196],[z+.038,0,0,.158,.204]],'sash',c['regions']['sash'],.006)
    volume('sash_knot',[[1.03,.154,.112,.019,.026],[1.075,.173,.112,.031,.036],[1.13,.152,.112,.019,.025]],'sash',c['regions']['knot'],.025)
    for name in ['tail_long','tail_short']:panel(name,c['panels'][name],'sash')
    for side in [-1,1]:
        lane='left' if side<0 else 'right';y=side*.17
        volume('baggy_trousers_'+lane,[[.35,0,y,.064,.068],[.43,-.01,y,.09,.103],[.57,-.015,y,.119,.120],[.72,-.014,y,.121,.109],[.83,-.008,y*.9,.10,.095]],'trousers',c['regions']['trouser_'+lane],.042)
        volume('calfwrap_'+lane,[[.09,.015,y,.045,.045],[.20,.008,y,.052,.057],[.35,0,y,.066,.065]],'wrap',c['regions']['wrap_'+lane],.015)
        volume('open_sandal_'+lane,[[.02,.066,y,.104,.057],[.055,.063,y,.106,.055],[.093,.032,y,.07,.046],[.11,.016,y,.042,.043]],'skin',c['regions']['sandal_'+lane],0)
        volume('sleeve_'+lane,[[1.025,0,side*.292,.078,.072],[1.11,-.02,side*.298,.09,.095],[1.26,-.023,side*.27,.101,.108],[1.415,-.02,side*.226,.082,.088]],'cream',c['regions']['sleeve_'+lane],.036)
        volume('rolled_cuff_'+lane,[[1.02,.01,side*.292,.080,.084],[1.065,.015,side*.292,.089,.091],[1.10,0,side*.292,.078,.081]],'cream',c['regions']['cuff_'+lane],.01)
        volume('forearm_hand_'+lane,[[.71,.045,side*.29,.029,.037],[.79,.045,side*.29,.038,.045],[.88,.032,side*.29,.035,.04],[1.02,.01,side*.292,.045,.05]],'skin',c['regions']['arm_'+lane],0)
    # Closed samehead volume with geometric brow/nose/jaw and D1 semantic face.
    volume('source_face_head',[[1.55,.025,0,.042,.044],[1.59,.020,0,.075,.065],[1.68,0,0,.094,.079],[1.76,-.008,0,.077,.074],[1.79,-.009,0,.05,.058]],'face',c['regions']['face'],0)
    volume('nose_volume',[[1.64,.081,0,.018,.022],[1.68,.10,0,.022,.018],[1.72,.075,0,.012,.014]],'skin',c['regions']['nose'],0)
    volume('goatee_volume',[[1.535,.062,0,.012,.017],[1.565,.071,0,.020,.026],[1.59,.066,0,.015,.023]],'hair',c['regions']['beard'],0)
    # Actual sourcepointedcrown, nonflat brim with exposedface corridor. Nohattilt.
    volume('pointed_conical_hat',[[1.80,-.025,0,.284,.284],[1.845,-.025,0,.239,.239],[1.93,-.025,0,.13,.13],[2.025,-.025,0,.003,.003]],'straw',c['regions']['hat'],0)
    # Cutaway of frontbrim is NOT alpha/card: minimumfrontsurfaceheight geometric.
    hat=scene.objects['pointed_conical_hat']
    for v in hat.data.vertices:
        if v.co.x>-.025 and v.co.z<1.865:v.co.z+=.06*max(0,(v.co.x+.025)/.284)
    # Fixedfamilycamera nofit. WorldBlender handedness sameas priorenginebasis.
    q=math.sqrt(2);right=Vector((1/q,1/q,0));up=Vector((-.5/q,.5/q,math.sqrt(3)/2));normal=Vector((math.sqrt(3)/2/q,-math.sqrt(3)/2/q,.5))
    pivot=c['pivot'];ppm=256/c['orthoScale'];target=right*((128-pivot[0])/ppm)+up*((pivot[1]-128)/ppm)
    bpy.ops.object.camera_add(location=target+normal*6);cam=bpy.context.object;cam.data.type='ORTHO';cam.data.ortho_scale=c['orthoScale'];cam.rotation_euler=(-normal).to_track_quat('-Z','Y').to_euler();scene.camera=cam
    for loc,power in [((3,-4,5),180),((-3,-1,3),110)]:
        bpy.ops.object.light_add(type='AREA',location=loc);light=bpy.context.object;light.data.energy=power;light.data.size=5;light.rotation_euler=(Vector((0,0,1))-light.location).to_track_quat('-Z','Y').to_euler()
    scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=32;scene.render.threads_mode='FIXED';scene.render.threads=2
    scene.render.resolution_x=scene.render.resolution_y=256;scene.render.resolution_percentage=100;scene.render.film_transparent=True;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None'
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'source_garment_candidate.blend'))
    (out/'source-control.json').write_text(json.dumps({'control':c,'rendered':False,'appearance':'UNKNOWN','rear':'PROPOSED','textureFiles':[c['canonicalD1']['path']]},indent=2)+'\n')
    return root,scene
if __name__=='__main__':raise SystemExit('506 CODE_ONLY. Separate root authoring/render authorization required; no execution or render permitted.')
