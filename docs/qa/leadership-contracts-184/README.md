#184 mechanics rule closure receipt

Owned only docs/gameplay/leadership-logistics-rules-184.md, tests/leadership-contracts184.test.js and this QA directory. Runtime untouched. No build/browser/full-match/benchmark/network/Git write. Sol6.1 low retained.

Inspected current master/dossier/data/sim and audit154G5/G6/G7; no historical facts inferred from unread URLs. Ledger provides12 descriptions→effects, scope, timing, cooldown, passives, synergy and same-choice stacking as CURRENT behavior. Recruitment global finite cost abstraction and center-terrain building placement remain explicitly bounded policy questions; master does not expressly specify recruitment-locality/full-footprint rules. No master override or new balance approval.

New synthetic mechanics contracts exercise all12 kinds by observable movement/damage/visibility/repair/gather/production/healing/resupply/delivery control comparisons, owner rejection, cooldown/expiration and terrain denial. Related existing tests deliberately scoped, no full AI/naval repeats.

Runs retained:
- first-run.tap9PASS/4FAIL: helper selected first entity (Residence) in full-world fixtures instead of actual King; corrected helper, no runtime/guard changes.
- second-run.tap17PASS/1FAIL: construction fixture relocated units without updating fog; legal command correctly rejected unexplored ground. Advanced ordinary step to refresh visibility before placement.
- third-run.tap18/18PASS after fixture corrections.
- description-repro.tap19PASS/1FAIL after adding expiration and advertised-first-strike contract. This is a real description/current behavior discrepancy, not PASS.
- related.tap5/5PASS: node --test --test-name-pattern='12 characters|mobilization|saved actual duration' tests/sim.test.js tests/logistics-ui163.test.js.

Open discrepancy: Nguyen Hue ability wording promises first-strike damage while advancing. Synthetic ordinary move command, one step, ability and attack command: the second stationary impact within40ticks of last movement deals15.238 versus11.26 without ability. Actual source predicates amplify every hit while lastMovedTick>tick−40; no consumed first-strike state. Proposed minimal follow-up changes only description to 'Nearby troops gain speed and damage shortly after moving.' A single-hit runtime model needs an explicit balance/order decision. No runtime fix attempted; durable test intentionally retains failing promise pending root order. The20-test run is NOT declared overall PASS.
