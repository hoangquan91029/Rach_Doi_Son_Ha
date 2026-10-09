import assert from 'node:assert/strict';
// Preparation helper only. A terminal122 actualUI plan and source pins must bind this call.
export async function verifyBarracksUi({page,snapshot,wait,center,point,actions,plan}) {
 assert.equal(plan?.status,'ROOT_ACCEPTED_TERMINAL122_UI_PLAN');
 assert.ok(Number.isFinite(plan.buildTarget?.x)&&Number.isFinite(plan.buildTarget?.y));
 assert.ok(Number.isFinite(plan.idleOpaquePickOffset?.x)&&Number.isFinite(plan.idleOpaquePickOffset?.y));
 let s=await snapshot();const owner=s.localPlayer;const existing=new Set(s.displayedState.entities.map(e=>e.id));
 const worker=s.displayedState.entities.find(e=>e.owner===owner&&e.type==='villager'&&e.hp>0&&!e.embarked);assert.ok(worker);
 await center(worker.x,worker.y);await page.locator('#world').click({position:await page.evaluate(id=>rtsDiagnostics.entityPoint(id),worker.id)});
 await wait(s=>s.selection.includes(worker.id));await page.locator('[data-act="build"][data-value="barracks"]').click();
 await center(plan.buildTarget.x,plan.buildTarget.y);await page.locator('#world').click({position:await point(plan.buildTarget.x,plan.buildTarget.y)});
 s=await wait(s=>s.displayedState.entities.some(e=>!existing.has(e.id)&&e.owner===owner&&e.type==='barracks'&&e.construction));
 const b=s.displayedState.entities.find(e=>!existing.has(e.id)&&e.owner===owner&&e.type==='barracks');assert.ok(b.construction);actions.push({test:'actual Barracks construction reserved',entity:b});
 s=await wait(s=>s.displayedState.entities.some(e=>e.id===b.id&&e.hp>0&&!e.construction),plan.completionTimeoutMs||60000);
 const idle=s.displayedState.entities.find(e=>e.id===b.id);assert.ok(!idle.construction);await center(idle.x,idle.y);
 const anchor=await point(idle.x,idle.y);const pick={x:anchor.x+plan.idleOpaquePickOffset.x*s.camera.zoom,y:anchor.y+plan.idleOpaquePickOffset.y*s.camera.zoom};
 await page.locator('#world').click({position:pick});await wait(s=>s.selection.includes(b.id));actions.push({test:'completed idle Barracks opaque-pixel selection',entity:idle,pick});
 s=await snapshot();const before=new Set(s.displayedState.entities.filter(e=>e.owner===owner&&e.type==='infantry').map(e=>e.id));
 await page.locator('[data-act="train"][data-value="infantry"]').click();s=await wait(s=>s.displayedState.entities.find(e=>e.id===b.id)?.queue?.some(q=>q.unit==='infantry'));actions.push({test:'one Infantry queued by ordinary UI',queue:s.displayedState.entities.find(e=>e.id===b.id).queue});
 s=await wait(s=>s.displayedState.entities.some(e=>e.owner===owner&&e.type==='infantry'&&e.hp>0&&!before.has(e.id)),plan.trainTimeoutMs||60000);
 actions.push({test:'one Infantry spawned',entity:s.displayedState.entities.find(e=>e.owner===owner&&e.type==='infantry'&&e.hp>0&&!before.has(e.id))});
 return {barracksId:b.id,workerId:worker.id};
}
