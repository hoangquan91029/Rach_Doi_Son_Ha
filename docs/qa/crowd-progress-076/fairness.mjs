import {createMatch,step,command} from '../crowd-admission-core-073/sim-draft.js';
import {writeFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
const s=createMatch({seed:47}),sample=structuredClone(s.entities.find(e=>e.type==='infantry'));s.entities=[];s.map.tiles.fill('plain');s.map.resources=[];s.aiPlayer=null;
function unit(x,y){const e=structuredClone(sample);Object.assign(e,{id:s.nextId++,x,y,order:{type:'hold'},path:[],pendingAttack:undefined});s.entities.push(e);return e;}
const movers=[];for(let i=0;i<10;i++)movers.push(unit(5.5+(i%2)*25,3.5+Math.floor(i/2)*9));for(const e of movers)for(let i=0;i<8;i++){const angle=i*Math.PI/4;unit(e.x+.61*Math.cos(angle),e.y+.61*Math.sin(angle));}for(const e of movers)assert.ok(command(s,0,{type:'move',ids:[e.id],x:e.x+3.7,y:e.y}).ok);
const counts=Object.fromEntries(movers.map(e=>[e.id,0])),replay=[];
for(let i=0;i<200;i++){const due=movers.filter(e=>(e.crowdRetry??0)<=s.tick+1);step(s);for(const e of due)if(s.crowdStats.eligible.includes(e.id)&&e.crowdRetry===s.tick+10)counts[e.id]++;if(i%10===0)replay.push({tick:s.tick,eligible:s.crowdStats.eligible,plans:s.crowdStats.plans,requesters:movers.map(e=>({id:e.id,x:e.x,y:e.y,retry:e.crowdRetry,routeLength:e.crowdRoute?.length,attempts:counts[e.id]}))});}
const result={case:'static10requester-fairness-200',counts,replay,state:s};await writeFile('docs/qa/crowd-progress-076/fairness-receipt.json',JSON.stringify(result,null,2));assert.ok(Object.values(counts).every(n=>n>0),'Every persistently blocked requester must receive at least one actual planner admission across200ticks');console.log('FAIRNESS_PASS');
