import {chromium,firefox} from 'playwright';
import {mkdir,writeFile} from 'node:fs/promises';
const base=process.env.GAME_URL||'http://127.0.0.1:3000/',out=process.env.QA_OUTPUT||'artifacts/performance/shore-contrasts',duration=Number(process.env.QA_DURATION||4000);
await mkdir(out,{recursive:true});
const percentile=(values,p)=>values.length?[...values].sort((a,b)=>a-b)[Math.floor((values.length-1)*p)]:null;
const summarize=values=>({p50:percentile(values,.5),p95:percentile(values,.95),count:values.length});
async function sample(page,diagnostics=false){
 const result=await page.evaluate(({duration,diagnostics})=>new Promise(resolve=>{
  const start=performance.now(),cadence=[],frameCost=[],cloneCost=[];let prior,lastSnapshot=start;
  function frame(now){if(prior!==undefined)cadence.push(now-prior);prior=now;
   if(diagnostics&&now-lastSnapshot>=1000){const before=performance.now(),s=window.rtsDiagnostics.snapshot();cloneCost.push(performance.now()-before);frameCost.push(s.frameMs);lastSnapshot=now;}
   if(now-start>=duration)resolve({cadence,frameCost,cloneCost,visibility:document.visibilityState});else requestAnimationFrame(frame);
  }requestAnimationFrame(frame);
 }),{duration,diagnostics});
 return {cadenceMs:summarize(result.cadence),frameCostMs:summarize(result.frameCost),snapshotCloneMs:summarize(result.cloneCost),visibility:result.visibility};
}
const results=[];
for(const engine of (process.env.QA_BROWSER?[process.env.QA_BROWSER]:['chromium','firefox'])){
 const browser=await ({chromium,firefox}[engine]).launch({headless:true});
 try{for(const candidate of [false,true]){
  const page=await browser.newPage({viewport:{width:1440,height:900},deviceScaleFactor:1}),errors=[];page.on('pageerror',e=>errors.push(e.message));
  const url=new URL(base);if(candidate)url.searchParams.set('art','pilot');await page.goto(url.href,{waitUntil:'networkidle'});
  const menu=await sample(page);
  await page.locator('#singleStart').click();await page.locator('#difficulty').selectOption('easy');await page.locator('#launchSingle').click();
  await page.waitForFunction(()=>window.rtsDiagnostics.snapshot().tick>10);await page.waitForTimeout(500);
  const basePure=await sample(page),baseRare=await sample(page,true);
  const before=await page.evaluate(()=>window.rtsDiagnostics.snapshot()),map=before.displayedState.map;
  // Camera movement is an ordinary minimap click. No orders, entities or state injection.
  const mini=page.locator('#minimap'),box=await mini.boundingBox();await mini.click({position:{x:27/map.width*box.width,y:24/map.height*box.height}});await page.waitForTimeout(500);
  const riverPure=await sample(page),riverRare=await sample(page,true),after=await page.evaluate(()=>window.rtsDiagnostics.snapshot());
  const receipt={engine,version:browser.version(),candidate,menu,basePure,baseRare,riverPure,riverRare,entities:before.displayedState.entities.length,camera:{base:before.camera,river:after.camera},tick:after.tick,artAssets:after.art.pipeline.ready,terrainCache:after.terrainCache,errors};results.push(receipt);console.log(JSON.stringify(receipt));await page.close();
 }}finally{await browser.close();}
}
await writeFile(`${out}/receipt.json`,JSON.stringify({url:base,viewport:[1440,900],headless:true,durationMs:duration,method:'Actual initial easy single-player UI and minimap camera movement; pure RAF samples plus separate 1Hz read-only snapshots. No dense battle.',results},null,2));
