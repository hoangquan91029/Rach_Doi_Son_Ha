import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {chromium,firefox} from 'playwright';
import {createGameServer} from './stage/server/index.js';
import {launchOwnedBrowser} from '../../../../../scripts/qa/browser-custody510.mjs';
const root=process.cwd(),out=path.join(root,'docs/audits/art-rebuild-538/root/runtime');
const receipt={scope:'PRIVATE_STATIC_ART_DIRECTION_AND_NATIVE_RENDER_INFRASTRUCTURE',runs:[],errors:[],acceptance:{owner:'PENDING',motion:'NOT_STARTED',fullGame:'OPEN',release:'NOT_REQUESTED'}};
const write=()=>fs.writeFileSync(path.join(out,'receipt.json'),JSON.stringify(receipt,null,2)+'\n');
let game;
try{
 game=await createGameServer({port:0,distDir:path.join(out,'build')});
 const origin='http://127.0.0.1:'+game.server.address().port;
 for(const [name,type] of [['chromium',chromium],['firefox',firefox]]){
  let owned,context;
  const run={browser:name,errors:[],failedRequests:[],screenshots:[],checks:[]};receipt.runs.push(run);
  try{
   owned=await launchOwnedBrowser({browserType:type,directory:path.join(out,name+'-custody-2'),launchOptions:{headless:true}});
   run.version=owned.browser.version();context=await owned.newContext({viewport:{width:1366,height:768},deviceScaleFactor:1});const page=await context.newPage();page.setDefaultTimeout(15000);
   page.on('pageerror',e=>run.errors.push(e.message));page.on('requestfailed',q=>run.failedRequests.push({url:q.url(),error:q.failure()}));
   await page.goto(origin+'/client/art-direction-scene.html');await page.locator('body[data-ready=true]').waitFor();
   for(const size of [{width:1366,height:768},{width:1920,height:1080}]){
    await page.setViewportSize(size);
    await page.screenshot({path:path.join(out,`${name}-scene-${size.width}.png`)});run.screenshots.push(`${name}-scene-${size.width}.png`);
    const layout=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,canvas:[document.querySelector('#village').width,document.querySelector('#village').height],smallText:[...document.querySelectorAll('p,button,.kicker,.review-note,.resources span,.map-panel span')].filter(e=>e.getBoundingClientRect().width).filter(e=>parseFloat(getComputedStyle(e).fontSize)<14).map(e=>e.textContent)}));
    assert.equal(layout.scroll,size.width);assert.deepEqual(layout.canvas,[size.width,size.height]);assert.deepEqual(layout.smallText,[]);run.checks.push({viewport:size,layout});
   }
   await page.getByRole('button',{name:'Cận cảnh & hình bóng',exact:true}).click();assert.equal(await page.locator('#studyDialog').evaluate(e=>e.open),true);await page.screenshot({path:path.join(out,name+'-study.png')});await page.getByRole('button',{name:'Đóng cận cảnh'}).click();
   await page.getByRole('button',{name:'½ · Điều quân',exact:true}).click();assert.equal(await page.locator('#zoomLabel').innerText(),'50%');
   await page.getByRole('button',{name:'1:1 · Chơi thật',exact:true}).click();assert.equal(await page.locator('#zoomLabel').innerText(),'100%');
   await page.locator('#move').click();await page.locator('#village').click({position:{x:1050,y:600}});assert.match(await page.locator('#commandStatus').innerText(),/Đã đánh dấu mẫu/);await page.locator('#clearCommand').click();
   await page.locator('#openMenu').click();assert.equal(await page.locator('#menuDialog').evaluate(e=>e.open),true);await page.screenshot({path:path.join(out,name+'-menu.png')});await page.locator('#backToScene').click();
   run.checks.push('static scene, two sizes, readable Vietnamese DOM text, closeup/silhouette, zoom, UI target marker, matching menu');
   // Ordinary game menu path: viewer button was blocked in537.
   await page.goto(origin+'/');await page.locator('#singleStart').waitFor({state:'visible'});
   await page.getByRole('button',{name:'Xem sprite trong game',exact:true}).click();
   const dialog=page.getByRole('dialog',{name:'Xem sprite trong game'});await dialog.locator('#status').filter({hasText:'registry empty'}).waitFor();
   assert.deepEqual(await dialog.locator('#direction option').allTextContents(),['S','SW','W','NW','N','NE','E','SE']);
   await dialog.locator('#pause').click();assert.equal(await dialog.locator('#pause').innerText(),'Resume');await dialog.locator('#pause').click();await dialog.locator('#stop').click();await dialog.locator('#closeViewer').click();await dialog.waitFor({state:'detached'});
   assert.equal(await page.evaluate(()=>document.activeElement.textContent),'Xem sprite trong game');
   assert.equal(await page.getByRole('link',{name:'Duyệt cảnh mỹ thuật'}).getAttribute('href'),'/client/art-direction-scene.html');
   await page.locator('#singleStart').click();await page.locator('[data-map="delta"]').click();await page.locator('#difficulty').selectOption('easy');await page.locator('#launchSingle').click();
   await page.waitForFunction(()=>{const d=window.rtsDiagnostics?.snapshot();return d?.tick>3&&!d.artLoading;},{},{timeout:25000});
   const snap=await page.evaluate(()=>window.rtsDiagnostics.snapshot());assert.equal(snap.camera.zoom,1);assert.equal(snap.art.pipeline.failed,0);run.game={mode:snap.mode,tick:snap.tick,camera:snap.camera,artFailures:snap.art.pipeline.failed,qualification:'EMPTY_NATIVE_BANK_INFRASTRUCTURE_ONLY'};
   await page.locator('#pauseBtn').click();await page.locator('#resume').waitFor();const t=await page.evaluate(()=>window.rtsDiagnostics.snapshot().tick);await page.waitForTimeout(250);assert.equal(await page.evaluate(()=>window.rtsDiagnostics.snapshot().tick),t);await page.locator('#resume').click();await page.waitForFunction(t=>window.rtsDiagnostics.snapshot().tick>t,t);
   await page.locator('#pauseBtn').click();await page.locator('#toMenu').click();await page.locator('#singleStart').waitFor({state:'visible'});
   assert.deepEqual(run.errors,[]);run.checks.push('ordinary game viewer reachable, exact empty bank/controller diagnostic, focus restore, SP Delta startup zoom1, Pause/Resume/menu');run.status='SCOPED_PASS';
  }catch(e){run.status='HOLD';run.firstException=e.stack;receipt.errors.push(name+': '+e.message);process.exitCode=1;}
  finally{if(context)await context.close();if(owned)await owned.close();run.handles={browserConnected:owned?.browser?.isConnected()??false,browserProcessAlive:owned?.server?.process()?.exitCode==null&&!owned?.server?.process()?.signalCode};write();}
 }
}catch(e){receipt.errors.push(e.stack);process.exitCode=1;}
finally{if(game)await game.close();receipt.serverListening=game?.server.listening??false;receipt.rooms=game?.rooms.size??0;receipt.status=receipt.errors.length?'HOLD':'SCOPED_STATIC_SCENE_AND_INFRASTRUCTURE_PASS';receipt.limits=['Scene uses three stills, outside animation registry. No pose duplication/atlas/animation or approved game art.','No eight-direction motion/contact/combat/HP0 visual/performance qualification; existing focused source checks separate.','Headless local Chrome/Firefox only; no production deployment.'];write();console.log(JSON.stringify({status:receipt.status,errors:receipt.errors,handles:receipt.runs.map(r=>r.handles),serverListening:receipt.serverListening}));}
