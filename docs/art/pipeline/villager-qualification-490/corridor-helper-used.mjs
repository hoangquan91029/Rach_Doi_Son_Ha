/** Pure read-only corridor geometry; direction is the simulation atan2 octant. */
export const WORLD_OCTANTS=Object.freeze([[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1]].map(v=>Object.freeze(v)));
export function corridorPoint(start,direction,distance){
 if(!Number.isInteger(direction)||direction<0||direction>7)throw Error('Invalid walk direction');
 const [dx,dy]=WORLD_OCTANTS[direction],length=Math.hypot(dx,dy);
 return {x:start.x+dx/length*distance,y:start.y+dy/length*distance};
}
export function clearWalkSegment(state,actor,end){
 const map=state.map,distance=Math.hypot(end.x-actor.x,end.y-actor.y),steps=Math.ceil(distance/.25);
 for(let i=0;i<=steps;i++){
  const t=steps?i/steps:0,p={x:actor.x+(end.x-actor.x)*t,y:actor.y+(end.y-actor.y)*t},x=Math.floor(p.x),y=Math.floor(p.y);
  if(x<0||y<0||x>=map.width||y>=map.height)return false;
  const index=y*map.width+x;
  if(!state.fog.visible[index]||!['plain','hill'].includes(map.tiles[index]))return false;
  if(state.entities.some(u=>u.id!==actor.id&&u.hp>0&&!u.embarked&&(u.kind==='building'?Math.abs(u.x-p.x)<1.8&&Math.abs(u.y-p.y)<1.8:Math.hypot(u.x-p.x,u.y-p.y)<.55)))return false;
 }
 return true;
}

export function clearWalkCorridor(state,actor,direction,distance){return clearWalkSegment(state,actor,corridorPoint(actor,direction,distance));}
/** Finite visible tile-center search, shortest verified clear ordinary move first. */
export function findWalkClearance(state,actors,direction,distance=9){
 const choices=[];
 for(const actor of actors)for(let y=0;y<state.map.height;y++)for(let x=0;x<state.map.width;x++){
  const start={...actor,x:x+.5,y:y+.5},travel=Math.hypot(start.x-actor.x,start.y-actor.y);
  if(travel<1||travel>12||!clearWalkCorridor(state,start,direction,distance)||WORLD_OCTANTS.some((_,d)=>!clearWalkCorridor(state,{...start,...corridorPoint(start,d,.700001)},direction,distance))||!clearWalkSegment(state,actor,start))continue;
  choices.push({actorId:actor.id,start:{x:start.x,y:start.y},travel,direction,distance});
 }
 return choices.sort((a,b)=>a.travel-b.travel||a.actorId-b.actorId||a.start.y-b.start.y||a.start.x-b.start.x)[0]??null;
}
