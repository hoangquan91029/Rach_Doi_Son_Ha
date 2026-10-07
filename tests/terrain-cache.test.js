import test from 'node:test';
import assert from 'node:assert/strict';
import {createTerrainCache} from '../client/terrain-cache.js';
function fixture(){const canvases=[],draws=[],cache=createTerrainCache({createCanvas:(width,height)=>{const c={width,height,getContext:()=>({setTransform(){},clearRect(){}})};canvases.push(c);return c;}});let paints=0;
 return {cache,canvases,draws,options:{map:{id:'same',width:2,height:1,tiles:['plain','river']},project:(x,y)=>({x:100+(x-y)*27,y:50+(x+y)*13.5}),paintTile:()=>{paints++;}},ctx:{drawImage:(...args)=>draws.push(args)},paints:()=>paints};}
test('pan and zoom reuse immutable ground; content and art readiness invalidate same map ID',()=>{
 const f=fixture(),before=JSON.stringify(f.options.map);assert.equal(f.cache.draw(f.ctx,f.options),true);assert.equal(f.paints(),2);assert.equal(JSON.stringify(f.options.map),before);
 f.cache.draw(f.ctx,{...f.options,project:()=>({x:300,y:200}),zoom:1.08});assert.equal(f.paints(),2);assert.equal(f.draws[1][1],300-91*1.08);
 f.options.map.tiles[0]='ford';f.cache.draw(f.ctx,f.options);assert.equal(f.paints(),4);
 f.cache.draw(f.ctx,{...f.options,artRevision:'ready-11'});assert.equal(f.paints(),6);assert.equal(f.cache.status.builds,3);
});
test('DPR quality invalidates while full 64x48 backing storage remains bounded',()=>{
 const f=fixture();f.options.map={width:64,height:48,tiles:Array(64*48).fill('plain')};const before=JSON.stringify(f.options.map);
 assert.equal(f.cache.draw(f.ctx,{...f.options,qualityScale:2}),true);assert.ok(f.cache.status.pixels<=8_000_000);assert.equal(JSON.stringify(f.options.map),before);
 f.cache.draw(f.ctx,{...f.options,qualityScale:1});assert.equal(f.cache.status.builds,2);f.cache.dispose();assert.equal(f.cache.status.pixels,0);
});
