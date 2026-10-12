/** Pure presentation sampling. Markers describe art; they never apply gameplay commands. */
export function validateFrameEvents(frame) {
 if(frame.events===undefined)return;
 if(!Array.isArray(frame.events)||frame.events.length>32)throw Error('Invalid frame events');
 for(const event of frame.events){
  if(!event||typeof event.name!=='string'||!/^[A-Z][A-Z0-9_]{0,63}$/.test(event.name)||!Number.isSafeInteger(event.offsetMs)||event.offsetMs<0||event.offsetMs>=frame.durationMs)throw Error('Invalid frame event marker');
 }
}

/** Durations are in milliseconds, independent of display refresh and simulation tick rate. */
export function sampleSpriteAnimation(frames,{timeMs=0,loop=true,frame:requestedFrame}={}) {
 const durationMs=frames.reduce((sum,frame)=>sum+frame.durationMs,0);
 const supplied=Number.isFinite(timeMs)?timeMs:0;
 let frame=0,elapsedMs=0;
 if(Number.isInteger(requestedFrame))frame=((requestedFrame%frames.length)+frames.length)%frames.length;
 else {
  elapsedMs=loop?((supplied%durationMs+durationMs)%durationMs):Math.max(0,Math.min(supplied,durationMs));
  while(frame<frames.length-1&&elapsedMs>=frames[frame].durationMs){elapsedMs-=frames[frame].durationMs;frame++;}
 }
 return {frame,elapsedMs,durationMs,events:(frames[frame].events||[]).map(event=>({...event}))};
}

export function defaultAnimationLoop(asset){return asset.loop??['idle','walk','construction','build','repair'].includes(asset.state);}
/** Map an authored contact marker onto authoritative impact; no gameplay dispatch. */
export function attackAnimationTime(asset,entity,visualTimeMs){
 const start=entity.attackStartedTick*50,impact=entity.attackImpactTick*50,ready=entity.attackReadyTick*50;
 const confirmedTime=entity.lastAttack>=entity.attackImpactTick&&Number.isFinite(impact)?Math.max(impact,visualTimeMs):visualTimeMs;
 const fallback=Math.max(0,confirmedTime-(Number.isFinite(start)?start:(entity.lastAttack||0)*50));
 if(!Number.isFinite(start)||!Number.isFinite(impact)||impact<=start)return fallback;
 let marker=null,total=0,count=0;
 for(const frame of asset.frames){for(const event of frame.events||[]){if(['DEAL_DAMAGE','FIRE_PROJECTILE','WEAPON_CONTACT'].includes(event.name)&&Number.isSafeInteger(event.offsetMs)&&event.offsetMs>=0&&event.offsetMs<frame.durationMs){marker=total+event.offsetMs;count++;}}total+=frame.durationMs;}
 if(count!==1||marker<=0||marker>=total||!Number.isFinite(ready)||ready<=impact)return fallback;
 const time=entity.lastAttack>=entity.attackImpactTick?Math.max(impact,visualTimeMs):visualTimeMs;
 if(time<=impact)return Math.max(0,Math.min(marker,(time-start)/(impact-start)*marker));
 return Math.min(total,marker+(time-impact)/(ready-impact)*(total-marker));
}
