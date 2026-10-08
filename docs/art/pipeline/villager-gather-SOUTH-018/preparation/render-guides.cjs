const {chromium}=require('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha/node_modules/playwright');
const fs=require('fs');const path=require('path');
(async()=>{const browser=await chromium.launch({headless:true});const page=await browser.newPage({viewport:{width:1254,height:1254},deviceScaleFactor:1});for(let i=0;i<8;i++){const name=`guide-F${String(i).padStart(2,'0')}`;await page.setContent(fs.readFileSync(path.join(__dirname,name+'.svg'),'utf8'));await page.locator('svg').screenshot({path:path.join(__dirname,name+'.png')});}await browser.close();})();
