import {UNITS,BUILDINGS,CHARACTERS,MAPS} from './data.js';
const clone=v=>JSON.parse(JSON.stringify(v));
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

export function matchArtScope(state){return {map:state.map.id,roster:Object.keys(UNITS),buildings:Object.keys(BUILDINGS),leaders:[...new Set((state.players||[]).flatMap(p=>[p.king,p.general]).filter(Boolean))]};}
