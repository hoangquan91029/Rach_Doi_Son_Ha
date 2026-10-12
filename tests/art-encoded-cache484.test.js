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

const cachedSetup=(assets,{pages=3,budget=8,decode}={})=>{const f=setup(assets,{budget,decode});const store={records:new Map(),manifests:new Map(),bytes:0,maxBytes:png.length*pages};f.pipeline.attachEncodedStore(store);return {...f,store};};
const load=async(f,id)=>{f.pipeline.get(id);await f.pipeline.whenIdle();assert.ok(f.pipeline.get(id).image,id);await turn();};
test('many deferred pages stay bounded while eager bytes remain protected',async()=>{
 const f=cachedSetup([asset('idle','idle'),...Array.from({length:12},(_,i)=>asset('p'+i))]);await f.pipeline.preload();
 for(let i=0;i<12;i++){await load(f,'p'+i);assert.ok(f.store.bytes<=f.store.maxBytes);assert.ok([...f.store.records.keys()].some(k=>k.includes('/idle.png|')));}
 assert.equal(f.pipeline.stats.evictedEncodedPages,10);assert.equal(f.pipeline.stats.pageErrors.length,0);assert.equal(f.pipeline.stats.retainedDecodedBytes,8);f.pipeline.dispose();
});
test('encoded LRU revisit refreshes age and evicted page refetches',async()=>{
 const f=cachedSetup([asset('idle','idle'),asset('a'),asset('b'),asset('c')]);await f.pipeline.preload();await load(f,'a');await load(f,'b');const n=f.requests.length;await load(f,'a');assert.equal(f.requests.length,n);await load(f,'c');
 assert.ok([...f.store.records.keys()].some(k=>k.includes('/a.png|')));assert.ok(![...f.store.records.keys()].some(k=>k.includes('/b.png|')));await load(f,'b');assert.equal(f.requests.filter(x=>x.endsWith('/b.png')).length,2);f.pipeline.dispose();
});
test('decoded cache remains usable after encoded eviction, without refetch',async()=>{
 const f=cachedSetup([asset('idle','idle'),asset('a'),asset('b')],{pages:2,budget:12});await f.pipeline.preload();await load(f,'a');await load(f,'b');assert.ok(![...f.store.records.keys()].some(k=>k.includes('/a.png|')));const n=f.requests.length;f.offline();assert.ok(f.pipeline.get('a').image);assert.equal(f.requests.length,n);f.pipeline.dispose();
});
test('eager pages cannot evict to make room for a deferred page',async()=>{
 const f=cachedSetup([asset('idle','idle'),asset('a')],{pages:1});await f.pipeline.preload();f.pipeline.get('a');await f.pipeline.whenIdle();assert.match(f.pipeline.stats.pageErrors[0].message,/Encoded bank byte budget/);assert.equal(f.store.bytes,png.length);assert.ok(f.pipeline.get('idle').image);f.pipeline.dispose();
});
test('disposal during current decode preserves shared verified bytes and releases reservation',async()=>{
 let enter,resume;const entered=new Promise(r=>enter=r),blocked=new Promise(r=>resume=r);let closes=0;
 const f=cachedSetup([asset('a')],{pages:1,decode:async()=>{enter();await blocked;return {width:1,height:1,close(){closes++;}};}});await f.pipeline.preload();f.pipeline.get('a');await entered;assert.equal([...f.store.records.values()][0].users,1);f.pipeline.dispose();resume();await f.pipeline.whenIdle();assert.equal(closes,1);assert.equal([...f.store.records.values()][0].users,0);assert.equal(f.pipeline.stats.retainedDecodedBytes,0);assert.equal(f.store.bytes,png.length);
});
