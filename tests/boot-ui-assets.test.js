import test from 'node:test';
import assert from 'node:assert/strict';
import {createBootUiAssets} from '../client/boot-ui-assets.js';
test('pixel rebuild boot never loads archived portraits; hanging fonts bounded on repeated preload',async()=>{
 let created=0,fontCalls=0;const loader=createBootUiAssets({characters:{a:{},b:{}},timeoutMs:10,makeImage:()=>{created++;throw Error('archived portrait forbidden');},fonts:{load:()=>{fontCalls++;return new Promise(()=>{});}}});
 await loader.preload();assert.equal(created,0);assert.equal(loader.status.declared,0);assert.equal(loader.status.ready,0);assert.equal(loader.portraits.size,0);assert.deepEqual(loader.status.failures,[]);assert.equal(loader.status.fontWarnings.length,7);
 await loader.preload();assert.equal(created,0);assert.equal(fontCalls,14);assert.equal(loader.status.fontWarnings.length,7);assert.equal(loader.portraits.size,0);
});
test('font failure is reported without blocking no-portrait boot; missing fonts need no Image',async()=>{
 const loader=createBootUiAssets({characters:{a:{}},fonts:{load:async()=>{throw Error('font unavailable');}},makeImage:()=>{throw Error('archived portrait forbidden');}});await loader.preload();assert.equal(loader.status.fontWarnings.length,7);assert.deepEqual(loader.status.failures,[]);const empty=createBootUiAssets({characters:{a:{}},fonts:null,makeImage:()=>{throw Error('archived portrait forbidden');}});await empty.preload();await empty.preload();assert.deepEqual(empty.status.fontWarnings,[]);assert.equal(empty.portraits.size,0);
});
