# Runtime motion contract — support161

Read-only source research for a practical movement pilot. This document changes no runtime, art, generation, simulation or playback. It does not certify foot lock or visual acceptance.

## What the current renderer actually preserves

`client/art-assets.js` validates isotropic source-to-cell dimensions, one fixed source-space pivot and one logical render size. It rejects per-frame pivot overrides and incompatible layout inside the same literal family. `client/raster-slice.js` draws the entire selected cell with that fixed transform; it does not rotate, mirror, warp, interpolate body parts or deform pixels. Animation chooses a discrete frame through `client/sprite-timing.js`. Therefore body/clothing/equipment shape changes visible inside neighboring full images originate in the illustration sequence; presentation can change the frame, position, timing or apparent size, but cannot repair anatomical or costume changes within it.

The family guard uses literal family strings. Old D0 `villager` and newer D1 `unit.villager` are two different guarded families even though renderer selection treats both as the same unit identity. Thus existing validation does not itself guarantee visual scale equality across those aliases. Preserve the entire family transform across authored frames; do not fit individual alpha bounds or move each frame's pivot.

Camp148's actual D1 walk has source1254², cell128², render89² and source pivot(654,1140). Eight 75ms frames total600ms. Its `distancePerCycle=1.26` is explicitly provisional: speed2.1 world units/s ×0.6s, not a foot-lock measurement. D1 idle, wood and iron use the same canvas/cell/pivot/render family layout; the work loops use unequal durations. D0 idle uses source1254²/cell512²/render38² with the same source pivot but belongs to the older literal family.

## Distance phase and state selection

`client/locomotion-phase.js` accumulates actual observed Euclidean displacement per entity when current or previous state is walk, time advances and presentation is not frozen. Identity changes, missing entities, backward tick/time or implausible jumps reset/remove tracking; ordinary idle/Stop does not reset accumulated distance. For cycle length L and total authored duration T, animation time is `(travelledDistance mod L)/L × T`. Frame duration boundaries therefore define fractions of travel distance; they are not simply fixed wall-clock playback during movement. With no displacement the walk phase stays fixed. Pausing freezes accumulation. If an asset lacks locomotion metadata, it uses presentation time instead, so a new walk pilot must not silently omit that contract.

The renderer selects actual engine `entity.dir`, exact state and matching authored family. Live hit overrides ordinary state; hp<=0 selects death. Idle cannot stand in for walk. Missing direction/action returns the existing fallback. Stop changes the actual state to idle; there is no invented transition blend or per-step phase reset. Loaded return movement uses ordinary walk in simulation. Online render positions are interpolated by `interpolateView` before this observer; offline rendering uses current simulation positions. Compare phase against those actual rendered positions, not a separate synthetic velocity clock.

## D0 and D1 are world headings

`shared/sim.js` sets dir by rounded `atan2(dy,dx)/(π/4)`. D0 means world(+x,0). D1 means world(+x,+y), normalized to `(1/√2,1/√2)` for unit distance. With tile54×27, zoom z, the camera-relative projection increment is:

`ΔP = z × (27(Δx−Δy), 13.5(Δx+Δy))` logical pixels.

At default z1.08, one world-distance unit at D0 moves screen(+29.16,+14.58), an ESE/down-right heading. D1 moves screen(0,+20.62), screenSouth. ScreenSouth is not worldSouth. Do not relabel or inject facing to obtain a convenient view. Camera pan is a common additional translation; remove it when comparing world contact positions.

## World stance-foot condition

Let q_i be a selected stance-foot contact coordinate inside runtime cell i, p be its fixed runtime pivot, and S be the fixed cell-to-logical transform: diagonal `(renderWidth/cellWidth, renderHeight/cellHeight)`. Its displayed position is:

`F_i = P(X_i) + z S(q_i−p)`.

For the same planted foot across two samples, fixed zoom and after compensating camera movement, no slip requires:

`ΔF = z A ΔX + z S Δq ≈ 0`, where `A=[[27,−27],[13.5,13.5]]`.

For straight travel direction u and phase advance Δφ, actual travelled distance gives `ΔX ≈ u L Δφ`; thus the needed local foot displacement during stance is:

`S Δq ≈ −A u L Δφ`.

The planted foot must move backward inside the illustration by the projected root advance. Keeping it fixed in a stationary-cell preview while the root advances in gameplay causes sliding. Merely matching cadence to speed or returning the pivot to the same point proves neither contact nor world foot lock. Swing phase is exempt from this planted-foot condition. Never compare alternate feet as if they were one continuous ground contact.

For the current L1.26 and z1.08, a full cycle advances root D0(+36.74,+18.37)px or D1(0,+25.98)px. A hypothetical half-cycle stance needs approximately the opposite half of that displacement: D0(−18.37,−9.19)px, D1(0,−12.99)px. These are examples from current provisional L, not targets imposed on unaccepted D0 artwork. At D1 render89/cell128, that half-cycle example corresponds to about17.30 cell pixels of backward foot motion. A changed physical stride should be assessed through the whole action's L and authored contacts, without changing gameplay speed to conceal art.

Discrete frames are held while the root moves between boundaries. Exact continuous cancellation is therefore impossible with finite static frames: expect small within-hold residuals and a compensating change when a frame advances. Use brief gameplay-size observation to judge whether this quantization is visible, then record a few contact samples only if needed. Do not demand microscopic zero error or infer failure solely from a native-resolution pixel discrepancy.

## Separate source defects from playback defects

| Visible problem | Useful distinction | Preserve / practical response |
|---|---|---|
| Torso, costume or limbs change shape between keys | Present inside original whole images at a fixed transform | Correct whole illustrated keys/inbetweens; no limb patching or pixel splicing |
| Whole body jumps at a frame boundary | Contact/root coordinate differs inside images, or metadata/layout differs | Check fixed pivot/cell/render first; compare the apparent ground point once |
| Foot slides while travelling | Local stance displacement does not cancel actual projected root travel | Use observed ΔX and contact Δq; cadence alone is insufficient |
| Loop advances while stopped or phase skips | Wrong state/phase input, identity/time reset, absent locomotion metadata | Preserve actual simulation state and distance-driven phase; diagnose recorded inputs |
| Walk→idle suddenly changes size | Different family transform or idle silhouette | Align a whole family after actual mixed scene intake; never per-frame fitting |
| Turning changes screen travel direction | Correct dimetric projection may differ from filename/screen label | Preserve engine heading and actual UI movement; use D0/D1 numeric labels |

Coverage157's measured visible-alpha extents at z1.08 are old villagerD0 idle38.96px, D1 idle90.11px and D1 walk91.61–93.12px. These include shadows/equipment, so they are not anatomical body-height measurements. D1 Stop can change silhouette extent by roughly1.5–3px with unchanged render size; the much larger D0↔D1 gap reflects old/new scale/family separation. A future D0 walk at the newer family scale would need compatible D0 idle to avoid a Stop-size jump. No new D0 runtime walk exists in this inspected bank and this document does not predict acceptance of its selected contact candidates.

## Minimal preview inputs and evidence

For one qualified identity/action/direction, retain whole-image custody hashes, frame order/durations, source/cell/render dimensions, one pivot, locomotion L and numeric engine heading. Supply actual gameplay zoom/DPR, actual observed position samples and presentation time, selected frame index and accumulated distance. Record the chosen stance foot plus a few contact coordinates only across its claimed contact interval. Compute camera-compensated root advance, contact displacement and net ΔF in logical pixels; use the metric to explain visible slip, not replace the brief visual look.

Use a short stationary loop to spot source deformation/seam and a separate genuine travel→Stop sample to check world movement and idle transition. A stationary preview is not travel acceptance. Preserve simulation speed, collision/pathing, authoritative direction, liveness/ownership guards, exact source pixels, family scale and history. Do not add a fake travel test, full match, repeated anatomy audit, per-frame warp, cutout assembly or broader roster fanout for this research support.

Sources inspected: `client/renderer.js`, `client/raster-slice.js`, `client/art-assets.js`, `client/locomotion-phase.js`, `client/sprite-timing.js`, `client/main.js`, `client/world-presentation.js`, `shared/sim.js`, actual `public/assets/art-v1/camp-148-manifest.json`, and coverage157 report. This is current local-source reasoning; no browser run or external research was performed.
