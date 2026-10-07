import {chromium} from 'playwright';
import {mkdir,writeFile,readFile} from 'node:fs/promises';
import assert from 'node:assert/strict';

// Network failures are browser fixtures; no simulation state is injected.
const base=process.env.GAME_URL||'http://127.0.0.1:3000/?art=pilot';
const expectedAssets=JSON.parse(await readFile(new URL('../public/assets/art-v1/manifest.json',import.meta.url),'utf8')).assets.length;
const out=process.env.QA_OUTPUT||'artifacts/loading-recovery';await mkdir(out,{recursive:true});
const browser=await chromium.launch({headless:true}),page=await browser.newPage({viewport:{width:1280,height:800}});
page.setDefaultTimeout(30000);const results=[];
try{
 await page.route('**/assets/art-v1/manifest.json',route=>route.fulfill({status:503,body:'fixture unavailable'}));
 await page.goto(base,{waitUntil:'domcontentloaded'});
 await page.locator('#bootContinue').waitFor({state:'visible'});
 assert.match(await page.locator('#bootStatus').textContent(),/could not finish loading/);
 assert.equal(await page.evaluate(()=>window.rtsDiagnostics.snapshot().art.pipeline.failed),1);
 await page.screenshot({path:`${out}/error.png`});
 await page.locator('#bootContinue').click();await page.locator('#singleStart').click();await page.locator('#launchSingle').click();
 await page.waitForFunction(()=>window.rtsDiagnostics.snapshot().tick>10);
 assert.equal(await page.evaluate(()=>window.rtsDiagnostics.snapshot().art.pipeline.approved),0);
 results.push({scenario:'manifest unavailable',errorVisible:true,explicitDevelopmentContinuation:true,matchStarted:true});
 await page.unroute('**/assets/art-v1/manifest.json');await page.reload({waitUntil:'domcontentloaded'});
 await page.locator('#singleStart').waitFor({state:'visible'});
 assert.equal(await page.evaluate(()=>window.rtsDiagnostics.snapshot().art.pipeline.ready),expectedAssets);
 results.push({scenario:'fresh retry after network recovery',readyAssets:expectedAssets});
 await page.route('**/assets/index-*.js',route=>route.abort('failed'));
 await page.reload({waitUntil:'domcontentloaded'});
 await page.locator('#bootRetry').waitFor({state:'visible',timeout:25000});
 assert.match(await page.locator('#bootStatus').textContent(),/taking too long/);
 await page.unroute('**/assets/index-*.js');await page.locator('#bootRetry').click();
 await page.locator('#singleStart').waitFor({state:'visible'});
 assert.equal(await page.evaluate(()=>window.rtsDiagnostics.snapshot().art.pipeline.ready),expectedAssets);
 results.push({scenario:'bundle network failure',watchdogVisible:true,retryReadyAssets:expectedAssets});
 await writeFile(`${out}/receipt.json`,JSON.stringify({url:base,networkFixtures:true,simulationMutation:false,results},null,2));
 console.log(JSON.stringify(results));
}finally{await browser.close();}
