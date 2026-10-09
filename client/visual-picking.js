// Invisible selection masks follow the artwork; they never draw replacement art.
import {fortificationContains} from './fortification-picking.js';
const alphaCache=new WeakMap();
function alphaAt(image,x,y){
 let pixels=alphaCache.get(image);
 if(!pixels){const canvas=document.createElement('canvas');canvas.width=image.width;canvas.height=image.height;const c=canvas.getContext('2d',{willReadFrequently:true});c.drawImage(image,0,0);pixels=c.getImageData(0,0,canvas.width,canvas.height);alphaCache.set(image,pixels);}
 const ix=Math.floor(x),iy=Math.floor(y);if(ix<0||iy<0||ix>=pixels.width||iy>=pixels.height)return 0;
 return pixels.data[(iy*pixels.width+ix)*4+3];
}
export function pickVisibleEntity(renderer,screenX,screenY){
 const state=renderer.state;if(!state)return null;
 const z=renderer.camera.zoom,pipeline=renderer.raster.pipeline;
 const entities=state.entities.filter(e=>e.hp>0&&!e.embarked&&renderer.visible(e,state,renderer.localPlayer)).slice().sort((a,b)=>(b.x+b.y)-(a.x+a.y)||b.id-a.id);
 for(const e of entities){const p=renderer.project(e.x,e.y);
  const raster=renderer.raster.sampleEntity(e,{tick:state.tick,timeMs:renderer.visualTimeMs??state.tick*50})?.raster;
  if(raster?.image){const width=raster.render.width*z,height=raster.render.height*z,left=p.x-raster.pivot.x/raster.sw*width,top=p.y-raster.pivot.y/raster.sh*height;
   if(screenX>=left&&screenX<left+width&&screenY>=top&&screenY<top+height&&alphaAt(raster.image,raster.sx+(screenX-left)/width*raster.sw,raster.sy+(screenY-top)/height*raster.sh)>=80)return e;
   continue;
  }
  if(e.kind==='building'&&['wall','gate'].includes(e.type)){
   if(fortificationContains(renderer,e,screenX,screenY))return e;
   continue;
  }
  const building=e.kind==='building',vehicle=['wagon','artillery','warship','transport'].includes(e.type),horse=e.type==='cavalry';
  const half=building?29:horse?19:vehicle?21:9,height=building?38:horse?36:vehicle?24:30;
  if(Math.abs(screenX-p.x)<=half*z&&screenY>=p.y-height*z&&screenY<=p.y+3*z)return e;
 }
 return null;
}
