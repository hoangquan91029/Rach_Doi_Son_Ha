# Logistics UI candidate163 — staged intake receipt

2026-10-09. Stage `/tmp/logistics-ui-163`; canonical baseline sim SHA256 `8f0ef62fea99b72d6a6f3ec40461e00b26ef0f08bc3bdfb34acbdc20a427a62a` retains156/159.

## Change

Training enqueue saves `total` from the actual unit trainTime multiplied by all currently combined player train modifiers. Each job keeps this binding; later modifier changes do not rewrite it. The HUD uses saved total and clamps progress to0–99 while remaining work is positive,100 when completed. Mobilization continues accelerating work at the existing rate. Legacy entries without total retain a bounded base-duration fallback; their original modified total cannot be reconstructed reliably.

Own army warning derives from displayed own living military/leadership/naval unit rations, including embarked passengers; villagers/wagons are excluded. It uses existing BALANCE.lowSupply0.25, independently of strategic food totals and cargo. A persistent readable `ARMY LOW ON FOOD` banner aggregates units needing resupply and clears on recovery. Text changes only when its summary changes; no repeated event/toast messages, extra authoritative warning state, or new mechanics thresholds were added. Snapshot ownership/liveness and finite ration mechanics are unchanged.

Owned patch paths: shared/sim.js, client/main.js, new client/logistics-hud.js, tests/logistics-ui163.test.js. No index/CSS/data/server changes.

## Verification

- `before-duration.tap`: new duration contract against original159 sim with new pure HUD helpers:7 tests,3 PASS/4 FAIL. Warning/helper tests pass because this isolates missing authoritative queue metadata, not old UI rendering.
- `focused.tap`:22/22 PASS,2.891seconds:8 new contracts + passenger156, splash159 and existing storage HUD. Covers default and combined/overlapping leader train modifiers,0% enqueue, saved duration, bounded legacy progress,100 only at completed work, ordinary legal mobilization2× progression, owner-only full/compact queue snapshots, freeze without stepping, finite own-ration aggregation/recovery (including actual simulation store depletion), embarked/leadership/naval/support/dead/enemy scope, and resource-pool independence.
- `build.txt`: successful staging-only Vite build into `/tmp/logistics-ui-163/build`; build/source hashes in binding.json. No broad full suite was necessary for this metadata/presentation package.
- Browser proof (`browser-proof.json`): Chromium151.0.7922.34, ordinary UI only,0 page errors. Actual combined leaders bind total6.11064; after0.5s work the selected Barracks displays8%, pause keeps tick/progress stable and production completes after resume. Two legal Xiang Yu ability pairs at their existing cooldown produce4 low-ration military units at tick1332 despite552.4 strategic food; banner remains stable during pause. After legal commitment expiration, ordinary F2/Move orders bring troops into finite resupply and the banner clears at tick1711. Final screenshot was inspected: centered banner is readable without overlapping commander cards. `modified-training-visible.png` shows live unblurred progress; `army-low-food.png` and `army-food-recovered.png` show warning and recovery. No simulation mutation or injected gameplay commands.

## Preserved repair history

`initial-fixture-failure.tap`: warning test mutated embark/position-sensitive fixture state then incorrectly expected first view's fog refresh not to change the hash. Final test refreshes the view before recording its baseline and checks repeated pure warning calls do not mutate state.

`initial-browser-selector-failure.json/.png`: first script used obsolete resumeBtn selector; actual UI uses resume/toMenu. Corrected harness, no product code change.

`initial-overlap-proof/`: initial successful UI training/warning proof and its binding preserved. Warning overlapped the King card; final source moves it to centered below resource totals. Paused training screenshot is deliberately a pause proof; final visible training screenshot supplies unblurred progress evidence.

`shock-commitment-proof/`: final placement/paused warning proof succeeded, but immediate recovery movement was legitimately rejected during Xiang Yu shock commitment. Final harness waits for the existing commitment to expire before issuing a resupply movement order; guards and mechanics were preserved.

## Scope

This is a staged code candidate, not canonical installation/public promotion or broad match acceptance. Client/shared/tests copied into isolation; public/node_modules read-only symlinks. Public dist/service, canonical source, Git and top-level status untouched. No art/API calls or quota checks. Root intake required; overall project remains INCOMPLETE.
