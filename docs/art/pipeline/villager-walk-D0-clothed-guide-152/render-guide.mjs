import { chromium } from 'playwright'; import fs from 'node:fs';
const dir=new URL('.',import.meta.url).pathname; const browser=await chromium.launch({headless:true});
try{const page=await browser.newPage({viewport:{width:1254,height:1254},deviceScaleFactor:1});await page.setContent('<html><body style="margin:0;background:transparent">'+fs.readFileSync(dir+'clothed-F04-guide.svg','utf8')+'</body></html>');await page.screenshot({path:dir+'clothed-F04-guide.png',omitBackground:true});}finally{await browser.close();}
