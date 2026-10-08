# Controlled2D character production specification

Model routing (human instruction, 2026-10-08): use `model='gpt-6.1-sol'` and `reasoning_effort='low'` for every future code and art task in this project. Do not use Luna anywhere or silently fall back to another model. This supersedes the old master art Luna/HIGH split; preserve the original briefs, assets, directives and receipts as history. This is project routing policy, not a claim that the current chat UI model changed.

Current evidence: South009–011 provide four selected keys and four illustrated in-betweens; actual eight-frame atlas/APNG/browser playback is in `pure2d-loop-preview-012/`. Brief review identifies only F7 calf crossing; South013 completed one finite whole-frame correction; corrected loop014 has separated calves and fresh actual Chromium playback. No open call. Latest human instruction in `REVIEW_PRIORITY_20261008.md` prioritizes natural smooth gameplay-size motion and avoids exhaustive audits. Small cloth/pixel differences are nonblocking; preserved old South008 holds are historical, not instructions to repeat contact polishing.

Runtime015: real ?art=walk loading and reusable distance phase implemented. Actual UI test is HELD_NAVIGATION because path() uses only cardinal neighbors; next implement deterministic corner-safe eight-direction routes, then observe actual South movement/pause/stop. No new art batch or production acceptance.

Authority: PURE_2D_MASTER_DIRECTIVE_20261008.txt. No required3D geometry/model/Blender/UV/skin/clip/render steps. The final source is a complete illustrated2DPNG, not detached rotated limb textures. All gates begin pending.

## Canonical reference system

Each identity record declares source paths/encoded+RGBA hashes, full canvas, authored fixed ground anchor, face/proportions/outfit/equipment/sash side, light/highlight/shadow direction, palette/material richness, camera/view mapping and visual review receipt. Original high-quality files are immutable. Editable derived frames retain parent/reference/prompt/tool provenance. Store guides separately from illustration originals and runtime derivatives.

Current villager canonicalAppearanceSource is docs/art/characters/villager-neutral-D00-screen-ESE/raw.png. VILLAGER_IDENTITY_LOCK_007.json binds eight static candidate references; its source1254²/pivot[654,1140]/old38px presentation is immutable seal history, not current target-size acceptance. South isD01/worldSE; anatomicalLEFT is viewerRIGHT, confirmed by original sash. Selected oldF0 is only PASS_KEY_CANDIDATE_ONLY, not loop/scale/final acceptance. Review its actual image under the new80px baseline before qualification. Do not alter the seal to pretend it contains animated frames.

A new family consistency record must freeze one global source→runtime scale, exact authored ground anchor and declared camera/light directions. If tool output size differs, preserve raw and record one uniform full-canvas transform shared by the family, never a per-frame bounding-box fit. A failure to maintain canvas/anchor is held, not repaired by undisclosed shifts. Source filenames use identity/action/screen-direction/phase/version; engine direction mapping stays explicit.

## Key and in-between workflow

Use one canonical identity and controlled2D skeleton/landmarks/contact silhouettes/masks for each pose. Existing2D guide measures may be reused after checking actual artwork; no new3D model or source dependency. Whole-image warping/layered editing/inpainting/paint-over is permitted as an authoring tool under this directive, but must reconstruct anatomy, sleeve/shoulder/tunic transitions and coherent materials in the final whole illustration. Do not collect new isolated limb textures or force illustration quality down to fit a puppet.

| Phase | Pose | Support/transition |
| --- | --- | --- |
| F0 | LEFT forward contact | Receives weight, opposite arm forward |
| F1 | Transfer/down | LEFT stance, RIGHT lift |
| F2 | RIGHT passes LEFT | LEFT planted, RIGHT clearance/overlap |
| F3 | LEFT push-off/up | Toe support; RIGHT approaches contact |
| F4 | RIGHT forward contact | Opposite support/contact roles |
| F5 | Transfer/down | RIGHT stance, LEFT lift |
| F6 | LEFT passes RIGHT | RIGHT planted, LEFT clearance/overlap |
| F7 | RIGHT push-off/up | Toe support; LEFT approachesF0 |

First validate oppositeF0/F4. Then qualifyF2/F6 beforeF1/F3/F5/F7. Key anatomy/contact validation precedes final fold/detail polishing. Each in-between attaches canonical identity and its two selected neighboring keys, with guide plus explicit target pose. Never use held frames as selected neighbors. Retain raw outputs even on failure. One reviewed defect list and a finite targeted correction order replace unrestricted retries. Final textures/light/anatomy must remain rich and consistent, including paused frames.

## Supporting-leg validation

Annotate anatomicalLEFT/RIGHT hip/knee/ankle/heel/toe ownership on a separate2D guide; near/far or screen side never renames a limb. Declare root and ground-contact line/region for each phase in shared coordinates. Measure source foot landmarks from actual output, not prompt claims. F0vsF4 must visibly swap receiving/front contact roles; F2/F6 must visibly pass the opposite stance foot with plausible knee/ankle clearance. Heel rise/push-off and brief double contact are permitted where planned.

Render a real eight-image loop and a world-moving preview at authoritative interpolated travel speed. Track planted heel/toe positions in world-screen space through held frame intervals, contact transitions and seam. Report contact drift at64/80/96px; proposed≤2CSSpx tolerance must be frozen with cadence/travel calibration before full-loop acceptance. No per-frame fitting/root compensation or slower simulation hides sliding. Inspect body bounce, arm counter-swing, garment occlusion, seam and texture flicker at normal rate and paused frames. Foot measurements/numeric checks do not replace an actual independent visual loop review. No default325/650ms period or48 samples is inherited from superseded3D.

## Eight directions and camera

Existing mapping:SE=D00/E;S=D01/SE;SW=D02/S;W=D03/SW;NW=D04/W;N=D05/NW;NE=D06/N;E=D07/NE (screen/engine/world). Read client/world-presentation.js for actual54×27 dimetric grid/elevation metadata/zoom. Establish2D camera-reference, ground-axis and height/occlusion guides compatible with buildings/trees, not a requirement for a physical3D camera. Unresolved visual perspective remains a gate; do not silently modify gameplay headings or engine projection.

Do not generate other direction animations before first direction qualifies. Preserved eight static originals may inform consistency without new calls. AnatomicalLEFT sash makes villager mirroring unsafe; no automatic mirrored villagers/leaders/asymmetric weapons. Symmetric generic units may use a declared mirrored pair only after equipment, clothing, lighting/shadow and hand ownership checks. Kings/Generals receive individual illustrated directions and premium identity attention.

## Reusable2D archetypes / actual action mapping

HUMANOID_GENERIC: villager/light infantry/civilian proportions and locomotion references. HUMANOID_SPEAR: polearm grip/reach/overlap. HUMANOID_FIREARM: aim/fire/reload/two-hand grip. COMMANDER: distinct identity/posture/command/ability actions. CAVALRY: dedicated horse gait+mounted rider. ARTILLERY_CREW: wheel/crew/deploy/aim/fire/recoil/reload/destroyed. SUPPLY_WAGON: draft animal/driver/load/unload/destroyed. SHIP: vessel move/fire/damage/sink and coherent crew.

Reuse timing/pose/QA templates, never identical copied identities or humanoid rig assumptions for complex units. Verified12 current shared/data.js entries are bound in PURE_2D_EXISTING_INVENTORY.json. The directive examples name Trịnh Tùng/Nguyễn Phúc Nguyên whereas current configuration uses Trịnh Cương/Nguyễn Phúc Chu; retain this discrepancy for original-dossier/roster review before leader fanout, do not silently rename portraits or gameplay. Preserve all148 supplied leadership sources and historical dossiers. Build a runtime-state matrix per unit: idle/walk/run only if actually distinct, role-specific resource/work/carry/repair actions, attack/reload/command/ability where required, hit and nonlooping death. Shared work artwork is allowed only when the visible activity and tool fit; absent states remain placeholder, not mislabeled idle.

## Atlas and manifest standards

PNG originals with genuine alpha, preserved raw/high-quality editable source and separate optimized atlas. Each source/derivative has encoded and decodedRGBA hashes, dimensions, alpha bounds, fixed family pivot, declared uniform derivation, source/reference provenance and finite frame count/order. Contact sheets/preview are diagnostics, not source originals. No guide labels, checkerboard background, duplicate/missing limbs or clipped weapons in finished frames.

Reuse schemaVersion1 in public/assets/art-v1/manifest.json and client/art-assets.js: camera, exact state/direction, family source/cell/render layout, source/runtime hashes, frame rectangles/durations/events, contact shadow, loop and explicit candidate/reviewer/receipt. All new assets remainCANDIDATE until actual gates pass. Current uniform full-canvas family contract does NOT yet implement arbitrary per-frame trims; cropping/gutters/page banks need reviewed compiler/validator/runtime support before use. Never manually maintain thousands of rectangles. Nonlooping death holds final frame; animation events are cosmetic and align with authoritative combat, never decide damage/resources/victory.

Automation must validate names, frame count, alpha, dimensions/pivot, derivation/hash/frame rectangles and produce contact sheets, loop previews, atlases and manifests. Existing scripts/validate-art-assets.py and client/sprite-timing.js/art-assets.js remain reusable; old South tooling/atlas.py correctly derives rectangles and preserves original custody but hardcodes1254canvas/38px/600ms and runtime cells≥256, so its algorithms require a new parameterized adapter before the flexible baseline. Old walk-south-keys-v2/build-guides.py contains3D IK/projection and is NOT a pure2D guide dependency; preserve it as superseded history only. inspect exact coverage before crediting a gate. Loader currently batches preload; true match-specific lazy banks/decoded-memory budget/LOD remain open. Asset compile automation should derive rectangles from actual files.

## Reuse and stop inventory

REUSE: canonical/directional full illustrations, original historical/leadership sources, immutable identity custody, selectedF0 contact as candidate only, verified2D root/proportion/LR/contact guides, existing complete-frame custody tools, PNG/alpha/hash validation, Canvas sprite API, event sampler and browser capture/contact-sheet code with correctly declared timing/scale.

HOLD/PRESERVE: failedF2 contact attempts, oldlimb textures/components and calibration/rig experiments, blocky001–004 sprite outputs, binding005 source/evaluation. They are not selected final art or required production inputs. Old guide errors/omissions remain disclosed.

REMOVE FROM REQUIRED TASKS: Blender installation/modeling/rigging/UV/material bake; new3D skin/skeleton/clip/renderer; capsule garment solver iteration;3D-derived pose generation dependency; model-based camera reconciliation. No such package is installed locally. Existing experimental files remain frozen; no deletion. Optional old2D rig complexity is discarded from active scheduling unless it concretely improves a finished image. Do not migrate the engine to implement2D authoring.

## Concrete next jobs

1. Root updatesplan/spec/status/automation and preserves directive/terminal005 receipt.
2. Art worker prepares one new2D opposite-contactF4 guide/spec/order from canonicalSouth+selectedF0. Parent verifies anatomical labels/target contacts and references before one built-in image edit. No other key calls open.
3. Actual source is copied intact with prompt/reference/tool receipt, inspected at native and fixed gameplay size; measure contact ownership/anchor/identity. Hold on any major defect; no implied approval/retry.
4. If contacts qualify, open finiteF2/F6 key orders, then in-betweens; eight-frame loop/independent motion review/atlas/browser gate. If a tool fails, preserve diagnostics, report limitation and continue feasible tooling; no CLI/API fallback without explicit user selection.
5. Finish remaining directional walk/states; validate one military humanoid and cavalry reuse pilot before roster fanout, then battlefield and full web validation.
