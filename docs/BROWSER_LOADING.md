# Browser loading and recovery — 7 October 2026

**Development build; final visual acceptance remains absent.** Production loading now shows artwork progress and provides bounded failure/retry recovery. This does not establish a fast load on arbitrary networks.

## Measured public transfer

The first thirteen-candidate public smoke timed out at its 30-second `networkidle` wait while the static boot screen remained visible. No page error or failed request was recorded. The original failure remains at `artifacts/art-v1/gradient-thirteen-public/`.

A fresh measured HTTPS retry with normal certificate verification reached the menu at 31.232 seconds. The document arrived around 1.01 seconds, bundle around 1.739 seconds and manifest around 2.33 seconds. The largest Residence raster kept its four-resource batch waiting until 21.281 seconds; later batches finished around 30.803 seconds. This supports slow relay raster transfer plus batch barriers, rather than a JavaScript initialization failure. Exact request timings and limitations remain in `artifacts/performance/public-loading-retry/receipt.json`.

The source Residence PNG remains unchanged. A new lossless WebP derivative resizes the entire 1254px canvas to 512px with Lanczos, retains the same source-coordinate pivot and 130px logical render size, and reduces runtime transfer from 1,250,654 to 229,022 bytes. The previous runtime remains preserved. `docs/art/residence/variant-02/runtime-512-provenance.json` records both hashes and decoded pixel custody. The source-to-runtime validator passes; low-alpha fringe warnings remain candidates, not final margin approval.

After these changes, one fresh public Chromium smoke reached menu at 24.934 seconds, loaded all thirteen candidates, trained cavalry and scouted normally, with zero page errors or failed requests. TLS1.3 was verified against the public hostname; the browser connected to relay103.84.155.153:443 without certificate bypass. Receipt: `artifacts/art-v1/loading-fixed-thirteen-public/receipt.json`. These two samples are not a controlled network benchmark; only the byte reduction is deterministic. Ground-cache counters after real camera movement were one build, 2,591 draws and 5,169,280 backing pixels.

## Recovery behavior

`client/loading-deadline.js` covers fetch, response body, digest and decode. Per-resource deadlines are30seconds, with a60second total preload budget; a late bitmap is closed instead of entering the loaded set. Existing four-way batches, runtime SHA checks, path restrictions and candidate rejection remain intact. Boot shows checked/total artwork counts, retains truthful errors and offers Retry or explicitly labeled development placeholders. A20second pre-main watchdog offers Retry if the game bundle cannot initialize. Successful default development loading still enters the menu normally.

Three targeted automated deadline tests pass; the full suite has57passes. Actual browser network fixtures also pass: a503manifest shows a visible error, explicit development continuation starts a match with zero approved assets, recovery loads thirteen candidates, and a failed bundle shows the watchdog before a successful Retry. Evidence: `artifacts/loading-recovery/receipt.json`; these are controlled failure fixtures, not ordinary production failures.

Browser smoke navigation now waits for DOM readiness, then for the visible menu within a75second bound that includes the client's own recovery window. It records actual menu time, transport and errors. Increasing that test bound is not reported as a loading performance fix.
