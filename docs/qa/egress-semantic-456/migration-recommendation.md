# Proposed strict historical contract migration

Original177 optimized-query memo contract should compare memoized and nonmemoized implementations of the same intended navigation semantics. The455 egress fix changes those semantics intentionally; retaining an occupiedpoint navigation bug merely to match the oldstatehash is inappropriate.

Keep original177 fixture, originaltests and455 failurelogs as immutable historical evidence. Introduce a separatelynamed/pinned reference by copying oldnonmemoized177sharedsource and applying the identical singleoccupiednonterminalreconnect predicate. This makes the optimization reference share the intendedbugfix while preserving its independentnonmemoizedquery implementation. Do not drop crowdStats, routes or positions from the strict test.

`reference-fixed/shared/` holds that newreference. `navigation-cache177-migration-proposal.test.js` is a proposed file for future root-controlled installation into the testsdirectory: only fixture URL and SHA differ from originaltest; completehash assertions and all8scenario bodies stay unchanged. It is not installed. `fixed-reference-equivalence.test.js` proves all8strict scenarios now PASS using candidate455 and thatreference.

Separate semantic diagnostic ignoringONLYcrowdStats reveals actual AI paths diverge from original177 at tick501 for enemyvillager25 on bothmaps; terminalstates differ through2000. Same-tickbuild/combat scenario remains equivalent across109ticks exceptcounters. This is an intentionalbehaviorchange, not a counters-onlyclaim. Everytickbudget stays4plans/4096plannerEdges.

Root must review thebugfix/referenceprovenance and qualify a newpairedruntime/UI before protectedsource/publicdeployment. Existingbackend230 remains unchanged.
