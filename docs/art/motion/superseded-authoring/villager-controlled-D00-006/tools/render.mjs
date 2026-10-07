// Render only preflighted SVG compositions of genuine original components.
import {chromium} from '/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha/node_modules/playwright/index.mjs';
import {readFile,readdir,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
const directory=path.resolve(process.argv[2]||''),receipt=JSON.parse(await readFile(path.join(directory,'render-inputs.json'),'utf8'));
const browser=await chromium.launch({headless:true}),page=await browser.newPage({viewport:{width:1254,height:1254},deviceScaleFactor:1});
try{receipt.renderer={browser:'Chromium',version:browser.version(),deviceScaleFactor:1,canvas:[1254,1254]};receipt.frames=[];for(const file of (await readdir(directory)).filter(f=>/^[FP]\d\d\.svg$/.test(f)).sort()){
 const svg=await readFile(path.join(directory,file),'utf8');await page.setContent('<style>html,body{margin:0;background:transparent}</style>'+svg);
 await page.evaluate(()=>Promise.all([...document.images].map(i=>i.decode())));const png=await page.screenshot({omitBackground:true,path:path.join(directory,file.replace('.svg','.png'))});receipt.frames.push({file:file.replace('.svg','.png'),sha256:createHash('sha256').update(png).digest('hex')});
 }await writeFile(path.join(directory,'render-receipt.json'),JSON.stringify(receipt,null,2));}finally{await browser.close();}

execFileSync('python3',[fileURLToPath(new URL('./render_custody.py',import.meta.url)),directory],{stdio:'inherit'});
