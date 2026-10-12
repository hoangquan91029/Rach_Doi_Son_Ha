import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
import {createMatch,command,step,view} from '../shared/sim.js';
import {UNITS} from '../shared/data.js';
import {visibleUnitAction,beginActionEpisode} from '../shared/visible-action.js';
import {authoredActionStates,episodeAnimationTime} from '../client/action-presentation.js';
const beforePath=resolve('docs/art/pipeline/action-episodes-478/before/shared/sim.js');
const beforeSource=readFileSync(beforePath,'utf8').replaceAll("'./visible-action.js'",JSON.stringify(pathToFileURL(resolve('shared/visible-action.js')).href)).replaceAll("'./data.js'",JSON.stringify(pathToFileURL(resolve('shared/data.js')).href));
const baseline=await import('data:text/javascript;base64,'+Buffer.from(beforeSource).toString('base64'));
const entity=(s,type)=>s.entities.find(e=>e.owner===0&&e.type===type);
const stripped=s=>JSON.parse(JSON.stringify(s,(key,value)=>key==='actionEpisode'?undefined:value));
test('successful ability only, private bounded sanitized ticks, stop cancels',()=>{
 const s=createMatch(),e=entity(s,'king');e.state='idle';assert.equal(command(s,0,{type:'ability',ids:[e.id]}).ok,true);const action=view(s,0).entities.find(u=>u.id===e.id).visibleAction;assert.deepEqual(action,{kind:'ability',startedTick:0,endTick:12,loop:false});assert.equal(view(s,0).entities.find(u=>u.id===e.id).actionEpisode,undefined);
 const episode=structuredClone(e.actionEpisode);assert.equal(command(s,0,{type:'ability',ids:[e.id]}).ok,false);assert.deepEqual(e.actionEpisode,episode);assert.equal(command(s,0,{type:'stop',ids:[e.id]}).ok,true);assert.equal(e.actionEpisode,undefined);
 beginActionEpisode(s,e,'ability');s.tick=12;assert.equal(visibleUnitAction(s,e),null);
});
test('positive wagon flow has continuous episode; empty/full no-op creates no pose',()=>{
 const s=createMatch(),e=entity(s,'wagon'),b=entity(s,'residence');e.x=b.x+2;e.y=b.y;e.cargo.food=0;b.cargo.food=100;
 assert.equal(command(s,0,{type:'load',ids:[e.id],target:b.id}).ok,true);assert.equal(e.actionEpisode,undefined);step(s);assert.equal(e.actionEpisode.kind,'load');const start=e.actionEpisode.startedTick;step(s);assert.equal(e.actionEpisode.startedTick,start);assert.equal(visibleUnitAction(s,e).kind,'load');
 command(s,0,{type:'stop',ids:[e.id]});b.cargo.food=0;e.cargo.food=0;command(s,0,{type:'load',ids:[e.id],target:b.id});step(s);assert.equal(e.actionEpisode,undefined);
 command(s,0,{type:'unload',ids:[e.id],target:b.id});step(s);assert.equal(e.actionEpisode,undefined);
 b.cargo.food=100;e.cargo.food=UNITS.wagon.capacity;s.entities=s.entities.filter(u=>u.id===e.id||u.id===b.id||u.owner!==0);command(s,0,{type:'load',ids:[e.id],target:b.id});step(s);assert.equal(e.actionEpisode,undefined);
});
test('successful transport boarding/unload finite, empty unload no pose',()=>{
 const s=createMatch(),ship=entity(s,'wagon'),u=entity(s,'villager');ship.type='transport';ship.cargo.units=[];ship.x=u.x;ship.y=u.y;
 assert.equal(command(s,0,{type:'load',ids:[ship.id],target:u.id}).ok,true);step(s);assert.equal(u.embarked,ship.id);assert.equal(ship.actionEpisode.kind,'load');assert.equal(ship.actionEpisode.endTick-ship.actionEpisode.startedTick,12);
 command(s,0,{type:'unload',ids:[ship.id],target:ship.id});step(s);assert.equal(u.embarked,null);assert.equal(ship.actionEpisode.kind,'unload');command(s,0,{type:'unload',ids:[ship.id],target:ship.id});step(s);assert.equal(ship.actionEpisode,undefined);
});
test('repair work starts only with positive repair and uses build alias',()=>{
 const s=createMatch(),u=entity(s,'villager'),b=entity(s,'granary');u.x=b.x+2;u.y=b.y;b.hp-=20;
 assert.equal(command(s,0,{type:'repair',ids:[u.id],target:b.id}).ok,true);step(s);assert.equal(u.actionEpisode.kind,'build');const publicUnit=view(s,0).entities.find(e=>e.id===u.id);assert.deepEqual(authoredActionStates(publicUnit,publicUnit.state),['build']);assert.deepEqual(authoredActionStates({type:'king'},'repair'),['build']);
 command(s,0,{type:'stop',ids:[u.id]});s.players[0].resources.wood=0;command(s,0,{type:'repair',ids:[u.id],target:b.id});step(s);assert.equal(u.actionEpisode,undefined);
});
test('hit/death/attack and actual movement preempt; episode time bounded',()=>{
 const s=createMatch(),u=entity(s,'wagon');beginActionEpisode(s,u,'load');u.state='walk';u.lastMovedTick=s.tick;assert.equal(visibleUnitAction(s,u),null);assert.deepEqual(authoredActionStates({...u,visibleAction:{kind:'load'}},'walk'),['walk']);u.state='idle';u.hitUntil=3;assert.equal(visibleUnitAction(s,u),null);u.hitUntil=0;u.state='attack';assert.equal(visibleUnitAction(s,u),null);u.state='idle';u.hp=0;assert.equal(visibleUnitAction(s,u),null);
 assert.equal(episodeAnimationTime({visibleAction:{kind:'load',startedTick:10,endTick:22}},5000),600);assert.deepEqual(authoredActionStates({type:'wagon',visibleAction:{kind:'load'}},'idle'),['load']);
});
test('representative commands and steps equal frozen gameplay after stripping new metadata',()=>{
 for(const scenario of ['ability','load','repair','move']){
  const actual=createMatch(),frozen=baseline.createMatch();for(const s of [actual,frozen]){const w=entity(s,'wagon'),b=entity(s,'residence');w.x=b.x+2;w.y=b.y;w.cargo.food=0;b.cargo.food=100;const u=entity(s,'villager'),g=entity(s,'granary');u.x=g.x+2;u.y=g.y;g.hp-=20;}
  const a=scenario==='ability'?{type:'ability',ids:[entity(actual,'king').id]}:scenario==='load'?{type:'load',ids:[entity(actual,'wagon').id],target:entity(actual,'residence').id}:scenario==='repair'?{type:'repair',ids:[entity(actual,'villager').id],target:entity(actual,'granary').id}:{type:'move',ids:[entity(actual,'wagon').id],x:20,y:20};
  assert.deepEqual(command(actual,0,a),baseline.command(frozen,0,a));for(let i=0;i<18;i++){step(actual);baseline.step(frozen);assert.deepEqual(stripped(actual),frozen,`${scenario} tick${i}`);}
 }
});

test('full transport rejects cosmetic boarding, and new move/attack cancels stale metadata',()=>{
 const s=createMatch(),ship=entity(s,'wagon'),u=entity(s,'villager');ship.type='transport';ship.x=u.x;ship.y=u.y;ship.cargo.units=Array(UNITS.transport.capacity).fill(999);command(s,0,{type:'load',ids:[ship.id],target:u.id});step(s);assert.equal(u.embarked,undefined);assert.equal(ship.actionEpisode,undefined);
 const infantry=entity(s,'infantry');beginActionEpisode(s,infantry,'ability');assert.equal(command(s,0,{type:'move',ids:[infantry.id],x:20,y:20}).ok,true);assert.equal(infantry.actionEpisode,undefined);
 beginActionEpisode(s,infantry,'ability');const enemy=s.entities.find(e=>e.owner===1&&e.type==='infantry');enemy.x=infantry.x+1;enemy.y=infantry.y;assert.equal(command(s,0,{type:'attack',ids:[infantry.id],target:enemy.id}).ok,true);assert.equal(infantry.actionEpisode,undefined);
});
test('construction work aliases build only after authoritative construction progress',()=>{
 const s=createMatch(),u=entity(s,'villager'),b=entity(s,'granary');u.x=b.x+2;u.y=b.y;b.construction={remaining:10,total:10,builder:u.id};u.order={type:'build',target:b.id};step(s);assert.ok(b.construction.remaining<10);assert.equal(u.actionEpisode.kind,'build');assert.equal(visibleUnitAction(s,u).kind,'build');
 command(s,0,{type:'stop',ids:[u.id]});step(s);assert.equal(u.actionEpisode,undefined);
});

test('non-unit train/cancel commands ignore malformed/unowned extra ids and preserve cues',()=>{
 const s=createMatch(),u=entity(s,'king'),b=entity(s,'granary');beginActionEpisode(s,u,'ability');const cue=structuredClone(u.actionEpisode);
 const producer=s.entities.find(e=>e.owner===0&&e.type==='residence');assert.equal(command(s,0,{type:'train',building:producer.id,unit:'villager',ids:123}).ok,true);assert.deepEqual(u.actionEpisode,cue);
 b.construction={remaining:5,total:10,builder:entity(s,'villager').id};assert.equal(command(s,0,{type:'cancel',building:b.id,ids:{malformed:true}}).ok,true);assert.deepEqual(u.actionEpisode,cue);
 assert.equal(command(s,0,{type:'train',building:producer.id,unit:'villager',ids:[u.id,99999]}).ok,true);assert.deepEqual(u.actionEpisode,cue);
 assert.equal(command(s,0,{type:'surrender',ids:123}).ok,true);assert.deepEqual(u.actionEpisode,cue);
});
test('continuous work loops and finite episode maps to actual authored clip duration',()=>{
 const s=createMatch(),u=entity(s,'wagon');beginActionEpisode(s,u,'load',{continuous:true});assert.equal(visibleUnitAction(s,u).loop,true);beginActionEpisode(s,u,'unload');assert.equal(visibleUnitAction(s,u).loop,false);
 assert.equal(episodeAnimationTime({visibleAction:{kind:'load',startedTick:10,endTick:22,loop:false}},800,800),400);assert.equal(episodeAnimationTime({visibleAction:{kind:'load',startedTick:10,endTick:22,loop:true}},800,800),300);
});
