import {createPixelSpriteBank} from './pixel-sprite-bank.js';
import {PIXEL_DIRECTIONS} from './pixel-animation.js';
/** Preview-only episode fields. Never sends commands or alters a game entity. */
export function startPixelPreviewEpisode(entity,clip,{action=clip?.action??'idle',timeMs=0,instance=0}={}){
 const startTimeMs=Math.ceil(timeMs/50)*50,startedTick=startTimeMs/50;
 for(const key of ['visibleAction','attackStartedTick','attackImpactTick','attackReadyTick','lastAttack','hitUntil'])delete entity[key];
 entity.createdTick=instance;entity.state=action==='chop_tree'?'gather':action;
 const total=clip?.frameDurationsMs.reduce((a,b)=>a+b,0)??800,endTick=startedTick+Math.max(1,Math.ceil(total/50));
 if(['ability','load','unload','build'].includes(action))entity.visibleAction={kind:action,startedTick,endTick,loop:clip?.loop===true};
 if(action==='chop_tree'||action.startsWith('gather_'))entity.visibleAction={kind:'gather',resource:action==='chop_tree'?'wood':action.slice(7),startedTick};
 if(action==='hit')entity.hitUntil=startedTick+5;
 if(action==='attack'){
  const event=clip?.events.find(e=>['WEAPON_CONTACT','DEAL_DAMAGE','FIRE_PROJECTILE'].includes(e.name));
  const contact=event?clip.frameDurationsMs.slice(0,event.frame).reduce((a,b)=>a+b,0):total/2;
  entity.attackStartedTick=startedTick;entity.attackImpactTick=startedTick+Math.max(1,Math.ceil(contact/50));entity.attackReadyTick=Math.max(entity.attackImpactTick+1,endTick);entity.lastAttack=-1;
 }
 return {startTimeMs,missing:!clip};
}
export async function mountPixelSpriteViewer(host=document,{bankOptions={}}={}){
const $=id=>host.querySelector('#'+id),bank=createPixelSpriteBank(bankOptions),canvas=host.querySelector('canvas'),ctx=canvas.getContext('2d');
let disposed=false,animationFrame=null;
const dispose=()=>{disposed=true;if(animationFrame!==null)cancelAnimationFrame(animationFrame);};
if(host!==document)host.addEventListener('close',dispose,{once:true});
let paused=false,timeMs=0,last=performance.now(),distance=0,episode=0,fresh=true;
const entity={id:'viewer',kind:'unit',type:'villager',hp:1,x:0,y:0,dir:1,state:'idle'};
for(let row=0;row<8;row++)$('direction').add(new Option(PIXEL_DIRECTIONS[row],String((row+1)%8)));
function restart(action=$('action').value){fresh=true;const clip=bank.registry.clips.find(c=>c.identity===$('identity').value&&c.action===action);timeMs=startPixelPreviewEpisode(entity,clip,{action,timeMs,instance:++episode}).startTimeMs;bank.observeEntities([entity],{tick:timeMs/50,timeMs,frozen:paused});if(!clip)$('status').textContent=`MISSING: ${entity.type}/${action} clip absent`;}

function actions(){const clips=bank.registry.clips.filter(c=>c.identity===$('identity').value);$('action').replaceChildren(...[...new Set(clips.map(c=>c.action))].map(a=>new Option(a,a)));restart();}
$('identity').onchange=()=>{entity.type=$('identity').value;actions();};$('action').onchange=()=>restart();$('pause').onclick=()=>{paused=!paused;$('pause').textContent=paused?'Resume':'Pause';};$('stop').onclick=()=>{$('action').value='idle';restart('idle');};
try{await bank.preload();const ids=[...new Set(bank.registry.clips.map(c=>c.identity))];$('identity').replaceChildren(...ids.map(id=>new Option(id,id)));if(ids.length){entity.type=ids[0];actions();$('status').textContent=`${bank.status.clips} registry clips · ${bank.status.candidateOnly?'PRIVATE CANDIDATE / UNQUALIFIED':'all review fields PASS'}`;for(const c of bank.registry.clips){const a=document.createElement('a');a.href=c.atlas.replace(/\.png$/,'.gif');a.textContent=`${c.identity} ${c.action} GIF (if compiled)`;a.style.display='block';$('gifs').appendChild(a);}}else{$('status').textContent='MISSING: registry empty · zero accepted pixel poses';$('identity').disabled=$('action').disabled=true;$('gifs').textContent='GIF previews missing: no selected pixel artwork.';}}catch(error){$('status').textContent=`ERROR: ${error.message}`;}
function frame(now){if(disposed||(host!==document&&!host.open))return;const dt=fresh?0:Math.min(100,now-last);fresh=false;last=now;if(!paused){timeMs+=dt;if(entity.state==='walk'){distance+=dt/1000;entity.x=distance;}}if(entity.visibleAction?.loop)entity.visibleAction.endTick=Math.max(entity.visibleAction.endTick,Math.ceil(timeMs/50)+1);entity.dir=Number($('direction').value);bank.observeEntities([entity],{tick:Math.floor(timeMs/50),timeMs,frozen:paused});ctx.clearRect(0,0,256,256);const sample=bank.sampleEntity(entity);bank.drawEntity(ctx,entity,{point:{x:128,y:160},zoom:1,sample});$('detail').textContent=sample.missing?sample.reason:`Frame ${sample.frame??'missing'} · row ${sample.row??'?'}${sample.unqualified?' · UNQUALIFIED: '+sample.reason:''}`;animationFrame=requestAnimationFrame(frame);}if(!disposed&&(host===document||host.open))animationFrame=requestAnimationFrame(frame);
return {dispose,bank};

}
