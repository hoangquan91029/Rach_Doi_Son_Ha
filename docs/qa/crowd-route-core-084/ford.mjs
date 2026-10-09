import {createMatch,step,command,CROWD_RADII} from './sim-draft.js';
import {UNITS,TICK_RATE} from '../../../shared/data.js';
import {writeFile,readFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
const out=new URL('./',import.meta.url),results=[];
const distance=(a,b)=>Math.hypot(a.x-b.x,a.y-b.y);
function arena(){const s=createMatch({seed:47}),sample=s.entities.find(e=>e.type==='infantry');s.entities=[];s.map.tiles.fill('plain');s.map.resources=[];s.aiPlayer=null;return {s,sample};}
function unit(s,sample,x,y,owner=0){const e=structuredClone(sample);Object.assign(e,{id:s.nextId++,owner,x,y,order:{type:'hold'},path:[],pendingAttack:undefined});s.entities.push(e);return e;}
let state,caseName;
try{
 caseName='opposing-ford-900';const {s,sample}=arena();state=s;for(let y=0;y<48;y++)s.map.tiles[y*64+12]='river';s.map.tiles[10*64+12]='ford';const groups=[[],[]];for(let p=0;p<2;p++)for(let i=0;i<8;i++)groups[p].push(unit(s,sample,p?16.5+(i%2)*.75:8.5-(i%2)*.75,9.5+Math.floor(i/2)*.75,p));for(let p=0;p<2;p++)assert.ok(command(s,p,{type:'attackMove',ids:groups[p].map(e=>e.id),x:p?8.5:16.5,y:10.5}).ok);const replay=[];let hits=0;
 for(let i=0;i<900;i++){const prior=new Map(s.entities.map(e=>[e.id,{x:e.x,y:e.y,pending:e.pendingAttack}]));step(s);const living=s.entities.filter(e=>e.hp>0);for(let j=0;j<living.length;j++){const a=living[j],old=prior.get(a.id);assert.ok(distance(a,old)<=UNITS.infantry.speed/TICK_RATE*1.01+1e-8,'speed bound');if(old.pending&&a.pendingAttack)assert.ok(distance(a,old)<1e-8,'pending windup anchor');assert.notEqual(s.map.tiles[Math.floor(a.y)*64+Math.floor(a.x)],'river');for(const b of living.slice(j+1))assert.ok(distance(a,b)>=2*CROWD_RADII.land-1e-8,'physical clearance');}hits=Math.max(hits,s.entities.filter(e=>e.lastAttack).length);if(i%30===0)replay.push({tick:s.tick,entities:s.entities.map(e=>({id:e.id,x:e.x,y:e.y,hp:e.hp,order:e.order,pending:e.pendingAttack})),stats:structuredClone(s.crowdStats)});}
 await writeFile(new URL('ford-replay.json',out),JSON.stringify(replay));assert.ok(hits>=4,'several soldiers must complete impacts in900ticks');assert.ok(s.entities.some(e=>e.hp<e.maxHp)||s.entities.length<16,'combat progress');results.push({caseName,passed:true,hits,tick:s.tick});
 // Retained fixtures are uncalled if the first algorithm gate fails.
 await writeFile(new URL('receipt.json',out),JSON.stringify({status:'FORD_PASS_REMAINING_PREPARATION',results},null,2));
}catch(error){await writeFile(new URL('failure.json',out),JSON.stringify({caseName,results,error:error.stack,state},null,2));console.log(error.stack);process.exitCode=1;}
const bytes=await readFile(new URL('./sim-draft.js',import.meta.url));await writeFile(new URL('source-pin.json',out),JSON.stringify({source:'docs/qa/crowd-admission-core-073/sim-draft.js',sha256:createHash('sha256').update(bytes).digest('hex')},null,2));
