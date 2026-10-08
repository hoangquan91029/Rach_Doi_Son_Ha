Rejected implementation attempt; NOT integrated.

Actual local online candidate14 receipt disclosed exact coincident unit positions and overlapping normal-zoom silhouettes. shared/sim.js originally lacks physical unit clearance, recruitment exit occupancy and separate transport landing positions; formation destinations quantize to grid centers.

Proposed bounded occupancy steering draft is preserved in sim-proposal.js and proposal.patch; its tests are proposal-only in crowd-proposal.test.js. Land radius0.28, naval0.4, fixed-ID-handed local alternatives, swept terrain/building tests, no post-tick pushing, distinct recruitment exits, unique formation rows and subcell steering were attempted.

Initial39-test simulation suite:31pass/8fail: all six240second AI victories and both AI naval sorties failed. Narrow direct-lane lookahead correction improved held-anchor fixture but current deltaeasyAI still had nullwinner after240simulationseconds. Current new invariant suite6/7; naval-held-anchor progress failed. Occupied BFS waypoint centers remain mandatory and local steering circles rather than bypasses them. No broader pathfinder rewrite attempted.

Parent requested stopping expansion and restoring original. shared/sim.js restored byte-for-byte from9dbd8bc, SHA2560613dad6d4557c49a483a87deed918f8771ad6b8849c6dd1f4f80a4bb6bf7318. Proposed source SHA256178d7978c902c140dff7235857895b047e08ded6bb83fa2b34fcbaaeb25a3abe; proposed tests SHA256a88c9ed75e4f7a622649b0aec2a9112831ac6023f25a1bcd0eb1544c6e4d7827. Failing proposal tests removed from active suite. No deployment/service restart/browser rerun or balance change.

A future small correction must make locally occupied intermediate waypoints advisory while validating every physical movement, then prove narrowford progress and existingAI/naval regression suite. Additional unfinished proposal requirements: naval-aware formation spacing >=diameter+margin, distinct passable transport landing spots with partial pending unload, swept building/gate tests. Do not label current draft accepted.

Restored full npmtest confirms72/72pass,0fail,37331.35ms; retained in restored-full-suite.log. Main worktree runnable; crowd issue remains open.
