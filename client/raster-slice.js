import {unitArtFamilies} from '../shared/unit-art.js';
import {selectFortificationArt} from './fortification-art.js';
import {artRoute} from './art-routes.js';
import {mountainPropPlacements,hillGroundPlacements,foodResourceEligible,staticResourceEligible} from './terrain-props.js';
import {authoredActionStates,gatherAnimationTime} from './action-presentation.js';
import {sampleSpriteAnimation,defaultAnimationLoop,attackAnimationTime} from './sprite-timing.js';
import {createArtAssetPipeline} from './art-assets.js';
import {createTerrainTransitions} from './terrain-transitions.js';
import {createLocomotionPhase} from './locomotion-phase.js';
import {TILE_WIDTH,TILE_HEIGHT} from './world-presentation.js';

const TW=TILE_WIDTH,TH=TILE_HEIGHT;
const finite=n=>Number.isFinite(n);
const normalState=entity=>entity.hp<=0?'death':entity.kind==='building'&&(entity.construction||entity.underConstruction===true)?'construction':entity.state;
/** Optional candidate art over actual simulation. No substitute map, fake units, or sprite mirroring. */
export function createRasterSlice({enabled=artRoute().enabled,manifestUrl=artRoute().manifestUrl,onStatus=()=>{},materialWorldSize=8}={}) {
 const worldArtEnabled=()=>artRoute().world;
 const pipeline=createArtAssetPipeline({manifestUrl,allowCandidates:true,onStatus});
 const locomotion=createLocomotionPhase();
 const cells=new Map(),patterns=new WeakMap(),missing=new Set();let ready=false;
 const status={enabled,phase:enabled?'CANDIDATE':'DISABLED',quality:'PLACEHOLDER_ONLY',groundDraws:0,propDraws:0,entityDraws:0,walkDraws:0,idleDraws:0,lastWalk:null,gatherDraws:0,lastGather:null,buildingDeathDraws:0,lastBuildingDeath:null,missing:[],pipeline:pipeline.stats};
 const recordMissing=(key,reason)=>{if(!missing.has(key)){missing.add(key);status.missing.push({key,reason,status:'PLACEHOLDER_ONLY'});status.quality='PLACEHOLDER_ONLY';}};
 const select=({families,kind,state,direction,variant=0,timeMs=0})=>{
  if(!enabled||!ready)return null;
  const candidates=(pipeline.manifest?.assets||[]).filter(asset=>asset.kind===kind&&families.includes(asset.family||asset.id)&&asset.state===state&&asset.direction===direction);
  if(!candidates.length){recordMissing(`${families[0]}:${state}:${direction}`,'No exact authored raster state/direction');return null;}
  const candidate=candidates[((variant%candidates.length)+candidates.length)%candidates.length];
  const raster=pipeline.get(candidate.id,{state,direction,timeMs});if(!raster.image){recordMissing(candidate.id,raster.reason);return null;}return raster;
 };
 const mountainReady=()=>worldArtEnabled()&&Boolean(select({families:['mountain','prop.mountain'],kind:'prop',state:'static',direction:null,timeMs:0})?.image);
 const mountainGround=()=>worldArtEnabled()&&pipeline.manifest?.assets?.some(a=>a.family==='mountain-ground'&&a.kind==='terrain'&&a.state==='material'&&a.direction===null)?select({families:['mountain-ground'],kind:'terrain',state:'material',direction:null,timeMs:0}):null;
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
  observeEntities(entities,options){status.lastGather=null;status.lastBuildingDeath=null;if(enabled)locomotion.observe(entities,options);},
  drawTransitions(ctx,options){if(!enabled||!ready)return false;return transitions.draw(ctx,options);},
  async preload(){if(!enabled)return this;await pipeline.preload();ready=true;status.quality=pipeline.stats.status;return this;},
  /** project uses existing renderer logical pixels; camera zoom and DPR must not be applied twice. */
  drawGround(ctx,{x,y,terrain,project,zoom=1,timeMs=0}={}) {
   if(!enabled||!ready||!finite(x)||!finite(y)||typeof project!=='function'||!finite(zoom)||zoom<=0)return false;
   const water=['river','sea'].includes(terrain),ford=terrain==='ford';if(!water&&!ford&&!['plain','forest','hill'].includes(terrain)&&!(terrain==='mountain'&&mountainReady())){recordMissing(`ground:${terrain}`,'No authored material for this terrain');return false;}
   const raster=(terrain==='mountain'?mountainGround():null)||select({families:ford?['ford','terrain.ford']:water?['water','terrain.water']:['grass','terrain.grass'],kind:'terrain',state:'material',direction:null,timeMs});if(!raster)return false;
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
   if(!enabled||!ready||!['forest','mountain'].includes(type)||typeof project!=='function'||!finite(x)||!finite(y))return false;
   const raster=select({families:type==='mountain'?['mountain','prop.mountain']:['forest','prop.forest'],kind:'prop',state:'static',direction:null,variant,timeMs});if(!raster)return false;
   if(rasterAt(ctx,raster,project(x,y),zoom)){status.propDraws++;return true;}return false;
  },
  drawHillGround(ctx,{state,project,zoom=1,timeMs=0}={}) {
   if(!enabled||!ready||!worldArtEnabled()||typeof project!=='function')return 0;
   const raster=select({families:['hill'],kind:'prop',state:'static',direction:null,timeMs});
   const placements=hillGroundPlacements(state,Boolean(raster?.image));let drawn=0;
   for(const p of placements){if(p.drawOverlay===false)continue;ctx.save();ctx.beginPath();for(const cell of p.cells){const q=project(cell.x+.5,cell.y+.5),rx=TW*zoom/2,ry=TH*zoom/2;ctx.moveTo(q.x,q.y-ry);ctx.lineTo(q.x+rx,q.y);ctx.lineTo(q.x,q.y+ry);ctx.lineTo(q.x-rx,q.y);ctx.closePath();}ctx.clip();if(rasterAt(ctx,raster,project(p.artX??p.x,p.artY??p.y),zoom))drawn++;ctx.restore();}
   status.hillDraws=(status.hillDraws||0)+drawn;return drawn;
  },
  drawResource(ctx,{resource,project,zoom=1,timeMs=0}={}) {
   if(!enabled||!ready||!worldArtEnabled()||!staticResourceEligible(resource)||typeof project!=='function')return false;
   const raster=select({families:[resource.type,`resource.${resource.type}`],kind:'prop',state:'static',direction:null,timeMs});if(!raster)return false;
   if(rasterAt(ctx,raster,project(resource.x,resource.y),zoom)){const key=resource.type==='iron'?'ironResourceDraws':'foodResourceDraws';status[key]=(status[key]||0)+1;return true;}return false;
  },
  sampleEntity(entity,{tick=0,timeMs=tick*50,fortificationTopology}={}) {
   if(!enabled||!ready||!entity||entity.embarked||!finite(entity.x)||!finite(entity.y))return false;
   let families,kind,direction;
   if(entity.kind==='building'){if(['wall','gate'].includes(entity.type)&&!['fort','stone'].includes(artRoute().name))return false;if(!['residence','granary','wall','gate'].includes(entity.type)&&!(['barracks','depot','artilleryWorkshop','cavalryCamp'].includes(entity.type)&&worldArtEnabled())&&!(entity.type==='shipyard'&&['shipyard','fort'].includes(artRoute().name) )&&!(entity.type==='fort'&&artRoute().name==='fort'))return false;families=[entity.type,`building.${entity.type}`];kind='building';direction=null;}
   else {families=unitArtFamilies(entity);if(!families)return false;kind='unit';direction=entity.dir;}
   const state=normalState(entity);if(typeof state!=='string'||!(direction===null||Number.isInteger(direction)&&direction>=0&&direction<=7))return false;
   // Exact authored actions have priority. Missing living-unit actions may retain a diagnosed static illustration.
   const baseVisualState=state!=='construction'&&entity.hp>0&&(entity.hitUntil||0)>tick?'hit':state;
   const states=authoredActionStates(entity,baseVisualState);let candidates=[],visualState=baseVisualState;
   for(const requested of states){candidates=(pipeline.manifest?.assets||[]).filter(a=>a.kind===kind&&families.includes(a.family||a.id)&&a.state===requested&&a.direction===direction);if(candidates.length){visualState=requested;break;}}
   const requestedState=baseVisualState,requestedDirection=direction;let staticIllustrationFallback=false;
   if(!candidates.length){
    recordMissing(`${families[0]}:${visualState}:${direction}`,'No exact authored raster state/direction');
    // Preserve identity and life/construction state; never depict a dead or unfinished entity as idle.
    if(entity.hp>0&&state!=='death'&&state!=='construction'&&(kind==='unit'||kind==='building'&&baseVisualState==='hit'&&!['wall','gate'].includes(entity.type))){
     const idle=(pipeline.manifest?.assets||[]).filter(a=>a.kind===kind&&families.includes(a.family||a.id)&&a.state==='idle');
     candidates=idle.filter(a=>a.direction===direction);
     if(!candidates.length&&kind==='unit')candidates=idle.filter(a=>a.direction===0);
     if(candidates.length){visualState='idle';direction=candidates[0].direction;staticIllustrationFallback=true;}
    }
    if(!candidates.length)return false;
   }
   let asset=candidates[0];if(kind==='building'&&['wall','gate'].includes(entity.type)){const chosen=selectFortificationArt(pipeline.manifest.assets,entity,fortificationTopology,visualState);if(!chosen.asset){recordMissing(`${entity.type}:${visualState}:topology`,chosen.reason);return false;}asset=chosen.asset;}let elapsed=timeMs;
   let walkPhase=null;
   // Construction loops describe visible activity, never private completion progress.
   if(staticIllustrationFallback)elapsed=0;
   else if(visualState==='construction')elapsed=Math.max(0,tick*50);
   else if(visualState==='walk'&&asset.locomotion){walkPhase=locomotion.sample(entity.id,{distancePerCycle:asset.locomotion.distancePerCycle,cycleDurationMs:asset.frames.reduce((sum,f)=>sum+f.durationMs,0)});elapsed=walkPhase.timeMs;}
   else if(visualState==='gather'||visualState.startsWith('gather_'))elapsed=gatherAnimationTime(entity,timeMs);
   else if(visualState==='hit')elapsed=Math.max(0,timeMs-((entity.hitUntil||tick)-6)*50);
   else if(visualState==='death')elapsed=Math.max(0,(kind==='building'?(asset.fortification?.deathSite==='completed'?Math.min(tick*50,finite(timeMs)?timeMs:tick*50):tick*50):timeMs)-(entity.deadTick??tick)*50);
   else if(visualState==='attack'&&finite(entity.attackStartedTick??entity.lastAttack))elapsed=attackAnimationTime(asset,entity,timeMs);
   const sample=sampleSpriteAnimation(asset.frames,{timeMs:elapsed,loop:defaultAnimationLoop(asset)});
   const raster=pipeline.get(asset.id,{state:visualState,direction,timeMs:elapsed,frame:sample.frame});if(!raster.image){recordMissing(asset.id,raster.reason);return false;}
   return {raster,visualState,walkPhase,sample,direction,elapsed,requestedState,requestedDirection,staticIllustrationFallback,presentation:staticIllustrationFallback?'STATIC_ILLUSTRATION':'AUTHORED'};
  },
  drawEntity(ctx,entity,{project,zoom=1,tick=0,timeMs=tick*50,fortificationTopology}={}) {
   if(typeof project!=='function')return false;const result=this.sampleEntity(entity,{tick,timeMs,fortificationTopology});if(!result)return false;const {raster,visualState,walkPhase,sample,direction,elapsed}=result,asset=raster.asset;
   if(rasterAt(ctx,raster,project(entity.x,entity.y),zoom)){status.entityDraws++;if(result.staticIllustrationFallback){status.staticIllustrationDraws=(status.staticIllustrationDraws||0)+1;status.lastStaticIllustration={entityId:entity.id,assetId:asset.id,requestedState:result.requestedState,requestedDirection:result.requestedDirection,illustrationDirection:direction,presentation:'STATIC_ILLUSTRATION'};}if(visualState==='death'&&entity.kind==='building'){status.buildingDeathDraws++;status.lastBuildingDeath={entityId:entity.id,assetId:asset.id,frame:sample.frame,tick,deadTick:entity.deadTick??tick,elapsedMs:elapsed,presentationTimeMs:timeMs};}if(['gather_wood','gather_food','gather_iron'].includes(visualState)&&entity.type==='villager'){status.gatherDraws++;status.lastGather={entityId:entity.id,frame:sample.frame,direction,assetId:asset.id,visualState,startedTick:entity.visibleAction?.startedTick??null,elapsedMs:sample.elapsedMs,timeMs:elapsed,presentationTimeMs:timeMs};}if(walkPhase){status.walkDraws++;status.lastWalk={entityId:entity.id,frame:sample.frame,distance:walkPhase.distance,distancePerCycle:asset.locomotion.distancePerCycle,direction};}else if(visualState==='idle'&&asset.family==='unit.villager')status.idleDraws++;return true;}return false;
  },
  /** Deterministic existing forest density, sorted ready for a merged prop/entity depth queue. */
  propsForState(state,{onlyVisible=true}={}) {
   if(!enabled||!state?.map?.tiles)return [];
   const {width,height,tiles}=state.map,props=[];
   for(let y=0;y<height;y++)for(let x=0;x<width;x++){const index=y*width+x,v=(x*17+y*31)%19;if(tiles[index]!=='forest'||v>=5||onlyVisible&&state.fog?.visible&&!state.fog.visible[index])continue;props.push({type:'forest',x:x+.5,y:y+.5,variant:v,key:`forest:${x}:${y}`,depth:x+y});}
   props.push(...mountainPropPlacements(state,mountainReady(),{onlyVisible,clustered:Boolean(mountainGround()?.image)}));return props.sort((a,b)=>a.depth-b.depth||a.y-b.y||a.x-b.x);
  },
  dispose(){locomotion.clear();transitions.dispose();transitionMaterials.clear();pipeline.dispose();cells.clear();ready=false;}
 };
}
