import test from 'node:test';
import assert from 'node:assert/strict';
import {createMatch,step,command,view,hashState,CROWD_RADII} from './sim-draft.js';
import {UNITS,TICK_RATE} from '../../../shared/data.js';
const advance=(s,n)=>{for(let i=0;i<n;i++)step(s);};
function arena(){const s=createMatch({seed:47}),sample=s.entities.find(e=>e.type==='infantry');s.entities=[];s.map.tiles.fill('plain');s.map.resources=[];s.aiPlayer=null;return {s,sample};}
function unit(s,sample,x,y,owner=0){const e=structuredClone(sample);Object.assign(e,{id:s.nextId++,owner,x,y,order:{type:'hold'},path:[],pendingAttack:undefined});s.entities.push(e);return e;}
const distance=(a,b)=>Math.hypot(a.x-b.x,a.y-b.y);
test('actual worker outside gather radius despite qualifying start tile reaches food contact',()=>{const s=createMatch({mapId:'coast',seed:81}),w=s.entities.find(e=>e.owner===1&&e.type==='villager'),food=s.map.resources.find(e=>e.id===7);s.aiPlayer=null;s.entities=s.entities.filter(e=>e===w);w.x=53.866097;w.y=19.983426;w.cargo={food:0,wood:0,iron:0,units:[]};assert.ok(Math.hypot(w.x-food.x,w.y-food.y)>1.1);assert.ok(Math.hypot(Math.floor(w.x)+.5-food.x,Math.floor(w.y)+.5-food.y)<=1.1);assert.ok(command(s,1,{type:'gather',ids:[w.id],target:food.id}).ok);const amount=food.amount;for(let i=0;i<80;i++)step(s);assert.ok(w.cargo.food>0&&food.amount<amount);assert.ok(Math.hypot(w.x-food.x,w.y-food.y)<=1.1);});
