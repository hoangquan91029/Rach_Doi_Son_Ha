# Project status — 2026-10-07

**NOT COMPLETE under sections81–114. VISUAL GATE FAILED.** This is a deployed playable development build. Do not turn implementation or automated checks into final visual or map acceptance.

Public playtest: https://kieu-hoang-quan-loq-15iax9.tail5247a0.ts.net/
The earlier port-8443 URL also works. Both serve the same production build and authoritative server. The machine must remain awake and connected. Active rooms are in memory and do not survive a server restart.

## Implemented and measured
- Browser menu, local single-player AI, online two-seat room/code/invitation/ready flow, two map choices, twelve King and General choices, result and return flow.
- Shared 20 Hz simulation. Authoritative online server sends fog-filtered snapshots at 5 Hz; clients do not decide damage, resource balances or victory.
- Villager economy, physical food inventories, per-unit rations, wagon loads/unloads/resupply, remote wood/iron delivery, ten buildings and all listed troop/naval types.
- General-death defeat; one residence including an unfinished replacement; no defeat on residence destruction; only surviving King can rebuild; bounded repairs/cancel refunds.
- AI economy, army, General protection, wagon support, shipyard/transport construction, embarkation and coastal landings using normal validated commands.
- Disconnect pause, 60-second resume grace, rotating bearer tokens, expiry/forfeit, consensus rematch, payload/rate/connection limits.
- Development isometric rendering, selection/commands/formation drag/control groups, leader portrait HUD and minimap. Optional raster candidate preview uses the actual simulation; it is not a finished visual slice. Historical portraits use hashed compressed derivatives of supplied originals.

## Current verification
- Automated checks: 48 passing tests, including simulation/server invariants and presentation-only fog/state preservation.
- All 148 original source files unchanged; 96 RGBA directional derivatives verified against hashes.
- Public Chromium: both maps passed single-player browser interactions including running after network loss; both maps passed real two-context online combat, General-death victory, guest reload/reconnect, synchronized results, rematch and return to menu. No browser JavaScript or HTTP errors in these receipts.
- Public Firefox: both maps passed the same single-player and complete online acceptance after the measured/fixed RFC7692 compression negotiation rejection. Receipt: `artifacts/production-firefox/receipt.json`.
- Evidence scripts: `scripts/browser-acceptance.mjs`, `scripts/verify-assets.py`, `scripts/benchmark.mjs`. Production browser captures live under `artifacts/production-*`; artifacts are preserved locally and excluded from Git.
- Both maps completed public HTTPS browser human victories against easy AI through ordinary UI, with General-death results and menu return: delta 121.05 seconds, coast 122.65 seconds, zero page errors. Normal TLS verification was retained. Normal AI defeat checks are also preserved; see `docs/BROWSER_AI_VICTORY.md`. Single-player simulation runs locally after loading; these wins do not by themselves prove online WSS acceptance.
- Mixed Chromium/Firefox public relay matches pass on both maps after presentation changes, including reload/reconnect, synchronized General-death results and rematch; `artifacts/production-presentation-mixed/receipt.json`.
- Synthetic Node benchmark is simulation-only and does not establish browser FPS or maximum match-size rendering acceptance.

## Open critical gates
New visual brief: `docs/visual-quality-requirements.md`; binding art bible: `docs/ART_DIRECTION.md`; unresolved PLACEHOLDER_ONLY debt: `docs/VISUAL_PLACEHOLDERS.md`; parent rejection ratings: `docs/art/VISUAL_AUDIT_001.md` and `VISUAL_AUDIT_002.md`.

Checkpoint: ten raster candidates pass source/runtime packaging; strict final-art approval remains absent. Both bounded villager F04 methods failed and are preserved without runtime integration (`docs/art/VISUAL_AUDIT_003.md`). Known gaps: `docs/KNOWN_GAPS.md`. Compact measured receipts are tracked in `docs/qa/checkpoint/`; full screenshots and failed attempts remain preserved locally in `artifacts/`.

Final candidate smoke: fresh public-relay Chromium and local-production Firefox both loaded ten assets, completed normal paid cavalry production and scouting, and recorded missing motion with zero page errors. The parent reviewed actual normal-zoom captures and retained the visual rejection. Production bundle: `index-D0s8sbeX.js` (122.74 kB, gzip 41.07 kB); 48/48 tests pass.

1. Final major-unit and historical leader visual/motion acceptance. Eight-direction procedural state rigs exist, but they are simplified development art; source static directions are not final animation frames.
2. Both maps need final strategic/layout and gameplay acceptance. Topology works in automated tests; the measured minor asymmetric coast ford was corrected and terrain/resource reflection regressions now pass.
3. Final integrated build must repeat browser acceptance after remaining corrections, record dense-battle render timings, and repeat the measured human-versus-AI win/lose and online flows on that accepted build.
4. Clean Chromium and Firefox peers complete full public HTTPS relay matches on both maps. They are separate browser engines on the same physical host; a separate external device is additional validation, not an already measured result.
5. No known severe desync is demonstrated in completed tested matches, but broader latency/long-match coverage remains required. Durability through server restarts and permanent cloud uptime are not implemented.

## Reproduction
`npm ci`, `npm test`, `npm run build`, `npm start`.
Browser QA: `GAME_URL=https://kieu-hoang-quan-loq-15iax9.tail5247a0.ts.net QA_BROWSER=chromium node scripts/browser-acceptance.mjs` (repeat `firefox`). Browser engines are developer test dependencies only; players install nothing.
Deployment: `deploy/README.md`; network lifecycle: `docs/NETWORK_RECEIPT.md`; Firefox diagnosis: `docs/FIREFOX_WEBSOCKET_DIAGNOSIS.md`; input custody: `docs/leadership-source-hashes.json`.
