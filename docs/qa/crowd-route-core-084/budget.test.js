import test from 'node:test';
import assert from 'node:assert/strict';
import {createMatch,step,command,view,hashState,CROWD_RADII} from './sim-draft.js';
import {UNITS,TICK_RATE} from '../../../shared/data.js';
const advance=(s,n)=>{for(let i=0;i<n;i++)step(s);};
function arena(){const s=createMatch({seed:47}),sample=s.entities.find(e=>e.type==='infantry');s.entities=[];s.map.tiles.fill('plain');s.map.resources=[];s.aiPlayer=null;return {s,sample};}
function unit(s,sample,x,y,owner=0){const e=structuredClone(sample);Object.assign(e,{id:s.nextId++,owner,x,y,order:{type:'hold'},path:[],pendingAttack:undefined});s.entities.push(e);return e;}
const distance=(a,b)=>Math.hypot(a.x-b.x,a.y-b.y);
test('planner budget exhaustion cannot prevent independent unobstructed movement',()=>{const {s,sample}=arena(),a=unit(s,sample,10.5,10.5);command(s,0,{type:'move',ids:[a.id],x:18,y:10});step(s);s.crowdStats.plannerEdges=4097;s.crowdStats.edges=4097;s.crowdIndex.tick=s.tick+1;const before={x:a.x,y:a.y};step(s);assert.ok(distance(before,a)>0,'unobstructed mover retains normal physical step');assert.ok(distance(before,a)<=UNITS.infantry.speed/TICK_RATE+1e-8);});
