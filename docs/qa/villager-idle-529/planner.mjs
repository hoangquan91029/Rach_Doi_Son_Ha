import {BUILDINGS,TERRAIN} from '../../../shared/data.js';
export function pointReason(state,actor,p,{plain=false}={}){
 const m=state.map;if(!m||!Number.isInteger(m.width)||!Number.isInteger(m.height)||!Array.isArray(m.tiles))return 'missing-public-map';
 const x=Math.floor(p.x),y=Math.floor(p.y);if(x<1||y<1||x>=m.width-1||y>=m.height-1)return 'out-of-interior';const i=y*m.width+x,t=m.tiles[i];
 if(!state.fog?.visible)return 'missing-public-visibility';if(!state.fog.visible[i])return 'not-visible';
 if(!TERRAIN[t]||TERRAIN[t].impassable||TERRAIN[t].water&&!TERRAIN[t].land)return 'not-land-passable';if(plain&&t!=='plain')return 'not-plain';
 for(const b of state.entities||[])if(b.kind==='building'&&b.hp>0&&b.id!==actor.id&&!(b.type==='gate'&&b.owner===actor.owner)){const r=BUILDINGS[b.type]?.radius;if(!Number.isFinite(r))return 'unknown-building-footprint';if(Math.abs(p.x-b.x)<r+.15&&Math.abs(p.y-b.y)<r+.15)return 'building-footprint:'+b.id;}
 return null;
}
function segmentBuildingReason(state,actor,from,to){for(const b of state.entities||[]){if(b.kind!=='building'||!(b.hp>0)||b.id===actor.id||b.type==='gate'&&b.owner===actor.owner)continue;const r=BUILDINGS[b.type]?.radius;if(!Number.isFinite(r))return 'unknown-building-footprint';let lo=0,hi=1,intersection=true;for(const axis of ['x','y']){const d=to[axis]-from[axis],min=b[axis]-r-.15,max=b[axis]+r+.15;if(d===0){if(from[axis]<=min||from[axis]>=max){intersection=false;break;}}else{const a=(min-from[axis])/d,z=(max-from[axis])/d;lo=Math.max(lo,Math.min(a,z));hi=Math.min(hi,Math.max(a,z));if(lo>=hi){intersection=false;break;}}}if(intersection&&lo<hi)return 'ground-segment-building:'+b.id;}return null;}
export function diagonalReason(state,actor,from,d=4.5){const to={x:from.x+d,y:from.y+d},cross=segmentBuildingReason(state,actor,from,to);if(cross)return cross;const steps=Math.ceil(d/.25);let prev=from;for(let k=0;k<=steps;k++){const p={x:from.x+d*k/steps,y:from.y+d*k/steps},reason=pointReason(state,actor,p,{plain:true});if(reason)return reason;for(const side of [{x:p.x,y:prev.y},{x:prev.x,y:p.y}]){const r=pointReason(state,actor,side);if(r)return 'neighbor-'+r;}for(const e of state.entities||[])if(e.id!==actor.id&&e.hp>0&&!e.embarked&&e.kind==='unit'&&Math.hypot(e.x-p.x,e.y-p.y)<.7)return 'occupied-unit:'+e.id;prev=p;}return null;}
/** Conservative rectangle contains both .7 arrival squares, fixed first-target paths,
 * and every translated short1.5 segment from the first arrival square.
 * Tile centers for every intersecting cell also certify diagonal neighbors. */
export function envelopeReason(state,actor,center,{arrival=.7}={}){
 if(arrival!==.7)throw Error('Engine arrival envelope must remain0.7');
 const box={minX:center.x-arrival,minY:center.y-arrival,maxX:center.x+4.5+arrival,maxY:center.y+4.5+arrival};
 for(let y=Math.floor(box.minY);y<=Math.floor(box.maxY);y++)for(let x=Math.floor(box.minX);x<=Math.floor(box.maxX);x++){
  const reason=pointReason(state,actor,{x:x+.5,y:y+.5},{plain:true});if(reason)return 'envelope-cell-'+reason;
 }
 for(const b of state.entities||[]){if(b.kind!=='building'||!(b.hp>0)||b.id===actor.id||b.type==='gate'&&b.owner===actor.owner)continue;const r=BUILDINGS[b.type]?.radius;if(!Number.isFinite(r))return 'unknown-building-footprint';if(box.minX<b.x+r+.15&&box.maxX>b.x-r-.15&&box.minY<b.y+r+.15&&box.maxY>b.y-r-.15)return 'envelope-building:'+b.id;}
 for(const e of state.entities||[])if(e.id!==actor.id&&e.hp>0&&!e.embarked&&e.kind==='unit'&&e.x>box.minX-.7&&e.x<box.maxX+.7&&e.y>box.minY-.7&&e.y<box.maxY+.7)return 'envelope-unit:'+e.id;
 return null;
}
export function fixedTargetReason(state,actor,from,to,{units=true}={}){
 const angle=Math.atan2(to.y-from.y,to.x-from.x),dir=(Math.round(angle/(Math.PI/4))+8)%8;if(dir!==1)return 'target-not-natural-D1';
 const building=segmentBuildingReason(state,actor,from,to);if(building)return building;
 const steps=Math.ceil(Math.hypot(to.x-from.x,to.y-from.y)/.25);let prev=from;
 for(let k=0;k<=steps;k++){const p={x:from.x+(to.x-from.x)*k/steps,y:from.y+(to.y-from.y)*k/steps};const reason=pointReason(state,actor,p,{plain:true});if(reason)return reason;for(const side of[{x:p.x,y:prev.y},{x:prev.x,y:p.y}]){const r=pointReason(state,actor,side);if(r)return 'neighbor-'+r;}for(const e of units?(state.entities||[]):[])if(e.id!==actor.id&&e.hp>0&&!e.embarked&&e.kind==='unit'&&Math.hypot(e.x-p.x,e.y-p.y)<.7)return 'occupied-unit:'+e.id;prev=p;}
 return null;
}
export function planEgress(snapshot,{radius=8,maxCells=4096}={}){
 if(!Number.isInteger(radius)||radius<1||radius>8||!Number.isInteger(maxCells)||maxCells<1||maxCells>4096)throw Error('Invalid finite planner bounds');
 const state=snapshot.displayedState,rejections=[];if(!state?.map||!state.fog?.visible)return{selected:null,rejections:[{reason:'missing-public-map-or-visibility'}]};const m=state.map;if(m.width*m.height>maxCells)return{selected:null,rejections:[{reason:'map-search-cap'}]};const actors=state.entities.filter(e=>e.owner===snapshot.localPlayer&&e.type==='villager'&&e.hp>0&&e.state==='idle'&&!e.order&&!e.embarked);if(actors.length>24)return{selected:null,rejections:[{reason:'actor-search-cap'}]};
 for(const actor of actors){const sx=Math.floor(actor.x),sy=Math.floor(actor.y),queue=[[sx,sy]],visited=new Set([sy*m.width+sx]);let head=0;while(head<queue.length&&head<maxCells){const[x,y]=queue[head++];for(const[dx,dy]of[[1,0],[0,1],[-1,0],[0,-1],[1,1],[-1,1],[-1,-1],[1,-1]]){const xx=x+dx,yy=y+dy,key=yy*m.width+xx;if(visited.has(key)||pointReason(state,actor,{x:xx+.5,y:yy+.5}))continue;if(dx&&dy&&(pointReason(state,actor,{x:xx+.5,y:y+.5})||pointReason(state,actor,{x:x+.5,y:yy+.5})))continue;visited.add(key);queue.push([xx,yy]);}}
 const candidates=[];for(let y=sy-radius;y<=sy+radius;y++)for(let x=sx-radius;x<=sx+radius;x++)candidates.push({x:x+.5,y:y+.5});candidates.sort((a,b)=>Math.hypot(a.x-actor.x,a.y-actor.y)-Math.hypot(b.x-actor.x,b.y-actor.y)||a.y-b.y||a.x-b.x);
 for(const p of candidates){let reason=pointReason(state,actor,p,{plain:true});if(!reason&&!visited.has(Math.floor(p.y)*m.width+Math.floor(p.x)))reason='not-visible-reachable';if(!reason&&Math.hypot(p.x-actor.x,p.y-actor.y)<1.5)reason='insufficient-egress-distance';if(!reason)reason=envelopeReason(state,actor,p);if(!reason)reason=diagonalReason(state,actor,p);if(reason){rejections.push({actorId:actor.id,point:p,reason});continue;}return{selected:{actorId:actor.id,staging:p,firstTarget:{x:p.x+3,y:p.y+3},secondTarget:{x:p.x+4.5,y:p.y+4.5},certificate:{arrivalRadius:.7,method:'Conservativewholecellplain-visible rectangle plus exactcontinuous buildingAABB, fixedfirsttarget and recheckedshortactualsegment',box:{minX:p.x-.7,minY:p.y-.7,maxX:p.x+5.2,maxY:p.y+5.2},naturalD1:'delta range[2.3,3.7] forbothaxes; ratio range0.621..1.609 strictlyinsideD1sector0.414..2.414'}},rejections,search:{actors:actors.length,visitedCells:visited.size,radius,maxCells}};}
 }
 return{selected:null,rejections,search:{actors:actors.length,radius,maxCells}};
}
