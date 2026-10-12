import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
const TASKS=['audit','art','runtime','release'];
const LEDGER='docs/art/pipeline/unit-production/order-ledger.json';
const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
export function agentPreflight({root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..'),task,sources=[]}={}){
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
 const ledgerFile=resolveInside(LEDGER),ledgerBytes=fs.readFileSync(ledgerFile),ledger=JSON.parse(ledgerBytes);
 if(!Array.isArray(ledger.orders))throw Error('Invalid trusted order ledger');
 const unresolvedClaims=ledger.orders.flatMap(order=>(order.slots||[]).flatMap((slot,index)=>slot.status==='used'&&slot.claim&&!slot.settlement?[{order:order.id,slot:index}]:[]));
 const ledgerLocked=fs.existsSync(ledgerFile+'.lock');
 if(task==='art'&&(ledgerLocked||unresolvedClaims.length))throw Error(`Art preflight denied: ledger lock=${ledgerLocked}, unresolved claims=${unresolvedClaims.length}; never reset automatically`);
 const git=(args)=>execFileSync('git',args,{cwd:root,encoding:'utf8',stdio:['ignore','pipe','pipe']}).trimEnd();
 return {schema:'rds-agent-preflight/v1',task,head:git(['rev-parse','HEAD']),status:git(['status','--short']),readFiles,sources:sourceFiles,ledger:{path:LEDGER,sha256:hash(ledgerBytes),locked:ledgerLocked,unresolvedClaims},limits:['Existence and byte hashes do not establish understanding, permission, approval or tool availability.','Explicit invocation only; this helper is not a mandatory global hook.','Externally verify tools and actual live handles/preservation guards; no guards are declared closed.']};
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 try{
  let task;const sources=[];
  for(let i=2;i<process.argv.length;i++){const flag=process.argv[i],value=process.argv[++i];if(!value)throw Error('Missing argument');if(flag==='--task'&&!task)task=value;else if(flag==='--source')sources.push(value);else throw Error('Usage: agent-preflight.mjs --task audit|art|runtime|release --source relative-file [--source relative-file]');}
  console.log(JSON.stringify(agentPreflight({task,sources}),null,2));
 }catch(error){console.error(JSON.stringify({ok:false,error:error.message}));process.exitCode=1;}
}
