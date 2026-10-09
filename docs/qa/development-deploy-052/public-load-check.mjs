import {chromium,firefox} from 'playwright';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {writeFile} from 'node:fs/promises';
const base='https://kieu-hoang-quan-loq-15iax9.tail5247a0.ts.net',results=[];
for(const [name,engine] of Object.entries({chromium,firefox})){
 const browser=await engine.launch({headless:true});
 try{for(const art of [false,true]){const ctx=await browser.newContext(),p=await ctx.newPage(),errors=[],pins=[],jobs=[];p.on('pageerror',e=>errors.push(e.message));p.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`);if(/\/assets\/index-[^/]+\.js$/.test(r.url()))jobs.push(r.body().then(b=>pins.push(createHash('sha256').update(b).digest('hex'))));});await p.goto(base+(art?'/?art=work':'/'),{waitUntil:'domcontentloaded'});await p.waitForFunction(()=>!!window.rtsDiagnostics,null,{timeout:30000});if(art)await p.waitForFunction(()=>window.rtsDiagnostics.snapshot().art.pipeline.ready===17,null,{timeout:30000});const s=await p.evaluate(()=>window.rtsDiagnostics.snapshot());await Promise.all(jobs);assert.equal(s.art.enabled,art);if(art){assert.equal(s.art.pipeline.ready,17);assert.equal(s.art.pipeline.failed,0);}else assert.equal(s.art.quality,'PLACEHOLDER_ONLY');assert.deepEqual(errors,[]);assert.ok(pins.length&&pins.every(h=>h==='33da4dd6348b742f8f83bb241c4e01c892dba850668160368a1dadfff047e548'));results.push({name,art,url:p.url(),artStatus:s.art,pins,errors});await ctx.close();}}
 finally{await browser.close();}
}
await writeFile('docs/qa/development-deploy-052/public-load-receipt.json',JSON.stringify({base,normalTLS:true,results},null,2));console.log('PUBLIC_LOAD_PASS',results.length);
