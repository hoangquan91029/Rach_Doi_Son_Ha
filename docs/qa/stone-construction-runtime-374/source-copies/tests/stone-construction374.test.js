import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {buildFortificationTopology} from '../client/fortification-topology.js';
import {createRasterSlice} from '../client/raster-slice.js';
test('wholeSTONE construction373 exact raster public/private site, staticframe and state eligibility',async()=>{
 const prior=globalThis.location;
 try{for(const route of ['', '?art=fort']){
 globalThis.location={search:route};const manifest=JSON.parse(readFileSync(new URL('../public/assets/art-v1/'+(route?'fort-202-manifest.json':'stone-361-manifest.json'),import.meta.url)));
 const r=createRasterSlice();r.pipeline.preload=async()=>{};Object.defineProperty(r.pipeline,'manifest',{value:manifest});r.pipeline.get=id=>{const a=manifest.assets.find(a=>a.id===id);return {image:{width:128,height:128},asset:a,contactShadow:a.contactShadow,render:a.render,pivot:{x:a.pivot.x/1254*128,y:a.pivot.y/1254*128},sw:128,sh:128,sx:0,sy:0};};await r.preload();
 const e={id:1,x:8.5,y:30.5,type:'wall',kind:'building',owner:0,hp:400,state:'idle'},draws=[];
 for(const flag of [{underConstruction:true},{construction:{remaining:1,total:5}}]){const site={...e,...flag,hitUntil:200};const got=r.sampleEntity(site,{tick:100});assert.equal(got.visualState,'construction');assert.equal(got.raster.asset.id,'stone-wall-construction-373');assert.equal(got.sample.frame,0);assert.equal(r.drawEntity({drawImage:(...a)=>draws.push(a)},site,{tick:100,project:()=>({x:100,y:100})}),true);assert.equal(r.sampleEntity({...site,hp:0},{tick:100}),false);}
 assert.equal(draws.length,2);assert.equal(r.status.entityDraws,2);assert.equal(r.sampleEntity(e,{tick:100,fortificationTopology:buildFortificationTopology([e])}).visualState,'idle');for(const patch of [{hp:0},{hitUntil:200},{state:'attack'}])assert.equal(r.sampleEntity({...e,...patch},{tick:100}),false);globalThis.location={search:'?art=unknown'};assert.equal(r.sampleEntity({...e,underConstruction:true},{tick:100}),false);
 }}finally{globalThis.location=prior;}
});
