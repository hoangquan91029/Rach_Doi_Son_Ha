import {TILE_WIDTH,TILE_HEIGHT} from './world-presentation.js';
/** Invisible coverage only: samples original world-anchored materials on the receiving side. */
const water=t=>t==='river'||t==='sea';
const land=t=>['plain','forest','hill'].includes(t);
export function terrainTransitionEdges(map,fog) {
 if(!map?.tiles)return [];
 const {width,height,tiles}=map,edges=[];
 const known=i=>!fog?.visible||Boolean(fog.visible[i]||fog.explored?.[i]);
 for(let y=0;y<height;y++)for(let x=0;x<width;x++) {
  const i=y*width+x;if(!known(i))continue;
  for(const [dx,dy] of [[1,0],[0,1]]) {
   const nx=x+dx,ny=y+dy;if(nx>=width||ny>=height)continue;
   const j=ny*width+nx;if(!known(j))continue;
   const a=tiles[i],b=tiles[j];let receiver,source;
   // Deep water never receives shallow ford art: impassable river stays visibly deep.
   if(water(a)&&(land(b)||b==='ford')){receiver={x:nx,y:ny,t:b};source=a;}
   else if(water(b)&&(land(a)||a==='ford')){receiver={x,y,t:a};source=b;}
   else if(a==='ford'&&land(b)){receiver={x:nx,y:ny,t:b};source=a;}
   else if(b==='ford'&&land(a)){receiver={x,y,t:a};source=b;}
   else continue;
   edges.push({x:dx?x+1:x,y:dy?y+1:y,axis:dx?'y':'x',sign:dx?(receiver.x===x?-1:1):(receiver.y===y?-1:1),receiver:receiver.t,source});
  }
 }
 return edges;
}
/** Gradient is perpendicular to the projected edge, so alpha stays constant along its tangent. */
export function transitionGradient(edge,project,depth) {
 const point=(along,inward)=>edge.axis==='y'?project(edge.x+edge.sign*inward,edge.y+along):project(edge.x+along,edge.y+edge.sign*inward);
 const a=point(0,0),b=point(1,0),c=point(0,depth),tx=b.x-a.x,ty=b.y-a.y,length=Math.hypot(tx,ty);
 const nx=-ty/length,ny=tx/length,distance=(c.x-a.x)*nx+(c.y-a.y)*ny;
 return {points:[a,b,point(1,depth),c],start:a,end:{x:a.x+nx*distance,y:a.y+ny*distance}};
}
/** Shared world vertices make coverage independent of camera and edge enumeration. */
export function shorelineDepth(edge,along){if(edge.receiver==='ford')return .09;const vertex=(x,y)=>.26+.055*Math.sin(x*1.73+y*2.19);const a=vertex(edge.x,edge.y),b=vertex(edge.x+(edge.axis==='x'?1:0),edge.y+(edge.axis==='y'?1:0));return a+(b-a)*along+.08*Math.sin(Math.PI*along)**2;}
export function shorelineContour(edge,project,fraction=1){const points=[];for(let i=0;i<=16;i++){const t=i/16,d=shorelineDepth(edge,t)*fraction;points.push(edge.axis==='y'?project(edge.x+edge.sign*d,edge.y+t):project(edge.x+t,edge.y+edge.sign*d));}return points;}
export function createTerrainTransitions({paintMaterial,materialKey=()=>'',hasBank=()=>false,onMissingBank=()=>{},createCanvas=(w,h)=>{
 const canvas=typeof OffscreenCanvas==='function'?new OffscreenCanvas(w,h):globalThis.document?.createElement('canvas');if(canvas){canvas.width=w;canvas.height=h;}return canvas;
}}) {
 let key='',edges=[],revision='',pixels=0;const patches=new Map(),maxPatches=512,maxPixels=2_000_000;
 const clear=()=>{patches.clear();pixels=0;};
 const build=(edge,zoom,timeMs,bank)=>{
  const stableProject=(x,y)=>({x:(x-y)*TILE_WIDTH*zoom/2,y:(x+y)*TILE_HEIGHT*zoom/2});
  const shape=transitionGradient(edge,stableProject,edge.receiver==='ford'?.09:.40);if(land(edge.receiver))shape.points=[...shorelineContour(edge,stableProject,0),...shorelineContour(edge,stableProject).reverse()];
  const left=Math.floor(Math.min(...shape.points.map(p=>p.x)))-1,top=Math.floor(Math.min(...shape.points.map(p=>p.y)))-1;
  const width=Math.ceil(Math.max(...shape.points.map(p=>p.x)))-left+1,height=Math.ceil(Math.max(...shape.points.map(p=>p.y)))-top+1;
  if(width*height>maxPixels||width<1||height<1)return null;
  const output=createCanvas(width,height),layer=createCanvas(width,height),out=output?.getContext('2d'),c=layer?.getContext('2d');if(!out||!c)return null;
  const localProject=(x,y)=>{const p=stableProject(x,y);return {x:p.x-left,y:p.y-top};};
  const paint=(material,detail)=>{
   c.clearRect(0,0,width,height);c.save();c.beginPath();shape.points.forEach((p,i)=>i?c.lineTo(p.x-left,p.y-top):c.moveTo(p.x-left,p.y-top));c.closePath();c.clip();
   const painted=paintMaterial(c,material,{project:localProject,zoom,timeMs,bounds:{x:0,y:0,width,height}});
   if(painted){const gradient=c.createLinearGradient(shape.start.x-left,shape.start.y-top,shape.end.x-left,shape.end.y-top);
    if(detail){gradient.addColorStop(0,'rgba(0,0,0,0)');gradient.addColorStop(.5,'rgba(0,0,0,.5)');gradient.addColorStop(1,'rgba(0,0,0,0)');}
    else {gradient.addColorStop(0,'rgba(0,0,0,1)');gradient.addColorStop(1,'rgba(0,0,0,0)');}
    c.globalCompositeOperation='destination-in';if(land(edge.receiver)){const mask=createCanvas(width,height),m=mask?.getContext('2d');if(m){for(let band=0;band<24;band++){const lo=band/24,hi=(band+1)/24,alpha=detail?Math.sin(Math.PI*(lo+hi)/2)*.5:1-(lo+hi)/2;const polygon=[...shorelineContour(edge,localProject,lo),...shorelineContour(edge,localProject,hi).reverse()];m.fillStyle=`rgba(255,255,255,${alpha})`;m.beginPath();polygon.forEach((p,i)=>i?m.lineTo(p.x,p.y):m.moveTo(p.x,p.y));m.closePath();m.fill();}c.drawImage(mask,0,0);}else{c.fillStyle=gradient;c.fillRect(0,0,width,height);}}else{c.fillStyle=gradient;c.fillRect(0,0,width,height);}
   }c.restore();if(painted)out.drawImage(layer,0,0);return painted;
  };
  if(!paint(edge.source,false))return null;
  if(bank&&land(edge.receiver))paint('shore',true);
  return {canvas:output,left,top,width,height};
 };
 return {
  draw(ctx,{map,fog,project,zoom=1,timeMs=0}={}) {
   if(!map?.tiles||typeof project!=='function'||!Number.isFinite(zoom)||zoom<=0)return false;
   const topology=JSON.stringify([map.width,map.height,map.tiles]);
   const observed=fog?.visible?Array.from(fog.visible,(v,i)=>v||fog.explored?.[i]?1:0).join(''):'';
   const next=topology+observed;if(next!==key){key=next;edges=terrainTransitionEdges(map,fog);}
   const bank=hasBank();if(!bank&&edges.some(e=>land(e.receiver)))onMissingBank();
   const materials=JSON.stringify([zoom,topology,materialKey('river',timeMs),materialKey('ford',timeMs),bank?materialKey('shore',timeMs):null]);
   if(materials!==revision){revision=materials;clear();}
   let drawn=false;const origin=project(0,0),scale=ctx.getTransform?.().a||1,viewWidth=ctx.canvas?.width/scale,viewHeight=ctx.canvas?.height/scale;
   for(const edge of edges) {
    const a=project(edge.x,edge.y),b=edge.axis==='y'?project(edge.x,edge.y+1):project(edge.x+1,edge.y);const margin=32*zoom;
    if(Math.max(a.x,b.x)<-margin||Math.max(a.y,b.y)<-margin||Math.min(a.x,b.x)>viewWidth+margin||Math.min(a.y,b.y)>viewHeight+margin)continue;
    const patchKey=JSON.stringify(edge);let patch=patches.get(patchKey);
    if(!patch){patch=build(edge,zoom,timeMs,bank);if(!patch)continue;
     while(patches.size>=maxPatches||pixels+patch.width*patch.height>maxPixels){const oldest=patches.keys().next().value;if(oldest===undefined)break;const old=patches.get(oldest);pixels-=old.width*old.height;patches.delete(oldest);}
     patches.set(patchKey,patch);pixels+=patch.width*patch.height;
    }
    ctx.drawImage(patch.canvas,origin.x+patch.left,origin.y+patch.top);drawn=true;
   }return drawn;
  },
  dispose(){key='';edges=[];revision='';clear();}
 };
}
