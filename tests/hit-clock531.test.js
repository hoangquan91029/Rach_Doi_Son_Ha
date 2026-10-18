import test from 'node:test';
import assert from 'node:assert/strict';
import {createRasterSlice} from '../client/raster-slice.js';
import {createPresentationClock} from '../client/action-presentation.js';

const actor={id:12,type:'villager',kind:'unit',hp:100,state:'idle',dir:1,x:3,y:4,owner:0};
async function fixture({cold=false,missing=false}={}){
 const r=createRasterSlice({enabled:true}),calls=[];
 const asset=(id,state,durations)=>({id,kind:'unit',family:'unit.villager',state,direction:1,frames:durations.map(durationMs=>({durationMs})),contactShadow:{mode:'baked'}});
 const idle=asset('idle','idle',[750,750,750,750]),hit=asset('hit','hit',[50,50,50,100]);
 if(cold)hit.loadPolicy='on-demand';
 r.pipeline.preload=async()=>{};
 Object.defineProperty(r.pipeline,'manifest',{value:{assets:missing?[idle]:[idle,hit]}});
 r.pipeline.get=(id,o)=>{calls.push({id,...o});const a=id==='idle'?idle:hit;return cold&&id==='hit'?{asset:a,image:null,pending:true}:{asset:a,image:{},frame:o.frame,sx:0,sy:0,sw:128,sh:128,render:{width:42,height:42},pivot:{x:64,y:110},contactShadow:{mode:'baked'}};};
 await r.preload();
 return {r,calls,sample(entity,tick,timeMs=tick*50){const o={tick,timeMs};r.observeEntities([entity],o);return r.sampleEntity(entity,o);}};
}
test('five-tick hit starts F0, uses interpolated time, reaches recovery and expires at authoritative tick',async()=>{
 const f=await fixture(),hurt={...actor,hitUntil:105};
 for(const [tick,timeMs,frame,elapsed] of [[100,4950,0,0],[100,5000,0,0],[100,5049,0,49],[101,5050,1,50],[102,5100,2,100],[103,5150,3,150],[104,5249,3,249]]){
  const p=f.sample(hurt,tick,timeMs);assert.equal(p.visualState,'hit');assert.equal(p.elapsed,elapsed);assert.equal(p.sample.frame,frame);assert.equal(p.raster.frame,frame);
 }
 const expired=f.sample(hurt,105);assert.equal(expired.visualState,'idle');assert.equal(expired.sample.frame,0);assert.equal(expired.elapsed,0);
 f.r.dispose();
});
test('refreshed hitUntil restarts event F0, a late observer samples received event age',async()=>{
 const f=await fixture();assert.equal(f.sample({...actor,hitUntil:105},103).sample.frame,3);
 const renewed=f.sample({...actor,hitUntil:108},103);assert.equal(renewed.elapsed,0);assert.equal(renewed.sample.frame,0);
 const fresh=await fixture();assert.equal(fresh.sample({...actor,hitUntil:105},102).sample.frame,2);f.r.dispose();fresh.r.dispose();
});
test('missing and cold hit stay diagnosed static original idle; HP0 never requests art',async()=>{
 for(const options of [{cold:true},{missing:true}]){
  const f=await fixture(options),p=f.sample({...actor,hitUntil:105},102);assert.equal(p.requestedState,'hit');assert.equal(p.visualState,'idle');assert.equal(p.presentation,'STATIC_ILLUSTRATION');assert.equal(p.sample.frame,0);assert.equal(p.elapsed,0);
  if(options.cold)assert.equal(p.pagePending,true);
  const count=f.calls.length;assert.equal(f.sample({...actor,hp:0,hitUntil:105},102),false);assert.equal(f.calls.length,count);f.r.dispose();
 }
});
test('Pause keeps hit phase on frozen presentation time and Resume advances only received ticks',async()=>{
 const f=await fixture(),clock=createPresentationClock(),hurt={...actor,hitUntil:105};
 clock.reset({tick:100,map:{id:'test'}},0);clock.receive({tick:102,map:{id:'test'}},100);const time=clock.sample(150);
 const before=f.sample(hurt,102,time);clock.receive({tick:102,map:{id:'test'}},150,{paused:true});
 assert.equal(clock.sample(9999),time);const paused=f.sample(hurt,102,clock.sample(9999));assert.equal(paused.elapsed,before.elapsed);assert.equal(paused.sample.frame,before.sample.frame);
 clock.receive({tick:103,map:{id:'test'}},10000);const resumed=f.sample(hurt,103,clock.sample(10100));assert.equal(resumed.elapsed,150);assert.equal(resumed.sample.frame,3);f.r.dispose();
});
