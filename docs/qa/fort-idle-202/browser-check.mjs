import {chromium} from 'playwright';
import {createGameServer} from '/tmp/rds-fort202/server/index.js';
import {writeFile,mkdir} from 'node:fs/promises';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
const out=new URL('./scene/',import.meta.url);await mkdir(out,{recursive:true});
const game=await createGameServer({port:0,distDir:'/tmp/rds-fort202/candidate-dist'}),browser=await chromium.launch({headless:true}),context=await browser.newContext({viewport:{width:1280,height:800},deviceScaleFactor:1}),p=await context.newPage();
const r={status:'RUNNING',method:'Ordinary UI mouse/keyboard only; diagnostics read-only; no command/state/facing/speed injection',errors:[],failures:[]};let bid,tid;const start=Date.now();
p.on('pageerror',e=>r.errors.push(e.message));p.on('requestfailed',q=>r.failures.push(q.url()));p.on('response',async q=>{if(/\/assets\/index-.*\.js$/.test(q.url()))r.bundleSHA=createHash('sha256').update(await q.body()).digest('hex');});
const snap=()=>p.evaluate(()=>rtsDiagnostics.snapshot());const wait=async(fn,ms=30000)=>{const t=Date.now();assert.ok(t-start<180000,'finite180s trial');while(Date.now()-t<ms){const s=await snap();if(fn(s))return s;await p.waitForTimeout(100);}throw Error('ActualUI condition timeout');};
const entity=(s,id)=>s.displayedState.entities.find(e=>e.id===id);
const center=async(x,y)=>{const s=await snap(),box=await p.locator('#minimap').boundingBox();await p.locator('#minimap').click({position:{x:x/s.displayedState.map.width*box.width,y:y/s.displayedState.map.height*box.height}});await p.waitForTimeout(100);};
const clickPoint=async(x,y,button='left')=>{const pt=await p.evaluate(([x,y])=>rtsDiagnostics.point(x,y),[x,y]);await p.locator('#world').click({position:pt,button});};
const select=async id=>{const s=await snap(),e=entity(s,id);assert.ok(e&&e.owner===0&&e.hp>0&&!e.embarked);await center(e.x,e.y);const pt=await p.evaluate(id=>rtsDiagnostics.entityPoint(id),id);await p.locator('#world').click({position:pt});await wait(s=>s.selection.length===1&&s.selection[0]===id);return pt;};
const shot=async name=>p.screenshot({path:new URL(name+'.png',out).pathname});
try{
 await p.goto(`http://127.0.0.1:${game.server.address().port}/?art=fort`);await p.locator('#singleStart').waitFor();r.boot=await snap();assert.equal(r.boot.bootUi.ready,12);assert.equal(r.boot.art.pipeline.failed,0);
 await p.locator('#singleStart').click();await p.locator('[data-map=delta]').click();await p.locator('#difficulty').selectOption('easy');await p.locator('#launchSingle').click();let s=await wait(s=>s.tick>2);assert.equal(s.camera.zoom,1.08);r.map=s.displayedState.map.id;
 const worker=s.displayedState.entities.filter(e=>e.owner===0&&e.type==='villager'&&e.hp>0).sort((a,b)=>b.y-a.y)[0];r.workerId=worker.id;await select(worker.id);
 const map=s.displayedState.map,sites=[];
 for(let y=1;y<map.height-1;y++)for(let x=1;x<map.width-1;x++){
 const wx=x+.5,wy=y+.5,d=Math.hypot(wx-worker.x,wy-worker.y);
 if(d>6||!s.displayedState.fog.visible[y*map.width+x]||!['plain','hill'].includes(map.tiles[y*map.width+x]))continue;
 if(s.displayedState.entities.some(e=>e.hp>0&&Math.abs(e.x-wx)<2&&Math.abs(e.y-wy)<2)||map.resources.some(e=>e.amount>0&&Math.hypot(e.x-wx,e.y-wy)<1.5))continue;
 sites.push({x:wx,y:wy,d,tile:map.tiles[y*map.width+x],visible:true});}
 sites.sort((a,b)=>a.d-b.d);assert.ok(sites.length,'actualvisiblelegalcandidate');r.site=sites[0];r.preflightResources=s.displayedState.players[0].resources;
 await select(worker.id);await p.locator('[data-act=build][data-value=fort]').click();await center(r.site.x,r.site.y);r.placementClick={x:Math.floor(r.site.x),y:Math.floor(r.site.y),reason:'UI rounds before simulation floor+half; integer click targets planned actualcenter'};await clickPoint(r.placementClick.x,r.placementClick.y);r.construction=await wait(s=>s.displayedState.entities.some(e=>e.owner===0&&e.type==='fort'&&e.construction));bid=r.construction.displayedState.entities.find(e=>e.owner===0&&e.type==='fort').id;await shot('actual-construction');r.idle=await wait(s=>entity(s,bid)&&!entity(s,bid).construction&&entity(s,bid).hp>0&&entity(s,bid).state==='idle',45000);await shot('actual-idle');
 r.selectionPoint=await select(bid);await p.waitForFunction(()=>document.querySelector('#selectionPanel').textContent.includes('Fort'));r.selected=await snap();r.selectionHUD=await p.locator('#selectionPanel').innerText();assert.match(r.selectionHUD,/Fort/);await shot('actual-selected-fort');
 await p.locator('#pauseBtn').click();r.paused=await snap();await p.waitForTimeout(200);assert.equal((await snap()).tick,r.paused.tick);await shot('actual-paused');await p.locator('#resume').click();r.resumed=await wait(s=>s.tick>r.paused.tick);await select(worker.id);await p.locator('[data-act=stop]').click();r.stopped=await wait(s=>entity(s,r.workerId)?.state==='idle'&&!entity(s,r.workerId)?.order);await shot('actual-stopped');assert.equal(r.stopped.art.pipeline.failed,0);assert.deepEqual(r.errors,[]);assert.deepEqual(r.failures,[]);
 await p.locator('#pauseBtn').click();await p.locator('#toMenu').click();await p.locator('#singleStart').waitFor();r.menuReturned=true;r.status='PASS_NARROW_DELTA_UI_FORT_BUILD_IDLE_SELECT_PAUSE_RESUME_STOP_MENU';
}catch(error){r.status='HOLD';r.error=error.stack;r.failureSnapshot=await snap().catch(()=>null);await shot('failure').catch(()=>{});process.exitCode=1;}
finally{await context.close();await browser.close();await game.close();r.cleanup={rooms:game.rooms.size,listening:game.server.listening,browserClosed:true};r.fortId=bid;r.transportId=tid;r.actualSceneVisualAccepted=false;const compact=s=>s?.displayedState?{tick:s.tick,mode:s.mode,paused:s.paused,localPlayer:s.localPlayer,selection:s.selection,camera:s.camera,art:s.art,bootUi:s.bootUi,resources:s.displayedState.players?.[0]?.resources,entities:s.displayedState.entities.filter(e=>[bid,tid,r.workerId,...(s.selection||[])].includes(e.id))}:s;for(const k of Object.keys(r))r[k]=compact(r[k]);await writeFile(new URL('receipt.json',out),JSON.stringify(r,null,2));console.log(JSON.stringify({status:r.status,error:r.error,cleanup:r.cleanup}));}
