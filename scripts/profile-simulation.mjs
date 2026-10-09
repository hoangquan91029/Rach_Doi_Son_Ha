import inspector from 'node:inspector';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {performance} from 'node:perf_hooks';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {createMatch,step} from '../shared/sim.js';
import {TICK_RATE} from '../shared/data.js';
import {snapshotView} from '../server/index.js';
import {statistics} from './benchmark-simulation.mjs';
const root=path.dirname(path.dirname(fileURLToPath(import.meta.url))),us=()=>Number(process.hrtime.bigint()/1000n);
const counts=s=>({tick:s.tick,winner:s.winner,livingUnits:s.entities.filter(e=>e.hp>0&&e.kind==='unit').length,unitsByOwner:[0,1].map(owner=>s.entities.filter(e=>e.owner===owner&&e.hp>0&&e.kind==='unit').length),entities:s.entities.length});
export function summarizeProfile(profile,windows){
 const nodes=new Map(profile.nodes.map(n=>[n.id,n])),parents=new Map();for(const n of profile.nodes)for(const child of n.children||[])parents.set(child,n.id);
 const key=n=>JSON.stringify([n.callFrame.functionName,n.callFrame.url,n.callFrame.lineNumber,n.callFrame.columnNumber]),functions=new Map(),phases={};let stamp=profile.startTime,index=0;
 const functionRow=n=>{const k=key(n);if(!functions.has(k))functions.set(k,{functionName:n.callFrame.functionName||'(anonymous)',url:n.callFrame.url,line:n.callFrame.lineNumber<0?null:n.callFrame.lineNumber+1,column:n.callFrame.columnNumber<0?null:n.callFrame.columnNumber+1,selfSamples:0,inclusiveSamples:0,selfByPhase:{},inclusiveByPhase:{}});return functions.get(k);};
 for(let i=0;i<(profile.samples||[]).length;i++){
  stamp+=profile.timeDeltas?.[i]||0;while(index<windows.length&&windows[index].endUs<stamp)index++;const w=windows[index],phase=w&&stamp>=w.startUs&&stamp<=w.endUs?w.phase:'inspector-or-other';phases[phase]=(phases[phase]||0)+1;
  const node=nodes.get(profile.samples[i]);if(!node)continue;const self=functionRow(node);self.selfSamples++;self.selfByPhase[phase]=(self.selfByPhase[phase]||0)+1;
  const seen=new Set();for(let current=node;current;current=nodes.get(parents.get(current.id))){const k=key(current);if(seen.has(k))continue;seen.add(k);const r=functionRow(current);r.inclusiveSamples++;r.inclusiveByPhase[phase]=(r.inclusiveByPhase[phase]||0)+1;}
 }
 const total=profile.samples?.length||0,rows=[...functions.values()].map(r=>({...r,selfPercent:total?100*r.selfSamples/total:0,inclusivePercent:total?100*r.inclusiveSamples/total:0}));
 return {totalSamples:total,profileDurationUs:profile.endTime-profile.startTime,samplePhases:phases,gcSamples:rows.filter(r=>r.functionName==='(garbage collector)').reduce((n,r)=>n+r.selfSamples,0),inclusiveDefinition:'Each function is counted once per sampled stack, deduplicating recursive frames; inclusive totals overlap.',topSelf:rows.sort((a,b)=>b.selfSamples-a.selfSamples).slice(0,30),topInclusive:[...rows].sort((a,b)=>b.inclusiveSamples-a.inclusiveSamples).slice(0,30),allFunctions:rows};
}
async function main(){
 let ticks=200,sampleUs=1000,outDir=path.join(root,'docs/qa/performance-profile-176');const integer=(v,min,max)=>{if(!/^\d+$/.test(v||''))throw Error('Expected bounded integer');const n=Number(v);if(n<min||n>max)throw Error(`Expected ${min}..${max}`);return n;};
 for(let i=2;i<process.argv.length;i++){const flag=process.argv[i],value=process.argv[++i];if(flag==='--ticks')ticks=integer(value,100,200);else if(flag==='--sample-us')sampleUs=integer(value,100,1000);else if(flag==='--out-dir'&&value)outDir=path.resolve(value);else throw Error('Unknown/missing option '+flag);}
 await mkdir(outDir,{recursive:true});const files=['shared/sim.js','shared/data.js','shared/visible-action.js','server/index.js','scripts/benchmark-simulation.mjs','scripts/profile-simulation.mjs'],hashes=async()=>Object.fromEntries(await Promise.all(files.map(async f=>[f,createHash('sha256').update(await readFile(path.join(root,f))).digest('hex')]))),sourceHashes=await hashes();
 const started=performance.now(),deadline=started+90000,check=()=>{if(performance.now()>deadline)throw Error('90-second finite profile wall limit exceeded');},worlds=Array.from({length:5},(_,i)=>createMatch({mapId:'delta',seed:171+i,aiPlayer:1,difficulty:'normal'}));
 const initial=worlds.map(counts);for(const s of worlds)for(let tick=0;tick<90*TICK_RATE&&s.winner===null;tick++){step(s);if(tick%20===0)check();}
 const evolved=worlds.map(counts);for(let tick=0;tick<20;tick++){for(const s of worlds)if(s.winner===null)step(s);if(tick%4===0)for(const s of worlds)for(const player of [0,1])JSON.stringify({type:'state',state:snapshotView(s,player),paused:false});check();}
 const checkpoint=worlds.map(counts),preparationMs=performance.now()-started,session=new inspector.Session();session.connect();const post=(method,params={})=>new Promise((resolve,reject)=>session.post(method,params,(error,result)=>error?reject(error):resolve(result)));
 const windows=[],epochs=[];let profile;
 try{
  await post('Profiler.enable');await post('Profiler.setSamplingInterval',{interval:sampleUs});await post('Profiler.start');
  for(let sample=0;sample<ticks;sample++){
   check();const active=worlds.filter(s=>s.winner===null);if(!active.length)break;const batch=us(),worldTimes=[];
   for(const s of active){const tick=s.tick+1,startUs=us();step(s);const endUs=us();windows.push({phase:tick%45===0?'step-periodic-ai':'step-normal',startUs,endUs,tick});worldTimes.push((endUs-startUs)/1000);}
   const stepMs=(us()-batch)/1000;let snapshotMs=0;
   if(sample%4===0){const startUs=us();for(const s of worlds)for(const player of [0,1])JSON.stringify({type:'state',state:snapshotView(s,player),paused:false});const endUs=us();windows.push({phase:'snapshot-view-json',startUs,endUs,tick:worlds[0].tick});snapshotMs=(endUs-startUs)/1000;}
   epochs.push({sample,tick:worlds[0].tick,periodicAI:worlds[0].tick%45===0,activeWorlds:active.length,stepMs,snapshotMs,worldTimesMs:worldTimes});
  }
  ({profile}=await post('Profiler.stop'));await post('Profiler.disable');
 }finally{session.disconnect();}
 await writeFile(path.join(outDir,'raw.cpuprofile'),JSON.stringify(profile));const sourceHashesAfter=await hashes(),summary=summarizeProfile(profile,windows),report={kind:'mature-shared-simulation-cpu-profile',date:new Date().toISOString(),config:{map:'delta',worlds:5,seed:171,aiPlayer:1,difficulty:'normal',evolveSeconds:90,warmupTicks:20,measurementTicks:ticks,samplingIntervalUs:sampleUs,snapshotEveryTicks:4,wallLimitSeconds:90},gitCommit:execFileSync('git',['rev-parse','HEAD'],{cwd:root,encoding:'utf8'}).trim(),sourceHashes,sourceHashesAfter,sourcesUnchanged:JSON.stringify(sourceHashes)===JSON.stringify(sourceHashesAfter),hardware:{cpu:os.cpus()[0]?.model,logicalCpus:os.cpus().length,totalMemoryBytes:os.totalmem(),platform:os.platform(),release:os.release(),loadAverageAfter:os.loadavg(),exclusiveCpu:false},runtime:{node:process.version,v8:process.versions.v8},initial,evolved,checkpoint,final:worlds.map(counts),preparationMs,elapsedMs:performance.now()-started,measuredEpochs:epochs.length,stepMs:statistics(epochs.map(e=>e.stepMs)),periodicAIStepMs:statistics(epochs.filter(e=>e.periodicAI).map(e=>e.stepMs)),normalStepMs:statistics(epochs.filter(e=>!e.periodicAI).map(e=>e.stepMs)),snapshotEpochMs:statistics(epochs.filter((e,i)=>i%4===0).map(e=>e.snapshotMs)),summary,limitations:['Profiler is OFF during all90-second preparation and warmup.','Nonexclusive CPU, synchronized world phases, sampler overhead and short finite workload; not online headroom failure/PASS.','Only built-in player1 AI; online human-vs-human has no AI.','No minted resources/units, external gameplay commands, service/network/compression/send queues, browser, build or optimization.','step-periodic-ai labels epochs due for normal AI cadence45; they include the whole step, not only ai(). Inclusive stack samples identify actual ai() ancestry.']};
 await writeFile(path.join(outDir,'epochs.json'),JSON.stringify({windows,epochs},null,2)+'\n');await writeFile(path.join(outDir,'profile.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({preparationMs,measuredEpochs:epochs.length,totalSamples:summary.totalSamples,samplePhases:summary.samplePhases,topSelf:summary.topSelf.slice(0,8),topInclusive:summary.topInclusive.slice(0,8)},null,2));
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url))main().catch(e=>{console.error(e.stack);process.exitCode=1;});
