#!/usr/bin/env node
/** Deterministic whole-entry catalog/compiler. Nothing writes without --output. */
import {readFile,writeFile,mkdir,realpath} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {ART_ROUTES} from '../client/art-routes.js';
import {validateAsset,validateManifest} from '../client/art-assets.js';
import {UNITS,BUILDINGS,CHARACTERS,MAPS} from '../shared/data.js';
const rootDefault=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const hash=b=>createHash('sha256').update(b).digest('hex');
const clone=v=>JSON.parse(JSON.stringify(v));
const canonical=v=>JSON.stringify(v&&typeof v==='object'?Array.isArray(v)?v.map(x=>JSON.parse(canonical(x))):Object.fromEntries(Object.keys(v).sort().map(k=>[k,JSON.parse(canonical(v[k]))])):v);
const SHA=/^[a-f0-9]{64}$/i;
function safePath(value,{absolute=false}={}){
 if(typeof value!=='string'||!value||value.includes('\\')||value.includes('\0')||value.includes('?')||value.includes('#')||value.includes('%')||value.split('/').some(p=>p==='..'||p==='.')||/^[a-z]+:/i.test(value)||(!absolute&&value.startsWith('/')))throw Error(`Unsafe asset path: ${value}`);
 return value;
}
function custodyPath(value,roots){
 if(typeof value==='string'&&value.startsWith('../../../docs/art/'))return safePath(value.slice('../../../docs/art/'.length));
 safePath(value,{absolute:true});if(value.startsWith('/')&&!roots.some(root=>value.startsWith(path.resolve(root)+path.sep)))throw Error(`Source custody outside authoring roots: ${value}`);
 return value;
}
function validateEntry(a,custodyRoots=[path.join(rootDefault,'docs/art')]){
 validateAsset(a);safePath(a.runtime.path);custodyPath(a.source.path,custodyRoots);
 for(const f of a.frames)if(f.source)custodyPath(f.source.path,custodyRoots);
 if(!SHA.test(a.source.sha256)||!SHA.test(a.runtime.sha256))throw Error(`Missing hashes: ${a.id}`);
 return a;
}
export function createCatalog(manifests,{ownerEvidence=[],custodyRoots=[path.join(rootDefault,'docs/art')]}={}){
 const definitions={},recipes={};
 for(const [route,manifest] of Object.entries(manifests)){
  if(!Object.hasOwn(ART_ROUTES,route))throw Error(`Unknown route: ${route}`);
  validateManifest(manifest);const {assets,...header}=clone(manifest);const ids=[];
  for(const asset of assets){validateEntry(asset,custodyRoots);const entrySHA256=hash(canonical(asset)),existing=definitions[asset.id];
   if(existing&&existing.entrySHA256!==entrySHA256)throw Error(`Conflicting asset ID: ${asset.id}`);
   if(!existing)definitions[asset.id]={asset:clone(asset),entrySHA256,mappingKey:JSON.stringify([asset.kind,asset.family||asset.id,asset.state,asset.direction,asset.runtime.sha256]),acceptance:{manifestDeclaration:clone(asset.review),candidate:asset.candidate,ownerEvidence:ownerEvidence.filter(e=>e.action===asset.state&&e.engineDirection===asset.direction&&asset.family==='unit.villager'),release:{status:'NOT_ESTABLISHED'}}};
   ids.push(asset.id);
  }
  recipes[route]={manifestUrl:ART_ROUTES[route].manifestUrl,header,assetIds:ids};
 }
 return {schema:'rds-art-catalog/v1',custodyRoots:[...custodyRoots],definitions,recipes,portraitDependencies:{},scopePolicy:'Map-scoped world assets are conservative: existing terrain/props retained for either map; no new map-specific art or missing animations manufactured.'};
}
export async function loadCatalog({root=rootDefault,verifyRuntime=true}={}){
 const manifests={};for(const [route,recipe] of Object.entries(ART_ROUTES))manifests[route]=JSON.parse(await readFile(path.join(root,'public',recipe.manifestUrl.slice(1))));
 const ownerEvidence=[];
 for(const receipt of ['docs/art/pipeline/owner-motion-review-032/review.json','docs/art/pipeline/owner-iron-motion-review-141/review.json']){
  const r=JSON.parse(await readFile(path.join(root,receipt))),subject=await readFile(path.join(root,r.subject.path));
  if(hash(subject)!==r.subject.sha256)throw Error(`Owner evidence subject hash mismatch: ${receipt}`);
  ownerEvidence.push({receipt,receiptSHA256:hash(await readFile(path.join(root,receipt))),subjectSHA256:r.subject.sha256,action:r.subject.action,engineDirection:r.subject.engineDirection,verdict:r.verdict,scope:r.scope,runtimeEquivalence:'NOT_ESTABLISHED',releaseAcceptance:'NOT_ESTABLISHED'});
 }
 const catalog=createCatalog(manifests,{ownerEvidence,custodyRoots:[await realpath(path.join(root,'docs/art'))]});
 if(verifyRuntime){const checked=new Set();for(const d of Object.values(catalog.definitions)){const a=d.asset,key=`${a.runtime.path}|${a.runtime.sha256}`;if(checked.has(key))continue;const bytes=await readFile(path.join(root,'public/assets/art-v1',a.runtime.path));if(hash(bytes)!==a.runtime.sha256)throw Error(`Runtime hash mismatch: ${a.id}`);checked.add(key);}}
 const leaders=JSON.parse(await readFile(path.join(root,'public/assets/leadership/manifest.json')));
 for(const [id,c] of Object.entries(leaders.characters)){if(!Object.hasOwn(CHARACTERS,id))throw Error(`Unknown portrait identity: ${id}`);safePath(c.portrait);const bytes=await readFile(path.join(root,'public',c.portrait));catalog.portraitDependencies[id]={id,path:c.portrait,sha256:hash(bytes),scope:'Portrait only; static directional references excluded from animation catalog'};}
 return catalog;
}
function validateScope(scope){
 if(scope===undefined)return null;
 if(!scope||typeof scope!=='object'||Array.isArray(scope)||Object.keys(scope).some(k=>!['map','roster','buildings','leaders'].includes(k))||!MAPS.some(m=>m.id===scope.map))throw Error('Invalid bank scope');
 const result={map:scope.map};
 for(const [key,known] of [['roster',UNITS],['buildings',BUILDINGS],['leaders',CHARACTERS]]){const values=scope[key]??[];if(!Array.isArray(values)||values.some(x=>typeof x!=='string'||!Object.hasOwn(known,x))||new Set(values).size!==values.length)throw Error(`Invalid bank scope ${key}`);result[key]=[...values];}
 return result;
}
export function selectBank(catalog,{route,scope}={}){
 if(!Object.hasOwn(catalog.recipes,route))throw Error(`Unknown route: ${route}`);
 const recipe=catalog.recipes[route],selection=validateScope(scope),wanted=new Set();
 for(const id of recipe.assetIds){const a=catalog.definitions[id]?.asset;if(!a)throw Error(`Missing recipe definition: ${id}`);const identity=(a.family||a.id).replace(/^(unit|building)\./,'');
  if(!selection||['terrain','prop'].includes(a.kind)||a.kind==='building'&&selection.buildings.includes(identity)||a.kind==='unit'&&(selection.roster.includes(identity)||selection.leaders.includes(identity)))wanted.add(id);
 }
 const visit=id=>{const d=catalog.definitions[id];if(!d)throw Error(`Missing dependency: ${id}`);const shadow=d.asset.contactShadow;if(shadow?.mode==='separate'&&!wanted.has(shadow.assetId)){if(!recipe.assetIds.includes(shadow.assetId))throw Error(`Dependency outside route bank: ${shadow.assetId}`);wanted.add(shadow.assetId);visit(shadow.assetId);}};
 for(const id of [...wanted])visit(id);
 const ids=[...new Set(recipe.assetIds)].filter(id=>wanted.has(id));const missingFamilies=selection?[...selection.roster,...selection.buildings,...selection.leaders].filter(identity=>!ids.some(id=>(catalog.definitions[id].asset.family||id).replace(/^(unit|building)\./,'')===identity)):[];
 const portraits=selection?selection.leaders.map(id=>{const p=catalog.portraitDependencies[id];if(!p)throw Error(`Missing selected leader portrait: ${id}`);return clone(p);}):[];
 return {route,scope:selection,assetIds:ids,portraits,missingFamilies,worldPolicy:catalog.scopePolicy};
}
export function compileManifest(catalog,{route,scope,mode='candidate'}={}){
 if(!['candidate','release'].includes(mode))throw Error(`Invalid compile mode: ${mode}`);
 const bank=selectBank(catalog,{route,scope});const assets=bank.assetIds.map(id=>{const d=catalog.definitions[id];validateEntry(d.asset,catalog.custodyRoots);if(hash(canonical(d.asset))!==d.entrySHA256)throw Error(`Catalog definition changed: ${id}`);return clone(d.asset);});
 if(mode==='release'){
  if(!assets.length||bank.missingFamilies.length)throw Error('Release refused: empty/incomplete requested bank');
  const pending=assets.filter(a=>{const e=catalog.definitions[a.id].acceptance.release;return a.candidate||a.review.status!=='APPROVED'||e.status!=='RELEASE_ACCEPTED'||!e.receipt||!e.reviewer||!SHA.test(e.receiptSHA256)||e.runtimeSHA256!==a.runtime.sha256||e.entrySHA256!==catalog.definitions[a.id].entrySHA256;});
  if(pending.length)throw Error(`Release refused: pending/unaccepted entries: ${pending.map(a=>a.id).join(', ')}`);
 }
 const manifest={...clone(catalog.recipes[route].header),assets};if(mode==='release')manifest.status='APPROVED';validateManifest(manifest);return {manifest,bank,acceptance:bank.assetIds.map(id=>({id,...clone(catalog.definitions[id].acceptance)}))};
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const args=process.argv.slice(2),value=flag=>{const i=args.indexOf(flag);if(i<0)return undefined;if(!args[i+1]||args[i+1].startsWith('--'))throw Error(`Missing value for ${flag}`);return args[i+1];};
 const catalog=await loadCatalog({root:value('--root')||rootDefault});const route=value('--route'),scope=value('--scope');const result=route?compileManifest(catalog,{route,scope:scope?JSON.parse(scope):undefined,mode:args.includes('--release')?'release':'candidate'}):catalog;
 const output=value('--output'),serialized=JSON.stringify(result,null,2)+'\n';if(output){await mkdir(path.dirname(path.resolve(output)),{recursive:true});await writeFile(output,serialized);}else process.stdout.write(serialized);
}
