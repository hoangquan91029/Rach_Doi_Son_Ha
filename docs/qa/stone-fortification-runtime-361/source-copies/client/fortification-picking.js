import {STONE_WALL_HEIGHT,STONE_GATE_HEIGHT} from './stone-fortification.js';
import {fortificationSpans} from './fortification-topology.js';

function segmentDistance(x,y,a,b){
 const dx=b.x-a.x,dy=b.y-a.y,length=dx*dx+dy*dy;
 const t=length?Math.max(0,Math.min(1,((x-a.x)*dx+(y-a.y)*dy)/length)):0;
 return Math.hypot(x-a.x-t*dx,y-a.y-t*dy);
}
function inside(x,y,points){
 let result=false;
 for(let i=0,j=points.length-1;i<points.length;j=i++){
  const a=points[j],b=points[i];
  if(segmentDistance(x,y,a,b)<1e-7)return true;
  if((a.y>y)!==(b.y>y)&&x<(b.x-a.x)*(y-a.y)/(b.y-a.y)+a.x)result=!result;
 }
 return result;
}
/** Invisible hit mask for the actual procedural stone wall faces, caps and gate piers.
 * Shadows and the open gate passage do not intercept clicks. No gameplay changes. */
export function fortificationContains(renderer,entity,x,y){
 const z=renderer.camera.zoom;
 if(!Number.isFinite(x)||!Number.isFinite(y)||!(z>0))return false;
 const parts=fortificationSpans(entity,renderer.fortificationTopology?.get(entity.id));
 const project=p=>renderer.project(p.x,p.y);
 const beam=(from,to,height,base=0)=>{
  const a=project(from),b=project(to);
  const face=[{x:a.x,y:a.y-base*z},{x:b.x,y:b.y-base*z},{x:b.x,y:b.y-height*z},{x:a.x,y:a.y-height*z}];
  return inside(x,y,face)||segmentDistance(x,y,{x:a.x,y:a.y-(height-3)*z},{x:b.x,y:b.y-(height-3)*z})<=1.5*z||segmentDistance(x,y,face[2],face[3])<=.75*z;
 };
 if(parts.spans.some(span=>beam(span.from,span.to,STONE_WALL_HEIGHT)))return true;
 if(entity.type==='gate'){
  if(beam(parts.posts[0],parts.posts[1],STONE_GATE_HEIGHT,STONE_WALL_HEIGHT))return true;
  return parts.posts.some(post=>{const p=project(post);return segmentDistance(x,y,p,{x:p.x,y:p.y-STONE_GATE_HEIGHT*z})<=1.5*z;});
 }
 const p=project(entity);
 return segmentDistance(x,y,p,{x:p.x,y:p.y-STONE_WALL_HEIGHT*z})<=1.5*z;
}
