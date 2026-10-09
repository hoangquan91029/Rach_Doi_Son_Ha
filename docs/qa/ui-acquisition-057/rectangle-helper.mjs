export async function selectUniqueUnitRectangle(p,id){
 const plan=await p.evaluate(id=>{const s=window.rtsDiagnostics.snapshot(),e=s.displayedState?.entities.find(e=>e.id===id);if(!e||e.owner!==s.localPlayer||e.kind!=='unit'||e.hp<=0||e.embarked)return {eligible:false,id,tick:s.tick};const point=window.rtsDiagnostics.point(e.x,e.y),bounds={x1:point.x-4,y1:point.y-4,x2:point.x+4,y2:point.y+4};const inside=s.displayedState.entities.filter(u=>u.owner===s.localPlayer&&u.kind==='unit'&&u.hp>0&&!u.embarked).filter(u=>{const q=window.rtsDiagnostics.point(u.x,u.y);return q.x>=bounds.x1&&q.x<=bounds.x2&&q.y>=bounds.y1&&q.y<=bounds.y2;}).map(u=>u.id);return {eligible:true,id,tick:s.tick,type:e.type,state:e.state,point,bounds,inside,priorSelection:s.selection,ordinaryPoint:window.rtsDiagnostics.entityPoint(id)};},id);
 if(!plan.eligible)return {used:false,plan};
 const box=await p.locator('#world').boundingBox(),b=plan.bounds;
 if(plan.inside.length!==1||plan.inside[0]!==id||b.x1<0||b.y1<0||b.x2>box.width||b.y2>box.height)return {used:false,plan};
 if(Math.hypot(b.x2-b.x1,b.y2-b.y1)<=7)throw Error('Rectangle drag must exceed ordinary UI threshold');
 await p.mouse.move(box.x+b.x1,box.y+b.y1);await p.mouse.down();await p.mouse.move(box.x+b.x2,box.y+b.y2,{steps:2});await p.mouse.up();
 const after=await p.evaluate(()=>window.rtsDiagnostics.snapshot()),current=after.displayedState.entities.find(e=>e.id===id);
 const trace={used:true,plan,after:{tick:after.tick,selection:after.selection,current:current&&{id:current.id,owner:current.owner,kind:current.kind,type:current.type,hp:current.hp,embarked:current.embarked}}};
 if(after.selection.length!==1||after.selection[0]!==id||!current||current.owner!==after.localPlayer||current.kind!=='unit'||current.type!==plan.type||current.hp<=0||current.embarked){throw Error('Unique rectangle must acquire exact CURRENT living own unit '+JSON.stringify(trace));}
 return trace;
}
