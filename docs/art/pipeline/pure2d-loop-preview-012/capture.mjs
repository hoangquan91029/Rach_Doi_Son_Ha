import {chromium} from 'playwright';
import {mkdir,writeFile,readFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import path from 'node:path';
const [url,output]=process.argv.slice(2);
if(!url||!output||!/^http:\/\/127\.0\.0\.1:\d+\//.test(url))throw Error('Localhost URL and NEW output required');
const out=path.resolve(output);await mkdir(out,{recursive:false});const browser=await chromium.launch({headless:true});
try {
 const page=await browser.newPage({viewport:{width:900,height:560},deviceScaleFactor:1}),errors=[];page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`)});
 await page.goto(url);await page.waitForFunction(()=>window.atlasDiagnostic?.frames===8);
 const first=await page.evaluate(()=>window.atlasDiagnostic);if(first.status.includes('NON_ART'))throw Error('No synthetic motion capture');
 await page.waitForFunction(()=>{const d=window.atlasDiagnostic;return d.speed===1&&!d.paused&&d.clock>=d.cycleDurationMs*3&&d.seen.length===8},null,{timeout:60000});
 await page.screenshot({path:path.join(out,'normal-playback.png')});const state=await page.evaluate(()=>window.atlasDiagnostic);const hash=createHash('sha256').update(await readFile(path.join(out,'normal-playback.png'))).digest('hex');
 await writeFile(path.join(out,'receipt.json'),JSON.stringify({status:errors.length?'CAPTURE_FAILED':'EIGHT_FRAMES_SEEN_THREE_CYCLES_TECHNICAL_CAPTURE',url,browser:browser.version(),dpr:1,errors,state,screenshotSha256:hash,artifact:'APNG produced separately by export-apng.py; screenshot alone is not motion evidence'},null,2)+'\n');if(errors.length)throw Error(errors.join('\n'));
}finally{await browser.close()}
