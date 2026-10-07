import {chromium} from '/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha/node_modules/playwright/index.mjs';
import {readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
const directory=new URL('./',import.meta.url),browser=await chromium.launch({headless:true}),page=await browser.newPage({viewport:{width:1254,height:1254},deviceScaleFactor:1});
const receipt={status:'MODEL_ONLY_NON_ART_NOT_ANIMATION',browser:browser.version(),canvas:[1254,1254],deviceScaleFactor:1,outputs:[],imageCalls:0,runtimeChanges:false};
try{for(const name of ['guide','guide-qa']){await page.setContent('<style>html,body{margin:0}</style>'+await readFile(new URL(name+'.svg',directory),'utf8'));const png=await page.screenshot({path:fileURLToPath(new URL(name+'.png',directory))});receipt.outputs.push({path:name+'.png',sha256:createHash('sha256').update(png).digest('hex')});}await writeFile(new URL('render-receipt.json',directory),JSON.stringify(receipt,null,2));}finally{await browser.close();}
