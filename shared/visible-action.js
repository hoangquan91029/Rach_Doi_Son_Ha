/** Current visible activity only: no target IDs, positions, quantities or future orders. */
export function visibleVillagerAction(state,e){
 if(e.type!=='villager'||e.hp<=0||e.embarked)return null;
 if(e.state==='gather'){
  const resource=state.map.resources.find(r=>r.id===e.order?.target);
  if(e.order?.type==='gather'&&resource&&Math.hypot(e.x-resource.x,e.y-resource.y)<=1.1&&['wood','food','iron'].includes(resource.type)){const action={kind:'gather',resource:resource.type};if(e.gatherEpisode?.target===resource.id&&e.gatherEpisode.lastTick===state.tick&&Number.isInteger(e.gatherEpisode.startedTick))action.startedTick=e.gatherEpisode.startedTick;return action;}
 }
 if(e.state==='walk'&&e.lastMovedTick===state.tick){const loads=['wood','food','iron'].filter(k=>(e.cargo?.[k]||0)>0);if(loads.length)return {kind:'carry',load:loads.length>1?'mixed':loads[0],moving:true};}
 return null;
}

/** Private bounded cosmetic episode; callers must already have committed a successful action. */
export function beginActionEpisode(state,entity,kind,{durationTicks=12,continuous=false}={}){
 const previous=entity.actionEpisode,continuing=continuous&&previous?.kind===kind&&previous.lastTick>=state.tick-1;
 entity.actionEpisode={kind,startedTick:continuing?previous.startedTick:state.tick,endTick:state.tick+(continuous?1:durationTicks),lastTick:state.tick,loop:continuous};
}
export function cancelActionEpisode(entity){delete entity.actionEpisode;}
/** Sanitized present activity only. Movement, impact and death preempt cosmetic episodes. */
export function visibleUnitAction(state,entity){
 if(entity.hp<=0||entity.embarked)return null;
 if((entity.hitUntil||0)>state.tick||entity.state==='attack'||entity.pendingAttack||entity.state==='walk'&&entity.lastMovedTick===state.tick)return visibleVillagerAction(state,entity);
 const episode=entity.actionEpisode;
 if(episode&&['ability','load','unload','build'].includes(episode.kind)&&Number.isInteger(episode.startedTick)&&Number.isInteger(episode.endTick)&&episode.startedTick<=state.tick&&episode.endTick>state.tick)return {kind:episode.kind,startedTick:episode.startedTick,endTick:episode.endTick,loop:episode.loop===true};
 return visibleVillagerAction(state,entity);
}
