# Authoritative action timing receipt

Sections 139–140: simulation attacks now reserve one fixed-tick action slot. At 20 Hz the windups are melee 4 ticks (200 ms), spear/firearm/fort 6 (300 ms), naval 8 (400 ms), and artillery 10 (500 ms). These modest data-owned delays distinguish physical commitment and heavier weapons; they are gameplay interpretations, independent of art availability. Existing cooldown seconds are recovery after impact, rounded up to whole ticks. This deliberately increases start-to-start attack time by the windup; balance needs normal play review.

Starting an eligible strike publishes `attackStartedTick`, `attackImpactTick`, `attackCueKind`, and `attackReadyTick`. A private `pendingAttack` holds the target, origin and committed order. Successful impact retains public timing for late snapshots and sets `lastAttack` to the impact tick. All player/compact snapshots omit `pendingAttack`, including the owner's snapshot. Raster attack elapsed uses `(tick - (attackStartedTick ?? lastAttack)) * 50`, clamped at zero. Art frame events are presentation data only; no browser callback deals damage.

Damage, existing splash rules, death and General defeat occur only at authoritative impact. Impact requires a living, unembarked attacker and enemy target, unchanged committed order/origin, current visibility and current range. Movement and fresh fog precede impact resolution. Accepted new movement/stop/hold/work/transport orders, retargeting, death and embarkation cancel the pending strike. The reserved ready tick survives cancellation. Repeated same-target commands preserve the pending start and impact. Splash retains the existing area-damage semantics around a legal primary impact (it may hit a concealed enemy in that area); primary hidden targets cannot be struck.

Fog is refreshed at fixed tick boundaries and after movement/impact so read-only snapshot frequency cannot change subsequent combat or complete-state hashes. Views still refresh fog for existing direct-state setup callers. No map, logistics, residence, animation asset, runtime event-dispatch or server protocol command changes were introduced.

Validation: existing full suite passed 61/61 before focused additions, including six AI victories, both naval maps, server victory/reconnect, logistics and residence invariants. Focused tests cover absent pre-impact damage, one hit, late timing, dead/moved/stopped/embarked/hidden/out-of-range cancellation, repeated orders and retarget reservation, all-view/compact snapshot privacy, display sampling state invariance, invalid affiliation and delayed splash. Final `npm test`: **68/68 passed**, zero failures, 35.327 s. `git diff --check` passed.

Bounded local Node simulation cost (seed 140, normal AI, actual ordinary army formation, not browser FPS): Delta 3052 ticks, peak 54 living entities, 2587 samples at 40+ entities: p50 0.760 ms / p95 1.218 ms. Coast 3061 ticks, peak 53, 2596 samples: p50 0.717 ms / p95 0.884 ms. These include the extra fixed-tick fog refreshes and are not maximum-density or device performance guarantees.

Production build succeeded (`index-DkM7ieNZ.js`, 133.53 kB; Vite 7.3.7). No service restart, deployment, commit, art modification or finished-animation approval.

## Continuous cosmetic presentation

`client/action-presentation.js` now maintains a clock between received snapshot times, capped at the latest known simulation tick. A 5 Hz online snapshot stream therefore permits intermediate render samples without extrapolating future gameplay. Offline rendering uses the accumulator fraction within the previous-to-current tick interval. Pause, disconnected transport and result freeze cosmetic time; new matches, resumed `start` messages and map/tick resets clear the timeline and impact deduplication. Current snapshot membership, fog, HP, death and result remain immediate. No authoritative object is modified by the clock.

Raster sampling receives `visualTimeMs` separately. Exact authored action tracks default to nonlooping (idle/walk loop), unless the asset explicitly specifies `loop`. One valid contact marker (`DEAL_DAMAGE`, `FIRE_PROJECTILE` or `WEAPON_CONTACT`) maps piecewise from the authoritative start to impact and recovery-ready tick, respecting unequal frame durations and marker offsets. Confirmed `lastAttack` prevents a lagging visual clock from showing pre-impact anticipation. Missing or ambiguous markers use truthful elapsed time; no authored coverage is invented. Death and hit tracks start from their authoritative ticks.

The existing procedural muzzle flash and artillery/naval recoil now use a deduplicated 90 ms pulse triggered only by a known `lastAttack`, with a bounded 500 ms late-snapshot catch-up allowance. Pending future impacts cannot emit it, frozen views suppress it, and reconnect/new-match reset cannot replay an old shot. Other fallback motion uses cosmetic simulation time so it freezes too. These remain existing procedural fallback visuals, not approved raster animation or new VFX art.

Focused pure tests cover bounded interpolation, freeze/reset, offline fractions, snapshot immutability, equal samples across display rates, exact marker offset/late impact alignment, one-shot hold, invalid-marker fallback and pulse deduplication. Presentation build and final test results follow below.

Presentation validation: full `npm test` **72/72 passed**, zero failures, 35.599 s. The subsequent stricter freeze-at-last-sample adjustment also passed all four pure presentation tests. Final production build passed: `index-ClW3IlNb.js` (136.13 kB; 46.13 kB gzip). `git diff --check` passed. No browser art qualification is claimed: current static candidates provide no complete attack loop to review. No server restart, deployment or commit.

## Public deployment acceptance — 2026-10-08

Fresh health reported `rooms:0` before the authorized user-service restart at 02:55:58 +07. Public normal-TLS acceptance completed at 2026-10-07T20:00:13.257Z (03:00:13 +07), serving `index-ClW3IlNb.js`, SHA256 `ca8e6428603c0033ccd9926fdb69daa5d78cee28fef4259607946530fe02e08b`. Final health again reported zero rooms. Compact tracked evidence is [ACTION_TIMING_DEPLOYMENT_RECEIPT.json](ACTION_TIMING_DEPLOYMENT_RECEIPT.json).

Both Delta and Coast passed offline UI play and mixed-engine online reload/reconnect, ordinary combat General defeat, result, consensual rematch and return to menu. Chromium 151.0.7922.34 hosted; Firefox 153.0 was the peer. Chromium used resolver 103.84.155.153; TLS validation stayed enabled. Captured page errors, HTTP failures and server error messages were zero. Existing online scenario wall durations were 36.214 s / 61.082 s, including post-victory checks; these are not isolated combat-duration benchmarks.

The first failed attempt is preserved at `artifacts/production-action-timing-mixed/failure.json`: Delta offline passed, then the host remained in lobby without match state. The existing QA script selected an already-active map and could ready before both browsers received the configuration acknowledgment; configuration resets readiness. The QA script now awaits read-only lobby acknowledgments before readying, records served build/engine versions/current timestamp, and captures timeout screenshots/snapshots. No runtime change or second restart was needed. Passing receipts and inspected victory screenshots are under `artifacts/production-action-timing-mixed/retry-lobby-ack/`.

Limits: both headless engines ran on the same host through the public HTTPS endpoint, not separate external devices. The default presentation mode and existing easy offline scenario were used; this proves ordinary UI/network/gameplay acceptance, not dense-battle performance, art=pilot coverage or finished animation quality. No art/status documents were changed and no commit was made.

## Public pilot human-versus-AI replay — 2026-10-08

One bounded attempt per map with `?art=pilot`, existing easy AI UI strategy and normal authoritative timing passed without retries or strategy/game-code changes. Delta ended at tick 2593 (129.65 simulation s / 129.768 wall s); Coast at tick 2529 (126.45 simulation s / 126.413 wall s). Both produced normal `Enemy General defeated` player victory, verified result-to-menu, and zero captured page errors. Actual victory screenshots were inspected. Compact tracked evidence: [ACTION_TIMING_AI_RECEIPT.json](ACTION_TIMING_AI_RECEIPT.json); full per-second windows/actions/timeline/screenshots: `artifacts/production-action-timing-ai/`.

Chromium 151.0.7922.34 used public HTTPS with normal TLS validation and resolver 103.84.155.153. Both served bundle `index-ClW3IlNb.js` SHA256 `ca8e6428603c0033ccd9926fdb69daa5d78cee28fef4259607946530fe02e08b` and 14-asset manifest SHA256 `4fda8d2ec7f6bb4690a36644bacf2e222b722091905f9cfcc904295fa4e59814`; all 14 assets were ready. Actual runtime asset hashes are retained in the full receipt.

| Map | Combat RAF samples/windows | Combat cadence p50/p95 | Peak viewport entities/military/attacking military | Peak observed-state entities/military |
| --- | --- | --- | --- | --- |
| Delta | 1136 / 19 | 16.7 / 16.7 ms | 30 / 15 / 13 | 53 / 18 |
| Coast | 959 / 16 | 16.7 / 16.7 ms | 32 / 15 / 13 | 54 / 20 |

Viewport counts use living, unembarked ground anchors inside the 1280×800 canvas; they do not measure overlap/occlusion or imply all entities remain simultaneously onscreen. Observed-state counts are fog-filtered and are separate from viewport density. A combat window means at least one viewport military entity in `attack` state. Pure RAF callbacks collect only numeric intervals; sparse read-only snapshots run once per second. Terrain cache built once per map, backing 5,169,280 pixels; last sampled draws were 7745 / 7569. `frameCostMs` is only one sample per second and includes offline simulation step/view as well as synchronous drawing.

These measured scenes were smooth on this headless host and preserve the normal human victory after added windups. They do not establish maximum-density battle performance, external-device behavior, or finished raster attack animation quality. No server restart, deployment update, commit or art change occurred during this validation.
