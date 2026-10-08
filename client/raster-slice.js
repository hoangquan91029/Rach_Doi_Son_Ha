import {authoredActionStates,gatherAnimationTime} from './action-presentation.js';
import {sampleSpriteAnimation,defaultAnimationLoop,attackAnimationTime} from './sprite-timing.js';
import {createArtAssetPipeline} from './art-assets.js';
import {createTerrainTransitions} from './terrain-transitions.js';
import {createLocomotionPhase} from './locomotion-phase.js';
import {TILE_WIDTH,TILE_HEIGHT} from './world-presentation.js';

const TW=TILE_WIDTH,TH=TILE_HEIGHT;
const finite=n=>Number.isFinite(n);
const normalState=entity=>entity.hp<=0?'death':entity.state;
/** Optional candidate art over actual simulation. No substitute map, fake units, or sprite mirroring. */
export function createRasterSlice({enabled=['pilot','walk','work'].includes(new URLSearchParams(globalThis.location?.search||'').get('art')),manifestUrl=new URLSearchParams(globalThis.location?.search||'').get('art')==='work'?'/assets/art-v1/gather-026-manifest.json':new URLSearchParams(globalThis.location?.search||'').get('art')==='walk'?'/assets/art-v1/walk-014-manifest.json':'/assets/art-v1/manifest.json',onStatus=()=>{},materialWorldSize=8}={}) {
 const pipeline=createArtAssetPipeline({manifestUrl,allowCandidates:true,onStatus});
 const locomotion=createLocomotionPhase();
 const cells=new Map(),patterns=new WeakMap(),missing=new Set();let ready=false;
 const status={enabled,phase:enabled?'CANDIDATE':'DISABLED',quality:'PLACEHOLDER_ONLY',groundDraws:0,propDraws:0,entityDraws:0,walkDraws:0,idleDraws:0,lastWalk:null,gatherDraws:0,lastGather:null,missing:[],pipeline:pipeline.stats};
 const recordMissing=(key,reason)=>{if(!missing.has(key)){missing.add(key);status.missing.push({key,reason,status:'PLACEHOLDER_ONLY'});status.quality='PLACEHOLDER_ONLY';}};
 const select=({families,kind,state,direction,variant=0,timeMs=0})=>{
  if(!enabled||!ready)return null;
  const candidates=(pipeline.manifest?.assets||[]).filter(asset=>asset.kind===kind&&families.includes(asset.family||asset.id)&&asset.state===state&&asset.direction===direction);
  if(!candidates.length){recordMissing(`${families[0]}:${state}:${direction}`,'No exact authored raster state/direction');return null;}
  const candidate=candidates[((variant%candidates.length)+candidates.length)%candidates.length];
  const raster=pipeline.get(candidate.id,{state,direction,timeMs});if(!raster.image){recordMissing(candidate.id,raster.reason);return null;}return raster;
 };
 const cellImage=raster=>{
  if(raster.sx===0&&raster.sy===0&&raster.sw===raster.image.width&&raster.sh===raster.image.height)return raster.image;
  const key=`${raster.id}:${raster.frame}`;if(!cells.has(key)){const canvas=typeof OffscreenCanvas==='function'?new OffscreenCanvas(raster.sw,raster.sh):globalThis.document?.createElement('canvas');if(!canvas)return null;canvas.width=raster.sw;canvas.height=raster.sh;const c=canvas.getContext('2d');c.drawImage(raster.image,raster.sx,raster.sy,raster.sw,raster.sh,0,0,raster.sw,raster.sh);cells.set(key,canvas);}return cells.get(key);
 };
 const drawAt=(ctx,raster,point,zoom)=>{
  if(!raster?.image||!finite(point?.x)||!finite(point?.y)||!finite(zoom)||zoom<=0)return false;
  const width=raster.render.width*zoom,height=raster.render.height*zoom;
  const x=point.x-raster.pivot.x/raster.sw*width,y=point.y-raster.pivot.y/raster.sh*height;
  ctx.drawImage(raster.image,raster.sx,raster.sy,raster.sw,raster.sh,x,y,width,height);return true;
 };
 const shadowAt=(ctx,raster,point,zoom)=>{
  if(raster.contactShadow.mode!=='separate')return true;
  const shadow=pipeline.get(raster.contactShadow.assetId);if(!shadow.image){recordMissing(raster.contactShadow.assetId,'Separate authored contact shadow unavailable');return false;}
  return drawAt(ctx,shadow,point,zoom);
 };
 const rasterAt=(ctx,raster,point,zoom)=>{if(!shadowAt(ctx,raster,point,zoom))return false;return drawAt(ctx,raster,point,zoom);};
 const transitionMaterials=new Map();
 const transitionRaster=(terrain,timeMs)=>{
  const cached=transitionMaterials.get(terrain);if(cached?.timeMs===timeMs)return cached.raster;
  const families=terrain==='shore'?['shore']:terrain==='ford'?['ford','terrain.ford']:['water','terrain.water'];
  const raster=select({families,kind:'terrain',state:'material',direction:null,timeMs});if(!raster)return false;
  transitionMaterials.set(terrain,{timeMs,raster});return raster;
 };
 const paintMaterial=(ctx,terrain,{project,zoom,timeMs,bounds})=>{
  const raster=transitionRaster(terrain,timeMs);if(!raster)return false;
  const image=cellImage(raster);if(!image)return false;
  let byRaster=patterns.get(ctx);if(!byRaster){byRaster=new Map();patterns.set(ctx,byRaster);}
  const key=`${raster.id}:${raster.frame}`;if(!byRaster.has(key))byRaster.set(key,{pattern:ctx.createPattern(image,'repeat'),last:null});
  const cached=byRaster.get(key),pattern=cached.pattern;if(!pattern?.setTransform){recordMissing(raster.id,'World-anchored CanvasPattern transform unsupported');return false;}
  const repeat=raster.asset.materialWorldSize,wx=finite(repeat?.width)&&repeat.width>0?repeat.width:materialWorldSize,wy=finite(repeat?.height)&&repeat.height>0?repeat.height:materialWorldSize,origin=project(0,0);
  if(!finite(wx)||!finite(wy)||wx<=0||wy<=0||!finite(origin?.x)||!finite(origin?.y))return false;
  pattern.setTransform({a:TW*zoom/2*wx/raster.sw,b:TH*zoom/2*wx/raster.sw,c:-TW*zoom/2*wy/raster.sh,d:TH*zoom/2*wy/raster.sh,e:origin.x,f:origin.y});cached.last=null;
  ctx.fillStyle=pattern;ctx.fillRect(bounds.x,bounds.y,bounds.width,bounds.height);return true;
 };
 const transitions=createTerrainTransitions({paintMaterial,
  materialKey:(terrain,timeMs)=>{const r=transitionRaster(terrain,timeMs);return r?JSON.stringify([r.id,r.frame,r.asset.runtime?.sha256,r.asset.source?.sha256,r.asset.materialWorldSize]):null;},
  hasBank:()=>Boolean(pipeline.manifest?.assets?.some(a=>a.kind==='terrain'&&a.family==='shore'&&a.state==='material'&&a.direction===null)),
  onMissingBank:()=>recordMissing('shore:material:null','Dedicated authored bank material unavailable; bounded original-material blending remains a candidate')});
 return {
  status,pipeline,
  observeEntities(entities,options){status.lastGather=null;if(enabled)locomotion.observe(entities,options);},
  drawTransitions(ctx,options){if(!enabled||!ready)return false;return transitions.draw(ctx,options);},
  async preload(){if(!enabled)return this;await pipeline.preload();ready=true;status.quality=pipeline.stats.status;return this;},
  /** project uses existing renderer logical pixels; camera zoom and DPR must not be applied twice. */
  drawGround(ctx,{x,y,terrain,project,zoom=1,timeMs=0}={}) {
   if(!enabled||!ready||!finite(x)||!finite(y)||typeof project!=='function'||!finite(zoom)||zoom<=0)return false;
   const water=['river','sea'].includes(terrain),ford=terrain==='ford';if(!water&&!ford&&!['plain','forest','hill'].includes(terrain)){recordMissing(`ground:${terrain}`,'No authored material for this terrain');return false;}
   const raster=select({families:ford?['ford','terrain.ford']:water?['water','terrain.water']:['grass','terrain.grass'],kind:'terrain',state:'material',direction:null,timeMs});if(!raster)return false;
   const image=cellImage(raster);if(!image)return false;
   let byRaster=patterns.get(ctx);if(!byRaster){byRaster=new Map();patterns.set(ctx,byRaster);}const key=`${raster.id}:${raster.frame}`;if(!byRaster.has(key))byRaster.set(key,{pattern:ctx.createPattern(image,'repeat'),last:null});const cached=byRaster.get(key),pattern=cached.pattern;
   if(!pattern?.setTransform){recordMissing(raster.id,'World-anchored CanvasPattern transform unsupported');return false;}
   const repeat=raster.asset.materialWorldSize;const wx=finite(repeat?.width)&&repeat.width>0?repeat.width:materialWorldSize,wy=finite(repeat?.height)&&repeat.height>0?repeat.height:materialWorldSize;
   if(!finite(wx)||!finite(wy)||wx<=0||wy<=0)return false;
   const origin=project(0,0),point=project(x,y);if(!finite(origin.x)||!finite(origin.y)||!finite(point.x)||!finite(point.y))return false;
   // One continuous world plane. Clip masks are invisible coverage; no tile strokes or procedural detail.
   const last=cached.last;if(!last||last.zoom!==zoom||last.x!==origin.x||last.y!==origin.y||last.wx!==wx||last.wy!==wy){pattern.setTransform({a:TW*zoom/2*wx/raster.sw,b:TH*zoom/2*wx/raster.sw,c:-TW*zoom/2*wy/raster.sh,d:TH*zoom/2*wy/raster.sh,e:origin.x,f:origin.y});cached.last={zoom,x:origin.x,y:origin.y,wx,wy};}
   ctx.save();ctx.beginPath();const rx=TW*zoom/2+.25,ry=TH*zoom/2+.125;ctx.moveTo(point.x,point.y-ry);ctx.lineTo(point.x+rx,point.y);ctx.lineTo(point.x,point.y+ry);ctx.lineTo(point.x-rx,point.y);ctx.closePath();ctx.clip();ctx.fillStyle=pattern;ctx.fillRect(point.x-rx,point.y-ry,rx*2,ry*2);ctx.restore();status.groundDraws++;return true;
  },
  /** World props can share x+y depth sorting with entities. Coordinates remain simulation coordinates. */
  drawProp(ctx,{x,y,type='forest',project,zoom=1,timeMs=0,variant=0}={}) {
   if(!enabled||!ready||type!=='forest'||typeof project!=='function'||!finite(x)||!finite(y))return false;
   const raster=select({families:['forest','prop.forest'],kind:'prop',state:'static',direction:null,variant,timeMs});if(!raster)return false;
   if(rasterAt(ctx,raster,project(x,y),zoom)){status.propDraws++;return true;}return false;
  },
  sampleEntity(entity,{tick=0,timeMs=tick*50}={}) {
   if(!enabled||!ready||!entity||entity.embarked||!finite(entity.x)||!finite(entity.y))return false;
   if(entity.kind==='building'&&entity.construction){recordMissing(`${entity.type}:construction`,'No authored construction sequence');return false;}
   let families,kind,direction;
   if(entity.kind==='building'){if(!['residence','granary'].includes(entity.type))return false;families=[entity.type,`building.${entity.type}`];kind='building';direction=null;}
   else if(['villager','infantry','cavalry'].includes(entity.type)){families=[entity.type,`unit.${entity.type}`];kind='unit';direction=entity.dir;}
   else if(entity.type==='general'&&entity.character==='tran_hung_dao'){families=['tran_hung_dao','unit.tran_hung_dao'];kind='unit';direction=entity.dir;}
   else return false;
   const state=normalState(entity);if(typeof state!=='string'||!(direction===null||Number.isInteger(direction)&&direction>=0&&direction<=7))return false;
   // A hit frame must be authored too; an idle key never stands in for movement, combat or death.
   const baseVisualState=entity.hp>0&&(entity.hitUntil||0)>tick?'hit':state;
   const states=authoredActionStates(entity,baseVisualState);let candidates=[],visualState=baseVisualState;
   for(const requested of states){candidates=(pipeline.manifest?.assets||[]).filter(a=>a.kind===kind&&families.includes(a.family||a.id)&&a.state===requested&&a.direction===direction);if(candidates.length){visualState=requested;break;}}
   if(!candidates.length){recordMissing(`${families[0]}:${visualState}:${direction}`,'No exact authored raster state/direction');return false;}
   const asset=candidates[0];let elapsed=timeMs;
   let walkPhase=null;
   if(visualState==='walk'&&asset.locomotion){walkPhase=locomotion.sample(entity.id,{distancePerCycle:asset.locomotion.distancePerCycle,cycleDurationMs:asset.frames.reduce((sum,f)=>sum+f.durationMs,0)});elapsed=walkPhase.timeMs;}
   else if(visualState==='gather'||visualState.startsWith('gather_'))elapsed=gatherAnimationTime(entity,timeMs);
   else if(visualState==='hit')elapsed=Math.max(0,timeMs-((entity.hitUntil||tick)-6)*50);
   else if(visualState==='death')elapsed=Math.max(0,timeMs-(entity.deadTick??tick)*50);
   else if(visualState==='attack'&&finite(entity.attackStartedTick??entity.lastAttack))elapsed=attackAnimationTime(asset,entity,timeMs);
   const sample=sampleSpriteAnimation(asset.frames,{timeMs:elapsed,loop:defaultAnimationLoop(asset)});
   const raster=pipeline.get(asset.id,{state:visualState,direction,timeMs:elapsed,frame:sample.frame});if(!raster.image){recordMissing(asset.id,raster.reason);return false;}
   return {raster,visualState,walkPhase,sample,direction,elapsed};
  },
  drawEntity(ctx,entity,{project,zoom=1,tick=0,timeMs=tick*50}={}) {
   if(typeof project!=='function')return false;const result=this.sampleEntity(entity,{tick,timeMs});if(!result)return false;const {raster,visualState,walkPhase,sample,direction,elapsed}=result,asset=raster.asset;
   if(rasterAt(ctx,raster,project(entity.x,entity.y),zoom)){status.entityDraws++;if(visualState==='gather_wood'&&entity.type==='villager'){status.gatherDraws++;status.lastGather={entityId:entity.id,frame:sample.frame,direction,assetId:asset.id,visualState,startedTick:entity.visibleAction?.startedTick??null,elapsedMs:sample.elapsedMs,timeMs:elapsed,presentationTimeMs:timeMs};}if(walkPhase){status.walkDraws++;status.lastWalk={entityId:entity.id,frame:sample.frame,distance:walkPhase.distance,distancePerCycle:asset.locomotion.distancePerCycle,direction};}else if(visualState==='idle'&&asset.family==='unit.villager')status.idleDraws++;return true;}return false;
  },
  /** Deterministic existing forest density, sorted ready for a merged prop/entity depth queue. */
  propsForState(state,{onlyVisible=true}={}) {
   if(!enabled||!state?.map?.tiles)return [];
   const {width,height,tiles}=state.map,props=[];
   for(let y=0;y<height;y++)for(let x=0;x<width;x++){const index=y*width+x,v=(x*17+y*31)%19;if(tiles[index]!=='forest'||v>=5||onlyVisible&&state.fog?.visible&&!state.fog.visible[index])continue;props.push({type:'forest',x:x+.5,y:y+.5,variant:v,key:`forest:${x}:${y}`,depth:x+y});}
   return props.sort((a,b)=>a.depth-b.depth||a.y-b.y||a.x-b.x);
  },
  dispose(){locomotion.clear();transitions.dispose();transitionMaterials.clear();pipeline.dispose();cells.clear();ready=false;}
 };
}
