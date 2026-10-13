/** Placement policy shared by authority and visible-client preview.
 * Reserve links for living construction sites too: completing them must not
 * silently turn a permitted line/corner into a T or cross. Enemy links do not
 * join a friendly wall. Existing junctions are never deleted by this policy.
 */
const directions = [[1,0],[-1,0],[0,1],[0,-1]];
const fortification = e => e?.kind === 'building' && ['wall','gate'].includes(e.type) && e.hp > 0 && !e.embarked && Number.isInteger(e.x-.5) && Number.isInteger(e.y-.5);
const key = (x,y) => `${x}:${y}`;
export function fortificationPlacement(entities, owner, type, x, y) {
  if (!['wall','gate'].includes(type)) return {ok:true,error:null};
  if (!Number.isFinite(x) || !Number.isFinite(y)) return {ok:false,error:'Invalid construction site'};
  x = Math.floor(x)+.5; y = Math.floor(y)+.5;
  const cells = new Set(entities.filter(e=>fortification(e)&&e.owner===owner).map(e=>key(e.x,e.y)));
  // The ordinary footprint validator owns overlap rejection.
  if (cells.has(key(x,y))) return {ok:true,error:null};
  cells.add(key(x,y));
  for (const [cx,cy] of [[x,y],...directions.map(([dx,dy])=>[x+dx,y+dy])]) {
    if (!cells.has(key(cx,cy))) continue;
    const links = directions.filter(([dx,dy])=>cells.has(key(cx+dx,cy+dy))).length;
    if (links>2) return {ok:false,error:'Stone walls and wooden gates support straight lines and corners only; T and cross junctions are not allowed.'};
  }
  return {ok:true,error:null};
}
