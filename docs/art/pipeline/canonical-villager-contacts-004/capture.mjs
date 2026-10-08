/** Capture existing-image appearance comparisons. No render/art/source mutation. */
import {chromium} from 'playwright';
import {mkdir,writeFile} from 'node:fs/promises';
import path from 'node:path';
const url=process.argv[2],out=path.resolve(process.argv[3]);
if(!/^http:\/\/127\.0\.0\.1:\d+\//.test(url))throw Error('Local URL required');
await mkdir(out,{recursive:false});
const browser=await chromium.launch({headless:true});
try{
 const page=await browser.newPage({viewport:{width:1180,height:720},deviceScaleFactor:1}),errors=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`)});
 await page.goto(url);await page.waitForFunction(()=>window.appearanceAudit?.snapshot().ready);
 const states=[];
 for(const ground of ['neutral','light','dark']){
  await page.selectOption('#ground',ground);await page.screenshot({path:path.join(out,`${ground}.png`)});states.push(await page.evaluate(()=>window.appearanceAudit.snapshot()));
 }
 await writeFile(path.join(out,'receipt.json'),JSON.stringify({status:errors.length?'FAIL':'STATIC_COMPARISON_CAPTURED',browser:browser.version(),url,errors,states,artApproved:false,motionApproved:false},null,2)+'\n');
 if(errors.length)throw Error(errors.join('\n'));
 console.log('Three static gameplay-size comparisons captured; no art/motion approval');
}finally{await browser.close()}
