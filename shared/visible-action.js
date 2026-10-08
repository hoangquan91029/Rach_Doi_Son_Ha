/** Current visible activity only: no target IDs, positions, quantities or future orders. */
export function visibleVillagerAction(state,e){
 if(e.type!=='villager'||e.hp<=0||e.embarked)return null;
 if(e.state==='gather'){
  const resource=state.map.resources.find(r=>r.id===e.order?.target);
  if(e.order?.type==='gather'&&resource&&Math.hypot(e.x-resource.x,e.y-resource.y)<=1.1&&['wood','food','iron'].includes(resource.type))return {kind:'gather',resource:resource.type};
 }
 if(e.state==='walk'&&e.lastMovedTick===state.tick){const loads=['wood','food','iron'].filter(k=>(e.cargo?.[k]||0)>0);if(loads.length)return {kind:'carry',load:loads.length>1?'mixed':loads[0],moving:true};}
 return null;
}
