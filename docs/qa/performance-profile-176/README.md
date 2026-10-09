# Mature simulation CPU profile176

Checkpoint `509903bafe02e5a5c960f3413f42c0c549a13d65`. Exactly one Delta/5-world diagnostic run: normal built-in player1 AI, seeds 171–175,90 s natural preparation +20 warmup ticks with profiler OFF. Inspector then measured 200 ticks/10 simulation seconds at 1000µs sampling, two-player compact snapshotView+JSON every 4 ticks. Preparation 14.844s; total 17.085s. No service/network/build or gameplay mutation.

```sh
node scripts/profile-simulation.mjs --ticks 200 --sample-us 1000 --out-dir docs/qa/performance-profile-176
```

At tick 1820 each world had 39 living units (owners 9/30),50 entities; final tick 2020 had 38 living units and49 entities. Every world remained active; no full-match result, minted armies/resources or 200-unit claim.

| Work phase | Sampled stacks | Five-world step p50/p95/max ms |
|---|---:|---|
| Normal step | 1616 | 4.738/55.162/68.917 |
| Periodic AI-due step | 61 | 14.291/19.386/19.386 |
| Snapshot view + JSON | 342 | snapshot epoch p95 7.830 |
| Inspector/other gaps | 5 | excluded from step timings |

Four periodic AI-due cohorts were measured. Exact ai() ancestry accounts for 34/2024 samples (1.68%); GC accounts for 24/2024 (1.19%). The high step tail is mainly outside periodic AI execution. Phase labels mark whole AI-due steps, while inclusive ai() stack counts identify its actual contribution.

| Exact function in shared/sim.js | Line | Self samples (% total) | Inclusive samples (% total) |
|---|---:|---|---|
| updateFog | 147 | 476 (23.52%) | 511 (25.25%) |
| travel | 132 | 139 (6.87%) | 795 (39.28%) |
| path | 81 | 98 (4.84%) | 367 (18.13%) |
| navigationStep | 72 | 144 (7.11%) | 286 (14.13%) |
| crowdPatch | 116 | 24 (1.19%) | 277 (13.69%) |
| crowdSweep | 106 | 134 (6.62%) | 205 (10.13%) |
| ai | 351 | 0 (0.00%) | 34 (1.68%) |

The normal-step tail was analyzed separately from the full profile: 14 normal cohorts above 25ms contain 700 samples. Within those sampled stacks travel is inclusive 620 (88.57%), path 334 (47.71%), navigationStep 245 (35%), crowdPatch 165 (23.57%), and updateFog 36 (5.14%). Exact function URLs, columns and all counts are in spike-hotspots/profile JSON. Inclusive percentages overlap because functions share stacks; recursive frames are counted once per function/sample.

Many expensive ticks recur about 20 ticks apart (1832,1852,1872,1892,1912,1932,1952,1972,1992,2012). Source travel() at 135 retries failed global paths after 20 ticks. That is a plausible explanation for the periodic navigation tail, not proof of the precise entity/retry cause. CPU evidence justifies a finite path/navigation investigation before changing algorithms. A candidate could reduce repeated integer-cell terrain/building queries while preserving exact owner-gate exceptions, continuous fractional guards, diagonals, range/terminal arrival, navigation invalidation, deterministic tie order and AI/naval contracts. No cache, path algorithm, retry cadence, fog phase, speed, balance or guard was changed. A NEW finite patch order is required.

## Sampler accuracy and limits

Raw raw.cpuprofile is directly emitted by Node Inspector. Monotonic hrtime windows in epochs.json align CPU sample timestamps to actual step and snapshot phases; only 5 samples fall in instrumentation/other gaps. summary-check.mjs validates a known call tree, recursive deduplication, timestamp phase assignment, GC classification and one-based lines. It passes without starting a profile or game. analyze-spikes.mjs is offline re-analysis of the same raw profile; no second workload was run.

Hardware: 12th Gen Intel(R) Core(TM) i5-12450HX, 12 logical CPUs, Linux 7.0.0-38-generic; Node v24.15.0, V8 13.6.233.17-node.48, final load averages [1.45, 0.74, 0.58]. CPU was nonexclusive with concurrent project work. Sampler counts do not establish exact GC pause durations. Sampler overhead, synchronized worlds and short finite sampling limit precision; profile timing is not an unprofiled benchmark replacement.

This is not an online-room failure/headroom PASS, dense-army/browser/network/compression/send-queue or final-release acceptance. Online human-vs-human has no AI, although this profile indicates its sampled tail here comes primarily from normal movement/navigation. No production service, dist, server/sim/data/client/status or Git mutation. Only new script and assigned QA were written. Runtime sources remained byte-identical before/after; hashes.json binds profile and sources. Overall project remains INCOMPLETE.
