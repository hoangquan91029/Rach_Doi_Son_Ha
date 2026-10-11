import test from 'node:test';
import assert from 'node:assert/strict';
import {cameraGroundCorners} from '../client/camera-viewport.js';
import {TILE_WIDTH,TILE_HEIGHT} from '../client/world-presentation.js';

test('minimap outline projects to the four actual screen edges at each zoom and viewport size',()=>{
 for(const [width,height,zoom] of [[1280,746,1.68],[900,646,.6],[1600,900,1.8]]){
  const camera={x:19,y:27,zoom},corners=cameraGroundCorners(camera,width,height);
  const expected=[[0,0],[width,0],[width,height],[0,height]];
  corners.forEach((p,i)=>{
   const x=width/2+(p.x-p.y-camera.x+camera.y)*TILE_WIDTH*zoom/2;
   const y=height/2+(p.x+p.y-camera.x-camera.y)*TILE_HEIGHT*zoom/2;
   assert.ok(Math.abs(x-expected[i][0])<1e-9);
   assert.ok(Math.abs(y-expected[i][1])<1e-9);
  });
 }
});

test('zoom halves the visible ground dimensions while panning translates every corner',()=>{
 const camera={x:12,y:14,zoom:1},a=cameraGroundCorners(camera,1200,720);
 const b=cameraGroundCorners({...camera,zoom:2},1200,720);
 const c=cameraGroundCorners({...camera,x:17,y:11},1200,720);
 a.forEach((p,i)=>{
  assert.ok(Math.abs(b[i].x-camera.x-(p.x-camera.x)/2)<1e-9);
  assert.ok(Math.abs(b[i].y-camera.y-(p.y-camera.y)/2)<1e-9);
  assert.ok(Math.abs(c[i].x-p.x-5)<1e-9);assert.ok(Math.abs(c[i].y-p.y+3)<1e-9);
 });
 assert.deepEqual(camera,{x:12,y:14,zoom:1});
});
