import test from 'node:test';
import assert from 'node:assert/strict';
import {validatePixelClip} from '../client/pixel-animation.js';
const pin=path=>({path,sha256:'a'.repeat(64)});
const native=()=>({kind:'native-raster',sources:[pin('docs/art/pixel-worker-537/raw/S.png')],recipe:pin('docs/art/pixel-worker-537/authoring/draw.py'),framePlan:pin('docs/art/pixel-worker-537/authoring/plan.json')});
const clip=provenance=>({schema:'rds-pixel-clip/v1',identity:'worker',action:'walk',atlas:'/assets/worker_walk.png',cellSize:128,atlasSize:1024,frameCount:8,directions:['S','SW','W','NW','N','NE','E','SE'],anchor:[64,112],renderSize:[128,128],frameDurationsMs:Array(8).fill(100),loop:true,events:[],palette:['#000000'],review:{structural:null,visual:null,runtime:null},provenance});
test('typed native pins and existing provider shape accepted without granting review',()=>{for(const p of [native(),{sources:native().sources,callTokens:['actual-token']}])assert.equal(validatePixelClip(clip(p)).review.visual,null);});
test('strict union rejects fake tokens modes extra/missing fields and forbidden paths',()=>{
 const changes=[p=>p.kind='imagegen',p=>p.callTokens=['fake'],p=>delete p.recipe,p=>p.extra=true,p=>p.sources=[],p=>p.recipe.path='docs/art/pixel-other/authoring/draw.py',p=>p.framePlan.path='docs/art/pixel-worker-537/authoring/plan.py',p=>p.recipe.sha256='bad',p=>p.sources[0].path='docs/art/pipeline/old.png',p=>p.sources[0].path='docs/art/pixel-worker-537/raw/../old.png',p=>p.recipe.path='docs/art/pixel-worker-537/authoring/./draw.py'];
 for(const change of changes){const p=native();change(p);assert.throws(()=>validatePixelClip(clip(p)));}
 for(const callTokens of [[],[''],['x','x']])assert.throws(()=>validatePixelClip(clip({sources:native().sources,callTokens})));
});
