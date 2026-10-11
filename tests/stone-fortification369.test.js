import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {artRoute} from '../client/art-routes.js';
import {createRasterSlice} from '../client/raster-slice.js';
import {buildFortificationTopology} from '../client/fortification-topology.js';
const manifest=JSON.parse(readFileSync(new URL('../public/assets/art-v1/stone-361-manifest.json',import.meta.url)));
test('explicit stone route retains stone walls without world art; explicit unknown remains disabled',()=>{
 assert.equal(artRoute('?art=stone').name,'stone');assert.equal(artRoute('?art=stone').enabled,true);assert.equal(artRoute('?art=stone').world,false);
 assert.equal(artRoute('?art=unknown').enabled,false);
});
test('real raster route draws all three stone shapes on explicit stone route, rather than loading unused PNGs',async()=>{
 const prior=globalThis.location;globalThis.location={search:'?art=stone'};
 try{
  const r=createRasterSlice();r.pipeline.preload=async()=>{};Object.defineProperty(r.pipeline,'manifest',{value:manifest});
  r.pipeline.get=id=>{const a=manifest.assets.find(a=>a.id===id);return {image:{width:128,height:128},asset:a,contactShadow:a.contactShadow,render:a.render,pivot:{x:a.pivot.x/1254*128,y:a.pivot.y/1254*128},sw:128,sh:128,sx:0,sy:0};};
  await r.preload();const entities=[[1,8.5,30.5],[2,9.5,30.5],[3,8.5,31.5]].map(([id,x,y])=>({id,x,y,type:'wall',kind:'building',owner:0,hp:400,state:'idle'})),topology=buildFortificationTopology(entities),draws=[];
  for(const e of entities){const sample=r.sampleEntity(e,{tick:100,fortificationTopology:topology});assert.equal(sample.raster.asset.material,'stone');assert.equal(sample.raster.asset.fortification.mask,topology.get(e.id).mask);assert.equal(r.drawEntity({drawImage:(...a)=>draws.push(a)},e,{tick:100,fortificationTopology:topology,project:()=>({x:100,y:100})}),true);}
  assert.equal(draws.length,3);assert.equal(r.status.entityDraws,3);
  for(const patch of [{hp:0,state:'death'},{hitUntil:101},{state:'attack'}])assert.equal(r.sampleEntity({...entities[0],...patch},{tick:100,fortificationTopology:topology}),false);
  for(const flag of [{underConstruction:true},{construction:{remaining:1}}]){const e={...entities[0],...flag,hitUntil:101};const sample=r.sampleEntity(e,{tick:100,fortificationTopology:topology});assert.equal(sample.visualState,'construction');assert.equal(sample.raster.asset.id,'stone-wall-construction-373');assert.equal(sample.sample.frame,0);assert.equal(r.drawEntity({drawImage:(...a)=>draws.push(a)},e,{tick:100,fortificationTopology:topology,project:()=>({x:100,y:100})}),true);}
  assert.equal(draws.length,5);globalThis.location={search:'?art=unknown'};assert.equal(r.sampleEntity(entities[0],{tick:100,fortificationTopology:topology}),false);
 }finally{globalThis.location=prior;}
});
