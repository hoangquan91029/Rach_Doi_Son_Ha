import test from 'node:test';
import assert from 'node:assert/strict';
import {terrainTransitionEdges} from '../client/terrain-transitions.js';
test('shore blending only receives into land or ford and preserves authoritative terrain',()=>{
 const map={width:3,height:2,tiles:['plain','river','ford','mountain','sea','forest']};const before=JSON.stringify(map);
 const edges=terrainTransitionEdges(map);
 assert.equal(edges.length,4);assert.ok(edges.every(e=>e.receiver!=='river'&&e.receiver!=='sea'&&e.receiver!=='mountain'));
 assert.ok(edges.some(e=>e.receiver==='ford'&&e.source==='river'));assert.equal(JSON.stringify(map),before);
});
test('unobserved cell boundaries do not contribute transition coverage',()=>{
 const map={width:2,height:1,tiles:['plain','river']};
 assert.deepEqual(terrainTransitionEdges(map,{visible:[1,0],explored:[1,0]}),[]);
 assert.equal(terrainTransitionEdges(map,{visible:[1,0],explored:[1,1]}).length,1);
});

import {createTerrainTransitions,transitionGradient} from '../client/terrain-transitions.js';
const project=(x,y)=>({x:(x-y)*27,y:(x+y)*13.5});
test('alpha gradient normal is perpendicular to either dimetric edge tangent',()=>{
 for(const axis of ['x','y'])for(const sign of [-1,1]){
  const g=transitionGradient({x:3,y:4,axis,sign},project,.22),[a,b,,c]=g.points;
  const gradient={x:g.end.x-g.start.x,y:g.end.y-g.start.y};
  assert.ok(Math.abs(gradient.x*(b.x-a.x)+gradient.y*(b.y-a.y))<1e-9);
  const dot=p=>((p.x-a.x)*gradient.x+(p.y-a.y)*gradient.y)/(gradient.x**2+gradient.y**2);
  assert.ok(Math.abs(dot(b))<1e-9);assert.ok(Math.abs(dot(c)-1)<1e-9);
 }
});
test('original-material patches reuse on pan and invalidate for zoom, terrain and actual material revision',()=>{
 let paints=0,revision='hash1',bank=false;const stops=[];
 const context=()=>({clearRect(){},save(){},restore(){},beginPath(){},moveTo(){},lineTo(){},closePath(){},clip(){},fillRect(){},drawImage(){},createLinearGradient(){return {addColorStop:(...args)=>stops.push(args)};}});
 const t=createTerrainTransitions({paintMaterial:()=>{paints++;return true;},materialKey:()=>revision,hasBank:()=>bank,createCanvas:(width,height)=>({width,height,getContext:context})});
 const map={width:2,height:1,tiles:['plain','river']},ctx={canvas:{width:500,height:500},getTransform:()=>({a:1}),drawImage(){}};
 t.draw(ctx,{map,project});assert.equal(paints,1);assert.deepEqual(stops.slice(0,2),[[0,'rgba(0,0,0,1)'],[1,'rgba(0,0,0,0)']]);
 t.draw(ctx,{map,project:(x,y)=>{const p=project(x,y);return {x:p.x+100,y:p.y+100};}});assert.equal(paints,1);
 t.draw(ctx,{map,project,zoom:1.08});assert.equal(paints,2);revision='hash2';t.draw(ctx,{map,project,zoom:1.08});assert.equal(paints,3);
 bank=true;t.draw(ctx,{map,project,zoom:1.08});assert.equal(paints,5);assert.deepEqual(stops.slice(-3),[[0,'rgba(0,0,0,0)'],[.5,'rgba(0,0,0,.5)'],[1,'rgba(0,0,0,0)']]);
 map.tiles[0]='ford';t.draw(ctx,{map,project,zoom:1.08});assert.equal(paints,6); // No shore layer on ford receiving side.
 t.draw(ctx,{map,fog:{visible:[0,0],explored:[0,0]},project,zoom:1.08});assert.equal(paints,6);
});
