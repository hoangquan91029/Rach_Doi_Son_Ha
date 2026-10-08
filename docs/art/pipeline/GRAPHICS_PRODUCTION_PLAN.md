# Graphics production plan — 8 October 2026

Authority: the latest human clarification requires realistic illustrated graphics matching the existing canonical assets. Primitive pilots001–004 are motion scaffolds, not official art. Motion, appearance, exact camera, runtime and release acceptance remain separate. This plan does not approve a held artifact.

## Production route

Build one complete clothed character per identity, with a shared rig/clip where anatomically appropriate. Author outfit volume, silhouette, hat/sash ownership and a coherent whole-model material/UV treatment from the existing artwork. Use soft, consistent lighting and readable low-frequency cloth forms; no anatomical micro-detail or zoomed-frame beauty target. Bake complete transparent 2D sprite frames for the browser. The player sees whole illustrated frames, never independently rotated limb cutouts.

Evaluate Blender as the offline authoring/render tool for the faithful reconstruction, rather than treating the bespoke primitive rasterizer as a proven final-art renderer. Its official [UV projection documentation](https://docs.blender.org/manual/en/latest/modeling/modifiers/modify/uv_project.html) describes projection onto a mesh, and its [baking documentation](https://docs.blender.org/manual/en/4.4/render/cycles/baking.html) describes coherent material/lighting texture baking. These capabilities are not evidence that a model automatically matches the canonical art. Current local inspection found neither Blender/bpy nor a completed .blend/.gltf/.glb/.obj/.fbx character model. Tool installation, faithful modeling and visual qualification are outstanding, not implemented by this plan. Pin an actual supported tool version when installed, before reproduction.

Do not project a walking image onto an unrelated primitive and call it reconstruction. Match the whole silhouette and garment construction first, then align/paint coherent surfaces once for reuse. Preserve raw sources, historical/leadership assets and all held attempts. Never generate separate limb textures. AI repaint remains optional only after a genuinely faithful whole-model result is reviewed at gameplay size and still appears too flat; any fallback must retain finite frame orders, identity/contact controls, source custody and actual loop review.

## Ordered gates

| Stage | Deliverable | Gate to next stage |
| --- | --- | --- |
| 1. One complete villager appearance | Faithful clothed model and reusable materials; complete opposite contacts in the existing D07 pilot direction | At nominal80/96px, hat, wrapped tunic, sash, loose trousers and material appearance match the existing reference. No primitive/toon substitute; no owner approval inferred. |
| 2. One villager walk | Complete sprite loop from the preserved003 clip, changed garment deformation and a real-size in-engine/looping preview | Independent actual loop review: support exchange, visible foot contact, no sliding, stable pivot, smooth cadence/seam, no garment clipping or identity wobble. Static contacts/numeric preflight cannot pass this gate. |
| 3. Camera and full villager package | Reconciled exact game projection, eight true directions; idle/walk/carry/work/attack/hit/death states | Per-action/view finite pilots, original identity consistency, no asymmetric mirroring, correct simulation-driven action timing, fixed calibration and browser atlas validation. Do not blindly export48 frames for every action. |
| 4. Shared archetypes and roster | Humanoid infantry/spear/firearm/King/General; distinct horse+rider, wagon and ship/crew rigs; complete required actions | One qualified representative of each distinct rig/action topology before a finite batch. Leaders keep individual historical appearance; firearms need reload/grip, cavalry needs horse contact, logistics needs loaded/carry variants. Shared rig does not mean identical outfits/faces. |
| 5. Finished battlefield slice | Residence/Granary/depot/military/naval buildings, resources, terrain transitions/props, combat VFX, UI/minimap and both authored maps | Units, supplies, leaders and attack routes remain readable at default zoom; coherent light/palette/scale, useful terrain contrast, no excessive effects or repetitive unfinished tiling. Review dense fighting, fog, forest/shore/hill occlusion and multiple routes. |
| 6. Browser production qualification | Accepted atlases/manifests, required WebGL batching, loading/memory policy and public accepted-art build | Measured crowd/long-match performance, bounded decode/load costs, Chrome and practical Firefox acceptance, full public single-player and cross-browser1v1/reconnect/rematch with final art. A prototype preview is not release acceptance. |

Stages1–2 are the immediate priority. Preparation for later stages is allowed, but no new direction/unit source batch opens before the current pilot gates pass. Existing eight-view static authoring identity custody is preserved; it is not eight qualified animated directions.

## Resolution and temporal sampling

- Proposed source canvas256², character about224–233px; runtime128², character about112–116.5px; proposed default character80px with64/96px diagnostic review. Current004 measures226/113px. This2:1 reduction supplies edge sampling while staying within source192–256/runtime96–128 character ranges. Historical1254px sources are preserved references, not new-frame targets.
- Eight key poses specify a walk, not a guaranteed eight-image playback budget. Frozen003 uses48 temporal samples over649.579324ms because the earlier eight-image playback slid at actual travel speed. Keep its accepted motion narrowly; changed cloth must be reviewed again. Determine other action counts from real timing and readability, not copied walk counts.
- Never fit individual frame bounds or move pivots to conceal sliding. Keep exact ground calibration, coherent scene zoom and original gait/world-speed relation. A future default scale change requires fresh world-motion/contact qualification, not only a CSS resize.
- Atlas pages may exceed256px because they aggregate small frames. Use a declared shared union crop/offset contract and padding/extrusion, while retaining each frame's identical ground anchor. Packing/cropping requires explicit compiler/manifest support; it is not currently established production behavior.

## Batch economics and runtime

The reusable investment is the whole identity model/material plus the archetype motion, not independent image prompts. One reviewed rig can animate several compatible outfits, each keeping its own identity and qualified action set. Freeze source model, camera, materials, lights, pose tracks, frame times and tool version. Export finite reproducible jobs with input/output hashes and retained failure history. Never overwrite a frozen producer directory.

Measure atlas cost before roster fanout. Frozen003 is394,265PNG bytes/3MiB decodedRGBA for only one direction of one walk; eight equally packed directions would be24MiB decoded before other actions or identities. That is a planning estimate, not a measured roster budget. Use shared union crops, page banks and bounded loading/unloading only after pixel/pivot contracts pass. Do not assume compressed downloads equal decoded memory or assume one48-frame loop is cheap at roster scale.

Presentation reads simulation state: traveled distance controls walk phase; stop/pause/reconnect/terrain behavior remains authoritative. Sprite markers trigger cosmetic effects/sound, never resource transfer, damage or victory. The current elapsed-time walk clock, exact physical-camera reconciliation, production crop/padding, WebGL requirement and dense-crowd acceptance remain open.

## Current atomic task and actual status

The work order is /home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha-art-lease/canonical-villager-binding-005/WORK_ORDER.json. At this plan checkpoint, producer /root/arm_tool is running; source/evaluation are not yet delivered. Check its live agent/session state before restarting or reissuing work. A saved work order is not proof of a live job.

Binding005 is an internal geometry tool order only: deterministic knee-aware deformation of the complete004 lower garment/panels on frozen003 poses. Sourceframes0, AIcalls0, one501-phase geometry evaluation; no art render, loop export, runtime edit or fanout. Its numerical clearance result cannot qualify appearance, actual cloth motion or physical collision correctness. Parent will review its exact evidence before integration. Any failed samples stay held; no retry batch is authorized.

The full game remains NOT COMPLETE. No final graphics acceptance is recorded by this plan.

VI: Mục tiêu là đồ họa minh họa chân thực như asset gốc, nhìn rõ ở kích thước chơi thật. Dựng một nhân vật hoàn chỉnh có trang phục/vật liệu thống nhất, kiểm tra diện mạo trước, kiểm tra vòng đi sau, rồi mới tám hướng và các nhóm unit. Các hình khối hiện tại chỉ là khung chuyển động. Làm xong các kiểm tra số học hoặc đóng atlas không đồng nghĩa đồ họa đã đạt.
