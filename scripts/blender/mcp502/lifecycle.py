#!/usr/bin/env python3
"""Owned lifecycle STDIO launcher for the reviewed read-only Blender MCP fork."""
import hashlib
import json
import os
from pathlib import Path
import signal
import socket
import subprocess
import sys
import time
import uuid

REPO=Path(__file__).resolve().parents[3]
BASE=REPO/'docs/audits/blender-runtime-502/connection'
PYTHON='/home/kieu-hoang-quan/.local/share/rach-doi-son-ha/tools/mcp501/venv/bin/python'
PORT=19876
PINS={
 'scripts/blender/mcp500/offline_addon_candidate.py':'219a496eda7248dfada013b5c83ce5e3356da590cbf24493dadb65ca92f03c7c',
 'scripts/blender/mcp500/offline_server_candidate.py':'95ccf3d3ee9c88ccd09751530359ff17d36cb35c0e107fdf0787afae8fb5720b',
 'scripts/blender/mcp501/addon_launcher.py':'010e97960179897f6fe079a36d10d02dd97a57ad4e2c072b79d95e59ce55c67a',
 'docs/audits/blender-runtime-500/capability/CHECKPOINT.json':'5c0e3540553cf4d509a74953e59d8968d251e031581edb03fdb114ba79f4eea7',
}
STOP=False

def signal_stop(signum,frame):
 global STOP
 STOP=True

def owned_close(process):
 if process is None:return
 if process.poll() is None:
  try:os.killpg(process.pid,signal.SIGTERM)
  except ProcessLookupError:pass
 try:process.wait(timeout=1.5)
 except subprocess.TimeoutExpired:
  try:os.killpg(process.pid,signal.SIGKILL)
  except ProcessLookupError:pass
  process.wait(timeout=1.5)

def listeners():
 return subprocess.check_output(['ss','-ltnp'],text=True)

def main():
 global STOP
 for name,sha in PINS.items():
  if hashlib.sha256((REPO/name).read_bytes()).hexdigest()!=sha:raise ValueError('reviewed source drift: '+name)
 if Path(sys.prefix).resolve()!=Path(PYTHON).parent.parent.resolve():raise ValueError('actual reviewed venv Python required')
 cap=json.loads((REPO/'docs/audits/blender-runtime-500/capability/CHECKPOINT.json').read_text())
 binary=Path(cap['runtime']['binary'])
 if hashlib.sha256(binary.read_bytes()).hexdigest()!=cap['runtime']['binarySha256']:raise ValueError('Blenderbinary drift')
 probe=socket.socket();probe.settimeout(.2)
 try:
  if probe.connect_ex(('127.0.0.1',PORT))==0:raise ValueError('selected loopbackport occupied; unrelatedprocess untouched')
 finally:probe.close()
 run=BASE/'runs'/uuid.uuid4().hex
 run.mkdir(parents=True,mode=0o700)
 env=os.environ.copy();env.update(cap['runtime']['checks']['environmentOverrides'])
 env.update({'BLENDER_USER_CONFIG':str(run/'private-config'),'BLENDER_USER_SCRIPTS':str(run/'private-scripts'),'BLENDERMCP_NO_UPDATE_CHECK':'1','BLENDER_MCP_DISABLE_TELEMETRY':'1','DISABLE_TELEMETRY':'1','MCP_DISABLE_TELEMETRY':'1','LIBGL_ALWAYS_SOFTWARE':'1','PYTHONDONTWRITEBYTECODE':'1'})
 receipt={'schema':'rds-owned-stdio/v1','runDirectory':str(run),'port':PORT,'GUIpid':None,'serverPID':None,'ready':False,'closed':False,'failure':None}
 gui=server=None
 for sig in (signal.SIGTERM,signal.SIGINT):signal.signal(sig,signal_stop)
 try:
  with (run/'gui.log').open('w') as gui_log:
   os.chmod(run/'gui.log',0o600)
   argv=[str(binary),'--factory-startup','--disable-autoexec','--python',str(REPO/'scripts/blender/mcp501/addon_launcher.py'),'--',str(PORT)]
   gui=subprocess.Popen(argv,cwd=run,env=env,stdout=gui_log,stderr=subprocess.STDOUT,start_new_session=True)
   receipt['GUIpid']=gui.pid
   deadline=time.monotonic()+25
   while time.monotonic()<deadline and not STOP:
    if gui.poll() is not None:raise RuntimeError('ownedGUI exited '+str(gui.returncode))
    snapshot=listeners()
    if f'127.0.0.1:{PORT}' in snapshot and f'pid={gui.pid},' in snapshot:
     (run/'listener.log').write_text(snapshot);receipt['ready']=True;break
    time.sleep(.1)
   if STOP:return
   if not receipt['ready']:raise TimeoutError('ownedGUI loopbacklistener timeout25s')
   # STDIO protocol stays on inherited stdin/stdout. GUI and server diagnostics never use stdout.
   server=subprocess.Popen([PYTHON,str(REPO/'scripts/blender/mcp500/offline_server_candidate.py'),'--port',str(PORT)],cwd=REPO,env=env,stdin=sys.stdin.buffer,stdout=sys.stdout.buffer,stderr=sys.stderr.buffer,start_new_session=True)
   receipt['serverPID']=server.pid
   while not STOP and server.poll() is None:
    if gui.poll() is not None:raise RuntimeError('ownedGUI closed while MCP active')
    time.sleep(.1)
   receipt['serverExitBeforeCleanup']=server.poll()
 except BaseException as error:
  receipt['failure']=str(error)
  raise
 finally:
  # Kill both owned groups promptly before waiting, preventing stdin cancellation from leaking GUI.
  for process in (server,gui):
   if process is not None and process.poll() is None:
    try:os.killpg(process.pid,signal.SIGTERM)
    except ProcessLookupError:pass
  owned_close(server);owned_close(gui)
  snapshot=listeners();(run/'listener-closed.log').write_text(snapshot)
  receipt.update(serverExit=None if server is None else server.returncode,GUIexit=None if gui is None else gui.returncode,closed=(server is None or server.poll() is not None) and (gui is None or gui.poll() is not None) and f'127.0.0.1:{PORT}' not in snapshot)
  (run/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');os.chmod(run/'receipt.json',0o600)

if __name__=='__main__':main()
