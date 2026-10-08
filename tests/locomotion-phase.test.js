import test from 'node:test';
import assert from 'node:assert/strict';
import {createLocomotionPhase} from '../client/locomotion-phase.js';
const cycle={distancePerCycle:1.26,cycleDurationMs:600};
const entity=(x,y=0,state='walk')=>({id:1,type:'villager',owner:0,x,y,state});
test('distance rather than elapsed clock drives terrain cadence; pause and stop retain phase',()=>{
 const p=createLocomotionPhase();p.observe([entity(0)],{tick:0});p.observe([entity(.315)],{tick:10});assert.equal(p.sample(1,cycle).timeMs,150);
 p.observe([entity(.315)],{tick:30});assert.equal(p.sample(1,cycle).timeMs,150);
 p.observe([entity(.315)],{tick:30,frozen:true,timeMs:1500});assert.equal(p.sample(1,cycle).timeMs,150);
 p.observe([entity(.315,0,'idle')],{tick:31});assert.equal(p.sample(1,cycle).timeMs,150);
 p.observe([entity(.315,.315)],{tick:51});assert.equal(p.sample(1,cycle).timeMs,300);
 const slow=createLocomotionPhase();slow.observe([entity(0)],{tick:0});slow.observe([entity(.315)],{tick:50});assert.equal(slow.sample(1,cycle).timeMs,150);
});
test('rewind, teleport and removed/reused entities reset without mutating simulation',()=>{
 const p=createLocomotionPhase(),e=entity(0);const before=JSON.stringify(e);p.observe([e],{tick:0});p.observe([entity(.315)],{tick:10});p.observe([entity(.4)],{tick:1});assert.equal(p.sample(1,cycle).distance,0);
 p.observe([entity(20)],{tick:2});assert.equal(p.sample(1,cycle).distance,0);
 p.observe([entity(20.1)],{tick:3});p.observe([],{tick:4});p.observe([entity(20.2)],{tick:5});assert.equal(p.sample(1,cycle).distance,0);assert.equal(JSON.stringify(e),before);
 p.observe([entity(20.3)],{tick:6});p.observe([{...entity(20.4),owner:1}],{tick:7});assert.equal(p.sample(1,cycle).distance,0);
});
