import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {BUILDINGS} from '../shared/data.js';
const check=(ok,message)=>{if(!ok)throw Error(message);};
const same=(a,b)=>a&&b&&a.sha256===b.sha256&&path.resolve(a.path)===path.resolve(b.path);
const exact=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
export const BUILDING_FIELDS=Object.freeze(['buildingType','state','direction','phase','master','assemblyLock','invariants']);
export function buildingPin(pin){check(pin&&/^[a-f0-9]{64}$/.test(pin.sha256||''),'Building source pin required');check(createHash('sha256').update(fs.readFileSync(pin.path)).digest('hex')===pin.sha256,'Building source pin mismatch');return pin;}
export function validateBuildingOrder(order,values,slotIndex){
 check(order?.jobKind==='building-state'&&order.kind==='building'&&order.status==='OPEN'&&order.closed!==true,'Explicit OPEN building-state order required');
 check(Object.hasOwn(BUILDINGS,order.buildingType)&&['construction','hit','death','attack'].includes(order.state),'Unknown building/state');
 check(order.state!=='attack'||BUILDINGS[order.buildingType].damage>0,'Building attack requires actual damage');
 check(order.buildingType===values.buildingType&&order.state===values.state&&order.direction===null&&values.direction==='none','Building state/type/null direction mismatch');
 check(order.enforcement?.version===1&&typeof order.enforcement.taskId==='string','Building requires guarded task enforcement');
 check(Array.isArray(order.slots)&&order.slots.length===4,'Building state requires four planned slots');
 for(const [i,s] of order.slots.entries())check(s.frame===i&&s.phase===i/4&&['pending','used','held','selected'].includes(s.status)&&['initial','correction'].includes(s.kind)&&s.template==='building_key','Building slot/phase/template mismatch');
 for(const k of ['callLimit','callsUsed','correctionCap','correctionsUsed'])check(Number.isInteger(order[k])&&order[k]>=0,'Invalid building finite budget');
 check(order.callLimit<=4+order.correctionCap&&order.correctionCap<=2&&order.callsUsed<order.callLimit&&order.correctionsUsed<=order.correctionCap,'Building exhausted/invalid budget');
 const slot=order.slots[slotIndex];check(slot?.status==='pending'&&values.phase===String(slot.phase),'Building pending slot phase mismatch');
 check(slot.kind!=='correction'||order.correctionsUsed<order.correctionCap,'Building correction cap exhausted');
 return slot;
}
export function prepareBuildingOrder(order,slotIndex,values,references,registry){
 validateBuildingOrder(order,values,slotIndex);
 check(Object.keys(values).length===BUILDING_FIELDS.length&&Object.keys(values).every(k=>BUILDING_FIELDS.includes(k)),'Unexpected building prompt field');
 for(const k of BUILDING_FIELDS)check(typeof values[k]==='string'&&values[k].trim()&&!/[{}<>]|\b(TODO|PLACEHOLDER)\b/i.test(values[k]),'Invalid building prompt field');
 check(registry?.schema==='rds-building-identity/v1'&&registry.kind==='building'&&registry.buildingType===order.buildingType&&registry.masterAuthority==='original','Original building identity authority required');
 check(registry.productionOrders?.includes(order.id),'Building order not registered');
 buildingPin(registry.master);buildingPin(registry.descriptor);buildingPin(registry.assemblyLock?.source);
 check(same(registry.assemblyLock.source,registry.master)&&values.assemblyLock===registry.assemblyLock.statement&&values.master===registry.master.sha256,'Whole building assembly/master lock mismatch');
 const descriptor=JSON.parse(fs.readFileSync(registry.descriptor.path));
 check(descriptor.kind==='building'&&descriptor.direction===null&&descriptor.source?.sha256===registry.master.sha256,'Building descriptor original/kind/direction mismatch');
 const layout={family:descriptor.family,pivot:descriptor.pivot,render:descriptor.render,contactShadow:descriptor.contactShadow};
 check(typeof layout.family==='string'&&layout.family.replace(/^building\./,'')===order.buildingType,'Building descriptor family/type mismatch');
 check(typeof layout.family==='string'&&layout.family.length&&layout.pivot?.space==='source'&&[layout.pivot.x,layout.pivot.y].every(Number.isFinite)&&Number.isFinite(layout.render?.width)&&layout.render.width>0&&Number.isFinite(layout.render?.height)&&layout.render.height>0&&['baked','separate'].includes(layout.contactShadow?.mode)&&exact(registry.layout,layout),'Building descriptor/layout mismatch');
 const binding=order.job;
 check((registry.jobs||[]).filter(j=>j.id===binding?.id&&same(j,binding)).length===1,'Pinned building job not registered');buildingPin(binding);
 const job=JSON.parse(fs.readFileSync(binding.path));
 check(job.schema==='rds-building-job/v1'&&job.id===binding.id&&job.kind==='building'&&job.buildingType===order.buildingType&&job.state===order.state&&job.direction===null&&job.frameCount===4&&job.descriptorSHA===registry.descriptor.sha256&&same(job.originalMaster,registry.master)&&exact(job.layout,registry.layout),'Building job binding/layout mismatch');
 check(Array.isArray(job.frames)&&job.frames.length===4&&job.frames.every((f,i)=>f.frame===i&&f.phase===i/4&&['pending','selected','held'].includes(f.status)),'Building job frames mismatch');
 check(job.frames[slotIndex].status==='pending','Building job target not missing');
 check(Array.isArray(references)&&references.length&&references[0].role==='originalmaster'&&same(references[0],registry.master),'Building original whole master must be first');
 for(const pin of references){
  check(!(registry.excludedReferencePaths||[]).some(p=>path.resolve(p)===path.resolve(pin.path))&&!['held','rejected'].includes(pin.status),'Excluded/held building reference');buildingPin(pin);
  if(pin===references[0])continue;
  const frame=job.frames[pin.frame];check(pin.role==='neighbor'&&pin.jobId===job.id&&frame?.status==='selected'&&frame.phase===pin.phase&&same(frame.input,pin),'Building selected exact-job neighbor required');
 }
 const template=fs.readFileSync(new URL('../docs/art/pipeline/unit-production/templates/building_key.txt',import.meta.url),'utf8');
 const fields=[...template.matchAll(/\{\{(\w+)\}\}/g)].map(m=>m[1]);check(BUILDING_FIELDS.every(f=>fields.includes(f))&&fields.every(f=>BUILDING_FIELDS.includes(f)),'Building template contract mismatch');
 return {prompt:template.replace(/\{\{(\w+)\}\}/g,(_,f)=>values[f]),referenced_image_paths:references.map(p=>path.resolve(p.path)),orderId:order.id,slotIndex,scope:'Finite missing whole-building key preparation only; no call, selection, clip completion or approval'};
}
