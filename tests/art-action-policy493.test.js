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
function setup(assets,{budget=64,decode,unitActionPolicy='on-demand'}={}){const requests=[],closed=[],signals=[];let offline=false,decoded=0;globalThis.createImageBitmap=async blob=>{decoded++;return decode?decode(blob):{width:1,height:1,close(){closed.push(true);}};};
 const fetchImpl=async(url,{signal}={})=>{requests.push(new URL(url).pathname);signals.push(signal);if(offline)throw Error('offline');if(signal?.aborted)throw Error('aborted');return new URL(url).pathname.endsWith('manifest.json')?{ok:true,text:async()=>JSON.stringify(makeManifest(assets))}:{ok:true,arrayBuffer:async()=>png.buffer.slice(png.byteOffset,png.byteOffset+png.byteLength)};};
 const pipeline=createArtAssetPipeline({manifestUrl:'/test/manifest.json',allowCandidates:true,fetchImpl,maxDecodedBytes:budget,unitActionPolicy});return {pipeline,requests,closed,signals,get decoded(){return decoded;},offline(){offline=true;},fetchImpl};}
const turn=()=>new Promise(r=>setTimeout(r,0));
test('manifest default keeps legacy action eager; invalid policy rejected',async()=>{
 const f=setup([asset('idle','idle',undefined),asset('walk','walk','eager')],{unitActionPolicy:'manifest'});await f.pipeline.preload();assert.equal(f.decoded,2);assert.ok(f.pipeline.get('walk').image);f.pipeline.dispose();
 assert.throws(()=>createArtAssetPipeline({unitActionPolicy:'automatic'}),/unit action policy/);
 const legacy=asset('default','walk');delete legacy.loadPolicy;
 const g=setup([legacy]);
 const p=createArtAssetPipeline({manifestUrl:'/test/manifest.json',allowCandidates:true,fetchImpl:g.fetchImpl});await p.preload();assert.equal(p.stats.unitActionPolicy,'manifest');assert.ok(p.get('default').image);p.dispose();g.pipeline.dispose();
});
test('legacy encoded menu warming survives offline match and action demand without eager action decode',async()=>{
 const legacy=asset('legacy','attack');delete legacy.loadPolicy;const eager=asset('eager','walk','eager');const future=asset('future');
 const f=setup([asset('idle','idle'),legacy,eager,future]);const bank=createArtBank();bank.attach(f.pipeline);await bank.prime(f.pipeline);
 assert.equal(f.decoded,0);assert.equal(f.pipeline.stats.ready,0);assert.ok(f.requests.includes('/test/legacy.png'));assert.ok(f.requests.includes('/test/eager.png'));assert.ok(!f.requests.includes('/test/future.png'));
 const requests=f.requests.length;f.offline();assert.equal(await bank.activate(f.pipeline,{map:{id:'delta'},players:[]}),true);assert.equal(f.decoded,1);assert.equal(f.pipeline.stats.unitActionPolicy,'on-demand');assert.equal(f.pipeline.stats.eagerDeclared,1);assert.equal(f.pipeline.stats.deferredDeclared,3);
 assert.equal(f.pipeline.get('legacy',{state:'attack',direction:0}).pending,true);await f.pipeline.whenIdle();assert.ok(f.pipeline.get('legacy').image);assert.equal(f.decoded,2);assert.equal(f.requests.length,requests);assert.equal(f.pipeline.stats.pageErrors.length,0);
 f.pipeline.get('eager');await f.pipeline.whenIdle();assert.ok(f.pipeline.get('eager').image);assert.equal(f.requests.length,requests);f.pipeline.dispose();bank.release();assert.equal(f.pipeline.stats.retainedDecodedBytes,0);
});
test('explicit demand action never fetched before exact request; mandatory kinds and separate shadow eager',async()=>{
 const action=asset('walk');action.contactShadow={mode:'separate',assetId:'shadow'};
 const other=(id,kind)=>({...asset(id,'static'),family:id,kind,contactShadow:{mode:'none'},alphaPolicy:kind==='terrain'?'opaque':'transparent'});
 const f=setup([asset('idle','idle'),action,other('terrain','terrain'),other('ui','ui'),other('portrait','portrait'),other('shadow','vfx')]);await f.pipeline.cacheEncoded();assert.equal(f.decoded,0);assert.ok(!f.requests.includes('/test/walk.png'));await f.pipeline.preload();assert.equal(f.decoded,5);assert.equal(f.pipeline.stats.eagerDeclared,5);assert.equal(f.pipeline.stats.deferredDeclared,1);
 f.pipeline.get('walk',{direction:1});assert.equal(f.pipeline.stats.pending,0);assert.ok(!f.requests.includes('/test/walk.png'));assert.equal(f.pipeline.get('walk',{direction:0}).pending,true);await f.pipeline.whenIdle();assert.equal(f.decoded,6);assert.ok(f.pipeline.get('walk').image);f.pipeline.dispose();
});
test('shared idle/action page decoded once remains eager and aliases demand without another decode',async()=>{
 const idle=asset('idle','idle'),action=asset('walk','walk','eager');action.runtime={...idle.runtime};const f=setup([idle,action]);await f.pipeline.preload();assert.equal(f.decoded,1);assert.equal(f.pipeline.stats.ready,1);assert.equal(f.pipeline.get('walk').pending,true);await f.pipeline.whenIdle();assert.ok(f.pipeline.get('walk').image);assert.equal(f.decoded,1);assert.equal(f.pipeline.stats.uniqueDecodedImages,1);f.pipeline.dispose();assert.equal(f.closed.length,1);
});
test('demanded legacy action disposal closes late decode and clears reservations',async()=>{
 let entered,resume;const started=new Promise(r=>entered=r),blocked=new Promise(r=>resume=r);let closed=0;
 const f=setup([asset('walk','walk','eager')],{decode:async()=>{entered();await blocked;return {width:1,height:1,close(){closed++;}};}});await f.pipeline.cacheEncoded();await f.pipeline.preload();assert.equal(f.decoded,0);f.pipeline.get('walk');await started;f.pipeline.dispose();resume();await f.pipeline.whenIdle();assert.equal(closed,1);assert.equal(f.pipeline.stats.ready,0);assert.equal(f.pipeline.stats.retainedDecodedBytes,0);assert.equal(f.pipeline.stats.reservedDecodedBytes,0);assert.equal(f.pipeline.stats.pending,0);
});
