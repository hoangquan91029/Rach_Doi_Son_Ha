#177 query-local navigation pass memo

Candidate only, awaiting root intake. Runtime ownership: shared/sim.js. Added tests/navigation-cache177.test.js and this receipt/helper directory. No server/data/client/art/build/service changes or Git writes.

The exact176 sim fixture is SHA256 a266e0de5a6719579e48fd8a57888f09509f6af745190cb09b47c5641bab7796; candidate is c95e26d9c7e77d1e1f196b53833fdc38bc871f2fa5a9ade044e56829e118bb27. Baseline dependencies are byte preserved under baseline/shared and imported from an isolated temporary ESM directory. hashes.json binds test and dependencies; candidate.patch contains the runtime diff.

Each path query allocates one Uint8Array: unknown/blocked/passable entries memoize exact pass(s,e,x+.5,y+.5). Destination and diagonal side-cell predicates reuse it. It lives only within that invocation. WeakMap building/navVersion cache, owner/gate/self/naval rules, search heap/order/cost/ties, retry cadence, fractional crowd movement and final groundSegment remain unchanged. No balance/ration/range changes.

## Correctness

correctness.tap:82/82 PASS,68.383s. Command:

    node --test tests/navigation-cache177.test.js tests/navigation.test.js tests/crowd.test.js tests/sim.test.js tests/passenger-physiology156.test.js tests/per-victim-splash159.test.js tests/logistics-ui163.test.js

New contracts compare baseline/candidate command replies and full serialized state hashes every tick, including paths: both maps diagonal/fractional/unreachable; own/enemy gate; terrain mutation and next query; legally trained sea transport versus inland targets; same-tick legal wall construction followed by authoritative enemy destruction; unmodified normal AI both maps through tick2000. Existing durable navigation/crowd/arrival and all simulation AI victories/naval regressions passed, retaining156/159/163 contracts. Synthetic setup cases are correctness diagnostics, not ordinary browser acceptance.

first-fixture-failure.tap preserves the initial focused run: one fixture failed because its enemy infantry overlapped the proposed wall center, correctly rejecting the build in BOTH versions. The enemy was moved clear while within attack range; the isolated fixture then passed, followed by the complete82-test run. This failure is not counted as PASS.

## One paired unprofiled diagnostic

paired-benchmark.mjs was run once after correctness PASS. paired-results.json and paired-run.log retain evidence. Delta5 isolated natural normal-AI worlds, seeds171..175,1800 preparation ticks,20 warmup,100 measured ticks; compact player snapshots using exact server map shape every4 ticks. No minted resources/armies or external gameplay commands. Preparation unmeasured; baseline then candidate sequential run. Full state hashes equal for all checkpoint and measurement states across5 worlds. Each world naturally reached39 living units at tick1820 and38 at1920; no winner/no-op dilution.

| Five-world cohort | Baseline176 | Candidate177 |
|---|---:|---:|
| Step p50 ms |4.737|4.677|
| Step p95 ms |52.934|11.924|
| Step p99 ms |62.163|61.056|
| Step max ms |63.407|63.678|
| Snapshot p95 ms |8.130|8.312|
| Snapshot p95 bytes |494460|494460|

Observed step p95 ratio0.2253; tails remain near64ms, so this single contract does not remove every spike. Node24.15.0/V813.6, Intel i5-12450HX12 logical CPUs. CPU environment nonexclusive with concurrent project work; order/JIT/GC/scheduling and short samples limit causal timing precision. This is offline diagnostic simulation, not network/send-queue/browser/dense-army or production room-headroom acceptance. No timing promise or public promotion verdict.
