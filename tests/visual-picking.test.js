import test from 'node:test';
import assert from 'node:assert/strict';
import {pickVisibleEntity} from '../client/visual-picking.js';
test('picker uses current rendered sample for tall hat and excludes transparent areas',()=>{
 const image={width:128,height:128},pixels=new Uint8ClampedArray(128*128*4);pixels[(10*128+64)*4+3]=253;
 const old=globalThis.document;globalThis.document={createElement:()=>({getContext:()=>({drawImage(){},getImageData:()=>({width:128,height:128,data:pixels})})})};
 try{const e={id:1,x:0,y:0,hp:100,type:'villager',state:'walk',dir:1},calls=[];const renderer={state:{tick:20,entities:[e]},visualTimeMs:1025,camera:{zoom:1},localPlayer:0,visible:()=>true,project:()=>({x:100,y:100}),raster:{status:{enabled:true},pipeline:{},sampleEntity(entity,opts){calls.push(opts);return {raster:{image,render:{width:89,height:89},pivot:{x:64,y:116},sw:128,sh:128,sx:0,sy:0}}}}};
  const x=100,y=100-(116-10.5)/128*89;assert.equal(pickVisibleEntity(renderer,x,y),e);assert.equal(pickVisibleEntity(renderer,x+10,y),null);assert.deepEqual(calls[0],{tick:20,timeMs:1025});
 }finally{globalThis.document=old;}
});
