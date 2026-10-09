/** Actual terrain props: anchors never create knowledge or change passability. */
export function mountainPropPlacements(state,ready,{onlyVisible=true}={}){if(!ready||!state?.map?.tiles)return [];const {width,height,tiles}=state.map,props=[];for(let y=0;y<height;y++)for(let x=0;x<width;x++){const i=y*width+x;if(tiles[i]!=='mountain'||onlyVisible&&!state.fog?.visible?.[i])continue;props.push({type:'mountain',x:x+.5,y:y+.5,key:`mountain:${x}:${y}`,depth:x+y});}return props;}
export function drawTerrainPropFallback(renderer,ctx,prop,zoom){const p=renderer.project(prop.x,prop.y);if(prop.type==='forest')renderer.tree(ctx,p.x,p.y,zoom,prop.variant);else if(prop.type==='mountain')renderer.rock(ctx,p.x,p.y,zoom,0);}

/** Visible passable rises are ground overlays, never depth props. */
export function hillGroundPlacements(state,ready){
 if(!ready||!state?.map?.tiles||!state.fog?.visible)return [];
 const {width,height,tiles}=state.map,visible=state.fog.visible,out=[];
 for(let y=0;y<height;y+=2)for(let x=0;x<width;x+=2){const cells=[];for(let yy=y;yy<Math.min(y+2,height);yy++)for(let xx=x;xx<Math.min(x+2,width);xx++){const i=yy*width+xx;if(tiles[i]==='hill'&&Boolean(visible[i]))cells.push({x:xx,y:yy});}if(cells.length)out.push({type:'hill',x:x+1,y:y+1,key:`hill:${x}:${y}`,cells});}
 return out;
}

export function staticResourceEligible(r){return ['food','iron'].includes(r?.type)&&Number.isFinite(r.amount)&&r.amount>0&&Number.isFinite(r.x)&&Number.isFinite(r.y);}
export function foodResourceEligible(r){return r?.type==='food'&&staticResourceEligible(r);}
