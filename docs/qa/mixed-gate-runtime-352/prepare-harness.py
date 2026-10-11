from pathlib import Path
out=Path(__file__).resolve().parent
s=Path('docs/qa/gate-y-runtime-255A/browser.mjs').read_text()
s=s.replace("import {chromium} from 'playwright';", "import {chromium} from '/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha/node_modules/playwright/index.mjs';import {readFile} from 'node:fs/promises';")
s=s.replace('/tmp/rds-gate255-stage/client/','/tmp/rds-mixed-gate352-stage/client/').replace('/tmp/rds-gate255-stage/server/index.js','/home/kieu-hoang-quan/.local/share/rach-doi-son-ha/releases/230/runtime230/server/index.js').replace('/tmp/rds-gate255-build','/tmp/rds-mixed-gate352-build')
s=s.replace('const game=await',"const authorization=JSON.parse(await readFile(new URL('./root-go.json',import.meta.url),'utf8'));assert.equal(authorization.order,352);assert.equal(authorization.status,'SEALED_SELECTED351_ROOT_GO');\nconst game=await",1)
s=s.replace('One255A wholeGateY ordinaryDelta trial','One352 whole mixedGate mask5 ordinaryDelta trial').replace('fresh255 isolated42manifest','sealed352 isolated55manifest').replace('Date.now()+240000','Date.now()+240000')
a=s.index(' const candidates=[];'); b=s.index(' candidates.sort',a)
s=s[:a]+''' const candidates=[];const width=s.displayedState.map.width,height=s.displayedState.map.height;for(let y=3;y<height-4;y++)for(let x=4;x<width-5;x++){
 const cells=[{x:x+.5,y:y+.5},{x:x+1.5,y:y+.5},{x:x+.5,y:y+1.5}],staging={x:x-.5,y:y-1.5},corridor=[];
 for(let dy=-2;dy<=2;dy++)for(let dx=-3;dx<=2;dx++)corridor.push({x:x+.5+dx,y:y+.5+dy});
 if(Math.hypot(staging.x-worker.x,staging.y-worker.y)>7)continue;
 if([...cells,staging,...corridor].some(q=>!s.displayedState.fog.visible[Math.floor(q.y)*width+Math.floor(q.x)]||s.displayedState.map.tiles[Math.floor(q.y)*width+Math.floor(q.x)]!=='plain'||s.displayedState.entities.some(e=>e.hp>0&&e.id!==worker.id&&Math.abs(e.x-q.x)<1.9&&Math.abs(e.y-q.y)<1.9)||s.displayedState.map.resources.some(e=>e.amount>0&&Math.hypot(e.x-q.x,e.y-q.y)<1.7)))continue;
 candidates.push({x:x+.5,y:y+.5,staging,d:Math.hypot(staging.x-worker.x,staging.y-worker.y)});}
''' +s[b:]
s=s.replace("[['wall',0,-1],['gate',0,0],['wall',0,1]]","[['gate',0,0],['wall',1,0],['wall',0,1]]")
a=s.index(' assert.equal(r.structures[1].y');b=s.index("await click(p.locator('#pauseBtn'));",a)
s=s[:a]+''' s=await snap();r.topology=r.structures.map(b=>({id:b.id,...buildFortificationTopology(s.displayedState.entities).get(b.id)}));assert.deepEqual(r.topology.map(t=>t.mask),[5,2,8]);assert.equal(r.topology[0].axis,'X');r.threeStructuresCompleted=true;await save();assert.equal(s.camera.zoom,1.08);
 r.builderAwayOrder=await move(line.x-2.5,line.y-2.5);await wait(s=>{const e=entity(s,worker.id);return e?.hp>0&&e.state==='idle'&&e.order===null&&Math.hypot(e.x-r.builderAwayOrder.x,e.y-r.builderAwayOrder.y)<=.7+1e-6;});await center(line.x,line.y);await p.screenshot({path:new URL('actual-mixed-gate-default.png',out).pathname});r.opaqueSelections=[];for(const b of r.structures){await select(b.id);r.opaqueSelections.push({id:b.id,selection:(await snap()).selection});}assert.equal((await snap()).art.pipeline.ready,55);assert.equal((await snap()).art.pipeline.failed,0);await select(r.structures[0].id);r.gateSelection=(await snap()).selection;await save();''' +s[b:]
a=s.index('r.beforeCrossingOrder=');b=s.index('await select(worker.id);await click',a)
s=s[:a]+'''r.beforeCrossingOrder=await move(line.x-.25,line.y-2.5);s=await wait(s=>{const e=entity(s,worker.id);return e?.hp>0&&e.state==='idle'&&e.order===null&&Math.hypot(e.x-r.beforeCrossingOrder.x,e.y-r.beforeCrossingOrder.y)<=.7+1e-6&&e.y<line.y-.7;});r.beforeCrossing={tick:s.tick,worker:entity(s,worker.id)};
 const sampledArrival=async(order,phase)=>{const s=await wait(s=>{const e=entity(s,worker.id);assert.ok(e&&e.owner===0&&e.hp>0&&!e.embarked);assert.equal(s.displayedState.winner,null);r.movement.push({phase,tick:s.tick,x:e.x,y:e.y,dir:e.dir,state:e.state,order:e.order});return e.state==='idle'&&e.order===null&&Math.hypot(e.x-order.x,e.y-order.y)<=.7+1e-6;});await save();return s;};
 r.apertureOrder=await move(line.x-.25,line.y+.30);await sampledArrival(r.apertureOrder,'north_aperture');
 assert.ok(r.movement.some(e=>e.phase==='north_aperture'&&Math.abs(e.x-line.x)<.4&&Math.abs(e.y-line.y)<.45),'actual movement must enter gate footprint, not pass beside it');
 r.negativeXExitOrder=await move(line.x-2.5,line.y+.30);s=await sampledArrival(r.negativeXExitOrder,'negativeX_exit');assert.ok(entity(s,worker.id).x<line.x-1.5);assert.ok(r.movement.some(e=>e.phase==='negativeX_exit'&&Math.abs(e.x-line.x)<.5&&Math.abs(e.y-line.y)<.5),'exit must start through actual gate footprint');
 r.clearCorridorOrder=await move(line.x-2.5,line.y+2.5);await sampledArrival(r.clearCorridorOrder,'clear_negativeX_corridor');r.ownGateTravelPassed=true;await save();await p.screenshot({path:new URL('actual-through-own-mixed-gate.png',out).pathname});''' +s[b:]
s=s.replace('PASS_WHOLE_GATE_Y_LINE_SELECT_PAUSE_RESUME_FRIENDLY_TRANSIT_STOP_MENU','PASS352_MASK5_THREE_PICKS_OBSERVED_FOOTPRINT_NEGATIVEX_EXIT_PAUSE_RESUME_STOP_MENU')
s=s.replace("errors:[],structures:[]", "errors:[],networkErrors:[],httpErrors:[],structures:[]")
s=s.replace("p.on('pageerror',e=>r.errors.push(e.message));", "p.on('pageerror',e=>r.errors.push(e.message));p.on('requestfailed',q=>r.networkErrors.push({url:q.url(),error:q.failure()}));p.on('response',q=>{if(q.status()>=400)r.httpErrors.push({url:q.url(),status:q.status()});});")
s=s.replace("assert.deepEqual(r.errors,[]);", "assert.deepEqual(r.errors,[]);assert.deepEqual(r.networkErrors,[]);assert.deepEqual(r.httpErrors,[]);")
(out/'browser.mjs').write_text(s)
