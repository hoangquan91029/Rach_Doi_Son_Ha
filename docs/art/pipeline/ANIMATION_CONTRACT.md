# Animation contract — v1, audit488

## Five layers and authority

| Layer | Reusable inputs/output | Authority / maturity |
|---|---|---|
|Identity|immutable original, selected views, physical equipment, exclusions, layout|Existing identity.json; missing locks remain missing|
|Motion|phase/contact/support/swing/body/tool intents in normalized cycle|Reusable archetype below; numeric per-unit pose constraints still authored|
|Projection|engine octant, ground vector, depth/occlusion, source landmarks|Existing54×27 projection + per-view authoring, never screen-side anatomy guessing|
|Frames|whole original-derived keys, neighbor in-betweens, raw/provenance|Built-in edits are probabilistic; local2D branch unqualified|
|Runtime|compiler descriptor/atlas, fixed pivot, distance/tick clocks, bank|Existing implementations reused; no simulation decisions from art|

**Implemented tools:** `scripts/sprite-prompts.mjs`, `sprite-order-run.mjs`, `sprite-production.py`, `sprite-action-bank.mjs`, `sprite-preview.html`, `qa/sprite-preview.mjs`, `qa/unit-walk-scene.mjs`, `unit-art-coverage.mjs`. Inspect their CLI before invoking; do not invent options.

**Implemented P1 (489):** dispatch requires explicit `jobKind:view` or `jobKind:action`. View has one frame0/phase0 slot and no action/phase prompt values; callLimit≤1. Action binds an exact immutable `registry.jobs` record `{id,action,direction,variant,path,sha256}`. New typed orders do not fall back to currentJob. Historic helpers remain compatible for inspection. `equipmentLock` uses verified/not-applicable/unknown with source/basis; missing master stays unknown. Idle-only N/A allows view/idle/walk, and cannot establish action tools. Source reuse resolves exact job/frame/phase. Root registers common metadata; durable claim still precedes tool. These guards do not create visual acceptance or authorize an order.

## Action matrix

Authoritative applicability and default counts: `shared/unit-action-spec.js`. All applicable clips D0–D7, no mirroring. Standard:idle4,walk8,attack8,hit4,death8,work8,ability6,load8,unload8. Build/repair and villager return aliases are explicit; no new carry/run/charge/deploy. Same leader identity shares common clips across roles; King-only build; ability has its own poses.

Walk phases: F0contactA, F1weightA, F2BpassesA, F3Breaches, F4contactB, F5weightB, F6ApassesB, F7AreachesF0. A/B name physical legs with a persistent landmark; contact starts weight transfer, not an instantaneous support flip. Same normalized phases across directions. Keep natural counter-swing/body bob/cloth; do not freeze the upper body.

## Contact and distance

For ground travel use observed foot contacts in the exact projection, not file labels. Record stance intervals, physical foot, landmark pixel coordinates, world travel vector, source→logical scale and measurement uncertainty. At zoom1, a stance point is `P(worldPosition)+scale*localFoot`. During planted support it should stay approximately fixed.

Candidate stride can be fit from `d*(phaseDelta)*P(normalizedTravel)+scale*(footB-footA)≈0` over actual stance samples of the SAME physical foot, unwrapping phase at the seam. Inspect residual and body rhythm in real movement; perpendicular foot motion cannot be fixed by one distance scalar. Use multiple support samples, not one boot tip. Existing infantry0.15 produces15.33cycles/sec at2.3 and is not production-qualified. Never change game speed to fit bad poses or copy Villager stride into Infantry.

## Events and time

Simulation authority remains unchanged. Walk phase follows traveled distance; stationary ticks don't advance walk. Attack follows committed impact tick; markers are presentation only even if a legacy name is DEAL_DAMAGE. Hit can preempt drawing but cannot cancel already authoritative damage. Death is nonloop,≤4000ms current corpse window, finalpose held until corpse removal, never living-idle fallback.

`shared/visible-action.js` carries sanitized ability/load/unload/build start/end/loop only after successful gameplay action. It does not leak target/cargo/passengers. Continuous build/work loops; finite ability/load/unload/hit/death do not loop; explicit metadata wins. Firearm aim/fire/reload and artillery recoil/recovery are attack phases. Pause/reconnect/background return use bounded game time, not accumulated rAF callbacks. No animation-frame streams over network.

## Packaging and evidence

Keep existing schema2 compiler jobs and runtime schema1 descriptors. Whole raw→working256 and separately raw→runtime128; fixed family canvas/pivot/render/shadow,2px padding, no trim/rotate/per-framefit. Page≤2048;128MiBdecoded/64MiBencoded/2MiBmanifest caps. Larger envelopes need a versioned compiler extension before use.

`ASSET_MANIFEST_SCHEMA.json` is a strict **rds-animation-record/v1 evidence envelope**, not a replacement for runtime fort manifest. `validate-animation-record.py` checks pinned job/descriptor/source/atlas linkage. It does not judge motion. Its current production path deliberately refuses until the trusted qualification/stride adapter is implemented; candidate validation is usable now. Existing compiler production mode remains the existing route and still requires its source-bound qualification. Do not represent a candidate envelope as newly approved art.

Record availability(candidate/selected/held), technical, motion, runtime, owner and release separately. PASS requires nonempty pinned evidence; existence of that evidence still does not establish its truth. Unknown generator/model/time stays null. Mirror source is always null. Source hashes and actual ordered references are immutable. Historical records must not be silently upgraded.

Provenance JSONL starts with a clearly scoped seed, not a claim that all legacy assets are indexed. Coverage counts exact animation/sharedclip/staticfallback/missing/N/A; fallback never closes the required bank. Root controls selection and manifest promotion after independent review.

## Guide-first authoring reference contract492

`guide_key` uses the strict key fields. `guidetarget` must be primary in a typed OPEN action order with `referenceMode:guide-first` and exact `poseGuide` job/frame/phase/provenance pin. Second input is original matching master or selected matching view, preserving identity authority. Registered guide status is authoring-only, derived from original master. `rds-guide-target/v1` binds identity/action/direction/job/frame/phase, originalMaster, appearance, output and sourcePixelUse=false. Hash checks cover actual original/appearance/guide/provenance. `preparePrompt` without an order cannot prepare this route; durableclaim still precedes dispatch. Existing held/excluded/edit-target/view/neighbor safeguards remain.

This metadata proves declared byte relationships only. Actual492ONE trial is HELD for passing/scale; guide-first is implemented but **not motion-qualified**. No new call/production authorization comes from this section.
