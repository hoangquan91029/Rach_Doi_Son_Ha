# Architecture

`shared/data.js` holds balance, character/tag synergy, terrain, unit, building and map definitions. `shared/sim.js` is the pure fixed-step simulation shared by Node and browsers. Authoritative `command` validates intent/ownership/costs/terrain; `step` mutates at 20Hz; `view` filters visibility; `hashState` supports reproducibility checks. Single-player executes locally; online executes only on server.

`server/index.js` hosts production static client and same-origin WebSocket `/ws`. In-memory two-seat rooms, cryptographic resume tokens, ready gate, lifecycle, reconnect grace pause, timeout forfeits, rematch consensus, cleanup and bounded payload/rate handling. No account is needed. A process restart loses active rooms; durable restart recovery is not yet guaranteed.

`client/main.js` owns menu/config/lobby/HUD/input and local fixed-tick accumulator or online snapshots. `client/renderer.js` draws an isometric battlefield/minimap and separate animation/camera logic; presentation does not decide online combat. `client/style.css` owns responsive DOM layout.

Food inventory is physical in `entity.cargo.food` for buildings/wagons. Rations are per unit. Wood/iron carried to residence/depot credit the central stockpile. Food delivery/resupply transfers finite quantities, never creates an unlimited aura. The player's economy pool used for training is distinct from remote frontline food inventories; exact transfers must remain conservative.

Nav grid tile terrain and authored maps support ship/land domains, fords, passable gates, blocking buildings, supply and alternate routes. Ship transport has cargo.units. Every action remains subject to simulation validation regardless of UI affordances.

Original leadership inputs are excluded from Git to avoid duplicating 207 MB; source hashes and selected compressed outputs are tracked. All originals remain untouched at their supplied paths.

## Candidate raster and presentation pipeline

`client/world-presentation.js` holds the single shared 54 × 27 / 1.08 presentation scale; simulation coordinates remain unchanged. `client/art-assets.js` validates manifest camera/layout/custody, fetches and verifies encoded SHA-256, decodes bounded raster memory, and selects exact states/directions. `client/raster-slice.js` is enabled only by `?art=pilot`. It draws world-anchored materials and authored candidates in the real match. Missing states stay explicitly PLACEHOLDER_ONLY; no idle-as-walk or mirrored direction substitution is allowed.

`scripts/validate-art-assets.py` verifies source/runtime encoded and decoded hashes, exact full-canvas resize/copy derivation, alpha margins, cells, pivots and family consistency. Candidate fringe warnings do not satisfy strict release checks. `public/assets/art-v1/manifest.json` is CANDIDATE and contains no final approvals.

`client/visual-picking.js` samples actual candidate alpha for invisible selection masks and uses development body bounds for procedural placeholders. `window.rtsDiagnostics.entityPoint(id)` is a read-only shown-body coordinate for browser QA. `client/presentation.js` interpolates only positions between online snapshots; it never adds entities absent from current fog-filtered state, changes simulation coordinates, or delays death/embarkation/reconnect jumps. HUD, damage, resource balances, commands and victory still use current authoritative state.

`client/terrain-cache.js` caches only static ground in a surface bounded to 8 million backing pixels. Exact terrain content, material identity and output quality invalidate it; camera panning reuses it. Fog, resources, props and entities remain dynamic. `client/terrain-transitions.js` caches bounded original-material gradient patches along known water/ford/land boundaries; these invisible masks do not change navigation or reveal unknown cells. Final fog still draws above the world.

Art acceptance is separate from technical tests. See `docs/ART_DIRECTION.md`, `docs/VISUAL_PLACEHOLDERS.md` and the parent visual audits. The candidate manifest has fourteen assets, including distinct ford/shore materials, three forest profiles and exact idle Residence/Granary art. Shared full-canvas foliage derivatives retain a common cell and pivot. Failed motion leases remain outside runtime. The game is not visually complete.

## Finished-frame authoring and timing

Sections115–145 require complete illustrated frames at runtime. Internal rigs/IK/mannequins are authoring tools only. D00-006 raw components and partials are byte-preserved under`docs/art/motion/superseded-authoring/`; no runtime bones or completed motion were integrated. South007 uses screenSouth=engineD01/worldSE, one1254canvas, sourcepivot6541140and38pxwholecanvas presentation scale. Its static reference is a candidate; eight-view identity lock remains incomplete.

`client/sprite-timing.js` performs pure millisecond-based variable-duration frame sampling; `client/art-assets.js` exposes elapsed time and detached optional event markers. Browser/Python validation checks marker names and offsets. Markers are presentation data with no gameplay callbacks. Authoritative20Hz simulation still owns attacks/resources/food/movement/victory. Attacks reserve start/impact/recovery ticks and validate living targets, current visibility/range and unchanged commitment at impact. Snapshots omit private pending target data. `client/action-presentation.js` provides bounded interpolation/freeze and known-impact pulse deduplication; one authored contact marker aligns to server impact without gameplay callbacks. Finished attack/transfer artwork remains open; see `docs/ACTION_TIMING.md`.

The preserved standalone South atlas authoring compiler requires byte-bound eight-view identity and four-key review, complete whole-character originals, fixed canvas/pivot and finite8-frame phase/timing declarations. It computes uniform4x2atlas rectangles, source/cell pivots, durations and contact markers; outputs remain review-only. Six NON_ART fixtures check custody/packing/refusal, not visual quality. It refuses overwrite and missing identity gates. No actual South walking frames or accepted atlas exist.
