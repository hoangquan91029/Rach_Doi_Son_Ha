import {createMatch,step,hashState} from '../shared/sim.js';
import {performance} from 'node:perf_hooks';
import {writeFile,mkdir} from 'node:fs/promises';
const rows=[];
for(const n of [20,50,100,200,500]) {
 const state=createMatch({mapId:'delta',seed:17,aiPlayer:null});
 const template=state.entities.find(e=>e.type==='infantry')||state.entities.find(e=>e.type==='spearman');
 if(!template) throw Error('No combat unit template available');
 let id=Math.max(...state.entities.map(e=>e.id))+1;
 while(state.entities.filter(e=>e.kind==='unit').length<n){let copy=structuredClone(template);Object.assign(copy,{id:id++,owner:id%2,x:8+(id%8),y:8+(Math.floor(id/8)%10)});state.entities.push(copy);}
 const times=[];
 for(let tick=0;tick<400;tick++){const t=performance.now();step(state);times.push(performance.now()-t);}
 times.sort((a,b)=>a-b);rows.push({units:n,meanTickMs:times.reduce((a,b)=>a+b,0)/times.length,p95TickMs:times[Math.floor(times.length*.95)],maxTickMs:times.at(-1),finalHash:hashState(state)});
}
await mkdir('artifacts',{recursive:true});await writeFile('artifacts/benchmark.json',JSON.stringify({date:'2026-10-07',environment:'Node v24 Linux; simulation only, not browser rendering performance',rows},null,2));console.log(JSON.stringify(rows,null,2));
