// Prepared only. Run after exact root-selected351 append/build/seal; no command/state injection.
import assert from 'node:assert/strict';import {readFile} from 'node:fs/promises';import {createHash} from 'node:crypto';
import {validateManifest} from '/tmp/rds-mixed-gate352-stage/client/art-assets.js';
import {selectFortificationArt} from '/tmp/rds-mixed-gate352-stage/client/fortification-art.js';
import {topologyForMask} from '/tmp/rds-mixed-gate352-stage/client/fortification-topology.js';
const json=async p=>JSON.parse(await readFile(p,'utf8')),base='/tmp/rds-terrain-public342-stage/public/assets/art-v1/fort-202-manifest.json',candidate='/tmp/rds-mixed-gate352-build/assets/art-v1/fort-202-manifest.json',selected=await json(new URL('./selected351.json',import.meta.url)),old=await json(base),m=await json(candidate);
validateManifest(m);assert.equal(old.assets.length,54);assert.equal(m.assets.length,55);assert.deepEqual(m.assets.slice(0,54),old.assets);assert.deepEqual(m.assets[54],selected.descriptor);
const e={id:1,kind:'building',type:'gate',hp:100,owner:0},ctx=mask=>new Map([[1,topologyForMask(mask)]]),a=selectFortificationArt(m.assets,e,ctx(5),'idle').asset;assert.equal(a.id,selected.descriptor.id);assert.equal(a.fortification.axis,'X');assert.deepEqual(a.pivot,{x:627,y:900,space:'source'});assert.deepEqual(a.render,{width:42.3225,height:42.3225});assert.equal(a.runtime.sha256,createHash('sha256').update(await readFile('/tmp/rds-mixed-gate352-build/assets/art-v1/'+a.runtime.path)).digest('hex'));
for(const mask of [0,1,2,3,4,8,12])assert.deepEqual(selectFortificationArt(m.assets,e,ctx(mask),'idle'),selectFortificationArt(old.assets,e,ctx(mask),'idle'));
for(const changed of [{hp:0},{construction:{remaining:1,total:1}},{underConstruction:true},{embarked:1}])assert.equal(selectFortificationArt(m.assets,{...e,...changed},ctx(5),'idle').asset,null);
assert.equal(selectFortificationArt(m.assets,e,ctx(6),'idle').asset,null);
console.log('PASS352 retained54, exact selected351/fixedlayout, supported retained Gate masks and actual state guards');
