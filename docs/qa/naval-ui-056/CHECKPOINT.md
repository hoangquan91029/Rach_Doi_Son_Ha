# 056 terminal HOLD — scouting reveals coast; QA arrival radius incorrect

ONE actual scout-first Coasteasy Chromium attempt on frozen043 candidate33da4dd6…7e548. Exact own scout10 selected, ordinary rightclick move9/36 issued; no injected state/order/entity/resource and no hidden enemy queries. Original054 no-visible-water preflight retained. No retries, build/train/transport calls or publicservice operations. Raw full snapshots/code/sourcepins/failure screenshot preserved.

Scout completed ordinary movement at8.574802/35.574802, lastMovedTick160, stateidle/ordernull, hp65. Requested9/36 residual≈0.60132; harness incorrectly waited for residual<0.3 until37.706s/tick718. shared/sim.js tickUnit uses `travel(s,e,o,0.7,true)` for move; actual arrival is within its real0.7 completion radius. This is a harness predicate mismatch, not evidence of a new navigation failure. Original HOLD is unchanged; no predicate edit or rerun occurred.

Actual final ownfog has revealed southern water and the9/38 shore site. A next fresh finite order should use **actual order completion plus distance≤0.7 and target fog reveal** for scouting, preserving exact identity/ownership/living guards. The same documented0.7 applies to normal naval movement; embark uses separate2.6 contact radius. Do not demand arbitrary sub0.3 ground arrival or change simulation to accommodate QA.

Next after intake: finite ordinaryUI scout→revealed vacant dock9/38→build15s→transporttrain16s→same scout rendezvous9/39→shipLoad→revealed-water move→Unloadnearlegalground. Revalidate affordability, visible legal site/water spawn/destination and no newly occupied obstruction at each stage. Keep150s total/0retries; stop failures; do not assert naval proof from this scouting-only attempt. Code has not executed its later stages.

Errors0/networkfailures0; ownedbrowser/serverclosed, healthrooms0/roomsAfterClose0/listeningAfterClosefalse. Only docs/qa/naval-ui-056 changed. No naval completion, finalart or production claim.
