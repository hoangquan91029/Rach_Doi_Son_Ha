import { chromium } from 'playwright';
import fs from 'node:fs';
const dir=new URL('.',import.meta.url).pathname;
const browser=await chromium.launch({headless:true});
try {
  const page=await browser.newPage({viewport:{width:256,height:256},deviceScaleFactor:1});
  for(const frame of ['MODEL',...Array.from({length:8},(_,i)=>'F'+String(i).padStart(2,'0'))]) {
    await page.setContent('<html><body style="margin:0;background:transparent">'+fs.readFileSync(dir+frame+'-rough.svg','utf8')+'</body></html>');
    await page.screenshot({path:dir+frame+'-rough.png',omitBackground:true});
  }
} finally {await browser.close();}
