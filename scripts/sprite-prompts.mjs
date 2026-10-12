import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {actionSpec} from '../shared/unit-action-spec.js';
const common=['identity','master','direction','camera','screenFacing','weaponOwnership','referenceRoles','invariants'];
export const TEMPLATE_FIELDS=Object.freeze({view:[...common],key:[...common,'action','phase','support','movingParts','bodyMotion','equipmentMotion','nextKey'],inbetween:[...common,'action','phase','neighbors','support','movingParts','bodyMotion','equipmentMotion','nextKey'],correction:[...common,'action','phase','defect','neighbors','movingParts','bodyMotion','equipmentMotion','nextKey'],worker_order:[...common,'action','phase','budget','ownership','movingParts','bodyMotion','equipmentMotion','nextKey']});
export function renderPrompt(kind,values){
 const fields=TEMPLATE_FIELDS[kind];if(!fields)throw Error('Unknown prompt kind');
 if(Object.keys(values).some(k=>!fields.includes(k)))throw Error('Unexpected placeholder');
 for(const field of fields)if(typeof values[field]!=='string'||!values[field].trim()||/[{}<>]|\b(TODO|PLACEHOLDER)\b/i.test(values[field]))throw Error(`Invalid placeholder: ${field}`);
 if(!actionSpec(values.identity,'idle').applicable)throw Error('Unknown identity');
 if(!/^[0-7]$/.test(values.direction))throw Error('Invalid direction');
 if(values.action&&!actionSpec(values.identity,values.action).applicable)throw Error('Action does not apply');
 const template=fs.readFileSync(new URL(`../docs/art/pipeline/unit-production/templates/${kind}.txt`,import.meta.url),'utf8');
 const placeholders=[...template.matchAll(/\{\{(\w+)\}\}/g)].map(m=>m[1]);
 if(fields.some(f=>!placeholders.includes(f))||placeholders.some(f=>!fields.includes(f)))throw Error('Template contract mismatch');
 return template.replace(/\{\{(\w+)\}\}/g,(_,key)=>values[key]);
}
export function validateMaster(pin){if(!pin||!/^([a-f0-9]{64})$/.test(pin.sha256))throw Error('Missing master pin');if(createHash('sha256').update(fs.readFileSync(pin.path)).digest('hex')!==pin.sha256)throw Error('Master pin mismatch');return true;}

export function preparePrompt(kind,values,references){
 if(!Array.isArray(references)||!references.length)throw Error('Pinned references required');
 if(!actionSpec(values.identity,'idle').applicable)throw Error('Unknown identity');
 const registry=JSON.parse(fs.readFileSync(new URL(`../docs/art/pipeline/unit-production/${values.identity}/identity.json`,import.meta.url)));
 validatePromptReferences(kind,values,references,registry);
 return renderPrompt(kind,values);
}

/** Pure reference checks; order preparation always supplies the trusted on-disk registry. */
export function validatePromptReferences(kind,values,references,registry){
 if(registry.identity!==values.identity)throw Error('Reference identity mismatch');
 if(!Array.isArray(references)||!references.length)throw Error('Pinned references required');
 const d=Number(values.direction),view=registry.views.find(v=>v.direction===d);
 if(values.camera!==registry.camera.label||values.screenFacing!==registry.camera.screenFacing[d])throw Error('Camera/facing binding mismatch');
 if(!registry.weaponOwnership||values.weaponOwnership!==registry.weaponOwnership)throw Error('Weapon ownership lock missing or mismatched');
 const same=(a,b)=>a&&b&&a.sha256===b.sha256&&path.resolve(a.path)===path.resolve(b.path);
 const primary=references[0],editing=primary.role==='edittarget';
 const anchor=editing?references[1]:primary;
 if(editing&&primary.status!==undefined&&primary.status!=='selected')throw Error('Held or unselected edit target');
 if(editing&&(!['key','correction'].includes(kind)||!anchor))throw Error('Edit target requires key/correction and appearance anchor');
 if(anchor.role==='originalmaster'){if(registry.masterAuthority!=='original'||!same(anchor,registry.master))throw Error('Original master binding mismatch');if(kind!=='view'&&registry.master.direction!==d)throw Error('Target direction requires selected matching view');}
 else if(anchor.role==='directionalview'){if(view?.status!=='selected'||!same(anchor,view.source))throw Error('Selected view binding mismatch');}
 else throw Error('Primary reference role invalid');
 if(values.master!==anchor.sha256)throw Error('Primary master binding mismatch');
 for(const pin of references){
  if(registry.excludedReferencePaths?.includes(path.resolve(pin.path)))throw Error('Excluded reference');
  validateMaster(pin);
  if(pin===anchor)continue;
  if(pin.role==='adjacentview'){const adjacent=registry.views.find(v=>v.direction===pin.direction);if(kind!=='view'||!Number.isInteger(pin.direction)||![(d+7)%8,(d+1)%8].includes(pin.direction)||adjacent?.status!=='selected'||!same(pin,adjacent.source))throw Error('Selected adjacent view binding mismatch');continue;}
  const allowed=(registry.allowedReferences||[]).find(a=>same(pin,a)&&(pin.role===a.role||pin===primary&&editing&&a.role==='neighbor'));
  if(!allowed||['held','rejected'].includes(allowed.status))throw Error('Unregistered or held reference');
  if(pin.role==='neighbor'||pin===primary&&editing){
   if(allowed.status!=='selected'||pin.frame!==allowed.frame||pin.phase!==allowed.phase||pin.jobId!==allowed.jobId)throw Error('Neighbor frame/phase/current job mismatch');
   if(editing&&pin===primary&&String(pin.phase)!==values.phase)throw Error('Edit target phase mismatch');
   validateMaster(registry.currentJob);const job=JSON.parse(fs.readFileSync(registry.currentJob.path));const frame=job.frames[pin.frame];
   if(job.id!==pin.jobId||job.direction!==d||job.action!==values.action||frame?.status!=='selected'||frame.phase!==pin.phase||!same(frame.input,pin))throw Error('Selected job neighbor mismatch');
  }else if(pin.role==='guide'){
   if(allowed.derivedFromSHA!==registry.master?.sha256||!allowed.provenance)throw Error('Guide original provenance missing');validateMaster(allowed.provenance);
  }else throw Error('Secondary reference role invalid');
 }
 if(values.referenceRoles!==references.map(p=>p.role).join(','))throw Error('Reference role listing mismatch');
 return references.map(pin=>path.resolve(pin.path));
}

/** Pure finite-slot checks; preparation still requires the trusted on-disk ledger. */
export function validateFiniteOrder(order,values,slotIndex){
 if(!order||order.status!=='OPEN'||order.identity!==values.identity||order.action!==values.action||order.direction!==Number(values.direction))throw Error('Finite order identity/action/direction/status mismatch');
 const spec=actionSpec(order.identity,order.action);
 if(!spec.applicable||!Array.isArray(order.slots)||order.slots.length!==spec.frames)throw Error('Ordered frame slots mismatch');
 for(let i=0;i<order.slots.length;i++){const slot=order.slots[i];if(slot.frame!==i||slot.phase!==i/spec.frames||!['pending','used','selected','held'].includes(slot.status))throw Error('Ordered frame/phase mismatch');}
 for(const field of ['callLimit','callsUsed','correctionCap','correctionsUsed'])if(!Number.isInteger(order[field])||order[field]<0)throw Error('Invalid finite budget');
 if(order.slots.filter(s=>s.status==='used').length>order.callsUsed)throw Error('Used slot budget mismatch');
 if(order.callLimit>spec.frames+order.correctionCap||order.correctionCap>2||order.callsUsed>=order.callLimit||order.correctionsUsed>order.correctionCap)throw Error('Exhausted or invalid finite call budget');
 const slot=order.slots[slotIndex];if(!slot||slot.status!=='pending'||values.phase!==String(slot.phase))throw Error('Slot not pending or phase mismatch');
 if(slot.kind==='correction'&&order.correctionsUsed>=order.correctionCap)throw Error('Exhausted correction cap');
 if(!['initial','correction'].includes(slot.kind))throw Error('Invalid call slot kind');
 return slot;
}
export function prepareOrder(orderId,slotIndex,kind,values,references){
 const ledger=JSON.parse(fs.readFileSync(new URL('../docs/art/pipeline/unit-production/order-ledger.json',import.meta.url)));
 const order=ledger.orders.find(o=>o.id===orderId);validateFiniteOrder(order,values,slotIndex);
 const registry=JSON.parse(fs.readFileSync(new URL(`../docs/art/pipeline/unit-production/${values.identity}/identity.json`,import.meta.url)));
 if(!registry.productionOrders?.includes(orderId))throw Error('Order not registered to identity');
 if(order.slots[slotIndex].template!==kind)throw Error('Order template slot mismatch');
 return {prompt:preparePrompt(kind,values,references),referenced_image_paths:references.map(pin=>path.resolve(pin.path)),orderId,slotIndex,scope:'Validated finite pending slot; no image call performed or budget consumed'};
}
