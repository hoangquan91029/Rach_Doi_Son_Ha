import {TICK_RATE} from '../../shared/data.js';
export function observeTrain(before,after,requested,errors=[]){
 if(errors.length)return {status:'REJECTED',errors};
 const b=before.queue,a=after.queue;
 // CPU training advances at DT or twice DT under mobilize (shared/sim.js303).
 // Missing ability data forces a conservative maximum; no elapsed evidence means no binding.
 if(!Number.isSafeInteger(before.tick)||!Number.isSafeInteger(after.tick)||after.tick<=before.tick)return {status:'PENDING',reason:'no positive authoritative tick interval'};
 const budget=(after.tick-before.tick)/TICK_RATE*2,epsilon=1e-7;
 for(let removed=0;removed<=b.length;removed++){
  if(b.slice(0,removed).reduce((n,q)=>n+q.remaining,0)>budget+epsilon)continue;
  const retained=b.slice(removed);
  if(a.length!==retained.length+1)continue;
  if(!retained.every((q,i)=>q.unit===a[i].unit&&q.total===a[i].total&&a[i].remaining<=q.remaining+epsilon&&q.remaining-a[i].remaining<=budget+epsilon))continue;
  const added=a.at(-1);
  if(added.unit===requested&&added.total>0&&added.remaining>0&&added.remaining<=added.total+epsilon&&added.remaining>=added.total-budget-epsilon)return {status:'ACCEPTED_QUEUE',removed,added,tickBudgetSeconds:budget};
 }
 return {status:'PENDING',newRequestedIds:after.units.filter(u=>u.type===requested&&!before.units.some(v=>v.id===u.id)).map(u=>u.id),limitation:'spawn alone cannot bind this command to producer'};
}
