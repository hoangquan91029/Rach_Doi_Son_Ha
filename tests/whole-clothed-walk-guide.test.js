import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {guidePose, renderGuide} from '../scripts/whole-clothed-walk-guide.mjs';

const config=JSON.parse(fs.readFileSync(new URL('../docs/art/pipeline/villager-pose-control-491/control.json',import.meta.url)));
const travel=(config.motion.frontSoleY-config.motion.rearSoleY)/config.motion.stanceFraction;
const near=(a,b,tolerance=0.0002)=>assert.ok(Math.abs(a-b)<=tolerance,`${a} != ${b}`);

test('each planted physical sole cancels projected root travel across its full stance',()=>{
 for(const id of ['A','B']){
  const start=config.motion.receivingContacts[id];
  const fixed=config.motion.frontSoleY+travel*start;
  for(let i=0;i<100;i++){
   const phase=start+config.motion.stanceFraction*i/100;
   const foot=guidePose(config,phase).feet[id];
   assert.equal(foot.stance,true);assert.equal(foot.lift,0);
   near(foot.sole[1]+travel*phase,fixed);
   assert.equal(foot.sole[0],config.physicalLegs[id].laneX);
  }
 }
});

test('opposite contacts and passing phases exchange physical support without swapping cuff identity',()=>{
 const keys=[0,.25,.5,.75].map(p=>guidePose(config,p));
 assert.equal(keys[0].feet.A.stance,true);assert.equal(keys[0].feet.B.stance,false);
 assert.equal(keys[2].feet.B.stance,true);assert.equal(keys[2].feet.A.stance,false);
 assert.equal(keys[1].feet.B.lift,config.motion.swingLiftPx);
 assert.equal(keys[3].feet.A.lift,config.motion.swingLiftPx);
 near(keys[1].feet.A.groundY,keys[3].feet.B.groundY);
 near(keys[1].feet.B.groundY,keys[3].feet.A.groundY);
 assert.deepEqual(guidePose(config,0),guidePose(config,1));
});

test('stance and Hermite swing join with matching sole position and velocity',()=>{
 const epsilon=.001;
 for(const edge of [0,.5]){
  const before=guidePose(config,edge-epsilon).feet.A;
  const at=guidePose(config,edge).feet.A;
  const after=guidePose(config,edge+epsilon).feet.A;
  near((at.groundY-before.groundY)/epsilon,-travel,2);
  near((after.groundY-at.groundY)/epsilon,-travel,2);
  near(at.lift,0);
 }
});

test('authoring output stays explicitly scoped and contains no source raster or mirrored transform',()=>{
 assert.throws(()=>guidePose({...config,direction:0},0),/D1/);
 assert.throws(()=>guidePose(config,NaN),/Finite/);
 for(let i=0;i<8;i++){
  const svg=renderGuide(config,i/8);
  assert.match(svg,/AUTHORING_ONLY_UNQUALIFIED/);
  assert.match(svg,/data-physical-leg="A"/);assert.match(svg,/data-physical-leg="B"/);
  assert.doesNotMatch(svg,/<image\b|data:image|transform=|scale\(-/);
 }
});
