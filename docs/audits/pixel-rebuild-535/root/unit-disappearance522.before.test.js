import test from 'node:test';
import assert from 'node:assert/strict';
import {expectedMatrix} from '../scripts/art-coverage.mjs';
import {IsoRenderer} from '../client/renderer.js';
import {createRasterSlice} from '../client/raster-slice.js';
import {ACTIONS,ACTION_FRAMES,identityActions,actionSpec} from '../shared/unit-action-spec.js';
const actor={id:12,type:'villager',kind:'unit',hp:50,maxHp:100,state:'idle',dir:1,x:3,y:4,owner:0};
const options={project:(x,y)=>({x,y}),tick:10,timeMs:500};
test('HP0 unit/building direct raster calls do not request even available death pages',async()=>{
 const r=createRasterSlice({enabled:true});r.pipeline.preload=async()=>{};
 const asset={id:'death',kind:'unit',family:'unit.villager',state:'death',direction:1,frames:[{durationMs:100}],contactShadow:{mode:'baked'}};
 Object.defineProperty(r.pipeline,'manifest',{value:{assets:[asset]}});let requests=0;r.pipeline.get=()=>{requests++;throw Error('dead page requested');};await r.preload();
 for(const e of [{...actor,hp:0,state:'death'},{...actor,hp:-1},{...actor,kind:'building',type:'granary',hp:0,state:'death'}]){r.observeEntities([e],options);assert.equal(r.sampleEntity(e,options),false);assert.equal(r.drawEntity({drawImage(){throw Error('dead draw');}},e,options),false);assert.deepEqual(r.status.currentEntityDraws,{});}
 assert.equal(requests,0);assert.deepEqual(r.status.missing,[]);r.dispose();
});
test('renderer hides dead actors before observations and any authored or primitive fallback; living healthbar stays',()=>{
 const seen=[],impact=[],fills=[];const ctx={setTransform(){},clearRect(){},fillRect(...a){fills.push(a);}};
 const renderer={ctx,canvas:{width:100,height:100},dpr:1,camera:{zoom:1},raster:{observeEntities:e=>seen.push(e),drawEntity:()=>false},impactPulses:{update:e=>impact.push(e)},project:()=>({x:20,y:40}),selected:[],localPlayer:0,drawUnit(){this.unitCalls=(this.unitCalls||0)+1;},drawBuilding(){throw Error('dead primitive building');}};
 const dead={...actor,id:13,hp:0,state:'death'},building={...dead,id:14,kind:'building',type:'granary'};const state={tick:12,entities:[actor,dead,building]};
 IsoRenderer.prototype.render.call(renderer,state,0,[]);assert.deepEqual(seen[0],[actor]);assert.deepEqual(impact[0],[actor]);
 for(const e of [dead,building])IsoRenderer.prototype.drawEntity.call(renderer,new Proxy({}, {get(){throw Error('dead rendering touched canvas');}}),e,0);
 renderer.raster.drawEntity=()=>true;IsoRenderer.prototype.drawEntity.call(renderer,ctx,actor,0);assert.equal(fills.at(-2)[2],24);assert.equal(fills.at(-1)[2],12);assert.equal(fills.at(-1)[3],3);assert.equal(actor.hp,50);assert.equal(state.entities.length,3);
});
test('current coverage keeps living actions and waives death/destroyed/sink while retaining historical frame counts',()=>{
 assert.ok(expectedMatrix().every(row=>!row.actions.includes('death')));
 assert.equal(ACTION_FRAMES.death,8);assert.ok(!ACTIONS.includes('death'));
 for(const id of ['villager','infantry','wagon','transport','warship','artillery','tran_nhan_tong']){assert.ok(identityActions(id).includes('walk'));for(const a of ['death','destroyed','sink'])assert.equal(actionSpec(id,a).applicable,false);}
 assert.equal(actionSpec('wagon','load').requiresSeparatePoses,true);assert.deepEqual(actionSpec('tran_nhan_tong','build').roles,['king']);
});

test('HP0 buildings vanish from minimap while living building healthbar remains',()=>{
 const fills=[];const ctx={clearRect(){},fillRect(...args){fills.push(args);},beginPath(){},moveTo(){},lineTo(){},closePath(){},stroke(){}};
 const renderer={mctx:ctx,minimap:{width:100,height:100},camera:{x:0,y:0,zoom:1},canvas:{width:100,height:100},dpr:1,visible:()=>true};
 const alive={...actor,kind:'building',type:'granary',id:20,x:1,y:1};const dead={...alive,id:21,hp:0,x:2,y:2};
 IsoRenderer.prototype.drawMinimap.call(renderer,{map:{width:1,height:1,tiles:['plain']},entities:[alive,dead]},0);assert.equal(fills.filter(a=>a[2]===4&&a[3]===4).length,1);
 const bars=[];IsoRenderer.prototype.drawEntity.call({project:()=>({x:10,y:20}),camera:{zoom:1},selected:[],raster:{drawEntity:()=>true},localPlayer:0,state:{tick:1}}, {fillRect(...a){bars.push(a);}},alive,0);assert.equal(bars[0][2],38);assert.equal(bars[1][2],19);
});
