import test from 'node:test';
import assert from 'node:assert/strict';
import {interpolateView} from '../client/presentation.js';

test('render smoothing preserves current fog membership and never changes authoritative coordinates',()=>{
 const previous={map:{id:'delta'},entities:[{id:1,x:0,y:0,hp:80},{id:99,x:1,y:1,hp:80}]};
 const current={map:{id:'delta'},tick:40,winner:null,entities:[{id:1,x:2,y:0,hp:60,dir:0,state:'walk'}]};
 const before=JSON.stringify(current),shown=interpolateView(current,previous,.5);
 assert.equal(shown.entities[0].x,1);assert.equal(shown.entities[0].hp,60);assert.equal(shown.entities[0].state,'walk');
 assert.deepEqual(shown.entities.map(e=>e.id),[1]);assert.equal(JSON.stringify(current),before);assert.equal(previous.entities[0].x,0);
});
test('death, embarkation, victory and reconnect jumps appear from current state without delayed travel',()=>{
 const previous={map:{id:'delta'},entities:[1,2,3].map(id=>({id,x:0,y:0,hp:80}))};
 const current={map:{id:'delta'},winner:1,entities:[{id:1,x:2,y:0,hp:0,state:'death'},{id:2,x:2,y:0,hp:80,embarked:9},{id:3,x:30,y:0,hp:80}]};
 const shown=interpolateView(current,previous,.25);assert.equal(shown.winner,1);
 for(let i=0;i<3;i++)assert.equal(shown.entities[i],current.entities[i]);
});
test('new maps and completed interpolation retain the current view',()=>{
 const current={map:{id:'coast'},entities:[]},previous={map:{id:'delta'},entities:[]};
 assert.equal(interpolateView(current,previous,.5),current);assert.equal(interpolateView(current,{...previous,map:current.map},1),current);
});
