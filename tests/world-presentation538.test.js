import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {NORMAL_ZOOM,TILE_WIDTH,TILE_HEIGHT,CAMERA_ELEVATION} from '../client/world-presentation.js';
import {pixelDrawBounds} from '../client/pixel-animation.js';
test('default view renders native128 cell one to one without changing projection axes',()=>{assert.equal(NORMAL_ZOOM,1);assert.deepEqual([TILE_WIDTH,TILE_HEIGHT,CAMERA_ELEVATION],[54,27,26.565]);const bounds=pixelDrawBounds({cellSize:128,anchor:[64,112],renderSize:[128,128]},{x:300,y:250},NORMAL_ZOOM);assert.deepEqual(bounds,{left:236,top:138,width:128,height:128});});
test('launch uses shared default while keyboard and wheel retain distant zoom controls',async()=>{const main=await readFile('client/main.js','utf8');assert.ok(main.includes('renderer.camera.zoom=NORMAL_ZOOM'));assert.ok(main.includes("if(key==='-')renderer.camera.zoom=Math.max(.55,renderer.camera.zoom/1.12)"));assert.ok(main.includes("Math.max(.5,Math.min(1.75,renderer.camera.zoom*(e.deltaY<0?1.1:.91)))"));});
