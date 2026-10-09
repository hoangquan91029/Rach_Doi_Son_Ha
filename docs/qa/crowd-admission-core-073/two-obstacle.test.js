import test from 'node:test';
import assert from 'node:assert/strict';
import {createMatch,step,command,view,hashState,CROWD_RADII} from './sim-draft.js';
import {UNITS,TICK_RATE} from '../../../shared/data.js';
const advance=(s,n)=>{for(let i=0;i<n;i++)step(s);};
function arena(){const s=createMatch({seed:47}),sample=s.entities.find(e=>e.type==='infantry');s.entities=[];s.map.tiles.fill('plain');s.map.resources=[];s.aiPlayer=null;return {s,sample};}
function unit(s,sample,x,y,owner=0){const e=structuredClone(sample);Object.assign(e,{id:s.nextId++,owner,x,y,order:{type:'hold'},path:[],pendingAttack:undefined});s.entities.push(e);return e;}
const distance=(a,b)=>Math.hypot(a.x-b.x,a.y-b.y);
test('two-obstacle detour preserves anchors, clearance, speed and deterministic state with views',()=>{const run=()=>{const {s,sample}=arena(),a=unit(s,sample,10.5,10.5),b=unit(s,sample,12.5,10.5),c=unit(s,sample,13.5,11);command(s,0,{type:'move',ids:[a.id],x:16.2,y:10.8});return {s,a,b,c};},x=run(),y=run();for(let i=0;i<160;i++){const old={x:x.a.x,y:x.a.y};step(x.s);step(y.s);view(y.s,0);view(y.s,1);assert.equal(hashState(x.s),hashState(y.s));assert.ok(distance(x.a,old)<=UNITS.infantry.speed/TICK_RATE+1e-8);for(const b of [x.b,x.c])assert.ok(distance(x.a,b)>=2*CROWD_RADII.land-1e-8);}assert.deepEqual([x.b.x,x.b.y,x.c.x,x.c.y],[12.5,10.5,13.5,11]);assert.ok(x.a.x>15,'must pass both obstacles');});
