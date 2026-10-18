import fs from 'node:fs';
import path from 'node:path';
export const KEY_MAP=Object.freeze([{frame:0,phase:0,row:0,column:0},{frame:2,phase:.25,row:0,column:1},{frame:4,phase:.5,row:1,column:0},{frame:6,phase:.75,row:1,column:1}]);
const exact=(object,keys)=>object&&Object.keys(object).sort().join(',')===keys.sort().join(',');
const same=(a,b)=>a&&b&&a.sha256===b.sha256&&path.resolve(a.path)===path.resolve(b.path);
export function validateKeyStudyOrder(order,values,slotIndex){
 if(!order||order.jobKind!=='key-study'||order.studySchema!=='rds-key-study/v1'||order.status!=='OPEN'||order.identity!==values.identity||order.direction!==Number(values.direction)||order.action!=='walk'||values.action!=='walk')throw Error('Key study typed identity/walk/direction/status mismatch');
 if(['mirror','transform','mask','seed','api','fit','warp'].some(k=>Object.hasOwn(order,k)))throw Error('Key study unsupported transform/backend fields');
 if(order.callLimit!==1||order.callsUsed!==0||order.correctionCap!==0||order.correctionsUsed!==0)throw Error('Key study requires one initial call and zero corrections');
 if(slotIndex!==0||!Array.isArray(order.slots)||order.slots.length!==1)throw Error('Key study requires ONE request slot');
 const slot=order.slots[0];
 if(!exact(slot,['frame','phase','status','kind','template'])||slot.frame!==0||slot.phase!==0||slot.status!=='pending'||slot.kind!=='initial'||slot.template!=='key_study')throw Error('Key study request slot mismatch');
 if(JSON.stringify(order.keyMap)!==JSON.stringify(KEY_MAP))throw Error('Key study four-key mapping mismatch');
 if(values.phase!==undefined)throw Error('Key study has no single frame phase');
 return slot;
}
export function prepareKeyStudy(order,slotIndex,values,references,registry,helpers){
 validateKeyStudyOrder(order,values,slotIndex);
 if(!registry.productionOrders?.includes(order.id))throw Error('Order not registered to identity');
 const binding=helpers.validateJobBinding(order.job,registry,values);const job=JSON.parse(fs.readFileSync(binding.path));
 if(job.action!=='walk'||job.frames?.length!==8||KEY_MAP.some(k=>job.frames[k.frame]?.phase!==k.phase))throw Error('Key study actual walk job phase mismatch');
 if(references?.length!==3||references.map(r=>r.role).join(',')!=='directionalview,originalmaster,studyguide'||values.referenceRoles!=='directionalview,originalmaster,studyguide')throw Error('Key study exact ordered references required');
 const [anchor,original,guide]=references;
 const view=registry.views?.find(v=>v.direction===Number(values.direction));
 if(view?.status!=='selected'||anchor.status!==undefined&&anchor.status!=='selected'||!same(anchor,view.source)||registry.masterAuthority!=='original'||!same(original,registry.master)||original.status!==undefined&&original.status!=='selected'||values.master!==anchor.sha256)throw Error('Key study selected anchor/original mismatch');
 // Reuse camera/equipment/source exclusion guards on the selected appearance anchor.
 helpers.validatePromptReferences('key',{...values,referenceRoles:'directionalview'},[{...anchor,role:'directionalview'}],registry,{jobKind:'action',job:order.job});
 for(const pin of references){if(registry.excludedReferencePaths?.some(p=>path.resolve(p)===path.resolve(pin.path)))throw Error('Excluded study reference');helpers.validateMaster(pin);if(['held','rejected'].includes(pin.status))throw Error('Held study reference');}
 if(guide.provenance&&registry.excludedReferencePaths?.some(p=>path.resolve(p)===path.resolve(guide.provenance.path)))throw Error('Excluded study provenance');
 const registered=(registry.allowedReferences||[]).filter(r=>r.role==='studyguide'&&same(r,guide));
 if(registered.length!==1||registered[0].derivedFromSHA!==registry.master.sha256||registered[0].status!=='authoring-only'||guide.status!=='authoring-only'||!same(order.studyGuide,guide)||!same(guide.provenance,registered[0].provenance)||!same(order.studyGuide.provenance,guide.provenance))throw Error('Key study registered whole guide binding mismatch');
 helpers.validateMaster(guide.provenance);const provenance=JSON.parse(fs.readFileSync(guide.provenance.path));
 if(provenance.schema!=='rds-key-study-guide/v1'||provenance.kind!=='complete-whole-clothed-cycle'||provenance.sourcePixelUse!==false||provenance.identity!==values.identity||provenance.action!=='walk'||provenance.direction!==Number(values.direction)||!same(provenance.job,binding)||!same(provenance.input?.originalMaster,original)||!same(provenance.input?.appearance,anchor)||!same(provenance.output,guide)||JSON.stringify(provenance.keyMap)!==JSON.stringify(KEY_MAP)||JSON.stringify(provenance.cyclePhases)!==JSON.stringify(Array.from({length:8},(_,i)=>({frame:i,phase:i/8}))))throw Error('Key study structured guide provenance mismatch');
 const layout=order.studyLayout;
 if(!exact(layout,['cell','pivot','render','columns','rows'])||layout.columns!==2||layout.rows!==2||JSON.stringify(layout.cell)!==JSON.stringify(job.fixedCanvas)||JSON.stringify(layout.pivot)!==JSON.stringify(job.pivot)||JSON.stringify(layout.render)!==JSON.stringify(job.render)||JSON.stringify(provenance.layout)!==JSON.stringify(layout))throw Error('Key study identical fixed cell/pivot/scale mismatch');
 if(!exact(layout.cell,['width','height'])||!Number.isSafeInteger(layout.cell.width)||layout.cell.width<=0||layout.cell.width!==layout.cell.height||layout.cell.width!==256||layout.pivot?.space!=='source'||!['x','y'].every(k=>Number.isFinite(layout.pivot[k])&&layout.pivot[k]>=0&&layout.pivot[k]<=layout.cell.width)||!['width','height'].every(k=>Number.isFinite(layout.render[k])&&layout.render[k]>0)||layout.render.width!==layout.render.height)throw Error('Key study invalid fixed layout');
 const motion=provenance.motion;
 if(!exact(motion,['physicalA','physicalB','keys'])||!Array.isArray(motion.keys)||motion.keys.length!==4||['physicalA','physicalB'].some(k=>typeof motion[k]!=='string'||!motion[k].trim()||/[{}<>]/.test(motion[k]))||motion.physicalA===motion.physicalB)throw Error('Key study physical A/B landmark descriptions required');
 for(let i=0;i<4;i++){const k=motion.keys[i];if(!exact(k,['frame','support','swing','occlusion'])||k.frame!==KEY_MAP[i].frame||['support','swing','occlusion'].some(f=>typeof k[f]!=='string'||!k[f].trim()||/[{}<>]/.test(k[f])))throw Error('Key study four-key support/swing/occlusion descriptions required');}
 const motionBlock=`Physical A: ${motion.physicalA}; physical B: ${motion.physicalB}. `+motion.keys.map(k=>`F${k.frame}: support ${k.support}; swing ${k.swing}; occlusion ${k.occlusion}`).join('. ');
 return {prompt:helpers.renderPrompt('key_study',{...values,studyLayout:`2x2 identical ${layout.cell.width}x${layout.cell.height} source cells; fixed source pivot ${layout.pivot.x},${layout.pivot.y}; logical ${layout.render.width}x${layout.render.height}`,motionBlock,keyMapping:'upper-left F0 phase0; upper-right F2 phase0.25; lower-left F4 phase0.5; lower-right F6 phase0.75'}),referenced_image_paths:references.map(r=>path.resolve(r.path)),orderId:order.id,slotIndex,scope:'ONE candidate raw 2x2 study sheet; four cells are not accepted frames; durable claim required; no call/selection/approval'};
}
