"""Actual MCP SDK STDIO client; read-only one finite private handshake."""
import asyncio
import json
from pathlib import Path
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
repo=Path(__file__).resolve().parents[3]
out=repo/'docs/audits/blender-runtime-501/handshake/sdk-response.json'
async def handshake():
 params=StdioServerParameters(command=sys.executable,args=[str(repo/'scripts/blender/mcp500/offline_server_candidate.py'),'--port','19876'])
 async with stdio_client(params) as (read,write):
  async with ClientSession(read,write) as session:
   init=await session.initialize()
   tools=await session.list_tools()
   names=[t.name for t in tools.tools]
   if 'get_scene_info' not in names or 'get_addon_status' not in names:raise ValueError('expected actual read-only tools missing')
   status=await session.call_tool('get_addon_status',{})
   scene=await session.call_tool('get_scene_info',{})
   if status.isError or scene.isError:raise ValueError('actual read-only tool returned isError')
   out.write_text(json.dumps({'initialize':init.model_dump(mode='json'),'toolNames':names,'status':status.model_dump(mode='json'),'scene':scene.model_dump(mode='json'),'calls':['initialize','tools/list','get_addon_status','get_scene_info'],'limitation':'Only private SDK STDIO handshake; no Codexconfiguration/tool exposure, no authoring/artapproval'},indent=2)+'\n')
asyncio.run(asyncio.wait_for(handshake(),timeout=25))
