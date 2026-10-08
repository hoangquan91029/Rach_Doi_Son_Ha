/** Cosmetic clock: interpolates only already received simulation time. */
export function createPresentationClock(){let from=0,to=0,at=0,span=1,last=0,key=null,frozen=false;return {
 reset(state,now=0){key=state?.map?.id;from=to=last=Math.max(0,(state?.tick||0)*50);at=now;span=1;frozen=false;},
 receive(state,now=0,{paused=false}={}){const next=Math.max(0,(state?.tick||0)*50);if(key!==state?.map?.id||next<to){this.reset(state,now);}else{from=paused||state?.winner!=null?last:this.sample(now);span=Math.max(50,Math.min(300,next-to||200));to=next;at=now;}frozen=paused||state?.winner!=null;if(frozen)last=from;},
 sample(now,{paused=false}={}){if(paused)frozen=true;if(frozen)return last;last=Math.max(from,Math.min(to,from+(to-from)*Math.max(0,Math.min(1,(now-at)/span))));return last;}
};}
export function offlineVisualTime(tick,acc,{frozen=false,previousTimeMs}={}){return Math.max(0,frozen?(Number.isFinite(previousTimeMs)?previousTimeMs:tick*50):Math.min(tick*50,(tick-1)*50+Math.max(0,Math.min(.05,acc))*1000));}
/** One bounded catch-up pulse per known impact; never a pending impact. */
export function createImpactPulses(){const seen=new Map(),until=new Map();return {
 reset(entities=[]){seen.clear();until.clear();for(const e of entities)if(Number.isFinite(e.lastAttack))seen.set(e.id,e.lastAttack);},
 update(entities,tick,now,{frozen=false}={}){const present=new Set();for(const e of entities){present.add(e.id);if(Number.isFinite(e.lastAttack)&&e.lastAttack<=tick&&seen.get(e.id)!==e.lastAttack){seen.set(e.id,e.lastAttack);if(!frozen&&e.hp>0&&!e.embarked&&tick-e.lastAttack<=10)until.set(e.id,now+90);}}for(const id of seen.keys())if(!present.has(id)){seen.delete(id);until.delete(id);}if(frozen)until.clear();},
 active(id,now){return now<(until.get(id)||0);}
};}

/** Resource-specific gathering; loaded return movement always uses the existing walk pose. */
export function authoredActionStates(entity,baseState){
 if(entity.type!=='villager'||['hit','death','attack'].includes(baseState))return [baseState];
 const action=entity.visibleAction;
 if(baseState==='gather'&&action?.kind==='gather'&&['wood','food','iron'].includes(action.resource))return [`gather_${action.resource}`,'gather'];
 return [baseState];
}
