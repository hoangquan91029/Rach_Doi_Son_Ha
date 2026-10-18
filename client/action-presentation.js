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
 if(['hit','death','attack','walk'].includes(baseState))return [baseState];
 const action=entity.visibleAction;
 if(['ability','load','unload','build'].includes(action?.kind))return [action.kind];
 if(baseState==='repair')return ['build'];
 if(entity.type!=='villager')return [baseState];
 if(baseState==='gather'&&action?.kind==='gather'&&['wood','food','iron'].includes(action.resource))return [`gather_${action.resource}`,'gather'];
 return [baseState];
}

/** Existing bounded presentation clock, anchored only to authoritative current gather episode. */
export function gatherAnimationTime(entity,timeMs){const start=entity.visibleAction?.startedTick;return Number.isInteger(start)&&start>=0&&entity.visibleAction?.kind==='gather'?Math.max(0,timeMs-start*50):timeMs;}

/** Finite/action-work clocks use only sanitized authoritative episode ticks. */
export function episodeAnimationTime(entity,timeMs,clipDurationMs){
 const action=entity.visibleAction;if(!['ability','load','unload','build'].includes(action?.kind)||!Number.isInteger(action.startedTick))return timeMs;
 const elapsed=Math.max(0,Math.min(timeMs,action.endTick*50)-action.startedTick*50),duration=(action.endTick-action.startedTick)*50;
 return action.loop!==true&&Number.isFinite(clipDurationMs)&&clipDurationMs>0&&duration>0?elapsed/duration*clipDurationMs:elapsed;
}

/** Bounded cosmetic rest clock. Observes requested actions even when their artwork is absent. */
export function createIdleEntryClock({maxEntries=1024}={}){
 if(!Number.isInteger(maxEntries)||maxEntries<1)throw Error('Invalid idle clock capacity');
 const tracks=new Map();let lastTime=-Infinity,lastTick=-Infinity;
 return {
  observe(entities,{tick=0,timeMs=tick*50,frozen=false}={}){
   if(!Number.isFinite(timeMs))return;
   if(timeMs<lastTime||tick<lastTick)tracks.clear();lastTime=timeMs;lastTick=tick;
   const idle=entities.filter(e=>e.id!=null&&e.kind==='unit'&&e.hp>0&&!e.embarked&&authoredActionStates(e,(e.hitUntil||0)>tick?'hit':e.state)[0]==='idle');
   const present=new Set(idle.map(e=>e.id));
   for(const id of tracks.keys())if(!present.has(id))tracks.delete(id);
   for(const e of idle){
    const identity=JSON.stringify([e.owner,e.type,e.character??null,e.createdTick??null,e.dir]);
    let t=tracks.get(e.id);
    if(!t||t.identity!==identity){if(t||tracks.size<maxEntries){t={identity,start:timeMs,last:timeMs};tracks.set(e.id,t);}else continue;}
    else {if(frozen)t.start+=Math.max(0,timeMs-t.last);t.last=timeMs;}
   }
  },
  sample(id){const t=tracks.get(id);return t?Math.max(0,t.last-t.start):0;},
  clear(){tracks.clear();lastTime=-Infinity;lastTick=-Infinity;},
  get size(){return tracks.size;}
 };
}
