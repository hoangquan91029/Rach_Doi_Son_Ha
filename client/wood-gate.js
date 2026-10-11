import {fortificationSpans} from './fortification-topology.js';
/** Original347 gate-only whole native geometry; walls retain stone presentation. */
export function drawWoodGate(renderer,c,e,z,color,trim){
  const parts=fortificationSpans(e,renderer.fortificationTopology?.get(e.id));
  // World half-cell endpoints share the same projection; no building scale distorts joins.
  const beam=(from,to,height=12,base=0)=>{const a=renderer.project(from.x,from.y),b=renderer.project(to.x,to.y);c.fillStyle='#5c5442';c.beginPath();c.moveTo(a.x,a.y-base*z);c.lineTo(b.x,b.y-base*z);c.lineTo(b.x,b.y-height*z);c.lineTo(a.x,a.y-height*z);c.closePath();c.fill();c.strokeStyle=color;c.lineWidth=3*z;c.beginPath();c.moveTo(a.x,a.y-(height-3)*z);c.lineTo(b.x,b.y-(height-3)*z);c.stroke();c.strokeStyle=trim;c.lineWidth=1.5*z;c.beginPath();c.moveTo(a.x,a.y-height*z);c.lineTo(b.x,b.y-height*z);c.stroke();};
  c.save();c.lineCap='round';
  for(const span of parts.spans){const a=renderer.project(span.from.x,span.from.y),b=renderer.project(span.to.x,span.to.y);c.strokeStyle='rgba(20,27,22,.4)';c.lineWidth=5*z;c.beginPath();c.moveTo(a.x,a.y+2*z);c.lineTo(b.x,b.y+2*z);c.stroke();beam(span.from,span.to);}
  if(e.type==='gate'){beam(parts.posts[0],parts.posts[1],16,12);for(const post of parts.posts){const p=renderer.project(post.x,post.y);c.strokeStyle=trim;c.lineWidth=3*z;c.beginPath();c.moveTo(p.x,p.y);c.lineTo(p.x,p.y-16*z);c.stroke();}}
  c.restore();
}
