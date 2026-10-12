import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile,mkdtemp,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {validateManifest} from '../client/art-assets.js';
import {createHash} from 'node:crypto';
import {ART_ROUTES,artRoute} from '../client/art-routes.js';
import {createCatalog,loadCatalog,compileManifest,selectBank} from '../scripts/art-catalog.mjs';
const catalog=await loadCatalog();
const copy=v=>JSON.parse(JSON.stringify(v));
const hash=b=>createHash('sha256').update(b).digest('hex');
for(const [route,recipe] of Object.entries(ART_ROUTES))test(`legacy ${route} compilation preserves exact header/order/whole entries`,async()=>{
 const original=JSON.parse(await readFile(new URL('../public'+recipe.manifestUrl,import.meta.url)));
 const compiled=compileManifest(catalog,{route});assert.deepEqual(compiled.manifest,original);
 assert.deepEqual(compiled.bank.assetIds,original.assets.map(a=>a.id));
 assert.equal(JSON.stringify(compileManifest(catalog,{route})),JSON.stringify(compiled));
});
test('shared route registry restores illustrated default and keeps unknown disabled and exact world opt-ins',()=>{
 assert.deepEqual(artRoute(''),{name:'fort',enabled:true,...ART_ROUTES.fort});
 for(const search of ['?art=unknown','?art=constructor','?art=__proto__'])assert.deepEqual(artRoute(search),{name:new URLSearchParams(search).get('art'),enabled:false,manifestUrl:ART_ROUTES.pilot.manifestUrl,world:false});
 for(const [route,recipe] of Object.entries(ART_ROUTES)){const selected=artRoute('?art='+route);assert.equal(selected.enabled,true);assert.equal(selected.manifestUrl,recipe.manifestUrl);assert.equal(selected.world,['terrain','iron','workshop','camp','shipyard','fort'].includes(route));}
});
test('scoped bank retains world, desired building/body/portrait and separate-shadow dependency only',()=>{
 const scope={map:'coast',roster:['infantry'],buildings:['shipyard'],leaders:['tran_hung_dao']};const bank=selectBank(catalog,{route:'shipyard',scope});
 for(const id of ['grass','water','forest','shore','ford','infantry-idle-D00','unit-contact-shadow','shipyard-idle-164','tran-hung-dao-idle-D00'])assert.ok(bank.assetIds.includes(id),id);
 for(const id of ['villager-idle-D00','villager-walk-south-014','cavalry-idle-D00','residence','barracks-idle-121'])assert.ok(!bank.assetIds.includes(id),id);
 assert.deepEqual(bank.portraits.map(p=>p.id),['tran_hung_dao']);assert.match(bank.portraits[0].sha256,/^[a-f0-9]{64}$/);assert.deepEqual(bank.missingFamilies,[]);
 assert.deepEqual(selectBank(catalog,{route:'shipyard',scope:{...scope,map:'delta'}}).assetIds,bank.assetIds,'both maps conservatively share authored world assets');
 const result=compileManifest(catalog,{route:'shipyard',scope});assert.deepEqual(result.manifest.assets.map(a=>a.id),bank.assetIds);assert.ok(!result.manifest.assets.some(a=>a.kind==='portrait'));
});
test('catalog deduplicates definitions, recipes deduplicate bank IDs, runtime variants stay distinct',()=>{
 assert.equal(Object.keys(catalog.definitions).length,29);const c=copy(catalog);c.recipes.pilot.assetIds.push(c.recipes.pilot.assetIds[0]);const bank=selectBank(c,{route:'pilot'});assert.equal(bank.assetIds.filter(id=>id==='grass').length,1);
 const original=catalog.definitions['villager-walk-south-014'];assert.equal(original.mappingKey,JSON.stringify(['unit','unit.villager','walk',1,original.asset.runtime.sha256]));assert.equal(compileManifest(c,{route:'pilot'}).manifest.assets.length,catalog.recipes.pilot.assetIds.length);
});
test('missing requested family remains explicit fallback and cannot be a release scope',()=>{
 const scope={map:'coast',roster:['spearman'],buildings:['fort'],leaders:['han_xin']};const result=compileManifest(catalog,{route:'shipyard',scope});assert.deepEqual(result.bank.missingFamilies,['spearman','fort','han_xin']);assert.deepEqual(result.bank.portraits.map(p=>p.id),['han_xin']);assert.throws(()=>compileManifest(catalog,{route:'shipyard',scope,mode:'release'}),/empty\/incomplete/);
});
test('invalid scopes and recipe/dependency corruption are rejected',()=>{
 for(const scope of [{map:'bogus'},{map:'coast',extra:true},{map:'coast',roster:['invented']},{map:'coast',leaders:['invented']},{map:'coast',buildings:'shipyard'},{map:'coast',roster:['infantry','infantry']}])assert.throws(()=>selectBank(catalog,{route:'shipyard',scope}),/Invalid bank scope/);
 assert.throws(()=>selectBank(catalog,{route:'constructor'}),/Unknown route/);const c=copy(catalog);c.recipes.shipyard.assetIds=c.recipes.shipyard.assetIds.filter(id=>id!=='unit-contact-shadow');assert.throws(()=>selectBank(c,{route:'shipyard',scope:{map:'coast',roster:['infantry']}}),/Dependency outside route bank/);
 const d=copy(catalog);d.definitions.grass.asset.render.width+=1;assert.throws(()=>compileManifest(d,{route:'pilot'}),/distorted|changed/);
});
test('conflicting IDs, unsafe runtime/source paths and missing hashes fail before compilation',async()=>{
 const original=JSON.parse(await readFile(new URL('../public/assets/art-v1/manifest.json',import.meta.url)));
 const collision=copy(original);collision.assets[0].render={width:128,height:128};assert.throws(()=>createCatalog({pilot:original,walk:collision}),/Conflicting asset ID/);
 for(const unsafe of ['../outside.png','/outside.png','https://example.com/a.png','runtime/%2e%2e/outside.png','runtime/a.png?query']){const m=copy(original);m.assets[0].runtime.path=unsafe;assert.throws(()=>createCatalog({pilot:m}),/Unsafe asset path/);}
 const source=copy(original);source.assets[0].source.path='../../../../etc/passwd';assert.throws(()=>createCatalog({pilot:source}),/Unsafe asset path/);
 const absolute=copy(original);absolute.assets[0].source.path='/etc/passwd';assert.throws(()=>createCatalog({pilot:absolute}),/outside authoring roots/);
 const missing=copy(original);delete missing.assets[0].runtime.sha256;assert.throws(()=>createCatalog({pilot:missing}),/SHA256|hash/);
});
test('owner naturalness evidence remains shown-loop evidence and cannot approve release',()=>{
 const wood=catalog.definitions['villager-gather-wood-south-024'];assert.equal(wood.acceptance.ownerEvidence.length,1);assert.equal(wood.acceptance.ownerEvidence[0].runtimeEquivalence,'NOT_ESTABLISHED');assert.equal(wood.acceptance.release.status,'NOT_ESTABLISHED');assert.equal(catalog.definitions['villager-walk-south-014'].acceptance.ownerEvidence.length,0);
 for(const route of ['work','food','shipyard'])assert.throws(()=>compileManifest(catalog,{route,mode:'release'}),/Release refused.*pending\/unaccepted/);
});
test('release evidence must bind exact entry and runtime hashes even for synthetic approved metadata',async()=>{
 const m=JSON.parse(await readFile(new URL('../public/assets/art-v1/manifest.json',import.meta.url)));m.assets=[m.assets[0]];m.status='APPROVED';m.assets[0].candidate=false;m.assets[0].review={status:'APPROVED',reviewer:'fixture',receipt:'fixture'};
 const c=createCatalog({pilot:m}),d=c.definitions.grass;d.acceptance.release={status:'RELEASE_ACCEPTED',reviewer:'fixture',receipt:'fixture',receiptSHA256:hash('fixture'),entrySHA256:d.entrySHA256,runtimeSHA256:d.asset.runtime.sha256};assert.equal(compileManifest(c,{route:'pilot',mode:'release'}).manifest.status,'APPROVED');
 d.acceptance.release.entrySHA256=hash('different entry');assert.throws(()=>compileManifest(c,{route:'pilot',mode:'release'}),/Release refused/);d.acceptance.release.entrySHA256=d.entrySHA256;d.acceptance.release.runtimeSHA256=hash('different runtime');assert.throws(()=>compileManifest(c,{route:'pilot',mode:'release'}),/Release refused/);
});

test('CLI emits a loader-ready standalone manifest and requires its route',async()=>{
 const directory=await mkdtemp(path.join(tmpdir(),'catalog170-'));
 try{
  const output=path.join(directory,'manifest.json'),ledger=path.join(directory,'ledger.json');
  const cli=new URL('../scripts/art-catalog.mjs',import.meta.url);
  const run=spawnSync(process.execPath,[cli.pathname,'--route','shipyard','--manifest-output',output,'--output',ledger],{encoding:'utf8'});
  assert.equal(run.status,0,run.stderr);
  const manifest=JSON.parse(await readFile(output));validateManifest(manifest);
  assert.deepEqual(manifest,JSON.parse(await readFile(new URL('../public'+ART_ROUTES.shipyard.manifestUrl,import.meta.url))));
  assert.deepEqual(JSON.parse(await readFile(ledger)).manifest,manifest);
  const invalid=spawnSync(process.execPath,[cli.pathname,'--manifest-output',path.join(directory,'invalid.json')],{encoding:'utf8'});
  assert.notEqual(invalid.status,0);assert.match(invalid.stderr,/requires --route/);
  await assert.rejects(readFile(path.join(directory,'invalid.json')),/ENOENT/);
 }finally{await rm(directory,{recursive:true,force:true});}
});
