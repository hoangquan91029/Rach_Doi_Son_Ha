import test from 'node:test';
import assert from 'node:assert/strict';
import {createMatch,step,command,view,hashState,CROWD_RADII} from './sim-draft.js';
import {UNITS,TICK_RATE} from '../../../shared/data.js';
const advance=(s,n)=>{for(let i=0;i<n;i++)step(s);};
function arena(){const s=createMatch({seed:47}),sample=s.entities.find(e=>e.type==='infantry');s.entities=[];s.map.tiles.fill('plain');s.map.resources=[];s.aiPlayer=null;return {s,sample};}
function unit(s,sample,x,y,owner=0){const e=structuredClone(sample);Object.assign(e,{id:s.nextId++,owner,x,y,order:{type:'hold'},path:[],pendingAttack:undefined});s.entities.push(e);return e;}
const distance=(a,b)=>Math.hypot(a.x-b.x,a.y-b.y);
test('detour near building corner cannot cross footprint or impassable diagonal sides',()=>{const {s,sample}=arena(),a=unit(s,sample,10.5,10.5),anchor=unit(s,sample,12.5,10.5);s.entities.push({id:s.nextId++,owner:0,type:'wall',kind:'building',x:12.5,y:11.5,hp:400,maxHp:400,queue:[],cargo:{food:0}});s.map.tiles[9*64+12]='mountain';command(s,0,{type:'move',ids:[a.id],x:15.2,y:10.8});for(let i=0;i<180;i++){const old={x:a.x,y:a.y};step(s);assert.ok(distance(a,old)<=UNITS.infantry.speed/TICK_RATE+1e-8);assert.ok(distance(a,anchor)>=2*CROWD_RADII.land-1e-8);assert.notEqual(s.map.tiles[Math.floor(a.y)*64+Math.floor(a.x)],'mountain');assert.ok(!(Math.abs(a.x-12.5)<.6&&Math.abs(a.y-11.5)<.6),'cannot enter wall');}assert.ok(a.x>14,'must route around corner obstruction');});
