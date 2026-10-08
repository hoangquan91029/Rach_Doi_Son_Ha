import test from 'node:test';
import assert from 'node:assert/strict';
import {sampleSpriteAnimation} from '../client/sprite-timing.js';
import {createMatch,step,command,view} from '../shared/sim.js';
import {gatherAnimationTime,createPresentationClock} from '../client/action-presentation.js';
test('actual gather episode continues, target change or interrupted work starts a new episode without leaking target',()=>{
 const s=createMatch();s.map.tiles.fill('plain');const u=s.entities.find(e=>e.owner===0&&e.type==='villager');u.x=10.5;u.y=23.5;const r={id:999,type:'wood',x:10.5,y:23.5,amount:100},r2={...r,id:998};s.map.resources.push(r,r2);command(s,0,{type:'gather',ids:[u.id],target:r.id});step(s);const first=u.gatherEpisode.startedTick,amount=u.cargo.wood;step(s);assert.equal(u.gatherEpisode.startedTick,first);assert.ok(Math.abs(u.cargo.wood-2*amount)<1e-9);
 const own=view(s,0).entities.find(e=>e.id===u.id);assert.equal(own.visibleAction.startedTick,first);assert.equal(own.gatherEpisode,undefined);
 const enemy=s.entities.find(e=>e.owner===1&&e.type==='villager');enemy.x=u.x;enemy.y=u.y;enemy.state='gather';enemy.order={type:'gather',target:r.id};enemy.gatherEpisode={target:r.id,startedTick:first,lastTick:s.tick};const shown=view(s,0).entities.find(e=>e.id===enemy.id);assert.deepEqual(shown.visibleAction,{kind:'gather',resource:'wood',startedTick:first});assert.equal(shown.gatherEpisode,undefined);assert.equal(shown.order,undefined);
 command(s,0,{type:'gather',ids:[u.id],target:r2.id});step(s);assert.ok(u.gatherEpisode.startedTick>first);command(s,0,{type:'stop',ids:[u.id]});step(s);assert.equal(view(s,0).entities.find(e=>e.id===u.id).visibleAction,undefined);command(s,0,{type:'move',ids:[u.id],x:15.5,y:23.5});step(s);assert.equal(view(s,0).entities.find(e=>e.id===u.id).visibleAction?.kind==='gather',false);
 const old=u.gatherEpisode.startedTick;u.x=r.x;u.y=r.y;command(s,0,{type:'gather',ids:[u.id],target:r.id});step(s);assert.ok(u.gatherEpisode.startedTick>old);enemy.x=55;enemy.y=45;assert.equal(view(s,0).entities.some(e=>e.id===enemy.id),false);
});
test('actual presentation pause preserves gather frame and resumes current episode without rewind',()=>{
 // NON_ART timing fixture: frame sampling only, no art or motion approval.
 const frames=[100,100,100,100].map(durationMs=>({durationMs}));
 const clock=createPresentationClock(),state=tick=>({tick,map:{id:'delta'},winner:null}),e={visibleAction:{kind:'gather',startedTick:20}};
 const pose=now=>sampleSpriteAnimation(frames,{timeMs:gatherAnimationTime(e,clock.sample(now))}).frame;
 clock.reset(state(19),0);clock.receive(state(20),0);assert.equal(pose(0),0,'received work starts frame0 even when presentation lags behind start');
 clock.receive(state(24),100);assert.equal(pose(300),2);const frozenTime=clock.sample(300),frozenFrame=pose(300);
 clock.receive(state(24),300,{paused:true});assert.equal(clock.sample(9000),frozenTime);assert.equal(pose(9000),frozenFrame,'wall time cannot advance paused work');
 clock.receive(state(26),9000,{paused:false});assert.equal(pose(9000),frozenFrame);assert.ok(clock.sample(9050)>=frozenTime);assert.equal(pose(9100),3);assert.equal(e.visibleAction.startedTick,20);
 const bounded=clock.sample(20000);assert.equal(bounded,26*50);assert.equal(gatherAnimationTime({visibleAction:{kind:'gather'}},bounded),bounded,'unknown legacy start retains bounded received clock');
});
