import {chromium} from 'playwright';
import {mkdir,writeFile,readFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import path from 'node:path';
const [url,output]=process.argv.slice(2);
if(!url||!output||!/^http:\/\/127\.0\.0\.1:\d+\//.test(url))throw Error('Usage: capture.mjs http://127.0.0.1:PORT/preview.html NEW_OUTPUT');
const out=path.resolve(output);await mkdir(out,{recursive:false});
const browser=await chromium.launch({headless:true});
try {
 const page=await browser.newPage({viewport:{width:1120,height:670},deviceScaleFactor:1}),errors=[],states=[],captures=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`)});
 await page.goto(url);await page.waitForFunction(()=>window.contactDiagnostic?.snapshot().ready,{},{timeout:15000});
 for(const ground of ['neutral','light','dark']) {await page.selectOption('#ground',ground);const file=path.join(out,ground+'.png');await page.screenshot({path:file});states.push(await page.evaluate(()=>window.contactDiagnostic.snapshot()));captures.push({path:file,encodedSha256:createHash('sha256').update(await readFile(file)).digest('hex')})}
 await writeFile(path.join(out,'receipt.json'),JSON.stringify({status:errors.length?'CAPTURE_FAILED':'STATIC_CONTACT_DIAGNOSTIC_NOT_MOTION_APPROVAL',url,browser:browser.version(),errors,states,captures},null,2)+'\n');
 if(errors.length)throw Error(errors.join('\n'));
} finally {await browser.close()}
