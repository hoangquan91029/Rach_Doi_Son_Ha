import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {validateTaskContracts,validateTaskSnapshot,validateTaskReceipt,validateGuardedOrder,validateClaimAccounting} from '../scripts/agent-task-contract.mjs';
import {createOrderRunner} from '../scripts/sprite-order-run.mjs';
const sha=b=>createHash('sha256').update(b).digest('hex');
function fixture(t){
 const root=fs.mkdtempSync(path.join(os.tmpdir(),'rds495-controls-'));t.after(()=>fs.rmSync(root,{recursive:true,force:true}));
 const pin=(name,bytes)=>{fs.mkdirSync(path.dirname(path.join(root,name)),{recursive:true});fs.writeFileSync(path.join(root,name),bytes);return {path:name,sha256:sha(bytes)};};
 const input=pin('input.txt','immutable input'),evidence=pin('evidence.txt','observed fixture evidence');
 const task={schema:'rds-agent-task/v1',id:'worker495',status:'ACTIVE',purpose:'Scoped fixture',worker:{id:'producer',model:'gpt-6.1-sol',reasoningEffort:'low'},outputs:['outputs'],slots:[{orderId:'fixture',slotIndex:0}],inputs:[input]};
 const order={id:'fixture',jobKind:'view',status:'OPEN',identity:'infantry',direction:0,callLimit:1,callsUsed:0,correctionCap:0,correctionsUsed:0,slots:[{frame:0,phase:0,status:'pending',kind:'initial',template:'view'}],enforcement:{version:1,taskId:task.id,method:{family:'fixture-method',parentOrderIds:[]},prerequisites:[],baseline:{callsUsed:0,correctionsUsed:0}}};
 const ledgerPath=path.join(root,'ledger.json'),taskRegistryPath=path.join(root,'tasks.json');
 const save=()=>{fs.writeFileSync(ledgerPath,JSON.stringify({schema:'rds-unit-order-ledger/v2',orders:[order]}));fs.writeFileSync(taskRegistryPath,JSON.stringify({schema:'rds-agent-tasks/v1',tasks:[task]}));};save();
 const request=()=>({expectedLedgerSHA:sha(fs.readFileSync(ledgerPath)),orderId:order.id,slotIndex:0,kind:'view',values:{identity:'infantry',direction:'0'},references:[],taskId:task.id,expectedInputs:[input]});
 const runner=createOrderRunner({root,ledgerPath,taskRegistryPath,prepare:()=>({prompt:'fixture preparation'})});
 const receipt=()=>({schema:'rds-agent-receipt/v1',taskId:task.id,checks:[{command:'node fixture',cwd:root,method:'fixture execution',state:'VERIFIED',executed:true,exitCode:0,observation:'fixture passed',evidence:[evidence]}],...Object.fromEntries(['technical','motion','runtime','owner','release'].map(name=>[name,{state:'UNKNOWN',limitation:'No approval requested'}])),handles:[{id:'fixture-call',status:'CLOSED',observation:'fixture settled'}]});
 return {root,pin,input,evidence,task,order,save,request,runner,receipt,ledgerPath};
}
test('ownership rejects parent/child overlap and slot duplication across active workers',t=>{
 const f=fixture(t),other={...f.task,id:'other',outputs:['outputs/sub/file'],slots:[]};
 assert.throws(()=>validateTaskContracts(f.root,[f.task,other]),/ownership overlap/);
 assert.throws(()=>validateTaskContracts(f.root,[f.task,{...other,outputs:['separate'],slots:f.task.slots}]),/slot ownership overlap/);
 assert.doesNotThrow(()=>validateTaskContracts(f.root,[f.task,{...other,status:'CLOSED'}]));
 assert.throws(()=>validateTaskContracts(f.root,[{...f.task,worker:{...f.task.worker,model:'unknown'}}]),/gpt-6.1-sol/);
 const rootTask={...f.task,id:'root-task',outputs:['root-owned'],slots:[],worker:{role:'ROOT',id:'/root',model:null,reasoningEffort:null}};
 assert.doesNotThrow(()=>validateTaskContracts(f.root,[f.task,rootTask]));
 assert.throws(()=>validateTaskContracts(f.root,[{...rootTask,worker:{...rootTask.worker,id:'forged'}}]),/Root metadata/);
 assert.throws(()=>validateTaskContracts(f.root,[{...rootTask,worker:{...rootTask.worker,model:'gpt-6.1-sol'}}]),/Root metadata/);
 assert.throws(()=>validateTaskContracts(f.root,[{...f.task,worker:{...f.task.worker,id:'/root'}}]),/gpt-6.1-sol/);
 assert.throws(()=>validateTaskContracts(f.root,[{...f.task,worker:{...f.task.worker,role:'UNKNOWN'}}]),/gpt-6.1-sol/);
});
test('nonexistent output under symlink aliases is compared physically and escapes denied',t=>{
 const f=fixture(t);fs.mkdirSync(path.join(f.root,'outputs'));fs.symlinkSync('outputs',path.join(f.root,'alias'));
 assert.throws(()=>validateTaskContracts(f.root,[f.task,{...f.task,id:'other',outputs:['alias/new.png'],slots:[]}]),/ownership overlap/);
 fs.symlinkSync(os.tmpdir(),path.join(f.root,'outside'));
 assert.throws(()=>validateTaskContracts(f.root,[{...f.task,outputs:['outside/new.png']}]),/symlink/);
 assert.throws(()=>validateTaskContracts(f.root,[{...f.task,outputs:['../outside']}]),/escapes/);
});
test('scoped snapshot rejects omitted stale duplicate and changed inputs',t=>{
 const f=fixture(t);assert.equal(validateTaskSnapshot(f.root,[f.task],f.task.id,[f.input]).id,f.task.id);
 assert.throws(()=>validateTaskSnapshot(f.root,[f.task],f.task.id,[]),/Expected scoped/);
 assert.throws(()=>validateTaskSnapshot(f.root,[f.task],f.task.id,[{...f.input,sha256:'0'.repeat(64)}]),/snapshot mismatch/);
 fs.appendFileSync(path.join(f.root,f.input.path),'changed');assert.throws(()=>validateTaskSnapshot(f.root,[f.task],f.task.id,[f.input]),/pin mismatch/);
});
test('guarded runner denies stale input and unowned slot without consuming ledger',t=>{
 const f=fixture(t),before=fs.readFileSync(f.ledgerPath);
 assert.throws(()=>f.runner.claim({...f.request(),taskId:'unknown'}),/task\/version/);
 f.task.slots=[];f.save();assert.throws(()=>f.runner.claim(f.request()),/ownership/);
 assert.deepEqual(fs.readFileSync(f.ledgerPath),before);
 f.task.slots=[{orderId:'fixture',slotIndex:0}];f.save();fs.appendFileSync(path.join(f.root,f.input.path),'change');assert.throws(()=>f.runner.claim(f.request()),/pin mismatch/);assert.deepEqual(fs.readFileSync(f.ledgerPath),before);
});
test('renamed closed method and failed-parent unsupported new family fail closed',t=>{
 const f=fixture(t),parent={id:'old',closed:true,status:'HELD',enforcement:{method:{family:'fixture-method'}}},ledger={orders:[parent,f.order]};
 const args={taskId:f.task.id,expectedInputs:[f.input],slotIndex:0};
 assert.throws(()=>validateGuardedOrder(f.root,ledger,f.order,args,[f.task]),/renamed/);
 parent.enforcement.taskId=f.task.id;parent.enforcement.method.qualification=f.pin('fake-qualification.json',JSON.stringify(f.receipt()));
 assert.throws(()=>validateGuardedOrder(f.root,ledger,f.order,args,[f.task]),/motion and owner/);delete parent.enforcement.method.qualification;
 f.order.enforcement.method={family:'different',parentOrderIds:['old']};
 assert.throws(()=>validateGuardedOrder(f.root,ledger,f.order,args,[f.task]),/different-control evidence/);
 const record={schema:'rds-method-difference/v1',family:'different',decision:'MATERIALLY_DIFFERENT',reviewer:'producer',changedControl:'declared new mechanism',parentOrderIds:['old']};
 f.order.enforcement.method.differenceEvidence=f.pin('difference.json',JSON.stringify(record));
 assert.throws(()=>validateGuardedOrder(f.root,ledger,f.order,args,[f.task]),/binding invalid/);
 record.reviewer='independent';f.order.enforcement.method.differenceEvidence=f.pin('difference.json',JSON.stringify(record));assert.equal(validateGuardedOrder(f.root,ledger,f.order,args,[f.task]).enforced,true);
});
test('selected prerequisite rejects held phase stale byte and foreign source',t=>{
 const f=fixture(t),frame={status:'selected',phase:0,input:f.input},job=f.pin('job.json',JSON.stringify({frames:[frame]}));
 const p={job,frame:0,phase:0,input:f.input};f.order.enforcement.prerequisites=[p];
 const validate=()=>validateGuardedOrder(f.root,{orders:[f.order]},f.order,{taskId:f.task.id,expectedInputs:[f.input],slotIndex:0},[f.task]);
 assert.equal(validate().enforced,true);p.phase=.5;assert.throws(validate,/exact phase/);p.phase=0;
 frame.status='held';p.job=f.pin('job.json',JSON.stringify({frames:[frame]}));assert.throws(validate,/selected/);
 frame.status='selected';frame.input={...f.input,sha256:'0'.repeat(64)};p.job=f.pin('job.json',JSON.stringify({frames:[frame]}));assert.throws(validate,/source mismatch/);
 frame.input=f.input;p.job=f.pin('job.json',JSON.stringify({frames:[frame]}));fs.appendFileSync(path.join(f.root,'job.json'),' ');assert.throws(validate,/pin mismatch/);
});
test('durable accounting catches counter reset after held settlement and mismatched token',t=>{
 const f=fixture(t);f.order.callsUsed=1;f.order.slots[0]={...f.order.slots[0],status:'held',claim:{token:'once'},settlement:{token:'once'}};
 assert.doesNotThrow(()=>validateClaimAccounting(f.order));f.order.callsUsed=0;assert.throws(()=>validateClaimAccounting(f.order),/accounting/);f.order.callsUsed=1;f.order.slots[0].settlement.token='foreign';assert.throws(()=>validateClaimAccounting(f.order),/history/);
 assert.doesNotThrow(()=>validateClaimAccounting({...f.order,enforcement:undefined}));
});
test('receipt refuses old check as rerun failed check PASS still review owner rejection and local release',t=>{
 const f=fixture(t),receipt=f.receipt();assert.equal(validateTaskReceipt(f.root,receipt).valid,true);
 receipt.checks[0].executed=false;assert.throws(()=>validateTaskReceipt(f.root,receipt),/execution/);receipt.checks[0].executed=true;receipt.checks[0].exitCode=1;assert.throws(()=>validateTaskReceipt(f.root,receipt),/Nonzero/);receipt.checks[0].exitCode=0;
 receipt.motion={state:'VERIFIED',limitation:'Declared observation',observation:'loop',method:'SAMPLES_ONLY',producer:'producer',reviewer:'independent',evidence:[f.evidence]};assert.throws(()=>validateTaskReceipt(f.root,receipt),/continuous/);receipt.motion.method='CONTINUOUS_LOOP';receipt.motion.reviewer='producer';assert.throws(()=>validateTaskReceipt(f.root,receipt),/independent/);receipt.motion.reviewer='independent';
 receipt.owner={state:'VERIFIED',limitation:'Declared human reply',observation:'reply',decision:'REJECTED',humanReply:'actual reply',evidence:[f.evidence]};assert.throws(()=>validateTaskReceipt(f.root,receipt),/Owner approval/);receipt.owner.decision='APPROVED';
 receipt.release={state:'VERIFIED',limitation:'Local fixture',observation:'local test',scope:'LOCAL',evidence:[f.evidence]};assert.throws(()=>validateTaskReceipt(f.root,receipt),/public\/build/);
});
test('closure refuses unsettled claim and unknown handles; held settlement closes without refund or approval',t=>{
 const f=fixture(t),claim=f.runner.claim(f.request()),receipt=f.receipt();receipt.handles[0].id=claim.token;
 const request=()=>({expectedLedgerSHA:sha(fs.readFileSync(f.ledgerPath)),orderId:'fixture',taskId:f.task.id,receipt});
 assert.throws(()=>f.runner.close(request()),/Unresolved claim/);
 f.runner.settle({expectedLedgerSHA:claim.ledgerSHA,orderId:'fixture',slotIndex:0,token:claim.token,failure:'fixture failed; no retry'});
 receipt.handles[0].status='UNRESOLVED';assert.throws(()=>f.runner.close(request()),/Unresolved/);receipt.handles[0].status='CLOSED';
 const result=f.runner.close(request());assert.equal(result.approval,false);const order=JSON.parse(fs.readFileSync(f.ledgerPath)).orders[0];assert.equal(order.callsUsed,1);assert.equal(order.slots[0].status,'held');assert.equal(order.status,'CLOSED');assert.throws(()=>f.runner.close(request()),/OPEN guarded/);
});
test('guarded output settlement rejects other task path and closes only actual owned claim token',t=>{
 const f=fixture(t),claim=f.runner.claim(f.request()),foreign=f.pin('foreign.png','foreign returned bytes');
 const settle=output=>f.runner.settle({expectedLedgerSHA:sha(fs.readFileSync(f.ledgerPath)),orderId:'fixture',slotIndex:0,token:claim.token,output:{...output,path:path.join(f.root,output.path)}});
 assert.throws(()=>settle(foreign),/outside task ownership/);
 settle(f.pin('outputs/raw.png','owned returned bytes'));
 const request={expectedLedgerSHA:sha(fs.readFileSync(f.ledgerPath)),orderId:'fixture',taskId:f.task.id,receipt:f.receipt()};
 assert.throws(()=>f.runner.close(request),/Unresolved/);request.receipt.handles[0].id=claim.token;assert.equal(f.runner.close(request).status,'CLOSED');
});
