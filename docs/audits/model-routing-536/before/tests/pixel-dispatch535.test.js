import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {validateFiniteOrder} from '../scripts/sprite-prompts.mjs';
import {preparePixelOrder} from '../scripts/pixel-sprite-contract.mjs';
import {createOrderRunner} from '../scripts/sprite-order-run.mjs';
const sha=b=>createHash('sha256').update(b).digest('hex');
function fixture(){
 const root=fs.mkdtempSync(path.join(os.tmpdir(),'rds-pixel-dispatch535-'));
 const pin=(name,body)=>{fs.writeFileSync(path.join(root,name),body);return {path:name,sha256:sha(body)};};
 const inputs=[pin('design','New identity, no legacy pixels'),pin('style','Native128 pixel'),pin('prompt','Eight genuine whole-body phases'),pin('job',JSON.stringify({identity:'villager',action:'walk',direction:1}))];
 const task={schema:'rds-agent-task/v1',id:'new-pixel',status:'ACTIVE',purpose:'Isolated fixture, never imagegen',workKind:'image-generation',worker:{id:'/root/fixture',model:'gpt-6-luna',reasoningEffort:'high'},outputs:['raw'],slots:[{orderId:'native-pixel',slotIndex:0}],inputs};
 const order={id:'native-pixel',jobKind:'fresh-pixel',identityMode:'new-pixel-identity',status:'OPEN',identity:'villager',action:'walk',direction:1,designPin:inputs[0],stylePin:inputs[1],promptPin:inputs[2],jobPin:inputs[3],lineage:{humanScope:'pixel-rebuild-535'},slots:[{kind:'initial',template:'pixel_strip',status:'pending'}],callLimit:1,callsUsed:0,callsRemaining:1,correctionCap:0,correctionsUsed:0,enforcement:{version:1,taskId:task.id,baseline:{callsUsed:0,correctionsUsed:0},method:{family:'isolated-new-pixel-test',parentOrderIds:[]},prerequisites:[]}};
 const ledgerPath=path.join(root,'ledger.json'),taskRegistryPath=path.join(root,'tasks.json');
 fs.writeFileSync(ledgerPath,JSON.stringify({schema:'rds-unit-order-ledger/v2',orders:[order]}));fs.writeFileSync(taskRegistryPath,JSON.stringify({schema:'rds-agent-tasks/v1',tasks:[task]}));
 const runner=createOrderRunner({root,ledgerPath,taskRegistryPath,prepare:(id,index,kind,values,references)=>preparePixelOrder(order,index,kind,values,references,{root})});
 const request=()=>({expectedLedgerSHA:sha(fs.readFileSync(ledgerPath)),orderId:order.id,slotIndex:0,kind:'pixel_strip',values:{identity:'villager',action:'walk',direction:'1'},references:[],taskId:task.id,expectedInputs:inputs});
 return {root,order,runner,request,ledgerPath,dispose:()=>fs.rmSync(root,{recursive:true,force:true})};
}
test('new pixel dispatch consumes a durable call; settlement holds custody without approval',()=>{
 const f=fixture();try{
  assert.equal(validateFiniteOrder(f.order,f.request().values,0).template,'pixel_strip');
  const result=f.runner.claim(f.request());assert.equal(result.prepared.prompt,'Eight genuine whole-body phases');assert.equal(Object.hasOwn(result.prepared,'referenced_image_paths'),false);
  const ledger=JSON.parse(fs.readFileSync(f.ledgerPath));assert.equal(ledger.orders[0].callsUsed,1);assert.equal(ledger.orders[0].callsRemaining,0);assert.equal(ledger.orders[0].slots[0].claim.token,result.token);
  assert.throws(()=>f.runner.claim(f.request()));
  fs.mkdirSync(path.join(f.root,'raw'));fs.writeFileSync(path.join(f.root,'raw/output.png'),'fixture custody bytes only');
  const output={path:path.join(f.root,'raw/output.png'),sha256:sha('fixture custody bytes only')};
  const held=f.runner.settle({expectedLedgerSHA:sha(fs.readFileSync(f.ledgerPath)),orderId:f.order.id,slotIndex:0,token:result.token,output});assert.equal(held.status,'held');assert.equal(held.approval,false);
 }finally{f.dispose();}
});
test('banned legacy reference/pin drift cannot consume a new pixel call',()=>{
 const f=fixture();try{
  const before=fs.readFileSync(f.ledgerPath);assert.throws(()=>f.runner.claim({...f.request(),references:[{role:'originalmaster',path:'legacy.png'}]}));assert.deepEqual(fs.readFileSync(f.ledgerPath),before);
  fs.writeFileSync(path.join(f.root,'job'),'drift');assert.throws(()=>f.runner.claim(f.request()));assert.deepEqual(fs.readFileSync(f.ledgerPath),before);
 }finally{f.dispose();}
});
test('fresh pixel schema cannot open an old illustration order or extra values',()=>{
 const f=fixture();try{assert.throws(()=>validateFiniteOrder({...f.order,jobKind:'action'},f.request().values,0));assert.throws(()=>validateFiniteOrder(f.order,{...f.request().values,prompt:'unbound override'},0));}finally{f.dispose();}
});
