/** Actual terrain props: anchors never create knowledge or change passability. */
export function mountainPropPlacements(state,ready,{onlyVisible=true}={}){
 if(!ready||!state?.map?.tiles)return [];const {width,height,tiles}=state.map,props=[];
 for(let y=0;y<height;y+=2)for(let x=0;x<width;x+=2){const cells=[];for(let yy=y;yy<Math.min(y+2,height);yy++)for(let xx=x;xx<Math.min(x+2,width);xx++)if(tiles[yy*width+xx]==='mountain')cells.push({x:xx,y:yy});
  // Three/four connected cells share one whole illustrated mountain cluster.
  // Sparse/diagonal fragments retain their individual landmarks.
  const anchors=cells.length>=3?[{x:cells.reduce((n,c)=>n+c.x+.5,0)/cells.length,y:cells.reduce((n,c)=>n+c.y+.5,0)/cells.length,key:`mountain-cluster:${x}:${y}`}]:cells.map(c=>({x:c.x+.5,y:c.y+.5,key:`mountain:${c.x}:${c.y}`}));
  for(const a of anchors){const i=Math.floor(a.y)*width+Math.floor(a.x);if(tiles[i]!=='mountain'||onlyVisible&&!state.fog?.visible?.[i])continue;props.push({type:'mountain',...a,depth:a.x+a.y-1});}
 }return props.sort((a,b)=>a.y-b.y||a.x-b.x);
}
export function drawTerrainPropFallback(renderer,ctx,prop,zoom){const p=renderer.project(prop.x,prop.y);if(prop.type==='forest')renderer.tree(ctx,p.x,p.y,zoom,prop.variant);else if(prop.type==='mountain')renderer.rock(ctx,p.x,p.y,zoom,0);}

/** Visible passable rises are ground overlays, never depth props. */
export function hillGroundPlacements(state,ready){
 if(!ready||!state?.map?.tiles||!state.fog?.visible)return [];
 const {width,height,tiles}=state.map,visible=state.fog.visible,out=[];
 for(let y=0;y<height;y+=2)for(let x=0;x<width;x+=2){const cells=[];for(let yy=y;yy<Math.min(y+2,height);yy++)for(let xx=x;xx<Math.min(x+2,width);xx++){const i=yy*width+xx;if(tiles[i]==='hill'&&Boolean(visible[i]))cells.push({x:xx,y:yy});}if(cells.length){
   // Decoration is stable in world space, independent of current fog and unit motion.
   let hash=(Math.imul(x+1,73856093)^Math.imul(y+1,19349663)^Math.imul(width,83492791)^height)>>>0;
   hash=Math.imul(hash^(hash>>>16),0x7feb352d)>>>0;hash=Math.imul(hash^(hash>>>15),0x846ca68b)>>>0;hash=(hash^(hash>>>16))>>>0;
   let full=0,companions=0;for(let yy=y;yy<Math.min(y+2,height);yy++)for(let xx=x;xx<Math.min(x+2,width);xx++)if(tiles[yy*width+xx]==='hill')full++;
   for(const [dx,dy]of [[-2,0],[2,0],[0,-2],[0,2]]){let present=false;for(let yy=y+dy;yy<y+dy+2&&!present;yy++)for(let xx=x+dx;xx<x+dx+2;xx++)if(xx>=0&&yy>=0&&xx<width&&yy<height&&tiles[yy*width+xx]==='hill'){present=true;break;}if(present)companions++;}
   const artX=x+1+((hash&255)/255-.5)*.7,artY=y+1+(((hash>>>8)&255)/255-.5)*.7;
   out.push({type:'hill',x:x+1,y:y+1,artX,artY,drawOverlay:full<4||companions<2||(hash&3)!==0,key:`hill:${x}:${y}`,cells});
  }}
 return out;
}

export function staticResourceEligible(r){return ['food','iron'].includes(r?.type)&&Number.isFinite(r.amount)&&r.amount>0&&Number.isFinite(r.x)&&Number.isFinite(r.y);}
export function foodResourceEligible(r){return r?.type==='food'&&staticResourceEligible(r);}
