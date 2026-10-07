import {TILE_WIDTH,TILE_HEIGHT} from './world-presentation.js';
const MAX_PIXELS=8_000_000;
/** Static presentation cache only; never owns fog, entities, resources or authoritative map data. */
export function createTerrainCache({createCanvas=(w,h)=>{
 const canvas=typeof OffscreenCanvas==='function'?new OffscreenCanvas(w,h):globalThis.document?.createElement('canvas');
 if(canvas){canvas.width=w;canvas.height=h;}return canvas;
},maxPixels=MAX_PIXELS}={}) {
 let cached=null,key='';
 const status={builds:0,draws:0,pixels:0};
 return {
  status,
  draw(ctx,{map,artRevision='',qualityScale=1,project,zoom=1,paintTile}={}) {
   if(!Number.isFinite(maxPixels)||maxPixels<1)return false;
   if(!map?.tiles||!Number.isInteger(map.width)||!Number.isInteger(map.height)||map.width<=0||map.height<=0||typeof project!=='function'||typeof paintTile!=='function'||!Number.isFinite(zoom)||zoom<=0||!Number.isFinite(qualityScale)||qualityScale<=0)return false;
   const pad=64,width=(map.width+map.height)*TILE_WIDTH/2+pad*2,height=(map.width+map.height)*TILE_HEIGHT/2+pad*2;
   // Quality may reflect zoom/DPR but total backing storage stays bounded.
   const scale=Math.min(qualityScale,Math.sqrt(maxPixels/(width*height)));
   const pixelWidth=Math.floor(width*scale),pixelHeight=Math.floor(height*scale);
   if(pixelWidth<1||pixelHeight<1||pixelWidth*pixelHeight>maxPixels)return false;
   // Exact terrain content avoids hash collisions and same-ID/new-map stale art.
   const next=JSON.stringify([map.width,map.height,map.tiles,artRevision,pixelWidth,pixelHeight]);
   if(!cached||next!==key) {
    const canvas=createCanvas(pixelWidth,pixelHeight),c=canvas?.getContext('2d');if(!c)return false;
    const origin={x:map.height*TILE_WIDTH/2+pad,y:pad};
    const worldProject=(x,y)=>({x:origin.x+(x-y)*TILE_WIDTH/2,y:origin.y+(x+y)*TILE_HEIGHT/2});
    c.setTransform(scale,0,0,scale,0,0);c.clearRect(0,0,width,height);
    for(let y=0;y<map.height;y++)for(let x=0;x<map.width;x++) {
     if(paintTile(c,{x,y,terrain:map.tiles[y*map.width+x]||'plain',project:worldProject,zoom:1,point:worldProject(x+.5,y+.5)})===false)return false;
    }
    cached={canvas,width:pixelWidth/scale,height:pixelHeight/scale,origin};key=next;status.builds++;status.pixels=pixelWidth*pixelHeight;
   }
   const origin=project(0,0);if(!Number.isFinite(origin?.x)||!Number.isFinite(origin?.y))return false;
   ctx.drawImage(cached.canvas,origin.x-cached.origin.x*zoom,origin.y-cached.origin.y*zoom,cached.width*zoom,cached.height*zoom);status.draws++;return true;
  },
  invalidate(){cached=null;key='';status.pixels=0;},
  dispose(){this.invalidate();}
 };
}
