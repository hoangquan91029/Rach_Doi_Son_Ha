// State membership, not viewport membership, governs selectable friendly entities.
export function liveSelection(ids,state,owner){const valid=new Set((state?.entities||[]).filter(e=>e.owner===owner&&e.hp>0&&!e.embarked).map(e=>e.id));return [...new Set(ids||[])].filter(id=>valid.has(id));}
export function pruneSelectionState(selected,groups,state,owner){return {selected:liveSelection(selected,state,owner),groups:Object.fromEntries(Object.entries(groups||{}).map(([key,ids])=>[key,liveSelection(ids,state,owner)]))};}
