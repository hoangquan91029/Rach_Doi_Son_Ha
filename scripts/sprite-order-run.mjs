import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash,randomUUID} from 'node:crypto';
import {prepareOrder,validateFiniteOrder,validateMaster} from './sprite-prompts.mjs';
const trustedLedger=fileURLToPath(new URL('../docs/art/pipeline/unit-production/order-ledger.json',import.meta.url));
const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
/** Dependency injection is for isolated fixtures. Production CLI never accepts a ledger or preparer override. */
export function createOrderRunner({ledgerPath=trustedLedger,prepare=prepareOrder}={}){
 const mutate=(expectedLedgerSHA,action)=>{
  if(!/^[a-f0-9]{64}$/.test(expectedLedgerSHA||''))throw Error('Expected ledger SHA required');
  const lock=ledgerPath+'.lock';let fd;
  try{fd=fs.openSync(lock,'wx',0o600);}catch(e){if(e.code==='EEXIST')throw Error('Ledger locked; no automatic retry or stale reset');throw e;}
  let temp;
  try{
   const raw=fs.readFileSync(ledgerPath);if(hash(raw)!==expectedLedgerSHA)throw Error('Ledger SHA mismatch');
   const ledger=JSON.parse(raw);if(ledger.schema!=='rds-unit-order-ledger/v2'||!Array.isArray(ledger.orders))throw Error('Unsupported ledger schema');
   const result=action(ledger);const bytes=JSON.stringify(ledger,null,2)+'\n';
   temp=ledgerPath+'.'+randomUUID()+'.tmp';const out=fs.openSync(temp,'wx',fs.statSync(ledgerPath).mode&0o777);
   try{fs.writeFileSync(out,bytes);fs.fsyncSync(out);}finally{fs.closeSync(out);}
   fs.renameSync(temp,ledgerPath);temp=null;const dir=fs.openSync(path.dirname(ledgerPath),'r');try{fs.fsyncSync(dir);}finally{fs.closeSync(dir);}
   return {...result,ledgerSHA:hash(bytes)};
  }finally{if(temp&&fs.existsSync(temp))fs.unlinkSync(temp);fs.closeSync(fd);fs.unlinkSync(lock);}
 };
 return {
  claim({expectedLedgerSHA,orderId,slotIndex,kind,values,references}){return mutate(expectedLedgerSHA,ledger=>{
   const order=ledger.orders.find(o=>o.id===orderId),slot=validateFiniteOrder(order,values,slotIndex);
   if(slot.template!==kind)throw Error('Order template slot mismatch');
   const prepared=prepare(orderId,slotIndex,kind,values,references);
   const token=randomUUID(),requestSHA=hash(JSON.stringify({kind,values,references,prompt:prepared.prompt}));
   slot.status='used';slot.claim={token,requestSHA,claimedAt:new Date().toISOString()};order.callsUsed++;if(slot.kind==='correction')order.correctionsUsed++;
   order.callsRemaining=order.callLimit-order.callsUsed;
   return {token,orderId,slotIndex,requestSHA,prepared,scope:'Durable consumed claim; no dispatch, retry, selection or approval'};
  });},
  settle({expectedLedgerSHA,orderId,slotIndex,token,output,failure}){return mutate(expectedLedgerSHA,ledger=>{
   const order=ledger.orders.find(o=>o.id===orderId),slot=order?.slots?.[slotIndex];
   if(!token||slot?.status!=='used'||slot.claim?.token!==token)throw Error('Claim token/order/slot mismatch or already settled');
   if(Boolean(output)===Boolean(failure))throw Error('Exactly one output or failure required');
   if(output)validateMaster(output);else if(typeof failure!=='string'||!failure.trim())throw Error('Failure description required');
   slot.status='held';slot.settlement={token,settledAt:new Date().toISOString(),...(output?{output:{path:path.resolve(output.path),sha256:output.sha256}}:{failure}),approval:false};
   return {orderId,slotIndex,status:'held',approval:false,scope:'Custody only; selection requires separate review'};
  });}
 };
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 try{const [operation,requestPath,...extra]=process.argv.slice(2);if(!['claim','settle'].includes(operation)||!requestPath||extra.length)throw Error('Usage: sprite-order-run.mjs claim|settle request.json');
  const request=JSON.parse(fs.readFileSync(requestPath));if('ledgerPath'in request||'prepare'in request)throw Error('CLI trusted ledger cannot be overridden');console.log(JSON.stringify(createOrderRunner()[operation](request),null,2));
 }catch(error){console.error(error.message);process.exitCode=1;}
}
