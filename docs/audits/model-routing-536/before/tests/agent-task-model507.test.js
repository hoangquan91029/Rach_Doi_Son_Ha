import test from 'node:test';
import assert from 'node:assert/strict';
import {validateTaskContracts} from '../scripts/agent-task-contract.mjs';
const task={schema:'rds-agent-task/v1',id:'model-policy',status:'ACTIVE',purpose:'Model policy fixture',worker:{id:'/fixture/illustrator',role:'WORKER',model:'gpt-6-luna',reasoningEffort:'high'},outputs:['docs/audits/animation-context-507/fixture-output'],slots:[],inputs:[{path:'AGENTS.md',sha256:'0'.repeat(64)}]};
const check=t=>validateTaskContracts(process.cwd(),[t]);
test('Luna High is accepted only for explicit image-generation work',()=>{
 assert.throws(()=>check(task),/Task worker/);
 assert.doesNotThrow(()=>check({...task,workKind:'image-generation'}));
 for(const workKind of ['runtime','review','image-generation '])assert.throws(()=>check({...task,workKind}),/Task worker/);
 for(const reasoningEffort of ['low','medium'])assert.throws(()=>check({...task,workKind:'image-generation',worker:{...task.worker,reasoningEffort}}),/Task worker/);
});
test('historical Sol Low contracts stay valid; no unrelated model or forged root allowed',()=>{
 assert.doesNotThrow(()=>check({...task,worker:{...task.worker,model:'gpt-6.1-sol',reasoningEffort:'low'}}));
 for(const model of ['gpt-5.6-luna','gpt-6-sol','unknown'])assert.throws(()=>check({...task,workKind:'image-generation',worker:{...task.worker,model}}),/Task worker/);
 assert.throws(()=>check({...task,workKind:'image-generation',worker:{...task.worker,id:'/root'}}),/Task worker/);
});
test('explicit Blender removal exception is restricted to the authorized task508',()=>{
 assert.doesNotThrow(()=>check({...task,id:'blender-removal508',workKind:'blender-removal'}));
 assert.throws(()=>check({...task,id:'unrelated-maintenance',workKind:'blender-removal'}),/Task worker/);
 assert.throws(()=>check({...task,id:'blender-removal508',workKind:'runtime'}),/Task worker/);
});
