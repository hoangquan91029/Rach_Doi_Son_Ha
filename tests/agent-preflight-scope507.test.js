import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {agentPreflight} from '../scripts/agent-preflight.mjs';
const ledgerPath='docs/art/pipeline/unit-production/order-ledger.json';
function fixture(t){
 const root=fs.mkdtempSync(path.join(os.tmpdir(),'rds-scope507-'));t.after(()=>fs.rmSync(root,{recursive:true,force:true}));
 const write=(p,x)=>{fs.mkdirSync(path.dirname(path.join(root,p)),{recursive:true});fs.writeFileSync(path.join(root,p),typeof x==='string'?x:JSON.stringify(x));};
 write('source','source');write('new-job','new');write('old-job','old');
 const input={path:'source',sha256:createHash('sha256').update('source').digest('hex')};
 const task=(id,outputs,slots)=>({schema:'rds-agent-task/v1',id,status:'ACTIVE',purpose:'fixture',worker:{id,model:'gpt-6.1-sol',reasoningEffort:'low'},outputs,slots,inputs:[input]});
 const tasks=[task('new-task',['new-output'],[{orderId:'new',slotIndex:0}]),{...task('old-task',['old-output'],[{orderId:'old',slotIndex:0}]),status:'CLOSED'}];
 const order=(id,identity)=>({id,status:'OPEN',jobKind:'action',identity,action:'walk',direction:1,job:{id:id+'-job',path:id==='new'?'new-job':'old-job'},callLimit:1,callsUsed:0,correctionCap:0,correctionsUsed:0,callsRemaining:1,slots:[{status:'pending',kind:'initial'}],enforcement:{version:1,taskId:id+'-task',baseline:{callsUsed:0,correctionsUsed:0},method:{family:id+'-family',parentOrderIds:[]},prerequisites:[]}});
 const orders=[order('new','villager'),order('old','infantry')];Object.assign(orders[1],{callsUsed:1,callsRemaining:0});orders[1].slots=[{status:'used',kind:'initial',claim:{token:'retained'}}];
 write('docs/agent-read-contract.json',{schema:'rds-agent-read/v1',common:[],tasks:{art:[],audit:[]}});
 const save=()=>{write(ledgerPath,{orders});write('docs/audits/implementation-495/tasks.json',{schema:'rds-agent-tasks/v1',tasks});};save();
 execFileSync('git',['init','-q'],{cwd:root});execFileSync('git',['add','.'],{cwd:root});execFileSync('git',['-c','user.name=Fixture','-c','user.email=f@example.invalid','commit','-qm','fixture'],{cwd:root});
 const args={root,task:'art',sources:['source'],taskId:'new-task',expectedInputs:[input],orderId:'new'};
 return {root,write,orders,tasks,save,args,run:()=>agentPreflight(args)};
}
test('disjoint scoped art retains unresolved accounting and exact ledger bytes; default still refuses',t=>{const f=fixture(t),before=fs.readFileSync(path.join(f.root,ledgerPath));const r=f.run();assert.equal(r.orderScope.unrelatedUnresolvedClaims,1);assert.deepEqual(r.ledger.unresolvedClaims,[{order:'old',slot:0}]);assert.deepEqual(fs.readFileSync(path.join(f.root,ledgerPath)),before);assert.throws(()=>agentPreflight({...f.args,orderId:undefined}),/unresolved claims=1/);});
const failures=[
 ['missing task',f=>{f.args.taskId='missing';},/Active registered/],
 ['stale snapshot',f=>f.write('source','changed'),/pin mismatch/],
 ['missing enforcement',f=>delete f.orders[0].enforcement,/guarded order/],
 ['same job id',f=>{f.orders[1].job.id=f.orders[0].job.id;},/overlaps order\/job/],
 ['same physical job path',f=>{f.orders[1].job.path=path.join(f.root,'new-job');},/overlaps order\/job/],
 ['same identity action direction',f=>{f.orders[1].identity='villager';},/identity-action-direction/],
 ['same order unresolved slot',f=>{f.orders[0].callLimit=2;f.orders[0].callsUsed=1;f.orders[0].callsRemaining=1;f.orders[0].slots.push({status:'used',kind:'initial',claim:{token:'second'}});},/overlaps order\/job/],
 ['overlapping closed ownership',f=>{f.tasks[1].outputs=['new-output/nested'];},/task\/output/],
 ['overlapping active ownership',f=>{f.tasks[1].status='ACTIVE';f.tasks[1].outputs=['new-output/nested'];},/ownership overlap/],
 ['unknown claim task',f=>{f.orders[1].enforcement.taskId='missing';},/Unknown unresolved claim task/],
 ['unknown subject',f=>{delete f.orders[1].identity;},/Unknown identity/],
 ['ledger lock',f=>f.write(ledgerPath+'.lock','retained'),/lock=true/],
 ['claim accounting tamper',f=>{f.orders[1].callsUsed=0;},/accounting mismatch/],
 ['missing input snapshot',f=>{delete f.args.expectedInputs;},/Expected scoped/],
 ['closed method renamed',f=>{f.orders.push({...f.orders[1],id:'failed',status:'CLOSED',enforcement:{...f.orders[1].enforcement,method:{family:'new-family',parentOrderIds:[]}}});},/Closed method family/],
 ['invalid selected prerequisite',f=>{f.orders[0].enforcement.prerequisites=[{job:{path:'new-job',sha256:'0'.repeat(64)},frame:0,phase:0,input:{path:'source',sha256:'0'.repeat(64)}}];},/pin mismatch/],
 ['scope cannot be audit',f=>{f.args.task='audit';},/requires art/],
 ['unknown order',f=>{f.args.orderId='missing';},/guarded order/],
];
for(const [name,change,pattern] of failures)test(name+' denies scoped art',t=>{const f=fixture(t);change(f);f.save();assert.throws(f.run,pattern);});
