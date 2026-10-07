import {chromium,firefox} from 'playwright';
import {mkdir,writeFile} from 'node:fs/promises';
import assert from 'node:assert/strict';

// Actual UI commands and read-only diagnostics. This never edits simulation state.
const engine=process.env.QA_BROWSER||'chromium';
const base=process.env.GAME_URL||'http://127.0.0.1:3000/';
const out=process.env.QA_OUTPUT||`artifacts/art-v1/browser-${engine}`;
await mkdir(out,{recursive:true});
const browser=await ({chromium,firefox}[engine]).launch({headless:true,...(engine==='chromium'&&process.env.QA_RESOLVE_IP?{args:[`--host-resolver-rules=MAP ${new URL(base).hostname} ${process.env.QA_RESOLVE_IP}`]}:{})});
const page=await browser.newPage({viewport:{width:1440,height:900},deviceScaleFactor:1});
page.setDefaultTimeout(30000);
const errors=[],failedRequests=[];page.on('pageerror',error=>errors.push(error.message));page.on('requestfailed',request=>failedRequests.push({url:request.url(),failure:request.failure()}));
const snap=()=>page.evaluate(()=>window.rtsDiagnostics.snapshot());
const click=async(x,y,button='left')=>{const s=await snap(),mini=page.locator('#minimap'),box=await mini.boundingBox();await mini.click({position:{x:x/s.displayedState.map.width*box.width,y:y/s.displayedState.map.height*box.height}});await page.waitForTimeout(80);const pt=await page.evaluate(([x,y])=>window.rtsDiagnostics.point(x,y),[x,y]);await page.locator('#world').click({position:pt,button});};
const select=async(e)=>{const s=await snap(),mini=page.locator('#minimap'),box=await mini.boundingBox();await mini.click({position:{x:e.x/s.displayedState.map.width*box.width,y:e.y/s.displayedState.map.height*box.height}});await page.waitForTimeout(80);const pt=await page.evaluate(id=>window.rtsDiagnostics.entityPoint(id),e.id);await page.locator('#world').click({position:pt});};
const wait=async(predicate,timeout=45000)=>{const started=Date.now();while(Date.now()-started<timeout){const s=await snap();if(predicate(s))return s;await page.waitForTimeout(200);}throw Error('Timed out waiting for normal gameplay action');};
try{
 const url=new URL(base);url.searchParams.set('art','pilot');await page.goto(url.href,{waitUntil:'networkidle'});
 await page.locator('#singleStart').click();await page.locator('#difficulty').selectOption('easy');await page.locator('#launchSingle').click();
 let s=await wait(s=>s.tick>10);assert.equal(s.camera.zoom,1.08);assert.equal(s.art.pipeline.failed,0);
 await page.screenshot({path:`${out}/start.png`});
 await page.locator('[data-leader="general"]').click();s=await snap();assert.ok(s.selection.includes(s.displayedState.entities.find(e=>e.owner===0&&e.type==='general').id));
 await page.screenshot({path:`${out}/general-hud.png`});
 const worker=s.displayedState.entities.find(e=>e.owner===0&&e.type==='villager');await select(worker);await wait(s=>s.selection.includes(worker.id));
 await page.locator('[data-act="build"][data-value="cavalryCamp"]').click();await click(17,21);
 s=await wait(s=>s.displayedState.entities.some(e=>e.owner===0&&e.type==='cavalryCamp'&&!e.construction));
 const camp=s.displayedState.entities.find(e=>e.owner===0&&e.type==='cavalryCamp');await select(camp);await wait(s=>s.selection.includes(camp.id));
 await page.locator('[data-act="train"][data-value="cavalry"]').click();s=await wait(s=>s.displayedState.entities.some(e=>e.owner===0&&e.type==='cavalry'));
 await page.screenshot({path:`${out}/trained-cavalry.png`});
 const cavalry=s.displayedState.entities.find(e=>e.owner===0&&e.type==='cavalry');await select(cavalry);await wait(s=>s.selection.includes(cavalry.id));await click(23,24,'right');
 s=await wait(s=>s.displayedState.entities.find(e=>e.id===cavalry.id)?.state==='walk');await page.screenshot({path:`${out}/movement-placeholder.png`});
 assert.ok(s.art.missing.some(item=>item.key.startsWith('cavalry:walk:')),'Missing walk must be explicitly recorded');
 await click(32,24,'right');s=await wait(s=>s.displayedState.entities.find(e=>e.id===cavalry.id)?.x>29);
 const minimap=page.locator('#minimap'),box=await minimap.boundingBox();await minimap.click({position:{x:32/s.displayedState.map.width*box.width,y:24/s.displayedState.map.height*box.height}});await page.waitForTimeout(250);
 await page.screenshot({path:`${out}/scouted-river.png`});s=await snap();

 await writeFile(`${out}/receipt.json`,JSON.stringify({date:new Date().toISOString(),url:url.href,engine,normalZoom:1.08,commands:'UI only',visualApproval:false,quality:'PLACEHOLDER_ONLY',errors,art:s.art},null,2));assert.deepEqual(errors,[]);
 console.log(JSON.stringify({engine,normalZoom:s.camera.zoom,trainedCavalry:true,missingMovementRecorded:true,errors,visualApproval:false}));
}catch(error){await page.screenshot({path:`${out}/failure.png`});const snapshot=await snap().catch(()=>null);await writeFile(`${out}/failure.json`,JSON.stringify({error:error.stack,url:page.url(),snapshot,errors,failedRequests},null,2));throw error;}finally{await browser.close();}
