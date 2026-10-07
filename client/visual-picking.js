// Invisible selection masks follow the artwork; they never draw replacement art.
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
 for(const e of entities){const p=renderer.project(e.x,e.y),family=e.kind==='building'?e.type:e.character||e.type,visualState=(e.hitUntil||0)>state.tick?'hit':e.state;
  const asset=renderer.raster.status.enabled&&!e.construction&&pipeline.manifest?.assets.find(a=>a.family===family&&a.state===visualState&&a.direction===(e.kind==='building'?null:e.dir));
  const raster=asset?pipeline.get(asset.id,{timeMs:state.tick*50}):null;
  if(raster?.image){const width=raster.render.width*z,height=raster.render.height*z,left=p.x-raster.pivot.x/raster.sw*width,top=p.y-raster.pivot.y/raster.sh*height;
   if(screenX>=left&&screenX<left+width&&screenY>=top&&screenY<top+height&&alphaAt(raster.image,raster.sx+(screenX-left)/width*raster.sw,raster.sy+(screenY-top)/height*raster.sh)>=80)return e;
   continue;
  }
  const building=e.kind==='building',vehicle=['wagon','artillery','warship','transport'].includes(e.type),horse=e.type==='cavalry';
  const half=building?29:horse?19:vehicle?21:9,height=building?38:horse?36:vehicle?24:30;
  if(Math.abs(screenX-p.x)<=half*z&&screenY>=p.y-height*z&&screenY<=p.y+3*z)return e;
 }
 return null;
}
