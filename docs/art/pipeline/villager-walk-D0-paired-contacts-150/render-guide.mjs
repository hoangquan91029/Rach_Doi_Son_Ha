import { chromium } from 'playwright';
import fs from 'node:fs';
const dir=new URL('.',import.meta.url).pathname;
const browser=await chromium.launch({headless:true});
try {
 const page=await browser.newPage({viewport:{width:1024,height:512},deviceScaleFactor:1});
 await page.setContent('<html><body style="margin:0">'+fs.readFileSync(dir+'paired-contact-guide.svg','utf8')+'</body></html>');
 await page.screenshot({path:dir+'paired-contact-guide.png'});
} finally { await browser.close(); }
