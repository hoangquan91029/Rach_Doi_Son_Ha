import test from 'node:test';import assert from 'node:assert/strict';import {readFileSync} from 'node:fs';import {foodResourceEligible} from '../client/terrain-props.js';
test('only live finite food resources select illustrated node',()=>{const r={type:'food',amount:1,x:4,y:8};const before=JSON.stringify(r);assert.equal(foodResourceEligible(r),true);for(const p of [{type:'wood'},{amount:0},{amount:-1},{amount:Infinity},{x:NaN},{y:undefined}])assert.equal(foodResourceEligible({...r,...p}),false);assert.equal(JSON.stringify(r),before);});
test('empty resource suppression and ordinary fallback remain after raster attempt',()=>{const r=readFileSync(new URL('../client/renderer.js',import.meta.url),'utf8');assert.match(r,/resources\|\|\[\]\)\.filter\(r=>r.amount>0/);assert.match(r,/drawResource\(c,r\)\{if\(!\(r.amount>0\)\)return;if\(this.raster.drawResource/);assert.ok(r.indexOf('this.raster.drawResource(c')<r.indexOf("c.fillStyle='#dab872'"));const s=readFileSync(new URL('../client/raster-slice.js',import.meta.url),'utf8');assert.match(s,/!worldArtEnabled\(\)\|\|!staticResourceEligible/);assert.match(s,/if\(!raster\)return false/);});
test('food static schema relative loader path and exact wholecanvas custody',()=>{const m=JSON.parse(readFileSync(new URL('../public/assets/art-v1/terrain-115-manifest.json',import.meta.url)));assert.equal(m.assets.length,20);const a=m.assets.find(a=>a.id==='food-resource-114');assert.equal(a.kind,'prop');assert.equal(a.state,'static');assert.equal(a.direction,null);assert.deepEqual(a.render,{width:48,height:48});assert.equal(a.runtime.path,'food-resource-115/food.png');assert.equal(a.runtime.sha256,'bf51cb7b25174a866bd86506a94dede5348bd30f0eae5c4a365aec0ef7b68801');assert.equal(a.pivot.y/a.source.height*a.runtime.height,92.16);});

// Exercise renderer route gating through real manifest/hash loading. Only browser I/O
// (fetch and bitmap decode) is replaced; eligibility and route/state logic are real.
import {createRasterSlice} from '../client/raster-slice.js';
import {createHash} from 'node:crypto';
test('world route contract permits terrain/iron/workshop/camp and excludes character-only routes',async()=>{
 const saved=Object.fromEntries(['location','fetch','createImageBitmap'].map(k=>[k,Object.getOwnPropertyDescriptor(globalThis,k)]));
 const bank=JSON.parse(readFileSync(new URL('../public/assets/art-v1/camp-148-manifest.json',import.meta.url)));
 bank.assets=bank.assets.filter(a=>a.id==='food-resource-114'||a.family==='hill');assert.equal(bank.assets.length,2);
 const sizes=new Map(bank.assets.map(a=>[a.runtime.sha256,[a.runtime.width,a.runtime.height]]));
 try{
  globalThis.fetch=async url=>{const pathname=new URL(url).pathname;return {ok:true,text:async()=>JSON.stringify(bank),arrayBuffer:async()=>{const b=readFileSync(new URL(`../public${pathname}`,import.meta.url));return b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength);}};};
  globalThis.createImageBitmap=async blob=>{const bytes=Buffer.from(await blob.arrayBuffer()),size=sizes.get(createHash('sha256').update(bytes).digest('hex'));assert.ok(size,'only actual pinned images decoded');return {width:size[0],height:size[1],close(){}};};
  for(const route of ['terrain','iron','workshop','camp','pilot','walk','work','food','']){
   globalThis.location={href:`https://contract.test/?art=${route}`,search:`?art=${route}`};
   // Use one exact bank for all routes so gate failures cannot be masked by missing assets.
   const slice=createRasterSlice({manifestUrl:'/assets/art-v1/camp-148-manifest.json'});await slice.preload();
   if(route)assert.equal(slice.pipeline.stats.ready,2);
   const draws=[],ctx={drawImage(...args){draws.push(args);}},project=(x,y)=>({x,y});
   const allowed=['terrain','iron','workshop','camp'].includes(route);
   assert.equal(slice.drawResource(ctx,{resource:{type:'food',amount:1,x:4,y:8},project}),allowed,route);
   assert.equal(slice.drawResource(ctx,{resource:{type:'food',amount:0,x:4,y:8},project}),false,`${route}: depleted`);
   const state={map:{width:2,height:2,tiles:Array(4).fill('hill')},fog:{visible:Array(4).fill(true)}};
   assert.equal(slice.drawHillGround(ctx,{state,project}),allowed?1:0,`${route}: hill`);
   state.fog.visible[0]=false;assert.equal(slice.drawHillGround(ctx,{state,project}),0,`${route}: hidden hill`);
   assert.equal(draws.length,allowed?2:0,`${route}: no extra drawing`);
   slice.dispose();
  }
 }finally{for(const [key,descriptor] of Object.entries(saved)){if(descriptor)Object.defineProperty(globalThis,key,descriptor);else delete globalThis[key];}}
});
