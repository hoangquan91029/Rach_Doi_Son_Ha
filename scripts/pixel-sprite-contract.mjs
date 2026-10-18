import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
const hash=b=>createHash('sha256').update(b).digest('hex');
const assert=(ok,m)=>{if(!ok)throw Error(`Pixel order: ${m}`);};
export function validatePixelOrder(order,values,slotIndex){
 assert(order?.jobKind==='fresh-pixel'&&order.status==='OPEN'&&order.identityMode==='new-pixel-identity','typed fresh identity required');
 assert(Object.keys(values).sort().join(',')==='action,direction,identity','exact bound values');
 assert(order.identity===values.identity&&order.action===values.action&&order.direction===Number(values.direction),'binding');
 assert(/^[a-z][a-z0-9_-]*$/.test(order.identity)&&['idle','walk','chop_tree'].includes(order.action)&&Number.isInteger(order.direction)&&order.direction>=0&&order.direction<8,'pilot scope');
 assert(order.enforcement&&order.designPin&&order.stylePin&&order.promptPin&&order.jobPin&&order.lineage?.humanScope==='pixel-rebuild-535','root pins/enforcement/lineage');
 assert(Array.isArray(order.slots)&&order.slots.length>=1&&order.slots.length<=3,'finite slots');
 assert(order.slots.every((s,i)=>s.template==='pixel_strip'&&s.kind===(i===0?'initial':'correction')&&['pending','used','held','selected'].includes(s.status)),'slot kind');
 for(const k of ['callsUsed','callLimit','correctionCap','correctionsUsed'])assert(Number.isInteger(order[k])&&order[k]>=0,'budget integer');
 assert(order.callLimit===order.slots.length&&order.correctionCap===order.slots.length-1&&order.correctionCap<=2&&order.callsUsed<order.callLimit&&order.correctionsUsed<=order.correctionCap,'budget');
 const consumed=order.slots.filter(s=>s.status!=='pending');assert(consumed.length===order.callsUsed&&consumed.filter(s=>s.kind==='correction').length===order.correctionsUsed,'custody accounting');
 const slot=order.slots[slotIndex];assert(Number.isInteger(slotIndex)&&slot?.status==='pending'&&order.slots.slice(0,slotIndex).every(s=>s.status==='held'),'pending slot / correction predecessor');
 return slot;
}
export function preparePixelOrder(order,slotIndex,kind,values,references,{root=process.cwd()}={}){
 validatePixelOrder(order,values,slotIndex);assert(kind==='pixel_strip','template');assert(Array.isArray(references)&&references.length===0,'fresh pilot must have no legacy references');
 const readPin=pin=>{assert(pin&&typeof pin.path==='string'&&/^[a-f0-9]{64}$/.test(pin.sha256),'pin');const base=fs.realpathSync(root),file=fs.realpathSync(path.resolve(root,pin.path));assert(file.startsWith(base+path.sep),'pin outside root');const bytes=fs.readFileSync(file);assert(hash(bytes)===pin.sha256,'pin hash mismatch');return bytes.toString('utf8');};
 const design=readPin(order.designPin),style=readPin(order.stylePin),prompt=readPin(order.promptPin),job=JSON.parse(readPin(order.jobPin));
 assert(job.identity===order.identity&&job.action===order.action&&job.direction===order.direction,'job binding');
 assert(design.trim()&&style.trim()&&prompt.trim(),'empty design/style/prompt');
 return {prompt,orderId:order.id,slotIndex,transparent_background:true,scope:'Fresh pixel finite pending strip; no call consumed or approval',pixel:{schema:'rds-pixel-request/v1',identity:order.identity,action:order.action,direction:order.direction,width:1024,height:128,cellSize:128,frames:8,designPin:order.designPin,stylePin:order.stylePin,promptPin:order.promptPin,jobPin:order.jobPin}};
}
