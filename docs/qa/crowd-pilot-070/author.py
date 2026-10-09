from pathlib import Path
src=Path('shared/sim.js').read_text()
Path('docs/qa/crowd-pilot-070/baseline.js').write_text(src.replace("'./data.js'","'../../../shared/data.js'"))
src=src.replace("'./data.js'","'../../../shared/data.js'")
a=src.index('function travel('); b=src.index('function updateFog',a)
block='''export const CROWD_RADII=Object.freeze({land:0.28,naval:0.4});
const crowdRadius=e=>UNITS[e.type]?.naval?CROWD_RADII.naval:CROWD_RADII.land;
function crowdSweep(s,e,from,to){
 const stats=s.crowdStats??={tick:s.tick,plans:0,edges:0,expansions:0,waits:0};
 if(stats.tick!==s.tick){stats.tick=s.tick;stats.plans=0;stats.edges=0;}
 if(++stats.edges>4096)return false;
 if(!groundSegment(s,e,from,to))return false;
 const length=dist(from,to),parts=Math.max(1,Math.ceil(length/.1));
 for(let i=0;i<=parts;i++){const q=i/parts;if(!pass(s,e,from.x+(to.x-from.x)*q,from.y+(to.y-from.y)*q))return false;}
 const dx=to.x-from.x,dy=to.y-from.y,dd=dx*dx+dy*dy;
 return !s.entities.some(u=>{if(u.id===e.id||u.kind!=='unit'||!living(u)||!!UNITS[u.type]?.naval!==!!UNITS[e.type]?.naval)return false;const q=dd?Math.max(0,Math.min(1,((u.x-from.x)*dx+(u.y-from.y)*dy)/dd)):0;return Math.hypot(from.x+q*dx-u.x,from.y+q*dy-u.y)<crowdRadius(e)+crowdRadius(u)-1e-8;});
}
function crowdPatch(s,e,goal){
 const stats=s.crowdStats;if(stats.plans>=4){stats.waits++;return null;}stats.plans++;
 const ox=Math.round(e.x*2)/2-4.5,oy=Math.round(e.y*2)/2-4.5,nodes=[];
 for(let y=0;y<19;y++)for(let x=0;x<19;x++)nodes.push({x:ox+x*.5,y:oy+y*.5});
 const cost=new Float64Array(361).fill(Infinity),parent=new Int32Array(361).fill(-2),open=[];
 for(let i=0;i<nodes.length;i++)if(dist(e,nodes[i])<=.72&&crowdSweep(s,e,e,nodes[i])){cost[i]=dist(e,nodes[i]);parent[i]=-1;open.push(i);}
 let found=-1;const done=new Uint8Array(361);
 while(open.length){open.sort((a,b)=>(cost[a]+dist(nodes[a],goal))-(cost[b]+dist(nodes[b],goal))||a-b);const i=open.shift();if(done[i])continue;done[i]=1;stats.expansions++;
 if(dist(nodes[i],goal)<=.72&&crowdSweep(s,e,nodes[i],goal)){found=i;break;}
 const x=i%19,y=Math.floor(i/19);
 for(const [dx,dy] of [[1,0],[0,1],[-1,0],[0,-1],[1,1],[-1,1],[-1,-1],[1,-1]]){const xx=x+dx,yy=y+dy,j=yy*19+xx;if(xx<0||yy<0||xx>=19||yy>=19||done[j]||!crowdSweep(s,e,nodes[i],nodes[j]))continue;const c=cost[i]+dist(nodes[i],nodes[j]);if(c>=cost[j])continue;cost[j]=c;parent[j]=i;open.push(j);}
 }
 if(found<0){stats.waits++;return null;}const route=[{...goal}];for(let i=found;i>=0;i=parent[i])route.push(nodes[i]);route.reverse();return route;
}
function travel(s,e,target,range=0.65,finalGround=false){
 if(dist(e,target)<=range){e.path=[];e.crowdRoute=[];return true;}
 const key=`${Math.floor(target.x)},${Math.floor(target.y)},${range},${s.navVersion}`;
 if(!e.path.length||e.pathKey!==key){if(e.retryPath&&e.retryPath>s.tick)return false;e.path=path(s,e,target,range,finalGround);e.pathKey=key;e.crowdRoute=[];if(!e.path.length){e.retryPath=s.tick+20;return false;}}
 let remaining=speed(s,e)*DT;
 while(e.path.length&&remaining>1e-8){let next=e.crowdRoute?.[0]||e.path[0];const d=dist(e,next),amount=Math.min(d,remaining),to=d?{x:e.x+(next.x-e.x)*amount/d,y:e.y+(next.y-e.y)*amount/d}:next;
 if(!crowdSweep(s,e,e,to)){
  e.crowdRoute=[];if((e.crowdRetry??0)>s.tick)break;
  const goal=[...e.path].reverse().find(q=>dist(e,q)<=4&&dist(e,q)>1)||e.path[0];const route=crowdPatch(s,e,goal);e.crowdRetry=s.tick+10;if(!route)break;e.crowdRoute=route;e.crowdGoal={...goal};continue;
 }
 if(d>0)e.dir=(Math.round(Math.atan2(to.y-e.y,to.x-e.x)/(Math.PI/4))+8)%8;e.x=to.x;e.y=to.y;remaining-=amount;
 if(d<=amount+1e-8){if(e.crowdRoute?.length){e.crowdRoute.shift();if(!e.crowdRoute.length){const i=e.path.findIndex(q=>q.x===e.crowdGoal.x&&q.y===e.crowdGoal.y);if(i>=0)e.path.splice(0,i+1);}}else e.path.shift();}
 }
 e.state='walk';const arrived=dist(e,target)<=range;if(finalGround&&arrived)e.path=[];return arrived;
}
'''
Path('docs/qa/crowd-pilot-070/sim-draft.js').write_text(src[:a]+block+src[b:])
