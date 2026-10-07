# Shore candidate browser performance diagnosis — 7 October 2026

The current ten-material/sprite candidate shows a real rendering slowdown in this headless environment. Removing frequent diagnostic snapshots does not remove it. This is an initial 17-entity scene comparison, **not dense-battle acceptance or hardware-independent FPS certification**.

## Bounded measurement

Run `node scripts/browser-performance.mjs` against the local production server. The script opens ordinary easy single-player games in Chromium 151 and Firefox 153 at 1440×900, DPR 1, normal zoom 1.08. It samples requestAnimationFrame timestamps for four seconds without touching diagnostics, then separately repeats with one read-only snapshot per second. It moves the camera through an ordinary minimap click toward world (27,24). That river camera remains subject to actual current fog; no scouting, map/entity mutation or fabricated units occurs. Default and candidate games start independently. Screens remain document-visible.

Evidence: `artifacts/performance/shore-contrasts/receipt.json`; Chromium renderer environment: `artifacts/performance/shore-contrasts/chromium-gpu.json`. Current candidate has ten assets, with no dedicated shore material yet. Measurements apply to the integrated 12-band transition pass and continuous per-cell material painting, before any proposed cache change.

| Browser / mode | Menu RAF p50/p95 ms | Base pure RAF p50/p95 ms | River pure RAF p50/p95 ms |
| --- | --- | --- | --- |
| Chromium / default | 16.7 / 16.8 | 16.7 / 16.7 | 16.7 / 33.4 |
| Chromium / candidate | 16.7 / 16.7 | 50.0 / 50.1 | 66.6 / 66.7 |
| Firefox / default | 17.06 / 17.16 | 17.06 / 17.12 | 17.08 / 33.22 |
| Firefox / candidate | 17.06 / 17.16 | 33.30 / 50.36 | 50.32 / 66.44 |

Candidate pure base/river RAF sample counts are Chromium 87/66 and Firefox 101/77. The separate sparse-snapshot cadence is essentially unchanged. Chromium snapshot cloning costs approximately 0.4 ms at its three samples per window; Firefox exposes coarser zero-millisecond clone measurements. Sparse app `frameMs` medians are Chromium candidate 5.7 ms base / 9.7 ms river and Firefox candidate 40 ms / 51 ms. Those three-sample values are illustrative, not robust frame-time percentiles. Existing diagnostics measure the entire synchronous game frame through renderer return, including offline simulation step/view, and exclude some later HUD/paint work. The older receipt label `renderMs` should not be interpreted as renderer-only timing.

## Findings and limits

Both menus and default base rendering achieve approximately 60 Hz. Thus the environment is not imposing a universal 20 Hz RAF cap. Candidate base and river rendering have worse cadence with no per-frame cloning at all. The river camera adds work in both modes, and the candidate penalty is present in both browser engines. This supports a real candidate canvas rendering/rasterization cost rather than snapshot measurement overhead as the main explanation.

Chromium explicitly reports software 2D canvas, software GPU compositing/rasterization and ANGLE SwiftShader. Its synchronous JS frame timing does not include all deferred canvas/paint/compositor execution; the large cadence gap is consistent with that deferred work. Firefox's larger synchronous frame cost shows engine-dependent accounting and execution. No tracing isolated individual Canvas draw commands, so these contrasts do not prove whether original material fills, transitions or sprite sampling accounts for each millisecond. These are software-headless timings and should not be generalized to a player's GPU.

## Concrete next fix for parent consideration

Cache the static world-ground result (original continuous material planes plus bounded transition masks) in an offscreen surface or bounded chunks. Key it by map terrain content, actual material/frame identities and observed-terrain coverage; invalidate on relevant art or fog changes. Draw the resulting raster once per visible chunk while leaving final fog, props, entities and UI in their existing order. Preserve world anchoring and camera scale, and never bake enemy entities or remove fog. A bounded chunk cache avoids a full-world high-DPR allocation.

Additionally prepare material selection and pattern transforms once per material/frame/context rather than inside each of twelve bands per edge. Current transition painting repeats manifest filtering, raster selection and pattern transformation for every band; this is avoidable CPU work but does not by itself establish the deferred raster bottleneck. Static overlay caching removes repeated band clips/material resampling and provides a direct controlled comparison.

After parent authorizes an implementation, repeat these same contrasts against the unchanged ten-asset baseline, inspect actual normal-zoom browser captures for mask/camera/fog regressions, and then evaluate separate representative movement/combat scenes. No runtime renderer or terrain changes were made during this diagnosis.

## Controlled cache comparison

Parent integrated a static ground cache and repeated the same four contrasts against the unchanged ten-asset package. Original receipt: `artifacts/performance/ground-cache-ten/receipt.json`; associated manifest/bundle pin: `build-pin.json`; tracked copies: `docs/qa/checkpoint/ground-cache-*`. Normal-world projection, actual terrain content and source art remain unchanged. Fog, transition overlays, props, resources, entities and UI are dynamic and are not baked into the static terrain cache.

Chromium candidate base pure RAF p50/p95 improved from50.0/50.1ms to16.7/16.8ms; river from66.6/66.7ms to16.7/33.3ms. Firefox candidate base improved from33.30/50.36ms to17.04/17.18ms; river from50.32/66.44ms to17.04/17.18ms. Both runs have zero page errors. This is a substantial measured improvement in the same initial-scene software environment, not dense-battle acceptance.

`client/terrain-cache.js` retains one full-world offscreen surface bounded to8million backing pixels (~32MBRGBA). It keys actual terrain content, material encoded hashes/current frame and output quality, reuses across camera panning/zoom, and rebuilds on map/art/DPR change. A64logical-pixel pad retains existing development terrain overhangs. Explicit tests cover same-ID content changes, art readiness, pan reuse and memory bounds. Actual source PNGs are unchanged.

The later shoreB/foliage candidates require their own integrated smoke and performance checks; do not silently transfer the ten-asset measurement to an expanded package.

## Full actual delta victory with thirteen candidates

A single authorized candidate run completed through ordinary UI using `QA_PERFORMANCE=1`, local production `?art=pilot`, easy delta, 1280×800 viewport. It won by **Enemy General defeated** at tick 2433 (121.65 simulation seconds; 121.743 measured wall seconds after initial launch), with zero page errors and verified result-screen/menu return. All 121 sparse windows report thirteen ready assets. Receipt and victory capture: `artifacts/performance/candidate-thirteen-ai-win/delta-receipt.json` and `delta-victory.png`.

The build pin records `/assets/index-BGPMj5CE.js`, bundle SHA-256 `012b35851a515ecf4b1b3e22c69e4a0de8e05f5ad8eeda5191289a26fba6f441`, manifest SHA-256 `e6c9a68aa17332d34cd21158197885fc73fd2aaee84b591b43236e5066f59dfd`, and all thirteen immutable runtime hashes in `build-pin.json`.

The 7,246 numeric RAF intervals give p50/p95 cadence **16.7 / 16.7 ms**. Sparse synchronous app frame costs give p50/p95 **3.3 / 5.8 ms**, including offline simulation/view/render work. These are observed Chromium software-headless timings during this match, not a broad browser or hardware certification.

Sampled peak density was **52 live entities in the fog-filtered observed state**, **17 observed military**, **31 live entities inside the current viewport**, and **14 military inside the viewport**. These independent sampled maxima need not coincide. At a window with fourteen military in view, tick 2044 and camera approximately (30.14,24.50), there were 28 live viewport entities, RAF p50/p95 16.7 / 16.7 ms and app frame cost 4.3 ms. Own entities outside the viewport may remain in the observed state; hidden enemy populations and global maximum army size are not established. This is a real modest combat scene, not dense-battle acceptance.

The winning-run telemetry omitted terrain-cache counters, so no per-match cache-build/draw count is claimed. Separate root-controlled cache contrasts remain the appropriate evidence for cache reuse. No client/art changes or additional full-match reruns were performed during this measurement.

## Public HTTPS loading diagnosis and bounded recovery

The original thirty-second `networkidle` failure remains unchanged at `artifacts/art-v1/gradient-thirteen-public/failure.json`. A single fresh, normal-TLS Chromium retry with resolver IP 103.84.155.153 reached the menu at **31.232 seconds**, without page errors. Timing receipt: `artifacts/performance/public-loading-retry/receipt.json`.

Document transfer finished at 1.010 seconds, production bundle at 1.739 seconds and manifest at 2.331 seconds. The first four runtime requests started at 2.333 seconds; water/forest/grass finished at approximately 10.835/12.371/13.390 seconds. Residence finished at 21.281 seconds with approximately 18.946 seconds request duration, delaying the next four-resource batch until 21.305 seconds. Final palm transfer finished at 30.803 seconds. This supports relay/resource transfer latency compounded by the existing four-resource batch barrier; the bundle itself arrived promptly. An explicit DOMContentLoaded timestamp was not retained in this receipt, so document-transfer completion is reported separately from actual menu readiness without treating them as the same event.

The observed resource tail justifies progress and failure recovery; it does not justify calling the failed thirty-second run a success. The narrow client fix adds per-asset progress notifications, a thirty-second deadline covering each resource fetch/body/hash/decode, and a sixty-second total preload budget. The budget is shared across existing four-way batches. Validation, hash checks, asset rejection, source images and fallback classification remain intact. A late decoded bitmap is closed after its deadline. Failure keeps a truthful boot message with Retry and an explicit option to continue using development placeholders; failed art never becomes approved. A twenty-second HTML watchdog provides Retry if the main bundle never starts. Successful loading enters the normal menu.

Three targeted tests cover stalled-resource abort, disposal of a late decoded bitmap, and a manifest timeout resolving to a reported missing-art pipeline failure. The public timing above measures the pre-fix build. Patched loading UX and fresh actual HTTPS behavior still require parent build/browser verification. QA should wait for actual menu readiness separately from navigation rather than using network-idle completion as the game-readiness signal.
