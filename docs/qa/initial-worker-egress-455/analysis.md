# Initial worker egress455 — isolated candidate

Confirmed the original Coast9 accepted Move stalls after400steps. Its selected nonterminal reconnectpoint7.5/24.5 overlaps the stationary king5 body at7.5/25. The local planner insists on reaching that occupied point exactly.

One predicate checks nonterminal candidatewaypoints with the existing `crowdSweep(q,q,true)` before selecting them. Terminal contact handling remains unchanged. The check uses the existing terrain/building/body constraints and consumes the existing4096planningedge budget before FIFO admission. Fourplans/tick, queue order, speed and radii remain untouched. No unit is moved aside.

29 focused checks PASS:13 originalspawn regressions,10existing crowd tests,6existing navigation tests. ExactCoast9 reaches normalarrival range deterministically. Bothmaps worker7–12 trials reach freevisibleland from originalspawn with no bodyoverlap or displacement of uncommanded neighbors.

Historical navigationcache177 fullstate comparison: unchangedcurrent39e3eb0 passes8/8; candidatepasses5/8 and fails3exactwholehash assertions. Firstdifferences are only crowdStats.edges/queries/plannerEdges (build tick23 +1; bothAI tick45 +2), from the newbudgeted pointchecks. Entitypositions/path/orders match at firstdivergence. This does not establish identicallaterstates; original tests/assertions and allfailurelogs remain preserved. Firstisolated run lacked the historicalfixture, subsequently copied unchanged; that error is retained.

Allcanonical/public451/backend230/HEAD/baseline pins unchanged. Candidate stage and diff only, no browser/build/image/deployment. Handles CLOSED. Root review and pairedruntime/UI qualification remain pending.
