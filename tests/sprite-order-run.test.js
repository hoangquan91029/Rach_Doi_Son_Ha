import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {createOrderRunner} from '../scripts/sprite-order-run.mjs';
import {prepareOrderWithRegistry,TEMPLATE_FIELDS} from '../scripts/sprite-prompts.mjs';
const sha=bytes=>createHash('sha256').update(bytes).digest('hex');
function fixture(t){
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'sprite489-'));t.after(()=>fs.rmSync(dir,{recursive:true,force:true}));
 const pin=(name,bytes)=>{const p=path.join(dir,name);fs.writeFileSync(p,bytes);return {path:p,sha256:sha(bytes)};};
 const master=pin('master.png','retained fixture bytes');
 const registry={identity:'infantry',masterAuthority:'original',master:{...master,direction:0},camera:{label:'fixed camera',screenFacing:['ESE','South','WSW','West','WNW','North','ENE','East']},views:[],equipmentLock:{status:'verified',statement:'Physical original sword hand and shield hand retained',source:master,basis:'Pinned original ownership'},productionOrders:['view489','walk489','attack489'],jobs:[],allowedReferences:[]};
 const values=Object.fromEntries(TEMPLATE_FIELDS.view.map(f=>[f,'verified fixture']));Object.assign(values,{identity:'infantry',master:master.sha256,direction:'0',camera:registry.camera.label,screenFacing:'ESE',weaponOwnership:registry.equipmentLock.statement,referenceRoles:'originalmaster'});
 const order={id:'view489',jobKind:'view',status:'OPEN',identity:'infantry',direction:0,callLimit:1,callsUsed:0,correctionCap:2,correctionsUsed:0,slots:[{frame:0,phase:0,status:'pending',kind:'initial',template:'view'}]};
 const refs=[{...master,role:'originalmaster'}],ledgerPath=path.join(dir,'ledger.json');
 const save=()=>fs.writeFileSync(ledgerPath,JSON.stringify({schema:'rds-unit-order-ledger/v2',orders:[order]}));save();
 const prepare=(id,slot,kind,v,r)=>prepareOrderWithRegistry(JSON.parse(fs.readFileSync(ledgerPath)).orders.find(o=>o.id===id),slot,kind,v,r,registry);
 const runner=createOrderRunner({ledgerPath,prepare});
 const request=()=>({expectedLedgerSHA:sha(fs.readFileSync(ledgerPath)),orderId:order.id,slotIndex:0,kind:'view',values,references:refs});
 return {pin,registry,values,order,refs,ledgerPath,save,runner,request};
}
test('finite view traverses render references preparation and durable claim once',t=>{
 const f=fixture(t);const prepared=prepareOrderWithRegistry(f.order,0,'view',f.values,f.refs,f.registry);assert.match(prepared.prompt,/same whole original/i);assert.deepEqual(prepared.referenced_image_paths,[f.refs[0].path]);
 const claim=f.runner.claim(f.request());assert.ok(claim.token);assert.equal(JSON.parse(fs.readFileSync(f.ledgerPath)).orders[0].callsUsed,1);assert.throws(()=>f.runner.claim(f.request()),/Exhausted|pending/);
});
test('view refuses action values kind swaps caps extra slots unknown ownership and unknown refs without consumption',t=>{
 const f=fixture(t),prepare=(o=f.order,v=f.values,r=f.refs,reg=f.registry,k='view')=>prepareOrderWithRegistry(o,0,k,v,r,reg);
 assert.throws(()=>prepare({...f.order,jobKind:undefined}),/Explicit order jobKind/);assert.throws(()=>prepare({...f.order,action:'idle'}),/action/);assert.throws(()=>prepare(f.order,{...f.values,phase:'0'}),/action/);assert.throws(()=>prepare({...f.order,jobKind:'invented'}),/jobKind/);assert.throws(()=>prepare({...f.order,callLimit:2}),/budget/);assert.throws(()=>prepare({...f.order,correctionCap:3}),/budget/);assert.throws(()=>prepare({...f.order,slots:[...f.order.slots,...f.order.slots]}),/slots/);assert.throws(()=>prepare(f.order,f.values,f.refs,f.registry,'key'),/template/);
 assert.throws(()=>prepare(f.order,f.values,f.refs,{...f.registry,equipmentLock:{...f.registry.equipmentLock,status:'unknown'}}),/unknown/);
 assert.throws(()=>prepare(f.order,f.values,f.refs,{...f.registry,master:null,equipmentLock:{...f.registry.equipmentLock,status:'not-applicable'}}),/Missing master/);
 assert.throws(()=>prepare(f.order,f.values,f.refs,{...f.registry,equipmentLock:{...f.registry.equipmentLock,source:f.pin('foreign-equipment.png','unrelated equipment')}}),/bind original master/);
 assert.throws(()=>prepare(f.order,{...f.values,referenceRoles:'originalmaster,neighbor'},[...f.refs,{...f.pin('foreign.png','foreign'),role:'neighbor'}]),/Unregistered/);
 assert.equal(JSON.parse(fs.readFileSync(f.ledgerPath)).orders[0].callsUsed,0);
});
test('same identity disjoint action jobs bind exact registry records and reject cross-job stale held and fallback refs',t=>{
 const f=fixture(t);const jobs=['walk','attack'].map(action=>{const source=f.pin(action+'.png',action+' selected pose');const id=action+'489';const ref={...source,role:'neighbor',status:'selected',jobId:id,frame:0,phase:0};const record={id,action,direction:0,variant:'base',...f.pin(action+'.json',JSON.stringify({id,action,direction:0,variant:'base',frames:[{status:'selected',phase:0,input:source}]}))};f.registry.jobs.push(record);f.registry.allowedReferences.push(ref);return {ref,record};});
 const values=Object.fromEntries(TEMPLATE_FIELDS.key.map(k=>[k,'verified fixture']));Object.assign(values,f.values,{action:'walk',phase:'0',referenceRoles:'originalmaster,neighbor'});
 const order={...f.order,id:'walk489',jobKind:'action',action:'walk',job:jobs[0].record,callLimit:8,slots:Array.from({length:8},(_,frame)=>({frame,phase:frame/8,status:'pending',kind:'initial',template:'key'}))};
 const prepare=(o=order,r=[...f.refs,jobs[0].ref],v=values,reg=f.registry)=>prepareOrderWithRegistry(o,0,'key',v,r,reg);
 assert.ok(prepare().prompt);assert.throws(()=>prepare({...order,id:'attack489',action:'attack',job:jobs[1].record},[...f.refs,jobs[1].ref],{...values,action:'attack'},{...f.registry,equipmentLock:{...f.registry.equipmentLock,status:'not-applicable'}}),/Idle-only N\/A/);assert.ok(prepare({...order,id:'attack489',action:'attack',job:jobs[1].record},[...f.refs,jobs[1].ref],{...values,action:'attack'}).prompt);
 assert.throws(()=>prepare(order,[...f.refs,jobs[1].ref]),/Selected job neighbor/);
 assert.throws(()=>prepare({...order,job:{...order.job,sha256:'0'.repeat(64)}}),/registry/);
 assert.throws(()=>prepare({...order,job:undefined}),/binding required/);
 assert.throws(()=>prepare(order,[...f.refs,jobs[0].ref],values,{...f.registry,allowedReferences:[{...jobs[0].ref,status:'held'}]}),/held/);
 fs.appendFileSync(order.job.path,' ');assert.throws(()=>prepare(),/pin mismatch/);
});

test('identical whole PNG is selected independently by immutable job metadata for neighbor and edit target',t=>{
 const f=fixture(t),source=f.pin('shared.png','one whole PNG intentionally reused');
 const jobs=['walk','attack'].map(action=>{const id=action+'489',ref={...source,role:'neighbor',status:'selected',jobId:id,frame:0,phase:0},record={id,action,direction:0,variant:'base',...f.pin(action+'-reuse.json',JSON.stringify({id,action,direction:0,variant:'base',frames:[{status:'selected',phase:0,input:source}]}))};f.registry.jobs.push(record);f.registry.allowedReferences.push(ref);return {ref,record};});
 for(const {ref,record} of jobs){
  const values=Object.fromEntries(TEMPLATE_FIELDS.key.map(k=>[k,'verified fixture']));Object.assign(values,f.values,{action:record.action,phase:'0',referenceRoles:'originalmaster,neighbor'});
  const order={...f.order,id:record.id,jobKind:'action',action:record.action,job:record,callLimit:8,slots:Array.from({length:8},(_,frame)=>({frame,phase:frame/8,status:'pending',kind:'initial',template:'key'}))};
  assert.ok(prepareOrderWithRegistry(order,0,'key',values,[...f.refs,ref],f.registry).prompt);
  assert.deepEqual(prepareOrderWithRegistry(order,0,'key',{...values,referenceRoles:'edittarget,originalmaster'},[{...ref,role:'edittarget'},...f.refs],f.registry).referenced_image_paths,[source.path,f.refs[0].path]);
  for(const changed of [{frame:1},{phase:.5},{jobId:'unknown-job'}])assert.throws(()=>prepareOrderWithRegistry(order,0,'key',values,[...f.refs,{...ref,...changed}],f.registry),/Unregistered/);
  const foreign=jobs.find(j=>j.record.id!==record.id).ref;assert.throws(()=>prepareOrderWithRegistry(order,0,'key',values,[...f.refs,foreign],f.registry),/Selected job neighbor mismatch/);
 }
});
