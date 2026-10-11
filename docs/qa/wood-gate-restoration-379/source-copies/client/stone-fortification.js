import {fortificationSpans} from './fortification-topology.js';
/** Native 2D baseline only. Authored whole stone illustrations can replace exact states later. */
export const STONE_WALL_HEIGHT=18.5625;
export const STONE_GATE_HEIGHT=STONE_WALL_HEIGHT+4;
export const STONE_FORTIFICATION_COLORS=Object.freeze({face:'#8b8d82',side:'#73776f',cap:'#c8c4b2',mortar:'#60675f',joint:'#b4b3a3',rubble:'#93958a'});
export function stoneFortificationAssetAllowed(asset){return asset?.family==='building.wall'?asset.material==='stone':asset?.family==='building.gate'?asset.material==='wood':true;}
export function stoneFortificationPresentation(entity,topology){
 const dead=entity.hp<=0||entity.state==='death',unfinished=!dead&&Boolean(entity.construction||entity.underConstruction===true);
 return {dead,unfinished,parts:fortificationSpans(entity,dead||unfinished?undefined:topology),height:dead?3:STONE_WALL_HEIGHT,material:'stone'};
}
export function drawStoneFortification(renderer,c,e,z){
 const view=stoneFortificationPresentation(e,renderer.fortificationTopology?.get(e.id)),col=STONE_FORTIFICATION_COLORS;
 const face=(from,to,height=STONE_WALL_HEIGHT,base=0)=>{const a=renderer.project(from.x,from.y),b=renderer.project(to.x,to.y);const at=(t,lift)=>({x:a.x+(b.x-a.x)*t,y:a.y+(b.y-a.y)*t-lift*z});
  c.fillStyle=view.dead?col.rubble:col.face;c.beginPath();for(const [t,h]of [[0,base],[1,base],[1,height],[0,height]]){const p=at(t,h);if(t===0&&h===base)c.moveTo(p.x,p.y);else c.lineTo(p.x,p.y);}c.closePath();c.fill();
  // Quiet staggered masonry joints, shared level caps for both axes; no timber posts or rails.
  c.strokeStyle=col.mortar;c.lineWidth=.6*z;
  for(let h=base+4;h<height;h+=4){const p=at(0,h),q=at(1,h);c.beginPath();c.moveTo(p.x,p.y);c.lineTo(q.x,q.y);c.stroke();}
  for(let row=0,h=base;h<height;h+=4,row++){for(const t of row%2?[.25,.75]:[.5]){const p=at(t,h),q=at(t,Math.min(h+4,height));c.beginPath();c.moveTo(p.x,p.y);c.lineTo(q.x,q.y);c.stroke();}}
  c.strokeStyle=col.cap;c.lineWidth=1.5*z;const p=at(0,height),q=at(1,height);c.beginPath();c.moveTo(p.x,p.y);c.lineTo(q.x,q.y);c.stroke();
  if(view.unfinished){c.strokeStyle=col.joint;c.setLineDash([2*z,2*z]);c.lineWidth=.65*z;c.beginPath();c.moveTo(p.x,p.y+2*z);c.lineTo(q.x,q.y+2*z);c.stroke();c.setLineDash([]);}
 };
 const pier=(post,height)=>{const p=renderer.project(post.x,post.y);c.fillStyle=col.side;c.fillRect(p.x-1.5*z,p.y-height*z,3*z,height*z);c.strokeStyle=col.cap;c.lineWidth=.65*z;for(let h=4;h<height;h+=4){c.beginPath();c.moveTo(p.x-1.5*z,p.y-h*z);c.lineTo(p.x+1.5*z,p.y-h*z);c.stroke();}c.fillStyle=col.cap;c.fillRect(p.x-1.5*z,p.y-height*z,3*z,z);};
 c.save();c.lineCap='butt';c.lineJoin='miter';for(const span of view.parts.spans){const a=renderer.project(span.from.x,span.from.y),b=renderer.project(span.to.x,span.to.y);c.strokeStyle='rgba(20,27,22,.32)';c.lineWidth=5*z;c.beginPath();c.moveTo(a.x,a.y+2*z);c.lineTo(b.x,b.y+2*z);c.stroke();face(span.from,span.to,view.height);}
 if(e.type==='gate'&&!view.dead){face(view.parts.posts[0],view.parts.posts[1],STONE_GATE_HEIGHT,STONE_WALL_HEIGHT);for(const post of view.parts.posts)pier(post,STONE_GATE_HEIGHT);}else if(!view.dead)pier({x:e.x,y:e.y},STONE_WALL_HEIGHT);
 c.restore();
}
