import test from 'node:test';
import assert from 'node:assert/strict';
import {createMatch,view} from '../shared/sim.js';
import {visibleVillagerAction} from '../shared/visible-action.js';
import {authoredActionStates} from '../client/action-presentation.js';
import {createLocomotionPhase} from '../client/locomotion-phase.js';
test('own and visible enemy action exposes resource only, never target or future intent',()=>{
 const s=createMatch();const u=s.entities.find(e=>e.type==='villager'&&e.owner===1);u.x=10.5;u.y=23.5;u.state='gather';s.map.resources.push({id:999,type:'wood',x:10.5,y:23.5,amount:50});u.order={type:'gather',target:999};
 for(const player of [0,1]){const shown=view(s,player).entities.find(e=>e.id===u.id);assert.deepEqual(shown.visibleAction,{kind:'gather',resource:'wood'});if(player===0){assert.equal(shown.order,undefined);assert.equal(shown.cargo.wood,0);}}
 u.state='walk';u.cargo.wood=5;u.lastMovedTick=s.tick;assert.deepEqual(visibleVillagerAction(s,u),{kind:'carry',load:'wood',moving:true});u.cargo.iron=1;assert.equal(visibleVillagerAction(s,u).load,'mixed');u.cargo.iron=0;u.pendingAttack={target:777,impactTick:999};u.order={type:'gather',target:999,lastX:50,lastY:40};const enemyCarry=view(s,0).entities.find(e=>e.id===u.id);assert.deepEqual(enemyCarry.visibleAction,{kind:'carry',load:'wood',moving:true});assert.equal(enemyCarry.order,undefined);assert.equal(enemyCarry.pendingAttack,undefined);assert.deepEqual(enemyCarry.cargo,{food:0,wood:0,iron:0,units:[]});u.lastMovedTick=s.tick-1;assert.equal(visibleVillagerAction(s,u),null);u.cargo.wood=0;assert.equal(visibleVillagerAction(s,u),null);const marching=view(s,0).entities.find(e=>e.id===u.id);assert.equal(marching.visibleAction,undefined);assert.equal(marching.order,undefined);u.state='gather';u.x=15.5;assert.equal(visibleVillagerAction(s,u),null);assert.equal(view(s,1).entities.find(e=>e.id===u.id).visibleAction,undefined);
});
test('subtype preference retains generic fallback and carried motion uses travelled phase',()=>{
 assert.deepEqual(authoredActionStates({type:'villager',visibleAction:{kind:'gather',resource:'iron'}},'gather'),['gather_iron','gather']);assert.deepEqual(authoredActionStates({type:'villager',visibleAction:{kind:'carry',moving:true}},'walk'),['walk']);assert.deepEqual(authoredActionStates({type:'villager',visibleAction:{kind:'carry',moving:true}},'hit'),['hit']);
 assert.deepEqual(authoredActionStates({type:'villager',visibleAction:{kind:'gather',resource:'wood'}},'death'),['death']);assert.deepEqual(authoredActionStates({type:'villager'},'walk'),['walk']);
 for(const load of ['wood','food','iron','mixed'])assert.deepEqual(authoredActionStates({type:'villager',visibleAction:{kind:'carry',load,moving:true}},'walk'),['walk']);assert.deepEqual(authoredActionStates({type:'villager',visibleAction:{kind:'carry',load:'wood',moving:false}},'carry'),['carry']);
 const p=createLocomotionPhase();p.observe([{id:1,x:0,y:0,state:'walk'}],{tick:0});p.observe([{id:1,x:.63,y:0,state:'walk',visibleAction:{kind:'carry',moving:true}}],{tick:10});assert.equal(p.sample(1,{distancePerCycle:1.26,cycleDurationMs:600}).timeMs,300);
});
