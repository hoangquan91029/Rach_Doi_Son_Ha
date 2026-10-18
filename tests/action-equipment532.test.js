import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import {createHash} from 'node:crypto';
import {validatePromptReferences,prepareOrderWithRegistry,TEMPLATE_FIELDS} from '../scripts/sprite-prompts.mjs';
const original=JSON.parse(fs.readFileSync('docs/art/pipeline/unit-production/villager/identity.json'));
function fixture(t){
 const registry=structuredClone(original),source=registry.views.find(v=>v.direction===1).source;
 const lock={action:'hit',status:'verified',statement:'Preserve original empty hands during nonfatal hit recoil only.',basis:'Pinned whole original South view, no attack/work equipment claim.',source:{path:source.path,sha256:source.sha256}};
 registry.actionEquipmentLocks=[lock];
 const values=Object.fromEntries(TEMPLATE_FIELDS.key.map(f=>[f,'fixture metadata']));
 Object.assign(values,{identity:'villager',action:'hit',direction:'1',camera:registry.camera.label,screenFacing:registry.camera.screenFacing[1],weaponOwnership:lock.statement,master:source.sha256,referenceRoles:'directionalview',phase:'0'});
 const refs=[{...source,role:'directionalview'}];
 const run=()=>validatePromptReferences('key',values,refs,registry);
 return {registry,lock,values,refs,run};
}
test('actual original D1 separately pinned hit prepares finite order without mutating global lock',t=>{
 const f=fixture(t),before=JSON.stringify(f.registry.equipmentLock),dir=fs.mkdtempSync(path.join(os.tmpdir(),'action532-'));
 t.after(()=>fs.rmSync(dir,{recursive:true,force:true}));
 const job={id:'fixture-hit',action:'hit',direction:1,variant:'nonfatal',frames:[]},p=path.join(dir,'job.json');fs.writeFileSync(p,JSON.stringify(job));
 const binding={...job,path:p,sha256:createHash('sha256').update(fs.readFileSync(p)).digest('hex')};delete binding.frames;
 f.registry.jobs.push(binding);f.registry.productionOrders.push('fixture-order');
 const order={id:'fixture-order',jobKind:'action',status:'OPEN',identity:'villager',action:'hit',direction:1,job:binding,callLimit:3,callsUsed:0,correctionCap:0,correctionsUsed:0,slots:Array.from({length:4},(_,frame)=>({frame,phase:frame/4,status:'pending',kind:'initial',template:'key'}))};
 assert.ok(prepareOrderWithRegistry(order,0,'key',f.values,f.refs,f.registry).prompt.includes(f.lock.statement));assert.equal(JSON.stringify(f.registry.equipmentLock),before);
});
test('missing action pins keep legacy N/A restriction for attack and work',t=>{
 for(const action of ['attack','gather_wood','gather_iron','gather_food','build','repair']){const f=fixture(t);f.values.action=action;f.values.weaponOwnership=f.registry.equipmentLock.statement;assert.throws(f.run,/Idle-only N\/A/);}
 const f=fixture(t);delete f.registry.actionEquipmentLocks;f.values.weaponOwnership=f.registry.equipmentLock.statement;assert.throws(f.run,/Idle-only N\/A/);
});
test('unknown duplicate malformed or N/A hit action metadata is rejected',t=>{
 for(const change of [{action:'invented'},{status:'unknown'},{status:'not-applicable'},{statement:''},{basis:''}]){const f=fixture(t);Object.assign(f.lock,change);assert.throws(f.run,/unknown|invalid|N\/A/);}
 const f=fixture(t);f.registry.actionEquipmentLocks.push({...f.lock});assert.throws(f.run,/duplicate/);
 const g=fixture(t);g.registry.actionEquipmentLocks={};assert.throws(g.run,/array/);
 const h=fixture(t);h.values.weaponOwnership=h.registry.equipmentLock.statement;assert.throws(h.run,/mismatched/);
});
test('source must be unexcluded hash-valid original matching direction',t=>{
 for(const mutate of [f=>f.lock.source.sha256='0'.repeat(64),f=>f.lock.source={...f.registry.master},f=>f.registry.views[1].status='held',f=>f.registry.masterAuthority='candidate',f=>f.registry.master=null,f=>f.registry.excludedReferencePaths.push(f.lock.source.path),f=>f.registry.excludedReferences.push({path:f.lock.source.path}),f=>f.registry.master.sha256='0'.repeat(64)]){const f=fixture(t);mutate(f);assert.throws(f.run,/pin mismatch|matching view|authority|Excluded/);}
 const f=fixture(t);f.lock.source={path:'AGENTS.md',sha256:createHash('sha256').update(fs.readFileSync('AGENTS.md')).digest('hex')};assert.throws(f.run,/matching view/);
});
test('global lock remains validated even with valid scoped hit; legacy idle remains valid',t=>{
 const f=fixture(t);f.registry.equipmentLock.source={...f.lock.source};assert.throws(f.run,/bind original master/);
 const m=fixture(t);m.values.direction='0';m.values.screenFacing=m.registry.camera.screenFacing[0];m.values.master=m.registry.master.sha256;m.refs[0]={...m.registry.master,role:'originalmaster'};m.values.referenceRoles='originalmaster';m.lock.source={path:m.registry.master.path,sha256:m.registry.master.sha256};assert.ok(m.run());
 const g=fixture(t);g.values.action='idle';g.values.weaponOwnership=g.registry.equipmentLock.statement;assert.ok(g.run());
 const h=fixture(t);h.values.direction='0';h.values.screenFacing=h.registry.camera.screenFacing[0];assert.throws(h.run,/matching view/);
});
