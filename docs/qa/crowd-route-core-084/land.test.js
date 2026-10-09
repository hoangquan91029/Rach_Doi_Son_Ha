import test from 'node:test';
import assert from 'node:assert/strict';
import {createMatch,step,command,view,hashState,CROWD_RADII} from './sim-draft.js';
import {UNITS,TICK_RATE} from '../../../shared/data.js';
const advance=(s,n)=>{for(let i=0;i<n;i++)step(s);};
function arena(){const s=createMatch({seed:47}),sample=s.entities.find(e=>e.type==='infantry');s.entities=[];s.map.tiles.fill('plain');s.map.resources=[];s.aiPlayer=null;return {s,sample};}
function unit(s,sample,x,y,owner=0){const e=structuredClone(sample);Object.assign(e,{id:s.nextId++,owner,x,y,order:{type:'hold'},path:[],pendingAttack:undefined});s.entities.push(e);return e;}
const distance=(a,b)=>Math.hypot(a.x-b.x,a.y-b.y);
test('crowd movement preserves held and reserved attackers, clearance and fixed tick speed',()=>{const {s,sample}=arena(),a=unit(s,sample,10.5,10.5),anchor=unit(s,sample,12.5,10.5),enemy=unit(s,sample,13.5,10.5,1);command(s,0,{type:'attack',ids:[anchor.id],target:enemy.id});step(s);const impact=anchor.attackImpactTick,old={x:anchor.x,y:anchor.y},hp=enemy.hp;command(s,0,{type:'move',ids:[a.id],x:14.2,y:10.8});for(let i=0;i<120;i++){const before={x:a.x,y:a.y};step(s);assert.ok(distance(before,a)<=UNITS.infantry.speed/TICK_RATE+1e-8);assert.ok(distance(a,anchor)>=2*CROWD_RADII.land-1e-8);assert.deepEqual({x:anchor.x,y:anchor.y},old);}assert.ok(enemy.hp<hp,'reserved impact still happens');assert.ok(impact>0);assert.ok(a.x>13,'local steering progresses around anchor');});
