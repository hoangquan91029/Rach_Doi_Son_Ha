# Asset production and reuse audit — 488

Independent role C; model `gpt-6.1-sol`, reasoning `low`; 2026-10-12. Owned output: this report only. No code, assets, manifests, orders, production services or runtime settings were changed. No tests, builds, browsers, image calls or installations were run. Verification was read-only source inspection and Node arithmetic/JSON aggregation. Evidence labels below separate actual source facts from proposals and estimates. Confidence is high for counts and inspected guard behavior; visual quality, authoring effort, failure rate and dense browser performance remain unmeasured here.

## Scope and current production state

The initial reusable roster is nine ordinary identities plus twelve historical leader identities, not separate King and General artwork for the same character. `shared/unit-art.js:4-9` selects a leader by `entity.character`; `shared/unit-action-spec.js:3-17` defines shared combat/ability artwork across King/General roles and King-only build. Ability, load and unload require their own action poses. Repair aliases build, villager resource-return aliases ordinary walk, and destroyed/sink alias death. No additional gameplay actions or 576 duplicate leader-ability frames are needed under this contract.

| Claim | Status and source | Method / observed result | Remaining uncertainty |
|---|---|---|---|
| 21 identities, 135 identity-action banks, 1,080 directional clips, 7,104 required frame positions | VERIFIED; `shared/unit-action-spec.js:3-17`, identity JSON files under `docs/art/pipeline/unit-production/` | Read directory registries, apply `identityActions()` and sum `8 × ACTION_FRAMES[action]`; 21/135/1080/7104 | These are authored targets, not completed assets or image-call counts. |
| Current source coverage is 3 exact animations, 397 static fallbacks and 680 missing applicable slots | VERIFIED; `scripts/unit-art-coverage.mjs:20-31`, `public/assets/art-v1/fort-202-manifest.json` | Imported pure `coverage()` and supplied current source as both inputs without invoking writing CLI; same 1080 applicable / 7104 target. Exact animations: villager walk D1, gather_wood D1, gather_iron D1 | Presence of multi-frame loops does not prove naturalness, full-action approval or public identity. Public comparison was deliberately not performed by that call. |
| 11 non-null views across 10 identities; zero views marked selected | VERIFIED; 21 `identity.json` registries; assembler guard `scripts/sprite-action-bank.mjs:44-46` | Aggregate `views[].source` and exact `status === 'selected'` | Existing original/static references are retained custody, not eight-direction authoring permission. A future validated selection is needed. |
| Warship and ten leader world masters are absent | VERIFIED; registry `master` fields | Null masters: warship, han_xin, le_thanh_tong, ly_thuong_kiet, minh_menh, napoleon_bonaparte, nguyen_anh, nguyen_hue, nguyen_phuc_chu, trinh_cuong, xiang_yu | Portrait libraries do not complete missing world-body identities. |
| 19/21 identities have null physical equipment ownership | VERIFIED; registry `weaponOwnership`; `scripts/sprite-prompts.mjs:35` | Aggregated null fields; only two non-null locks. Preparation rejects missing/mismatched ownership | This may describe tools, rider/vehicle parts or empty hands, not merely weapon hands. Locks must be explicitly reviewed per identity. |
| Built-in image calls have durable finite-slot custody | VERIFIED implementation; `scripts/sprite-order-run.mjs:9-41` | Source inspection: exclusive ledger lock, expected SHA, durable consumed claim, token-bound held-only settlement | No execution here; this protects dispatch custody, not artistic success or final selection. Unknown claims must not be reset on elapsed time. |

The current contact repair remains unsuccessful. `docs/art/pipeline/infantry-F4-target-edit-486/CHECKPOINT.json:2-16` records one authorized trial closed HELD, no world-contact approval and an uncalled target-first reference fix. This is DOCUMENTED_ONLY as a retained receipt in this audit, not a fresh visual review. Orders 482/483/486 must not be reopened or copied to reset exhausted authorization. Production should resume only under the parent-approved next prerequisite and current user scope.

## Scalability defects before generation

**VERIFIED source mismatch; high confidence:** the `view` field contract excludes `action` (`scripts/sprite-prompts.mjs:5-10`; `templates/view.txt:1-8`). The finite-order contract requires `order.action === values.action` and a valid action frame count (`sprite-prompts.mjs:66-74`), while `prepareOrder()` then calls `preparePrompt()`/`renderPrompt()` (`:79-85`). Omitting action fails the finite guard; including it is rejected as an unexpected view placeholder. Consequently the current view preparation/claim path cannot complete through these combined contracts. This is a source proof, not an executed failing test. PROPOSED: give view authoring an explicit finite operation contract, or reconcile an explicit action field across both contracts, with isolated validation before any claim or call.

**INFERRED concurrency limit; high confidence:** selected neighbor validation loads a single `registry.currentJob` and checks job ID, action, direction and frame (`scripts/sprite-prompts.mjs:52-56`; infantry registry `currentJob` at `identity.json:258`). Two different simultaneous action/direction jobs using neighbor references cannot both match this one binding. PROPOSED: immutable job records keyed by job ID/action/direction, validated against the registered order; preserve all selected/held historical custody. Do not weaken reference checks to gain parallelism. Disjoint identities remain the safer scheduling boundary until this is implemented.

The pipeline already separates original identity and directional masters (`sprite-production.py:85,115-118,136`) and portable bank assembly (`sprite-action-bank.mjs:23-73`). It checks eight selected views/clips, exact custody, fixed family layout, events, explicit loops and held-source exclusions. Preserve these mechanisms. Template reuse currently reuses motion intent, camera, ownership and contracts; it does not establish that different bodies/equipment can reuse the same finished pixels.

## Mathematically verified production sizes

Frame counts below are **PROPOSED presets**, not implemented runtime settings. Standard matches `ACTION_FRAMES`; Low/Premium were supplied for audit comparison. Every applicable action retains all eight authored directions. No mirroring, static substitutions or role duplication is counted.

| Preset | Idle / walk / attack / hit / death | Each gather/build | Ability | Each load/unload |
|---|---|---:|---:|---:|
| Low | 2 / 6 / 6 / 2 / 6 | 6 | 4 | 6 |
| Standard | 4 / 8 / 8 / 4 / 8 | 8 | 6 | 8 |
| Premium | 6 / 12 / 12 / 6 / 12 | 12 | 8 | 12 |

| Identity set | Actions | Directional clips | Low positions | Standard positions | Premium positions |
|---|---:|---:|---:|---:|---:|
| One villager | 9 | 72 | 368 | 512 | 768 |
| One infantry/spearman/firearm/cavalry/artillery/warship | 5 | 40 | 176 | 256 | 384 |
| One wagon or transport | 6 | 48 | 224 | 320 | 480 |
| One leader identity shared across King/General | 7 | 56 | 256 | 368 | 544 |
| All 9 ordinary + 12 leader identities | 135 | 1,080 | 4,944 | 7,104 | 10,560 |

VERIFIED arithmetic: combat per direction = idle+walk+attack+hit+death; villager adds four work actions; each leader adds one ability and one build; wagon/transport omit attack and add load+unload. Full total = villager + six ordinary combat identities + two transport identities + twelve leaders. A single King-role identity uses the seven-action row. A strictly General-only subset excludes build and would be 208/304/448 positions, but that subset does not replace the full shared identity bank.

These numbers estimate final accepted frame positions, not independent PNGs, number of built-in calls, hours or money. Source masters, selected directional references, key/pose guides, corrections, rejected outputs and effects are additional authoring work. A reference can serve multiple qualified purposes; an output may be held or contain multiple usable candidates. The actual yield is UNKNOWN. No per-call price or retry distribution was supplied or measured. For a future measured pilot, record actual calls, held outputs, accepted positions, elapsed hands-on time and correction causes; only then derive accepted positions/hour or cost. Multiplying positions by a guessed API price would be unsupported.

## Memory, resolution and browser limits

| Quantity | VERIFIED calculation / inspection |
|---|---|
| Current canonical source manifest | 51 assets, 41 unique runtime path+SHA images; 19,301,888 decoded RGBA bytes; 4,608,899 encoded file bytes |
| Low target at padded 132×132×4 slots | 344,577,024 bytes = 328.61 MiB |
| Standard target at padded slots | 495,120,384 bytes = 472.18 MiB |
| Premium target at padded slots | 735,989,760 bytes = 701.89 MiB |
| Runtime budgets | 128 MiB decoded; 64 MiB encoded; `client/art-assets.js:53-58`, `client/art-bank.js:3-6` |
| Current compiler | 128 square runtime cell, padding 2, atlas ≤2048; `scripts/sprite-production.py:52-56,100-114,129-136` |
| Real launch zoom | 1.68; `client/world-presentation.js:4`, `client/main.js:51`; constructor zoom 1 is not final launch zoom |

Method: deduplicate canonical manifest runtime entries by path+SHA; sum width×height×4, and `fs.statSync` encoded file sizes under `public/assets/art-v1/`. This is a source-file inventory, not live public451 verification or observed browser allocation. Unique images include individual images as well as atlases. RGBA estimates exclude canvas/GPU copies, browser overhead and retained encoded bytes. Padded target figures exclude page slack and all non-unit art. Compression ratio for future animation pages is UNKNOWN; current still-image compression must not be extrapolated as a guarantee. Even Low exceeds the decoded budget if loaded all at once.

PROPOSED: qualify bounded match-specific/deferred working sets before roster promotion; page by identity/action/direction as justified by actual active use. Preserve original same-identity idle behavior during cold/error loading and protect active pins. Deferred loading/LRU code does not by itself prove a full-roster dense-scene budget. Profile actual retained pages, concurrent requests, encoded retention, GPU/canvas overhead, loading time and ordinary gameplay in both browsers and rooms only at the later permitted qualification stage.

The compiler currently forces square source canvas, 128-square cell and equal logical render width/height (`sprite-production.py:50-56`), and bank locks require the existing family geometry (`sprite-action-bank.mjs:58-64`). Larger spears, wagons, ships and ability motion may require wider/taller bounds, but clipping was not measured by this audit. PROPOSED: retain existing family locks; extend the schema/compiler/assembler/runtime together only for a demonstrated clipping or wasted-memory case, preserving a fixed pivot and fixed bounds for each clip/bank. Do not perform a blind rectangular rewrite or per-frame fit. At render size 42 and zoom 1.68, the whole canvas displays at 70.56 px; alpha margins mean that is not body height. Inspect useful silhouette and motion at the real launch zoom before choosing source resolution or larger cells.

## Production-method comparison

All comparisons are **INFERRED qualitative tradeoffs**, supported by inspected guards and failed-order receipts; no method benchmark, price, acceptance-rate advantage or browser-speed difference was measured. Browser cost depends on final exported pages and working set, not whether the illustrations originated in a rig or an image edit.

| Method | Identity / motion consistency | Reuse and eight-direction scale | Cost and automation implications | Recommendation |
|---|---|---|---|---|
| A. Independent generated PNG frames | Highest drift/contact risk when each description is unrelated; requires repeated identity and phase checks | Prompt reuse is easy; finished-frame/body continuity remains weak | Easy dispatch automation, unknown correction yield; provenance still mandatory | Avoid as the default production method. |
| B. Canonical whole illustration + controlled keyframes and in-betweens | Pinned original and selected neighbors constrain identity; prompt control alone has not solved infantry leg exchange | Reuse phases/contact intent/camera, then adapt equipment and silhouette per identity and direction | Existing templates/compiler fit this path; failed contacts create an early bottleneck | Preferred framework, contingent on one physically correct qualified pilot. |
| C. Temporary pure 2D whole-pose/joint guide followed by complete illustration | More explicit intended pose; the final illustration may still ignore or misread guidance | Reusable motion skeleton/phase specification, body/equipment-specific anchors | Guide tooling may reduce ambiguity but setup and yield remain unknown; 483 complete guide was held | A demonstrably different permitted control can be evaluated under a new authorized finite order; do not claim it proven. |
| D. Layered animation and image warping | Can hold appearance but risks cloth/anatomy distortion and puppet seams | Easy transformation reuse, difficult natural equipment/occlusion across views | Technically automatable; repair work and acceptance unmeasured | Current project restrictions exclude warp, limb cutouts, source pixel splicing and puppet seams; not an authorized final production path. |

A hybrid selects permitted whole-illustration controls by archetype, not a fifth proven technology. Humanoid contact plans can inform villager/infantry/spear/firearm/commander motion; horse-and-rider, artillery crew, whole wagon assembly and ships need independent equipment/contact plans. Preserve canonical identities and complete horse/cart/harness/cargo. Never transfer a finished leader body, handed weapon, or supporting-leg label merely because motion timing is shared.

## Practical staged recommendation

1. Parent consolidates audits and resolves the view/finite-order contract, equipment locks and immutable per-job reference binding before opening directional production orders. This audit authorizes no calls.
2. Retain current original references and failed-order custody. Establish the next permitted contact/control prerequisite. Then qualify one same-original whole-body pilot at real game size, with one brief loop and only visible fixes; schema success is insufficient motion evidence.
3. Demonstrate reuse on a second identity using the same motion definition and identity-specific equipment/anchors. Record actual effort/yield so the reuse benefit becomes measurable.
4. Author and independently select eight views, then finite action-direction clips. Package candidates with existing compiler/assembler contracts. Independent visual review, runtime behavior and owner acceptance remain separate from custody or packaging.
5. Qualify dense bounded working sets before default policy or paired frontend/backend release. Source manifests and local candidates do not change immutable public451/backend230. Final RTS roster, building states, maps, WAN and public modes remain outside the completion of this audit.

The immediate bottleneck is reliable whole-body pose/contact control plus missing production locks, not a shortage of atlas export code. Scaling image calls before those prerequisites would increase held-output inventory without establishing accepted motion.
