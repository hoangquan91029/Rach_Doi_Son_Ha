export function observeTrain(before,after,requested,errors=[]){
 if(errors.length)return {status:'REJECTED',errors};
 const b=before.queue,a=after.queue;
 // A queue entry decreases remaining; completion can remove only a prefix.
 for(let removed=0;removed<=b.length;removed++){
  const retained=b.slice(removed);
  if(a.length!==retained.length+1)continue;
  if(!retained.every((q,i)=>q.unit===a[i].unit&&q.total===a[i].total&&a[i].remaining<=q.remaining))continue;
  const added=a.at(-1);
  if(added.unit===requested&&added.total>0&&added.remaining>0&&added.remaining<=added.total&&added.remaining>=added.total-3)return {status:'ACCEPTED_QUEUE',removed,added};
 }
 return {status:'PENDING',newRequestedIds:after.units.filter(u=>u.type===requested&&!before.units.some(v=>v.id===u.id)).map(u=>u.id),limitation:'spawn alone cannot bind this command to producer'};
}
