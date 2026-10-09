# Package160 — world-art route test contract maintenance

The two original regex failures expected the historical terrain-only guard. Current intended world routes are terrain, iron, workshop and camp. Only `tests/food-resource115.test.js` and `tests/hill113.test.js` were edited; runtime/simulation/art files were not changed.

Original tests are byte-preserved in `before/`, with original hash pins and the actual two-failure test output in `before-pins.txt` and `before-failures.txt`. Updated static guards assert the actual shared `worldArtEnabled()` boundary while preserving all original eligibility, finite-resource suppression, current-knowledge/fog, fallback, render-order, exact manifest dimensions and SHA custody assertions.

A new behavior test loads the actual pinned food/hill assets through the actual manifest loader and renderer API. Browser fetch and bitmap decode are stubbed for Node; real runtime bytes must pass hash custody. The same available bank is deliberately supplied to each route so absent assets cannot make a missing gate look correct. Actual draw counts prove terrain/iron/workshop/camp allow food/hill while pilot/walk/work/food and the empty route do not; depleted food and hidden hill remain excluded. This is an automated API contract test, not browser or visual acceptance.

Command: `node --test tests/food-resource115.test.js tests/hill113.test.js tests/art-coverage.test.js`

Actual result in `after-tests.txt`: **13 passed, 0 failed** — six original world contracts, one new route behavior contract and six coverage157 contracts. Runtime raster SHA is identical in before/after pins. No full suite, build, deployment or scene proof was run. Ready for root integration; project remains INCOMPLETE.
