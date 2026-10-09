import test from 'node:test';
import assert from 'node:assert/strict';
import {createMatch,step,command,view,hashState} from '../shared/sim.js';
import {UNITS,TICK_RATE,BALANCE} from '../shared/data.js';
import {trainingProgress,armyFoodWarning} from '../client/logistics-hud.js';
import {snapshotView} from '../server/index.js';
const advance=(s,ticks)=>{for(let i=0;i<ticks;i++)step(s);};
for(const leaders of [{king:'tran_nhan_tong',general:'tran_hung_dao'},{king:'le_thanh_tong',general:'napoleon_bonaparte'},{king:'le_thanh_tong',general:'le_thanh_tong'}])test(`saved actual duration starts at zero and advances for ${leaders.king}/${leaders.general}`,()=>{
 const s=createMatch({players:[leaders,{}]}),b=s.entities.find(e=>e.owner===0&&e.type==='barracks');assert.equal(command(s,0,{type:'train',building:b.id,unit:'infantry'}).ok,true);
 const q=b.queue[0];assert.equal(q.total,UNITS.infantry.trainTime*s.players[0].modifiers.train);assert.equal(q.remaining,q.total);assert.equal(trainingProgress(q),0);
 const snapshot=view(s,0);assert.equal(trainingProgress(snapshot.entities.find(e=>e.id===b.id).queue[0]),0);const initialTotal=q.total;
 advance(s,Math.floor(q.total*TICK_RATE/2));assert.equal(q.total,initialTotal);assert.ok(trainingProgress(q)>=49&&trainingProgress(q)<=50);
 const frozen=hashState(s),progress=trainingProgress(q);view(s,0);snapshotView(s,0);assert.equal(hashState(s),frozen);assert.equal(trainingProgress(q),progress);
 s.players[0].modifiers.train=1;assert.equal(q.total,initialTotal);while(b.queue.length)step(s);assert.equal(trainingProgress(q),100);
});
test('mobilization advances actual training work twice as fast without changing saved total',()=>{
 const s=createMatch({players:[{king:'le_thanh_tong',general:'napoleon_bonaparte'},{}]}),b=s.entities.find(e=>e.owner===0&&e.type==='barracks'),king=s.entities.find(e=>e.owner===0&&e.type==='king');
 assert.equal(command(s,0,{type:'train',building:b.id,unit:'infantry'}).ok,true);const q=b.queue[0],total=q.total;assert.equal(command(s,0,{type:'ability',ids:[king.id]}).ok,true);advance(s,TICK_RATE);assert.ok(Math.abs(q.remaining-(total-2))<1e-8);assert.equal(q.total,total);assert.ok(trainingProgress(q)>25);
 const compact=snapshotView(s,0),full=view(s,0);assert.deepEqual(compact.entities.find(e=>e.id===b.id).queue,full.entities.find(e=>e.id===b.id).queue);assert.deepEqual(view(s,1).entities.find(e=>e.id===b.id)?.queue||[],[]);
});
test('progress clamps stale legacy data and cannot show100 before work completion',()=>{
 assert.equal(trainingProgress({unit:'infantry',total:6,remaining:0.001}),99);assert.equal(trainingProgress({unit:'infantry',total:6,remaining:7}),0);assert.equal(trainingProgress({unit:'infantry',remaining:9}),0);assert.equal(trainingProgress({unit:'infantry',remaining:4.5}),50);assert.equal(trainingProgress({unit:'infantry',total:6,remaining:0}),100);
});
test('warning derives own finite troop rations, not rich/empty global pools or enemy/support cargo',()=>{
 const s=createMatch(),u=s.entities.find(e=>e.owner===0&&e.type==='infantry');u.food=u.foodMax*(BALANCE.lowSupply-0.01);u.embarked=999;
 for(const e of s.entities)if(e.owner===1||['villager','wagon'].includes(e.type))e.food=0;
 const own=view(s,0),before=hashState(s);assert.equal(armyFoodWarning(own.entities,0),'ARMY LOW ON FOOD · 1 unit needs resupply');assert.ok(own.players[0].resources.food>0);assert.equal(hashState(s),before);
 const text=armyFoodWarning(own.entities,0);for(let i=0;i<100;i++)assert.equal(armyFoodWarning(own.entities,0),text);assert.equal(hashState(s),before);
 u.food=u.foodMax*BALANCE.lowSupply;assert.equal(armyFoodWarning(view(s,0).entities,0),'');s.players[0].resources.food=0;assert.equal(armyFoodWarning(view(s,0).entities,0),'');
 u.food=0;u.hp=0;assert.equal(armyFoodWarning(view(s,0).entities,0),'');
});
test('warning aggregates own naval/leadership rations and clears on finite recovery',()=>{
 const s=createMatch(),units=s.entities.filter(e=>e.owner===0&&e.kind==='unit'&&!['villager','wagon'].includes(e.type));for(const u of units)u.food=0;
 assert.equal(armyFoodWarning(view(s,0).entities,0),`ARMY LOW ON FOOD · ${units.length} units need resupply`);
 for(const u of units)u.food=u.foodMax;assert.equal(armyFoodWarning(view(s,0).entities,0),'');assert.equal(armyFoodWarning([{owner:0,kind:'unit',type:'transport',hp:1,food:0,foodMax:65}],0),'ARMY LOW ON FOOD · 1 unit needs resupply');
});
test('ordinary finite-store resupply clears warning without creating rations',()=>{
 const s=createMatch(),u=s.entities.find(e=>e.owner===0&&e.type==='infantry'),store=s.entities.find(e=>e.owner===0&&e.type==='granary');
 for(const e of s.entities)if(e.owner===0&&e.cargo)e.cargo.food=0;store.cargo.food=20;u.food=0;u.x=store.x+1.5;u.y=store.y;
 assert.match(armyFoodWarning(view(s,0).entities,0),/ARMY LOW ON FOOD/);advance(s,30);assert.equal(armyFoodWarning(view(s,0).entities,0),'');assert.ok(store.cargo.food<20);assert.ok(u.food+store.cargo.food<=20);assert.ok(u.food>u.foodMax*BALANCE.lowSupply);
});
