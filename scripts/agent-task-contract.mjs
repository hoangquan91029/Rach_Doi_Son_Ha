import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
const requireValue=(ok,message)=>{if(!ok)throw Error(message);};
const sha=bytes=>createHash('sha256').update(bytes).digest('hex');
const text=value=>typeof value==='string'&&Boolean(value.trim());

/** Resolve existing ancestors too: nonexistent outputs cannot bypass symlink ownership. */
export function taskPath(root,name){
 root=fs.realpathSync(root);
 requireValue(text(name)&&!path.isAbsolute(name),'Task paths must be repository-relative');
 const lexical=path.resolve(root,name),inside=p=>p!==root&&p.startsWith(root+path.sep);
 requireValue(inside(lexical),'Task path escapes repository');
 let ancestor=lexical;const tail=[];
 while(!fs.existsSync(ancestor)){tail.unshift(path.basename(ancestor));ancestor=path.dirname(ancestor);}
 const actual=path.join(fs.realpathSync(ancestor),...tail);
 requireValue(inside(actual),'Task path escapes repository through symlink');
 return actual;
}
export function taskPin(root,pin){
 requireValue(pin&&/^[a-f0-9]{64}$/.test(pin.sha256||''),'Task input SHA required');
 const actual=taskPath(root,pin.path);
 requireValue(fs.statSync(actual).isFile(),'Task pin must be a regular file');
 requireValue(sha(fs.readFileSync(actual))===pin.sha256,'Task input pin mismatch');
 return actual;
}
export function validateOwnedOutput(root,task,outputPath){
 const absolute=path.resolve(outputPath),relative=path.relative(fs.realpathSync(root),absolute);
 const output=taskPath(root,relative);
 requireValue(task.outputs.some(name=>{const owned=taskPath(root,name);return output===owned||output.startsWith(owned+path.sep);}),'Output outside task ownership');
 return output;
}
const overlaps=(a,b)=>a===b||a.startsWith(b+path.sep)||b.startsWith(a+path.sep);
/** Root registers records in its trusted task index. Validation never writes registration. */
export function validateTaskContracts(root,contracts){
 requireValue(Array.isArray(contracts),'Task contracts must be an array');
 const ids=new Set(),active=[];
 for(const contract of contracts){
  requireValue(contract?.schema==='rds-agent-task/v1'&&text(contract.id)&&!ids.has(contract.id),'Invalid or duplicate task contract');ids.add(contract.id);
  requireValue(['ACTIVE','CLOSED'].includes(contract.status)&&text(contract.purpose),'Task status/purpose required');
  const worker=contract.worker;
  requireValue(text(worker?.id),'Task worker identity required');
  if(worker.role==='ROOT')requireValue(worker.id==='/root'&&worker.model===null&&worker.reasoningEffort===null,'Root metadata must be /root with unknown model/effort');
  else requireValue((worker.role===undefined||worker.role==='WORKER')&&worker.id!=='/root'&&worker.model==='gpt-6.1-sol'&&worker.reasoningEffort==='low','Task worker must be gpt-6.1-sol/low');
  requireValue(Array.isArray(contract.outputs)&&contract.outputs.length&&Array.isArray(contract.slots)&&Array.isArray(contract.inputs)&&contract.inputs.length,'Task outputs/slots/inputs required');
  const outputs=contract.outputs.map(name=>taskPath(root,name));
  requireValue(new Set(outputs).size===outputs.length,'Duplicate task output');
  const slots=contract.slots.map(s=>{requireValue(text(s?.orderId)&&Number.isInteger(s.slotIndex)&&s.slotIndex>=0,'Invalid owned slot');return JSON.stringify([s.orderId,s.slotIndex]);});
  requireValue(new Set(slots).size===slots.length,'Duplicate task slot');
  for(const pin of contract.inputs)requireValue(pin&&text(pin.path)&&/^[a-f0-9]{64}$/.test(pin.sha256||''),'Invalid task input pin');
  requireValue(new Set(contract.inputs.map(p=>taskPath(root,p.path))).size===contract.inputs.length,'Duplicate task input');
  if(contract.status==='ACTIVE'){
   for(const prior of active){requireValue(!outputs.some(a=>prior.outputs.some(b=>overlaps(a,b))),'Active task output ownership overlap');requireValue(!slots.some(s=>prior.slots.includes(s)),'Active task slot ownership overlap');}
   active.push({outputs,slots});
  }
 }
 return contracts;
}
export function validateTaskSnapshot(root,contracts,taskId,expectedInputs){
 validateTaskContracts(root,contracts);
 const task=contracts.find(c=>c.id===taskId);
 requireValue(task?.status==='ACTIVE','Active registered task required');
 requireValue(Array.isArray(expectedInputs)&&expectedInputs.length===task.inputs.length,'Expected scoped task inputs required');
 const normalized=p=>JSON.stringify([taskPath(root,p.path),p.sha256]);
 requireValue(new Set(expectedInputs.map(normalized)).size===expectedInputs.length&&task.inputs.every(p=>expectedInputs.some(q=>normalized(p)===normalized(q))),'Scoped task snapshot mismatch');
 task.inputs.forEach(pin=>taskPin(root,pin));
 return task;
}
export function validateGuardedOrder(root,ledger,order,{taskId,expectedInputs,slotIndex},contracts=ledger.taskContracts){
 const gate=order.enforcement;
 if(!gate)return {enforced:false,scope:'Legacy order; no task/lineage/prerequisite enforcement'};
 requireValue(gate.version===1&&taskId===gate.taskId,'Guarded order task/version mismatch');
 const task=validateTaskSnapshot(root,contracts,taskId,expectedInputs);
 requireValue(task.slots.some(s=>s.orderId===order.id&&s.slotIndex===slotIndex),'Slot outside task ownership');
 validateClaimAccounting(order);
 const method=gate.method;
 requireValue(text(method?.family)&&Array.isArray(method.parentOrderIds),'Method lineage required');
 requireValue(new Set(method.parentOrderIds).size===method.parentOrderIds.length&&!method.parentOrderIds.includes(order.id),'Invalid method parents');
 // Closed custody is not qualification. A root-pinned qualification receipt is
 // required before reusing the same family after closure.
 const failed=parent=>parent.status!=='OPEN'&&!parent.enforcement?.method?.qualification;
 const parents=method.parentOrderIds.map(id=>{const parent=ledger.orders.find(o=>o.id===id);requireValue(parent,'Missing method parent');return parent;});
 for(const previous of ledger.orders.filter(o=>o.enforcement?.method?.qualification&&(o.enforcement.method.family===method.family||method.parentOrderIds.includes(o.id)))){
  const qualification=JSON.parse(fs.readFileSync(taskPin(root,previous.enforcement.method.qualification)));
  validateTaskReceipt(root,qualification);
  requireValue(qualification.taskId===previous.enforcement.taskId&&qualification.motion.state==='VERIFIED'&&qualification.owner.state==='VERIFIED','Method qualification requires bound motion and owner evidence');
 }
 requireValue(!ledger.orders.some(o=>o.id!==order.id&&o.enforcement?.method?.family===method.family&&failed(o)),'Closed method family cannot reopen under renamed order');
 if(parents.some(failed)){
  const evidence=method.differenceEvidence;requireValue(evidence,'Failed parent requires different-control evidence');
  const record=JSON.parse(fs.readFileSync(taskPin(root,evidence)));
  requireValue(record.schema==='rds-method-difference/v1'&&record.family===method.family&&record.decision==='MATERIALLY_DIFFERENT'&&text(record.reviewer)&&record.reviewer!==task.worker.id&&text(record.changedControl)&&Array.isArray(record.parentOrderIds)&&record.parentOrderIds.length===method.parentOrderIds.length&&method.parentOrderIds.every(id=>record.parentOrderIds.includes(id)),'Different-control evidence binding invalid');
 }
 requireValue(Array.isArray(gate.prerequisites),'Selected prerequisites required');
 for(const prerequisite of gate.prerequisites){
  const job=JSON.parse(fs.readFileSync(taskPin(root,prerequisite.job))),frame=job.frames?.[prerequisite.frame];
  requireValue(Number.isInteger(prerequisite.frame)&&frame?.status==='selected'&&frame.phase===prerequisite.phase,'Prerequisite frame must be selected at exact phase');
  const input=taskPin(root,prerequisite.input);
  const jobBase=path.dirname(taskPath(root,prerequisite.job.path));
  requireValue(frame.input&&path.resolve(jobBase,frame.input.path)===input&&frame.input.sha256===prerequisite.input.sha256,'Selected prerequisite source mismatch');
 }
 return {enforced:true,task};
}
export function validateClaimAccounting(order){
 if(!order.enforcement)return;
 const baseline=order.enforcement.baseline;
 requireValue(baseline&&['callsUsed','correctionsUsed'].every(k=>Number.isInteger(baseline[k])&&baseline[k]>=0),'Guarded baseline counts required');
 const claims=(order.slots||[]).filter(s=>s.claim);
 requireValue(new Set(claims.map(s=>s.claim.token)).size===claims.length&&claims.every(s=>text(s.claim.token)&&['used','held','selected'].includes(s.status)&&(!s.settlement||s.settlement.token===s.claim.token)),'Invalid durable claim history');
 requireValue(order.callsUsed===baseline.callsUsed+claims.length&&order.correctionsUsed===baseline.correctionsUsed+claims.filter(s=>s.kind==='correction').length,'Durable claim budget accounting mismatch');
 requireValue(order.callsRemaining===undefined||order.callsRemaining===order.callLimit-order.callsUsed,'Remaining call budget mismatch');
}
/** Checks declared evidence relationships. Cannot authenticate observation or human prose. */
export function validateTaskReceipt(root,receipt){
 requireValue(receipt?.schema==='rds-agent-receipt/v1'&&text(receipt.taskId),'Task receipt schema/id required');
 requireValue(Array.isArray(receipt.checks)&&Array.isArray(receipt.handles),'Receipt checks/handles required');
 const pins=value=>{requireValue(Array.isArray(value)&&value.length,'Evidence pins required');value.forEach(p=>taskPin(root,p));};
 for(const check of receipt.checks){
  requireValue(text(check.command)&&path.isAbsolute(check.cwd)&&text(check.method)&&['VERIFIED','DOCUMENTED_ONLY','FAILED','UNKNOWN'].includes(check.state),'Check command/cwd/method/state required');
  if(check.state==='VERIFIED'||check.state==='FAILED')requireValue(check.executed===true&&Number.isInteger(check.exitCode)&&text(check.observation),'Observed check execution required');
  if(check.state==='VERIFIED')requireValue(check.exitCode===0,'Nonzero check cannot be VERIFIED');
  if(check.state!=='UNKNOWN')pins(check.evidence);
 }
 for(const name of ['technical','motion','runtime','owner','release']){
  const stage=receipt[name];requireValue(stage&&['VERIFIED','DOCUMENTED_ONLY','INFERRED','PROPOSED','UNKNOWN','FAILED'].includes(stage.state)&&text(stage.limitation),'Separate evidence stage/limitation required');
  if(stage.state==='VERIFIED'){
   pins(stage.evidence);requireValue(text(stage.observation),'Verified stage observation required');
   if(name==='motion')requireValue(stage.method==='CONTINUOUS_LOOP'&&text(stage.reviewer)&&text(stage.producer)&&stage.reviewer!==stage.producer,'Motion requires independent continuous review');
   if(name==='owner')requireValue(text(stage.humanReply)&&stage.decision==='APPROVED','Owner approval requires explicit human reply binding');
   if(name==='release')requireValue(stage.scope==='PUBLIC'&&text(stage.url)&&text(stage.buildSHA)&&text(stage.backendPin)&&text(stage.rollbackPin),'Release requires scoped public/build/backend/rollback evidence');
  }
 }
 for(const handle of receipt.handles)requireValue(text(handle.id)&&['CLOSED','UNRESOLVED','INTENTIONALLY_RUNNING'].includes(handle.status)&&text(handle.observation),'Handle state/observation required');
 return {valid:true,limits:['Declared custody and mechanical scope only; no authenticity, comprehension, observation or permission guarantee.']};
}
