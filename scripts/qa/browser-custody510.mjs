import fs from 'node:fs';
import path from 'node:path';

// Public Playwright launchServer/process/connect APIs. Observe only handles launched here.
// Startup stderr before launchServer resolves is unavailable; no private API access.
export function createBrowserCustody({directory, maxEvents=256, maxStderrBytes=262144}) {
  if (!Number.isSafeInteger(maxEvents) || maxEvents<4 || !Number.isSafeInteger(maxStderrBytes) || maxStderrBytes<1) throw new Error('Invalid finite log limits');
  fs.mkdirSync(directory,{recursive:true});
  const eventPath=path.join(directory,'lifecycle.jsonl'), stderrPath=path.join(directory,'browser-stderr.bin'), statusPath=path.join(directory,'status.json');
  // Exclusive creation prevents accidental overwrite/reuse of a consumed observation.
  const eventFD=fs.openSync(eventPath,'wx');let stderrFD;
  try{stderrFD=fs.openSync(stderrPath,'wx');}catch(error){fs.closeSync(eventFD);throw error;}
  const started=performance.now(), listeners=[], contexts=new WeakSet(), pages=new WeakSet();
  const status={schema:'rds-browser-custody/v1',startedUTC:new Date().toISOString(),pid:null,eventCount:0,droppedEvents:0,stderrBytes:0,droppedStderrBytes:0,processExit:null,processClose:null,disconnected:false,cleanup:[],limitation:'stderr/process events observed only after launchServer resolves; markers record intent, not proven cause'};
  let finished=false;
  const durable=(fd,data)=>{fs.writeSync(fd,data);fs.fsyncSync(fd);};
  const save=()=>{const fd=fs.openSync(statusPath,'w');try{durable(fd,JSON.stringify(status,null,2)+'\n');}finally{fs.closeSync(fd);}};
  function event(type,data={}) {
    if(finished)return;
    const row={type,atUTC:new Date().toISOString(),elapsedMs:performance.now()-started,cleanupStarted:status.cleanup.length>0,...data};
    if(status.eventCount<maxEvents){durable(eventFD,JSON.stringify(row)+'\n');status.eventCount++;}else status.droppedEvents++;
    save();
  }
  function listen(emitter,type,fn){emitter.on(type,fn);listeners.push(()=>emitter.off(type,fn));}
  function attachProcess(child) {
    status.pid=child.pid??null;
    event('process-attached',{pid:status.pid,initialExitCode:child.exitCode??null,initialSignalCode:child.signalCode??null});
    if(child.exitCode!==null&&child.exitCode!==undefined || child.signalCode){status.processExit={code:child.exitCode??null,signal:child.signalCode??null,observed:'already-exited-at-attachment'};save();}
    if(child.stderr)listen(child.stderr,'data',chunk=>{if(finished)return;const b=Buffer.isBuffer(chunk)?chunk:Buffer.from(chunk),available=Math.max(0,maxStderrBytes-status.stderrBytes),kept=b.subarray(0,available);if(kept.length){durable(stderrFD,kept);status.stderrBytes+=kept.length;}status.droppedStderrBytes+=b.length-kept.length;save();});
    else event('stderr-unavailable');
    listen(child,'exit',(code,signal)=>{status.processExit={code,signal,atUTC:new Date().toISOString(),elapsedMs:performance.now()-started};event('process-exit',status.processExit);});
    listen(child,'close',(code,signal)=>{status.processClose={code,signal,atUTC:new Date().toISOString(),elapsedMs:performance.now()-started};event('process-close',status.processClose);});
    listen(child,'error',error=>event('process-error',{message:error.message.slice(0,2048)}));
  }
  function observePage(page) {
    if(pages.has(page))return;pages.add(page);
    event('page-observed');listen(page,'crash',()=>event('page-crash'));listen(page,'close',()=>event('page-close'));
  }
  function observeContext(context) {
    if(contexts.has(context))return;contexts.add(context);
    event('context-observed');listen(context,'close',()=>event('context-close'));listen(context,'page',observePage);
    for(const p of context.pages())observePage(p);
  }
  function observeBrowser(browser) {listen(browser,'disconnected',()=>{status.disconnected=true;event('browser-disconnected');});for(const c of browser.contexts())observeContext(c);}
  function cleanupIntent(scope) {if(status.cleanup.length>=32)throw new Error('Cleanup intent cap reached');const marker={scope:String(scope).slice(0,128),atUTC:new Date().toISOString(),elapsedMs:performance.now()-started};status.cleanup.push(marker);event('cleanup-intent',marker);}
  function finish() {if(finished)return;event('observer-finished');finished=true;for(const off of listeners)off();fs.closeSync(eventFD);fs.closeSync(stderrFD);}
  return {attachProcess,observeBrowser,observeContext,observePage,cleanupIntent,event,finish,status,listen};
}

const bounded=async(promise,ms)=>{let timer;try{return await Promise.race([promise,new Promise((_,reject)=>{timer=setTimeout(()=>reject(new Error('Owned browser close timeout')),ms);})]);}finally{clearTimeout(timer);}};
export async function launchOwnedBrowser({browserType,directory,launchOptions={},closeTimeoutMs=10000}) {
  const custody=createBrowserCustody({directory});let server,browser,closed=false,closing;
  const verifiedClosed=()=>{const p=server?.process();return !!p && (p.exitCode!==null&&p.exitCode!==undefined || !!p.signalCode) && (!browser || !browser.isConnected());};
  const owned={get browser(){return browser;},get server(){return server;},custody,
    async newContext(options){const c=await browser.newContext(options);custody.observeContext(c);return c;},
    close(){
      if(closed)return Promise.resolve();if(closing)return closing;
      closing=(async()=>{
        custody.cleanupIntent('owned-browser-server-close');
        try{await bounded(server.close(),closeTimeoutMs);}catch(error){custody.event('close-failed',{message:error.message});custody.cleanupIntent('owned-browser-server-kill');try{await bounded(server.kill(),closeTimeoutMs);}catch(killError){custody.event('kill-failed',{message:killError.message});if(!verifiedClosed()){killError.ownedBrowser=owned;throw killError;}}}
        if(!verifiedClosed()){const error=new Error('Owned process closure remains unresolved');error.ownedBrowser=owned;throw error;}
        closed=true;custody.event('cleanup-finished',{browserConnected:browser?.isConnected()??false,processExitCode:server.process().exitCode,processSignalCode:server.process().signalCode});custody.finish();
      })().finally(()=>{closing=null;});return closing;
    }
  };
  try {
    custody.event('launch-start');server=await browserType.launchServer(launchOptions);
    custody.attachProcess(server.process());custody.listen(server,'close',()=>custody.event('browser-server-close'));
    browser=await browserType.connect(server.wsEndpoint());custody.observeBrowser(browser);custody.event('browser-connected',{version:browser.version()});
  } catch(error) {
    custody.event('launch-or-connect-failed',{message:error.message.slice(0,2048)});
    if(server){try{await owned.close();}catch(cleanupError){error.ownedBrowser=owned;error.cleanupError=cleanupError;custody.event('cleanup-unresolved',{message:cleanupError.message});}}
    else custody.finish();
    throw error;
  }
  return owned;
}
