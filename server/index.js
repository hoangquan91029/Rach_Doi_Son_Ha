import http from 'node:http';
import { randomBytes } from 'node:crypto';
import { readFile, stat, realpath } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { WebSocketServer, WebSocket } from 'ws';
import { createMatch, step, command, view } from '../shared/sim.js';
import { CHARACTERS, MAPS, TICK_RATE } from '../shared/data.js';

const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const mime = { '.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.json':'application/json','.webp':'image/webp','.png':'image/png','.svg':'image/svg+xml','.ico':'image/x-icon','.woff2':'font/woff2' };
const token = () => randomBytes(32).toString('base64url');
const object = x => x && typeof x === 'object' && !Array.isArray(x);
const validId = x => typeof x === 'string' && Object.hasOwn(CHARACTERS,x);
const validMap = x => MAPS.some(m => m.id === x);
export function snapshotView(state,player) {
  const snapshot=view(state,player);
  const {id,width,height,resources}=snapshot.map;
  snapshot.map={id,width,height,resources};
  return snapshot;
}
const allowedCommands = new Set(['move','attackMove','stop','hold','attack','gather','build','train','load','unload','ability','surrender','repair','cancel']);
function validateCommand(c) {
  if (!object(c) || !allowedCommands.has(c.type)) return false;
  if (c.type === 'surrender') return Object.keys(c).length === 1;
  if (c.type === 'cancel') return Number.isSafeInteger(c.building) && c.building >= 0;
  if (['train'].includes(c.type)) return Number.isSafeInteger(c.building) && typeof c.unit === 'string';
  if (!Array.isArray(c.ids) || !c.ids.length || c.ids.length > 200 || c.ids.some(n=>!Number.isSafeInteger(n)||n<0) || new Set(c.ids).size !== c.ids.length) return false;
  if (['move','attackMove','build'].includes(c.type) && (![c.x,c.y].every(n=>Number.isFinite(n)&&Math.abs(n)<10000))) return false;
  if (['attack','gather','load','unload','repair'].includes(c.type) && !Number.isSafeInteger(c.target)) return false;
  return c.type !== 'build' || typeof c.building === 'string';
}

// Resolves after listen. port=0 allocates a test port; close() awaits all sockets.
export async function createGameServer({port=3000,host='127.0.0.1',distDir=path.join(root,'dist'),graceMs=60000,roomTtlMs=300000,maxRooms=8,maxConnections=64,allowedOrigins=[]}={}) {
  const rooms = new Map(); let closePromise;
  const server = http.createServer(async(req,res)=>{
    res.setHeader('X-Content-Type-Options','nosniff');
    if(req.url==='/health' && req.method==='GET') { res.setHeader('Content-Type','application/json'); res.end(JSON.stringify({ok:true,rooms:rooms.size})); return; }
    if(!['GET','HEAD'].includes(req.method)) {res.writeHead(405);res.end();return;}
    try {
      const url = new URL(req.url,'http://localhost'); const decoded=decodeURIComponent(url.pathname);
      if(decoded.includes('\0') || decoded.includes('\\') || decoded.split('/').includes('..')) throw new Error('path');
      const base=await realpath(distDir); let file=path.resolve(base,'.'+decoded);
      if(file!==base && !file.startsWith(base+path.sep)) throw new Error('path');
      try { if((await stat(file)).isDirectory()) file=path.join(file,'index.html'); } catch { if(!path.extname(decoded)) file=path.join(base,'index.html'); }
      file=await realpath(file); if(!file.startsWith(base+path.sep)) throw new Error('path');
      const content=await readFile(file);res.setHeader('Content-Type',mime[path.extname(file)]||'application/octet-stream');
      res.setHeader('Cache-Control',path.extname(file)==='.html'?'no-cache':'public, max-age=3600'); res.end(req.method==='HEAD'?undefined:content);
    } catch {res.writeHead(404);res.end('Not found');}
  });
  const wss = new WebSocketServer({noServer:true,maxPayload:16384,perMessageDeflate:{threshold:1024,serverNoContextTakeover:true,clientNoContextTakeover:true,serverMaxWindowBits:15,zlibDeflateOptions:{memLevel:7},concurrencyLimit:4}});
  server.on('upgrade',(req,socket,head)=>{
    let allowed=false;
    try { const url=new URL(req.url,'http://localhost'); const origin=req.headers.origin;
      allowed=url.pathname==='/ws' && wss.clients.size<maxConnections && (!origin || allowedOrigins.includes(origin) || new URL(origin).host===req.headers.host);
    } catch {}
    if(!allowed) {socket.end('HTTP/1.1 403 Forbidden\r\nConnection: close\r\n\r\n');return;}
    wss.handleUpgrade(req,socket,head,ws=>wss.emit('connection',ws,req));
  });
  const send=(ws,data)=>{if(ws?.readyState===WebSocket.OPEN) {if(ws.bufferedAmount>1024*1024) {ws.terminate();return;} ws.send(JSON.stringify(data));}};
  const lobby=r=>({code:r.code,players:r.seats.map(s=>s?{name:s.name,king:s.king,general:s.general,ready:s.ready,connected:!!s.ws,rematch:!!s.rematch}:null),mapId:r.mapId,status:r.status});
  const broadcastLobby=r=>r.seats.forEach(s=>send(s?.ws,{type:'lobby',...lobby(r)}));
  const snapshots=r=>r.seats.forEach((s,i)=>{if(s) send(s.ws,{type:'state',state:snapshotView(r.state,i),paused:r.status==='playing'&&r.seats.some(x=>!x?.ws),...(r.seats.some(x=>x?.lostAt)?{reconnectRemaining:Math.max(0,Math.ceil((graceMs-(Date.now()-Math.min(...r.seats.filter(x=>x?.lostAt).map(x=>x.lostAt))))/1000))}:{})});});
  const finish=(r,winner,reason)=>{r.state.winner=winner;r.state.reason=reason;r.status='finished';r.updated=Date.now();r.seats.forEach(s=>{if(s){s.ready=false;s.rematch=false;}});snapshots(r);broadcastLobby(r);};
  const detach=(ws,leave=false)=>{const r=ws.room,s=r?.seats[ws.player];if(!s||s.ws!==ws)return;ws.room=null;s.ws=null;s.ready=false;s.lostAt=Date.now();r.updated=Date.now();
    if(leave){s.token=null;if(r.status==='playing')finish(r,1-ws.player,'Opponent left');else r.seats[ws.player]=null;}
    if(leave && r.seats.every(x=>!x?.ws)) rooms.delete(r.code); else broadcastLobby(r);
  };
  const attach=(ws,r,i,s)=>{ws.room=r;ws.player=i;s.ws=ws;s.lostAt=null;s.token=token();r.updated=Date.now();send(ws,{type:'joined',code:r.code,player:i,token:s.token,lobby:lobby(r)});broadcastLobby(r);if(r.state)send(ws,{type:'start',player:i,state:view(r.state,i)});};
  const selection=m=>validId(m.king)&&validId(m.general)&&typeof m.name==='string'&&m.name.trim().length>0&&m.name.trim().length<=32&&!/[\x00-\x1f\x7f]/.test(m.name);
  wss.on('connection',ws=>{
    ws.alive=true; ws.on('pong',()=>{ws.alive=true;});let count=0,window=Date.now();
    ws.on('message',(raw,isBinary)=>{
      const error=message=>send(ws,{type:'error',message});
      if(Date.now()-window>1000){window=Date.now();count=0;} if(++count>40){ws.close(1008,'Rate limit');return;}
      let m;try{if(isBinary)throw Error();m=JSON.parse(raw.toString());if(!object(m)||typeof m.type!=='string')throw Error();}catch{error('Malformed message');return;}
      try {
        if(m.type==='ping'){send(ws,{type:'pong'});return;}
        if(['create','join','resume'].includes(m.type)) {
          if(ws.room){error('Already in a room');return;}
          if(m.type==='create') {
            if(!selection(m)||!validMap(m.mapId)){error('Invalid room configuration');return;}if(rooms.size>=maxRooms){error('Room capacity reached');return;}
            let code;do{code=randomBytes(4).toString('hex').slice(0,6).toUpperCase();}while(rooms.has(code));
            const r={code,mapId:m.mapId,status:'lobby',seats:[null,null],state:null,updated:Date.now()};rooms.set(code,r);r.seats[0]={name:m.name.trim(),king:m.king,general:m.general,ready:false};attach(ws,r,0,r.seats[0]);return;
          }
          if(typeof m.code!=='string'||!/^[A-Z0-9]{6}$/i.test(m.code)){error('Invalid room code');return;}const r=rooms.get(m.code.toUpperCase());if(!r){error('Room not found');return;}
          if(m.type==='resume') {const i=r.seats.findIndex(s=>s&&typeof m.token==='string'&&s.token===m.token);if(i<0||r.seats[i].ws||Date.now()-r.seats[i].lostAt>graceMs){error('Reconnect token invalid or expired');return;}attach(ws,r,i,r.seats[i]);return;}
          if(r.status!=='lobby'||!selection(m)){error('Room unavailable or invalid selection');return;}const i=r.seats.findIndex(s=>!s);if(i<0){error('Room full');return;}
          r.seats[i]={name:m.name.trim(),king:m.king,general:m.general,ready:false};r.seats.forEach(s=>{if(s)s.ready=false;});attach(ws,r,i,r.seats[i]);return;
        }
        const r=ws.room,s=r?.seats[ws.player];if(!r||s?.ws!==ws){error('Join a room first');return;}r.updated=Date.now();
        if(m.type==='leave'){detach(ws,true);return;}
        if(m.type==='configure') {if(r.status!=='lobby'||!validId(m.king)||!validId(m.general)||(m.mapId!==undefined&&(ws.player!==0||!validMap(m.mapId)))){error('Invalid configuration');return;}s.king=m.king;s.general=m.general;if(m.mapId)r.mapId=m.mapId;r.seats.forEach(x=>{if(x)x.ready=false;});broadcastLobby(r);return;}
        if(m.type==='ready') {if(r.status!=='lobby'||typeof m.ready!=='boolean'){error('Cannot ready now');return;}s.ready=m.ready;
          if(r.seats.every(x=>x?.ws&&x.ready)){r.state=createMatch({mapId:r.mapId,seed:randomBytes(4).readUInt32LE(),players:r.seats.map(x=>({name:x.name,king:x.king,general:x.general}))});r.status='playing';r.seats.forEach((x,i)=>send(x.ws,{type:'start',player:i,state:view(r.state,i)}));}broadcastLobby(r);return;}
        if(m.type==='command') {if(r.status!=='playing'||r.seats.some(x=>!x?.ws)){error('Match is not active');return;}if(!validateCommand(m.command)){error('Invalid command');return;}const result=command(r.state,ws.player,m.command);if(!result.ok)error(result.error||'Command rejected');if(r.state.winner!==null)finish(r,r.state.winner,r.state.reason);return;}
        if(m.type==='rematch'){if(r.status!=='finished'){error('Match has not ended');return;}s.rematch=true;if(r.seats.every(x=>x?.ws&&x.rematch)){r.status='lobby';r.state=null;r.seats.forEach(x=>{x.ready=false;x.rematch=false;});}broadcastLobby(r);return;}
        error('Unknown message type');
      } catch(e) {console.error('Room operation failed',e);error('Operation failed');}
    });
    ws.on('close',()=>detach(ws));ws.on('error',()=>{});
  });
  let snapshotCounter=0;
  const timer=setInterval(()=>{const now=Date.now();for(const r of rooms.values()){
    if(r.seats.every(s=>!s?.ws) && r.seats.every(s=>!s || now-s.lostAt>=graceMs)){rooms.delete(r.code);continue;}
    if(r.status==='playing') {const lost=r.seats.findIndex(s=>!s?.ws);if(lost>=0){if(r.seats[1-lost]?.ws && now-r.seats[lost].lostAt>=graceMs)finish(r,1-lost,'Opponent disconnected');}else {step(r.state);if(r.state.winner!==null)finish(r,r.state.winner,r.state.reason);}}
    else if(r.status==='lobby'){let removed=false;for(let i=0;i<2;i++)if(r.seats[i]&&!r.seats[i].ws&&now-r.seats[i].lostAt>=graceMs){r.seats[i]=null;removed=true;}if(removed)broadcastLobby(r);}
    if(now-r.updated>=roomTtlMs&&r.status!=='playing'){r.seats.forEach(s=>{if(s?.ws){s.ws.room=null;send(s.ws,{type:'error',message:'Room expired'});}});rooms.delete(r.code);}
    if(snapshotCounter%4===0&&r.state)snapshots(r);
  }snapshotCounter++;},1000/TICK_RATE);
  const heartbeat=setInterval(()=>{for(const ws of wss.clients){if(!ws.alive){ws.terminate();continue;}ws.alive=false;ws.ping();}},15000);
  try {await new Promise((resolve,reject)=>{server.once('error',reject);server.listen(port,host,resolve);});}
  catch(error){clearInterval(timer);clearInterval(heartbeat);wss.close();throw error;}
  return {server,wss,rooms,close:()=>{if(closePromise)return closePromise;closePromise=(async()=>{clearInterval(timer);clearInterval(heartbeat);for(const ws of wss.clients)ws.terminate();await new Promise(resolve=>wss.close(resolve));await new Promise(resolve=>server.close(resolve));rooms.clear();})();return closePromise;}};
}
export function serverOptionsFromEnv(env=process.env) {
  const bounded=(value,fallback,min,max)=>{const n=Number(value);return value!==undefined&&value!==''&&Number.isSafeInteger(n)&&n>=min&&n<=max?n:fallback;};
  return {maxRooms:bounded(env.MAX_ROOMS,8,1,64),maxConnections:bounded(env.MAX_CONNECTIONS,64,2,256),graceMs:bounded(env.RECONNECT_SECONDS,60,5,120)*1000};
}
if(process.argv[1] && path.resolve(process.argv[1])===fileURLToPath(import.meta.url)) {
  const game=await createGameServer({port:Number(process.env.PORT)||3000,host:process.env.HOST||'0.0.0.0',...serverOptionsFromEnv()});
  console.log(`Rạch Đôi Sơn Hà: http://localhost:${game.server.address().port}`);
  for(const signal of ['SIGINT','SIGTERM'])process.on(signal,async()=>{await game.close();process.exit(0);});
}
