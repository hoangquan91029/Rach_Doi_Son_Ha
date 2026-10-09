import {BALANCE,UNITS} from '../shared/data.js';
export function trainingProgress(job){
 const remaining=Math.max(0,Number(job?.remaining)||0),saved=Number(job?.total),total=saved>0&&Number.isFinite(saved)?saved:Math.max(UNITS[job?.unit]?.trainTime||1,remaining);
 return remaining===0?100:Math.max(0,Math.min(99,Math.floor(100*(1-remaining/total))));
}
export function armyFoodWarning(entities,owner){
 const count=(entities||[]).filter(e=>e.owner===owner&&e.kind==='unit'&&e.hp>0&&!['villager','wagon'].includes(e.type)&&e.foodMax>0&&e.food/e.foodMax<BALANCE.lowSupply).length;
 return count?`ARMY LOW ON FOOD · ${count} ${count===1?'unit needs':'units need'} resupply`:'';
}
