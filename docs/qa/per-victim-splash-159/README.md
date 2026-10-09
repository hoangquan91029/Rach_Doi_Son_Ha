# Per-victim splash candidate159 — staged intake receipt

2026-10-09. Based on canonical156 sim SHA256 `df4326ca874a0f935034d05bcad434b93fa5d14b1dca1655548cceb983f75d5b`, Git base `64f709049c753416cdfb12b5703cf4d1770b300a`. Candidate: `/tmp/per-victim-splash-159`.

## Change and policy

Extract existing primary damage calculation into `mitigatedAttackDamage`, reuse for primary and each secondary victim. Each victim independently applies type/kind bonus, supply-denial target bonus, own unit/building armor, owner armor/fortification, terrain and river-defense conditions. Attacker supply/morale/terrain/shock/tempo factors remain identical. Primary arithmetic/order is unchanged. Splash uses `max(1, mitigatedVictimDamage * 0.35)`, preserving original scaling order and minimum one.

Impact timing, range, visibility, attack commitment/cancellation, cooldown and existing secondary eligibility filters are unchanged. Dead/friendly/embarked secondary entities remain excluded by the existing predicate. No units data, balance, movement or passenger156 behavior changed.

`candidate.patch` owns only shared/sim.js and tests/per-victim-splash159.test.js. `binding.json` pins exact source/test/patch and full-suite additional160/157 inputs. Baseline sim bytes were copied before candidate edits and preserved at `/tmp/per-victim-splash-159-before/shared/sim.js`.

## Evidence

- `before-patch.tap`: unchanged156 baseline, 6 tests: 2 PASS/4 FAIL, reproducing independent-primary-armor, each-victim mitigation, mixed-building/supply bonuses and shared attacker-factor splash discrepancies.
- `focused.tap`: candidate6/6 PASS. Primary exact formula checked; varying primary armor leaves secondary damage constant; victim armor/hill/ford/fortification/river-defense matter; mixed unit/building and supply-denial bonuses apply correctly; no early damage, existing exclusions/minimum one preserved; same-seed/commands complete-state hash deterministic; attacker starvation/morale/forest/shock/tempo factors shared.
- `shared-regression.tap`: 60/60 PASS,85.569 seconds: shared sim/navigation/crowd/passenger156, six AI victories (both maps × three difficulty levels), two naval training/embark/landing/frontline-food regressions, General combat/transport defeat and commitment/timing/cancellation contracts.
- Full suite (`full-suite.tap`): 140/140 PASS, 0 FAIL, 83.092 seconds. Run only after package160 fixes were available; its two obsolete terrain-only regex tests copied into stage. Script157 copied into stage for the existing coverage157 test. Neither is part of159 patch.

## Scope and limits

Tests use in-memory ordinary attack command fixtures with explicitly placed/mutated terrain/entities/modifiers to isolate damage contracts. They are simulation evidence, not actual browser/visual/full-match acceptance. Existing snapshot ownership/visibility rules and world navigation are untouched.

`client/`, `public/`, `node_modules/` are read-only symlink inputs. Shared/server/tests are copied. No canonical edits, active dist writes, build, service restart, deployment, Git writes, top-level status changes, art/API calls or quota checks. Root intake is required for installation/promotion. Overall project remains INCOMPLETE.
