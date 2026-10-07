/** Deadline covers fetch body, hash and decode; late decoded bitmaps are disposed. */
export function withLoadingDeadline(action,{timeoutMs=30000,label='Resource'}={}) {
 const controller=new AbortController();let expired=false,timer;
 const operation=Promise.resolve().then(()=>action(controller.signal)).then(value=>{if(expired)value?.close?.();return value;});
 const deadline=new Promise((_,reject)=>{timer=setTimeout(()=>{expired=true;controller.abort();reject(Error(`${label} loading timed out`));},Math.max(1,timeoutMs));});
 return Promise.race([operation,deadline]).finally(()=>clearTimeout(timer));
}
