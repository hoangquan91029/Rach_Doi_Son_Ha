import {chromium} from 'playwright';import fs from 'node:fs';
const dir=new URL('.',import.meta.url).pathname,browser=await chromium.launch({headless:true});
try{const page=await browser.newPage({viewport:{width:256,height:256},deviceScaleFactor:1});
for(const name of fs.readdirSync(dir).filter(n=>n.endsWith('.svg'))){
await page.setContent('<html><body style="margin:0;background:transparent">'+fs.readFileSync(dir+name,'utf8')+'</body></html>');
await page.screenshot({path:dir+name.replace('.svg','.png'),omitBackground:true});
}}finally{await browser.close();}
