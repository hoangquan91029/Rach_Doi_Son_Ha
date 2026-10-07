// Actual immutable stills at one whole-canvas scale; never a motion or final-art approval.
import {chromium} from 'playwright';
import {readFile,writeFile,mkdir,access} from 'node:fs/promises';
import {resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
const out=resolve(process.env.QA_OUTPUT||'artifacts/villager-007-static-review');
await mkdir(out,{recursive:true});
if(await access(resolve(out,'receipt.json')).then(()=>true,()=>false))throw Error('Existing static review must not be overwritten; choose a new QA_OUTPUT');
const ledger=JSON.parse(await readFile('docs/art/VILLAGER_IDENTITY_LOCK_007.json','utf8'));
const entries=[];
for(const direction of ['N','NE','E','SE','S','SW','W','NW']){
 const e=ledger.directions[direction];
 if(e.source){const raw=await readFile(e.source);if(createHash('sha256').update(raw).digest('hex')!==e.sha256)throw Error('Static source custody drift: '+direction);}
 entries.push({direction,...e});
}
const count=entries.filter(e=>e.source&&e.status==='STATIC_IDENTITY_REFERENCE_CANDIDATE').length;
if(count!==ledger.staticCandidateCount)throw Error('Static candidate count disagrees with actual source slots');
const browser=await chromium.launch({headless:true});
const receipt={timestamp:new Date().toISOString(),status:count===8?'STATIC_IDENTITY_REVIEW_ONLY':'INCOMPLETE_STATIC_IDENTITY_REVIEW_ONLY',browser:browser.version(),sourceCanvas:[1254,1254],sourcePivot:[654,1140],characterImageEdits:0,animationFrames:0,finalArtApproved:false,entries,outputs:[]};
try{
 for(const size of [627,38]){
  const slot=Math.max(size,200),width=4*(slot+12)+24;
  const cards=entries.map(e=>`<article><div class="cell">${e.source?`<img src="${pathToFileURL(resolve(e.source)).href}" width="${size}" height="${size}" alt="${e.direction}">`:'<span>NOT AUTHORED</span>'}</div><footer>${e.direction} · D${String(e.engineDirection).padStart(2,'0')} / world ${e.worldDirection}<br>${e.source?'STATIC CANDIDATE':'GATE OPEN'}</footer></article>`).join('');
  const html=`<!doctype html><meta charset="utf-8"><title>Villager007 static identity review</title><style>html,body{margin:0;background:#263b32;color:#ece4d0;font:14px sans-serif}header{padding:12px}main{display:grid;grid-template-columns:repeat(4,${slot}px);gap:12px;padding:12px}article{background:#455c50}.cell{height:${size}px;display:flex;align-items:center;justify-content:center}img{display:block;width:${size}px;height:${size}px;object-fit:contain}footer{padding:6px;height:36px;box-sizing:content-box;font-size:12px;line-height:18px}</style><header>STATIC IDENTITY ONLY · ${ledger.staticCandidateCount}/8 · whole1254canvas → ${size}px · pivot6541140 · no motion/final approval</header><main>${cards}</main>`;
  const file=resolve(out,`review-${size}.html`);await writeFile(file,html);
  const page=await browser.newPage({viewport:{width,height:2*(size+60)+70},deviceScaleFactor:1});
  await page.goto(pathToFileURL(file).href);await page.evaluate(()=>Promise.all([...document.images].map(i=>i.decode())));
  const png=await page.screenshot({path:resolve(out,`review-${size}.png`),fullPage:true});receipt.outputs.push({size,path:`review-${size}.png`,sha256:createHash('sha256').update(png).digest('hex')});await page.close();
 }
 await writeFile(resolve(out,'receipt.json'),JSON.stringify(receipt,null,2)+'\n');console.log(JSON.stringify({status:receipt.status,count:ledger.staticCandidateCount,outputs:receipt.outputs}));
}finally{await browser.close();}
