/** Presentation-only travelled distance; never changes simulation or uses a global gait clock. */
export function createLocomotionPhase(){
 const tracks=new Map();let lastTick=-Infinity,lastTime=-Infinity;
 return {
  observe(entities,{tick=0,timeMs=tick*50,frozen=false}={}){
   if(tick<lastTick||timeMs<lastTime)tracks.clear();lastTick=tick;lastTime=timeMs;
   const present=new Set();
   for(const e of entities){if(e.id==null||!Number.isFinite(e.x)||!Number.isFinite(e.y))continue;present.add(e.id);const identity=JSON.stringify([e.owner,e.type,e.character??null,e.createdTick??null]);let t=tracks.get(e.id);
    if(!t||t.identity!==identity){tracks.set(e.id,{identity,x:e.x,y:e.y,timeMs,distance:0,state:e.state});continue;}
    const delta=Math.hypot(e.x-t.x,e.y-t.y),dt=Math.max(0,(timeMs-t.timeMs)/1000);
    if(delta>Math.max(2,dt*8))t.distance=0;
    else if(!frozen&&timeMs>t.timeMs&&(e.state==='walk'||t.state==='walk'))t.distance+=delta;
    t.x=e.x;t.y=e.y;t.timeMs=timeMs;t.state=e.state;
   }
   for(const id of tracks.keys())if(!present.has(id))tracks.delete(id);
  },
  sample(id,{distancePerCycle,cycleDurationMs}){const distance=tracks.get(id)?.distance||0;return {distance,timeMs:(distance%distancePerCycle)/distancePerCycle*cycleDurationMs};},
  clear(){tracks.clear();lastTick=-Infinity;lastTime=-Infinity;}
 };
}
