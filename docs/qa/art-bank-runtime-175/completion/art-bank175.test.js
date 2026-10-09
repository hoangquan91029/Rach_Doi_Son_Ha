import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {webcrypto,createHash} from 'node:crypto';
import {createArtAssetPipeline} from '../client/art-assets.js';
import {createArtBank} from '../client/art-bank.js';
import {matchArtScope} from '../shared/art-bank.js';
import {runInNewContext} from 'node:vm';
import {UNITS,BUILDINGS} from '../shared/data.js';
import {ART_ROUTES} from '../client/art-routes.js';
const url=ART_ROUTES.shipyard.manifestUrl;
const manifest=JSON.parse(await readFile(new URL('../public'+url,import.meta.url)));
const state=map=>({map:{id:map},players:[{king:'tran_nhan_tong',general:'tran_hung_dao'},{king:'le_thanh_tong',general:'ly_thuong_kiet'}]});
const originalBitmap=globalThis.createImageBitmap;globalThis.crypto ||= webcrypto;
let closed=0;globalThis.createImageBitmap=async blob=>{const bytes=new Uint8Array(await blob.arrayBuffer());const runtime=manifest.assets.find(a=>a.runtime.sha256===createHash('sha256').update(bytes).digest('hex')).runtime;return {width:runtime.width,height:runtime.height,close(){closed++;}};};
let calls=0,offline=false;
const fetchImpl=async request=>{calls++;if(offline)throw Error('offline');const u=new URL(request);const bytes=await readFile(new URL('../public'+u.pathname,import.meta.url));return {ok:true,text:async()=>bytes.toString(),arrayBuffer:async()=>bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength)};};
const pipe=bank=>bank.attach(createArtAssetPipeline({manifestUrl:url,allowCandidates:true,fetchImpl}));
test('both maps include every legal unit/building and both actual player leaders',()=>{for(const map of ['delta','coast']){const scope=matchArtScope(state(map));assert.deepEqual(scope.roster,Object.keys(UNITS));assert.deepEqual(scope.buildings,Object.keys(BUILDINGS));assert.deepEqual(scope.leaders,['tran_nhan_tong','tran_hung_dao','le_thanh_tong','ly_thuong_kiet']);}});
test('encoded startup has zero decoded ownership; offline both-map relaunch releases real images',async()=>{
 const bank=createArtBank(),boot=pipe(bank);await bank.prime(boot);assert.equal(boot.stats.ready,0);assert.equal(boot.stats.retainedDecodedBytes,0);assert.equal(boot.stats.encodedReady,manifest.assets.length);const fetched=calls,bytes=bank.status.encodedBytes;assert.ok(bytes>0);boot.dispose();offline=true;
 for(const map of ['delta','coast']){const p=pipe(bank);assert.equal(await bank.activate(p,state(map)),true);assert.equal(p.stats.ready,manifest.assets.length);assert.ok(p.stats.retainedDecodedBytes>0);assert.ok(p.get('building.shipyard',{state:'idle',direction:null}).image);const before=closed;p.dispose();bank.release();assert.ok(closed>before);assert.equal(p.stats.retainedDecodedBytes,0);assert.equal(p.stats.reservedDecodedBytes,0);assert.equal(p.stats.uniqueDecodedImages,0);assert.equal(p.get('building.shipyard').image,null);assert.equal(bank.status.phase,'menu');assert.deepEqual(bank.status.activeIds,[]);assert.equal(bank.status.encodedBytes,bytes);}
 assert.equal(calls,fetched);offline=false;
});
test('menu cancellation closes late decoded image and prevents epoch resurrection',async()=>{
 const bank=createArtBank(),boot=pipe(bank);await bank.prime(boot);boot.dispose();const p=pipe(bank),decode=globalThis.createImageBitmap;let resume,entered;const atDecode=new Promise(r=>entered=r),unblock=new Promise(r=>resume=r);globalThis.createImageBitmap=async blob=>{entered();await unblock;return decode(blob);};
 const pending=bank.activate(p,state('coast'));await atDecode;p.dispose();bank.release();const before=closed;resume();globalThis.createImageBitmap=decode;
 // Multiple bounded concurrent decodes each own their wait; disposal rejects later work.
 const result=await pending;assert.equal(result,false);assert.equal(bank.status.phase,'menu');assert.equal(p.stats.ready,0);assert.equal(p.stats.retainedDecodedBytes,0);assert.equal(p.stats.reservedDecodedBytes,0);assert.ok(closed>before);
});
test('encoded aggregate budget and hash mismatch fail without caching unverified bytes',async()=>{
 const bank=createArtBank({maxEncodedBytes:1});await assert.rejects(bank.prime(pipe(bank)),/Encoded bank byte budget/);assert.equal(bank.status.encodedBytes,0);
 const bad=createArtAssetPipeline({manifestUrl:url,allowCandidates:true,fetchImpl:async request=>new URL(request).pathname===url?{ok:true,text:async()=>JSON.stringify(manifest)}:{ok:true,arrayBuffer:async()=>new Uint8Array([1,2,3]).buffer}});
 await assert.rejects(bad.cacheEncoded(),/SHA256 mismatch/);assert.equal(bad.stats.retainedEncodedBytes,0);assert.equal(bad.stats.retainedDecodedBytes,0);bad.dispose();
});
test('Continue after partial encoded boot failure retries selected missing bytes on recovery',async()=>{
 const bank=createArtBank();let failed=true;const flaky=async request=>{if(failed&&new URL(request).pathname===new URL(manifest.assets[2].runtime.path,'http://localhost'+url).pathname)throw Error('temporary raster failure');return fetchImpl(request);};
 const boot=bank.attach(createArtAssetPipeline({manifestUrl:url,allowCandidates:true,fetchImpl:flaky}));await assert.rejects(bank.prime(boot),/temporary raster failure/);assert.ok(boot.manifest);assert.ok(boot.stats.encodedReady>0);assert.ok(bank.status.encodedBytes>0);assert.equal(boot.stats.retainedDecodedBytes,0);boot.dispose();bank.release();failed=false;
 const active=bank.attach(createArtAssetPipeline({manifestUrl:url,allowCandidates:true,fetchImpl:flaky}));assert.equal(await bank.activate(active,state('coast')),true);assert.equal(active.stats.ready,manifest.assets.length);assert.equal(active.stats.failed,0);active.dispose();bank.release();
});
test('unavailable boot manifest is explicitly primed again before recovered match decoding',async()=>{
 const bank=createArtBank();let failed=true;const flaky=async request=>{if(failed)throw Error('temporary manifest failure');return fetchImpl(request);};
 const boot=bank.attach(createArtAssetPipeline({manifestUrl:url,allowCandidates:true,fetchImpl:flaky}));await assert.rejects(bank.prime(boot),/temporary manifest failure/);assert.equal(boot.manifest,null);boot.dispose();bank.release();failed=false;
 const active=bank.attach(createArtAssetPipeline({manifestUrl:url,allowCandidates:true,fetchImpl:flaky}));assert.equal(await bank.activate(active,state('delta')),true);assert.equal(active.stats.ready,manifest.assets.length);active.dispose();bank.release();
});
test('actual launch failure keeps gameplay/Pause gate until explicit retry or menu',async()=>{
 const source=await readFile(new URL('../client/main.js',import.meta.url),'utf8');
 const extract=(start,end)=>source.slice(source.indexOf(start),source.indexOf(end,source.indexOf(start)));
 const buttons=new Map(),app={state:{map:{id:'coast'}},mode:'online'},messages=[];let commands=0,attempts=0,cancelled=false;
 const context={app,renderer:{activateArt:async()=>{attempts++;throw Error('decode fault');}},cancelAnimationFrame(){},animId:0,showModal:html=>messages.push(html),esc:String,$:selector=>{if(!buttons.has(selector))buttons.set(selector,{});return buttons.get(selector);},leaveToMenu(){cancelled=true;app.artLoading=false;},send(){commands++;}};
 runInNewContext(extract('async function launchGame(){','function frame(')+extract('function issue(cmd){',"const world=byId('world');")+extract('function openPause(){','function showModal('),context);
 await context.launchGame();assert.equal(app.artLoading,true);assert.match(messages.at(-1),/Artwork could not load/);context.issue({type:'stop'});context.openPause();assert.equal(commands,0);assert.match(messages.at(-1),/Artwork could not load/);
 await buttons.get('#retryArt').onclick();assert.equal(attempts,2);assert.equal(app.artLoading,true);buttons.get('#cancelArt').onclick();assert.equal(cancelled,true);assert.equal(app.artLoading,false);
});
test.after(()=>{globalThis.createImageBitmap=originalBitmap;});
