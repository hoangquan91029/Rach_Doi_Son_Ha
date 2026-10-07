# Persistent D00 rig adapter — proposal/tooling only

The sprite-production controlled-parts skill authoring guidance applies. The user selected this method; original core and arm components are arriving; no full animation loop, independent motion verdict or runtime integration exists yet. Four diagnostic tests verify positive uniform transforms and refusing missing original art. They are not a moving proxy or motion proof.

The master is visually inspected and byte-pinned in `../adapter-locks.json`. Use only genuine newly authored components following `../contracts/component-contract.md`; never master cutouts, rejected body frames or geometric substitutes. Scale is exactly **38/1254 for the whole canvas**, not 38 pixels fitted to visible bounds. Source PNGs and their byte/RGBA custody never change.

## Original component intake

Contract order ID → tooling slot:

- `core_head_torso_pelvis` → `core`
- `arm_far_upper`, `arm_far_forearm_hand` → `far_upper_arm`, `far_forearm_hand`
- `arm_near_upper`, `arm_near_forearm_hand` → `near_upper_arm`, `near_forearm_hand`
- `leg_far_thigh`, `leg_far_shin_wrap`, `foot_far_sandal` → `far_thigh`, `far_shin`, `far_foot`
- `leg_near_thigh`, `leg_near_shin_wrap`, `foot_near_sandal` → `near_thigh`, `near_shin`, `near_foot`

Each sidecar has `original` (relative immutable PNG path), `sha256`, `rgbaSha256` (decoded RGBA bytes), `dimensions`, tooling `slot`, contract `orderId`, `landmarks` (named natural raw-pixel points), and `inspection` with named `actor`, actual `method`, uncertainty description and `status: TECHNICALLY_USABLE`. The current rough master landmark hypotheses are not measured component sidecars. Unknown coordinates remain unresolved and cannot render. Explicitly authored hidden attachment hypotheses may render for prototype only when actor, method, uncertainty and parent preliminary calibration are retained; they must never be relabeled measured anatomy. The core hip hypotheses each retain ±60 raw-pixel uncertainty.

`rig.json` declares `canvas:[1254,1254]`, `root:[650,1140]`, `direction:D00`, numeric `scale:38/1254`, `strideWorldTiles`, `cycleDurationMs`, and eleven `parts`. Each part provides `sidecar`, one fixed positive `scale`, raw landmark `anchor`, persistent `joints`, and for articulated segments a raw landmark `distal` plus fixed source `length`. The length must equal measured raw landmark distance times the single static scale. `core.attachments` maps both shoulder and hip joint IDs to measured natural core landmarks. `core` and feet use a fixed raw anchor plus per-frame authored rotation in radians; limbs derive angle from their constant-length articulated endpoints. No part receives per-frame scaling, reflection, crop or fitting.

Declare one `drawOrder` of all eleven slots and preserve it through the loop. Both thighs must overlap under the tunic/core. Far arm is behind core, near arm in front; near/far ownership cannot swap to fake contact.

## Authored pose tracks and outputs

Declare `frameCount:24` and twenty-five `frames`: twenty-four rendered frames plus explicit frame0 seam closure. A configurable multiple of eight (at least16) is supported. Use eight authored contact/down/passing/up keys, evaluated at24 samples over nominal800ms for initial review. Each has consecutive `index`, `phase:index/frameCount`, unchanged reference `root`, actual named source-space `joints`, and `angles` for core and both feet. Key phase0 supports near; phase0.25 is `near_support_far_passing`; phase0.5 supports far; phase0.75 is `far_support_near_passing`; phase1 closes all joints and rigid-part rotations. These are actual distinct whole-body poses after parts arrive, not labels attached to an unchanged standing picture. Author knees, elbows, ankle roll, foot clearance and body support with fixed limb lengths; retain full character identity and height.

Preflight rejects missing originals/custody, missing natural anchors, bone stretch, attachment drift, absent authored rotations or failed seam. It does not assess anatomy, plausible support timing or visually believable contact: those require real loop review.

Commands after actual part intake and authored poses:

```
python3 tools/rig.py preflight rig.json
python3 tools/rig.py assemble rig.json --out rendered
node tools/render.mjs rendered
```

The assembler embeds byte-identical original PNGs in a fixed1254 SVG using only static calibration and articulated rigid transforms. It draws no visible skeleton or proxy. Browser PNG rendering uses fixed1254 viewport/DPR1 and transparent canvas; whole-body frames retain identical root/source scale. The render receipt pins rig input and every original/output hash. Twenty-four whole-body PNGs plus timing and custody sidecars are the independent review input; no runtime filenames or manifest are assigned here.

## Actual parts, partial diagnostics and stride reach

`partial-assemble` accepts a single explicitly `PARTIAL_NOT_MOTION` pose containing only available genuine painted components. It draws no placeholder missing arms/legs, and preserves full1254 canvas/root38/1254 scale. It must not be mistaken for a whole-body walk. Current actual partial rigs/diagnostics are at `../partial-core-far-arm.json`, `../partial-core-far-arm-hand.json` and matching `../diagnostics/` directories. Core uses the parent-accepted fixed uniform0.62 scale and translation(250,31). Limb calibration is separate and immutable per component; core scale does not apply to every original.

`support_tracks.py` provides numeric two-bone IK with persistent pole ownership, alternating stance/swing offsets and a conservative reachable-stride search. It rejects unreachable targets rather than stretching bones. No length, hidden pivot or rendered motion is fabricated from these helpers. Only actual measured raw endpoint distances and one accepted per-component uniform calibration supply limb lengths. Whole-loop review judges whether core authored hip hypotheses cause visible issues.

Stride remains **unset** until the actual fixed-length legs and source-space foot/contact track define a reachable range. Cap reach below full extension, preserve knee flexion, and inspect real sole contact before recording `strideStatus:REACHABLE_CONTACT_HYPOTHESIS`. Nominal800ms review timing does not imply1.68 tiles of travel or require any prechosen world stride. If reachable source stride is S pixels along the D00 projected direction, world stride hypothesis is `S*(38/1254)/hypot(27,13.5)`; actual rendered contact geometry must confirm it.

Eventual playback advances from actual displayed displacement: `phase += hypot(dx,dy)/strideWorldTiles`. D00 east projects to(27,13.5) logical pixels per tile. A planted stance foot's local offset must counter projected entity movement so its world position remains fixed. Alternating real legs/support and articulated knees create locomotion; whole-body source translation is not motion. A reviewed authored body bob may follow support transfer while the shared reference root remains fixed.

Current simulation speed is2.1 times player speed and terrain (forest0.72, hill0.8, ford0.6), positive low supply0.85 or empty0.6, and applicable active ability1.4. Actual displacement automatically accounts for compounded modifiers, stops and blockage. Nominal cycle playback may need a revised duration once reachable stride is known. Stop locomotion on zero displacement and use a reviewed idle transition; teleports/corrections reset contact rather than consume huge strides. Online phase bookkeeping must follow the actually displayed interpolated position.

The final PNG receipt records byte/RGBA hashes, dimensions, fixed root/scale and precise per-frame timing, plus rig/original component custody and original uncertainty metadata. GIF preview uses the whole38px canvas and explicitly notes integer-millisecond timing quantization. A real independent review must inspect anatomy, support transfer, contact and seam before runtime integration or other directions/actions.
