# Project status — 8 October2026

**NOT COMPLETE under sections81–145. Final visual gate FAIL.** This is a deployed playable development build, with fourteen unapproved raster candidates. Implementation and automated checks do not establish final art or map acceptance.

Public playtest: https://kieu-hoang-quan-loq-15iax9.tail5247a0.ts.net/ . Port8443 serves the same build; `?art=pilot` opens candidate art. The host must remain awake/connected. Active rooms are in memory and do not survive server restart.

## Implemented

- Browser loading/retry, menu, local human-vs-AI, online two-player room/code/invitation/ready flow, two maps, twelve King and General choices, victory/defeat, return and consensus rematch.
- Shared20Hz simulation; authoritative online server sends fog-filtered5Hz snapshots. Clients do not decide damage, resources, consumption or victory. Attack windup/impact/recovery uses fixed ticks, private pending targets and validation at impact; cosmetic clock and authored marker sampling follow simulation.
- Villagers/resources, physical food inventories, rations, Granary/depot/wagon resupply, remote wood/iron transfer, building/army/naval production and terrain/fog/combat mechanics.
- General-death defeat. Single residence including unfinished replacement, residence loss does not cause defeat, only surviving King can rebuild, bounded repairs/refunds.
- AI economy/army/General protection/wagon support/naval transport and coastal landing using ordinary validated commands.
- Disconnect pause,60second reconnect grace, rotating tokens, expiry/forfeit, payload/rate/connection limits.
- Development dimetric rendering, selection/commands/formations/control groups, leader portraits and minimap. Historical derivative custody retained. Procedural rigs and static raster candidates remain development art.

## Current evidence

72/72 Node checks pass; production bundle `index-ClW3IlNb.js`,136130bytes, SHA256`ca8e6428603c0033ccd9926fdb69daa5d78cee28fef4259607946530fe02e08b`. All148original leadership files remain preserved;96directional RGBA derivatives are hash verified.

Public mixed Chromium151/Firefox153 peers passed ordinary combat, General-death victory, guest reload/reconnect, results, rematch and menus on both maps after authoritative windup implementation, with normalTLS and zero captured errors. See `docs/ACTION_TIMING_DEPLOYMENT_RECEIPT.json`. Earlier original Firefox compression diagnosis and public receipts remain preserved.

Both public candidate easyAI matches won normally and returned to menu after the cadence change: Delta129.65simulationseconds and Coast126.45seconds, zero pageerrors. CombatRAF p50/p95 measured16.7/16.7ms, viewport military peak15/attacking13. This is modest combat in this headless environment, not dense/max-load or hardware-independent FPS acceptance. See `docs/ACTION_TIMING_AI_RECEIPT.json` and `PERFORMANCE_DIAGNOSIS.md`. Static ground cache stays below8million backing pixels and leaves fog/entities dynamic.

One additional publicDelta mixed-engine flow passed with ordered90ms application-message hold eachdirection (nominal180ms addedroundtrip):546send-API forwards, ordererrors0, captured errors0, realreload/reconnect, ordinary combat result, consensus rematch and both menus. First harnessclose-overtaking failure is preserved; narrow QA-only closeordering fix passed. NormalTLS and exactpublic bundle pinned, finalhealthrooms0. This does not emulate WAN packets or certify external-device/long-match/max-load/desync coverage. See `docs/ACTION_TIMING_DELAY_RECEIPT.json`.

Loading recovery and source-preserving Residence derivative, prior candidate smoke, AI win/lose and mixed-peer receipts remain in `docs/BROWSER_LOADING.md`, `BROWSER_AI_VICTORY.md`, `NETWORK_RECEIPT.md`, `docs/qa/checkpoint/` and local `artifacts/production-*`. Final accepted-art build must repeat acceptance.

## Current art boundary

Eight1254RGBA static villager identity views are sealed for South authoring only in `docs/art/VILLAGER_IDENTITY_LOCK_007.json` and byte-bound parent `VILLAGER_IDENTITY_REVIEW_007.json`. Every native/fixed38 image plus combined627/38 sheets was inspected. Fixed authored root6541140, whole-canvas38scale, screenSouth=D01/worldSE. HeldEast/RGBSE, alpha-repairedSE, originalwrong-labelv1 and correctedv2 guides remain preserved. No character mirroring or simulation-heading changes.

Four actual walk sources exist: selected F0 contact candidate and three held F2 attempts; zero complete/qualified loops. The correct LEFTsupport ownership and lifted RIGHT foot did not produce the necessary stance-foot retreat under body. One correction omitted its required annotatedguide; input custody discloses this. Final exactthree-input test attached the guide and still missed support track (sole1198 versus1130–1140target). All guided whole-character calls are stopped, noF4/in-betweens/fanout. Sources/prompts/inputlocks/parentreviews and live `walk/selected-keys.json` are preserved in `docs/art/motion/authoring-tools/villager-walk-SOUTH-007/`. Static lock's zero walk count records its immutable seal-time.

The user-selected persistent2D rig now has a parent-reviewed preparation contractv2:9original textures, separately controlled shin/foot semanticmeshes, per-pose depthorder, immutable source calibration and declared fixed-camera foreshortening. Originaldraft is preserved. Actualcomponents0, paidcomponentcalls0 authorized, finishedbakedkeys0. Natural source landmarks/calibrations remain unknown until actual originals are inspected. Current tool preparation is an internal authoring step, never final illustration/motion approval. Sections115–145 require complete illustrated cels/atlases, fourfinishedkeys first, then exactly8Southframes with sheets, normal/gridloop, all ratings≥8 and LegPhase10, plus independent motion review before other directions/actions. See `docs/art/SOUTH_WALK_RESTART_007.md` and `docs/FRAME_ANIMATION_REQUIREMENTS_115_145.md`.

## Open critical gates

Final major-unit and historical leader eight-direction state/motion acceptance remains absent. Final illustrated attack/hit/death/ability/work/transport events and visual slice are unfinished;14candidates have no final-art approval. Both maps require final authored visual/strategic/gameplay acceptance. Dense battle, long-match/high-latency coverage, separate external physical device and full final-build acceptance remain open. Current matches do not prove absence of desync under all conditions. Service restart durability/permanent cloud uptime are not implemented.

Binding visual brief `docs/visual-quality-requirements.md`; art bible `docs/ART_DIRECTION.md`; placeholder debt `docs/VISUAL_PLACEHOLDERS.md`; rejection audits `docs/art/VISUAL_AUDIT_001.md`/`VISUAL_AUDIT_002.md`; remaining gaps `docs/KNOWN_GAPS.md`. Preserve original leadership, every held/rejected candidate and raw custody.

## Continuation and reproduction

Existing `continue-r-ch-i-s-n-h-after-reset` heartbeat remains ACTIVE every5hours. It checks live quota and resumes this chat when permitted, quietly when unchanged; this is not an exact reset webhook. Near quota, master37 requires completing only the current atomic task, verifying/preserving and committing a resumable checkpoint. Current boundary is in `docs/CHECKPOINT.md` and `NEXT_STEPS.md`; the full objective stays unfinished.

`npm ci`, `npm test`, `npm run build`, `npm start`. Browser QA: `scripts/browser-acceptance.mjs` and `browser-ai-winning.mjs`; delayed run sets `QA_WS_DELAY_MS=90`, `QA_MAP=delta`, `QA_OFFLINE=0`, mixed engine flags. Players install nothing. Deployment instructions `deploy/README.md`; source custody `docs/leadership-source-hashes.json`.

Near-quota94% checkpoint: persistent rig preparation contractv2 and gated preflight/planner are saved;7targeted NON_ART numerical/custody checks pass. Rasterbaker explicitlyUNIMPLEMENTED, actualcomponents0/bakedkeys0/qualifiedloops0. Bothagents finished, nopaidcallpending. Next window finishes mesh/calibration validation and articulatedrasterbaking before a separateONEcore-original pilot order; no blind9partcalls ormoreguidedF2. Parenttoolreceipt `docs/art/motion/authoring-tools/villager-walk-SOUTH-007/pose-rig-south-v1/parent-tool-review.json`. Fivehourcontinuation remainsACTIVE.
