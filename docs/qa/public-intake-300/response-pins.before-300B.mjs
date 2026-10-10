import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {writeFile,readFile} from 'node:fs/promises';
const pending=new WeakMap();
export async function claimFiniteCall(name,binding){
 assert.equal(binding.rootAuthorized,true);assert.equal(binding.runGO,true);assert.equal(binding.promotion299Verified,true);
 assert.equal(binding.publicURL,'https://kieu-hoang-quan-loq-15iax9.tail5247a0.ts.net/?art=fort');
 assert.equal(binding.descriptors,53);assert.equal(binding.bundleSHA256,'7da48cba0210023ca9d2737d123e878cbc2fd510a8f5520531bd221dbdf05308');assert.equal(binding.manifestSHA256,'f835505f6fd76c51264af43061d0cc1e109c0c82e0a186a2073d1c0c12ac671f');
 assert.ok(binding.promotionReceiptSHA256&&binding.currentPairedRollbackSHA256,'Root must bind actual299 promotion and current paired rollback before GO');
 if(name==='firefox'){const c=JSON.parse(await readFile(new URL('./browser-receipt.json',import.meta.url),'utf8'));assert.equal(c.status,'PASS300_NORMALTLS_CHROME_CANCELLED_SITE_TERMINAL_WRECK_REMOVAL_EXACT_PICKS_PAUSE_RESUME_STOP_MENU');assert.equal(c.requiredResponsesExact,true);assert.equal(c.cleanup.browserClosed,true);}
 await writeFile(new URL(`./${name}-call-state.json`,import.meta.url),JSON.stringify({status:'CLAIMED_ONE_FINITE_CALL',campaigns:1,retries:0,startedAt:new Date().toISOString()},null,2),{flag:'wx'});
}
export function installResponseTracking(page,r){
 r.errors=[];r.requestFailures=[];r.httpFailures=[];r.actualResponsePins=[];r.responseCaptureErrors=[];const jobs=[];pending.set(r,jobs);
 page.on('pageerror',e=>r.errors.push(e.message));page.on('requestfailed',q=>r.requestFailures.push({url:q.url(),failure:q.failure()}));
 page.on('response',x=>{jobs.push((async()=>{try{const u=new URL(x.url());if(x.status()>=400)r.httpFailures.push({url:x.url(),status:x.status()});if(u.pathname==='/'||u.pathname.startsWith('/assets/')){const body=await x.body(),sha256=createHash('sha256').update(body).digest('hex');r.actualResponsePins.push({url:x.url(),status:x.status(),sha256,bytes:body.length,receivedAtUnixMs:Date.now(),requestTiming:x.request().timing()});if(/\/assets\/index-.*\.js$/.test(u.pathname))r.bundleSHA256=sha256;}}catch(e){r.responseCaptureErrors.push(String(e));}})());});
}
export async function verifyRequiredResponses(r,binding){
 await Promise.all(pending.get(r));assert.deepEqual(r.errors,[]);assert.deepEqual(r.requestFailures,[]);assert.deepEqual(r.httpFailures,[]);assert.deepEqual(r.responseCaptureErrors,[]);
 r.requiredResponsePins=[];for(const [file,sha] of Object.entries(binding.expectedResponseSHA256)){const pathname=file==='index.html'?'/':'/'+file;const rows=r.actualResponsePins.filter(x=>new URL(x.url).pathname===pathname);assert.ok(rows.length,`Required actual response absent: ${file}`);for(const row of rows){assert.equal(row.status,200);assert.equal(row.sha256,sha,`Actual response differs: ${file}`);}r.requiredResponsePins.push({file,expectedSHA256:sha,responses:rows});}r.requiredResponsesExact=true;
}
