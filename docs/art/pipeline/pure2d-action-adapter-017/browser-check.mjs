import {chromium} from 'playwright';
import {mkdir,writeFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
const base=process.env.ADAPTER_URL||'http://127.0.0.1:5173/docs/art/pipeline/pure2d-action-adapter-017/';
const out=new URL('./chromium/',import.meta.url).pathname;
await mkdir(out,{recursive:true});
const browser=await chromium.launch({headless:true});
const page=await browser.newPage({viewport:{width:1100,height:800},deviceScaleFactor:1});
const errors=[],results={};
page.on('pageerror',e=>errors.push(e.message));page.on('requestfailed',r=>errors.push(`${r.url()}: ${r.failure()?.errorText}`));
const diagnostic=()=>page.evaluate(()=>{const d=window.atlasDiagnostic;return typeof d==='function'?d():d?.snapshot?d.snapshot():JSON.parse(JSON.stringify(d));});
try{
 for(const state of ['idle','walk']){
  const url=new URL(`actual-demos/${state}/preview.html`,base).href;
  await page.goto(url);await page.waitForFunction(()=>window.atlasDiagnostic);
  let d=await diagnostic();const expected=state==='idle'?1:8;assert.equal(d.frames,expected);assert.equal(d.loop,true);
  const frames=new Set();const samples=[];const start=Date.now();while(Date.now()-start<1600){d=await diagnostic();frames.add(d.frame);samples.push(d);await page.waitForTimeout(25);}
  assert.deepEqual([...frames].sort((a,b)=>a-b),Array.from({length:expected},(_,i)=>i));
  if(state==='walk'){
   assert.equal(d.durationMs,600);await page.locator('#pause').click();await page.waitForFunction(()=>window.atlasDiagnostic.paused);const before=await diagnostic();assert.equal(before.paused,true);await page.waitForTimeout(180);const after=await diagnostic();assert.equal(after.frame,before.frame);assert.equal(after.clock,before.clock);
   await page.locator('#replay').click();await page.waitForFunction(()=>!window.atlasDiagnostic.paused&&window.atlasDiagnostic.clock<150);d=await diagnostic();assert.equal(d.paused,false);assert.ok(d.clock<150);assert.equal(d.finished,false);
  }
  await page.screenshot({path:`${out}/actual-${state}-89px.png`});
  const load=await page.evaluate(async manifestUrl=>{const {createArtAssetPipeline}=await import('/client/art-assets.js');const pipeline=createArtAssetPipeline({manifestUrl,allowCandidates:true});await pipeline.preload();const stats=JSON.parse(JSON.stringify(pipeline.stats));const assets=pipeline.manifest?.assets.map(a=>({id:a.id,state:a.state,direction:a.direction,frames:a.frames.length,loop:a.loop,render:a.render}));pipeline.dispose();return {stats,assets};},new URL(`actual-demos/${state}/manifest.json`,base).href);
  assert.equal(load.stats.failed,0);assert.ok(load.stats.ready>0);results[state]={url,observedFrames:[...frames].sort(),samples,load};
 }
 assert.deepEqual(errors,[]);await writeFile(`${out}/receipt.json`,JSON.stringify({status:'ACTUAL_IDLE_WALK_GENERIC_ADAPTER_BROWSER_PASS',engine:'chromium',drawSize:89,deviceScaleFactor:1,results,errors,limits:'Actual canonical idle and corrected014 walk only; no new action art, death/attack claim, visual approval or continuous motion verdict.'},null,2)+'\n');console.log(JSON.stringify({status:'PASS',states:Object.keys(results),errors}));
}catch(e){await page.screenshot({path:`${out}/failure.png`});await writeFile(`${out}/failure.json`,JSON.stringify({error:e.message,diagnostic:await diagnostic().catch(()=>null),results,errors},null,2)+'\n');throw e;}finally{await browser.close();}
