import test from 'node:test';
import assert from 'node:assert/strict';
import {createHash,webcrypto} from 'node:crypto';
import {createArtAssetPipeline} from '../client/art-assets.js';
import {createArtBank} from '../client/art-bank.js';
import {TILE_WIDTH,TILE_HEIGHT,CAMERA_ELEVATION} from '../client/world-presentation.js';
globalThis.crypto ||= webcrypto;
// Actual encoded 1px PNG fixture; mocked decode, real encoded hash verification.
const png=Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQIHWP4z8DwHwAFgAI/ScLttAAAAABJRU5ErkJggg==','base64');
const sha=createHash('sha256').update(png).digest('hex');
const asset=(id,state='walk',policy='on-demand')=>({id,family:'unit.infantry',kind:'unit',state,direction:0,source:{path:'original.png',width:1,height:1,sha256:sha,rgbaSha256:sha},runtime:{path:id+'.png',width:1,height:1,sha256:sha,rgbaSha256:sha,derivation:{method:'copy',sourceSha256:sha}},cell:{width:1,height:1},pivot:{space:'source',x:.5,y:1},render:{width:42,height:42},alphaPolicy:'transparent',contactShadow:{mode:'baked'},candidate:true,review:{status:'CANDIDATE'},frames:[{x:0,y:0,width:1,height:1,durationMs:100}],loadPolicy:policy});
const makeManifest=assets=>({schemaVersion:1,status:'CANDIDATE',camera:{projection:'dimetric',ratio:[2,1],tile:[TILE_WIDTH,TILE_HEIGHT],elevation:CAMERA_ELEVATION},assets});
function setup(assets,{budget=8,decode}={}){const requests=[],closed=[],signals=[];let offline=false;globalThis.createImageBitmap=decode|| (async()=>({width:1,height:1,close(){closed.push(true);}}));
 const fetchImpl=async(url,{signal}={})=>{requests.push(new URL(url).pathname);signals.push(signal);if(offline)throw Error('offline');if(signal?.aborted)throw Error('aborted');return new URL(url).pathname.endsWith('manifest.json')?{ok:true,text:async()=>JSON.stringify(makeManifest(assets))}:{ok:true,arrayBuffer:async()=>png.buffer.slice(png.byteOffset,png.byteOffset+png.byteLength)};};
 const pipeline=createArtAssetPipeline({manifestUrl:'/test/manifest.json',allowCandidates:true,fetchImpl,maxDecodedBytes:budget});return {pipeline,requests,closed,signals,offline(){offline=true;},fetchImpl};}
const turn=()=>new Promise(r=>setTimeout(r,0));
test('deferred pages excluded from encoded prime and decode startup; exact first request pending',async()=>{
 const f=setup([asset('idle','idle'),asset('walk')]);await f.pipeline.cacheEncoded();assert.deepEqual(f.requests,['/test/manifest.json','/test/idle.png']);await f.pipeline.preload();assert.equal(f.pipeline.stats.ready,1);assert.equal(f.pipeline.stats.deferredDeclared,1);
 assert.equal(f.pipeline.get('walk',{state:'walk',direction:0}).pending,true);assert.equal(f.pipeline.get('walk').image,null);await f.pipeline.whenIdle();assert.ok(f.pipeline.get('walk').image);assert.equal(f.requests.filter(x=>x.endsWith('walk.png')).length,1);f.pipeline.dispose();
});
test('LRU evicts only deferred page; retained encoded bytes permit offline re-decode',async()=>{
 const f=setup([asset('idle','idle'),asset('a'),asset('b')]);await f.pipeline.preload();f.pipeline.get('a');await f.pipeline.whenIdle();assert.ok(f.pipeline.get('a').image);await turn();f.pipeline.get('b');await f.pipeline.whenIdle();assert.equal(f.pipeline.stats.evictedPages,1);assert.ok(f.pipeline.get('idle').image);assert.ok(f.pipeline.get('b').image);await turn();const requests=f.requests.length;f.offline();f.pipeline.get('a');await f.pipeline.whenIdle();assert.ok(f.pipeline.get('a').image);assert.equal(f.requests.length,requests);assert.equal(f.pipeline.stats.retainedDecodedBytes,8);f.pipeline.dispose();
});
test('simultaneous requests serialize reservations, bounded budget and current-page pins',async()=>{
 const f=setup([asset('idle','idle'),asset('a'),asset('b'),asset('c')]);await f.pipeline.preload();for(const id of ['a','b','c'])f.pipeline.get(id);await f.pipeline.whenIdle();assert.equal(f.pipeline.stats.pending,0);assert.equal(f.pipeline.stats.reservedDecodedBytes,0);assert.equal(f.pipeline.stats.retainedDecodedBytes,8);assert.equal(f.pipeline.stats.pageErrors.length,0);assert.equal(f.pipeline.stats.evictedPages,2);
 assert.ok(f.pipeline.get('c').image);f.pipeline.get('a');await f.pipeline.whenIdle();assert.match(f.pipeline.stats.pageErrors[0].message,/budget/);assert.ok(f.pipeline.get('c').image);await turn();await f.pipeline.retry('a');assert.ok(f.pipeline.get('a').image);f.pipeline.dispose();
});
test('dispose aborts request signal, closes late decode and never restores page',async()=>{
 let resume,entered;const decoding=new Promise(r=>entered=r),blocked=new Promise(r=>resume=r);let closed=0;
 const f=setup([asset('a')],{decode:async()=>{entered();await blocked;return {width:1,height:1,close(){closed++;}};}});await f.pipeline.preload();f.pipeline.get('a');await decoding;f.pipeline.dispose();assert.ok(f.signals.at(-1).aborted);resume();await f.pipeline.whenIdle();assert.equal(closed,1);assert.equal(f.pipeline.stats.ready,0);assert.equal(f.pipeline.stats.retainedDecodedBytes,0);assert.equal(f.pipeline.stats.reservedDecodedBytes,0);assert.equal(f.pipeline.get('a').image,null);
});
test('separate shadow dependencies eagerly retained and bank activation checks only eager set',async()=>{
 const a=asset('walk');a.contactShadow={mode:'separate',assetId:'shadow'};const shadow={...asset('shadow','static'),family:'shadow',kind:'vfx',contactShadow:{mode:'none'}};const f=setup([asset('idle','idle'),a,shadow],{budget:12});const bank=createArtBank();bank.attach(f.pipeline);await bank.prime(f.pipeline);assert.ok(f.requests.includes('/test/shadow.png'));assert.ok(!f.requests.includes('/test/walk.png'));
 assert.equal(await bank.activate(f.pipeline,{map:{id:'delta'},players:[]}),true);assert.equal(f.pipeline.stats.eagerDeclared,2);assert.equal(f.pipeline.stats.ready,2);assert.ok(bank.status.availableIds.includes('walk'));f.pipeline.dispose();bank.release();
});

test('deferred aliases share unique decoded page and rejected art never queues',async()=>{
 const a=asset('a'),alias=asset('alias');alias.runtime={...a.runtime};const rejected=asset('rejected');rejected.review.status='REJECTED';const f=setup([a,alias,rejected],{budget:4});await f.pipeline.preload();assert.equal(f.pipeline.stats.skipped,1);f.pipeline.get('rejected');assert.equal(f.pipeline.stats.pending,0);f.pipeline.get('a');f.pipeline.get('alias');await f.pipeline.whenIdle();assert.equal(f.pipeline.stats.uniqueDecodedImages,1);assert.equal(f.pipeline.stats.retainedDecodedBytes,4);assert.ok(f.pipeline.get('alias').image);assert.equal(f.requests.filter(x=>x.endsWith('a.png')).length,1);f.pipeline.dispose();
});
test('deferred errors explicit; encoded limit and invalid load policy remain enforced',async()=>{
 const a=asset('bad');a.runtime.sha256='0'.repeat(64);const f=setup([a]);await f.pipeline.preload();f.pipeline.get('bad');await f.pipeline.whenIdle();assert.match(f.pipeline.stats.pageErrors[0].message,/SHA256/);assert.equal(f.pipeline.stats.retainedDecodedBytes,0);assert.equal(f.pipeline.stats.retainedEncodedBytes,0);f.pipeline.dispose();
 const g=setup([asset('a')]);const bank=createArtBank({maxEncodedBytes:1});bank.attach(g.pipeline);await bank.prime(g.pipeline);g.pipeline.get('a');await g.pipeline.whenIdle();assert.match(g.pipeline.stats.pageErrors[0].message,/Encoded bank byte budget/);assert.equal(g.pipeline.stats.retainedDecodedBytes,0);g.pipeline.dispose();
 const invalid=setup([{...asset('a'),loadPolicy:'automatic'}]);await assert.rejects(invalid.pipeline.cacheEncoded(),/load policy/);invalid.pipeline.dispose();
});
