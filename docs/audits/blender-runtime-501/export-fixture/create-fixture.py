import bpy,math
from mathutils import Matrix,Vector
from pathlib import Path
p=Path(__file__).resolve().parent
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
s=bpy.context.scene;s.name='TechnicalScene'
collection=bpy.data.collections.new('TechnicalRender');s.collection.children.link(collection)
bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,radius=.5,location=(0,0,.5));model=bpy.context.object;model.name='TechnicalModel'
for c in list(model.users_collection):c.objects.unlink(model)
collection.objects.link(model)
bpy.ops.object.armature_add(location=(0,0,0));rig=bpy.context.object;rig.name='TechnicalRig';rig.data.bones[0].name='TechnicalBone'
mod=model.modifiers.new('TechnicalArmature','ARMATURE');mod.object=rig;vg=model.vertex_groups.new(name='TechnicalBone');vg.add(list(range(len(model.data.vertices))),1,'REPLACE')
rig.animation_data_create();bone=rig.pose.bones['TechnicalBone'];bone.rotation_mode='XYZ'
for frame in range(1,5):bone.rotation_euler=(0,0,0);bone.keyframe_insert('rotation_euler',frame=frame)
rig.animation_data.action.name='IdleAction'
bpy.ops.object.camera_add();camera=bpy.context.object;camera.name='TechnicalCamera';camera.data.type='ORTHO';camera.data.ortho_scale=256/(27*math.sqrt(2));s.camera=camera
right=Vector((2**-.5,2**-.5,0));up=Vector((-.5*2**-.5,.5*2**-.5,math.sqrt(3)/2));view=Vector((math.sqrt(3/8),-math.sqrt(3/8),.5));m=Matrix((right,up,view)).transposed().to_4x4();m.translation=view*10+up*(104/(27*math.sqrt(2)));camera.matrix_world=m
bpy.ops.object.light_add(type='AREA',location=(1,-3,4));bpy.context.object.data.energy=400;bpy.context.object.data.size=4
s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=4;s.render.threads_mode='FIXED';s.render.threads=2;s.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(p/'technical.blend'))
print('TECHNICAL_ONLY_NO_ART_QUALIFICATION',bpy.app.version_string,rig.animation_data.action.name,rig.animation_data.action_slot)
