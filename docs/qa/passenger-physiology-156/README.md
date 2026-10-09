# Passenger physiology candidate 156 — staged intake receipt

2026-10-09. Base source `64f709049c753416cdfb12b5703cf4d1770b300a`.
Candidate stage: `/tmp/passenger-physiology-156`. Canonical source, active dist, production service and Git were not changed by this worker. `client/`, `public/`, `node_modules/` are read-only input symlinks; shared/server/tests are copied. No build was needed for this shared simulation contract.

## Change

Run starvation/grace/attrition and fed morale recovery for embarked passengers after their finite own-ration consumption. Keep resupply limited to non-embarked units. Return immediately after physiological death, then follow ship coordinates and return for living embarked passengers. Existing land orders, ability healing and world effects remain skipped aboard. No changes to balance, speed, range, ownership, visibility or liveness guards.

`candidate.patch` contains only shared/sim.js and the new targeted test. `binding.json` records baseline and exact hashes.

## Evidence

- `before-patch.tap`: same finalized five tests against copied original shared code: 1 PASS/4 FAIL. Ordinary train/load commands create the embark contract; fixture positions/inventory/HP are setup, not actual browser gameplay acceptance.
- `focused.tap`: 5 PASS/0 FAIL. Zero rations: 24-second no-damage grace, 30-second accumulated hunger and morale loss, equal land/passenger attrition; own snapshot preserves embark marker, movement command rejected. Fed: exact finite ration decrement, starvation reset, morale recovery, no automatic ship/wagon/store refill, cargo conservation and no strategic resource creation. Boarded General death causes authoritative defeat/frozen progression. Ordinary unload preserves hunger and restores land commands. Enemy warship destruction still kills hungry passenger.
- `full-suite.tap`: npm test, 127 tests, 125 PASS/2 FAIL, 84.435 seconds. All shared simulation contracts pass, including six delta/coast easy/normal/hard AI victories, both actual AI train/embark/land/frontline-food regressions, navigation/crowd and transport-General defeat.
- `canonical-unrelated-baseline.tap`: unchanged canonical tests reproduce the same two failures (6 tests, 4 PASS/2 FAIL): food-resource115 and hill113 static regex expectations for the old terrain-only gate conflict with current client route. These unrelated failures were not modified or labeled PASS.

## Fixture repair history

`initial-fixture-failure.tap` preserves initial 3 PASS/2 FAIL: own snapshots include passengers with an embark marker (renderer hides them); ship and wagon also consume nearby store stock. Final fixture checks the marker and gives competing consumers enough initial rations to isolate passenger refill.

`derived-pool-fixture-failure.tap` preserves 4 PASS/1 FAIL: setup changed store inventories but player food remained the prior cached total until economy recomputed it. Final contract checks the finite derived store total, unchanged wood/iron and non-increasing food pool.

## Lifecycle and limits

Existing `get` excludes dead units. Dead passenger IDs remain in transport cargo as in the pre-existing transport-death path; ordinary unload ignores dead IDs and clears them. Body retention, loss accounting and defeat semantics remain unchanged.

This package is a code candidate, not public promotion or browser/visual/full-match acceptance. Root intake is required before canonical installation. Full suite is not entirely green because of the two verified baseline failures. No GP2 splash work, art calls, API calls, quota checks or service restart occurred.
