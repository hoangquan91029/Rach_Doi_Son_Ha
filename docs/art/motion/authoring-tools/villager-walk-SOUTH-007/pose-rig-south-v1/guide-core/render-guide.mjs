import {chromium} from '/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha/node_modules/playwright/index.mjs';
import {readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
const dir=new URL('./',import.meta.url), browser=await chromium.launch({headless:true});
const page=await browser.newPage({viewport:{width:1254,height:1254},deviceScaleFactor:1});
const receipt={status:'MODEL_ONLY_GEOMETRY_PROPOSAL_NOT_ANATOMY_OR_ART',canvas:[1254,1254],deviceScaleFactor:1,imageCalls:0,runtimeChanges:false,outputs:[]};
try {
 for (const [name,transparent] of [['guide',true],['guide-qa',false]]) {
   await page.setContent('<style>html,body{margin:0}</style>'+await readFile(new URL(name+'.svg',dir),'utf8'));
   const bytes=await page.screenshot({path:fileURLToPath(new URL(name+'.png',dir)),omitBackground:transparent});
   receipt.outputs.push({path:name+'.png',sha256:createHash('sha256').update(bytes).digest('hex'),alpha:transparent?'transparent':'opaque QA only'});
 }
 await writeFile(new URL('render-receipt.json',dir),JSON.stringify(receipt,null,2)+'\n');
} finally { await browser.close(); }
