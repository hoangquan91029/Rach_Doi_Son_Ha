import {chromium} from 'playwright';
import {mkdir,writeFile} from 'node:fs/promises';
import path from 'node:path';
const url='http://127.0.0.1:8766/docs/art/pipeline/deterministic-villager-003/preview.html';
const out=path.resolve('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha-art-lease/deterministic-villager-003/independent-motion-review-v1/captures');
await mkdir(out,{recursive:true});
const browser=await chromium.launch({headless:true});
const context=await browser.newContext({viewport:{width:1120,height:700},deviceScaleFactor:1});
const page=await context.newPage();
const errors=[];page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`)});
await page.goto(url);await page.waitForFunction(()=>window.pilotPreview?.snapshot().ready,null,{timeout:15000});
const capture=async name=>{const snap=await page.evaluate(()=>window.pilotPreview.snapshot());await page.screenshot({path:path.join(out,name)});return snap};
const runs=[];
for(const height of [64,80,96]){
 await page.locator('#rate').selectOption('1');
 await page.locator('#height').selectOption(String(height));
 for(const ground of ['neutral','dark','light']){
  await page.locator('#ground').selectOption(ground);await page.waitForTimeout(740);
  const name=`loop-${height}-${ground}-1x.png`;const snap=await capture(name);
  runs.push({name,height,ground,rate:1,snapshot:snap});
 }
}
await page.locator('#height').selectOption('80');await page.locator('#ground').selectOption('neutral');
for(const rate of ['0.5','1.5']){
 await page.locator('#rate').selectOption(rate);await page.waitForTimeout(740);
 const name=`loop-80-neutral-${rate.replace('.','p')}x.png`;const snap=await capture(name);
 runs.push({name,height:80,ground:'neutral',rate:Number(rate),snapshot:snap});
}
await page.locator('#rate').selectOption('1');
for(const frame of [0,24,47,0]){
 await page.evaluate(f=>window.pilotPreview.setFrame(f),frame);
 await page.waitForTimeout(50);
 const name=`key-80-neutral-F${frame}-${runs.filter(x=>x.name.startsWith(`key-80-neutral-F${frame}-`)).length}.png`;
 const snap=await capture(name);runs.push({name,height:80,ground:'neutral',rate:1,forcedFrame:frame,snapshot:snap});
}
const result={status:errors.length?'BROWSER_FAIL':'BROWSER_CAPTURES_READY_NOT_VISUAL_APPROVAL',url,viewport:{width:1120,height:700},deviceScaleFactor:1,canvasSnapshot:await page.evaluate(()=>window.pilotPreview.snapshot()),errors,captures:runs};
await writeFile(path.join(out,'capture-receipt.json'),JSON.stringify(result,null,2)+'\n');
await context.close();await browser.close();
console.log(JSON.stringify({status:result.status,captures:runs.length,errors}));
