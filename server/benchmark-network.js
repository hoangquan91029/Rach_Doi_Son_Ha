import assert from 'node:assert/strict';
import { gzipSync } from 'node:zlib';
import { createMatch, step, view, hashState } from '../shared/sim.js';
import { snapshotView } from './index.js';
export function benchmarkNetwork() {
 const rows=[];
 for(const unitsPerPlayer of [20,100,200]) {
  const state=createMatch({seed:731});
  for(const owner of [0,1]) {
   const template=state.entities.find(e=>e.owner===owner&&e.type==='infantry');
   const count=state.entities.filter(e=>e.owner===owner&&e.kind==='unit').length;
   for(let i=count;i<unitsPerPlayer;i++) {
    const entity=structuredClone(template);entity.id=state.nextId++;entity.x+=(i%4)*.35;entity.y+=Math.floor(i/4)%5*.35;state.entities.push(entity);
   }
  }
  for(let i=0;i<200;i++)step(state);
  for(const player of [0,1]) {
   const full=view(state,player);const before=hashState(state);const compact=snapshotView(state,player);const after=hashState(state);
   assert.equal(before,after,'snapshot must not mutate authoritative gameplay state');
   const hydrated={...compact,map:{...full.map,...compact.map}};
   assert.deepEqual(hydrated,full,'hydrated view must equal original view');
   const raw=JSON.stringify({type:'state',state:full,paused:false}),reduced=JSON.stringify({type:'state',state:compact,paused:false});
   rows.push({unitsPerPlayer,player,tick:state.tick,hash:after,visibleEntities:compact.entities.length,fullBytes:Buffer.byteLength(raw),compactBytes:Buffer.byteLength(reduced),savedPercent:+((1-Buffer.byteLength(reduced)/Buffer.byteLength(raw))*100).toFixed(1),fullGzipBytes:gzipSync(raw).length,compactGzipBytes:gzipSync(reduced).length});
  }
 }
 return rows;
}
if(process.argv[1]?.endsWith('benchmark-network.js')) console.log(JSON.stringify(benchmarkNetwork(),null,2));
