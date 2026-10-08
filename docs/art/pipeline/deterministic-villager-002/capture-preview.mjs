/** Local candidate browser validation. Does not deploy, approve art or touch simulation. */
import {chromium,firefox} from 'playwright';
import {mkdir,writeFile} from 'node:fs/promises';
import path from 'node:path';
const url=process.argv[2],out=path.resolve(process.argv[3]||'pilot-browser-capture');
if(!url||!/^http:\/\/(127\.0\.0\.1|localhost):\d+\//.test(url))throw Error('Provide the local preview URL');
await mkdir(out,{recursive:true});
const results=[];
for(const [name,engine] of [['chromium',chromium],['firefox',firefox]]){
 const browser=await engine.launch({headless:true});
 const context=await browser.newContext({viewport:{width:1120,height:700},deviceScaleFactor:1,recordVideo:{dir:path.join(out,name),size:{width:1120,height:700}}});
 const page=await context.newPage(),errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`)});
 await page.goto(url);await page.waitForFunction(()=>window.pilotPreview?.snapshot().ready,null,{timeout:15000});
 const scaleResults=[];
 for(const height of [64,80,96]){
  await page.selectOption('#height',String(height));
  // Observe repeated actual playback; browser time is not a foot-contact proof.
  const first=await page.evaluate(()=>window.pilotPreview.snapshot());
  await page.waitForTimeout(1100);
  const last=await page.evaluate(()=>window.pilotPreview.snapshot());
  if(last.draws-first.draws<10||last.timeMs<=first.timeMs)throw Error('Preview is not animating');
  await page.screenshot({path:path.join(out,`${name}-${height}px-loop.png`)});
  scaleResults.push({height,first,last});
 }
 await page.selectOption('#height','80');
 const keys=[],imagesCount=await page.evaluate(()=>window.pilotPreview.snapshot().frameCount);
 for(const frame of [0,Math.floor(imagesCount/2),imagesCount-1]){
  await page.evaluate(f=>window.pilotPreview.setFrame(f),frame);
  await page.screenshot({path:path.join(out,`${name}-80px-F${frame}.png`)});
  keys.push(await page.evaluate(()=>window.pilotPreview.snapshot()));
 }
 const video=page.video();await context.close();const videoPath=await video.path();
 results.push({browser:name,version:browser.version(),scales:scaleResults,keys,errors,videoPath,status:errors.length?'FAIL':'BROWSER_PLAYBACK_PASS_NOT_VISUAL_APPROVAL'});
 await browser.close();
}
await writeFile(path.join(out,'browser-receipt.json'),JSON.stringify({url,results,artApproved:false,productionIntegrated:false},null,2)+'\n');
console.log(JSON.stringify(results.map(r=>({browser:r.browser,status:r.status,errors:r.errors})),null,2));
