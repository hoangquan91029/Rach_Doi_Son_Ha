// Render interpolation only. Commands, fog, damage and victory use server state.
export function interpolateView(current,previous,alpha){
 if(!current||!previous||current.map?.id!==previous.map?.id||alpha>=1)return current;
 const old=new Map(previous.entities.map(e=>[e.id,e]));
 return {...current,entities:current.entities.map(e=>{const before=old.get(e.id);if(!before||e.hp<=0||e.embarked||before.embarked||Math.hypot(e.x-before.x,e.y-before.y)>3)return e;return {...e,x:before.x+(e.x-before.x)*alpha,y:before.y+(e.y-before.y)*alpha};})};
}

/** One tick of local render delay, using only completed simulation positions. */
export function interpolateOfflineView(current,previous,acc,{frozen=false,frozenView}={}){
 if(!current||current.winner!=null)return current;
 if(frozen)return frozenView?interpolateView(current,frozenView,0):current;
 if(!previous||current.tick!==previous.tick+1)return current;
 const shown=interpolateView(current,previous,Math.max(0,Math.min(1,acc/.05)));
 if(shown===current)return current;
 // Stop/arrival and a new action use the actual anchor immediately.
 return {...shown,entities:shown.entities.map((e,i)=>current.entities[i].state==='walk'?e:current.entities[i])};
}
