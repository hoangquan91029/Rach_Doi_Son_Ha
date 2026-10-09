import {pathToFileURL} from 'node:url';
import {resolve} from 'node:path';
import {readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {spawn} from 'node:child_process';
import assert from 'node:assert/strict';
assert.equal(process.env.QA_ROOT_EXECUTION_APPROVED,'086','Root execution message required after085PASS');
const stage=resolve(process.env.QA_STAGE),dist=resolve(process.env.QA_DIST||stage+'/dist'),bundle=resolve(process.env.QA_BUNDLE_PATH),expected=process.env.QA_BUNDLE_SHA;
const bytes=await readFile(bundle);assert.equal(createHash('sha256').update(bytes).digest('hex'),expected);
const {createGameServer}=await import(pathToFileURL(stage+'/server/index.js'));
const receipt={stage,dist,bundle,expected,started:new Date().toISOString(),method:'085 exact isolatedserver+bundle,port0; no productionservice'};let game;
try{game=await createGameServer({port:0,host:'127.0.0.1',distDir:dist});receipt.url=`http://127.0.0.1:${game.server.address().port}`;console.log('OWNED086',receipt.url);receipt.exitCode=await new Promise((resolve,reject)=>{const child=spawn(process.execPath,['docs/qa/crowd-browser-086/harness-prepared.mjs'],{stdio:'inherit',env:{...process.env,GAME_URL:receipt.url,QA_OUTPUT:'docs/qa/crowd-browser-086/actual',QA_LIMIT_MS:'720000'}});child.on('error',reject);child.on('exit',(code,signal)=>{receipt.signal=signal;resolve(code);});});}
catch(error){receipt.error=error.stack;process.exitCode=1;}
finally{if(game){receipt.roomsBeforeClose=game.rooms.size;await game.close();receipt.roomsAfterClose=game.rooms.size;receipt.listening=game.server.listening;}receipt.finished=new Date().toISOString();await writeFile('docs/qa/crowd-browser-086/owned-server-receipt.json',JSON.stringify(receipt,null,2));if(receipt.exitCode!==0)process.exitCode=1;console.log('OWNED086_TERMINAL',JSON.stringify(receipt));}
