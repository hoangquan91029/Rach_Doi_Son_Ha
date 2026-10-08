# Graphics production plan — PURE 2D, 8 October2026

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

256² source canvas with224–233px character,112–116px runtime and roughly80px display is a baseline to validate, not immutable law. Review64/80/96px plus paused frames. Preserve high-quality originals separately and never upscale to invent detail. Larger declared canvases are allowed for weapons, horses or animation extents; never clip artwork or fit each frame independently. Use one family-wide scale/pivot and an explicitly validated bounding-box policy.

Eight walk frames are the first pilot. If real playback slides, first inspect2D foot tracks/cadence/travel calibration; additional controlled illustrated in-betweens require an explicit finite order. The superseded3D48-frame clip supplies no new2D key, timing acceptance or production dependency. Do not hide problems by changing gameplay speed, blur or per-frame pivot.

Keep editable PNG originals outside runtime atlases. Reuse current hash/alpha/frame/pivot validation, manifest schema and sprite sampling. Plan page banks/lazy loading based on selected map/roster, decoded-memory profiling, deduplication and optional visualLOD only after actual quality checks. Current loader preloads approved/candidate assets in bounded groups rather than true match-based lazy banks; that improvement remains open. Do not manually author thousands of rectangles. Renderer changes must address an actual runtime requirement, not the illustration method.

## Current next implementation

1. Audit existing South canonical andF0 contact. Keep static eight-view identity lock as preserved authoring evidence, not animated acceptance. OldF2 retries remain held; do not reuse them as selected continuity keys.
2. Prepare a new pure2D consistency/pose guide and one finite oppositeF4 edit order using canonical+F0+explicit guide, not unrelated prompts. No3D measurements/modules as dependencies; old2D proportions/root/left-right annotations may be reused when verified.
3. Inspect the actual returned image, keep raw/prompt/reference hashes, compare fixed-scaleF0/F4 at game size and record held/selected candidacy honestly. No in-betweens before four-key acceptance. No full loop claim until all finished frames are reviewed.
4. QualifyF2/F6 with planted-foot tracks and neighbors; produce in-betweens only after keys pass; use actual playback at simulation travel speed and independent review.
5. Integrate one qualified atlas through existing exact state/direction API, then the remaining directions/actions and two reuse pilots. Public deployment waits for its actual build/runtime gates.

Binding005 is terminalHELD and superseded: sampled clearance, continuity and triangle area failed;0 images/AI/runtime changes. Preserve its frozen evidence without further geometry work. The old hidden-joint/component rig is optional2D pose reference only; no new limb reconstruction art and no visible puppet assembly. Finished whole-body illustration quality takes precedence.

Detailed standards and reusable asset/script inventory: PURE_2D_CHARACTER_PIPELINE.md. Full game remains NOT COMPLETE; no art or owner approval is inferred by this plan.

VI: Quy trình đã đổi hoàn toàn sang minh họa2D có chiều sâu và hoạt ảnh từng frame. Giữ chất lượng asset gốc; kiểm tra hai contact, bốn key rồi vòng đi tám ảnh trước khi nhân rộng. Dừng dựng3D/Blender và giữ thử nghiệm cũ làm hồ sơ.
