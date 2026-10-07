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
