import test from 'node:test';
import assert from 'node:assert/strict';
import {withLoadingDeadline} from '../client/loading-deadline.js';
import {createArtAssetPipeline} from '../client/art-assets.js';
test('stalled resource aborts and rejects with truthful deadline status',async()=>{
 let signal;await assert.rejects(withLoadingDeadline(s=>{signal=s;return new Promise(()=>{});},{timeoutMs:10,label:'Residence'}),/Residence loading timed out/);assert.equal(signal.aborted,true);
});
test('decoded bitmap arriving after deadline is closed rather than becoming approved art',async()=>{
 let resolve,closed=0;const loading=withLoadingDeadline(()=>new Promise(r=>{resolve=r;}),{timeoutMs:10});await assert.rejects(loading,/timed out/);resolve({close(){closed++;}});await new Promise(r=>setTimeout(r,0));assert.equal(closed,1);
});
test('manifest deadline completes pipeline with missing-art failure rather than stranding boot',async()=>{
 const statuses=[],pipeline=createArtAssetPipeline({fetchImpl:()=>new Promise(()=>{}),resourceTimeoutMs:10,onStatus:s=>statuses.push(s)});
 await pipeline.preload();assert.equal(pipeline.stats.manifest,'error');assert.equal(pipeline.stats.failed,1);assert.equal(pipeline.stats.ready,0);assert.equal(pipeline.stats.status,'PLACEHOLDER_ONLY');assert.match(pipeline.stats.failures[0].message,/Manifest loading timed out/);assert.equal(statuses.at(-1).failed,1);pipeline.dispose();
});
