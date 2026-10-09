# Diagnostic simulation baseline171

2026-10-10. Source checkpoint `79c5b5b076b08762652d13da02b3bad2b9302339`; real shared createMatch/step/normal AI plus exact server compact snapshotView and JSON envelopes. No service was started. Run took 89.292s.

```sh
node scripts/benchmark-simulation.mjs --maps delta,coast --worlds 1,5,8 --evolve-seconds 90 --warmup-ticks 20 --measure-ticks 100 --seed 171 --wall-seconds 180 --out docs/qa/performance-baseline-171/baseline.json
```

Each cohort naturally evolves to 1800 ticks/90s, warms 20 ticks, then measures 100 ticks/5 simulated seconds. Two-player compact view+JSON runs every 4 ticks, matching server cadence. Every world stayed active throughout measurement. Worlds begin with 26 units/34 entities; at tick 1820 each reached 39 living units (owners 9/30), about 50 live entities and 11 combat units. Delta ends with 38 units; coast 39. No 200-unit claim, minted resources, cloned armies, external gameplay commands, speed changes or full-match result.

| Map | Worlds | Step p50/p95/p99/max ms | Both-seat snapshot epoch p95/max ms | Raw JSON bytes/s across cohort |
|---|---:|---|---|---:|
| delta | 1 | 0.984/11.788/12.803/12.958 | 1.681/1.751 | 493076 |
| delta | 5 | 4.699/54.630/61.134/61.262 | 7.624/7.662 | 2465379 |
| delta | 8 | 7.811/86.967/125.251/139.778 | 16.510/16.876 | 3944606 |
| coast | 1 | 0.973/6.458/12.350/12.439 | 1.563/1.653 | 490296 |
| coast | 5 | 4.950/32.022/61.356/61.609 | 8.465/8.694 | 2451479 |
| coast | 8 | 7.588/52.950/97.898/99.047 | 12.064/12.233 | 3922366 |

The measured tail is dominated by shared step/AI work: delta 5/8 and coast 8 exceed 50ms at p95, despite only 39 naturally reached units/world. Single-world median is about 1 ms while p95 reaches6.46–11.79ms. JSON alone is roughly 0.17–0.22ms/player at p95; compact view generation and all-world snapshot work are measured separately in baseline/summary. This locates the cost in shared step/AI at this checkpoint, not a specific function. A focused profile of the observed high-cost ticks is the next useful measurement; no optimization was made.

The 25 snapshot epochs/cohort make p99 equal the maximum for that distribution (nearest-rank quantiles). There are 100 measured batch ticks/cohort and individual samples for every active world. World start/AI phases are synchronized; this can align periodic work and differs from naturally staggered online rooms. Timer/byte accounting adds small measurement overhead. Seeded worlds can evolve identically because current gameplay does not necessarily use the seed for divergent decisions.

Hardware: 12th Gen Intel(R) Core(TM) i5-12450HX, 12 logical CPUs, 26.62GiB RAM; Linux 7.0.0-38-generic x64. Node v24.15.0, V8 13.6.233.17-node.48; initial load averages [0.24, 0.42, 0.64], final [0.95, 0.63, 0.69]. Memory/source hashes are recorded in baseline.json. CPU was nonexclusive: concurrent project workers/build tasks shared this machine; load averages do not establish isolation.

## Limits and custody

This is a diagnostic shared-simulation baseline. It does not accept Q01 headroom, live server rooms, network throughput, compression, send queues, browser/dense-army performance or public release. Normal player1 AI differs from two-human online traffic. Raw serialized byte rates are calculated from measured JSON payload sizes and cadence; they are not actual network traffic. Existing scripts/benchmark.mjs and server/benchmark-network.js use minted infantry fixtures; neither was run or relabeled here, and both remain unchanged.

Statistics/config guard tests 2/2 PASS (`tests.tap`); they test rare-tail calculation, nonmutating statistics and bounded malformed/runaway CLI requests. No broad suite, build, deploy, production restart, dist/source changes or quota checks. Only new tool/test and assigned QA were written. Sources were verified unchanged after the bounded run; hashes.json binds output and new files. Overall project remains INCOMPLETE.
