import test from 'node:test';import assert from 'node:assert/strict';import {mkdtempSync,cpSync,writeFileSync,readFileSync,rmSync} from 'node:fs';import os from 'node:os';import path from 'node:path';import {pathToFileURL} from 'node:url';import {createHash} from 'node:crypto';
import * as candidate from '/tmp/rds-egress455-stage/shared/sim.js';
const fixture=new URL('./reference-fixed/shared/',import.meta.url),temp=mkdtempSync(path.join(os.tmpdir(),'navigation-cache177-'));
assert.equal(createHash('sha256').update(readFileSync(new URL('sim.js',fixture))).digest('hex'),'caf654f1c472023346d79194d3b07c1e62cb389c373345124233944419cdf420');cpSync(fixture,path.join(temp,'shared'),{recursive:true});writeFileSync(path.join(temp,'package.json'),'{"type":"module"}');const baseline=await import(pathToFileURL(path.join(temp,'shared/sim.js')));test.after(()=>rmSync(temp,{recursive:true,force:true}));
const equal=(a,b)=>assert.equal(candidate.hashState(a),baseline.hashState(b),'complete authoritative state/path differs');
const pair=(setup,options={})=>[candidate,baseline].map(api=>{const s=api.createMatch(options);setup?.(s);return {api,s};});
const entity=(s,type,owner=0)=>s.entities.find(e=>e.owner===owner&&e.type===type&&e.hp>0);
const advance=(runs,ticks)=>{for(let i=0;i<ticks;i++){for(const {api,s} of runs)api.step(s);equal(runs[0].s,runs[1].s);}};
const move=(runs,type,x,y)=>{const replies=runs.map(({api,s})=>api.command(s,0,{type:'move',ids:[entity(s,type).id],x,y}));assert.deepEqual(replies[0],replies[1]);assert.equal(replies[0].ok,true,replies[0].error);};
function arena(s){s.map.tiles.fill('plain');s.map.resources=[];s.entities=s.entities.filter(e=>e.kind==='unit'&&e.type==='villager');const u=entity(s,'villager');u.x=10.5;u.y=10.5;s.navVersion++;}
for(const mapId of ['delta','coast'])test(`${mapId}: cell-query memo preserves diagonal, fractional and unreachable complete paths`,()=>{
 for(const target of [{x:18.5,y:18.5},{x:12.03,y:12.02},{x:12,y:12}]){const runs=pair(s=>{arena(s);s.map.tiles[10*s.map.width+11]='mountain';s.map.tiles[11*s.map.width+10]='sea';if(target.x===12)s.map.tiles[12*s.map.width+12]='mountain';},{mapId});move(runs,'villager',target.x,target.y);advance(runs,100);}
});
test('per-query owner-gate and building predicates retain exact routes without cross-query staleness',()=>{
 for(const owner of [0,1]){const runs=pair(s=>{arena(s);s.entities.push({id:s.nextId++,owner,type:'gate',kind:'building',x:12.5,y:10.5,hp:500,maxHp:500,queue:[],cargo:{food:0},cooldown:0});s.navVersion++;});move(runs,'villager',18.5,10.5);advance(runs,30);
  for(const {s} of runs){s.map.tiles[11*s.map.width+13]='mountain';s.navVersion++;entity(s,'villager').path=[];}move(runs,'villager',14.03,12.02);advance(runs,80);
 }
});
for(const mapId of ['delta','coast'])test(`${mapId}: legally trained naval unit keeps water/land and final fractional constraints`,()=>{
 const runs=pair(s=>{const yard=entity(s,'barracks');yard.type='shipyard';yard.x=10.5;yard.y=38.5;s.navVersion++;},{mapId});for(const {api,s} of runs)assert.equal(api.command(s,0,{type:'train',building:entity(s,'shipyard').id,unit:'transport'}).ok,true);advance(runs,400);assert.ok(entity(runs[0].s,'transport'));
 move(runs,'transport',15.05,42.03);advance(runs,100);move(runs,'transport',15.03,25.02);advance(runs,100);
});
test('legal same-tick build and authoritative combat death invalidate next-query behavior identically',()=>{
 const runs=pair(s=>{s.map.tiles.fill('plain');const u=entity(s,'villager'),builder=s.entities.filter(e=>e.owner===0&&e.type==='villager')[1],enemy=entity(s,'infantry',1);u.x=10.5;u.y=10.5;builder.x=10.5;builder.y=12.5;enemy.x=14.5;enemy.y=10.5;s.navVersion++;});move(runs,'villager',20.5,10.5);advance(runs,1);
 const replies=runs.map(({api,s})=>{const builder=s.entities.filter(e=>e.owner===0&&e.type==='villager')[1];return api.command(s,0,{type:'build',ids:[builder.id],building:'wall',x:13,y:10});});assert.deepEqual(replies[0],replies[1]);assert.equal(replies[0].ok,true,replies[0].error);
 for(const {api,s} of runs){const wall=s.entities.find(e=>e.id===replies[0].entity);wall.hp=1;assert.equal(api.command(s,1,{type:'attack',ids:[entity(s,'infantry',1).id],target:wall.id}).ok,true);}advance(runs,8);assert.equal(runs[0].s.entities.find(e=>e.id===replies[0].entity).hp,0);move(runs,'villager',20.03,10.02);advance(runs,100);
});
for(const mapId of ['delta','coast'])test(`${mapId}: unchanged normal AI authoritative state, orders and paths through mature tick2000`,()=>{const runs=pair(null,{mapId,seed:171,aiPlayer:1,difficulty:'normal'});advance(runs,2000);});
