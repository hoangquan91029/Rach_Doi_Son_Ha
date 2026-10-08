import {chromium,firefox} from 'playwright';
import {mkdir,writeFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
const engine=process.env.QA_BROWSER||'chromium',base=process.env.GAME_URL||'http://127.0.0.1:5173/?art=walk',out=new URL(`./${engine}/`,import.meta.url).pathname;
await mkdir(out,{recursive:true});
const browser=await ({chromium,firefox}[engine]).launch({headless:true});
const page=await browser.newPage({viewport:{width:1440,height:900},deviceScaleFactor:1}),errors=[];
page.on('pageerror',e=>errors.push(e.message));page.on('requestfailed',r=>errors.push(`${r.url()}: ${r.failure()?.errorText}`));
const snap=()=>page.evaluate(()=>window.rtsDiagnostics.snapshot());
const wait=async(predicate,timeout=12000)=>{const t=Date.now();while(Date.now()-t<timeout){const s=await snap();if(predicate(s))return s;await page.waitForTimeout(50);}throw Error('Normal UI gameplay condition not reached');};
try{
 await page.goto(base);await page.locator('#singleStart').waitFor({state:'visible'});await page.locator('#singleStart').click();await page.locator('#difficulty').selectOption('easy');await page.locator('#launchSingle').click();
 let s=await wait(s=>s.tick>3);assert.equal(s.art.pipeline.failed,0);assert.equal(s.camera.zoom,1.08);
 const e=s.displayedState.entities.find(e=>e.owner===0&&e.type==='villager');assert.ok(e);
 const mini=page.locator('#minimap'),box=await mini.boundingBox();await mini.click({position:{x:e.x/s.displayedState.map.width*box.width,y:e.y/s.displayedState.map.height*box.height}});
 const point=await page.evaluate(id=>window.rtsDiagnostics.entityPoint(id),e.id);await page.locator('#world').click({position:point});await wait(s=>s.selection.includes(e.id));
 const target={x:e.x+8,y:e.y+8},p=await page.evaluate(t=>window.rtsDiagnostics.point(t.x,t.y),target);await page.locator('#world').click({position:p,button:'right'});
 const samples=[],frames=new Set(),t=Date.now();while(Date.now()-t<5000){s=await snap();const w=s.art.lastWalk;if(w?.entityId===e.id&&w.direction===1){samples.push({tick:s.tick,...w});frames.add(w.frame);}if(frames.size===8)break;await page.waitForTimeout(30);}const fullSouthLoopObserved=frames.size===8;
 await page.screenshot({path:`${out}/moving.png`});await page.locator('#pauseBtn').click();await page.waitForTimeout(120);const before=await snap();await page.waitForTimeout(350);const after=await snap();assert.equal(before.tick,after.tick);const phasePauseVerified=Boolean(before.art.lastWalk&&after.art.lastWalk);if(phasePauseVerified){assert.equal(before.art.lastWalk.frame,after.art.lastWalk.frame);assert.equal(before.art.lastWalk.distance,after.art.lastWalk.distance);}
 await page.locator('#resume').click();await page.keyboard.press('s');s=await wait(s=>s.displayedState.entities.find(x=>x.id===e.id)?.state==='idle');await page.screenshot({path:`${out}/stopped.png`});assert.deepEqual(errors,[]);
 await writeFile(`${out}/receipt.json`,JSON.stringify({status:fullSouthLoopObserved?'ACTUAL_LOCAL_GAME_WALK_PAUSE_STOP_CHECK':'LOCAL_GAME_NAVIGATION_HOLD',engine,url:base,normalZoom:s.camera.zoom,commands:'UI only, no simulation mutation',entityId:e.id,frames:[...frames].sort(),samples,simulationPauseFrozen:true,phasePauseVerified,fullSouthLoopObserved,stoppedState:'idle',errors,art:s.art,limits:'One authored direction only; existing four-neighbor navigation prevented South/D1 full-loop observation. Loader/UI checks do not grant motion/foot-lock/production approval.'},null,2)+'\n');console.log(JSON.stringify({engine,frames:[...frames].sort(),simulationPauseFrozen:true,phasePauseVerified,fullSouthLoopObserved,stopped:true,errors}));
}catch(error){await page.screenshot({path:`${out}/failure.png`});await writeFile(`${out}/failure.json`,JSON.stringify({error:error.message,errors,snapshot:await snap().catch(()=>null)},null,2)+'\n');throw error;}finally{await browser.close();}
