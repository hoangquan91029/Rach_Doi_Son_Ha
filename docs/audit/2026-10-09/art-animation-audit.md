# Art and animation audit — 9 October 2026

Read-only audit of production/art; this report is the only file changed by this audit worker. No generation, source repair, deployment, game changes, browser match or repeated anatomy review. Evidence is local current source and receipts, not a new visual certification. Required routing: Sol 6.1 Low; built-in image tool only; pure complete 2D illustrations; no quota polling. Historical originals, rejected outputs and receipts remain authoritative custody.

## Finding

The game has a reusable frame renderer/exporter and several actual illustrated pilots, but does not yet have a complete illustrated villager, military class, leader or battlefield. Static building/node delivery is demonstrably faster than controlled locomotion. The next bottleneck is coherent pose sequencing and directional coverage, not atlas packing. Publishing each small static addition has validated a safe deployment process; it does not satisfy final visual release.

Human owner032 accepts the shown South/D1 wood loop; human141 accepts the shown South/D1 iron loop. Food101 is technically complete and locally integrated, but continuous-motion owner feedback remains pending. South walk014 is a technically working candidate; do not extend wood/iron owner acceptance to this locomotion or measured foot lock.

## Evidence hierarchy and freshness

- `AGENTS.md`, human routing and `REVIEW_PRIORITY_20261008.md` override old Luna/3D/numerical-anatomy scoring instructions. Human priorities are one brief real-size continuous look and correction of visible problems.
- `docs/FRAME_ANIMATION_REQUIREMENTS_115_145.md` requires whole-frame illustration, canonical identity, controlled neighboring keys, eight directions, stable pivot, unequal timing, atlas metadata, and simulation-independent presentation. Its old permitted internal3D and repeated scores are superseded by the pure2D directive and latest review priority. Frame ranges are suggested starting points, not an order to produce every listed action.
- `NEXT_STEPS.md` still leads with145/146 at this audit; use newer actual149/151/152/153 receipts for the latest target. Several checkpoint files intentionally preserve PREP text: execution receipts override it without deleting history.
- `docs/qa/cavalry-camp-public-149/public-receipt.json`: PUBLIC149_PASS_NARROW, `/assets/index-05PkH4eu.js`, SHA70808200c04fa3547aa4204a0baa6e04546f6d9206c93667ee4c3edf7556883b; Chromium/Firefox26ready/12portraits, build/select/train cavalry50/F2 exact cohort/Stop/menu, no errors/failures, rooms0. Decoded manifest image bytes16,942,592. This is receipt-derived deployment evidence; no new network request in this audit.
- `cavalry-camp-canonical-151/CHECKPOINT.md`: four exact148 target paths installed, all canonical client/shared/public/tests byteequal frozen148; local food preserved.
- `villager-walk-D0-paired-contacts-150/root-actual-pair-intake.json`: one call/zero retries HELD_SAME_LEADING_LEG; neither output selected, no repeat.
- `villager-walk-D0-clothed-guide-152/parent-selection.json`: selected033F00 and152F04 as opposite-contact key candidates only. Raw source hashes4a7d287b…041c and7ff8328a…2ef0. No loop acceptance.
- `villager-walk-D0-passing-keys-153/CHECKPOINT.md`: two clothed vector/PNG guides, zero calls, F02/F06 repaint UNCALLED; requires guide intake and a finite execution order. They are model guides, not finished character frames.

## Actual coverage matrix

Direction integers must be used in tickets. Engine/world direction0 is worldE, direction1 is worldSE, etc.; the camera maps D0 to screenESE/SE and D1 to screenSouth. Do not equate screenSouth with worldSouth or change headings to make an asset appear. Existing directional specification describes the screen/engine/world mapping in `PURE_2D_CHARACTER_PIPELINE.md`; runtime projection is `client/world-presentation.js`.

| Runtime identity/type | D0 | D1 | D2–D7 | Missing required visual coverage |
|---|---|---|---|---|
| Villager | Old one-frame neutral candidate at38logicalpx; separate034 matching idle export; selected033F0+152F4 walk keys only | idle1, walk8, wood8, iron8 in public optional routes; food8 in local optional food route | No completed runtime animation; preserved static identity references are not animation | all remaining facings; build/repair presentation, attack, hit, death; no separate resource-return carry pose |
| Infantry | one idle candidate,42logicalpx | none | none | idle facings, walk, attack, hit, death |
| Cavalry | one idle candidate,51logicalpx | none | none | coherent horse+rider movement, attack, hit, death, idle facings |
| General Trần Hưng Đạo | one idle candidate,42logicalpx | none | none | movement, attack, hit, death, command/ability personality; other facings |
| King (any identity) | none | none | none | complete body/action/direction coverage; portraits do not count |
| Other General identities | none | none | none | complete body/action/direction coverage |
| Spearman | none | none | none | all states/facings |
| Firearm infantry | none | none | none | all states/facings; firing/reload presentation tied to authoritative attack cycle |
| Artillery | none | none | none | whole equipment/crew move, attack/recoil/reload, hit/destroyed; deploy only if visible gameplay contract needs it |
| Wagon | none | none | none | whole wagon/animal/driver idle, move, load/unload, hit/destroyed |
| Warship | none | none | none | idle, move, fire/recoil, damage/sink |
| Transport | none | none | none | idle, move, boarding/unloading presentation if visible, damage/sink |

`shared/data.js` has11 unit types, including king/general, and12 actual leader identities: Han Xin, Xiang Yu, Napoleon Bonaparte, Lý Thường Kiệt, Trần Hưng Đạo, Nguyễn Huệ, Lê Thánh Tông, Minh Mạng/Minh Mệnh, Nguyễn Ánh, Nguyễn Phúc Chu, Trần Nhân Tông, Trịnh Cương. Use this configuration rather than historical example names Trịnh Tùng/Nguyễn Phúc Nguyên from earlier briefs. King and General can independently choose these identities (`shared/sim.js`), so the planning decision is12 shared character families with role overlays or24 separately finished role variants; never silently assume the smaller count satisfies both roles.

| Building (10 actual types) | Completed idle illustration | Other states |
|---|---|---|
| Residence | yes, old512cell/render130 | construction/hit/death/repair visual open |
| Granary | yes, old512cell/render85 | same |
| Barracks121 | yes,256cell/render112 | same |
| Depot126 | yes,256cell/render96 | same |
| Workshop140 | yes,256cell/render112 | same |
| Cavalry Camp147 | yes,256cell/render112 | same |
| Shipyard | absent | all |
| Fort | absent | all, including authored attack |
| Wall | absent | all; topology variants needed |
| Gate | absent | all; orientation/state variants needed |

Building idle source/actual scene intake is narrow acceptance, not construction/damage/death certification. New buildings support construction gameplay through existing fallback, then switch to idle art. Training a new cavalry/artillery unit does not mean its animation art exists.

| Battlefield category | Runtime candidate coverage | Remaining acceptance/work |
|---|---|---|
| Plain/forest/hill ground | grass material512 | material repetition and map composition |
| River/sea | one water material512 | distinct readable coasts/river interactions and final composition |
| Ford | one material512 | transitions/readability/accepted gameplay-size composition |
| Shore | one candidate512 |092/095 holds retained; final shores unaccepted |
| Forest | base+bamboo+palm props512/render75 | fringe/repetition/occlusion/dense readability |
| Mountain108 | one128/render56 | repeated silhouettes, both maps, partial terrain coverage |
| Hill111 | one128/render72 ground layer | partial edges/coverage/map composition |
| Food node114 | one128/render48 | final resource/depletion state readability |
| Iron node119 | one128/render48 | same |
| Wood resource | forest artwork supplies context | explicit depletion/stump/readability policy still needed |
| Contact shadow | one256 separate helper | family lighting/contact consistency |
| VFX/UI/minimap | existing gameplay implementation | no claim of full final illustrated VFX/UI package |

The camp148 manifest has26 asset entries and47 frame rectangles:23 single-frame assets plus three eight-frame sequences. Manifest counts are not unique animation counts across routes: older manifests repeat the same assets, hashes and files. Local food route has19 assets and food8, but does not itself include the newest world/building chain; combining routes is a future explicit manifest/build task after food acceptance. Public excludes food character route/data while static food node is published. Default unparameterized play remains the established fallback presentation; optional art is not the final default accepted art release.

## Source, runtime and display sizes

Proposed baseline:256source canvas,224–233character height,112–116runtime character height, roughly80display height. Actual new sources are1254×1254 raw illustrations; new villager cells128×128/render89 and common pivot[654,1140] in raw space. Height of the whole canvas is not visible character height. Older neutral unit cells512/render38/42/51 differ markedly in screen scale; the new villager and old troops cannot be called a unified accepted roster scale. Buildings use whole256 runtime cells/render96–112; source pivot[627,1010] for the recent family. Terrain global render56/72/48 differs honestly from author previews64/96/40; do not rewrite source provenance.

Preserve raw1254 originals. A future256 authoring derivative can be useful as a common guide/preview coordinate system, with a documented uniform fullcanvas transform and derived pivot; it does not turn the actual generator source into256 or establish pose locking. Freeze scale per identity/action family and inspect one real mixed scene. Do not individually fit frame bounding boxes, enlarge to invent detail or shrink a defective motion until it disappears.

## Reusable system versus per-identity labor

Already reusable: exporter0171..256frames/loop/terminalhold;098 actual-action preview and compatibility; PNG/hash/alpha validation; atlas rectangles; durations/events; `client/art-assets.js` bounded image preload/decoded128MiB guard; `sprite-timing.js`; locomotion distance phase; gather episodes; pause/presentation clock; exact sprite alpha selection; current rollback/static slice publishing.

`client/raster-slice.js` exact state/direction matching deliberately returns fallback if missing. It only maps villager/infantry/cavalry and Trần Hưng Đạo General today; extending manifest entries alone will not render king/spearman/firearm/artillery/wagon/ships. Construction is explicitly rejected as unauthored. Hit/death require authored states. `action-presentation.js` maps authoritative gather to resource-specific actions; repair/build share current build state; attack presentation is simulation-timed. Do not invent run/carry/deploy state assets without verifying a real state/event and visible need.

Per identity remains irreducible: historical body/equipment design, turnaround, whole illustrated keys and inbetweens, individual weapon/garment overlaps, camera/lighting, asymmetric hands/sash, leader personality. Reuse clothed-guide method and pose timing specifications, not villager pixels or a shared puppet.152 is one successful opposite-contact selection, not proof of reliable high-volume success.

Throughput bottlenecks: pose conditioning can repeat an old phase; large independent generation batches amplify drift; old exhaustion/retry history consumes time; recovered interrupted receipts can be confused with active calls; many nearly duplicate candidate manifests/promotion scripts increase clerical load; owner pending-food feedback is a separate acceptance gate; historical PREP files can mislead agents without execution receipt precedence.

Recommended automation (new finite code order, no art redesign): a read-only coverage report keyed identity/action/dir/review/runtime/public and SHA; declarative one action job manifest consumed by098/export017; receipt registry for called/returned/selected/held/interrupted slots; single route composition compiler and exact-image dedup; later match-based page banks. Keep technical pass, root visual intake and owner acceptance separate fields. Do not build another anatomy scoring framework or thousands of hand-maintained rectangles.

## Batching and mirror policy

Batch after a pilot gate, not before it. First contacts, then two passing keys, then four inbetweens with both selected neighbors, then one loop. Independent guides/metadata/export preparation can proceed in parallel; dependent frames cannot assume unreturned keys. Give each finished frame its own receipt and fixed family transform. Use2–4 finite source slots only after method qualifies; no blind retries. Stop on visible phase failure and change the control method explicitly, retaining the failed output.

Whole illustrated frames only; no limb donor splices, cutout assembly, source TPS repairs,3D intermediates or silent API fallback. Original vector pose guides are allowed and153 is PREP only. Villager anatomical-left sash prevents automatic mirrors; leaders/asymmetric weapons require real directions. A genuinely symmetric generic family might reduce8 to5authored views, but only after hands/equipment/light/shadow/pivot checks and explicit mapping support; renderer currently has no such mirror support. Budget all8 until a particular pair is approved. Mirroring never proves contact alternation.

## Workload estimates and execution milestones

Counts below are planning assumptions, not tool calls promised or accepted frames; retries/holds/guide labor add overhead. No fixed calendar promise is justified by the current receipts. Eight source calls yielded food8; iron required tool reference, readiness, interrupted recovery and phase reassignment; locomotion required numerous held approaches. Measure the next two qualified cycles before forecasting dates.

1. **D0 walk qualification:**153 guide intake, then two separately receipted F2/F6 whole-frame repaints. Brief89px key comparison, then four inbetweens only if keys pass. Six missing actual frames, minimum6successful source slots. Export using fixed128/89 family, brief continuous actual-size loop/travel/stop. Visible defect allows one explicitly bounded correction order, not exhausted-method retries. Preserve152 opposite-contact candidate acceptance separately.
2. **Food gate:** use existing101 actual-size loop and await the pending human feedback; no repeated approval request or new generation needed. After acceptance, exact local food+camp composition and one actual resource episode/pause/ordinarywalk deposit proof, then short public load/interaction proof with rollback. Pending feedback must not block independent D0/maps/tooling.
3. **Complete villager locomotion:** after D0, six remaining facings ×8=48new finished frames plus6matching idles minimum (static idle provisional; animated idle can follow visible need). One facing per finite job; gait/identity/fixedscale brief loop, then real travel/turn/stop. Existing8static references are guides, not these48frames.
4. **Complete functional villager:**8facings ×(three gather actions8+build/repair8+attack8+hit4+death8+walk8+idle1)=488frames baseline. Existing D1idle/walk/wood/iron/food provides33completed frames, though food acceptance pending; D0two selected keys adds2draft frames, not runtime coverage. Approximately453new finished frames to fill this inventory if all states need all8facings. Separately animated idle4 rather than1 adds24frames. No separate returncarry or run assumed.
5. **Military reuse gates:** one infantry complete direction (idle1+walk8+attack8+hit4+death8=29frames) and one cavalry complete direction (same29starting frames, with horse+rider-specific guide family). Validate actual attacks and terminal death before eight-direction batches. Baseline232frames per full8direction generic family. Infantry/spear/firearm/cavalry/artillery/warship are six combat families≈1392frames at that minimum; firearm reload/artillerycrew complexity likely increases it. Wagon and transport at idle1+move8+load8+unload8+hit4+death8=37/facing produce296each, or592combined, only if separate visible load/unload is required. Without separate load/unload, these two families need168combined; scope decision must be documented.
6. **Leaders:** minimum idle1+walk8+attack8+hit4+death8+command/ability8=37/facing;296per identity,12identities=3552finished frames. Distinct king/general visual families double to7104. Role overlays sharing one accepted identity save this duplication only if historically and visually accepted. Idle4adds288 across12identities. Do not confuse12portraits with3552body frames. One premium leader pilot must precede the roster.
7. **Buildings/maps:** four absent building idles minimum4sources;10types ×(construction3+damage2+ruin1)=60additional still states as an explicit initial proposal, plus wall/gate orientations/topology and Fort attack. These are stage images/frames, not a demand for60unconditional calls. One Shipyard source/runtime is a reasonable independent next static pilot, then Fort/wall/gate. Map work: one bounded shore transition slice preserving092/095 holds, then forest/dense occlusion, mountain repetition/hill edges on BOTHmaps. No large character batch depends on finishing every map pixel.
8. **Final integration/performance:** selected-map/selected-leader lazy banks and bounded requests, measure actual decoded memory, frame time and startup on practical external device; mixed full accepted roster/map footage. Then existing successful AI/online lifecycle contracts plus final accepted-art battle across BOTHmaps, reconnect/rematch and final owner visual review. Repeat full matches only for changed risks; client-only static art requires short load/interaction proof.

Combined lower-scope illustrative frame inventory: villager488 + sixcombat1392 + wagon/transport168 + leaders3552 =5600unit frames, before extra idles/reload/complex motions/building/map/VFX variants. Richer wagon/transport actions produce6024. Separate leader roles can add3552. This is why thousands of individual source calls should not be launched now. At128²RGBA,5600untrimmed cells occupy350MiB decoded before other art and duplicate page retention; at256² they occupy1400MiB. Existing128MiBguard will not make an all-roster preload viable. A single8frame128 atlas is0.5MiB decoded; encoded PNG/WebP download is a different metric. Final lazy loading/page banking is therefore a practical requirement, not optional polish.

## Acceptance contract

For each finite asset/action: immutable originals/references/tool receipts; actual selected frame count; one family transform/pivot; lightweight alpha/hash/atlas/missingframe checks; one brief actual gameplay-size continuous loop or static scene; correct visible pose/action; technical loader/pause/state tests appropriate to the change. Report narrow pass separately from owner acceptance. No claimed measured foot lock without measurement; no automatic fanout from technical pass; no speed/balance/fog manipulation to make art appear. Full project remains incomplete until real required8direction roster/action/world art and practical browser performance/final scene acceptance are delivered.

## Vietnamese summary

Hệ thống xuất atlas và hiển thị đã dùng lại được; nút thắt chính là tạo đúng các pose liên tiếp và đủ8hướng. Wood032 và iron141 chỉ được chủ dự án chấp nhận cho vòngSouth/D1đã xem; food còn chờ phản hồi. D0mới cóF0/F4được chọn,153chỉ có hai guide, chưa cóF2/F6hay vòng hoàn chỉnh. LàmD0hai key rồi bốnBI, kiểm tra ngắn vòng ở kích thước chơi thật; sau đó mới mở rộng từng hướng. Giữ ảnh1254gốc,256chỉ là bản dẫn xuất có ghi transform. Không lật villager có sash bất đối xứng, không ghép tay/chân, không3D/API. Khối lượng đầy đủ có thể khoảng5600–6000frame hoặc hơn tùyhai vai leader; cần đo năng suất pilot và chia tải theo trận, không nạp toàn bộ trước menu.

### Display measurement clarification

`render.height=89` is the full transparent canvas in logicalCSS pixels atzoom1, not opaque body height. Actual height is approximately `alphaBBoxHeight/runtimeImageHeight × render.height × camera.zoom`; frame-specific alpha extent must be measured from actual pixels when needed, without refitting. `client/renderer.js` defaultszoom1;149Chromium receipt initially records1 and later1.08. Thus an89canvas becomes96.12CSSpx at1.08, while old neutral42canvas becomes45.36CSSpx and cavalry51canvas55.08. Their visible bodies are smaller still. Root's brief1491280×800scene intake estimates units around35–45px; that is visual observation, not a pixel measurement. This confirms that an89preview alone cannot establish target64–96opaque character size or mixed-roster scaling. Freeze one scene scale and measure only enough actual opaque extents to resolve this visible discrepancy, then use it across families.

### Historical content bibliography

Leader body art must preserve distinct historical identity, but the presence of12portraits does not establish source-backed costume accuracy. Audit leadership dossier citation tokens separately: reconstruct a usable bibliography with titles/primary-sourceURLs and which costume/identity claims each supports, preserving existing opaque citation tokens and original dossier files. Recoverability and historical-art review are content milestones, independent of pose/tool/runtime qualification; do not label unverified equipment historically certified. No external bibliography research was performed in this worker.
