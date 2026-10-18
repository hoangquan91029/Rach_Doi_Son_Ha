import test from 'node:test';import assert from 'node:assert/strict';
import {createIdleEntryClock} from '../client/action-presentation.js';import {createRasterSlice} from '../client/raster-slice.js';
const actor={id:12,type:'villager',kind:'unit',hp:100,state:'idle',dir:1,x:3,y:4,owner:0};
const observe=(clock,entities,timeMs,extra={})=>clock.observe(entities,{tick:Math.floor(timeMs/50),timeMs,...extra});
test('true idle entry, semantic missing actions, hit/episode transitions, facing and identity reset',()=>{
 const c=createIdleEntryClock();observe(c,[actor],2250);assert.equal(c.sample(12),0);observe(c,[actor],3000);assert.equal(c.sample(12),750);
 let t=4000;for(const a of [{state:'walk'},{state:'attack'},{state:'idle',hitUntil:999},{state:'idle',visibleAction:{kind:'ability'}},{state:'gather',visibleAction:{kind:'gather',resource:'wood'}},{state:'idle',visibleAction:{kind:'load'}},{state:'repair'},{state:'idle',visibleAction:{kind:'unload'}},{state:'build'}]){observe(c,[{...actor,...a}],t);assert.equal(c.size,0);observe(c,[actor],t+250);assert.equal(c.sample(12),0);observe(c,[actor],t+750);assert.equal(c.sample(12),500);t+=1000;}
 observe(c,[{...actor,dir:2}],t);assert.equal(c.sample(12),0);observe(c,[{...actor,type:'infantry',dir:2}],t+500);assert.equal(c.sample(12),0);observe(c,[actor],100);assert.equal(c.sample(12),0);
});
test('pause freezes, reentry starts once, absent/dead pruned, capacity bounded and clear resets',()=>{
 const c=createIdleEntryClock({maxEntries:2});observe(c,[actor],2250);observe(c,[actor],2500);observe(c,[actor],3500,{frozen:true});assert.equal(c.sample(12),250);observe(c,[actor],4000);assert.equal(c.sample(12),750);
 observe(c,[actor,{...actor,id:13},{...actor,id:14}],4050);assert.equal(c.size,2);observe(c,[{...actor,id:14}],4100);assert.equal(c.size,1);assert.equal(c.sample(14),0);observe(c,[{...actor,id:14,hp:0}],4200);assert.equal(c.size,0);observe(c,[actor],4300);assert.equal(c.sample(12),0);c.clear();assert.equal(c.size,0);assert.equal(c.sample(12),0);
});
async function raster(){const r=createRasterSlice({enabled:true});const asset={id:'idle',kind:'unit',family:'unit.villager',state:'idle',direction:1,frames:Array.from({length:4},()=>({durationMs:750})),contactShadow:{mode:'baked'}};r.pipeline.preload=async()=>{};Object.defineProperty(r.pipeline,'manifest',{value:{assets:[asset]}});r.pipeline.get=(id,{frame})=>({asset,image:{},frame,sx:0,sy:0,sw:128,sh:128,render:{width:42,height:42},pivot:{x:64,y:110},contactShadow:{mode:'baked'}});await r.preload();return r;}
test('raster actual idle entry F0 at global2250; missing walking bank fallback static and return restartsF0',async()=>{
 const r=await raster();const o={tick:45,timeMs:2250};r.observeEntities([actor],o);assert.equal(r.sampleEntity(actor,o).sample.frame,0);r.observeEntities([actor],{tick:60,timeMs:3000});assert.equal(r.sampleEntity(actor,{tick:60,timeMs:3000}).sample.frame,1);
 const walking={...actor,state:'walk'};r.observeEntities([walking],{tick:70,timeMs:3500});let p=r.sampleEntity(walking,{tick:70,timeMs:3500});assert.equal(p.staticIllustrationFallback,true);assert.equal(p.elapsed,0);assert.equal(p.sample.frame,0);r.observeEntities([actor],{tick:80,timeMs:4000});p=r.sampleEntity(actor,{tick:80,timeMs:4000});assert.equal(p.staticIllustrationFallback,false);assert.equal(p.sample.frame,0);r.dispose();
 const fresh=await raster();fresh.observeEntities([actor],{tick:100,timeMs:5000});assert.equal(fresh.sampleEntity(actor,{tick:100,timeMs:5000}).sample.frame,0);fresh.dispose();
});

test('cold declared action still shows static originalF0 without preserving previous idle clock',async()=>{
 const r=await raster();const idle=r.pipeline.manifest.assets[0];const walk={...idle,id:'cold-walk',state:'walk',loadPolicy:'on-demand'};r.pipeline.manifest.assets.push(walk);const get=r.pipeline.get;r.pipeline.get=(id,o)=>id===walk.id?{asset:walk,image:null,pending:true}:get(id,o);
 r.observeEntities([actor],{tick:45,timeMs:2250});r.observeEntities([actor],{tick:60,timeMs:3000});const walking={...actor,state:'walk'};r.observeEntities([walking],{tick:65,timeMs:3250});const p=r.sampleEntity(walking,{tick:65,timeMs:3250});assert.equal(p.pagePending,true);assert.equal(p.presentation,'STATIC_ILLUSTRATION');assert.equal(p.sample.frame,0);assert.equal(p.elapsed,0);
 r.observeEntities([actor],{tick:70,timeMs:3500});assert.equal(r.sampleEntity(actor,{tick:70,timeMs:3500}).sample.frame,0);r.dispose();
});
