import test from 'node:test';
import assert from 'node:assert/strict';
import {interpolateOfflineView} from '../client/presentation.js';
import {createLocomotionPhase} from '../client/locomotion-phase.js';

const state=(tick,x,extra={})=>({tick,winner:null,map:{id:'delta'},entities:[{id:1,owner:0,type:'infantry',x,y:2,hp:100,state:'walk',...extra}]});
test('local sub-tick positions move smoothly without changing authoritative state or total distance',()=>{
 const phase=createLocomotionPhase(),current=state(1,.115),previous=state(0,0),pin=JSON.stringify(current);
 for(const acc of [0,.01,.02,.03,.04,.05]){
  const shown=interpolateOfflineView(current,previous,acc);
  assert.ok(Math.abs(shown.entities[0].x-.115*acc/.05)<1e-12);
  phase.observe(shown.entities,{tick:1,timeMs:acc*1000});
 }
 assert.ok(Math.abs(phase.sample(1,{distancePerCycle:1,cycleDurationMs:720}).distance-.115)<1e-12);
 assert.equal(JSON.stringify(current),pin);assert.equal(previous.entities[0].x,0);
});
test('catch-up uses last completed tick pair and never extrapolates beyond current position',()=>{
 const current=state(5,.575),previous=state(4,.46);
 assert.equal(interpolateOfflineView(current,previous,.025).entities[0].x,.5175);
 assert.equal(interpolateOfflineView(current,previous,.2),current);
 assert.equal(interpolateOfflineView(current,state(2,.23),.01),current);
 assert.equal(interpolateOfflineView(current,{...previous,map:{id:'coast'}},.01),current);
});
test('pause holds last displayed position, resume returns to the same sub-tick point',()=>{
 const current=state(1,.115),previous=state(0,0);
 const last=interpolateOfflineView(current,previous,.02);
 const held=interpolateOfflineView(current,previous,.04,{frozen:true,frozenView:last});
 assert.equal(held.entities[0].x,last.entities[0].x);
 assert.equal(interpolateOfflineView(current,previous,.02).entities[0].x,last.entities[0].x);
 assert.equal(interpolateOfflineView(current,previous,.02,{frozen:true}),current);
});
test('current fog membership, action, hit/death, embarkation and victory stay authoritative',()=>{
 const prior=state(0,0);prior.entities.push({id:2,x:1,y:1,hp:100});
 const current=state(1,.115,{state:'attack',order:{type:'attack',target:3},hitUntil:8});
 const shown=interpolateOfflineView(current,prior,.025);
 assert.deepEqual(shown.entities.map(e=>e.id),[1]);assert.equal(shown.entities[0].state,'attack');
 assert.equal(shown.entities[0].order,current.entities[0].order);assert.equal(shown.entities[0].hitUntil,8);
 assert.equal(shown.entities[0].x,.115);
 const stopped=state(1,.115,{state:'idle',order:null});
 assert.equal(interpolateOfflineView(stopped,prior,.01).entities[0],stopped.entities[0]);
 for(const extra of [{hp:0,state:'death'},{embarked:5}]){
  const dead=state(1,.115,extra);assert.equal(interpolateOfflineView(dead,prior,.01).entities[0],dead.entities[0]);
 }
 const won={...current,winner:0};assert.equal(interpolateOfflineView(won,prior,.01,{frozen:true,frozenView:prior}),won);
});
