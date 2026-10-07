import test from 'node:test';
import http from 'node:http';
import assert from 'node:assert/strict';
import { WebSocket } from 'ws';
import { mkdtemp, writeFile, rm } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { createGameServer, snapshotView, serverOptionsFromEnv } from '../server/index.js';
import { createMatch, view, hashState } from '../shared/sim.js';
import { CHARACTERS, MAPS } from '../shared/data.js';
const wait = ms => new Promise(r=>setTimeout(r,ms));
async function client(port){const ws=new WebSocket(`ws://127.0.0.1:${port}/ws`);const messages=[];ws.on('message',x=>messages.push(JSON.parse(x)));await new Promise((r,j)=>{ws.once('open',r);ws.once('error',j);});return {ws,messages,send:m=>ws.send(JSON.stringify(m)),async take(type){for(let i=0;i<100;i++){const n=messages.findIndex(x=>x.type===type);if(n>=0)return messages.splice(n,1)[0];await wait(10);}throw Error('Timed out '+type);}};}
const keys=Object.keys(CHARACTERS);
const config={name:'Commander',king:keys[0],general:keys[1],mapId:MAPS[0].id};
test('two seats, readiness, authority, reconnect rotation and consensual rematch',async t=>{
 const game=await createGameServer({port:0,graceMs:1000});t.after(()=>game.close());const port=game.server.address().port;
 const a=await client(port),b=await client(port),c=await client(port);a.send({type:'create',...config});const joined=await a.take('joined');
 b.send({type:'join',code:joined.code,...config,name:'Other'});await b.take('joined');c.send({type:'join',code:joined.code,...config});assert.match((await c.take('error')).message,/full/);
 a.send({type:'ready',ready:true});await wait(30);b.send({type:'configure',king:keys[2],general:keys[1]});await wait(30);assert.equal(game.rooms.get(joined.code).seats[0].ready,false);
 a.send({type:'ready',ready:true});b.send({type:'ready',ready:true});await a.take('start');await b.take('start');const room=game.rooms.get(joined.code);assert.equal(room.status,'playing');
 a.send({type:'command',command:{type:'giveResources',iron:99999}});assert.match((await a.take('error')).message,/Invalid/);
 const own=room.state.entities.find(x=>x.owner===1&&x.kind==='unit');a.send({type:'command',command:{type:'move',ids:[own.id],x:2,y:2}});await a.take('error');
 a.ws.close();await wait(80);const frozen=room.state.tick;await wait(80);assert.equal(room.state.tick,frozen);
 const d=await client(port);d.send({type:'resume',code:joined.code,token:joined.token});const resumed=await d.take('joined');assert.notEqual(resumed.token,joined.token);await d.take('start');
 c.send({type:'resume',code:joined.code,token:joined.token});assert.match((await c.take('error')).message,/token/);
 d.send({type:'command',command:{type:'surrender'}});await wait(40);assert.equal(room.state.winner,1);assert.equal(room.status,'finished');d.send({type:'rematch'});await wait(30);assert.equal(room.status,'finished');b.send({type:'rematch'});await wait(30);assert.equal(room.status,'lobby');assert.equal(room.state,null);assert.ok(room.seats.every(s=>!s.ready));
});
test('disconnect timeout awards opponent and malformed packets remain harmless',async t=>{
 const game=await createGameServer({port:0,graceMs:100});t.after(()=>game.close());const port=game.server.address().port;const a=await client(port),b=await client(port);
 a.ws.send('{');assert.match((await a.take('error')).message,/Malformed/);a.send({type:'create',...config});const joined=await a.take('joined');b.send({type:'join',code:joined.code,...config});await b.take('joined');a.send({type:'ready',ready:true});b.send({type:'ready',ready:true});await a.take('start');a.ws.close();await wait(250);assert.equal(game.rooms.get(joined.code).state.winner,1);const c=await client(port);c.send({type:'resume',code:joined.code,token:joined.token});assert.match((await c.take('error')).message,/expired/);
});
test('HTTP health, static MIME and traversal protection',async t=>{
 const dist=await mkdtemp(path.join(os.tmpdir(),'rts-static-'));await writeFile(path.join(dist,'index.html'),'<h1>Game</h1>');await writeFile(path.join(dist,'game.js'),'export const game=1');t.after(()=>rm(dist,{recursive:true,force:true}));const game=await createGameServer({port:0,distDir:dist});t.after(()=>game.close());const base=`http://127.0.0.1:${game.server.address().port}`;assert.equal((await fetch(base+'/health')).status,200);assert.equal((await fetch(base+'/%2e%2e%2fpackage.json')).status,404);assert.match((await fetch(base+'/game.js')).headers.get('content-type'),/javascript/);assert.equal(await (await fetch(base+'/join/ABC123')).text(),'<h1>Game</h1>');
});
test('both connections can resume within grace; repeated ready starts only once',async t=>{
 const game=await createGameServer({port:0,graceMs:1000});t.after(()=>game.close());const port=game.server.address().port;
 const a=await client(port),b=await client(port);a.send({type:'create',...config});const aj=await a.take('joined');b.send({type:'join',code:aj.code,...config});const bj=await b.take('joined');
 a.send({type:'ready',ready:true});b.send({type:'ready',ready:true});await a.take('start');await b.take('start');a.send({type:'ready',ready:true});assert.match((await a.take('error')).message,/ready/);assert.equal(a.messages.filter(x=>x.type==='start').length,0);
 a.ws.close();b.ws.close();await wait(100);assert.ok(game.rooms.has(aj.code));const c=await client(port),d=await client(port);c.send({type:'resume',code:aj.code,token:aj.token});await c.take('joined');d.send({type:'resume',code:aj.code,token:bj.token});await d.take('joined');const room=game.rooms.get(aj.code);const tick=room.state.tick;await wait(100);assert.ok(room.state.tick>tick);
 const e=await client(port);e.send({type:'resume',code:aj.code,token:room.seats[0].token});assert.match((await e.take('error')).message,/token/);
});
test('message rate cap closes abusive client',async t=>{
 const game=await createGameServer({port:0});t.after(()=>game.close());const a=await client(game.server.address().port);const closed=new Promise(r=>a.ws.once('close',r));for(let i=0;i<45;i++)a.send({type:'ping'});await closed;assert.equal(a.ws.readyState,WebSocket.CLOSED);
});
test('authoritative combat General death completes online match',async t=>{
 const game=await createGameServer({port:0});t.after(()=>game.close());const port=game.server.address().port;const a=await client(port),b=await client(port);
 a.send({type:'create',...config});const joined=await a.take('joined');b.send({type:'join',code:joined.code,...config});await b.take('joined');a.send({type:'ready',ready:true});b.send({type:'ready',ready:true});await a.take('start');await b.take('start');
 const room=game.rooms.get(joined.code);const attacker=room.state.entities.find(e=>e.owner===0&&e.type==='general');const target=room.state.entities.find(e=>e.owner===1&&e.type==='general');
 // Controlled combat fixture only: server simulation must acquire, damage and kill via public WS command.
 target.x=attacker.x+1;target.y=attacker.y;target.hp=1;
 a.send({type:'command',command:{type:'attack',ids:[attacker.id],target:target.id}});
 for(let i=0;i<100&&room.state.winner===null;i++)await wait(20);
 assert.equal(room.state.winner,0);assert.equal(room.status,'finished');assert.ok(target.hp<=0);
 const final=await a.take('state'); // Earlier snapshots may exist; authoritative result is checked above.
 assert.ok(final.state.players.length===2);
});
test('unseen enemy target is rejected by authoritative fog and cross-origin upgrade fails',async t=>{
 const game=await createGameServer({port:0});t.after(()=>game.close());const port=game.server.address().port;const a=await client(port),b=await client(port);a.send({type:'create',...config});const joined=await a.take('joined');b.send({type:'join',code:joined.code,...config});await b.take('joined');a.send({type:'ready',ready:true});b.send({type:'ready',ready:true});const start=await a.take('start');assert.ok(start.state.map.tiles.length>0);assert.match(a.ws.extensions,/permessage-deflate/);const update=await a.take('state');assert.equal(update.state.map.tiles,undefined);assert.equal(update.state.map.name,undefined);assert.equal(update.state.map.id,start.state.map.id);await b.take('start');const room=game.rooms.get(joined.code);const enemy=room.state.entities.find(e=>e.owner===1&&e.type==='general');assert.ok(!start.state.entities.some(e=>e.id===enemy.id));const own=room.state.entities.find(e=>e.owner===0&&e.type==='general');a.send({type:'command',command:{type:'attack',ids:[own.id],target:enemy.id}});assert.match((await a.take('error')).message,/visible|fog|seen|target/i);
 const hostile=new WebSocket(`ws://127.0.0.1:${port}/ws`,{origin:'https://evil.example'});const result=await new Promise(resolve=>{hostile.on('unexpected-response',(_r,res)=>{res.resume();hostile.terminate();resolve(res.statusCode);});hostile.on('error',()=>{});});assert.equal(result,403);
});
test('oversized payload is closed and fully disconnected room expires without winner',async t=>{
 const game=await createGameServer({port:0,graceMs:80});t.after(()=>game.close());const port=game.server.address().port;const huge=await client(port);huge.ws.on('error',()=>{});const closed=new Promise(resolve=>huge.ws.once('close',resolve));huge.ws.send(' '.repeat(20000));assert.equal(await closed,1009);
 const a=await client(port),b=await client(port);a.send({type:'create',...config});const joined=await a.take('joined');b.send({type:'join',code:joined.code,...config});await b.take('joined');a.send({type:'ready',ready:true});b.send({type:'ready',ready:true});await a.take('start');await b.take('start');const room=game.rooms.get(joined.code);a.ws.close();b.ws.close();await wait(200);assert.equal(room.state.winner,null);assert.equal(game.rooms.has(joined.code),false);
});

test('compact snapshot hydration equals full view at same tick without state mutation',()=>{const state=createMatch({seed:731});for(const player of [0,1]){const full=view(state,player),before=hashState(state),compact=snapshotView(state,player);assert.equal(hashState(state),before);assert.equal(compact.tick,full.tick);assert.deepEqual({...compact,map:{...full.map,...compact.map}},full);}});
test('public repair resumes construction; only owner can cancel reservation',async t=>{
 const game=await createGameServer({port:0});t.after(()=>game.close());const port=game.server.address().port;const a=await client(port),b=await client(port);a.send({type:'create',...config});const joined=await a.take('joined');b.send({type:'join',code:joined.code,...config});await b.take('joined');a.send({type:'ready',ready:true});b.send({type:'ready',ready:true});await a.take('start');await b.take('start');const room=game.rooms.get(joined.code),builder=room.state.entities.find(e=>e.owner===0&&e.type==='villager');
 a.send({type:'command',command:{type:'build',ids:[builder.id],building:'granary',x:20,y:23}});await wait(30);const site=room.state.entities.find(e=>e.owner===0&&e.construction);assert.ok(site,'build command must reserve a real site');
 a.send({type:'command',command:{type:'stop',ids:[builder.id]}});await wait(20);a.send({type:'command',command:{type:'repair',ids:[builder.id],target:site.id}});await wait(20);assert.equal(builder.order?.target,site.id);
 b.send({type:'command',command:{type:'cancel',building:site.id}});assert.match((await b.take('error')).message,/own/);assert.ok(site.hp>0);
 a.send({type:'command',command:{type:'cancel',building:site.id}});await wait(20);assert.equal(site.hp,0);
 await Promise.all([game.close(),game.close()]);
});

test('deployment capacity environment is finite and bounded',()=>{assert.deepEqual(serverOptionsFromEnv({}),{maxRooms:8,maxConnections:64,graceMs:60000});assert.deepEqual(serverOptionsFromEnv({MAX_ROOMS:'Infinity',MAX_CONNECTIONS:'99999',RECONNECT_SECONDS:'-1'}),{maxRooms:8,maxConnections:64,graceMs:60000});assert.deepEqual(serverOptionsFromEnv({MAX_ROOMS:'16',MAX_CONNECTIONS:'32',RECONNECT_SECONDS:'90'}),{maxRooms:16,maxConnections:32,graceMs:90000});});

test('Firefox bare permessage-deflate offer upgrades successfully with bounded compression',async t=>{
 const game=await createGameServer({port:0});t.after(()=>game.close());const port=game.server.address().port;
 const response=await new Promise((resolve,reject)=>{const req=http.get({hostname:'127.0.0.1',port,path:'/ws',headers:{Upgrade:'websocket',Connection:'Upgrade',Origin:`http://127.0.0.1:${port}`,'Sec-WebSocket-Version':'13','Sec-WebSocket-Key':'BbncgNB94vGu2NnobmYvcQ==','Sec-WebSocket-Extensions':'permessage-deflate'}},res=>{res.resume();reject(Error(`Unexpected HTTP ${res.statusCode}`));});req.on('upgrade',(res,socket)=>{socket.destroy();resolve(res);});req.on('error',reject);});
 assert.equal(response.statusCode,101);const extension=response.headers['sec-websocket-extensions'];assert.match(extension,/permessage-deflate/);assert.match(extension,/server_no_context_takeover/);assert.match(extension,/client_no_context_takeover/);assert.match(extension,/server_max_window_bits=15/);assert.ok(!extension.includes('client_max_window_bits'));
});

test('compact online snapshots strip private pending attack targets for both seats',()=>{const s=createMatch({seed:140});const a=s.entities.find(e=>e.owner===0&&e.type==='infantry');a.attackStartedTick=10;a.attackImpactTick=14;a.attackCueKind='melee';a.pendingAttack={target:987654,x:a.x,y:a.y,orderType:'attack'};for(const p of [0,1]){const snap=snapshotView(s,p);assert.equal(JSON.stringify(snap).includes('pendingAttack'),false);const publicA=snap.entities.find(e=>e.id===a.id);if(publicA){assert.equal(publicA.attackStartedTick,10);assert.equal(publicA.attackImpactTick,14);assert.equal(publicA.attackCueKind,'melee');}}assert.equal(a.pendingAttack.target,987654);});
