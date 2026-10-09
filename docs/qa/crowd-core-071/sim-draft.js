import {visibleVillagerAction} from '../../../shared/visible-action.js';
import {UNITS,BUILDINGS,CHARACTERS,MAPS,TERRAIN,BALANCE,TICK_RATE,SYNERGIES} from '../../../shared/data.js';
const DT=1/TICK_RATE, sq=(a,b)=>(a.x-b.x)**2+(a.y-b.y)**2, dist=(a,b)=>Math.sqrt(sq(a,b));
const living=e=>e.hp>0&&!e.embarked;
const stores=e=>['residence','granary','depot'].includes(e.type)&&e.hp>0&&!e.construction;
const combatant=e=>living(e)&&(UNITS[e.type]?.damage>0||BUILDINGS[e.type]?.damage>0);
const tile=(s,x,y)=>s.map.tiles[Math.floor(y)*s.map.width+Math.floor(x)];
const bounds=(s,x,y)=>Number.isFinite(x)&&Number.isFinite(y)&&x>=0&&y>=0&&x<s.map.width&&y<s.map.height;
const get=(s,id)=>s.entities.find(e=>e.id===id&&e.hp>0);
const clone=v=>JSON.parse(JSON.stringify(v));
function modifiers(king,general){
 const m={speed:1,damage:1,vision:1,train:1,gather:1,consumption:1,heal:1,naval:1,logistics:1,fortification:1,rebuild:1,morale:0,armor:0};
 const tags=new Set();
 for(const id of [king,general]){const c=CHARACTERS[id];for(const t of c.tags)tags.add(t);for(const [k,v] of Object.entries(c.passive))m[k]=['morale','armor'].includes(k)?m[k]+v:m[k]*v;}
 const synergies=[];for(const rule of SYNERGIES)if(rule.tags.every(t=>tags.has(t))){synergies.push(rule.name);for(const [k,v] of Object.entries(rule.modifiers))m[k]=['morale','armor'].includes(k)?m[k]+v:m[k]*v;}
 return {modifiers:m,synergies,tags:[...tags]};
}
function mapData(id,seed){
 const def=MAPS.find(m=>m.id===id)||MAPS[0],{width:w,height:h}=def,tiles=Array(w*h).fill('plain');
 const put=(x,y,t)=>{if(x>=0&&y>=0&&x<w&&y<h)tiles[y*w+x]=t;};
 // Mirrored strategic geography gives both seats equal routes and resource access.
 for(let y=0;y<h;y++)for(let x=0;x<w;x++){
  const mx=Math.min(x,w-1-x);
  if(y>=40)put(x,y,'sea');
  else if(def.id==='delta'){
   if(x>=30&&x<=33)put(x,y,[9,10,11,22,23,24,34,35,36].includes(y)?'ford':'river');
   else if(((mx>=17&&mx<=23)&&(y>=6&&y<=14||y>=28&&y<=35))||mx>=4&&mx<=7&&y>=12&&y<=17)put(x,y,'forest');
   else if(mx>=22&&mx<=27&&y>=17&&y<=20)put(x,y,'hill');
   else if(mx>=1&&mx<=3&&y>=2&&y<=6)put(x,y,'mountain');
  }else{
   if(y>=7&&y<=9)put(x,y,[9,10,11,30,31,32,33,52,53,54].includes(x)?'ford':'river');
   else if(x>=29&&x<=34&&y>=12&&y<=36&&!(y>=18&&y<=21||y>=29&&y<=32))put(x,y,'mountain');
   else if(mx>=19&&mx<=25&&y>=13&&y<=34)put(x,y,'forest');
   else if(mx>=25&&mx<=28&&y>=24&&y<=28)put(x,y,'hill');
  }
 }
 const resources=[];let rid=1;
 for(const x of [9,54]){const sign=x<32?1:-1;for(const [type,dx,dy,amount] of [['food',1,-5,4200],['wood',-4,-2,4200],['iron',4,3,3200],['food',8,9,3500],['wood',10,-10,3500],['iron',13,11,2600]]){
 const rx=x+sign*dx,ry=23+dy;put(rx,ry,type==='wood'?'forest':'plain');resources.push({id:rid++,type,x:rx+0.5,y:ry+0.5,amount});}}
 for(const [x,y,type] of [[25,10,'food'],[38,10,'food'],[24,35,'iron'],[39,35,'iron']]){put(x,y,'plain');resources.push({id:rid++,type,x:x+0.5,y:y+0.5,amount:2400});}
 return {...def,tiles,resources,seed,spawns:[{x:9.5,y:23.5},{x:54.5,y:23.5}]};
}
function add(s,owner,type,x,y,extra={}){
 const u=UNITS[type],b=BUILDINGS[type],d=u||b,m=s.players[owner].modifiers;
 const e={id:s.nextId++,owner,type,kind:u?'unit':'building',x,y,hp:d.hp*(['fort','wall','gate'].includes(type)?m.fortification:1),maxHp:d.hp*(['fort','wall','gate'].includes(type)?m.fortification:1),food:u?d.foodMax:0,foodMax:u?d.foodMax:0,morale:Math.min(100,80+m.morale),state:'idle',dir:owner===0?0:4,cooldown:0,order:null,path:[],queue:[],cargo:{food:0,wood:0,iron:0,units:[]},...extra};
 if(type==='king'||type==='general'){e.character=s.players[owner][type];e.abilityCooldown=0;}
 s.entities.push(e);return e;
}
function event(s,text,owner=null){s.events.push({tick:s.tick,text,owner});if(s.events.length>40)s.events.shift();}
function economy(s){for(const p of s.players){p.resources.food=s.entities.filter(e=>e.owner===p.id&&stores(e)).reduce((sum,e)=>sum+e.cargo.food,0);p.population=s.entities.filter(e=>e.owner===p.id&&e.kind==='unit'&&e.hp>0).length;p.populationQueued=s.entities.filter(e=>e.owner===p.id&&e.hp>0).reduce((n,e)=>n+e.queue.length,0);}}
export function createMatch({mapId='delta',seed=1,players=[{},{}],aiPlayer=null,difficulty='normal'}={}){
 const state={tick:0,seed:seed>>>0,map:mapData(mapId,seed),players:[],entities:[],nextId:1,winner:null,reason:'',events:[],aiPlayer:aiPlayer===0||aiPlayer===1?aiPlayer:null,difficulty:['easy','normal','hard'].includes(difficulty)?difficulty:'normal',effects:[],fog:[0,1].map(()=>({visible:Array(64*48).fill(false),explored:Array(64*48).fill(false),resources:{}})),navVersion:0};
 for(let i=0;i<2;i++){const input=players[i]||{},king=typeof input.king==='string'&&Object.hasOwn(CHARACTERS,input.king)?input.king:'tran_nhan_tong',general=typeof input.general==='string'&&Object.hasOwn(CHARACTERS,input.general)?input.general:'tran_hung_dao';state.players.push({id:i,name:String(input.name||`Player ${i+1}`).slice(0,24),king,general,...modifiers(king,general),resources:{wood:550,food:0,iron:260},population:0,populationCap:BALANCE.populationCap,stats:{kills:0,lost:0,gathered:0,foodTransported:0,buildingsDestroyed:0,wagonsDestroyed:0,abilities:0},ai:{phase:0,scout:0}});}
 for(let p=0;p<2;p++){const {x,y}=state.map.spawns[p],sign=p===0?1:-1;
  add(state,p,'residence',x,y,{cargo:{food:430,wood:0,iron:0,units:[]}});
  add(state,p,'granary',x-sign*3,y+3,{cargo:{food:260,wood:0,iron:0,units:[]}});
  add(state,p,'depot',x+sign*4,y+5,{cargo:{food:120,wood:0,iron:0,units:[]}});
  add(state,p,'barracks',x+sign*4,y-3);
  add(state,p,'king',x-sign*2,y+1.5);
  add(state,p,'general',x+sign*1.5,y+2);
  for(let j=0;j<6;j++)add(state,p,'villager',x-sign*2+(j%3)*0.6,y-2-Math.floor(j/3)*0.6);
  for(let j=0;j<4;j++)add(state,p,j===3?'spearman':'infantry',x+sign*6,y+j*0.65);
  add(state,p,'wagon',x+sign*3,y+7,{cargo:{food:100,wood:0,iron:0,units:[]}});
 }
 economy(state);updateFog(state);return state;
}
function terrainPass(s,e,x,y){if(!bounds(s,x,y))return false;const t=tile(s,x,y);if(UNITS[e.type]?.naval)return !!TERRAIN[t]?.water;return !TERRAIN[t]?.impassable&&(!TERRAIN[t]?.water||TERRAIN[t]?.land);}
const navigationBuildings=new WeakMap();
function blockers(s){const cached=navigationBuildings.get(s);if(cached?.version===s.navVersion)return cached.list;const list=s.entities.filter(e=>e.kind==='building'&&e.hp>0);navigationBuildings.set(s,{version:s.navVersion,list});return list;}
function pass(s,e,x,y){if(!terrainPass(s,e,x,y))return false;return !blockers(s).some(b=>b.id!==e.id&&!(b.type==='gate'&&b.owner===e.owner)&&Math.abs(x-b.x)<BUILDINGS[b.type].radius+0.15&&Math.abs(y-b.y)<BUILDINGS[b.type].radius+0.15);}
// Diagonal steps require both side cells, using the same terrain/building rules as destinations.
function navigationStep(s,e,x,y,xx,yy){return pass(s,e,xx,yy)&&(x===xx||y===yy||pass(s,e,xx,y)&&pass(s,e,x,yy));}
// Final ground segments remain inside a reachable cell and cannot cross building interiors.
function groundSegment(s,e,from,to){
 if(!navigationStep(s,e,from.x,from.y,to.x,to.y))return false;
 return !blockers(s).some(b=>{if(b.id===e.id||b.type==='gate'&&b.owner===e.owner)return false;const r=BUILDINGS[b.type].radius+0.15;let lo=0,hi=1;
  for(const axis of ['x','y']){const delta=to[axis]-from[axis],min=b[axis]-r,max=b[axis]+r;if(delta===0){if(from[axis]<=min||from[axis]>=max)return false;}else{const a=(min-from[axis])/delta,z=(max-from[axis])/delta;lo=Math.max(lo,Math.min(a,z));hi=Math.min(hi,Math.max(a,z));if(lo>=hi)return false;}}
  return lo<hi;
 });
}
function path(s,e,target,range=0.4,finalGround=false){
 const w=s.map.width,h=s.map.height,sx=Math.floor(e.x),sy=Math.floor(e.y),start=sy*w+sx;
 const parents=new Int32Array(w*h).fill(-2),costs=new Float64Array(w*h).fill(Infinity),heap=[];let serial=0;
 const before=(a,b)=>a.cost<b.cost||a.cost===b.cost&&a.order<b.order;
 const push=(i,cost)=>{const node={i,cost,order:serial++};let n=heap.length;heap.push(node);while(n){const p=(n-1)>>1;if(!before(node,heap[p]))break;heap[n]=heap[p];n=p;}heap[n]=node;};
 const pop=()=>{const first=heap[0],last=heap.pop();if(heap.length){let n=0;while(n*2+1<heap.length){let c=n*2+1;if(c+1<heap.length&&before(heap[c+1],heap[c]))c++;if(!before(heap[c],last))break;heap[n]=heap[c];n=c;}heap[n]=last;}return first;};
 costs[start]=0;parents[start]=-1;push(start,0);let found=-1,best=start,bestD=Infinity;
 // Fixed neighbor order and insertion ties make equal-cost routes reproducible.
 const neighbors=[[1,0],[0,1],[-1,0],[0,-1],[1,1],[-1,1],[-1,-1],[1,-1]];
 while(heap.length){const {i,cost}=pop();if(cost!==costs[i])continue;const x=i%w,y=Math.floor(i/w),dd=(x+0.5-target.x)**2+(y+0.5-target.y)**2;if(dd<bestD){bestD=dd;best=i;}if((dd<=range**2&&pass(s,e,x+0.5,y+0.5))||(finalGround&&x===Math.floor(target.x)&&y===Math.floor(target.y)&&groundSegment(s,e,{x:x+0.5,y:y+0.5},target))){found=i;break;}
  for(const [dx,dy] of neighbors){const xx=x+dx,yy=y+dy,j=yy*w+xx;if(xx<0||yy<0||xx>=w||yy>=h||!navigationStep(s,e,x+0.5,y+0.5,xx+0.5,yy+0.5))continue;const nextCost=cost+(dx&&dy?Math.SQRT2:1);if(nextCost>=costs[j])continue;costs[j]=nextCost;parents[j]=i;push(j,nextCost);}
 }
 if(found<0)found=best;const result=[];for(let i=found;i!==start&&i>=0;i=parents[i])result.push({x:i%w+0.5,y:Math.floor(i/w)+0.5});result.reverse();if(finalGround){const end={x:found%w+0.5,y:Math.floor(found/w)+0.5};if(dist(end,target)>range&&Math.floor(end.x)===Math.floor(target.x)&&Math.floor(end.y)===Math.floor(target.y)&&groundSegment(s,e,end,target))result.push({x:target.x,y:target.y,finalGround:true});}return result;
}
function active(s,e,kind){return s.effects.some(f=>f.owner===e.owner&&f.kind===kind&&f.until>s.tick&&(f.global||dist(e,f)<f.radius));}
function speed(s,e){const m=s.players[e.owner].modifiers,t=tile(s,e.x,e.y),r=e.food/e.foodMax;let v=UNITS[e.type].speed*m.speed*(TERRAIN[t]?.speed||1);if(UNITS[e.type].naval)v*=m.naval;if(e.type==='cavalry'&&t==='forest')v*=0.7;if(r<BALANCE.lowSupply)v*=r>0?0.85:0.6;if(active(s,e,'tempo')||active(s,e,'concentrate')||active(s,e,'deception'))v*=1.4;if(e.type==='wagon'&&active(s,e,'network'))v*=1.4;return v;}
export const CROWD_RADII=Object.freeze({land:0.28,naval:0.4});
const crowdRadius=e=>UNITS[e.type]?.naval?CROWD_RADII.naval:CROWD_RADII.land;
function crowdPrepare(s){
 if(s.crowdIndex?.tick===s.tick)return;
 const buckets={};for(const u of [...s.entities].sort((a,b)=>a.id-b.id)){if(u.kind!=='unit'||!living(u))continue;const key=`${Math.floor(u.x)},${Math.floor(u.y)}`;(buckets[key]??=[]).push(u.id);}
 const ids=s.entities.filter(u=>u.kind==='unit'&&living(u)&&u.order&& !u.pendingAttack&&u.order.type!=='hold').map(u=>u.id).sort((a,b)=>a-b);
 const offset=ids.length?s.tick%ids.length:0,eligible=ids.slice(offset).concat(ids.slice(0,offset)).slice(0,4);
 s.crowdIndex={tick:s.tick,buckets};s.crowdStats??={plans:0,edges:0,expansions:0,waits:0,queries:0,bodyChecks:0,rebuilds:0};Object.assign(s.crowdStats,{tick:s.tick,plans:0,edges:0,eligible});s.crowdStats.rebuilds++;
}
function crowdUpdate(s,e,old){const buckets=s.crowdIndex.buckets,from=`${Math.floor(old.x)},${Math.floor(old.y)}`,to=`${Math.floor(e.x)},${Math.floor(e.y)}`;if(from===to)return;buckets[from]=(buckets[from]||[]).filter(id=>id!==e.id);(buckets[to]??=[]).push(e.id);buckets[to].sort((a,b)=>a-b);}
function crowdSweep(s,e,from,to){
 crowdPrepare(s);const stats=s.crowdStats;if(++stats.edges>4096)return false;
 if(!groundSegment(s,e,from,to))return false;
 const length=dist(from,to),parts=Math.max(1,Math.ceil(length/.1));for(let i=0;i<=parts;i++){const q=i/parts;if(!pass(s,e,from.x+(to.x-from.x)*q,from.y+(to.y-from.y)*q))return false;}
 const ids=new Set();stats.queries++;const margin=crowdRadius(e)+CROWD_RADII.naval;
 for(let y=Math.floor(Math.min(from.y,to.y)-margin);y<=Math.floor(Math.max(from.y,to.y)+margin);y++)for(let x=Math.floor(Math.min(from.x,to.x)-margin);x<=Math.floor(Math.max(from.x,to.x)+margin);x++)for(const id of s.crowdIndex.buckets[`${x},${y}`]||[])ids.add(id);
 const dx=to.x-from.x,dy=to.y-from.y,dd=dx*dx+dy*dy;
 for(const id of [...ids].sort((a,b)=>a-b)){if(id===e.id)continue;const u=get(s,id);if(!u||!living(u)||!!UNITS[u.type]?.naval!==!!UNITS[e.type]?.naval)continue;stats.bodyChecks++;const q=dd?Math.max(0,Math.min(1,((u.x-from.x)*dx+(u.y-from.y)*dy)/dd)):0;if(Math.hypot(from.x+q*dx-u.x,from.y+q*dy-u.y)<crowdRadius(e)+crowdRadius(u)-1e-8)return false;}return true;
}
function crowdPatch(s,e,goal){
 const stats=s.crowdStats;if(stats.plans>=4||!stats.eligible.includes(e.id)){stats.waits++;return null;}stats.plans++;
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
 if(d>0)e.dir=(Math.round(Math.atan2(to.y-e.y,to.x-e.x)/(Math.PI/4))+8)%8;const old={x:e.x,y:e.y};e.x=to.x;e.y=to.y;crowdUpdate(s,e,old);remaining-=amount;
 if(d<=amount+1e-8){if(e.crowdRoute?.length){e.crowdRoute.shift();if(!e.crowdRoute.length){const i=e.path.findIndex(q=>q.x===e.crowdGoal.x&&q.y===e.crowdGoal.y);if(i>=0)e.path.splice(0,i+1);}}else e.path.shift();}
 }
 e.state='walk';const arrived=dist(e,target)<=range;if(finalGround&&arrived)e.path=[];return arrived;
}
function updateFog(s){
 const {width:w,height:h}=s.map;
 for(const p of s.players){const f=s.fog[p.id];f.visible.fill(false);for(const e of s.entities){if(e.owner!==p.id||!living(e))continue;const d=UNITS[e.type]||BUILDINGS[e.type],r=(d.vision||6)*p.modifiers.vision+(TERRAIN[tile(s,e.x,e.y)]?.vision||0);for(let y=Math.max(0,Math.floor(e.y-r));y<Math.min(h,Math.ceil(e.y+r));y++)for(let x=Math.max(0,Math.floor(e.x-r));x<Math.min(w,Math.ceil(e.x+r));x++)if((x+0.5-e.x)**2+(y+0.5-e.y)**2<=r*r){f.visible[y*w+x]=true;f.explored[y*w+x]=true;}}for(const r of s.map.resources)if(f.visible[Math.floor(r.y)*w+Math.floor(r.x)])f.resources[r.id]=clone(r);}
}
function visible(s,owner,e){if(e.embarked||!s.fog[owner].visible[Math.floor(e.y)*s.map.width+Math.floor(e.x)])return false;if(e.owner===owner)return true;const concealed=tile(s,e.x,e.y)==='forest'||active(s,e,'deception');return !concealed||s.entities.some(u=>u.owner===owner&&living(u)&&dist(u,e)<=3.5);}
function affordable(s,p,cost){economy(s);return ['wood','food','iron'].every(k=>s.players[p].resources[k]+1e-8>=(cost[k]||0));}
function spend(s,p,cost,origin){s.players[p].resources.wood-=cost.wood||0;s.players[p].resources.iron-=cost.iron||0;let remaining=cost.food||0;const nodes=s.entities.filter(e=>e.owner===p&&stores(e)).sort((a,b)=>dist(a,origin)-dist(b,origin)||a.id-b.id);for(const e of nodes){const n=Math.min(e.cargo.food,remaining);e.cargo.food-=n;remaining-=n;}economy(s);}
function placement(s,p,type,x,y){const d=BUILDINGS[type];if(!bounds(s,x,y)||!terrainPass(s,{type:'villager'},x,y)||tile(s,x,y)==='ford')return false;
 if(d.coastal&&!s.map.tiles.some((t,i)=>TERRAIN[t]?.water&&Math.abs(i%s.map.width+0.5-x)<=3&&Math.abs(Math.floor(i/s.map.width)+0.5-y)<=3))return false;
 return !s.entities.some(e=>e.hp>0&&!e.embarked&&(e.kind==='building'?Math.abs(e.x-x)<BUILDINGS[e.type].radius+d.radius+0.4&&Math.abs(e.y-y)<BUILDINGS[e.type].radius+d.radius+0.4:Math.abs(e.x-x)<d.radius+0.2&&Math.abs(e.y-y)<d.radius+0.2));
}
const reject=error=>({ok:false,error});
export function command(s,p,c){
 if(p!==0&&p!==1)return reject('Invalid player');if(s.winner!==null)return reject('Match finished');if(!c||typeof c!=='object'||Array.isArray(c)||typeof c.type!=='string')return reject('Invalid command');
 if(c.type==='surrender'){s.winner=1-p;s.reason='Surrender';event(s,`${s.players[p].name} surrendered`);return {ok:true};}
 if(c.type==='cancel'){
  const b=get(s,c.building);if(!b||b.owner!==p||!b.construction)return reject('Select own unfinished building');const fraction=b.construction.remaining/b.construction.total*0.65,cost=b.spentCost||BUILDINGS[b.type].cost;for(const k of ['wood','iron'])s.players[p].resources[k]+=(cost[k]||0)*fraction;for(const u of s.entities)if(u.order?.target===b.id&&u.order.type==='build')u.order=null;b.hp=0;b.deadTick=s.tick;b.state='death';s.navVersion++;event(s,'Construction canceled',p);return {ok:true};
 }
 if(c.type==='train'){
  const b=get(s,c.building),u=typeof c.unit==='string'&&Object.hasOwn(UNITS,c.unit)?UNITS[c.unit]:null;if(!b||b.owner!==p||b.kind!=='building'||b.construction||!u||!BUILDINGS[b.type].trains?.includes(c.unit))return reject('Invalid production order');
  economy(s);if(b.queue.length>=BALANCE.queueCap)return reject('Production queue full');if(s.players[p].population+s.players[p].populationQueued>=BALANCE.populationCap)return reject('Population limit');if(!affordable(s,p,u.cost))return reject('Not enough resources');
  spend(s,p,u.cost,b);b.queue.push({unit:c.unit,remaining:u.trainTime*s.players[p].modifiers.train});return {ok:true};
 }
 if(!Array.isArray(c.ids)||c.ids.length<1||c.ids.length>BALANCE.commandUnits||c.ids.some(id=>!Number.isSafeInteger(id)))return reject('Select units');
 const ids=[...new Set(c.ids)],es=ids.map(id=>get(s,id));if(es.some(e=>!e||e.owner!==p||e.kind!=='unit'||e.embarked))return reject('Invalid unit ownership');
 if(['move','attackMove'].includes(c.type)){
  if(!bounds(s,c.x,c.y))return reject('Invalid destination');if(es.some(e=>active(s,e,'shock')))return reject('Assault commitment prevents retreat orders');
  for(const [i,e] of es.entries()){const offset=es.length>1?{x:(i%5-2)*0.45,y:(Math.floor(i/5)%5-2)*0.45}:{x:0,y:0};const target={x:Math.max(0.5,Math.min(s.map.width-0.5,c.x+offset.x)),y:Math.max(0.5,Math.min(s.map.height-0.5,c.y+offset.y))};cancelAttack(e);e.order={type:c.type,...target};e.path=[];e.retryPath=0;e.state='walk';}return {ok:true};
 }
 if(c.type==='stop'||c.type==='hold'){if(es.some(e=>active(s,e,'shock')))return reject('Assault commitment is active');for(const e of es){cancelAttack(e);e.order=c.type==='hold'?{type:'hold'}:null;e.path=[];e.state='idle';}return {ok:true};}
 if(c.type==='attack'){
  const t=get(s,c.target);updateFog(s);if(!t||t.owner===p||!visible(s,p,t)||es.some(e=>UNITS[e.type].damage===0))return reject('Target cannot be attacked');for(const e of es){if(e.pendingAttack&&e.pendingAttack.target!==t.id)cancelAttack(e);e.order={type:'attack',target:t.id,lastX:t.x,lastY:t.y};e.path=[];e.retryPath=0;}return {ok:true};
 }
 if(c.type==='repair'){
  const b=get(s,c.target);if(es.length!==1||!b||b.kind!=='building'||b.owner!==p||!['king','villager'].includes(es[0].type)||(b.type==='residence'?es[0].type!=='king':es[0].type!=='villager'))return reject('Select a suitable friendly builder');
  const route=path(s,es[0],b,BUILDINGS[b.type].radius+1.25);if(dist(es[0],b)>BUILDINGS[b.type].radius+1.25&&(!route.length||dist(route.at(-1),b)>BUILDINGS[b.type].radius+1.25))return reject('Builder cannot reach this building');
  cancelAttack(es[0]);es[0].order={type:b.construction?'build':'repair',target:b.id};es[0].path=[];es[0].retryPath=0;if(b.construction)b.construction.builder=es[0].id;return {ok:true};
 }
 if(c.type==='gather'){
  const r=s.map.resources.find(r=>r.id===c.target&&r.amount>0);if(!r||es.some(e=>e.type!=='villager'))return reject('Invalid gathering order');updateFog(s);if(!s.fog[p].explored[Math.floor(r.y)*s.map.width+Math.floor(r.x)])return reject('Resource not discovered');for(const e of es){cancelAttack(e);e.order={type:'gather',target:r.id};e.path=[];e.retryPath=0;}return {ok:true};
 }
 if(c.type==='build'){
  const d=typeof c.building==='string'&&Object.hasOwn(BUILDINGS,c.building)?BUILDINGS[c.building]:null;if(!d||es.length!==1||!['king','villager'].includes(es[0].type))return reject('Invalid builder');
  if(c.building==='residence'&&(es[0].type!=='king'||s.entities.some(e=>e.owner===p&&e.type==='residence'&&e.hp>0)))return reject('Only the King may replace a destroyed Main Residence');
  if(c.building!=='residence'&&es[0].type!=='villager')return reject('Select a villager');if(!bounds(s,c.x,c.y))return reject('Invalid construction site');
  const x=Math.floor(c.x)+0.5,y=Math.floor(c.y)+0.5;if(!s.fog[p].visible[Math.floor(y)*s.map.width+Math.floor(x)])return reject('Construction site must be visible');if(!placement(s,p,c.building,x,y))return reject('Construction site blocked or shipyard is inland');
  const route=path(s,es[0],{x,y},d.radius+1.25);if(dist(es[0],{x,y})>d.radius+1.25&&(!route.length||dist(route.at(-1),{x,y})>d.radius+1.25))return reject('Builder cannot reach this site');
  const cost={...d.cost};if(c.building==='residence')cost.wood*=s.players[p].modifiers.rebuild;if(!affordable(s,p,cost))return reject('Not enough resources');spend(s,p,cost,es[0]);const b=add(s,p,c.building,x,y,{hp:d.hp*0.12,spentCost:cost,construction:{remaining:d.buildTime,total:d.buildTime,builder:es[0].id},cargo:{food:0,wood:0,iron:0,units:[]}});s.navVersion++;cancelAttack(es[0]);es[0].order={type:'build',target:b.id};es[0].path=[];es[0].retryPath=0;return {ok:true,entity:b.id};
 }
 if(c.type==='load'||c.type==='unload'){
  const target=get(s,c.target);if(es.some(e=>!['wagon','transport'].includes(e.type)))return reject('Select a wagon or transport');if(!target||target.owner!==p)return reject('Select friendly cargo source or destination');
  for(const e of es){if(e.type==='wagon'&&(!stores(target)||e.id===target.id))return reject('Wagons transfer food with completed stores');if(e.type==='transport'&&c.type==='load'&&(target.kind!=='unit'||UNITS[target.type].naval||target.embarked||target.id===e.id))return reject('Invalid passenger');}
  for(const e of es){cancelAttack(e);e.order={type:c.type,target:target.id};e.path=[];e.retryPath=0;}return {ok:true};
 }
 if(c.type==='ability'){
  if(es.some(e=>!e.character||e.abilityCooldown>0))return reject('Ability unavailable');
  for(const e of es){const a=CHARACTERS[e.character].ability;if(a.kind==='riverTrap'&&!s.map.tiles.some((t,i)=>TERRAIN[t]?.water&&Math.abs(i%s.map.width+0.5-e.x)<=5&&Math.abs(Math.floor(i/s.map.width)+0.5-e.y)<=5))return reject('Prepare this ability near a river, ford or coast');}
  for(const e of es){const a=CHARACTERS[e.character].ability;e.abilityCooldown=a.cooldown*TICK_RATE;s.effects.push({owner:p,source:e.id,kind:a.kind,x:e.x,y:e.y,radius:a.kind==='riverTrap'?5:9,until:s.tick+a.duration*TICK_RATE,global:['mobilize','fiscal','network'].includes(a.kind)});if(a.kind==='shock')for(const u of s.entities.filter(u=>u.owner===p&&living(u)&&u.kind==='unit'&&dist(e,u)<9))u.food=Math.max(0,u.food-8);s.players[p].stats.abilities++;event(s,`${a.name} activated`,p);}return {ok:true};
 }
 return reject('Unknown command');
}
function cancelAttack(e){delete e.pendingAttack;delete e.attackStartedTick;delete e.attackImpactTick;delete e.attackCueKind;}
function hurt(s,e,damage,attacker){
 if(e.hp<=0||s.winner!==null)return;e.hp=Math.max(0,e.hp-damage);e.hitUntil=s.tick+5;e.morale=Math.max(5,e.morale-damage*0.13);
 if(e.type==='general'&&s.tick%20<2)event(s,e.hp/e.maxHp<0.3?'GENERAL LOW HP':'GENERAL UNDER ATTACK',e.owner);
 if(e.hp>0)return;cancelAttack(e);e.state='death';e.deadTick=s.tick;e.order=null;e.path=[];s.players[e.owner].stats.lost++;
 if(attacker){s.players[attacker.owner].stats.kills++;if(e.kind==='building')s.players[attacker.owner].stats.buildingsDestroyed++;if(e.type==='wagon')s.players[attacker.owner].stats.wagonsDestroyed++;}
 if(e.kind==='building')s.navVersion++;
 if(e.type==='transport')for(const id of e.cargo.units){const passenger=get(s,id);if(passenger)hurt(s,passenger,passenger.hp,attacker);}
 if(e.type==='residence')event(s,'MAIN RESIDENCE DESTROYED — King may rebuild',e.owner);
 if(['wagon','granary','depot'].includes(e.type))event(s,'SUPPLY LINE DISRUPTED',e.owner);
 if(e.type==='general'){s.winner=1-e.owner;s.reason='Enemy General defeated';event(s,`${s.players[e.owner].name}'s General has fallen`);}
}
function attack(s,e,t){
 const d=UNITS[e.type]||BUILDINGS[e.type],range=d.range+(TERRAIN[tile(s,e.x,e.y)]?.range||0);
 if(e.pendingAttack)return true;
 if(dist(e,t)>range+0.25){if(e.kind==='unit'&&e.order?.type!=='hold')travel(s,e,t,range);return false;}
 e.state='attack';e.dir=(Math.round(Math.atan2(t.y-e.y,t.x-e.x)/(Math.PI/4))+8)%8;
 if(s.tick<(e.attackReadyTick??0)||e.attackReadyTick===undefined&&e.cooldown>0)return true;
 const windup=d.attackWindupTicks,recovery=Math.ceil(d.cooldown*TICK_RATE/(active(s,e,'concentrate')&&e.type==='artillery'?1.3:1));
 e.attackStartedTick=s.tick;e.attackImpactTick=s.tick+windup;e.attackCueKind=d.attackCueKind;
 e.attackReadyTick=e.attackImpactTick+recovery;e.cooldown=(windup+recovery)/TICK_RATE;
 e.pendingAttack={target:t.id,x:e.x,y:e.y,orderType:e.order?.type||null};return true;
}
function resolveAttack(s,e){
 const pending=e.pendingAttack;if(!pending)return;
 const sameOrder=pending.orderType===(e.order?.type||null)&&(pending.orderType!=='attack'||e.order.target===pending.target);
 if(!living(e)||e.construction||!sameOrder||e.x!==pending.x||e.y!==pending.y){cancelAttack(e);return;}
 if(s.tick<e.attackImpactTick)return;
 delete e.pendingAttack;
 const t=get(s,pending.target),d=UNITS[e.type]||BUILDINGS[e.type],terrain=tile(s,e.x,e.y),range=d.range+(TERRAIN[terrain]?.range||0);
 if(!t||!living(t)||t.owner===e.owner||!visible(s,e.owner,t)||dist(e,t)>range+.25){cancelAttack(e);e.state='idle';return;}
 const m=s.players[e.owner].modifiers,targetTerrain=tile(s,t.x,t.y);
 let damage=d.damage*m.damage*(d.bonus?.[t.type]||d.bonus?.[t.kind]||1);
 if(e.foodMax&&e.food/e.foodMax<BALANCE.lowSupply)damage*=e.food>0?0.85:0.55;damage*=0.7+e.morale/250;
 if(terrain==='forest'&&!e.lastAttack||terrain==='forest'&&s.tick-e.lastAttack>100)damage*=1.25;
 if(active(s,e,'shock'))damage*=1.45;if(active(s,e,'tempo')&&e.lastMovedTick>s.tick-40)damage*=1.3;
 if(s.players[e.owner].tags.includes('SUPPLY_DENIAL')&&['wagon','granary','depot','transport'].includes(t.type))damage*=1.2;
 let armor=(UNITS[t.type]||BUILDINGS[t.type]).armor*(['fort','wall','gate'].includes(t.type)?s.players[t.owner].modifiers.fortification:1)+(TERRAIN[targetTerrain]?.armor||0)+s.players[t.owner].modifiers.armor;if(active(s,t,'riverDefense')&&(targetTerrain==='ford'||s.entities.some(b=>b.owner===t.owner&&b.kind==='building'&&b.hp>0&&dist(b,t)<5)))armor+=6;
 hurt(s,t,Math.max(1,damage-armor),e);if(d.splash)for(const other of s.entities)if(other.owner!==e.owner&&other.id!==t.id&&living(other)&&dist(other,t)<d.splash)hurt(s,other,Math.max(1,(damage-armor)*0.35),e);
 e.lastAttack=s.tick;
}
function nearestEnemy(s,e,r){let best=null,bestScore=Infinity;for(const t of s.entities){if(!living(t)||t.owner===e.owner||!visible(s,e.owner,t)||dist(e,t)>r)continue;if(UNITS[e.type]?.naval&&UNITS[t.type]?.naval===false&&dist(e,t)>UNITS[e.type].range)continue;const score=dist(e,t)+(t.type==='general'?-2:0)+(t.kind==='building'?2:0);if(score<bestScore){best=t;bestScore=score;}}return best;}
function resupply(s,e){
 const m=s.players[e.owner].modifiers;for(const b of s.entities){if(b.owner!==e.owner||b.hp<=0||b.construction||b.embarked||!['granary','residence','wagon'].includes(b.type)||b.id===e.id)continue;const r=(b.type==='wagon'?3:BUILDINGS[b.type].resupplyRadius||3)*m.logistics*(active(s,e,'network')?1.4:1);if(dist(e,b)>r)continue;const n=Math.min(e.foodMax-e.food,b.cargo.food,BALANCE.resupplyPerSecond*DT);if(n>0){b.cargo.food-=n;e.food+=n;e.resuppliedTick=s.tick;if(b.type==='wagon')s.players[e.owner].stats.foodTransported+=n;}if(e.food>=e.foodMax-1e-6)break;}
}
function gather(s,e,r){
 const total=e.cargo.wood+e.cargo.food+e.cargo.iron;
 if(total>=BALANCE.carry-1e-6||!r||r.amount<=0){const nodes=s.entities.filter(b=>b.owner===e.owner&&stores(b)&&(e.cargo.food<=0||b.cargo.food<BUILDINGS[b.type].capacity));nodes.sort((a,b)=>dist(e,a)-dist(e,b)||a.id-b.id);const b=nodes[0];if(!b){e.state='idle';return;}if(travel(s,e,b,BUILDINGS[b.type].radius+1)){
  const m=s.players[e.owner].modifiers,bonus=active(s,e,'fiscal')?1.35:1;
  s.players[e.owner].resources.wood+=e.cargo.wood*bonus;s.players[e.owner].resources.iron+=e.cargo.iron*bonus;
  const n=Math.min(e.cargo.food,BUILDINGS[b.type].capacity-b.cargo.food);b.cargo.food+=n;e.cargo.food-=n;e.cargo.wood=0;e.cargo.iron=0;e.path=[];if(!r||r.amount<=0){e.order=null;event(s,'Resource patch exhausted',e.owner);}e.state='carry';}return;}
 if(travel(s,e,r,1.1)){if(e.gatherEpisode?.target!==r.id||e.gatherEpisode.lastTick!==s.tick-1)e.gatherEpisode={target:r.id,startedTick:s.tick,lastTick:s.tick};else e.gatherEpisode.lastTick=s.tick;const amount=Math.min(r.amount,BALANCE.carry-total,BALANCE.gatherPerSecond*DT*s.players[e.owner].modifiers.gather*(active(s,e,'inspection')?1.45:1));r.amount-=amount;e.cargo[r.type]+=amount;s.players[e.owner].stats.gathered+=amount;e.state='gather';}
}
function transfer(s,e,t,kind){
 if(e.type==='wagon'){
  if(!stores(t)){e.order=null;return;}if(travel(s,e,t,BUILDINGS[t.type].radius+1.1)){
   const source=kind==='load'?t:e,dest=kind==='load'?e:t,capacity=kind==='load'?UNITS.wagon.capacity:BUILDINGS[t.type].capacity,n=Math.min(source.cargo.food,capacity-dest.cargo.food,40*DT);
   if(n>0){source.cargo.food-=n;dest.cargo.food+=n;if(kind==='unload')s.players[e.owner].stats.foodTransported+=n;}e.state=kind==='load'?'carry':'idle';if(n<=1e-8)e.order=null;
  }return;
 }
 if(kind==='load'){
  if(!t||t.embarked||t.kind!=='unit'||UNITS[t.type].naval){e.order=null;return;}if(travel(s,e,t,2.6)&&dist(e,t)<=2.6){if(e.cargo.units.length<UNITS.transport.capacity){cancelAttack(t);t.embarked=e.id;t.order=null;t.path=[];e.cargo.units.push(t.id);}e.order=null;}
 }else{
  const candidates=[];for(let y=Math.floor(e.y)-3;y<=Math.floor(e.y)+3;y++)for(let x=Math.floor(e.x)-3;x<=Math.floor(e.x)+3;x++)if(pass(s,{type:'villager',owner:e.owner},x+0.5,y+0.5)&&dist(e,{x:x+0.5,y:y+0.5})<=3)candidates.push({x:x+0.5,y:y+0.5});
  if(!candidates.length){travel(s,e,t,2.5);return;}for(const id of e.cargo.units){const u=get(s,id);if(u){const spot=candidates[0];u.x=spot.x;u.y=spot.y;u.embarked=null;u.state='idle';}}e.cargo.units=[];e.order=null;
 }
}
function spawnPoint(s,b,type){const e={type,owner:b.owner};let best=null;for(let r=1;r<=4&&!best;r++)for(let y=-r;y<=r&&!best;y++)for(let x=-r;x<=r&&!best;x++){if(Math.abs(x)!==r&&Math.abs(y)!==r)continue;const xx=Math.floor(b.x)+x+0.5,yy=Math.floor(b.y)+y+0.5;if(pass(s,e,xx,yy))best={x:xx,y:yy};}return best;}
function tickBuilding(s,b){
 if(b.construction){const u=get(s,b.construction.builder);if(u&&u.order?.type==='build'&&u.order.target===b.id&&dist(u,b)<=BUILDINGS[b.type].radius+1.4){const amount=DT*(active(s,u,'restore')?2:1);b.construction.remaining-=amount;b.hp=Math.min(b.maxHp,b.hp+b.maxHp*0.88/b.construction.total*amount);u.state='build';if(b.construction.remaining<=0){b.construction=null;b.hp=b.maxHp;u.order=null;event(s,`${BUILDINGS[b.type].name} completed`,b.owner);}}return;}
 if(b.queue.length){const q=b.queue[0];q.remaining=Math.max(0,q.remaining-DT*(active(s,b,'mobilize')?2:1));if(q.remaining===0){const spot=spawnPoint(s,b,q.unit);if(spot){add(s,b.owner,q.unit,spot.x,spot.y);b.queue.shift();}}}
 if(b.type==='residence')for(const u of s.entities)if(u.owner===b.owner&&u.kind==='unit'&&living(u)&&dist(u,b)<=BUILDINGS.residence.healRadius)u.hp=Math.min(u.maxHp,u.hp+BUILDINGS.residence.heal*s.players[b.owner].modifiers.heal*DT);
 if(BUILDINGS[b.type].damage){const t=nearestEnemy(s,b,BUILDINGS[b.type].range);if(t)attack(s,b,t);}
}
function tickUnit(s,e){
 const d=UNITS[e.type],m=s.players[e.owner].modifiers;e.food=Math.max(0,e.food-d.consumption*m.consumption*DT);
 if(['han_xin','napoleon_bonaparte'].some(id=>[s.players[e.owner].king,s.players[e.owner].general].includes(id))&&!s.entities.some(b=>b.owner===e.owner&&stores(b)&&dist(b,e)<12))e.food=Math.max(0,e.food-d.consumption*0.2*DT);
 if(!e.embarked)resupply(s,e);else{const ship=get(s,e.embarked);if(ship){e.x=ship.x;e.y=ship.y;}return;}
 if(e.food<=0){e.starving=(e.starving||0)+DT;e.morale=Math.max(15,e.morale-0.5*DT);if(e.starving>BALANCE.starveGrace)hurt(s,e,BALANCE.starveDamage*DT,null);}else{e.starving=0;const nearLeader=s.entities.some(u=>u.owner===e.owner&&u.character&&living(u)&&dist(u,e)<7);e.morale=Math.min(Math.min(100,80+m.morale),e.morale+(nearLeader?3:0.5)*DT);}
 if(!living(e))return;if(active(s,e,'consensus')||active(s,e,'restore')){e.hp=Math.min(e.maxHp,e.hp+2*DT);e.morale=Math.min(100,e.morale+8*DT);}
 for(const f of s.effects)if(f.kind==='riverTrap'&&f.owner!==e.owner&&f.until>s.tick&&dist(e,f)<f.radius&&TERRAIN[tile(s,e.x,e.y)]?.water)hurt(s,e,7*DT,{owner:f.owner});
 if(!living(e))return;if(e.pendingAttack){e.state='attack';return;}const previous={x:e.x,y:e.y},o=e.order;e.state='idle';
 if(o?.type==='build'){const b=get(s,o.target);if(!b||!b.construction)e.order=null;else travel(s,e,b,BUILDINGS[b.type].radius+1.25);}
 else if(o?.type==='repair'){const b=get(s,o.target);if(!b||b.hp>=b.maxHp)e.order=null;else if(travel(s,e,b,BUILDINGS[b.type].radius+1.25)){const n=Math.min(b.maxHp-b.hp,6*DT,s.players[e.owner].resources.wood*5);if(n>0){b.hp+=n;s.players[e.owner].resources.wood-=n/5;e.state='build';}}}
 else if(o?.type==='gather')gather(s,e,s.map.resources.find(r=>r.id===o.target));
 else if(o?.type==='load'||o?.type==='unload'){const t=get(s,o.target);if(!t)e.order=null;else transfer(s,e,t,o.type);}
 else if(o?.type==='attack'){const t=get(s,o.target);if(!t)e.order=null;else if(visible(s,e.owner,t)){o.lastX=t.x;o.lastY=t.y;attack(s,e,t);}else if(travel(s,e,{x:o.lastX,y:o.lastY},0.8))e.order=null;}
 else if(o?.type==='move'){if(travel(s,e,o,0.7,true))e.order=null;}
 else if(o?.type==='attackMove'){const t=d.damage?nearestEnemy(s,e,Math.min(d.vision,7)):null;if(t)attack(s,e,t);else if(travel(s,e,o,0.7,true))e.order=null;}
 else if(d.damage>0&&e.type!=='villager'&&e.type!=='king'){const t=nearestEnemy(s,e,o?.type==='hold'||e.type==='general'?d.range:6);if(t)attack(s,e,t);}
 if(e.x!==previous.x||e.y!==previous.y)e.lastMovedTick=s.tick;
}
function navalSortie(s,p,own,army){
 const ai=s.players[p].ai,spawn=s.map.spawns[p],enemySpawn=s.map.spawns[1-p],shore={x:spawn.x,y:39.5},landing={x:enemySpawn.x,y:40.5};
 let n=ai.naval,ship=n&&get(s,n.transport);
 if(n&&!ship){ai.naval=null;ai.nextNaval=s.tick+60*TICK_RATE;n=null;}
 if(!n){
  if((ai.nextNaval||0)>s.tick)return new Set();ship=own.find(e=>e.type==='transport'&&!e.embarked);
  const available=army.filter(e=>!e.embarked&&e.hp>e.maxHp*0.55&&e.food>5);
  if(!ship||available.length<5)return new Set();
  const raiders=available.slice(-3);n=ai.naval={transport:ship.id,raiders:raiders.map(e=>e.id),stage:'muster',began:s.tick};
  for(const [i,e] of raiders.entries())command(s,p,{type:'move',ids:[e.id],x:shore.x+(i-1)*0.5,y:shore.y});
  command(s,p,{type:'move',ids:[ship.id],x:spawn.x,y:40.5});
 }
 const raiders=n.raiders.map(id=>get(s,id)).filter(Boolean),reserved=new Set(n.raiders);
 if(!raiders.length){ai.naval=null;ai.nextNaval=s.tick+60*TICK_RATE;return new Set();}
 if(n.stage==='muster'){
  const loaded=raiders.filter(e=>e.embarked===ship.id),waiting=raiders.find(e=>!e.embarked);
  if(waiting&&(!ship.order||ship.order.type==='move'&&dist(ship,{x:spawn.x,y:40.5})<1)){command(s,p,{type:'load',ids:[ship.id],target:waiting.id});}
  if(loaded.length===raiders.length||(s.tick-n.began>90*TICK_RATE&&loaded.length>0)){
   n.raiders=loaded.map(e=>e.id);n.stage='sail';command(s,p,{type:'move',ids:[ship.id],...landing});
  }else if(s.tick-n.began>120*TICK_RATE){ai.naval=null;ai.nextNaval=s.tick+60*TICK_RATE;return new Set();}
 }else if(n.stage==='sail'){
  if(dist(ship,landing)<1.5){n.stage='unload';command(s,p,{type:'unload',ids:[ship.id],target:ship.id});}
  else if(!ship.order)command(s,p,{type:'move',ids:[ship.id],...landing});
 }else if(n.stage==='unload'){
  if(raiders.every(e=>!e.embarked)){
   n.stage='raid';n.landed=s.tick;ai.navalLandings=(ai.navalLandings||0)+1;
   const known=s.entities.filter(e=>e.owner!==p&&visible(s,p,e)&&['granary','depot','wagon'].includes(e.type)).sort((a,b)=>dist(a,ship)-dist(b,ship));
   const destination=known[0]||{x:enemySpawn.x+(p===0?4:-4),y:enemySpawn.y+5};
   for(const e of raiders)command(s,p,{type:'attackMove',ids:[e.id],x:destination.x,y:destination.y});
  }else if(!ship.order)command(s,p,{type:'unload',ids:[ship.id],target:ship.id});
 }else if(n.stage==='raid'){
  const known=s.entities.filter(e=>e.owner!==p&&visible(s,p,e)&&['granary','depot','wagon'].includes(e.type)).sort((a,b)=>dist(a,ship)-dist(b,ship));
  for(const e of raiders)if(!e.order&&known[0])command(s,p,{type:'attackMove',ids:[e.id],x:known[0].x,y:known[0].y});
  if(s.tick-n.landed>60*TICK_RATE){n.stage='return';command(s,p,{type:'move',ids:[ship.id],x:spawn.x,y:40.5});return new Set();}
 }else if(n.stage==='return'){
  if(dist(ship,{x:spawn.x,y:40.5})<1.5){ai.naval=null;ai.nextNaval=s.tick+20*TICK_RATE;}return new Set();
 }
 return reserved;
}
function ai(s,p){
 const cadence=s.difficulty==='easy'?80:s.difficulty==='hard'?30:45;if(s.tick%cadence)return;
 const own=s.entities.filter(e=>e.owner===p&&e.hp>0),king=own.find(e=>e.type==='king'),general=own.find(e=>e.type==='general'),residence=own.find(e=>e.type==='residence'),home=residence||king;
 if(!home)return;const workers=own.filter(e=>e.type==='villager'),army=own.filter(e=>['infantry','spearman','firearm','cavalry','artillery'].includes(e.type));
 // Use the same command validation and costs as human players; AI has no resource cheats.
 if(king&&!residence){const sign=p===0?1:-1;for(const off of [[0,0],[-3,0],[0,5],[3,5]])if(command(s,p,{type:'build',ids:[king.id],building:'residence',x:king.x+sign*off[0],y:king.y+off[1]}).ok)break;}
 for(const [i,w] of workers.entries())if(!w.order||w.order.type==='gather'){
  const desired=i%3===0?'wood':i%3===1?'food':'iron';const patches=s.map.resources.filter(r=>r.type===desired&&r.amount>0&&s.fog[p].explored[Math.floor(r.y)*s.map.width+Math.floor(r.x)]).sort((a,b)=>dist(w,a)-dist(w,b));if(patches[0]&&w.order?.target!==patches[0].id)command(s,p,{type:'gather',ids:[w.id],target:patches[0].id});
 }
 if(residence&&!residence.construction&&workers.length<12&&residence.queue.length<2)command(s,p,{type:'train',building:residence.id,unit:'villager'});
 const sign=p===0?1:-1,plan=[['cavalryCamp',7,7],['shipyard',0,15],['artilleryWorkshop',-5,-6],['granary',9,2],['depot',13,5],['fort',12,-3]],pending=s.tick>400?plan.find(([type])=>!own.some(e=>e.type===type)):null;
 if(pending){const [type,dx,dy]=pending,ai=s.players[p].ai;let w=get(s,ai.builder);if(!w||!['villager'].includes(w.type)||ai.building!==type){w=workers.find(e=>!e.order||e.order.type==='gather');ai.builder=w?.id;ai.building=type;}
  if(w){const site={x:s.map.spawns[p].x+sign*dx,y:s.map.spawns[p].y+dy};
   if(!s.fog[p].visible[Math.floor(site.y)*s.map.width+Math.floor(site.x)]){if(w.order?.type!=='move')command(s,p,{type:'move',ids:[w.id],...site});}
   else for(const offset of [0,2,-2])if(command(s,p,{type:'build',ids:[w.id],building:type,x:site.x+sign*offset,y:site.y}).ok){ai.builder=null;ai.building=null;break;}
  }
 }
 const navalReserved=navalSortie(s,p,own,army);
 const production=own.filter(b=>b.kind==='building'&&!b.construction&&b.queue.length<2).sort((a,b)=>(a.type==='shipyard'?-1:0)-(b.type==='shipyard'?-1:0));
 for(const b of production){
  let type=null;if(b.type==='barracks'&&army.length<32)type=['infantry','spearman','firearm'][Math.floor(s.tick/cadence)%3];if(b.type==='cavalryCamp'&&army.filter(e=>e.type==='cavalry').length<7)type='cavalry';if(b.type==='artilleryWorkshop'&&army.filter(e=>e.type==='artillery').length<4)type='artillery';if(b.type==='depot'&&own.filter(e=>e.type==='wagon').length<3)type='wagon';if(b.type==='shipyard'){const transportExists=own.some(e=>e.type==='transport')||b.queue.some(q=>q.unit==='transport');if(!transportExists)type='transport';else if(own.filter(e=>e.type==='warship').length<3)type='warship';}
  const reserve=pending?BUILDINGS[pending[0]].cost.wood:0;
  if(type&&(type==='transport'||s.players[p].resources.wood>=(UNITS[type].cost.wood+reserve)))command(s,p,{type:'train',building:b.id,unit:type});
 }
 const visibleEnemies=s.entities.filter(e=>e.owner!==p&&visible(s,p,e));const threat=general&&visibleEnemies.find(e=>combatant(e)&&dist(e,general)<9);
 if(general&&(threat||general.hp<general.maxHp*0.55||general.food<general.foodMax*0.15)){command(s,p,{type:'move',ids:[general.id],x:home.x-sign*2,y:home.y+2});const defenders=army.filter(e=>dist(e,home)<15);if(threat&&defenders.length)command(s,p,{type:'attack',ids:defenders.map(e=>e.id),target:threat.id});}
 else if(general&&!general.order&&army.length>6){command(s,p,{type:'move',ids:[general.id],x:home.x+sign*4,y:home.y+2});}
 if(king&&king.hp<king.maxHp*0.5)command(s,p,{type:'move',ids:[king.id],x:home.x-sign*3,y:home.y+1});
 const enemyGeneral=visibleEnemies.find(e=>e.type==='general'),raid=visibleEnemies.find(e=>['wagon','depot','granary'].includes(e.type)),attackAt=s.difficulty==='easy'?1800:s.difficulty==='hard'?800:1200;
 if(s.tick>attackAt&&army.length>=7&&!threat){const target=enemyGeneral||raid||s.map.spawns[1-p];const attackers=army.filter((e,i)=>i>=2&&!navalReserved.has(e.id)&&!e.embarked);for(const e of attackers)if(!e.order||e.order.type!=='attackMove'&&e.order.type!=='attack')command(s,p,{type:'attackMove',ids:[e.id],x:target.x,y:target.y});}
 if(general&&general.abilityCooldown===0&&(threat||army.some(e=>e.state==='attack')))command(s,p,{type:'ability',ids:[general.id]});if(king&&king.abilityCooldown===0&&s.tick>500)command(s,p,{type:'ability',ids:[king.id]});
 for(const wagon of own.filter(e=>e.type==='wagon'))if(!wagon.order){const node=own.filter(stores).sort((a,b)=>b.cargo.food-a.cargo.food)[0];if(wagon.cargo.food<20&&node?.cargo.food>25)command(s,p,{type:'load',ids:[wagon.id],target:node.id});else if(wagon.cargo.food>=20){const advanced=army.filter(e=>dist(e,home)>8);if(advanced.length){const front=advanced.reduce((a,b)=>dist(b,home)>dist(a,home)?b:a);command(s,p,{type:'move',ids:[wagon.id],x:front.x-sign*2,y:front.y+1});}}}
 for(const ship of own.filter(e=>e.type==='warship'))if(!ship.order){const target=visibleEnemies.find(e=>UNITS[e.type]?.naval)||{x:s.map.spawns[1-p].x,y:42};command(s,p,{type:'attackMove',ids:[ship.id],x:target.x,y:target.y});}
}
export function step(s){
 if(s.winner!==null)return s;s.tick++;updateFog(s);s.effects=s.effects.filter(f=>f.until>s.tick);if(s.aiPlayer!==null)ai(s,s.aiPlayer);
 // Iteration snapshot prevents newly trained units taking an extra update on their birth tick.
 for(const e of [...s.entities]){if(s.winner!==null)break;if(e.hp<=0){cancelAttack(e);continue;}e.cooldown=e.attackReadyTick===undefined?Math.max(0,e.cooldown-DT):Math.max(0,(e.attackReadyTick-s.tick)/TICK_RATE);if(e.abilityCooldown)e.abilityCooldown=Math.max(0,e.abilityCooldown-1);if(e.kind==='building')tickBuilding(s,e);else tickUnit(s,e);
  if(e.kind==='building'&&active(s,e,'inspection'))e.hp=Math.min(e.maxHp,e.hp+DT*3);
 }
 // Current-tick movement/visibility precedes authoritative impact; view calls cannot change this timing.
 updateFog(s);for(const e of s.entities){if(s.winner!==null)break;resolveAttack(s,e);}
 s.entities=s.entities.filter(e=>e.hp>0||s.tick-(e.deadTick??s.tick)<TICK_RATE*4);updateFog(s);economy(s);return s;
}
export function view(s,p){
 if(p!==0&&p!==1)throw new Error('Invalid viewer');updateFog(s);const result={tick:s.tick,map:{id:s.map.id,name:s.map.name,width:s.map.width,height:s.map.height,tiles:[...s.map.tiles],resources:s.map.resources.map(r=>s.fog[p].resources[r.id]).filter(Boolean).map(clone)},players:s.players.map(player=>({id:player.id,name:player.name,king:player.king,general:player.general,resources:player.id===p?clone(player.resources):{wood:0,food:0,iron:0},population:player.id===p?player.population:0,populationCap:BALANCE.populationCap,synergies:player.synergies,stats:player.id===p||s.winner!==null?clone(player.stats):undefined})),entities:[],winner:s.winner,reason:s.reason,events:s.events.filter(e=>e.owner===null||e.owner===p).map(e=>e.text),fog:clone(s.fog[p]),effects:s.effects.filter(f=>f.owner===p||s.fog[p].visible[Math.floor(f.y)*s.map.width+Math.floor(f.x)]).map(clone)};
 for(const e of s.entities){if(e.owner!==p&&!visible(s,p,e))continue;const {path,pathKey,retryPath,order,pendingAttack,gatherEpisode,crowdRoute,crowdGoal,crowdRetry,...publicEntity}=e;const v=clone(publicEntity);const visibleAction=visibleVillagerAction(s,e);if(visibleAction)v.visibleAction=visibleAction;if(e.owner===p)v.order=order?clone(order):null;else{v.queue=[];v.cargo={food:0,wood:0,iron:0,units:[]};delete v.abilityCooldown;delete v.construction;}result.entities.push(v);}
 return result;
}
export function hashState(s){let hash=2166136261;const text=JSON.stringify(s);for(let i=0;i<text.length;i++){hash^=text.charCodeAt(i);hash=Math.imul(hash,16777619);}return (hash>>>0).toString(16).padStart(8,'0');}
