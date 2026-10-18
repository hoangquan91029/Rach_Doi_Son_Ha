import fs from 'node:fs';import {EventEmitter} from 'node:events';import {launchOwnedBrowser} from '../../../scripts/qa/browser-custody510.mjs';
const child=new EventEmitter();Object.assign(child,{pid:123,exitCode:null,signalCode:null,stderr:new EventEmitter()});
let closes=0,kills=0;const server=new EventEmitter();Object.assign(server,{process:()=>child,wsEndpoint:()=>'',close:async()=>{closes++;throw Error('close failure');},kill:async()=>{kills++;throw Error('kill failure');}});
const browser=new EventEmitter();Object.assign(browser,{contexts:()=>[],version:()=>'',isConnected:()=>true});
const owned=await launchOwnedBrowser({browserType:{launchServer:async()=>server,connect:async()=>browser},directory:'docs/qa/browser-custody-510-review/repro-observer'});
let error;try{await owned.close();}catch(e){error=e.message;}await owned.close();
console.log(JSON.stringify({error,closes,kills,connected:browser.isConnected(),exitListeners:child.listenerCount('exit'),serverCloseListeners:server.listenerCount('close'),status:owned.custody.status},null,2));
