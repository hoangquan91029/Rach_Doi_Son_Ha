import { chromium } from 'playwright';import fs from 'node:fs';
const dir=new URL('.',import.meta.url).pathname;const browser=await chromium.launch({headless:true});
try{const page=await browser.newPage({viewport:{width:1254,height:1254},deviceScaleFactor:1});for(const key of ['F01','F03','F05','F07']){await page.setContent('<html><body style="margin:0;background:transparent">'+fs.readFileSync(dir+key+'-clothed-guide.svg','utf8')+'</body></html>');await page.screenshot({path:dir+key+'-clothed-guide.png',omitBackground:true});}}finally{await browser.close();}
