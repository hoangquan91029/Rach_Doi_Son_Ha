"""Run only via actual isolated GUI Blender after root review; handshake-only."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys

REPO=Path(__file__).resolve().parents[3]
AUDIT=REPO/'docs/audits/blender-runtime-500/mcp'
ALLOW={'ping','get_addon_info','get_scene_info','get_telemetry_consent','get_polyhaven_status','get_hyper3d_status','get_sketchfab_status','get_polypizza_status','get_hunyuan3d_status','get_tripo_status'}

def main():
    import bpy
    if bpy.app.background:raise ValueError('actual GUI or virtual display required; background addon refuses socket')
    args=sys.argv[sys.argv.index('--')+1:]
    if len(args)!=1 or not args[0].isdigit() or not 1024<=int(args[0])<=65535:raise ValueError('one explicit port required')
    port=int(args[0])
    pins=json.loads((AUDIT/'upstream-pins.json').read_text())['files']
    source=AUDIT/'upstream/addon.py'
    expected=next(p['sha256'] for p in pins if p['path']=='addon.py')
    if hashlib.sha256(source.read_bytes()).hexdigest()!=expected:raise ValueError('reviewed addon drift')
    os.environ['BLENDERMCP_NO_UPDATE_CHECK']='1'
    # The addon requires requests even with integrations off; dependency must be reviewed.
    import requests
    def deny_request(*args,**kwargs):raise PermissionError('external integrations disabled by offline candidate')
    requests.sessions.Session.request=deny_request
    spec=importlib.util.spec_from_file_location('rds_reviewed_blender_mcp',source)
    addon=importlib.util.module_from_spec(spec);sys.modules[spec.name]=addon;spec.loader.exec_module(addon)
    # Never allow registration to schedule a listener or GitHub update lookup implicitly.
    addon._blendermcp_register_auto_start=lambda:None
    addon._addon_update_check_on_startup=lambda:None
    addon._telemetry_consent_enabled=lambda:False
    addon.register()
    for scene in bpy.data.scenes:
        scene.blendermcp_auto_start_server=False
        scene.blendermcp_port=port
        for name in ('polyhaven','hyper3d','sketchfab','polypizza','hunyuan3d','tripo'):
            setattr(scene,'blendermcp_use_'+name,False)
    addon.BlenderMCPServer.get_telemetry_consent=lambda self:{'consent':False}
    for name in ('polyhaven','hyper3d','sketchfab','polypizza','hunyuan3d'):
        setattr(addon.BlenderMCPServer,'get_'+name+'_status',lambda self:{'enabled':False,'message':'offline local-only candidate'})
    addon.premium_tripo_status=lambda:{'enabled':False,'message':'offline local-only candidate'}
    original=addon.BlenderMCPServer._execute_command_internal
    def restricted_command(self,command):
        if not isinstance(command,dict) or command.get('type') not in ALLOW:
            return {'status':'error','message':'handshake-only offline scope; command denied'}
        return original(self,command)
    addon.BlenderMCPServer._execute_command_internal=restricted_command
    # Status paths must never discover an inherited Premium license from the environment.
    addon.premium_active=lambda:False
    addon.premium_enabled_generators=lambda:[]
    server=addon.BlenderMCPServer(host='127.0.0.1',port=port)
    bpy.types.blendermcp_server=server
    server.start()
    if not server.running:raise RuntimeError('actual bridge failed to start')
    bpy.context.scene.blendermcp_server_running=True
    print('RDS offline handshake-only bridge started on 127.0.0.1:'+str(port),flush=True)

if __name__=='__main__':main()
