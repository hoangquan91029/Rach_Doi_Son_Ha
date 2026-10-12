import test from 'node:test';
import assert from 'node:assert/strict';
import {UNITS,CHARACTERS} from '../shared/data.js';
import {unitArtFamilies,UNIT_ART_FAMILIES,LEADER_ART_FAMILIES} from '../shared/unit-art.js';
import {selectBank,matchArtScope} from '../shared/art-bank.js';
import {createRasterSlice} from '../client/raster-slice.js';
const asset=(identity,state='idle',direction=1)=>({id:`fixture-${identity}-${state}-${direction}`,family:`unit.${identity}`,kind:'unit',state,direction,frames:[{x:0,y:0,width:128,height:128,durationMs:100}],loop:true});
const entity=(type,character)=>({id:1,kind:'unit',type,character,dir:1,state:'idle',x:10,y:10,hp:100});
async function raster(assets,{decoded=true,enabled=true}={}){const r=createRasterSlice({enabled});Object.defineProperty(r.pipeline,'manifest',{get:()=>({assets})});r.pipeline.preload=async()=>{};r.pipeline.get=(id,opts)=>({image:decoded?{width:128,height:128}:null,reason:'fixture decode unavailable',asset:assets.find(a=>a.id===id),frame:opts.frame});await r.preload();return r;}
test('registry covers legal nonleader units and every historical identity, preserving prior aliases',()=>{
 assert.deepEqual(Object.keys(UNIT_ART_FAMILIES),Object.keys(UNITS).filter(id=>!['king','general'].includes(id)));
 assert.deepEqual(Object.keys(LEADER_ART_FAMILIES),Object.keys(CHARACTERS));
 for(const id of Object.keys(UNIT_ART_FAMILIES))assert.deepEqual(unitArtFamilies(entity(id)),[id,`unit.${id}`]);
 for(const role of ['king','general'])for(const id of Object.keys(CHARACTERS))assert.deepEqual(unitArtFamilies(entity(role,id)),[id,`unit.${id}`]);
 assert.equal(unitArtFamilies(entity('general')),null);assert.equal(unitArtFamilies(entity('king','unknown')),null);assert.equal(unitArtFamilies(entity('unknown')),null);assert.equal(unitArtFamilies(entity('__proto__')),null);
});
test('real raster selector resolves every roster type and every leader role only to its exact authored identity',async()=>{
 const identities=[...Object.keys(UNIT_ART_FAMILIES),...Object.keys(CHARACTERS)],r=await raster(identities.map(id=>asset(id)));
 for(const type of Object.keys(UNIT_ART_FAMILIES))assert.equal(r.sampleEntity(entity(type)).raster.asset.family,`unit.${type}`);
 for(const role of ['king','general'])for(const id of Object.keys(CHARACTERS))assert.equal(r.sampleEntity(entity(role,id)).raster.asset.family,`unit.${id}`);
 for(const id of ['villager','infantry','cavalry','tran_hung_dao']){const a={...asset(id),family:id};assert.equal((await raster([a])).sampleEntity(entity(id==='tran_hung_dao'?'general':id,id)).raster.asset.family,id);}
});
test('exact identity owns living idle fallback; wrong identity, invalid direction, death construction and unavailable decode stay missing',async()=>{
 const r=await raster([asset('tran_hung_dao'),asset('general'),asset('king'),asset('infantry')]);
 for(const e of [entity('king','han_xin'),entity('general','ly_thuong_kiet'),entity('general'),entity('king','unknown'),entity('spearman'),entity('firearm'),entity('artillery'),entity('wagon'),entity('warship'),entity('transport'),entity('unknown')])assert.equal(r.sampleEntity(e),false);
 for(const id of [...Object.keys(UNIT_ART_FAMILIES),...Object.keys(CHARACTERS)]){const e=entity(Object.hasOwn(CHARACTERS,id)?'general':id,id),exact=await raster([asset(id)]);const walking={...e,state:'walk'},before=structuredClone(walking),q=exact.sampleEntity(walking);assert.equal(q.raster.asset.family,`unit.${id}`);assert.equal(q.presentation,'STATIC_ILLUSTRATION');assert.equal(q.direction,1);assert.equal(q.requestedState,'walk');assert.equal(q.elapsed,0);assert.deepEqual(walking,before);assert.equal(exact.sampleEntity({...e,dir:2}),false,'missing direction cannot borrow an arbitrary D1 idle');const d0=await raster([asset(id,'idle',0)]),turned={...e,dir:2},turnBefore=structuredClone(turned),fallback=d0.sampleEntity(turned);assert.equal(fallback.raster.asset.family,`unit.${id}`);assert.equal(fallback.presentation,'STATIC_ILLUSTRATION');assert.equal(fallback.requestedDirection,2);assert.equal(fallback.direction,0);assert.equal(fallback.elapsed,0);assert.deepEqual(turned,turnBefore);assert.equal(exact.sampleEntity({...e,hp:0}),false);assert.equal(exact.sampleEntity({...e,state:'death'}),false);assert.equal(exact.sampleEntity({...e,state:'construction'}),false);assert.equal(exact.sampleEntity({...e,dir:8}),false);assert.equal(exact.sampleEntity({...e,embarked:true}),false);assert.equal(exact.sampleEntity({...e,x:NaN}),false);assert.equal((await raster([asset(id)],{decoded:false})).sampleEntity(e),false);assert.equal((await raster([asset(id)],{enabled:false})).sampleEntity(e),false);}
});
test('selected leader bank and raster registry agree without pulling another leader identity',()=>{
 const ids=Object.keys(CHARACTERS),assets=ids.map(id=>asset(id));const catalog={recipes:{fixture:{assetIds:assets.map(a=>a.id)}},definitions:Object.fromEntries(assets.map(a=>[a.id,{asset:{...a,contactShadow:{mode:'baked'}}}])),portraitDependencies:Object.fromEntries(ids.map(id=>[id,{id}]))};
 for(const id of ids){const scope=matchArtScope({map:{id:'delta'},players:[{king:id,general:id}]});const bank=selectBank(catalog,{route:'fixture',scope});assert.deepEqual(bank.assetIds,[asset(id).id]);assert.deepEqual(bank.portraits,[{id}]);assert.ok(unitArtFamilies(entity('king',id)).includes(catalog.definitions[bank.assetIds[0]].asset.family));}
});
