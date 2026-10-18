import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {validatePixelOrder,preparePixelOrder} from '../scripts/pixel-sprite-contract.mjs';
const values={identity:'worker',action:'walk',direction:'0'};
function order(){return {id:'fresh',jobKind:'fresh-pixel',identityMode:'new-pixel-identity',status:'OPEN',identity:'worker',action:'walk',direction:0,enforcement:{taskId:'test'},lineage:{humanScope:'pixel-rebuild-535'},designPin:{},stylePin:{},promptPin:{},jobPin:{},slots:[{kind:'initial',template:'pixel_strip',status:'pending'}],callLimit:1,callsUsed:0,correctionCap:0,correctionsUsed:0};}
test('finite new identity guards and consumed calls',()=>{assert.equal(validatePixelOrder(order(),values,0).kind,'initial');for(const mutate of [o=>o.jobKind='action',o=>o.identityMode='legacy',o=>o.direction=8,o=>o.callsUsed=1,o=>o.lineage.humanScope='old',o=>o.slots[0].status='used']){const o=order();mutate(o);assert.throws(()=>validatePixelOrder(o,values,0));}});
test('root pinned design/style/prompt with empty refs; drift rejected',()=>{const root=fs.mkdtempSync(path.join(os.tmpdir(),'pixel535-'));try{const o=order();for(const key of ['designPin','stylePin','promptPin']){fs.writeFileSync(path.join(root,key),'native new pixel');o[key]={path:key,sha256:createHash('sha256').update('native new pixel').digest('hex')};}fs.writeFileSync(path.join(root,'job'),JSON.stringify({...values,direction:0}));o.jobPin={path:'job',sha256:createHash('sha256').update(fs.readFileSync(path.join(root,'job'))).digest('hex')};const p=preparePixelOrder(o,0,'pixel_strip',values,[],{root});assert.equal(p.pixel.width,1024);assert.equal(p.transparent_background,true);assert.equal(Object.hasOwn(p,'referenced_image_paths'),false);assert.throws(()=>preparePixelOrder(o,0,'pixel_strip',values,[{path:'legacy'}],{root}));fs.writeFileSync(path.join(root,'designPin'),'drift');assert.throws(()=>preparePixelOrder(o,0,'pixel_strip',values,[],{root}));}finally{fs.rmSync(root,{recursive:true});}});
