import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {pathToFileURL} from 'node:url';
import {chromium} from 'playwright';

const root=process.cwd(),out=path.join(root,'docs/audits/pixel-rebuild-537/root/runtime');
const stage=path.join(out,'stage'),build=path.join(out,'build');
const sha=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const write=(name,value)=>fs.writeFileSync(path.join(out,name),JSON.stringify(value,null,2)+'\n');
assert.ok(!fs.existsSync(path.join(out,'attempt.json')),'One scene only');
const pins=JSON.parse(fs.readFileSync(path.join(out,'frozen-before.json')));
function guard(){for(const [name,digest] of Object.entries(pins))assert.equal(sha(path.join(root,name)),digest,'Frozen input changed: '+name);}
const {createGameServer}=await import(pathToFileURL(path.join(stage,'server/index.js')));
const {launchOwnedBrowser}=await import(pathToFileURL(path.join(root,'scripts/qa/browser-custody510.mjs')));
const receipt={scope:'PRIVATE_EMPTY_BANK_INFRASTRUCTURE_ONLY',status:'RUNNING',errors:[],consoleErrors:[],failedRequests:[],requests:[],checks:[],cleanup:[]};
let game,owned,context,page;
const snapshot=()=>page.evaluate(()=>window.rtsDiagnostics.snapshot());
try{
 guard();write('attempt.json',{pid:process.pid,startedUTC:new Date().toISOString()});
 game=await createGameServer({port:0,distDir:build});
 owned=await launchOwnedBrowser({browserType:chromium,directory:path.join(out,'browser-custody'),launchOptions:{headless:true}});
 write('live-handles.json',{port:game.server.address().port,browserPID:owned.server.process().pid});
 context=await owned.newContext({viewport:{width:1920,height:1080},deviceScaleFactor:1});
 page=await context.newPage();page.setDefaultTimeout(15000);
 page.on('pageerror',e=>receipt.errors.push(e.message));
 page.on('console',m=>{if(m.type()==='error')receipt.consoleErrors.push(m.text());});
 page.on('request',q=>receipt.requests.push(new URL(q.url()).pathname));
 page.on('requestfailed',q=>receipt.failedRequests.push({url:q.url(),error:q.failure()}));
 await page.goto('http://127.0.0.1:'+game.server.address().port);
 await page.locator('#singleStart').waitFor({state:'visible'});
 await page.getByRole('button',{name:'Sprite viewer · pixel art pending',exact:true}).click();
 const viewer=page.locator('dialog');
 await viewer.locator('#status').filter({hasText:'registry empty'}).waitFor();
 const directions=await viewer.locator('#direction option').allTextContents();
 assert.deepEqual(directions,['S','SW','W','NW','N','NE','E','SE']);
 assert.equal(await viewer.locator('#identity').isDisabled(),true);
 assert.equal(await viewer.locator('#action').isDisabled(),true);
 for(let row=0;row<8;row++)await viewer.locator('#direction').selectOption(String((row+1)%8));
 await viewer.locator('#pause').click();assert.equal(await viewer.locator('#pause').innerText(),'Resume');
 await viewer.locator('#pause').click();assert.equal(await viewer.locator('#pause').innerText(),'Pause');
 await viewer.locator('#stop').click();
 await page.screenshot({path:path.join(out,'empty-viewer.png')});
 receipt.viewer={directions,status:await viewer.locator('#status').innerText(),detail:await viewer.locator('#detail').innerText(),gifs:await viewer.locator('#gifs').innerText(),qualification:'MISSING'};
 assert.match(receipt.viewer.status,/MISSING/);
 await viewer.locator('#closeViewer').click();await viewer.waitFor({state:'detached'});
 await page.locator('#singleStart').click();await page.locator('[data-map="delta"]').click();
 await page.locator('#difficulty').selectOption('easy');await page.locator('#launchSingle').click();
 await page.waitForFunction(()=>{const d=window.rtsDiagnostics?.snapshot();return d?.tick>3&&!d.artLoading;},{},{timeout:20000});
 receipt.startup=await snapshot();write('startup-snapshot.json',receipt.startup);
 assert.equal(receipt.startup.mode,'offline');assert.equal(receipt.startup.art.pipeline.failed,0);
 assert.equal(receipt.startup.displayedState.map.id,'delta');
 await page.locator('#pauseBtn').click();await page.locator('#resume').waitFor();
 const a=await snapshot();await page.waitForTimeout(300);const b=await snapshot();
 assert.equal(a.tick,b.tick);assert.equal(a.presentation.timeMs,b.presentation.timeMs);
 await page.screenshot({path:path.join(out,'empty-bank-game.png')});
 receipt.pause={tick:a.tick,timeMs:a.presentation.timeMs,heldTick:b.tick,heldTimeMs:b.presentation.timeMs};
 await page.locator('#resume').click();
 await page.waitForFunction(t=>window.rtsDiagnostics.snapshot().tick>t,a.tick,{timeout:5000});
 await page.locator('#pauseBtn').click();await page.locator('#toMenu').click();
 await page.locator('#singleStart').waitFor({state:'visible'});
 receipt.checks.push('ordinary viewer controls, eight direction options, explicit missing state, SP Delta startup, Pause/Resume/menu');
 // Compare actual requests to detached legacy-only URLs; shared world atlases remain permitted.
 const manifests=JSON.parse(fs.readFileSync(path.join(root,'docs/audits/pixel-rebuild-535/integration/legacy-inventory.json')));
 const forbidden=new Set(),retained=new Set();
 for(const entry of manifests){
  const url='http://local/'+entry.manifest.replace(/^public\//,'');
  for(const a of entry.detachedCharacterEntries)if(a.runtime?.path)forbidden.add(new URL(a.runtime.path,url).pathname);
  const original=JSON.parse(fs.readFileSync(path.join(root,entry.manifest)));
  for(const a of original.assets)if(!['unit','portrait'].includes(a.kind)&&a.runtime?.path)retained.add(new URL(a.runtime.path,url).pathname);
 }
 receipt.legacyOnlyRequests=[...new Set(receipt.requests.filter(p=>(forbidden.has(p)&&!retained.has(p))||p.startsWith('/assets/leadership/')))];
 assert.deepEqual(receipt.legacyOnlyRequests,[]);assert.deepEqual(receipt.errors,[]);
 assert.deepEqual(receipt.failedRequests,[]);assert.deepEqual(receipt.consoleErrors,[]);
 receipt.status='SCOPED_EMPTY_BANK_STARTUP_VIEWER_PAUSE_MENU_OBSERVED';
}catch(error){receipt.status='HOLD_FIRST_ERROR';receipt.firstException=error.stack;process.exitCode=1;}
finally{
 if(context)try{await context.close();receipt.cleanup.push('context closed');}catch(e){receipt.cleanup.push({contextError:e.message});process.exitCode=1;}
 try{await owned?.close();receipt.cleanup.push('owned browser closed');}catch(e){receipt.cleanup.push({browserError:e.message});process.exitCode=1;}
 try{await game?.close();receipt.cleanup.push('owned server closed');}catch(e){receipt.cleanup.push({serverError:e.message});process.exitCode=1;}
 const p=owned?.server?.process();receipt.handles={browserPID:p?.pid??null,browserConnected:owned?.browser?.isConnected()??false,browserProcessAlive:!!p&&p.exitCode==null&&!p.signalCode,serverListening:game?.server.listening??false,rooms:game?.rooms.size??0};
 try{guard();receipt.preservation=true;}catch(e){receipt.preservation=false;receipt.guardError=e.message;process.exitCode=1;}
 if(receipt.handles.browserConnected||receipt.handles.browserProcessAlive||receipt.handles.serverListening||receipt.handles.rooms){receipt.status='HOLD_UNRESOLVED_HANDLE';process.exitCode=1;}
 receipt.artAcceptance={structural:'NO_ART',visual:'UNKNOWN',motion:'UNKNOWN',runtime:'UNKNOWN',owner:'UNKNOWN',release:'UNKNOWN'};
 receipt.limitations=['Empty registry only; no actual pixel clip or motion tested.','Headless Chromium private localhost; no Firefox/public/WAN acceptance.'];
 delete receipt.startup;write('receipt.json',receipt);write('live-handles.json',receipt.handles);
 console.log(JSON.stringify({status:receipt.status,error:receipt.firstException,handles:receipt.handles,preservation:receipt.preservation}));
}
