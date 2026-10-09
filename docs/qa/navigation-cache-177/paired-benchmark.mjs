import {performance} from 'node:perf_hooks';
import os from 'node:os';
import {mkdtemp,cp,writeFile,rm,readFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {pathToFileURL} from 'node:url';
import * as candidate from '../../../shared/sim.js';
import {statistics} from '../../../scripts/benchmark-simulation.mjs';
const dir=new URL('./',import.meta.url),tmp=await mkdtemp(os.tmpdir()+'/navigation177-pair-');
await cp(new URL('./baseline/shared/',dir),tmp+'/shared',{recursive:true});await writeFile(tmp+'/package.json','{"type":"module"}');
const baseline=await import(pathToFileURL(tmp+'/shared/sim.js'));
const config={mapId:'delta',worlds:5,seed:171,evolveTicks:1800,warmupTicks:20,measureTicks:100,snapshotEvery:4};
const counts=s=>({tick:s.tick,winner:s.winner,livingUnits:s.entities.filter(e=>e.hp>0&&e.kind==='unit').length,unitsByOwner:[0,1].map(o=>s.entities.filter(e=>e.hp>0&&e.kind==='unit'&&e.owner===o).length)});
const snapshot=(api,s,p)=>{const v=api.view(s,p),{id,width,height,resources}=v.map;v.map={id,width,height,resources};return JSON.stringify({type:'state',state:v,paused:false});};
const start=performance.now(),bounded=()=>{if(performance.now()-start>150000)throw Error('150s finite bound exceeded');};
const run=(api,label)=>{console.error('Preparing '+label);const worlds=Array.from({length:5},(_,i)=>api.createMatch({mapId:'delta',seed:171+i,aiPlayer:1,difficulty:'normal'}));
for(const s of worlds)for(let t=0;t<1800;t++){api.step(s);if(t%100===0)bounded();}
for(let t=0;t<20;t++){worlds.forEach(s=>api.step(s));if(t%4===0)worlds.forEach(s=>[0,1].forEach(p=>snapshot(api,s,p)));}
const checkpoint=worlds.map(counts),checkpointHashes=worlds.map(api.hashState),stepMs=[],snapshotMs=[],bytes=[],hashes=[];
for(let t=0;t<100;t++){bounded();if(worlds.some(s=>s.winner!==null))throw Error('Winner would dilute workload');let now=performance.now();worlds.forEach(s=>api.step(s));stepMs.push(performance.now()-now);if(t%4===0){now=performance.now();let n=0;worlds.forEach(s=>[0,1].forEach(p=>{n+=Buffer.byteLength(snapshot(api,s,p));}));snapshotMs.push(performance.now()-now);bytes.push(n);}hashes.push(worlds.map(api.hashState));}
return {label,checkpoint,checkpointHashes,final:worlds.map(counts),stepCohortMs:statistics(stepMs),snapshotCohortMs:statistics(snapshotMs),snapshotBytes:statistics(bytes),hashes};};
try{const before=os.loadavg(),a=run(baseline,'baseline176'),b=run(candidate,'candidate177');if(JSON.stringify(a.hashes)!==JSON.stringify(b.hashes)||JSON.stringify(a.checkpointHashes)!==JSON.stringify(b.checkpointHashes))throw Error('Paired state mismatch');delete a.hashes;delete b.hashes;
const files=['shared/sim.js','shared/data.js','shared/visible-action.js','server/index.js','docs/qa/navigation-cache-177/baseline/shared/sim.js','docs/qa/navigation-cache-177/paired-benchmark.mjs'];const sources={};for(const p of files)sources[p]=createHash('sha256').update(await readFile(new URL('../../../'+p,dir))).digest('hex');
await writeFile(new URL('paired-results.json',dir),JSON.stringify({date:new Date().toISOString(),config,sources,runtime:{node:process.version,v8:process.versions.v8},hardware:{cpu:os.cpus()[0].model,logicalCpus:os.cpus().length,loadAverageBefore:before,loadAverageAfter:os.loadavg()},environment:'Nonexclusive CPU: concurrent project workers/build tasks; sequential baseline then candidate order may bias timing.',equivalence:'All checkpoint and 100 measurement tick full state hashes equal across5 worlds.',rows:[a,b],p95Ratio:b.stepCohortMs.p95/a.stepCohortMs.p95,elapsedMs:performance.now()-start,limitations:['Diagnostic unprofiled offline AI simulation only; no network/send queues/browser/online headroom verdict.','Natural growth only; no external commands, minted armies/resources or balance changes.','Short finite timing sample, GC/scheduling/order noise apply.']},null,2)+'\n');}finally{await rm(tmp,{recursive:true,force:true});}
