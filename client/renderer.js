import {buildFortificationTopology,fortificationSpans} from './fortification-topology.js';
import {createArtBank} from './art-bank.js';
import {drawTerrainPropFallback} from './terrain-props.js';
import {createImpactPulses} from './action-presentation.js';
import { BUILDINGS, UNITS, TICK_RATE } from '../shared/data.js';
import { createRasterSlice } from './raster-slice.js';
import { pickVisibleEntity } from './visual-picking.js';
import { createTerrainCache } from './terrain-cache.js';

import { TILE_WIDTH as TW, TILE_HEIGHT as TH } from './world-presentation.js';
const palette={plain:'#73895d',forest:'#355d43',hill:'#8a8c63',mountain:'#817b68',river:'#4d887f',sea:'#386e6e',ford:'#69948a'};
const clamp=(n,a,b)=>Math.max(a,Math.min(b,n));
function facing(dir){const d=((Math.round(Number(dir)||0)%8)+8)%8,a=d*Math.PI/4,dx=Math.cos(a),dy=Math.sin(a);return{d,dx,dy,screenX:dx-dy,screenY:(dx+dy)*TH/TW,angle:Math.atan2((dx+dy)*TH,(dx-dy)*TW)};}
const LEADER_STYLE={
 han_xin:{kind:'armor',coat:'#9a4d43',armor:'#9b9e94',trim:'#d0c5a8',hat:'knot',weapon:'staff',cape:'#8f3e38'},
 xiang_yu:{kind:'armor',coat:'#893f36',armor:'#b8b8aa',trim:'#dfd7be',hat:'crest',weapon:'sword',cape:'#762f2d'},
 napoleon_bonaparte:{kind:'coat',coat:'#274965',armor:'#d6d1bf',trim:'#c8a857',hat:'bicorne',weapon:'sword',cape:'#8b3733',pants:'#e5dfcd'},
 ly_thuong_kiet:{kind:'armor',coat:'#6d3330',armor:'#71776d',trim:'#bfae8d',hat:'knot',weapon:'sword',cape:'#552d2c'},
 tran_hung_dao:{kind:'armor',coat:'#843c35',armor:'#6e736e',trim:'#c9c1ac',hat:'helmet',weapon:'sword',cape:'#9f3d37',beard:true},
 nguyen_hue:{kind:'armor',coat:'#992f31',armor:'#a45b45',trim:'#e0c474',hat:'crest',weapon:'sword',cape:'#a92f31'},
 le_thanh_tong:{kind:'robe',coat:'#c39637',armor:'#d4b556',trim:'#e6d78e',hat:'official',weapon:'staff'},
 minh_menh:{kind:'robe',coat:'#d17031',armor:'#dc9844',trim:'#eed076',hat:'crown',weapon:'staff'},
 nguyen_anh:{kind:'robe',coat:'#c5973f',armor:'#d2b65e',trim:'#e1d38f',hat:'official',weapon:'staff'},
 nguyen_phuc_chu:{kind:'robe',coat:'#273c58',armor:'#40546e',trim:'#b2a580',hat:'knot',weapon:'staff'},
 tran_nhan_tong:{kind:'robe',coat:'#9f4039',armor:'#bd6550',trim:'#d0b27b',hat:'knot',weapon:'staff'},
 trinh_cuong:{kind:'robe',coat:'#4f344e',armor:'#674864',trim:'#c3aa80',hat:'official',weapon:'staff'}
};
export class IsoRenderer{
 constructor(canvas,minimap){this.canvas=canvas;this.ctx=canvas.getContext('2d');this.minimap=minimap;this.mctx=minimap.getContext('2d');this.camera={x:24,y:24,zoom:1};this.state=null;this.localPlayer=0;this.selected=[];this.dpr=1;this.artBank=createArtBank();this.raster=createRasterSlice();this.artBank.attach(this.raster.pipeline);this.terrainCache=createTerrainCache();this.impactPulses=createImpactPulses();this.resize();window.addEventListener('resize',()=>this.resize());}
 async preloadArt(){if(this.raster.status.enabled)await this.artBank.prime(this.raster.pipeline);}
 releaseArt(){this.fortificationTopology=null;this.artBank.release();this.raster.dispose();this.terrainCache.dispose();this.state=null;this.selected=[];this.raster=createRasterSlice();this.artBank.attach(this.raster.pipeline);}
 async activateArt(state){this.raster.dispose();this.terrainCache.dispose();this.raster=createRasterSlice();this.artBank.attach(this.raster.pipeline);if(!this.raster.status.enabled)return true;const raster=this.raster;const active=await this.artBank.activate(raster.pipeline,state);if(active&&this.raster===raster)await raster.preload();return active&&this.raster===raster;}
 resize(){const r=this.canvas.getBoundingClientRect();this.dpr=Math.min(2,window.devicePixelRatio||1);this.canvas.width=Math.max(1,Math.floor(r.width*this.dpr));this.canvas.height=Math.max(1,Math.floor(r.height*this.dpr));}
 project(x,y){const w=this.canvas.width/this.dpr,h=this.canvas.height/this.dpr,z=this.camera.zoom;return {x:w/2+(x-y)*TW*z/2-(this.camera.x-this.camera.y)*TW*z/2,y:h/2+(x+y-this.camera.x-this.camera.y)*TH*z/2};}
 unproject(px,py){const w=this.canvas.width/this.dpr,h=this.canvas.height/this.dpr,z=this.camera.zoom;const dx=(px-w/2+(this.camera.x-this.camera.y)*TW*z/2)/(TW*z/2),dy=(py-h/2+(this.camera.x+this.camera.y)*TH*z/2)/(TH*z/2);return {x:(dx+dy)/2,y:(dy-dx)/2};}
 render(state,player,selected,delta=0,{visualTimeMs=state?.tick*50||0,frozen=false}={}){this.visualTimeMs=visualTimeMs;this.raster.observeEntities(state?.entities||[],{tick:state?.tick||0,timeMs:visualTimeMs,frozen});this.impactPulses.update(state?.entities||[],state?.tick||0,delta,{frozen});this.presentationNow=delta;this.state=state;this.localPlayer=player;this.selected=selected||[];const ctx=this.ctx,w=this.canvas.width/this.dpr,h=this.canvas.height/this.dpr,z=this.camera.zoom;ctx.setTransform(this.dpr,0,0,this.dpr,0,0);ctx.clearRect(0,0,w,h);ctx.fillStyle='#355a53';ctx.fillRect(0,0,w,h);if(!state?.map)return;const {width,height,tiles}=state.map;const radius=Math.ceil((w/(TW*z)+h/(TH*z))/2)+3;const cx=this.camera.x,cy=this.camera.y;const materials=(this.raster.pipeline.manifest?.assets||[]).filter(a=>a.kind==='terrain'&&a.state==='material');const artRevision=this.raster.pipeline.stats.ready+':'+materials.map(a=>a.runtime.sha256+':'+this.raster.pipeline.get(a.id,{timeMs:state.tick*50}).frame).join('|');const cached=this.raster.status.enabled&&this.terrainCache.draw(ctx,{map:state.map,artRevision,qualityScale:this.dpr,project:(x,y)=>this.project(x,y),zoom:z,paintTile:(cacheCtx,{x,y,terrain,project,zoom,point})=>this.drawTile(cacheCtx,x,y,point,terrain,{zoom,project})});if(!cached)for(let y=Math.max(0,Math.floor(cy-radius));y<Math.min(height,Math.ceil(cy+radius));y++)for(let x=Math.max(0,Math.floor(cx-radius));x<Math.min(width,Math.ceil(cx+radius));x++){const p=this.project(x+.5,y+.5);if(p.x<-TW||p.x>w+TW||p.y<-TH||p.y>h+TH)continue;this.drawTile(ctx,x,y,p,tiles[y*width+x]||'plain');}
 this.raster.drawTransitions(ctx,{map:state.map,fog:state.fog,project:(x,y)=>this.project(x,y),zoom:z,timeMs:state.tick*50});
 this.raster.drawHillGround(ctx,{state,project:(x,y)=>this.project(x,y),zoom:z,timeMs:state.tick*50});
 const resources=(state.map.resources||[]).filter(r=>r.amount>0&&this.visible(xy(r),state,player));
 const entities=(state.entities||[]).filter(e=>!e.embarked&&this.visible(e,state,player));
 this.fortificationTopology=buildFortificationTopology(entities);
 const props=this.raster.propsForState(state).filter(e=>{const p=this.project(e.x,e.y);return p.x>-90*z&&p.x<w+90*z&&p.y>-90*z&&p.y<h+90*z;});
 const depthQueue=[...entities.map(e=>({entity:e,x:e.x,y:e.y})),...props.map(e=>({prop:e,x:e.x,y:e.y})),...resources.map(e=>({resource:e,x:e.x,y:e.y}))].sort((a,b)=>(a.x+a.y)-(b.x+b.y));
 for(const item of depthQueue){if(item.entity)this.drawEntity(ctx,item.entity,delta);else if(item.resource)this.drawResource(ctx,item.resource);else if(!this.raster.drawProp(ctx,{...item.prop,project:(x,y)=>this.project(x,y),zoom:z,timeMs:state.tick*50})){drawTerrainPropFallback(this,ctx,item.prop,z);}}
 const fog=state.fog;if(fog?.visible){
  // Fill each fog region as one path: shared cell edges must not accumulate antialias seams.
  for(const explored of [true,false]){ctx.beginPath();for(let y=0;y<height;y++)for(let x=0;x<width;x++){const index=y*width+x;if(fog.visible[index]||Boolean(fog.explored?.[index])!==explored)continue;const p=this.project(x+.5,y+.5);if(p.x<=-TW||p.x>=w+TW||p.y<=-TH||p.y>=h+TH)continue;const rx=TW*z/2,ry=TH*z/2;ctx.moveTo(p.x,p.y-ry);ctx.lineTo(p.x+rx,p.y);ctx.lineTo(p.x,p.y+ry);ctx.lineTo(p.x-rx,p.y);ctx.closePath();}ctx.fillStyle=explored?'rgba(12,28,24,.35)':'rgba(8,23,21,.85)';ctx.fill();}
 }
 this.drawMinimap(state,player);
 }
 selectionPoint(e){const p=this.project(e.x,e.y),z=this.camera.zoom;for(const dy of [-15,-24,-8,-32,0])for(const dx of [0,-4,4]){const point={x:p.x+dx*z,y:p.y+dy*z};if(pickVisibleEntity(this,point.x,point.y)?.id===e.id)return point;}return p;}
 pickEntity(x,y){const p=this.project(x,y);return pickVisibleEntity(this,p.x,p.y);}
 visible(e,s,p){if(e.owner===p||!s.fog?.visible)return true;const i=Math.floor(e.y)*s.map.width+Math.floor(e.x);return !!s.fog.visible[i];}
 drawTile(c,x,y,p,t,{zoom=this.camera.zoom,project=(x,y)=>this.project(x,y)}={}){const z=zoom,half=TW*z/2,hh=TH*z/2;if(this.raster.drawGround(c,{x:x+.5,y:y+.5,terrain:t,project,zoom:z,timeMs:(this.state?.tick||0)*50}))return;c.fillStyle=palette[t]||palette.plain;this.diamond(c,p.x,p.y,half,hh);c.strokeStyle='rgba(212,208,164,.075)';c.lineWidth=.65;this.diamondStroke(c,p.x,p.y,half,hh);const v=(x*17+y*31)%19;if(t==='forest'&&v<5&&!this.raster.status.enabled){this.tree(c,p.x,p.y,z,v);}else if(t==='hill'&&v<4){c.fillStyle='#a6a07755';this.diamond(c,p.x-2*z,p.y-1*z,half*.55,hh*.45);}else if(t==='mountain'){this.rock(c,p.x,p.y,z,v);}else if(t==='river'||t==='sea'){if(v<5){c.strokeStyle='rgba(190,213,183,.22)';c.lineWidth=z;c.beginPath();c.moveTo(p.x-5*z,p.y-1*z);c.lineTo(p.x+4*z,p.y+1*z);c.stroke();}}}
 rock(c,x,y,z,v){c.fillStyle='#4d594e';c.beginPath();c.moveTo(x-8*z,y);c.lineTo(x-6*z,y-8*z);c.lineTo(x-2*z,y-12*z);c.lineTo(x+2*z,y-7*z);c.lineTo(x+6*z,y-9*z);c.lineTo(x+10*z,y-1*z);c.closePath();c.fill();c.fillStyle='#9c9985';c.beginPath();c.moveTo(x-6*z,y-8*z);c.lineTo(x-2*z,y-12*z);c.lineTo(x+1*z,y-7*z);c.lineTo(x-2*z,y-5*z);c.fill();c.fillStyle='#626b59';c.beginPath();c.moveTo(x+2*z,y-7*z);c.lineTo(x+6*z,y-9*z);c.lineTo(x+10*z,y-1*z);c.lineTo(x+2*z,y+1*z);c.fill();}
 diamond(c,x,y,rx,ry){c.beginPath();c.moveTo(x,y-ry);c.lineTo(x+rx,y);c.lineTo(x,y+ry);c.lineTo(x-rx,y);c.closePath();c.fill();}
 diamondStroke(c,x,y,rx,ry){c.beginPath();c.moveTo(x,y-ry);c.lineTo(x+rx,y);c.lineTo(x,y+ry);c.lineTo(x-rx,y);c.closePath();c.stroke();}
 tree(c,x,y,z,v){const col=['#2c4f39','#355a3d','#466649','#31553e','#58704a'][v%5];c.fillStyle='#4b3d2a';c.fillRect(x-1.7*z,y-3*z,3*z,6*z);c.fillStyle=col;c.beginPath();c.arc(x,y-8*z,6.5*z,0,Math.PI*2);c.arc(x-4*z,y-5*z,5*z,0,Math.PI*2);c.arc(x+4*z,y-4*z,4*z,0,Math.PI*2);c.fill();}
 drawResource(c,r){if(!(r.amount>0))return;if(this.raster.drawResource(c,{resource:r,project:(x,y)=>this.project(x,y),zoom:this.camera.zoom,timeMs:(this.state?.tick||0)*50}))return;const p=this.project(r.x,r.y),z=this.camera.zoom;c.save();if(r.type==='wood'||r.type==='forest'){if(!this.raster.drawProp(c,{x:r.x,y:r.y,type:'forest',project:(x,y)=>this.project(x,y),zoom:z,timeMs:(this.state?.tick||0)*50}))this.tree(c,p.x,p.y,z,1);}else if(r.type==='food'){c.fillStyle='#dab872';c.beginPath();c.arc(p.x,p.y-2*z,5*z,0,Math.PI*2);c.fill();c.fillStyle='#67814c';c.fillRect(p.x-1*z,p.y-8*z,2*z,7*z);}else{c.fillStyle='#a6aaa0';c.beginPath();c.moveTo(p.x,p.y-9*z);c.lineTo(p.x+6*z,p.y-4*z);c.lineTo(p.x+4*z,p.y+2*z);c.lineTo(p.x-4*z,p.y+2*z);c.lineTo(p.x-6*z,p.y-4*z);c.fill();c.fillStyle='#d2b874';c.fillRect(p.x-2*z,p.y-6*z,2*z,3*z);}c.restore();}
 drawEntity(c,e,dt){const p=this.project(e.x,e.y),z=this.camera.zoom,isBuilding=e.kind==='building';if(this.selected.includes(e.id)&&e.hp>0){c.strokeStyle='#e8ca75';c.lineWidth=1.4;c.beginPath();c.ellipse(p.x,p.y+2*z,18*z,8*z,0,0,Math.PI*2);c.stroke();}
 const authored=this.raster.drawEntity(c,e,{project:(x,y)=>this.project(x,y),zoom:z,tick:this.state?.tick||0,timeMs:this.visualTimeMs,fortificationTopology:this.fortificationTopology});
 if(!authored){if(isBuilding)this.drawBuilding(c,e,p,z);else{c.fillStyle=e.owner===this.localPlayer?'#d8c16f':'#d6775b';c.beginPath();c.ellipse(p.x,p.y+2*z,8*z,4*z,0,0,Math.PI*2);c.fill();this.drawUnit(c,e,p,z,dt);}}
 const hp=(e.hp??0)/(e.maxHp||1);if(hp<.995&&e.hp>0){const bw=(isBuilding?38:24)*z,by=p.y-(isBuilding?36:37)*z;c.fillStyle='#311e1a';c.fillRect(p.x-bw/2,by,bw,3*z);c.fillStyle=hp>.5?'#92b37c':'#c3694e';c.fillRect(p.x-bw/2,by,bw*clamp(hp,0,1),3*z);}
 if(e.owner===this.localPlayer&&e.foodMax&&e.hp>0&&(this.selected.includes(e.id)||(e.food||0)<e.foodMax*.25)){c.fillStyle='#d8bd76';c.fillRect(p.x-8*z,p.y+8*z,16*z*clamp((e.food||0)/e.foodMax,0,1),1.8*z);}
 }
 drawUnit(c,e,p,z,dt){const type=e.type,team=e.owner===this.localPlayer?'#d6d0ae':'#c27961',moving=e.state==='walk'||e.state==='carry'||e.state==='gather'||e.state==='build',swing=moving?Math.sin(this.visualTimeMs/95+(e.id||0)):Math.sin(this.visualTimeMs/560+(e.id||0))*.09,breath=Math.sin(this.visualTimeMs/510+(e.id||0))*.45,attack=e.state==='attack',dir=facing(e.dir),hit=(e.hitUntil||0)>(this.state?.tick||0),dead=e.state==='death'||e.hp<=0;
 if(dead){this.drawCorpse(c,e,p,z,dir,team);return;}
 if(type==='warship'||type==='transport'){this.drawShip(c,e,p,z,dir,team,hit,attack);return;}
 if(type==='wagon'||type==='artillery'){this.drawWagon(c,e,p,z,dir,team,hit,attack);return;}
 if(type==='cavalry'){this.drawCavalry(c,e,p,z,dir,team,hit,attack,swing);return;}
 this.drawFoot(c,e,p,z,dir,team,hit,attack,moving,swing,breath);
 }
 drawFoot(c,e,p,z,dir,team,hit,attack,moving,swing,breath){
  const type=e.type,major=type==='king'||type==='general',style=major?LEADER_STYLE[e.character]:null,villager=type==='villager',spearman=type==='spearman',gunner=type==='firearm',rear=dir.d>=5,front=dir.d>=1&&dir.d<=3,side=dir.d===0||dir.d===4;
  const cloth=hit?'#ec745d':style?.coat||(major?(type==='king'?'#844b3c':'#405a49'):villager?'#6b805c':gunner?'#415044':'#45584a');
  const stride=moving?swing*3.2:breath*.15,weaponReach=attack?7+Math.max(0,Math.sin(this.visualTimeMs/75))*7:0,mag=Math.hypot(dir.screenX,dir.screenY)||1,fx=dir.screenX/mag,fy=dir.screenY/mag;
  const weaponX=(fx<-.2?-5:5)*z,sx=weaponX,sy=-13*z,weaponLen=(gunner?14:spearman?22:style?.weapon==='staff'?20:12)*z,tx=sx+fx*(weaponLen+weaponReach*z),ty=sy+fy*(weaponLen+weaponReach*z),torsoW=(side?3.6:4.7)*z;
  c.save();c.translate(p.x,p.y+Math.sin(this.visualTimeMs/150+(e.id||0))*.4*z);
  c.fillStyle='#312d24';c.beginPath();c.ellipse(0,0,5.8*z,2.8*z,0,0,Math.PI*2);c.fill();
  const drawWeapon=()=>{const staff=style?.weapon==='staff',sword=style?.weapon==='sword'||type==='infantry';c.strokeStyle=gunner?'#443d2f':staff?'#765536':sword?'#d7d0b6':'#d5c69f';c.lineWidth=(gunner?2.5:staff?1.6:1.1)*z;c.beginPath();c.moveTo(sx,sy);c.lineTo(tx,ty);c.stroke();if(spearman||staff){c.fillStyle=staff?'#d0b675':'#ddd0a8';c.beginPath();c.moveTo(tx+fx*3*z,ty+fy*3*z);c.lineTo(tx-fy*1.7*z,ty+fx*1.7*z);c.lineTo(tx+fy*1.7*z,ty-fx*1.7*z);c.fill();}if(sword){c.fillStyle='#d7d0b6';c.beginPath();c.moveTo(tx,ty);c.lineTo(tx+fx*3*z-fy*1.2*z,ty+fy*3*z+fx*1.2*z);c.lineTo(tx+fx*4*z,ty+fy*4*z);c.closePath();c.fill();c.strokeStyle='#b79b63';c.lineWidth=1.3*z;c.beginPath();c.moveTo(sx-fy*2*z,sy+fx*2*z);c.lineTo(sx+fy*2*z,sy-fx*2*z);c.stroke();}if(gunner){c.fillStyle='#c7b982';c.fillRect(sx-2*z,sy-2*z,4*z,2*z);if(this.impactPulses.active(e.id,this.presentationNow)){c.fillStyle='#f5d576';c.beginPath();c.arc(tx,ty,2.6*z,0,Math.PI*2);c.fill();}}};
  // The far-hand weapon is painted behind the body on north-facing sectors; near-hand kit stays above it.
  if(rear)drawWeapon();
  c.strokeStyle=hit?'#ffd2a3':'#3b4034';c.lineWidth=2.5*z;c.lineCap='round';c.beginPath();c.moveTo(-2.5*z,-8*z);c.lineTo((-3.4+stride)*z,-1*z);c.moveTo(2.5*z,-8*z);c.lineTo((3.4-stride)*z,-1*z);c.stroke();
  c.fillStyle=villager?'#655344':'#62573e';c.fillRect((-5+stride)*z,-1.2*z,4*z,1.7*z);c.fillRect((1-stride)*z,-1.2*z,4*z,1.7*z);
  if(style?.kind==='robe'){
   c.fillStyle=cloth;c.beginPath();c.moveTo(-5*z,-18*z);c.lineTo(5*z,-18*z);c.lineTo(8*z,-2*z);c.lineTo(-8*z,-2*z);c.closePath();c.fill();
   if(!rear){c.fillStyle=style.trim;c.beginPath();c.moveTo(-5*z,-18*z);c.lineTo(-3.5*z,-18*z);c.lineTo(-5.4*z,-3*z);c.lineTo(-7*z,-3*z);c.closePath();c.fill();c.beginPath();c.moveTo(3.5*z,-18*z);c.lineTo(5*z,-18*z);c.lineTo(7*z,-3*z);c.lineTo(5.4*z,-3*z);c.closePath();c.fill();c.fillStyle=style.armor;c.fillRect(-5*z,-12*z,10*z,1.5*z);}else{c.fillStyle='rgba(36,34,31,.34)';c.beginPath();c.moveTo(0,-17*z);c.lineTo(5*z,-15*z);c.lineTo(4*z,-3*z);c.lineTo(0,-1*z);c.lineTo(-4*z,-3*z);c.lineTo(-5*z,-15*z);c.closePath();c.fill();c.strokeStyle=style.trim;c.lineWidth=.7*z;c.beginPath();c.moveTo(0,-15*z);c.lineTo(0,-3*z);c.stroke();}
   c.fillStyle=cloth;c.fillRect(-8*z,-17*z,4*z,5*z);c.fillRect(4*z,-17*z,4*z,5*z);
  }else if(style?.kind==='coat'){
   c.fillStyle=style.pants;c.fillRect(-4.5*z,-8*z,3*z,7*z);c.fillRect(1.5*z,-8*z,3*z,7*z);c.fillStyle=cloth;c.beginPath();c.moveTo(-5*z,-18*z);c.lineTo(5*z,-18*z);c.lineTo(4*z,-8*z);c.lineTo(-4*z,-8*z);c.closePath();c.fill();if(rear){c.fillStyle='#1c3444';c.fillRect(-2.5*z,-17*z,5*z,7*z);c.strokeStyle=style.trim;c.lineWidth=1*z;c.beginPath();c.moveTo(-3*z,-15*z);c.lineTo(3*z,-11*z);c.stroke();}else{c.fillStyle=style.trim;c.fillRect(-1*z,-17*z,2*z,9*z);c.fillRect(-4*z,-12*z,8*z,1.3*z);}
  }else if(style?.kind==='armor'){
   c.fillStyle=style.cape;c.beginPath();c.moveTo(-5*z,-17*z);c.lineTo(5*z,-17*z);c.lineTo(8*z,-3*z);c.lineTo(-7*z,-2*z);c.closePath();c.fill();c.fillStyle=cloth;c.beginPath();c.moveTo(-5*z,-18*z);c.lineTo(5*z,-18*z);c.lineTo(4*z,-8*z);c.lineTo(-4*z,-8*z);c.closePath();c.fill();c.fillStyle=style.armor;c.fillRect(-5*z,-17*z,10*z,2.2*z);c.fillStyle=style.trim;if(rear){c.fillStyle='#5b625c';c.beginPath();c.moveTo(-4*z,-15*z);c.lineTo(4*z,-15*z);c.lineTo(3.4*z,-9*z);c.lineTo(-3.4*z,-9*z);c.closePath();c.fill();for(let row=0;row<3;row++)c.fillRect(-3.2*z,(-14+row*1.5)*z,6.4*z,.6*z);c.strokeStyle=style.cape;c.lineWidth=1.1*z;c.beginPath();c.moveTo(0,-8*z);c.lineTo(0,-3*z);c.stroke();}else{for(let row=0;row<3;row++)c.fillRect((-4+row*.3)*z,(-14+row*2.1)*z,(8-row*.6)*z,.7*z);c.fillStyle='#d1b469';c.fillRect(-4.5*z,-10*z,9*z,1.2*z);}
  }else{
   c.fillStyle=cloth;c.beginPath();c.moveTo(-torsoW,-18*z);c.lineTo(torsoW,-18*z);c.lineTo((side?3:4)*z,-8*z);c.lineTo(-(side?3:4)*z,-8*z);c.closePath();c.fill();c.fillStyle=major?'#d1b469':villager?'#b9a26a':'#7e8067';c.fillRect(-torsoW,-12*z,torsoW*2,1.3*z);
  }
  if(!villager){c.fillStyle='#78806c';c.fillRect(-5.2*z,-17*z,2*z,4*z);c.fillRect(3.2*z,-17*z,2*z,4*z);}
  if(spearman||type==='infantry'){c.fillStyle='#8e9978';c.beginPath();c.ellipse(-6*z,-12*z,2.8*z,4.2*z,-.15,0,Math.PI*2);c.fill();c.strokeStyle='#c5b47b';c.lineWidth=.8*z;c.beginPath();c.moveTo(-6*z,-14*z);c.lineTo(-6*z,-9*z);c.stroke();}
  if(villager){c.fillStyle='#8c7950';c.fillRect(-3.5*z,-18.8*z,7*z,1.3*z);if(e.state==='carry'||(e.cargo?.wood||0)>0){c.fillStyle='#73553a';c.fillRect(-3*z,-24*z,6*z,5*z);c.fillStyle='#ad8450';c.fillRect(-3*z,-24*z,6*z,1.4*z);}}
  c.strokeStyle=hit?'#f2ae87':(major?'#d4b875':'#c8b995');c.lineWidth=1.8*z;c.beginPath();if(side){const sx=dir.d===0?1:-1;c.moveTo(sx*2.5*z,-16*z);c.lineTo(sx*5*z,-11*z);}else{c.moveTo(-4*z,-16*z);c.lineTo(-6*z,-11*z);c.moveTo(4*z,-16*z);c.lineTo(6*z,-11*z);}c.stroke();if(style?.kind==='robe'&&!rear){c.fillStyle=style.trim;c.fillRect(-7*z,-16*z,3*z,4*z);c.fillRect(4*z,-16*z,3*z,4*z);}if(!rear)drawWeapon();
  // Eight discrete sectors change which facial side, headwear and shoulders face the viewer.
  c.fillStyle=major?'#c9a866':villager?'#d0ad83':'#d2b596';c.beginPath();if(rear){c.ellipse(0,-21*z,3.2*z,3.5*z,0,0,Math.PI*2);}else if(side){const sx=dir.d===0?1:-1;c.ellipse(-sx*.5*z,-21*z,2.45*z,3.25*z,0,0,Math.PI*2);c.fillStyle='#9b7657';c.beginPath();c.moveTo(sx*1.2*z,-23*z);c.lineTo(sx*4.1*z,-20.8*z);c.lineTo(sx*1.2*z,-19.2*z);c.closePath();c.fill();}else c.arc(0,-21*z,3.3*z,0,Math.PI*2);c.fill();
  if(villager){c.fillStyle='#bca667';c.beginPath();c.ellipse(0,-23.2*z,6*z,1.7*z,0,0,Math.PI*2);c.fill();c.fillStyle='#86784f';c.fillRect(-1*z,-26*z,2*z,3*z);}
  else if(style){this.drawLeaderHead(c,e,z,style,dir,front,rear,side);}
  else if(major){c.fillStyle=type==='king'?'#d7b858':'#a34f42';c.beginPath();c.moveTo(-3.7*z,-23*z);c.lineTo(-2*z,-27*z);c.lineTo(0,-24*z);c.lineTo(2*z,-28*z);c.lineTo(4*z,-23*z);c.fill();}
  else{c.fillStyle=gunner?'#806b47':'#787d65';c.beginPath();c.moveTo(-3.8*z,-22*z);c.lineTo(-2.8*z,-26*z);c.lineTo(2.8*z,-26*z);c.lineTo(3.8*z,-22*z);c.fill();}
  if(front){c.fillStyle='#40372c';c.fillRect(-2.2*z,-21.5*z,1*z,.8*z);c.fillRect(1.2*z,-21.5*z,1*z,.8*z);}else if(side){const sx=dir.d===0?1:-1;c.fillStyle='#40372c';c.fillRect((sx===1?1:-2)*z,-21.5*z,1.1*z,.8*z);}else if(rear){c.fillStyle='#49382e';c.beginPath();c.ellipse(0,-21*z,2.2*z,2.9*z,0,0,Math.PI*2);c.fill();c.fillStyle='#282720';c.beginPath();c.arc(0,-20*z,1.15*z,0,Math.PI*2);c.fill();}
  if(attack){c.strokeStyle='#e7d6a9';c.lineWidth=1.2*z;c.beginPath();c.moveTo(0,-18*z);c.lineTo(fx*4*z,-13*z+fy*2*z);c.stroke();}
  c.restore();if(hit){c.fillStyle='rgba(231,94,66,.18)';c.beginPath();c.ellipse(p.x,p.y-14*z,8*z,16*z,0,0,Math.PI*2);c.fill();}
 }
 drawLeaderHead(c,e,z,style,dir,front,rear,side){
  const sx=dir.d===0?1:-1;
  c.save();
  // Back-facing sectors show a nape, tied hair or helmet guard instead of a second face.
  if(rear){
   c.fillStyle=style.armor||style.coat;c.beginPath();c.ellipse(0,-23.5*z,4.6*z,3.6*z,0,0,Math.PI*2);c.fill();
   c.fillStyle='#332e28';c.beginPath();c.ellipse(0,-21*z,2.65*z,3.1*z,0,0,Math.PI*2);c.fill();
   if(style.hat==='helmet'||style.hat==='crest'){c.fillStyle=style.armor;c.fillRect(-4.2*z,-24.3*z,8.4*z,1.35*z);c.fillStyle='#363933';c.fillRect(-3.2*z,-22.8*z,6.4*z,2*z);}
   else if(style.hat==='knot'){c.fillStyle='#211f1c';c.beginPath();c.arc(0,-25.1*z,2.15*z,0,Math.PI*2);c.fill();c.strokeStyle=style.trim;c.lineWidth=.8*z;c.beginPath();c.moveTo(0,-27*z);c.lineTo(0,-29*z);c.stroke();}
   else if(style.hat==='official'){c.fillStyle='#252e2c';c.fillRect(-4.2*z,-27*z,8.4*z,3.4*z);c.fillStyle=style.trim;c.fillRect(-1*z,-26*z,2*z,1*z);}
   else if(style.hat==='crown'){c.fillStyle=style.trim;c.fillRect(-3.1*z,-27.4*z,6.2*z,2.3*z);c.fillStyle=style.coat;c.fillRect(-1.2*z,-27*z,2.4*z,1.1*z);}
   else if(style.hat==='bicorne'){c.fillStyle='#222c2d';c.beginPath();c.moveTo(-6*z,-26*z);c.lineTo(-4*z,-29*z);c.lineTo(0,-28*z);c.lineTo(4*z,-29*z);c.lineTo(6*z,-26*z);c.lineTo(3*z,-25*z);c.lineTo(-3*z,-25*z);c.closePath();c.fill();c.fillStyle=style.trim;c.fillRect(-4.5*z,-26.3*z,9*z,.65*z);}
   if(style.beard){c.fillStyle='#302923';c.beginPath();c.moveTo(-2.5*z,-20*z);c.lineTo(2.5*z,-20*z);c.lineTo(1*z,-16*z);c.lineTo(0,-15*z);c.lineTo(-1*z,-16*z);c.closePath();c.fill();}
   c.restore();return;
  }
  if(style.beard){c.fillStyle='#302923';c.beginPath();c.moveTo(-2*z,-21*z);c.lineTo(2*z,-21*z);c.lineTo(1.2*z,-16*z);c.lineTo(0,-14*z);c.lineTo(-1.6*z,-17*z);c.closePath();c.fill();}
  switch(style.hat){
   case'bicorne':c.fillStyle='#222c2d';c.beginPath();if(side){c.moveTo(-5*z,-25*z);c.lineTo(sx*7*z,-27*z);c.lineTo(sx*4*z,-24*z);c.lineTo(-4*z,-24*z);}else{c.moveTo(-7*z,-26*z);c.quadraticCurveTo(-3*z,-30*z,0,-27*z);c.quadraticCurveTo(4*z,-30*z,7*z,-26*z);c.lineTo(4*z,-24*z);c.lineTo(-4*z,-24*z);}c.closePath();c.fill();c.fillStyle=style.trim;c.fillRect(side?sx*-4*z:-6*z,-25*z,side?8*z:12*z,.8*z);break;
   case'official':c.fillStyle='#252e2c';if(side){c.fillRect(sx*-7*z,-27*z,14*z,2*z);c.fillRect(sx*-2*z,-30*z,5*z,4*z);c.fillStyle=style.trim;c.fillRect(sx*1*z,-29*z,3*z,1.2*z);}else{c.fillRect(-8*z,-27*z,16*z,2*z);c.fillRect(-4*z,-30*z,8*z,4*z);c.fillStyle=style.trim;c.fillRect(-2*z,-29*z,4*z,1.2*z);}break;
   case'knot':c.fillStyle='#292723';if(side){c.fillRect(sx*-2*z,-27*z,5*z,2*z);c.beginPath();c.arc(sx*-3*z,-28*z,2.3*z,0,Math.PI*2);c.fill();}else{c.fillRect(-3*z,-27*z,6*z,2*z);c.beginPath();c.arc(0,-29*z,2.4*z,0,Math.PI*2);c.fill();}c.fillStyle=style.trim;c.fillRect((side?sx*-3:0)*z-.7*z,-31*z,1.4*z,2*z);break;
   case'crown':c.fillStyle=style.trim;c.beginPath();if(side){c.moveTo(-3*z,-25*z);c.lineTo(-3*z,-30*z);c.lineTo(sx*2*z,-28*z);c.lineTo(sx*5*z,-31*z);c.lineTo(sx*4*z,-25*z);}else{c.moveTo(-4*z,-25*z);c.lineTo(-4*z,-30*z);c.lineTo(-2*z,-28*z);c.lineTo(0,-32*z);c.lineTo(2*z,-28*z);c.lineTo(4*z,-30*z);c.lineTo(4*z,-25*z);}c.closePath();c.fill();c.fillStyle=style.coat;c.fillRect(side?sx*-1*z:-2*z,-29*z,2*z,2*z);break;
   case'crest':case'helmet':c.fillStyle=style.armor;c.beginPath();if(side){c.moveTo(sx*-4*z,-23*z);c.lineTo(sx*-3*z,-28*z);c.lineTo(sx*1*z,-30*z);c.lineTo(sx*4*z,-26*z);c.lineTo(sx*3*z,-23*z);}else{c.moveTo(-4.5*z,-23*z);c.lineTo(-4*z,-28*z);c.lineTo(0,-30*z);c.lineTo(4*z,-28*z);c.lineTo(4.5*z,-23*z);}c.closePath();c.fill();c.fillStyle=style.trim;c.fillRect(side?sx*-2*z:-4*z,-24*z,side?5*z:8*z,1.2*z);if(style.hat==='crest'){c.fillStyle=style.cape;c.beginPath();c.moveTo(side?sx*.5*z:-1.4*z,-29*z);c.quadraticCurveTo(side?sx*5*z:-5*z,-35*z,0,-34*z);c.quadraticCurveTo(side?sx*3*z:5*z,-35*z,side?sx*2*z:1.4*z,-29*z);c.fill();}break;
  }
  c.restore();
 }
 drawCavalry(c,e,p,z,dir,team,hit,attack,swing){const yaw=dir.angle,hitColor=hit?'#bb5948':'#5b4734',recoil=this.impactPulses.active(e.id,this.presentationNow)?2:0;c.save();c.translate(p.x,p.y-4*z);c.rotate(yaw);c.fillStyle='#342e25';c.beginPath();c.ellipse(0,5*z,14*z,3*z,0,0,7);c.fill();
 // Horse faces along its own longitudinal axis. Four separately phased legs make a clear trot.
 c.fillStyle=hitColor;c.beginPath();c.ellipse(-1*z,-7*z,11*z,5.5*z,-.08,0,7);c.fill();c.beginPath();c.moveTo(6*z,-11*z);c.lineTo(10*z,-17*z);c.lineTo(15*z,-16*z);c.lineTo(13*z,-11*z);c.closePath();c.fill();c.fillStyle='#282e29';c.beginPath();c.arc(14*z,-15*z,.8*z,0,7);c.fill();c.strokeStyle='#493a2e';c.lineWidth=1.6*z;for(const [i,lx] of [-8,-3,3,8].entries()){const gait=swing*(i%2?1:-1);c.beginPath();c.moveTo(lx*z,-4*z);c.lineTo((lx+gait)*z,(2+Math.abs(gait)*.35)*z);c.stroke();}c.strokeStyle='#312b22';c.beginPath();c.moveTo(-10*z,-8*z);c.quadraticCurveTo(-15*z,-3*z,-12*z,0);c.stroke();
 c.restore();
 // Rider remains upright in screen space; only the horse and tack follow the projected ground heading.
 c.save();c.translate(p.x,p.y-14*z);const facingFront=dir.d>=1&&dir.d<=3,riderColor=hit?'#df7159':team;c.fillStyle='#433b2d';c.fillRect(-4*z,-4*z,8*z,3*z);c.fillStyle=riderColor;c.beginPath();c.moveTo(-4*z,-16*z);c.lineTo(4*z,-16*z);c.lineTo(3*z,-5*z);c.lineTo(-3*z,-5*z);c.fill();c.fillStyle='#c9a761';c.beginPath();c.arc(0,-20*z,3*z,0,Math.PI*2);c.fill();c.fillStyle='#4e4937';c.fillRect(-4*z,-22*z,8*z,2*z);c.strokeStyle='#d7c79b';c.lineWidth=1.5*z;const weaponSide=(dir.screenX<0?-1:1)*3*z;c.beginPath();c.moveTo(weaponSide,-13*z);c.lineTo(weaponSide+dir.screenX*4*z,-(22-recoil)*z+dir.screenY*5*z);c.stroke();if(facingFront){c.fillStyle='#40372c';c.fillRect(-1.5*z,-20*z,1*z,.8*z);c.fillRect(.7*z,-20*z,1*z,.8*z);}c.restore();if(hit){c.fillStyle='rgba(235,105,76,.25)';c.beginPath();c.ellipse(p.x,p.y-10*z,15*z,9*z,0,0,7);c.fill();}}
 drawWagon(c,e,p,z,dir,team,hit,attack){const yaw=dir.angle,shot=this.impactPulses.active(e.id,this.presentationNow)?3:0;c.save();c.translate(p.x,p.y);c.rotate(yaw);c.fillStyle='#30291f';c.beginPath();c.ellipse(0,3*z,16*z,3*z,0,0,7);c.fill();if(e.type==='artillery'){c.fillStyle='#554b3b';c.fillRect(-10*z,-9*z,20*z,9*z);c.fillStyle=hit?'#a55442':'#887148';c.fillRect(-8*z,-10*z,16*z,5*z);c.strokeStyle='#4b4335';c.lineWidth=4*z;c.beginPath();c.moveTo(-1*z,-8*z);c.lineTo((12-shot)*z,-13*z);c.stroke();c.strokeStyle='#bdb18e';c.lineWidth=1*z;c.beginPath();c.moveTo(10*z,-13*z);c.lineTo(17*z,-15*z);c.stroke();if(shot){c.fillStyle='#f2d07d';c.beginPath();c.arc(17*z,-15*z,3*z,0,7);c.fill();}}else{c.fillStyle=hit?'#ad5945':'#775e3c';c.fillRect(-12*z,-10*z,24*z,9*z);c.fillStyle='#a98a59';for(let i=-8;i<=8;i+=8){c.fillRect(i*z,-9*z,7*z,6*z);c.strokeStyle='#4c3e2d';c.lineWidth=.8*z;c.strokeRect(i*z,-9*z,7*z,6*z);}c.fillStyle='#262a25';for(const x of [-9,9]){c.beginPath();c.arc(x*z,0,3.4*z,0,7);c.fill();c.strokeStyle='#a58b58';c.lineWidth=1*z;c.beginPath();c.arc(x*z,0,1.7*z,0,7);c.stroke();}}c.restore();}
 drawShip(c,e,p,z,dir,team,hit,attack){const yaw=dir.angle,flash=this.impactPulses.active(e.id,this.presentationNow);
  // Only the hull follows the projected ground axis. Mast, deckhouse, and sails remain upright.
  c.save();c.translate(p.x,p.y);c.rotate(yaw);c.fillStyle='rgba(24,39,34,.55)';c.beginPath();c.ellipse(0,3*z,20*z,5*z,0,0,7);c.fill();c.fillStyle=hit?'#b64f43':e.type==='warship'?'#684b35':'#805a39';c.beginPath();c.moveTo(22*z,-1*z);c.lineTo(14*z,5*z);c.lineTo(-15*z,5*z);c.lineTo(-21*z,0);c.lineTo(-15*z,-5*z);c.lineTo(13*z,-5*z);c.closePath();c.fill();c.strokeStyle='#c1a36c';c.lineWidth=1*z;c.beginPath();c.moveTo(-14*z,3*z);c.lineTo(14*z,3*z);c.stroke();c.restore();
  c.save();c.translate(p.x,p.y);c.fillStyle=team;c.fillRect(-8*z,-8*z,16*z,6*z);c.fillStyle='#d4bd88';c.fillRect(-9*z,-9*z,18*z,1.2*z);c.strokeStyle='#d9cba8';c.lineWidth=1*z;c.beginPath();c.moveTo(0,-8*z);c.lineTo(0,-25*z);c.stroke();c.fillStyle='#e9dfc0';c.beginPath();c.moveTo(1*z,-24*z);c.lineTo(10*z,-10*z);c.lineTo(1*z,-11*z);c.closePath();c.fill();if(e.type==='warship'){c.fillStyle='#494536';c.fillRect(-8*z,-9*z,16*z,3*z);c.fillStyle='#d5cda9';for(const x of [-6,6]){c.beginPath();c.arc(x*z,-9*z,1.6*z,0,Math.PI*2);c.fill();}if(flash){c.fillStyle='#f4d079';c.beginPath();c.arc(10*z,-9*z,4*z,0,Math.PI*2);c.fill();}}else{c.fillStyle='#d8c18b';c.fillRect(-2*z,-9*z,4*z,2*z);}c.restore();if(hit){c.fillStyle='rgba(232,94,69,.2)';c.beginPath();c.ellipse(p.x,p.y,14*z,8*z,0,0,Math.PI*2);c.fill();}}
 drawCorpse(c,e,p,z,dir,team){
  const age=Math.max(0,(this.state?.tick||0)-(e.deadTick??(this.state?.tick||0))),alpha=clamp(1-age/(TICK_RATE*4),0,1);if(!alpha)return;
  c.save();c.globalAlpha=alpha;c.translate(p.x,p.y);
  if(e.type==='cavalry'){this.drawHorseWreck(c,z,dir);c.restore();return;}
  if(e.type==='wagon'||e.type==='artillery'){this.drawWagonWreck(c,z,e.type,dir);c.restore();return;}
  if(e.type==='warship'||e.type==='transport'){this.drawShipWreck(c,z,e.type,dir);c.restore();return;}
  c.rotate(dir.angle+Math.PI/2);c.fillStyle='#39352d';c.beginPath();c.ellipse(0,-3*z,7*z,3*z,-.1,0,7);c.fill();c.fillStyle=e.type==='villager'?'#78664e':e.type==='king'?'#784539':team;c.fillRect(-4*z,-14*z,8*z,11*z);c.fillStyle='#574938';c.beginPath();c.arc(0,-17*z,3*z,0,7);c.fill();c.strokeStyle='#6f6853';c.lineWidth=2*z;c.beginPath();c.moveTo(-2*z,-6*z);c.lineTo(-7*z,-1*z);c.moveTo(2*z,-6*z);c.lineTo(8*z,-2*z);c.stroke();c.restore();
 }
 drawHorseWreck(c,z,dir){
  c.rotate(dir.angle);c.fillStyle='rgba(35,30,24,.72)';c.beginPath();c.ellipse(0,4*z,16*z,4.5*z,0,0,Math.PI*2);c.fill();
  // Collapsed horse keeps a long body, downturned head, and folded legs under the tack.
  c.fillStyle='#534334';c.beginPath();c.moveTo(-13*z,-2*z);c.quadraticCurveTo(-8*z,-8*z,3*z,-6*z);c.lineTo(10*z,-3*z);c.lineTo(15*z,0);c.lineTo(9*z,4*z);c.lineTo(-8*z,4*z);c.closePath();c.fill();
  c.fillStyle='#66503a';c.beginPath();c.moveTo(7*z,-4*z);c.lineTo(11*z,-9*z);c.lineTo(16*z,-8*z);c.lineTo(14*z,-3*z);c.lineTo(10*z,0);c.fill();c.fillStyle='#322c25';c.beginPath();c.arc(15*z,-8*z,1*z,0,Math.PI*2);c.fill();
  c.strokeStyle='#332c24';c.lineWidth=2.2*z;c.lineCap='round';for(const [x,dx] of [[-9,-4],[-3,-5],[4,4],[9,5]]){c.beginPath();c.moveTo(x*z,2*z);c.lineTo((x+dx)*z,6*z);c.lineTo((x+dx+(x<0?2:-2))*z,4*z);c.stroke();}
  c.strokeStyle='#26221d';c.lineWidth=1.5*z;c.beginPath();c.moveTo(-12*z,-2*z);c.quadraticCurveTo(-17*z,0,-14*z,4*z);c.stroke();
  c.fillStyle='#853e34';c.beginPath();c.moveTo(-5*z,-6*z);c.lineTo(3*z,-7*z);c.lineTo(5*z,-2*z);c.lineTo(-4*z,-1*z);c.closePath();c.fill();c.strokeStyle='#c3a86d';c.lineWidth=.8*z;c.stroke();
  // Rider is a separate fallen shape beside the saddle, not the foot-unit corpse placeholder.
  c.fillStyle='#6e4335';c.beginPath();c.ellipse(-1*z,-11*z,7*z,3*z,-.18,0,Math.PI*2);c.fill();c.fillStyle='#bea06c';c.beginPath();c.arc(-9*z,-11*z,2.5*z,0,Math.PI*2);c.fill();c.strokeStyle='#c8b58d';c.lineWidth=1.5*z;c.beginPath();c.moveTo(-3*z,-10*z);c.lineTo(-6*z,-7*z);c.moveTo(2*z,-10*z);c.lineTo(6*z,-7*z);c.stroke();
 }
 drawWagonWreck(c,z,type,dir){
  c.rotate(dir.angle);c.fillStyle='rgba(35,30,24,.68)';c.beginPath();c.ellipse(0,4*z,17*z,4*z,0,0,Math.PI*2);c.fill();
  c.fillStyle='#302b23';for(const x of [-10,10]){c.beginPath();c.arc(x*z,2*z,4*z,0,Math.PI*2);c.fill();c.strokeStyle='#9b8051';c.lineWidth=1*z;c.beginPath();c.arc(x*z,2*z,2*z,0,Math.PI*2);c.stroke();}
  if(type==='artillery'){
   c.fillStyle='#514635';c.beginPath();c.moveTo(-11*z,-1*z);c.lineTo(-7*z,-9*z);c.lineTo(5*z,-8*z);c.lineTo(10*z,-1*z);c.closePath();c.fill();
   c.strokeStyle='#473b2b';c.lineWidth=4*z;c.beginPath();c.moveTo(-1*z,-7*z);c.lineTo(8*z,-12*z);c.lineTo(15*z,-8*z);c.stroke();c.strokeStyle='#ad8e58';c.lineWidth=1*z;c.beginPath();c.moveTo(4*z,-9*z);c.lineTo(8*z,-12*z);c.stroke();
   c.fillStyle='#b89556';c.beginPath();c.arc(-7*z,-9*z,2*z,0,Math.PI*2);c.fill();
  }else{
   c.fillStyle='#684d32';c.beginPath();c.moveTo(-12*z,-2*z);c.lineTo(-9*z,-10*z);c.lineTo(7*z,-8*z);c.lineTo(12*z,-2*z);c.lineTo(6*z,1*z);c.lineTo(-9*z,1*z);c.closePath();c.fill();
   c.strokeStyle='#b08b54';c.lineWidth=1*z;c.beginPath();c.moveTo(-8*z,-7*z);c.lineTo(-2*z,-2*z);c.lineTo(3*z,-8*z);c.moveTo(4*z,-7*z);c.lineTo(9*z,-4*z);c.stroke();
   c.fillStyle='#967447';c.fillRect(-12*z,-12*z,5*z,4*z);c.fillStyle='#bd9958';c.fillRect(5*z,-13*z,6*z,5*z);
  }
  c.strokeStyle='#4b3a29';c.lineWidth=1.5*z;c.beginPath();c.moveTo(-14*z,-2*z);c.lineTo(-18*z,-7*z);c.moveTo(12*z,-1*z);c.lineTo(17*z,-6*z);c.stroke();
 }
 drawShipWreck(c,z,type,dir){
  c.rotate(dir.angle);c.fillStyle='rgba(18,35,34,.85)';c.beginPath();c.ellipse(0,4*z,22*z,8*z,0,0,Math.PI*2);c.fill();
  c.fillStyle=type==='warship'?'#513d2e':'#664a31';c.beginPath();c.moveTo(20*z,0);c.lineTo(13*z,7*z);c.lineTo(-13*z,7*z);c.lineTo(-21*z,1*z);c.lineTo(-14*z,-4*z);c.lineTo(12*z,-4*z);c.closePath();c.fill();
  c.strokeStyle='#2c2822';c.lineWidth=2*z;c.beginPath();c.moveTo(-14*z,-2*z);c.lineTo(-4*z,4*z);c.lineTo(1*z,-3*z);c.lineTo(10*z,3*z);c.stroke();
  c.fillStyle='#292a25';c.fillRect(-4*z,-6*z,8*z,4*z);c.strokeStyle='#d2bd89';c.lineWidth=1*z;c.beginPath();c.moveTo(-1*z,-5*z);c.lineTo(-8*z,-16*z);c.lineTo(-13*z,-18*z);c.stroke();
  c.strokeStyle='#6c5035';c.lineWidth=2*z;c.beginPath();c.moveTo(-8*z,-16*z);c.lineTo(-13*z,-18*z);c.lineTo(-15*z,-13*z);c.stroke();
  c.fillStyle='#877149';c.beginPath();c.moveTo(11*z,-2*z);c.lineTo(18*z,-7*z);c.lineTo(17*z,-1*z);c.closePath();c.fill();
 }
 drawFortification(c,e,z,color,trim){
  const parts=fortificationSpans(e,this.fortificationTopology?.get(e.id));
  // World half-cell endpoints share the same projection; no building scale distorts joins.
  const beam=(from,to,height=12,base=0)=>{const a=this.project(from.x,from.y),b=this.project(to.x,to.y);c.fillStyle='#5c5442';c.beginPath();c.moveTo(a.x,a.y-base*z);c.lineTo(b.x,b.y-base*z);c.lineTo(b.x,b.y-height*z);c.lineTo(a.x,a.y-height*z);c.closePath();c.fill();c.strokeStyle=color;c.lineWidth=3*z;c.beginPath();c.moveTo(a.x,a.y-(height-3)*z);c.lineTo(b.x,b.y-(height-3)*z);c.stroke();c.strokeStyle=trim;c.lineWidth=1.5*z;c.beginPath();c.moveTo(a.x,a.y-height*z);c.lineTo(b.x,b.y-height*z);c.stroke();};
  c.save();c.lineCap='round';
  for(const span of parts.spans){const a=this.project(span.from.x,span.from.y),b=this.project(span.to.x,span.to.y);c.strokeStyle='rgba(20,27,22,.4)';c.lineWidth=5*z;c.beginPath();c.moveTo(a.x,a.y+2*z);c.lineTo(b.x,b.y+2*z);c.stroke();beam(span.from,span.to);}
  if(e.type==='gate'){beam(parts.posts[0],parts.posts[1],16,12);for(const post of parts.posts){const p=this.project(post.x,post.y);c.strokeStyle=trim;c.lineWidth=3*z;c.beginPath();c.moveTo(p.x,p.y);c.lineTo(p.x,p.y-16*z);c.stroke();}}
  else{const p=this.project(e.x,e.y);c.strokeStyle=color;c.lineWidth=3*z;c.beginPath();c.moveTo(p.x,p.y);c.lineTo(p.x,p.y-13*z);c.stroke();}
  c.restore();
 }
 drawBuilding(c,e,p,z){
  const key=e.type,color=e.owner===this.localPlayer?'#b69d64':'#9d5947',trim=e.owner===this.localPlayer?'#ddc98e':'#c78569';
  if(key==='wall'||key==='gate'){this.drawFortification(c,e,z,color,trim);return;}
  const w=21,h=key==='residence'?16:13;
  c.save();c.translate(p.x,p.y);c.scale(1.35,1.25);c.translate(-p.x,-p.y);
  // A dark cast shadow and separately shaded wall faces give every footprint a readable plinth.
  c.fillStyle='rgba(20,27,22,.48)';c.beginPath();c.ellipse(p.x,p.y+3*z,w*1.1*z,h*.52*z,0,0,Math.PI*2);c.fill();
  this.diamond(c,p.x,p.y+z,w*z,h*.45*z);
  // Raised stone/wood walls and a highlighted top edge make the roof sit above the ground plane.
  c.fillStyle='#514b3a';c.beginPath();c.moveTo(p.x-w*z,p.y-h*z*.45);c.lineTo(p.x,p.y);c.lineTo(p.x,p.y+6*z);c.lineTo(p.x-w*z,p.y-h*z*.45+4*z);c.closePath();c.fill();
  c.fillStyle='#726448';c.beginPath();c.moveTo(p.x+w*z,p.y-h*z*.45);c.lineTo(p.x,p.y);c.lineTo(p.x,p.y+6*z);c.lineTo(p.x+w*z,p.y-h*z*.45+4*z);c.closePath();c.fill();
  c.fillStyle=color;c.beginPath();c.moveTo(p.x,p.y-h*z);c.lineTo(p.x+w*z,p.y-h*z*.45);c.lineTo(p.x,p.y);c.lineTo(p.x-w*z,p.y-h*z*.45);c.closePath();c.fill();
  c.strokeStyle='rgba(238,215,160,.45)';c.lineWidth=.8*z;c.beginPath();c.moveTo(p.x,p.y-h*z);c.lineTo(p.x+w*z,p.y-h*z*.45);c.lineTo(p.x,p.y);c.stroke();
  if(key==='residence'){
   c.fillStyle='#57432e';c.fillRect(p.x-7*z,p.y-13*z,14*z,13*z);c.fillStyle='#775b3a';c.fillRect(p.x-7*z,p.y-8*z,14*z,7*z);
   for(const dx of [-4,4]){c.fillStyle='#d7c18b';c.fillRect(p.x+(dx-1)*z,p.y-11*z,2*z,3*z);}
   for(let level=0;level<3;level++){const yy=p.y-(13+level*5)*z,span=(12-level*1.3)*z;
    c.fillStyle=level===2?'#8c5e3a':'#b79558';c.beginPath();c.moveTo(p.x-span,yy+3*z);c.lineTo(p.x,yy-2*z);c.lineTo(p.x+span,yy+3*z);c.lineTo(p.x,yy+1*z);c.closePath();c.fill();
    c.fillStyle='#dfc98a';c.beginPath();c.moveTo(p.x-span-2*z,yy+3*z);c.lineTo(p.x,yy-3*z);c.lineTo(p.x+span+2*z,yy+3*z);c.lineTo(p.x+span,yy+4*z);c.lineTo(p.x,yy);c.lineTo(p.x-span,yy+4*z);c.closePath();c.fill();
    c.strokeStyle='#765339';c.lineWidth=.7*z;c.beginPath();c.moveTo(p.x-span-2*z,yy+3*z);c.lineTo(p.x,yy-3*z);c.lineTo(p.x+span+2*z,yy+3*z);c.stroke();
   }
   c.fillStyle='#322d25';c.fillRect(p.x-1.7*z,p.y-7*z,3.4*z,7*z);c.fillStyle='#d1b66e';c.fillRect(p.x-1*z,p.y-6*z,.7*z,3*z);
   c.fillStyle='#d2bc82';c.fillRect(p.x-15*z,p.y-h*z-1*z,3*z,9*z);c.fillRect(p.x+12*z,p.y-h*z-1*z,3*z,9*z);
  }else if(key==='granary'){
   c.fillStyle='#493f2d';for(const dx of [-8,7])c.fillRect(p.x+dx*z,p.y-10*z,1.5*z,10*z);
   c.fillStyle='#c49c5b';c.fillRect(p.x-10*z,p.y-11*z,20*z,3*z);c.fillStyle='#53674c';c.fillRect(p.x-11*z,p.y-14*z,22*z,3*z);
   c.fillStyle='#d9c58c';c.fillRect(p.x-12*z,p.y-15*z,24*z,1.4*z);
   for(const dx of [-6,0,6]){c.fillStyle='#8a5837';c.beginPath();c.ellipse(p.x+dx*z,p.y-18*z,3*z,4.5*z,0,0,Math.PI*2);c.fill();c.fillStyle='#bd915a';c.beginPath();c.ellipse(p.x+dx*z,p.y-19*z,1.6*z,2*z,0,0,Math.PI*2);c.fill();}
  }else if(key==='depot'){
   c.fillStyle='#9d8151';for(let row=0;row<2;row++)for(let col=0;col<3;col++){const bx=p.x+(-9+col*7)*z,by=p.y+(-11+row*5)*z;c.fillStyle=row?'#987749':'#b18f58';c.fillRect(bx,by,6*z,5*z);c.strokeStyle='#57462e';c.lineWidth=.8*z;c.strokeRect(bx,by,6*z,5*z);c.strokeStyle='#ddc78e';c.beginPath();c.moveTo(bx+z,by+z);c.lineTo(bx+5*z,by+z);c.stroke();}
  }else if(key==='barracks'){
   c.fillStyle='#634a34';c.fillRect(p.x-9*z,p.y-11*z,18*z,10*z);c.fillStyle='#7e6040';c.fillRect(p.x-9*z,p.y-6*z,18*z,5*z);
   c.fillStyle='#b28b51';c.beginPath();c.moveTo(p.x-13*z,p.y-10*z);c.lineTo(p.x,p.y-18*z);c.lineTo(p.x+13*z,p.y-10*z);c.lineTo(p.x,p.y-13*z);c.closePath();c.fill();
   c.fillStyle='#dfc489';c.beginPath();c.moveTo(p.x-14*z,p.y-10*z);c.lineTo(p.x,p.y-19*z);c.lineTo(p.x+14*z,p.y-10*z);c.strokeStyle='#dfc489';c.lineWidth=1.5*z;c.stroke();
   c.strokeStyle='#d7c99e';c.lineWidth=1.1*z;for(const dx of [-9,0,9]){c.beginPath();c.moveTo(p.x+dx*z,p.y-17*z);c.lineTo(p.x+dx*z,p.y-10*z);c.stroke();}
   c.fillStyle='#332c23';c.fillRect(p.x-3*z,p.y-6*z,6*z,6*z);
  }else if(key==='cavalryCamp'){
   c.fillStyle='#a88a56';c.beginPath();c.moveTo(p.x-13*z,p.y-8*z);c.lineTo(p.x,p.y-17*z);c.lineTo(p.x+13*z,p.y-8*z);c.lineTo(p.x+10*z,p.y-5*z);c.lineTo(p.x-10*z,p.y-5*z);c.closePath();c.fill();
   c.fillStyle='#483b2c';c.fillRect(p.x-9*z,p.y-8*z,18*z,8*z);c.fillStyle='#302c23';c.fillRect(p.x+2*z,p.y-8*z,6*z,8*z);
   c.strokeStyle='#d0b777';c.lineWidth=z;c.beginPath();c.moveTo(p.x-12*z,p.y-4*z);c.lineTo(p.x+12*z,p.y-4*z);c.stroke();
   c.fillStyle='#4a4435';c.beginPath();c.ellipse(p.x-5*z,p.y-3*z,4*z,2*z,0,0,Math.PI*2);c.fill();
  }else if(key==='shipyard'){
   c.fillStyle='#5b402d';c.fillRect(p.x-13*z,p.y-6*z,26*z,4*z);c.fillStyle='#9b6b3f';c.fillRect(p.x-10*z,p.y-12*z,18*z,7*z);
   c.fillStyle='#c0a76e';c.beginPath();c.moveTo(p.x-12*z,p.y-12*z);c.lineTo(p.x-1*z,p.y-19*z);c.lineTo(p.x+10*z,p.y-12*z);c.lineTo(p.x-1*z,p.y-9*z);c.closePath();c.fill();
   c.strokeStyle='#d6c89f';c.lineWidth=1.2*z;c.beginPath();c.moveTo(p.x-5*z,p.y-14*z);c.lineTo(p.x-5*z,p.y-3*z);c.moveTo(p.x+3*z,p.y-14*z);c.lineTo(p.x+3*z,p.y-3*z);c.stroke();
   c.strokeStyle='#d2bc82';c.lineWidth=1.2*z;c.beginPath();c.moveTo(p.x-15*z,p.y+2*z);c.lineTo(p.x+15*z,p.y+2*z);c.moveTo(p.x-13*z,p.y+5*z);c.lineTo(p.x+13*z,p.y+5*z);c.stroke();
  }else if(key==='artilleryWorkshop'){
   c.fillStyle='#534b3a';c.fillRect(p.x-10*z,p.y-12*z,20*z,11*z);c.fillStyle='#8c7048';c.fillRect(p.x-10*z,p.y-7*z,20*z,6*z);
   c.fillStyle='#a88c58';c.beginPath();c.moveTo(p.x-13*z,p.y-12*z);c.lineTo(p.x,p.y-20*z);c.lineTo(p.x+13*z,p.y-12*z);c.closePath();c.fill();
   c.fillStyle='#4d493b';c.fillRect(p.x+6*z,p.y-22*z,4*z,11*z);c.fillStyle='#c1a46a';c.fillRect(p.x+5*z,p.y-23*z,6*z,2*z);
   c.fillStyle='#d0b36f';c.beginPath();c.arc(p.x-4*z,p.y-6*z,2.2*z,0,Math.PI*2);c.fill();c.strokeStyle='#b89a61';c.lineWidth=1.2*z;c.beginPath();c.moveTo(p.x-5*z,p.y-3*z);c.lineTo(p.x+3*z,p.y-3*z);c.stroke();
  }else if(key==='fort'){
   c.fillStyle='#77715f';c.fillRect(p.x-12*z,p.y-14*z,24*z,13*z);c.fillStyle='#918773';c.fillRect(p.x-12*z,p.y-8*z,24*z,7*z);
   c.fillStyle='#c2b184';c.fillRect(p.x-13*z,p.y-16*z,26*z,3*z);for(let i=-12;i<12;i+=6)c.fillRect(p.x+i*z,p.y-19*z,4*z,4*z);
   c.fillStyle='#334235';c.fillRect(p.x-4*z,p.y-8*z,8*z,8*z);c.fillStyle='#262c26';c.fillRect(p.x-2*z,p.y-6*z,4*z,6*z);
   c.fillStyle='#b9a273';c.fillRect(p.x-9*z,p.y-12*z,2*z,3*z);c.fillRect(p.x+7*z,p.y-12*z,2*z,3*z);
  }else{
   c.fillStyle='#847657';c.fillRect(p.x-9*z,p.y-11*z,18*z,10*z);c.fillStyle='#b9a06a';c.beginPath();c.moveTo(p.x-12*z,p.y-10*z);c.lineTo(p.x,p.y-18*z);c.lineTo(p.x+12*z,p.y-10*z);c.lineTo(p.x,p.y-13*z);c.closePath();c.fill();c.fillStyle=trim;c.fillRect(p.x-13*z,p.y-10*z,26*z,1.2*z);
  }
  c.restore();
 }
 drawMinimap(s,player){const c=this.mctx,cv=this.minimap,w=cv.width,h=cv.height;c.clearRect(0,0,w,h);c.fillStyle='#263d32';c.fillRect(0,0,w,h);const sx=w/s.map.width,sy=h/s.map.height,fog=s.fog;for(let y=0;y<s.map.height;y++)for(let x=0;x<s.map.width;x++){const i=y*s.map.width+x,t=s.map.tiles[i];c.fillStyle=palette[t]||palette.plain;c.fillRect(x*sx,y*sy,Math.ceil(sx),Math.ceil(sy));if(fog?.explored&&!fog.explored[i]){c.fillStyle='#091b17';c.fillRect(x*sx,y*sy,Math.ceil(sx),Math.ceil(sy));}else if(fog?.visible&&!fog.visible[i]){c.fillStyle='rgba(9,24,20,.56)';c.fillRect(x*sx,y*sy,Math.ceil(sx),Math.ceil(sy));}}for(const e of s.entities||[]){if(e.embarked||!this.visible(e,s,player))continue;c.fillStyle=e.owner===player?'#ead276':'#da765f';c.fillRect(e.x*sx-1,e.y*sy-1,e.kind==='building'?4:2,e.kind==='building'?4:2);}c.strokeStyle='#ead28d';c.lineWidth=1;c.strokeRect((this.camera.x-7)*sx,(this.camera.y-5)*sy,14*sx,10*sy);}
}
function xy(e){return{x:e.x,y:e.y}}
