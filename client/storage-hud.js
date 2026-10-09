import {BUILDINGS,UNITS} from '../shared/data.js';
export function cargoLabels(entity,localPlayer){
 if(!entity?.cargo||entity.owner!==localPlayer)return [];
 const cargo=entity.cargo,labels=[],storage=['residence','granary','depot'].includes(entity.type),wagon=entity.type==='wagon';
 const foodKnown=Number.isFinite(cargo.food)&&cargo.food>=0;
 const capacity=storage?BUILDINGS[entity.type]?.capacity:wagon?UNITS.wagon.capacity:null;
 if((storage||wagon)&&foodKnown&&Number.isFinite(capacity))labels.push(`Food ${storage?'stock':'load'} ${Math.round(cargo.food)}/${capacity}`);
 const other=[];for(const kind of ['food','wood','iron'])if(Number.isFinite(cargo[kind])&&cargo[kind]>0&&!(kind==='food'&&(storage||wagon)&&foodKnown))other.push(`${Math.round(cargo[kind])} ${kind}`);
 if(Array.isArray(cargo.units)&&cargo.units.length)other.push(`${cargo.units.length} aboard`);
 if(other.length)labels.push(`Cargo ${other.join(' · ')}`);else if(!labels.length&&Object.keys(cargo).length)labels.push('Cargo empty');
 return labels;
}
