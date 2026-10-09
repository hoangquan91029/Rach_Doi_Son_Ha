#186 tempo first-strike runtime closure

Root chose to fulfill the existing promise, preserving the description. Owned shared/sim.js, tests/tempo-first-strike186.test.js, this QA directory, and an append-only CURRENT follow-up in184 ledger. Original184 mismatch text/receipts/tests remain unchanged; its promise now passes. No data/client/server/art/build/service/status/commit changes.183 scene/source evidence predates this runtime and is not claimed as186 proof.

Baseline177 sim: c95e26d9c7e77d1e1f196b53833fdc38bc871f2fa5a9ade044e56829e118bb27.
Candidate186 sim:4aa2bfbdb499371cd18adc4306b3ae313fe8c7410e3d4e2957a46b40e67c85a5.
candidate.patch and bindings.json bind exact source/test/evidence.

At each already validated authoritative impact, gather live owner tempo casts and prune consumed tokens against them. Eligibility retains existing anchored radius and40-tick recent-movement rule. One boolean applies×1.3 to the primary and all splash victims before each victim's own mitigation. Successful boosted impact consumes every currently eligible unconsumed cast token(source:until). Same cast cannot be renewed by moving again; simultaneous same-character King/General casts do not supply extra boosted hits. Later casts can renew. Invalid targets/canceled windup/nonadvancing/outside-radius/expired impacts do not consume. Speed×1.4,duration14,cooldown60 and all base/ration/morale/terrain/attack validations remain unchanged.

State uses serialized per-unit tempoConsumed strings, no WeakMap/hidden consumption state. Player view destructuring omits this internal field for BOTH owners/opponents. Token pruning occurs only at valid impact; obsolete entries can persist until the next valid impact but cannot become eligible or affect later casts.

Correctness:
- focused.tap29/29PASS:9 new first/second/re-advance, same-character overlap, nonadvancing, cancellation/dead target, expiry/radius, natural new cooldown cast, mixed-armor splash, JSON roundtrip/determinism/private views and enemy ownership; original18420 promises allPASS.
- regression.tap82/82PASS,67.959s: full simulation combat/AI/naval plus159per-victim,177exact baseline equivalence/default-character both-map AI, navigation/crowd/arrival,156physiology and163logistics contracts. No comparison weakening.

Commands:

    node --test tests/tempo-first-strike186.test.js tests/leadership-contracts184.test.js
    node --test tests/sim.test.js tests/per-victim-splash159.test.js tests/navigation-cache177.test.js tests/navigation.test.js tests/crowd.test.js tests/passenger-physiology156.test.js tests/logistics-ui163.test.js

first-focused.tap retains27PASS/1fixtureFAIL: the expiry fixture left an idle infantry beside an enemy for280ticks, allowing valid autoattacks before expiry and creating then pruning a legitimately consumed marker. Corrected fixture moves the target out of engagement during the wait, then restores it before the expiry probe. No runtime/guard correction used to hide that failure.

Synthetic mechanics contracts are not browser/public acceptance. No benchmark/full browser match/build was run. Candidate awaits root intake; public/service unchanged.
