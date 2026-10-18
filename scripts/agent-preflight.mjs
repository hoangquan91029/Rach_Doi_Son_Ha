import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {validateTaskSnapshot,validateGuardedOrder,validateClaimAccounting,taskPath} from './agent-task-contract.mjs';
const TASKS=['audit','art','runtime','release'];
const LEDGER='docs/art/pipeline/unit-production/order-ledger.json';
const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
export function agentPreflight({root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..'),task,sources=[],taskId,expectedInputs,orderId}={}){
 root=fs.realpathSync(root);
 if(!TASKS.includes(task))throw Error('Task must be audit, art, runtime or release');
 if(!Array.isArray(sources)||!sources.length)throw Error('At least one actual source file is required');
 function resolveInside(name){
  if(typeof name!=='string'||!name||path.isAbsolute(name))throw Error('Expected repository-relative file path');
  const lexical=path.resolve(root,name),inside=p=>p!==root&&p.startsWith(root+path.sep);
  if(!inside(lexical))throw Error('Path escapes repository');
  const actual=fs.realpathSync(lexical);
  if(!inside(actual))throw Error('Path escapes repository through symlink');
  if(!fs.statSync(actual).isFile())throw Error('Expected regular file');
  return actual;
 }
 function read(name){const actual=resolveInside(name),bytes=fs.readFileSync(actual);return {path:path.relative(root,actual).split(path.sep).join('/'),sha256:hash(bytes),bytes:bytes.length};}
 const contractPath='docs/agent-read-contract.json',contractFile=resolveInside(contractPath);
 const contract=JSON.parse(fs.readFileSync(contractFile,'utf8'));
 if(contract.schema!=='rds-agent-read/v1'||!Array.isArray(contract.common)||!contract.tasks||!Array.isArray(contract.tasks[task]))throw Error('Invalid read contract/task');
 const readFiles=[...new Set([contractPath,...contract.common,...contract.tasks[task]])].map(read);
 const sourceFiles=[...new Set(sources)].map(read);
 let assignment=null,registeredTasks;
 if(orderId&&task!=='art')throw Error('Order scope requires art task');
 if(taskId){
  const registrationPath='docs/audits/implementation-495/tasks.json';
  const registration=JSON.parse(fs.readFileSync(resolveInside(registrationPath),'utf8'));
  if(registration.schema!=='rds-agent-tasks/v1')throw Error('Invalid trusted task registration');
  registeredTasks=registration.tasks;
  const contract=validateTaskSnapshot(root,registration.tasks,taskId,expectedInputs);
  assignment={taskId,registration:read(registrationPath),inputs:contract.inputs,outputs:contract.outputs,slots:contract.slots};
 }
 const ledgerFile=resolveInside(LEDGER),ledgerBytes=fs.readFileSync(ledgerFile),ledger=JSON.parse(ledgerBytes);
 if(!Array.isArray(ledger.orders))throw Error('Invalid trusted order ledger');
 const unresolvedClaims=ledger.orders.flatMap(order=>(order.slots||[]).flatMap((slot,index)=>slot.claim&&!slot.settlement?[{order:order.id,slot:index}]:[]));
 const ledgerLocked=fs.existsSync(ledgerFile+'.lock');
 let orderScope=null;
 if(task==='art'){
  if(ledgerLocked)throw Error('Art preflight denied: ledger lock=true; never reset automatically');
  if(orderId){
   if(!assignment)throw Error('Scoped art requires registered task and input snapshot');
   const matches=ledger.orders.filter(o=>o.id===orderId),order=matches[0];
   if(matches.length!==1||order.status!=='OPEN'||!order.enforcement)throw Error('Scoped art requires unique OPEN guarded order');
   validateClaimAccounting(order);
   if(!Number.isInteger(order.callLimit)||order.callsUsed>=order.callLimit||!Number.isInteger(order.correctionCap)||order.correctionsUsed>order.correctionCap)throw Error('Scoped art finite budget unavailable');
   const slots=assignment.slots.filter(s=>s.orderId===orderId);
   if(!slots.length)throw Error('Scoped art requires exact owned order slots');
   for(const {slotIndex} of slots){
    const slot=order.slots?.[slotIndex];
    if(!slot||slot.status!=='pending'||slot.claim||slot.settlement)throw Error('Scoped slot must be pending and unclaimed');
    if(slot.kind==='correction'&&order.correctionsUsed>=order.correctionCap)throw Error('Scoped correction budget exhausted');
    validateGuardedOrder(root,ledger,order,{taskId,expectedInputs,slotIndex},registeredTasks);
   }
   const jobKey=o=>{
    if(typeof o.job?.id!=='string'||!o.job.id||typeof o.job.path!=='string')throw Error('Unknown order job scope');
    const relative=path.isAbsolute(o.job.path)?path.relative(root,o.job.path):o.job.path;
    return {id:o.job.id,path:taskPath(root,relative)};
   };
   const subject=o=>{
    if(o.jobKind==='building-state'&&typeof o.buildingType==='string'&&typeof o.state==='string'&&o.direction===null)return JSON.stringify(['building',o.buildingType,o.state,null]);
    if(typeof o.identity==='string'&&typeof o.action==='string'&&Number.isInteger(o.direction))return JSON.stringify(['unit',o.identity,o.action,o.direction]);
    throw Error('Unknown identity/action/direction scope');
   };
   const job=jobKey(order),identityActionDirection=subject(order);
   const overlap=(a,b)=>a===b||a.startsWith(b+path.sep)||b.startsWith(a+path.sep);
   for(const claim of unresolvedClaims){
    const prior=ledger.orders.find(o=>o.id===claim.order);
    validateClaimAccounting(prior);
    const priorJob=jobKey(prior);
    if(prior.id===order.id||priorJob.id===job.id||priorJob.path===job.path||subject(prior)===identityActionDirection)throw Error('Unresolved claim overlaps order/job/identity-action-direction');
    const priorTask=registeredTasks.find(t=>t.id===prior.enforcement?.taskId);
    if(!priorTask)throw Error('Unknown unresolved claim task ownership');
    if(priorTask.id===taskId||assignment.outputs.some(a=>priorTask.outputs.some(b=>overlap(taskPath(root,a),taskPath(root,b)))))throw Error('Unresolved claim overlaps task/output ownership');
   }
   orderScope={orderId,taskId,slots:slots.map(s=>s.slotIndex),unrelatedUnresolvedClaims:unresolvedClaims.length,scope:'Disjoint mechanical scope only; not image dispatch permission or custody closure'};
  }else if(unresolvedClaims.length)throw Error(`Art preflight denied: ledger lock=false, unresolved claims=${unresolvedClaims.length}; never reset automatically`);
 }

 const git=(args)=>execFileSync('git',args,{cwd:root,encoding:'utf8',stdio:['ignore','pipe','pipe']}).trimEnd();
 return {schema:'rds-agent-preflight/v1',task,head:git(['rev-parse','HEAD']),status:git(['status','--short']),readFiles,sources:sourceFiles,assignment,orderScope,ledger:{path:LEDGER,sha256:hash(ledgerBytes),locked:ledgerLocked,unresolvedClaims},limits:['Existence and byte hashes do not establish understanding, permission, approval or tool availability.','Explicit invocation only; this helper is not a mandatory global hook.','Externally verify tools and actual live handles/preservation guards; no guards are declared closed.']};
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 try{
  let task,taskId,expectedInputs,orderId;const sources=[];
  for(let i=2;i<process.argv.length;i++){const flag=process.argv[i],value=process.argv[++i];if(!value)throw Error('Missing argument');if(flag==='--task'&&!task)task=value;else if(flag==='--source')sources.push(value);else if(flag==='--task-id'&&!taskId)taskId=value;else if(flag==='--order-id'&&!orderId)orderId=value;else if(flag==='--inputs'&&!expectedInputs)expectedInputs=JSON.parse(fs.readFileSync(value));else throw Error('Usage: agent-preflight.mjs --task audit|art|runtime|release --source relative-file [--task-id id --inputs snapshot.json] [--order-id id]');}
  if(Boolean(taskId)!==Boolean(expectedInputs))throw Error('--task-id and --inputs must be supplied together');
  console.log(JSON.stringify(agentPreflight({task,sources,taskId,expectedInputs,orderId}),null,2));
 }catch(error){console.error(JSON.stringify({ok:false,error:error.message}));process.exitCode=1;}
}
