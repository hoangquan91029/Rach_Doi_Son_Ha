import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
const here=new URL('./',import.meta.url),source=resolve(process.env.QA_SIM_PATH||'shared/sim.js'),gate=process.env.QA_GATE||'prepare',run=process.env.QA_RUN_ID||'prepared';
if(!/^[a-zA-Z0-9_-]+$/.test(run))throw Error('Simple unique QA_RUN_ID required');
const output=new URL(run+'/',here);await mkdir(output,{recursive:false});
const pins=JSON.parse(await readFile(new URL('source-pins.json',here)));for(const pin of pins.filter(p=>p.path.startsWith('tests/'))){const b=await readFile(pin.path);if(createHash('sha256').update(b).digest('hex')!==pin.sha256)throw Error('Frozen test source drift '+pin.path);}
const files=[];for(const name of ['sim.test.js','navigation.test.js']){let s=await readFile(new URL('frozen-'+name,here),'utf8');s=s.replace(/from '(\.\.\/shared\/[^']+)'/g,(_,p)=>`from '${pathToFileURL(p.endsWith('/sim.js')?source:resolve('tests',p)).href}'`);const f=new URL(name,output);await writeFile(f,s);files.push(f.pathname);}
const patterns={ai:'AI completes normal combat victory',naval:'AI trains, embarks, lands naval raiders',navigation:null,combat:'windup|impact|recovery|attack|General combat death',all:null};
const receipt={gate,source,sourceSHA256:createHash('sha256').update(await readFile(source)).digest('hex'),method:'Frozen exact tests; import URLs only changed. No assertions/seeds/economy/timecaps edited.',preparedFiles:files};
if(gate!=='prepare'){if(!Object.hasOwn(patterns,gate))throw Error('Unknown gate');const args=['--test','--test-concurrency=1'];if(patterns[gate])args.push('--test-name-pattern='+patterns[gate]);args.push(...(gate==='navigation'?[files[1]]:gate==='all'?files:[files[0]]));receipt.command=[process.execPath,...args];const result=spawnSync(process.execPath,args,{encoding:'utf8'});await writeFile(new URL('console.txt',output),(result.stdout||'')+(result.stderr||''));receipt.exitCode=result.status;receipt.signal=result.signal;if(result.status!==0)process.exitCode=1;}
await writeFile(new URL('receipt.json',output),JSON.stringify(receipt,null,2)+'\n');console.log(JSON.stringify(receipt));
