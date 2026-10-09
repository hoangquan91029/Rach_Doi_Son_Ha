import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createMatch,command,view,step} from '../shared/sim.js';
import {createRasterSlice} from '../client/raster-slice.js';
function site(){
 const s=createMatch(),observer=s.entities.find(e=>e.owner===0&&e.type==='villager'),builder=s.entities.find(e=>e.owner===1&&e.type==='villager');
 s.entities=[observer,builder];s.aiPlayer=null;s.map.tiles.fill('plain');s.map.resources=[];s.navVersion++;s.crowdIndex=null;
 observer.x=12.5;observer.y=10.5;builder.x=14.5;builder.y=11.5;
 view(s,1);const result=command(s,1,{type:'build',ids:[builder.id],building:'wall',x:14,y:13});assert.equal(result.ok,true,result.error);
 const building=s.entities.find(e=>e.id===result.entity);return {s,observer,builder,building};
}
test('visible enemy construction has a visual flag without private job, queue, cargo or orders',()=>{
 const {s,building}=site();building.queue=[{unit:'infantry',remaining:7,total:10}];building.cargo.food=70;
 const seen=view(s,0).entities.find(e=>e.id===building.id);assert.ok(seen);assert.equal(seen.underConstruction,true);
 assert.equal(seen.construction,undefined);assert.equal(seen.order,undefined);assert.deepEqual(seen.queue,[]);assert.deepEqual(seen.cargo,{food:0,wood:0,iron:0,units:[]});assert.equal(building.underConstruction,undefined);
});
test('owner retains actual construction progress and builder alongside same visual flag',()=>{
 const {s,building}=site(),own=view(s,1).entities.find(e=>e.id===building.id);assert.equal(own.underConstruction,true);assert.deepEqual(own.construction,building.construction);
 own.construction.remaining=0;assert.ok(building.construction.remaining>0,'snapshot cannot mutate authoritative job');
});
test('hidden enemy site is omitted entirely, even when previously seen',()=>{
 const {s,observer,building}=site();assert.ok(view(s,0).entities.some(e=>e.id===building.id));observer.x=45.5;observer.y=30.5;
 assert.equal(view(s,0).entities.some(e=>e.id===building.id),false);
});
test('ordinary construction completion clears visual flag; damage never means under construction',()=>{
 const {s,building}=site();for(let i=0;i<220;i++)step(s);assert.equal(building.construction,null);
 assert.equal(view(s,0).entities.find(e=>e.id===building.id).underConstruction,false);
 building.hp=building.maxHp*.2;assert.equal(view(s,0).entities.find(e=>e.id===building.id).underConstruction,false);
});
test('visual flag adds no construction semantics to units',()=>{
 const {s,observer}=site();assert.equal(Object.hasOwn(view(s,0).entities.find(e=>e.id===observer.id),'underConstruction'),false);
});
test('authored completed building art is withheld for enemy construction flag, with idle retained after completion',async()=>{
 const previous=globalThis.location;globalThis.location={search:'?art=fort'};
 try{
  const m=JSON.parse(readFileSync(new URL('../public/assets/art-v1/fort-202-manifest.json',import.meta.url))),r=createRasterSlice({enabled:true});
  r.pipeline.preload=async()=>{};Object.defineProperty(r.pipeline,'manifest',{value:m});r.pipeline.get=id=>({image:{width:256,height:256},asset:m.assets.find(a=>a.id===id)});await r.preload();
  const e={id:99,owner:1,kind:'building',type:'fort',x:10.5,y:10.5,hp:500,maxHp:1250,state:'idle'};
  assert.equal(r.sampleEntity({...e,underConstruction:true},{tick:100}),false);
  assert.ok(r.sampleEntity({...e,underConstruction:false},{tick:100}));assert.ok(r.sampleEntity(e,{tick:100}),'legacy completed snapshots retain fallback compatibility');
 }finally{globalThis.location=previous;}
});
