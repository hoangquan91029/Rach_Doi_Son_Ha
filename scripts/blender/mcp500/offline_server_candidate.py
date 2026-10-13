#!/usr/bin/env python3
"""Reviewed candidate only; root must authorize dependency install and execution."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import socket
import sys
import types

REPO = Path(__file__).resolve().parents[3]
AUDIT = REPO/'docs/audits/blender-runtime-500/mcp'
PINNED = AUDIT/'upstream'

def verified_sources():
    manifest = json.loads((AUDIT/'upstream-pins.json').read_text())
    for pin in manifest['files']:
        raw = (PINNED/pin['path']).read_bytes()
        if hashlib.sha256(raw).hexdigest() != pin['sha256']:
            raise ValueError('reviewed source drift: '+pin['path'])

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--port',type=int,required=True)
    args=parser.parse_args()
    if not 1024 <= args.port <= 65535:raise ValueError('port out of bounds')
    verified_sources()
    os.environ.update({'BLENDER_MCP_DISABLE_TELEMETRY':'1','DISABLE_TELEMETRY':'1','MCP_DISABLE_TELEMETRY':'1','BLENDER_MCP_SAFE_MODE':'1','BLENDER_MCP_CONTEXT_LOG':'0','BLENDERMCP_NO_UPDATE_CHECK':'1','BLENDER_HOST':'127.0.0.1','BLENDER_PORT':str(args.port)})
    # Only the chosen loopback Blender endpoint can be contacted from this process.
    os.environ['XDG_DATA_HOME']=str(AUDIT/'isolated-runtime-data')
    os.environ['XDG_CONFIG_HOME']=str(AUDIT/'isolated-runtime-config')
    original_connect=socket.socket.connect
    def restricted_connect(self,address):
        if address != ('127.0.0.1',args.port):raise PermissionError('offline candidate denies outbound network')
        return original_connect(self,address)
    socket.socket.connect=restricted_connect
    sys.path.insert(0,str(PINNED/'src'))
    # Upstream Git omits config.py; this explicitly local derivative supplies no keys/URLs.
    config=types.ModuleType('blender_mcp.config')
    config.telemetry_config=types.SimpleNamespace(enabled=False,max_prompt_length=0,timeout=1,supabase_url='',supabase_anon_key='',supabase_bucket='')
    sys.modules['blender_mcp.config']=config
    from blender_mcp import consent_prompt
    async def no_consent_prompt(ctx):return ''
    consent_prompt.maybe_prompt_for_consent=no_consent_prompt
    from blender_mcp import server
    # CLI arguments are explicit and local; unknown ambient flags never inherited.
    sys.argv=['mcp-for-blender','--host','127.0.0.1','--port',str(args.port)]
    server.main()

if __name__=='__main__':main()
