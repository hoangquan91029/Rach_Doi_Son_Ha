import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {TEMPLATE_FIELDS, validateMaster, validateJobBinding, prepareOrderWithRegistry, preparePrompt} from '../scripts/sprite-prompts.mjs';

const base='docs/art/pipeline/unit-production';
const read=identity=>JSON.parse(fs.readFileSync(`${base}/${identity}/identity.json`));
const records=()=>fs.readdirSync(base).filter(n=>fs.existsSync(`${base}/${n}/identity.json`)).map(read);
const samePin=(a,b)=>a.sha256===b.sha256&&path.resolve(a.path)===path.resolve(b.path);

test('all21 identities have source-bound equipment or explicit missing-master uncertainty',()=>{
 const all=records();assert.equal(all.length,21);assert.equal(all.filter(r=>r.master).length,10);
 assert.equal(all.filter(r=>!r.master).length,11);
 for(const r of all){
  const lock=r.equipmentLock;assert.ok(lock,r.identity);assert.ok(lock.basis?.trim(),r.identity);
  if(!r.master){assert.equal(lock.status,'unknown',r.identity);assert.equal(lock.source,null);assert.equal(lock.statement,null);continue;}
  assert.ok(['verified','not-applicable'].includes(lock.status),r.identity);
  assert.ok(lock.statement?.trim(),r.identity);assert.equal(validateMaster(r.master),true);assert.equal(validateMaster(lock.source),true);
  assert.ok(samePin(lock.source,r.master),`Equipment evidence must belong to selected master: ${r.identity}`);
 }
});

test('infantry ownership and complete wagon assembly survive equipment intake',()=>{
 const infantry=read('infantry'),wagon=read('wagon');
 assert.equal(infantry.master.sha256,'084845e5f6cb50be8baf9903b8c2ae0798842811ad039aebf71486320eb0517f');
 assert.match(infantry.weaponOwnership,/Physical sword hand and shield hand remain/);
 assert.match(infantry.weaponOwnership,/screenleft.*screenright/);
 assert.equal(infantry.equipmentLock.statement,infantry.weaponOwnership);
 assert.equal(wagon.master.sha256,'93124b0a4959072880579ba0fd88f0a31ee227c4eb7369bde80880828d8a8030');
 assert.match(wagon.weaponOwnership,/whole original415 horse, cart, harness and cargo/);
 assert.equal(wagon.equipmentLock.status,'verified');assert.equal(wagon.equipmentLock.statement,wagon.weaponOwnership);
 for(const name of ['artillery','transport'])assert.equal(read(name).equipmentLock.status,'verified');
});

test('empty-handed idle evidence does not authorize work-tool equipment',()=>{
 const names=records().filter(r=>r.equipmentLock.status==='not-applicable').map(r=>r.identity).sort();
 assert.deepEqual(names,['tran_nhan_tong','villager']);
 const villager=read('villager');assert.match(villager.equipmentLock.statement,/idle master/);assert.match(villager.equipmentLock.statement,/work-action tools require their own existing source pins and grips/);
 assert.match(read('tran_nhan_tong').equipmentLock.statement,/static master.*future action equipment/);
 const values=Object.fromEntries(TEMPLATE_FIELDS.key.map(f=>[f,'observed static fixture']));
 Object.assign(values,{identity:'villager',master:villager.master.sha256,direction:'0',camera:villager.camera.label,screenFacing:villager.camera.screenFacing[0],weaponOwnership:'Hold a newly invented pickaxe',referenceRoles:'originalmaster',action:'gather_iron',phase:'0'});
 assert.throws(()=>preparePrompt('key',values,[{...villager.master,role:'originalmaster'}]),/Equipment ownership lock mismatched/);
 for(const action of ['gather_wood','gather_iron','gather_food','build','attack']){
  assert.throws(()=>preparePrompt('key',{...values,action,weaponOwnership:villager.equipmentLock.statement},[{...villager.master,role:'originalmaster'}]),/action equipment/i,`Idle N/A cannot authorize ${action} tools`);
 }
 const leader=read('tran_nhan_tong');
 for(const action of ['attack','build','ability']){
  assert.throws(()=>preparePrompt('key',{...values,identity:'tran_nhan_tong',master:leader.master.sha256,camera:leader.camera.label,screenFacing:leader.camera.screenFacing[0],action,weaponOwnership:leader.equipmentLock.statement},[{...leader.master,role:'originalmaster'}]),/action equipment/i,`Idle N/A cannot authorize leader ${action} equipment`);
 }

});

test('actual job bindings are unique typed pins to retained job content',()=>{
 let seen=0;
 for(const r of records()){
  assert.ok(Array.isArray(r.jobs),r.identity);const keys=new Set();
  for(const j of r.jobs){
   assert.equal(typeof j.id,'string');assert.equal(typeof j.action,'string');assert.ok(Number.isInteger(j.direction)&&j.direction>=0&&j.direction<=7);assert.ok(j.variant?.trim());
   const key=JSON.stringify([j.action,j.direction,j.variant]);assert.ok(!keys.has(key),`${r.identity} duplicate action/direction/variant`);keys.add(key);
   assert.equal(validateJobBinding(j,r,{action:j.action,direction:String(j.direction)}),j);seen++;
  }
 }
 assert.ok(seen>0,'Retained real action jobs must remain registered');
});

test('static intake cannot silently upgrade a view or imply motion, owner or release approval',()=>{
 for(const r of records()){
  assert.match(r.review,/No new approval/);assert.match(r.release,/No promotion authorization/);
  assert.equal(r.views.length,8);
  for(const v of r.views){
   if(v.status!=='selected'){assert.equal(v.status,v.source?'existing static source':'missing',`${r.identity} D${v.direction}`);continue;}
   // A later explicit appearance selection is distinct from the original equipment intake.
   assert.ok(v.selectionReceipt,`${r.identity} D${v.direction} needs scoped selection evidence`);
   validateMaster(v.selectionReceipt);
   const selection=JSON.parse(fs.readFileSync(v.selectionReceipt.path));
   assert.equal(selection.identity,r.identity);assert.equal(selection.direction,v.direction);
   assert.equal(selection.source.sha256,v.source.sha256);assert.equal(selection.master.sha256,r.master.sha256);
   assert.equal(selection.status,'SOURCE_SELECTED_STATIC_ONLY');
   for(const flag of ['motionApproval','ownerMotionApproval','runtimeInstall','release'])assert.equal(selection[flag],false);
  }
  if(r.layoutLock)assert.equal(r.layoutLock.visualApproval,false);
  if(r.sourceCustody)assert.equal(r.sourceCustody.motionApproval,false);
 }
 assert.match(read('tran_nhan_tong').masterAuthority,/original master verification pending/);
});

test('finite missing VillagerD2 view can prepare without action/phase while D2 action cannot borrow D0',()=>{
 const actual=read('villager');assert.equal(actual.views[2].source,null);
 const before=createHash('sha256').update(fs.readFileSync(`${base}/villager/identity.json`)).digest('hex');
 const order={id:'isolated-equipment-view-D2-fixture',jobKind:'view',identity:'villager',direction:2,status:'OPEN',callLimit:1,callsUsed:0,correctionCap:0,correctionsUsed:0,slots:[{frame:0,phase:0,status:'pending',kind:'initial',template:'view'}]};
 const registry=structuredClone(actual);registry.productionOrders=[...(registry.productionOrders||[]),order.id];
 const values={identity:'villager',master:actual.master.sha256,direction:'2',camera:actual.camera.label,screenFacing:actual.camera.screenFacing[2],weaponOwnership:actual.equipmentLock.statement,referenceRoles:'originalmaster',invariants:'Preserve the whole original body, costume, empty hands and camera.'};
 const prepared=prepareOrderWithRegistry(order,0,'view',values,[{...actual.master,role:'originalmaster'}],registry);
 assert.ok(prepared.prompt);assert.equal(Object.hasOwn(values,'action'),false);assert.equal(Object.hasOwn(values,'phase'),false);
 assert.equal(order.callsUsed,0);assert.equal(order.slots[0].status,'pending');
 const actionValues=Object.fromEntries(TEMPLATE_FIELDS.key.map(f=>[f,'bounded fixture']));
 Object.assign(actionValues,values,{action:'walk',phase:'0'});
 assert.throws(()=>preparePrompt('key',actionValues,[{...actual.master,role:'originalmaster'}]),/selected matching view/);
 assert.equal(createHash('sha256').update(fs.readFileSync(`${base}/villager/identity.json`)).digest('hex'),before);
});
