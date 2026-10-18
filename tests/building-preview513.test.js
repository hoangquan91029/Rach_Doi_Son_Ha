import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';import path from 'node:path';import http from 'node:http';import {chromium} from 'playwright';
test('SYNTHETIC whole-cell unit, looping construction and finite building preview controls',async()=>{
 const root=path.resolve('docs/qa/building-preview-513/fixture');fs.mkdirSync(root,{recursive:true});fs.copyFileSync('scripts/sprite-preview.html',path.join(root,'preview.html'));let browser,server;
 try{
 server=http.createServer((q,s)=>{const p=path.join(root,q.url==='/'?'preview.html':q.url);try{s.end(fs.readFileSync(p));}catch{s.writeHead(404).end();}});await new Promise(ok=>server.listen(0,'127.0.0.1',ok));browser=await chromium.launch({headless:true});
 const page=await browser.newPage();const url='http://127.0.0.1:'+server.address().port;
 for(const [building,loop] of [[false,true],[true,true],[true,false]]){
 const asset={kind:building?'building':'unit',direction:building?null:1,loop,runtime:{path:'atlas.png'},render:{width:42,height:42},frames:Array.from({length:4},(_,i)=>({x:i*16,y:0,width:16,height:16,durationMs:120}))};fs.writeFileSync(path.join(root,'asset.json'),JSON.stringify(asset));
 await page.goto(url);await page.waitForFunction(()=>previewState.ready);await page.waitForFunction(()=>previewState.looping?previewState.cycles>=3:previewState.completed);
 let state=await page.evaluate(()=>previewState);assert.equal(state.seen.length,4);assert.equal(await page.locator('#bank figure').count(),building?0:8);assert.equal(state.errors.length,0);
 if(!loop){assert.equal(state.frame,3);assert.equal(state.elapsed,480);await page.waitForTimeout(150);assert.equal(await page.evaluate(()=>previewState.elapsed),480);await page.locator('#replay').click();await page.waitForFunction(()=>previewState.elapsed>0&&!previewState.completed);}
 await page.locator('#toggle').click();const elapsed=await page.evaluate(()=>previewState.elapsed);await page.waitForTimeout(100);assert.equal(await page.evaluate(()=>previewState.elapsed),elapsed);await page.locator('#toggle').click();await page.waitForFunction(e=>previewState.elapsed>e,elapsed);assert.ok(Math.abs((await page.locator('#motion').boundingBox()).width-70.56)<.02);
 }
 }finally{await browser?.close();await new Promise(ok=>server?server.close(ok):ok());}
});
