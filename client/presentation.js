// Render interpolation only. Commands, fog, damage and victory use server state.
export function interpolateView(current,previous,alpha){
 if(!current||!previous||current.map?.id!==previous.map?.id||alpha>=1)return current;
 const old=new Map(previous.entities.map(e=>[e.id,e]));
 return {...current,entities:current.entities.map(e=>{const before=old.get(e.id);if(!before||e.hp<=0||e.embarked||before.embarked||Math.hypot(e.x-before.x,e.y-before.y)>3)return e;return {...e,x:before.x+(e.x-before.x)*alpha,y:before.y+(e.y-before.y)*alpha};})};
}
