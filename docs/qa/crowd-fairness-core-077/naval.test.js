import test from 'node:test';
import assert from 'node:assert/strict';
import {createMatch,step,command,view,hashState,CROWD_RADII} from './sim-draft.js';
import {UNITS,TICK_RATE} from '../../../shared/data.js';
const advance=(s,n)=>{for(let i=0;i<n;i++)step(s);};
function arena(){const s=createMatch({seed:47}),sample=s.entities.find(e=>e.type==='infantry');s.entities=[];s.map.tiles.fill('plain');s.map.resources=[];s.aiPlayer=null;return {s,sample};}
function unit(s,sample,x,y,owner=0){const e=structuredClone(sample);Object.assign(e,{id:s.nextId++,owner,x,y,order:{type:'hold'},path:[],pendingAttack:undefined});s.entities.push(e);return e;}
const distance=(a,b)=>Math.hypot(a.x-b.x,a.y-b.y);
test('naval units use their own physical radius and retain water-only navigation',()=>{const {s,sample}=arena();s.map.tiles.fill('sea');const a=unit(s,sample,10.5,10.5),anchor=unit(s,sample,12.5,10.5);for(const e of [a,anchor])Object.assign(e,{type:'transport',food:65,foodMax:65});command(s,0,{type:'move',ids:[a.id],x:14.2,y:10.8});for(let i=0;i<140;i++){step(s);assert.ok(distance(a,anchor)>=2*CROWD_RADII.naval-1e-8);assert.equal(s.map.tiles[Math.floor(a.y)*64+Math.floor(a.x)],'sea');}assert.ok(a.x>13);});
