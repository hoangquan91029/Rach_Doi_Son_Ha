import bpy,sys,time,json
from pathlib import Path
start=time.monotonic()
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,location=(0,0,0));sphere=bpy.context.object
mat=bpy.data.materials.new('technical-blue');mat.diffuse_color=(0.08,0.3,0.8,1);sphere.data.materials.append(mat)
bpy.ops.object.camera_add(location=(0,-5,2));cam=bpy.context.object;cam.rotation_euler=(1.1903,0,0);cam.data.type='ORTHO';cam.data.ortho_scale=3.4
bpy.ops.object.light_add(type='AREA',location=(1,-3,4));bpy.context.object.data.energy=450;bpy.context.object.data.shape='DISK';bpy.context.object.data.size=4
s=bpy.context.scene;s.camera=cam;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=8;s.render.resolution_x=256;s.render.resolution_y=256;s.render.resolution_percentage=100;s.render.film_transparent=True;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.filepath=str(Path(__file__).resolve().parent/'fixture.png');s.render.threads_mode='FIXED';s.render.threads=2
print('RUNTIME',json.dumps({'blender':bpy.app.version_string,'python':sys.version,'device':s.cycles.device,'output':s.render.filepath}),flush=True)
bpy.ops.render.render(write_still=True)
print('ELAPSED',time.monotonic()-start,flush=True)
