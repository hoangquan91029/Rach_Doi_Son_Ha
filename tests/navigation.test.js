import test from 'node:test';
import assert from 'node:assert/strict';
import {createMatch,command,step,hashState} from '../shared/sim.js';
function arena(){const s=createMatch({seed:91});s.map.tiles.fill('plain');s.map.resources=[];s.entities=s.entities.filter(e=>e.kind==='unit'&&['king','villager'].includes(e.type));const u=s.entities.find(e=>e.owner===0&&e.type==='villager');u.x=10.5;u.y=10.5;u.food=u.foodMax;s.navVersion++;return {s,u};}
const move=(s,u,x,y)=>assert.equal(command(s,0,{type:'move',ids:[u.id],x,y}).ok,true);
test('open diagonal uses distance-optimal sustained D1 and repeatable authoritative states',()=>{
 const a=arena(),b=arena();for(const {s,u} of [a,b])move(s,u,18.5,18.5);
 for(let i=0;i<60;i++){step(a.s);step(b.s);assert.equal(a.u.dir,1);assert.ok(Math.abs(a.u.x-a.u.y)<1e-10);assert.equal(hashState(a.s),hashState(b.s));}
 assert.ok(a.u.x>13);assert.ok(a.u.path.every(p=>p.x===p.y));
});
test('terrain side cells prevent diagonal corner cutting even when destination is legal',()=>{
 const {s,u}=arena();s.map.tiles[10*s.map.width+11]='mountain';s.map.tiles[11*s.map.width+10]='sea';move(s,u,12.5,12.5);step(s);assert.notEqual(u.dir,1);assert.notDeepEqual(u.path[0],{x:11.5,y:11.5});assert.ok(u.x<=10.5||u.y<=10.5);
});
test('building side cells and changed dynamic blockers prevent corner cutting',()=>{
 const {s,u}=arena();move(s,u,16.5,16.5);step(s);assert.equal(u.dir,1);
 s.entities.push({id:s.nextId++,type:'wall',kind:'building',owner:1,hp:200,maxHp:200,x:11.5,y:10.5,queue:[],cargo:{food:0},cooldown:0});s.navVersion++;
 const before={x:u.x,y:u.y};step(s);assert.ok(u.x<=before.x||u.y<=before.y,'blocked diagonal cannot continue through building corner');
});
