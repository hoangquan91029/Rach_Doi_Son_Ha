# Graphics production plan — PURE 2D, 8 October2026

Model routing (human instruction, 2026-10-08): use `model='gpt-6.1-sol'` and `reasoning_effort='low'` for every future code and art task in this project. Do not use Luna anywhere or silently fall back to another model. This supersedes the old master art Luna/HIGH split; preserve the original briefs, assets, directives and receipts as history. This is project routing policy, not a claim that the current chat UI model changed.

Current evidence: South009–011 provide four selected keys and four illustrated in-betweens; actual eight-frame atlas/APNG/browser playback is in `pure2d-loop-preview-012/`. Brief review identifies only F7 calf crossing; South013 completed one finite whole-frame correction; corrected loop014 has separated calves and fresh actual Chromium playback. No open call. Latest human instruction in `REVIEW_PRIORITY_20261008.md` prioritizes natural smooth gameplay-size motion and avoids exhaustive audits. Small cloth/pixel differences are nonblocking; preserved old South008 holds are historical, not instructions to repeat contact polishing.

Runtime016 resolves the local navigation hold: deterministic corner-safe eight-direction shared paths and exact sprite picking. All78 tests and actual Chromium/Firefox eight-frame movement/pause/stop/hat checks pass. Brief independent samples-only look found coherent identity/no new frame correction justified; recorded-video naturalness/foot lock remain unverified. Generic action exporter017 now supports1..256 frames, looping/nonloop terminal hold and real idle/walk demos through the existing client loader, with zero Chromium errors. Other actual action/roster artwork, public action mapping and shared roster/world scale remain open; no continuous naturalness/foot-lock/fanout or final production acceptance inferred. Read `pure2d-action-adapter-017/CHECKPOINT.md` and `action-production-017/RUNTIME_ACTION_MATRIX.md`; next prepare one finite controlled2D villager gathering pilot with a proper tool reference.

Latest authority: PURE_2D_MASTER_DIRECTIVE_20261008.txt explicitly replaces the prior3D proposal. Character production is pure2D illustration and controlled frame-by-frame animation. The previous plan remains recoverable in Git219d1fe; no source asset or experiment is deleted.

**Canonical2D Illustration →2D Character Consistency Specification →Controlled2D Key Poses →2D In-Between Frames →Finished Illustrated PNG Frames →Sprite Atlas →Web Game.**

## Why the3D proposal is abandoned

The human explicitly rejects character modeling, Blender, skinning, UV maps,3D material/lighting scenes, skeletal clips and3D-to-sprite baking, including required internal intermediates. The current primitive renders also failed canonical realistic appearance at gameplay size. No argument about classic RTS production techniques overrides the chosen art direction. Do not install Blender or evolve binding005. Preserve001–005 as superseded experiments, not production dependencies. No engine migration follows from this authoring change.

## Six stages

| Stage | Deliverable | Acceptance gate |
| --- | --- | --- |
| 1. Qualify one2D villager | Existing full-body canonical artwork, consistency specification and opposite illustrated contactsF0/F4 | Identity, proportions, historical outfit/material richness, consistent lighting/camera and anatomical support exchange at gameplay size; no simplified substitute. |
| 2. Complete one2D walk | ValidateF0/F2/F4/F6, then illustrateF1/F3/F5/F7 using neighboring keys; eight finished PNG frames and real loop preview | Correct contacts/weight transfer, no sliding, stable root/pivot, natural overlap/cloth, no texture flicker, smoothF7→F0 and convincing paused frames. Geometry alone is not evidence. |
| 3. Complete villager animations | Eight true directional references/walks, then role-specific idle/gather/chop/iron/food/carry/build/repair/hit/death and attack if actual gameplay uses it | Finite action/view pilots, same identity/light/camera, runtime state mapping and independent loop checks. Run only if gameplay requires a separate state. |
| 4. Expand military | One additional humanoid and one complex cavalry pilot, then2D archetype templates for spear/firearm/commanders/artillery/wagon/ship | Proven reuse of pose planning, QA/export/runtime tooling; unique illustrated equipment/outfits/leader identities, dedicated complex anatomy. No full army batch before villager succeeds. |
| 5. Finish battlefield art | Illustrated buildings/fortifications/trees/resources/forests/rivers/seas/hills/mountains plus UI/minimap/VFX on both maps | Coherent2.5D projection, light/shadow, scale/occlusion and readable routes/supply/units in dense gameplay; no crude final shapes. |
| 6. Validate web game | Automated atlases/manifests, bounded/lazy match asset loading and final accepted-art public build | Chrome/practicalFirefox load/memory/performance, actual SP and authoritative online1v1/reconnect/rematch; full battles with accepted artwork. |

## Resolution and performance

256² source canvas with224–233px character,112–116px runtime and roughly80px display is a baseline to validate, not immutable law. Use one brief loop review near80px; inspect another scale or paused frame only to resolve a visible problem. Preserve high-quality originals separately and never upscale to invent detail. Larger declared canvases are allowed for weapons, horses or animation extents; never clip artwork or fit each frame independently. Use one family-wide scale/pivot and an explicitly validated bounding-box policy.

Eight walk frames are the first pilot. If real playback slides, first inspect2D foot tracks/cadence/travel calibration; additional controlled illustrated in-betweens require an explicit finite order. The superseded3D48-frame clip supplies no new2D key, timing acceptance or production dependency. Do not hide problems by changing gameplay speed, blur or per-frame pivot.

Keep editable PNG originals outside runtime atlases. Reuse current hash/alpha/frame/pivot validation, manifest schema and sprite sampling. Plan page banks/lazy loading based on selected map/roster, decoded-memory profiling, deduplication and optional visualLOD only after actual quality checks. Current loader preloads approved/candidate assets in bounded groups rather than true match-based lazy banks; that improvement remains open. Do not manually author thousands of rectangles. Renderer changes must address an actual runtime requirement, not the illustration method.

## Current next implementation

1. Completed: one guide-bound F7 spacing correction in South013; first loop012 and all source originals preserved.
2. Completed: corrected loop014 rebuilt through existing atlas/APNG helpers; brief80px sheet shows separated calves and actual browser capture reports all eight frames/three cycles/zero errors. Naturalness remains a practical viewing judgment.
3. Integrate one usable atlas through existing state/direction APIs; check travel, stop and pause against simulation-authoritative movement.
4. Extend directions/actions and archetype reuse only after the first walk is usable. Keep finite work orders and source custody without repeated microscopic audits.
5. Finish battlefield art and validate the final public build against the full completion criteria.

Binding005 is terminalHELD and superseded: sampled clearance, continuity and triangle area failed;0 images/AI/runtime changes. Preserve its frozen evidence without further geometry work. The old hidden-joint/component rig is optional2D pose reference only; no new limb reconstruction art and no visible puppet assembly. Finished whole-body illustration quality takes precedence.

Detailed standards and reusable asset/script inventory: PURE_2D_CHARACTER_PIPELINE.md. Full game remains NOT COMPLETE; no art or owner approval is inferred by this plan.

VI: Quy trình đã đổi hoàn toàn sang minh họa2D có chiều sâu và hoạt ảnh từng frame. Giữ chất lượng asset gốc; kiểm tra hai contact, bốn key rồi vòng đi tám ảnh trước khi nhân rộng. Dừng dựng3D/Blender và giữ thử nghiệm cũ làm hồ sơ.
