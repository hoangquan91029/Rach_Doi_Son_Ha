import test from 'node:test';
import assert from 'node:assert/strict';
import {createBootUiAssets} from '../client/boot-ui-assets.js';
test('failed portrait decode is recoverable; successful decoded portraits retained; hanging fonts bounded',async()=>{
 let broken=true,created=0;const loader=createBootUiAssets({characters:{a:{},b:{}},timeoutMs:10,makeImage:()=>{const id=created++;return {src:'',decode:async()=>{if(broken&&id===1)throw Error('offline');}}},fonts:{load:()=>new Promise(()=>{})}});
 await assert.rejects(loader.preload(),/portraits unavailable/);assert.equal(loader.portraits.size,1);assert.equal(loader.status.failures.length,1);assert.equal(loader.status.fontWarnings.length,7);
 const retained=loader.portraits.get('a');broken=false;await loader.preload();assert.equal(loader.portraits.get('a'),retained);assert.equal(loader.portraits.size,2);assert.equal(created,3);assert.deepEqual(loader.status.failures,[]);
});
test('portrait deadline cannot hang boot or install a late decode',async()=>{
 let finish;const loader=createBootUiAssets({characters:{a:{}},timeoutMs:5,fonts:null,makeImage:()=>({src:'',decode:()=>new Promise(resolve=>finish=resolve)})});await assert.rejects(loader.preload(),/timed out/);finish();await new Promise(resolve=>setTimeout(resolve,0));assert.equal(loader.portraits.size,0);
});
