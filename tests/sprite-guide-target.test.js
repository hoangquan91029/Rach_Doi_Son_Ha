import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {prepareOrderWithRegistry,validatePromptReferences,TEMPLATE_FIELDS} from '../scripts/sprite-prompts.mjs';
import {createOrderRunner} from '../scripts/sprite-order-run.mjs';
const sha=bytes=>createHash('sha256').update(bytes).digest('hex');
function fixture(t){
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'guide492-'));t.after(()=>fs.rmSync(dir,{recursive:true,force:true}));
 const pin=(name,bytes)=>{const p=path.join(dir,name);fs.writeFileSync(p,bytes);return {path:p,sha256:sha(bytes)};};
 const master={...pin('original.png','original fixture'),direction:0},appearance=pin('south.png','appearance fixture'),output=pin('guide.png','clothed authoring fixture');
 const job={id:'walk492',action:'walk',direction:1,variant:'controlled',...pin('job.json',JSON.stringify({id:'walk492',action:'walk',direction:1,variant:'controlled',frames:Array.from({length:8},(_,frame)=>({phase:frame/8,status:'pending'}))}))};
 const provenanceData={schema:'rds-guide-target/v1',kind:'whole-clothed-authoring',identity:'villager',action:'walk',direction:1,jobId:job.id,frame:2,phase:.25,input:{originalMaster:master,appearance},output,sourcePixelUse:false};
 const provenance=pin('provenance.json',JSON.stringify(provenanceData));
 const guide={...output,role:'guidetarget',status:'authoring-only',jobId:job.id,frame:2,phase:.25,provenance};
 const registry={identity:'villager',masterAuthority:'original',master,camera:{label:'fixed camera',screenFacing:['ESE','South']},weaponOwnership:'original physical equipment',views:[{direction:1,status:'selected',source:appearance}],jobs:[job],productionOrders:['guide492'],allowedReferences:[{...guide,derivedFromSHA:master.sha256}]};
 const order={id:'guide492',identity:'villager',jobKind:'action',action:'walk',direction:1,status:'OPEN',referenceMode:'guide-first',job,poseGuide:guide,callLimit:1,callsUsed:0,correctionCap:0,correctionsUsed:0,slots:Array.from({length:8},(_,frame)=>({frame,phase:frame/8,status:frame===2?'pending':'selected',kind:'initial',template:'guide_key'}))};
 const values=Object.fromEntries(TEMPLATE_FIELDS.guide_key.map(k=>[k,'verified fixture']));Object.assign(values,{identity:'villager',action:'walk',direction:'1',phase:'0.25',master:appearance.sha256,camera:registry.camera.label,screenFacing:'South',weaponOwnership:registry.weaponOwnership,referenceRoles:'guidetarget,directionalview'});
 const refs=[guide,{...appearance,role:'directionalview'}];
 const prepare=(o=order,r=refs,reg=registry,v=values,k='guide_key')=>prepareOrderWithRegistry(o,2,k,v,r,reg);
 return {dir,pin,master,appearance,provenanceData,guide,registry,order,values,refs,prepare};
}
test('guide-first binds source bytes, appearance second, exact typed job and durable claim once',t=>{
 const f=fixture(t);assert.deepEqual(TEMPLATE_FIELDS.guide_key,TEMPLATE_FIELDS.key);assert.deepEqual(f.prepare().referenced_image_paths,f.refs.map(r=>r.path));
 const ledgerPath=path.join(f.dir,'ledger.json');fs.writeFileSync(ledgerPath,JSON.stringify({schema:'rds-unit-order-ledger/v2',orders:[f.order]}));
 const runner=createOrderRunner({ledgerPath,prepare:(id,slot,kind,v,r)=>prepareOrderWithRegistry(JSON.parse(fs.readFileSync(ledgerPath)).orders.find(o=>o.id===id),slot,kind,v,r,f.registry)});
 const request=()=>({expectedLedgerSHA:sha(fs.readFileSync(ledgerPath)),orderId:f.order.id,slotIndex:2,kind:'guide_key',values:f.values,references:f.refs});
 const claim=runner.claim(request());assert.ok(claim.token);assert.equal(JSON.parse(fs.readFileSync(ledgerPath)).orders[0].callsUsed,1);assert.throws(()=>runner.claim(request()),/Exhausted|pending/);
 runner.settle({expectedLedgerSHA:sha(fs.readFileSync(ledgerPath)),orderId:f.order.id,slotIndex:2,token:claim.token,failure:'isolated fixture, no image dispatch'});
 const closed=JSON.parse(fs.readFileSync(ledgerPath));closed.orders[0].status='CLOSED';fs.writeFileSync(ledgerPath,JSON.stringify(closed));assert.throws(()=>runner.claim(request()),/status/);assert.equal(fs.existsSync(ledgerPath+'.lock'),false);
});
test('guide target refuses no order, legacy key, wrong mode, arbitrary primary, held and unpinned metadata',t=>{
 const f=fixture(t);
 assert.throws(()=>validatePromptReferences('guide_key',f.values,f.refs,f.registry),/OPEN typed/);
 for(const referenceMode of [undefined,'target-first'])assert.throws(()=>f.prepare({...f.order,referenceMode}),/OPEN typed/);
 assert.throws(()=>f.prepare({...f.order,slots:f.order.slots.map(s=>({...s,template:'key'}))},f.refs,f.registry,f.values,'key'),/OPEN typed/);
 for(const patch of [{role:'guide'},{role:'edittarget',status:'held'},{role:'originalmaster'}])assert.throws(()=>f.prepare(f.order,[{...f.guide,...patch},f.refs[1]]),/Guide target/);
 for(const patch of [{status:'held'},{status:'rejected'},{jobId:'foreign'},{frame:6},{phase:.75},{provenance:undefined}])assert.throws(()=>f.prepare(f.order,[{...f.guide,...patch},f.refs[1]]),/Guide target/);
 for(const patch of [{status:'held'},{status:'selected'},{derivedFromSHA:'0'.repeat(64)},{jobId:'foreign'},{frame:6},{phase:.75},{provenance:undefined}])assert.throws(()=>f.prepare(f.order,f.refs,{...f.registry,allowedReferences:[{...f.registry.allowedReferences[0],...patch}]}),/Guide target/);
 assert.throws(()=>f.prepare(f.order,f.refs,{...f.registry,excludedReferencePaths:[f.guide.path]}),/Excluded/);
 assert.throws(()=>f.prepare(f.order,f.refs,{...f.registry,views:[{direction:1,status:'held',source:f.appearance}]}),/Selected view/);
 assert.throws(()=>f.prepare({...f.order,poseGuide:{...f.guide,frame:6}}),/Guide target/);
 assert.throws(()=>f.prepare(f.order,f.refs,f.registry,{...f.values,direction:'0'}),/direction/);
});
test('structured provenance checks every source and scope without asserting visual design truth',t=>{
 const f=fixture(t);
 const check=data=>{const provenance=f.pin('variant.json',JSON.stringify(data)),guide={...f.guide,provenance};return f.prepare({...f.order,poseGuide:guide},[guide,f.refs[1]],{...f.registry,allowedReferences:[{...f.registry.allowedReferences[0],provenance}]});};
 for(const patch of [{schema:'legacy'},{kind:'cutout'},{sourcePixelUse:true},{identity:'infantry'},{action:'attack'},{direction:0},{jobId:'foreign'},{frame:6},{phase:.75},{input:{originalMaster:f.appearance,appearance:f.appearance}},{input:{originalMaster:f.master,appearance:f.master}},{output:f.master}])assert.throws(()=>check({...f.provenanceData,...patch}),/provenance/);
 for(const p of [f.master.path,f.appearance.path,f.guide.path,f.guide.provenance.path]){const original=fs.readFileSync(p);fs.appendFileSync(p,'changed');assert.throws(()=>f.prepare(),/pin mismatch/);fs.writeFileSync(p,original);}
 assert.ok(f.prepare().prompt);
});
