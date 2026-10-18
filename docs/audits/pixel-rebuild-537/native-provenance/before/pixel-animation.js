/** Native pixel metadata and pure presentation only. Never mutates simulation. */
export const PIXEL_DIRECTIONS = Object.freeze(['S','SW','W','NW','N','NE','E','SE']);
const fail = message => { throw new Error(`Pixel clip: ${message}`); };
const exact = (o, keys) => o && typeof o === 'object' && !Array.isArray(o) && Object.keys(o).length === keys.length && keys.every(k => Object.hasOwn(o,k));
const same = (a,b) => JSON.stringify(a) === JSON.stringify(b);
export function validatePixelClip(c) {
 if(!exact(c,['schema','identity','action','atlas','cellSize','atlasSize','frameCount','directions','anchor','renderSize','frameDurationsMs','loop','events','palette','review','provenance'])) fail('fields');
 if(c.schema!=='rds-pixel-clip/v1'|| !/^[a-z][a-z0-9_-]*$/.test(c.identity)|| !/^[a-z][a-z0-9_]*$/.test(c.action)||!['idle','walk','attack','hit','gather_wood','gather_food','gather_iron','build','ability','load','unload','chop_tree'].includes(c.action))fail('identity/action/schema');
 if(typeof c.atlas!=='string'||!/^\/(?!\/)[a-zA-Z0-9_/-]+\.png$/.test(c.atlas)||c.atlas.includes('/../'))fail('atlas URL');
 if(c.cellSize!==128||c.atlasSize!==1024||c.frameCount!==8||!same(c.directions,PIXEL_DIRECTIONS)||!same(c.anchor,[64,112])||!same(c.renderSize,[64,64]))fail('layout');
 if(!Array.isArray(c.frameDurationsMs)||c.frameDurationsMs.length!==8||!c.frameDurationsMs.every(n=>Number.isSafeInteger(n)&&n>0)||typeof c.loop!=='boolean')fail('timing');
 if(!Array.isArray(c.events)||!c.events.every(e=>exact(e,['name','frame'])&&typeof e.name==='string'&&e.name.length>0&&Number.isInteger(e.frame)&&e.frame>=0&&e.frame<8)||new Set(c.events.map(e=>`${e.name}:${e.frame}`)).size!==c.events.length)fail('events');
 if(!Array.isArray(c.palette)||!c.palette.length||c.palette.length>32||!c.palette.every(x=>/^#[0-9a-f]{6}$/.test(x))||new Set(c.palette).size!==c.palette.length)fail('palette');
 if(!exact(c.review,['structural','visual','runtime'])||!Object.values(c.review).every(x=>x===null||['PASS','FAIL','UNKNOWN'].includes(x)))fail('review');
 const p=c.provenance;
 if(!exact(p,['sources','callTokens'])||!Array.isArray(p.sources)||!p.sources.length||!p.sources.every(s=>exact(s,['path','sha256'])&&typeof s.path==='string'&&/^docs\/art\/pixel-[a-zA-Z0-9_-]+\/(?:raw|raws)\/(?!\.)[^\\]+\.png$/.test(s.path)&&!s.path.split('/').includes('..')&&/^[a-f0-9]{64}$/.test(s.sha256))||!Array.isArray(p.callTokens)||!p.callTokens.length||!p.callTokens.every(t=>typeof t==='string'&&t.trim().length>0)||new Set(p.callTokens).size!==p.callTokens.length)fail('provenance');
 return c;
}
export function engineDirectionToRow(d){if(!Number.isInteger(d)||d<0||d>7)fail('engine direction');return [7,0,1,2,3,4,5,6][d];}
export function pixelFrameRect(c,row,frame){validatePixelClip(c);if(!Number.isInteger(row)||row<0||row>7||!Number.isInteger(frame)||frame<0||frame>7)fail('cell index');return {sx:frame*128,sy:row*128,sw:128,sh:128};}
export function createPixelAnimator({strideDistance}={}) {
 const states=new Map();
 return {clear(entityId){states.delete(entityId);},sample(c,{entityId,actionInstance,direction,timeMs,distance=0,frozen=false}){
  validatePixelClip(c); const row=engineDirectionToRow(direction);
  if(entityId==null||actionInstance==null||!Number.isFinite(timeMs)||!Number.isFinite(distance))fail('sample clocks/identity');
  if(c.action==='walk'&&!(Number.isFinite(strideDistance)&&strideDistance>0))return {frame:0,row,events:[],complete:false,unqualified:true,reason:'reviewed strideDistance required'};
  let s=states.get(entityId);const key=`${c.identity}/${c.action}/${actionInstance}`;
  if(!s||s.key!==key||s.clip!==c){s={key,clip:c,lastTime:timeMs,lastDistance:distance,elapsed:0,travel:0,position:-1};states.set(entityId,s);}
  if(!frozen){s.elapsed+=Math.max(0,timeMs-s.lastTime);s.travel+=Math.max(0,distance-s.lastDistance);}
  s.lastTime=timeMs;s.lastDistance=distance;
  const total=c.frameDurationsMs.reduce((a,b)=>a+b,0);
  const raw=c.action==='walk'?s.travel/strideDistance*total:s.elapsed;
  const bounded=c.loop?raw%total:Math.min(raw,total-Number.EPSILON*total);
  let frame=0,edge=c.frameDurationsMs[0];while(frame<7&&bounded>=edge)edge+=c.frameDurationsMs[++frame];
  const events=[];
  // Finite markers fire once even when a sample skips frames. Loop markers are presentation-only per crossed cycle.
  if(!frozen){let start=0;for(const e of c.events){start=c.frameDurationsMs.slice(0,e.frame).reduce((a,b)=>a+b,0);if(!c.loop){if(s.position<start&&raw>=start)events.push(e.name);}else{const first=Math.max(0,Math.floor((s.position-start)/total)+1),last=Math.floor((raw-start)/total);if(last>=first)events.push(e.name);}}s.position=raw;}
  return {frame,row,events,complete:!c.loop&&raw>=total};
 }};
}
