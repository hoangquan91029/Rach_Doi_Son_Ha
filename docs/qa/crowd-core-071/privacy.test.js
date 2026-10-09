import test from 'node:test';
import assert from 'node:assert/strict';
import {createMatch,step,command,view,hashState,CROWD_RADII} from './sim-draft.js';
import {UNITS,TICK_RATE} from '../../../shared/data.js';
const advance=(s,n)=>{for(let i=0;i<n;i++)step(s);};
function arena(){const s=createMatch({seed:47}),sample=s.entities.find(e=>e.type==='infantry');s.entities=[];s.map.tiles.fill('plain');s.map.resources=[];s.aiPlayer=null;return {s,sample};}
function unit(s,sample,x,y,owner=0){const e=structuredClone(sample);Object.assign(e,{id:s.nextId++,owner,x,y,order:{type:'hold'},path:[],pendingAttack:undefined});s.entities.push(e);return e;}
const distance=(a,b)=>Math.hypot(a.x-b.x,a.y-b.y);
test('visible enemy internal detour route does not leak through filtered view',()=>{const s=createMatch(),enemy=s.entities.find(e=>e.owner===1&&e.type==='infantry'),friend=s.entities.find(e=>e.owner===0&&e.type==='infantry');enemy.x=friend.x+1;enemy.y=friend.y;Object.assign(enemy,{crowdRoute:[{x:44,y:44}],crowdGoal:{x:44,y:44},crowdRetry:99});const v=view(s,0),e=v.entities.find(e=>e.id===enemy.id);assert.ok(e);for(const key of ['crowdRoute','crowdGoal','crowdRetry'])assert.ok(!Object.hasOwn(e,key));assert.ok(!Object.hasOwn(v,'crowdIndex'));assert.ok(!Object.hasOwn(v,'crowdStats'));});
