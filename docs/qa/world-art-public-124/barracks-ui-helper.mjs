import assert from 'node:assert/strict';
// Preparation helper only. A terminal122 actualUI plan and source pins must bind this call.
export async function verifyBarracksUi({page,snapshot,wait,center,point,actions,plan}) {
 assert.equal(plan?.status,'ROOT_ACCEPTED_TERMINAL122_UI_PLAN');
 assert.ok(plan.terminal122Pins); // supplied only after root terminal actual122 intake
 let s=await snapshot();const owner=s.localPlayer;const existing=new Set(s.displayedState.entities.map(e=>e.id));
 const worker=s.displayedState.entities.find(e=>e.owner===owner&&e.type==='villager'&&e.hp>0&&!e.embarked);assert.ok(worker);
 const map=s.displayedState.map,sites=[];for(let y=1;y<map.height-1;y++)for(let x=1;x<map.width-1;x++){const wx=x+.5,wy=y+.5,d=Math.hypot(wx-worker.x,wy-worker.y);if(d<2.2||d>5||!s.displayedState.fog.visible[y*map.width+x]||!['plain','hill'].includes(map.tiles[y*map.width+x])||s.displayedState.entities.some(e=>e.hp>0&&Math.hypot(e.x-wx,e.y-wy)<2)||map.resources.some(e=>e.amount>0&&Math.hypot(e.x-wx,e.y-wy)<1.8))continue;sites.push({x:wx,y:wy,d});}sites.sort((a,b)=>a.d-b.d);assert.ok(sites.length);const site=sites[0];actions.push({test:'visible unoccupied construction site',site});
 await center(worker.x,worker.y);await page.locator('#world').click({position:await page.evaluate(id=>rtsDiagnostics.entityPoint(id),worker.id)});
 await wait(s=>s.selection.includes(worker.id));await page.locator('[data-act="build"][data-value="barracks"]').click();
 await center(site.x,site.y);await page.locator('#world').click({position:await point(site.x,site.y)});
 s=await wait(s=>s.displayedState.entities.some(e=>!existing.has(e.id)&&e.owner===owner&&e.type==='barracks'&&e.construction));
 const b=s.displayedState.entities.find(e=>!existing.has(e.id)&&e.owner===owner&&e.type==='barracks');assert.ok(b.construction);actions.push({test:'actual Barracks construction reserved',entity:b});
 s=await wait(s=>s.displayedState.entities.some(e=>e.id===b.id&&e.hp>0&&!e.construction),plan.completionTimeoutMs||60000);
 const idle=s.displayedState.entities.find(e=>e.id===b.id);assert.ok(!idle.construction);await center(idle.x,idle.y);
 const pick=await page.evaluate(id=>rtsDiagnostics.entityPoint(id),b.id);assert.ok(pick);
 await page.locator('#world').click({position:pick});await wait(s=>s.selection.includes(b.id));actions.push({test:'completed idle Barracks opaque-pixel selection',entity:idle,pick});
 s=await snapshot();const before=new Set(s.displayedState.entities.filter(e=>e.owner===owner&&e.type==='infantry').map(e=>e.id));
 await page.locator('[data-act="train"][data-value="infantry"]').click();s=await wait(s=>s.displayedState.entities.find(e=>e.id===b.id)?.queue?.some(q=>q.unit==='infantry'));actions.push({test:'one Infantry queued by ordinary UI',queue:s.displayedState.entities.find(e=>e.id===b.id).queue});
 s=await wait(s=>s.displayedState.entities.some(e=>e.owner===owner&&e.type==='infantry'&&e.hp>0&&!before.has(e.id)),plan.trainTimeoutMs||60000);
 actions.push({test:'one Infantry spawned',entity:s.displayedState.entities.find(e=>e.owner===owner&&e.type==='infantry'&&e.hp>0&&!before.has(e.id))});
 return {barracksId:b.id,workerId:worker.id};
}
