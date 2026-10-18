import fs from 'node:fs';
import {chromium} from 'playwright';
import {launchOwnedBrowser} from '../../../scripts/qa/browser-custody510.mjs';
const directory=new URL('./fixture/',import.meta.url).pathname;
const owned=await launchOwnedBrowser({browserType:chromium,directory,launchOptions:{headless:true}});
try {const context=await owned.newContext();const page=await context.newPage();await page.goto('about:blank');owned.custody.event('fixture-blank-page');}finally {await owned.close();}
fs.writeFileSync(new URL('./fixture-result.json',import.meta.url),JSON.stringify({browserConnected:owned.browser.isConnected(),pid:owned.server.process().pid,exitCode:owned.server.process().exitCode,signalCode:owned.server.process().signalCode,status:owned.custody.status},null,2)+'\n');
