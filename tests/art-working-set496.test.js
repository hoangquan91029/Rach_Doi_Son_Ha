import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {createHash,webcrypto} from 'node:crypto';
import {createArtAssetPipeline} from '../client/art-assets.js';
globalThis.crypto ||= webcrypto;
const manifest=JSON.parse(fs.readFileSync('public/assets/art-v1/fort-202-manifest.json'));
// Actual retained raster bytes and descriptors; decoder mocked, not browser/gameplay qualification.
const originals=manifest.assets.filter(a=>a.kind==='terrain').slice(0,2);
const fixtures=originals.map((a,i)=>({...a,id:`fixture${i}`,kind:'vfx',family:`fixture${i}`,state:'static',contactShadow:{mode:'none'},alphaPolicy:'transparent',loadPolicy:'eager'}));
const bytes=a=>fs.readFileSync('public/assets/art-v1/'+a.runtime.path);
const lengths=fixtures.map(a=>bytes(a).length);
const fetchImpl=async url=>{const path=new URL(url).pathname;if(path.endsWith('manifest.json'))return {ok:true,text:async()=>JSON.stringify({...manifest,assets:fixtures})};const a=fixtures.find(a=>path.endsWith(a.runtime.path));const b=bytes(a);return {ok:true,arrayBuffer:async()=>b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength)};};
const store=()=>({records:new Map(),manifests:new Map(),bytes:0,maxBytes:Math.max(...lengths)});
const pipe=s=>createArtAssetPipeline({manifestUrl:'/assets/art-v1/fixture-manifest.json',allowCandidates:true,fetchImpl}).attachEncodedStore(s);
test('disposed eager encoded pages relinquish retention so a different selected epoch fits unchanged budget',async()=>{
 const s=store(),first=pipe(s);first.selectAssets(['fixture0']);await first.preload();assert.equal(first.stats.failed,0);first.dispose();
 const second=pipe(s);second.selectAssets(['fixture1']);await second.preload();assert.equal(second.stats.failed,0,JSON.stringify(second.stats.failures));assert.ok(s.bytes<=s.maxBytes);second.dispose();
});
globalThis.createImageBitmap=async blob=>{const b=Buffer.from(await blob.arrayBuffer()),hash=createHash('sha256').update(b).digest('hex'),a=fixtures.find(a=>a.runtime.sha256===hash);return {width:a.runtime.width,height:a.runtime.height,close(){}};};
test('live shared eager owner blocks eviction until every owner disposes; failed epoch can retry',async()=>{
 const s=store(),a=pipe(s),b=pipe(s);a.selectAssets(['fixture0']);b.selectAssets(['fixture0']);await Promise.all([a.preload(),b.preload()]);assert.equal(a.stats.failed+b.stats.failed,0);assert.equal(s.records.size,1);a.dispose();
 const blocked=pipe(s);blocked.selectAssets(['fixture1']);await blocked.preload();assert.match(blocked.stats.failures[0].message,/budget/);blocked.dispose();assert.equal(s.records.size,1);b.dispose();
 const recovered=pipe(s);recovered.selectAssets(['fixture1']);await recovered.preload();assert.equal(recovered.stats.failed,0);recovered.dispose();assert.ok([...s.records.values()].every(r=>r.requiredOwners.size===0));
});
test('bounded repeated selected epochs evict and refetch real pages without retained decoded ownership',async()=>{
 const s=store();for(let i=0;i<12;i++){const p=pipe(s);p.selectAssets([`fixture${i%2}`]);await p.preload();assert.equal(p.stats.failed,0);assert.ok(s.bytes<=s.maxBytes);assert.equal(s.records.size,1);p.dispose();assert.equal(p.stats.retainedDecodedBytes,0);assert.equal(p.stats.reservedDecodedBytes,0);assert.equal(p.stats.uniqueDecodedImages,0);}
});
