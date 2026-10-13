"""Own-process supervisor: finite GUI+SDK handshake, closes only its own handles."""
import hashlib
import json
import os
from pathlib import Path
import signal
import socket
import subprocess
import time
repo=Path(__file__).resolve().parents[3]
out=repo/'docs/audits/blender-runtime-501/handshake'
cap=json.loads((repo/'docs/audits/blender-runtime-500/capability/CHECKPOINT.json').read_text())
binary=Path(cap['runtime']['binary'])
if hashlib.sha256(binary.read_bytes()).hexdigest()!=cap['runtime']['binarySha256']:raise ValueError('actual Blenderbinary drift')
python='/home/kieu-hoang-quan/.local/share/rach-doi-son-ha/tools/mcp501/venv/bin/python'
env=os.environ.copy();env.update(cap['runtime']['checks']['environmentOverrides'])
# New private resources, no user preferences or startup scene.
env.update({'BLENDER_USER_CONFIG':str(out/'private-config'),'BLENDER_USER_SCRIPTS':str(out/'private-scripts'),'BLENDERMCP_NO_UPDATE_CHECK':'1','BLENDER_MCP_DISABLE_TELEMETRY':'1','DISABLE_TELEMETRY':'1','MCP_DISABLE_TELEMETRY':'1','LIBGL_ALWAYS_SOFTWARE':'1'})
port=19876
probe=socket.socket();probe.settimeout(.2)
if probe.connect_ex(('127.0.0.1',port))==0:raise ValueError('selectedport alreadyowned; no replacement')
probe.close()
argv=[str(binary),'--factory-startup','--disable-autoexec','--python',str(repo/'scripts/blender/mcp501/addon_launcher.py'),'--',str(port)]
receipt={'blenderArgv':argv,'environmentOverrides':{k:env[k] for k in cap['runtime']['checks']['environmentOverrides']},'ownedPID':None,'ready':False,'SDKExit':None,'allOwnedClosed':False}
with (out/'gui.log').open('w') as log:
 process=subprocess.Popen(argv,cwd=out,env=env,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
 receipt['ownedPID']=process.pid
 try:
  deadline=time.monotonic()+25
  while time.monotonic()<deadline:
   if process.poll() is not None:raise RuntimeError('actualGUIBlender exited '+str(process.returncode))
   # No command injection: OS listener inspection, then actual SDK obtains data.
   listening=subprocess.run(['ss','-ltnp'],capture_output=True,text=True,check=True).stdout
   if f'127.0.0.1:{port}' in listening and f'pid={process.pid},' in listening:
    (out/'listener.log').write_text(listening);receipt['ready']=True;break
   time.sleep(.25)
  if not receipt['ready']:raise TimeoutError('actualGUI bridge listener timeout')
  with (out/'sdk.log').open('w') as sdklog:
   sdk=subprocess.run([python,str(repo/'scripts/blender/mcp501/sdk_handshake.py')],cwd=repo,stdout=sdklog,stderr=subprocess.STDOUT,timeout=35)
  receipt['SDKExit']=sdk.returncode
  if sdk.returncode!=0:raise RuntimeError('actualSDK handshake failed')
  (out/'connections.log').write_text(subprocess.run(['ss','-tnp'],capture_output=True,text=True,check=True).stdout)
 except Exception as e:
  receipt['failure']=str(e)
 finally:
  if process.poll() is None:os.killpg(process.pid,signal.SIGTERM)
  try:process.wait(timeout=5)
  except subprocess.TimeoutExpired:os.killpg(process.pid,signal.SIGKILL);process.wait(timeout=5)
  receipt['BlenderExit']=process.returncode
  listening=subprocess.run(['ss','-ltnp'],capture_output=True,text=True,check=True).stdout
  (out/'listener-closed.log').write_text(listening)
  receipt['allOwnedClosed']=f'127.0.0.1:{port}' not in listening and process.poll() is not None
  (out/'actual-run.json').write_text(json.dumps(receipt,indent=2)+'\n')
if receipt.get('failure'):raise RuntimeError(receipt['failure'])
