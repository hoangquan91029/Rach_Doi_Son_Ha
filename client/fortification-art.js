import {topologyForMask} from './fortification-topology.js';
/** Optional whole illustrations, selected without transforming source pixels. */
export function validateFortificationArt(asset){
 const m=asset.fortification;if(m===undefined)return asset;
 const type=asset.family?.replace(/^building\./,'');
 if(asset.kind!=='building'||!['wall','gate'].includes(type)||asset.direction!==null||!m||Object.keys(m).some(k=>!['mask','axis','deathSite'].includes(k)))throw Error('Invalid whole fortification metadata');
 if(m.deathSite!==undefined&&(m.deathSite!=='completed'||asset.state!=='death'||m.mask!==0))throw Error('Invalid completed death site metadata');
 const t=topologyForMask(m.mask);
 if(m.axis!==undefined&&(type!=='gate'||m.axis!==t.axis))throw Error('Fortification gate axis must match deterministic mask');
 return asset;
}
export function validateFortificationVariants(assets){
 const keys=new Set(),layouts=new Map();
 for(const a of assets){if(a.fortification===undefined)continue;validateFortificationArt(a);const type=a.family.replace(/^building\./,''),key=JSON.stringify([type,a.state,a.direction,a.fortification.mask,a.fortification.deathSite??null]);if(keys.has(key))throw Error('Ambiguous whole fortification variant');keys.add(key);
 const layout=JSON.stringify([a.source.width,a.source.height,a.cell.width,a.cell.height,a.pivot,a.render]);if(layouts.has(type)&&layouts.get(type)!==layout)throw Error('Fortification variants change fixed layout');layouts.set(type,layout);}
}
export function selectFortificationArt(assets,entity,context,state){
 if(!entity||entity.kind!=='building'||!['wall','gate'].includes(entity.type)||entity.embarked)return {asset:null,reason:'Incomplete or ineligible fortification'};
 const dead=entity.hp<=0;
 if(dead!==(state==='death'))return {asset:null,reason:'Death requires dead fortification and exact authored death state'};
 const unfinished=!dead&&Boolean(entity.construction||entity.underConstruction===true);
 if(!dead&&unfinished!==(state==='construction'))return {asset:null,reason:'Construction requires exact authored construction state'};
 // Dead or unfinished sites have no completed links: only standalone mask0 art.
 const t=dead||unfinished?topologyForMask(0):context?.get(entity.id);if(!t||!Number.isInteger(t.mask)||t.mask<0||t.mask>15||t.axis!==topologyForMask(t.mask).axis)return {asset:null,reason:'No exact visible topology context'};
 const matches=assets.filter(a=>a.kind==='building'&&[entity.type,`building.${entity.type}`].includes(a.family)&&a.state===state&&a.direction===null&&a.fortification?.mask===t.mask&&(a.fortification.axis===undefined||a.fortification.axis===t.axis));
 const siteUnfinished=Boolean(entity.construction||entity.underConstruction===true);
 const qualified=dead&&!siteUnfinished?matches.filter(a=>a.fortification.deathSite==='completed'):[];
 if(qualified.length)return qualified.length===1?{asset:qualified[0],reason:null}:{asset:null,reason:'Ambiguous whole fortification variant'};
 const generic=matches.filter(a=>a.fortification.deathSite===undefined);
 return generic.length===1?{asset:generic[0],reason:null}:{asset:null,reason:generic.length?'Ambiguous whole fortification variant':'No whole illustration for exact topology/state'};
}
