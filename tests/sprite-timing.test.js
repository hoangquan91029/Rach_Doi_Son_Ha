import test from 'node:test';
import assert from 'node:assert/strict';
import {sampleSpriteAnimation,validateFrameEvents} from '../client/sprite-timing.js';

const walk=[80,70,80,70,80,70,80,70].map((durationMs,index)=>({durationMs,events:index===0||index===4?[{name:index===0?'LEFT_CONTACT':'RIGHT_CONTACT',offsetMs:0}]:[]}));

test('South walk keeps its unequal holds, switches support at 300ms and loops at 600ms',()=>{
 const times=[0,79,80,149,150,229,230,299,300,379,380,449,450,529,530,599,600];
 assert.deepEqual(times.map(timeMs=>sampleSpriteAnimation(walk,{timeMs}).frame),[0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,0]);
 assert.equal(sampleSpriteAnimation(walk,{timeMs:-1}).frame,7);
});

test('presentation sampling gives the same pose at shared times across 30,60,120Hz',()=>{
 const before=JSON.stringify(walk);
 for(const hz of [30,60,120]){
  // The three render schedules coincide at each 100ms. Missed paints do not advance a counter.
  for(let timeMs=0;timeMs<=1200;timeMs+=100){
   const renderedTime=Math.round(timeMs*hz/1000)*1000/hz;
   assert.deepEqual(sampleSpriteAnimation(walk,{timeMs:renderedTime}),sampleSpriteAnimation(walk,{timeMs}));
  }
 }
 assert.equal(JSON.stringify(walk),before);
});

test('nonlooping death holds the last pose after completion; markers are detached data',()=>{
 assert.equal(sampleSpriteAnimation(walk,{timeMs:600,loop:false}).frame,7);
 assert.equal(sampleSpriteAnimation(walk,{timeMs:60000,loop:false}).frame,7);
 assert.equal(sampleSpriteAnimation(walk,{timeMs:-100,loop:false}).frame,0);
 const sample=sampleSpriteAnimation(walk,{timeMs:300});
 assert.deepEqual(sample.events,[{name:'RIGHT_CONTACT',offsetMs:0}]);
 sample.events[0].name='MUTATED';assert.equal(walk[4].events[0].name,'RIGHT_CONTACT');
 assert.equal(sampleSpriteAnimation(walk,{frame:-1}).frame,7);
});

test('event markers reject out-of-frame timing, invalid names and oversized lists',()=>{
 validateFrameEvents({durationMs:70});
 validateFrameEvents({durationMs:70,events:[{name:'MUZZLE_FLASH',offsetMs:69}]});
 for(const events of [[{name:'DEAL_DAMAGE',offsetMs:70}],[{name:'FIRE_PROJECTILE',offsetMs:-1}],[{name:'CONTACT',offsetMs:1.5}],[{name:'bad name',offsetMs:0}],Array(33).fill({name:'CONTACT',offsetMs:0}),{}])assert.throws(()=>validateFrameEvents({durationMs:70,events}));
});
