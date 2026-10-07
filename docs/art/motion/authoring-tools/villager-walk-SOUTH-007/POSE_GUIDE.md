# Controlled South eight-frame walk — authoring specification only

No finished South reference, selected key poses or accepted walk currently exists. This document is a pose plan, not a proxy animation or approval. D00 lease006 is held; its raw components/partials are preserved and never renamed South.

**Direction:** screen-down/front-facing SOUTH = engineD01/worldSE. In this view anatomical LEFT is normally viewer-right and anatomical RIGHT viewer-left. Lock these identities in the actual inspected South reference; no near/far substitution, limb swapping or mirrored half-cycle. Existing D00 master is identity/material reference only. Do not animate before the true South reference is inspected. Complete and seal eight actual full-body static identity views with one byte-bound review BEFORE authoring any animation. This requires eight stills, not eight motions. Only the South walk opens after that identity gate.

**Canvas/anchor:** propose1254×1254 RGBA and one root(654,1140) between the ground feet. Confirm and seal that pivot once against the real South reference. Whole-canvas world scale38/1254; every frame uses identical canvas, root and scale. Anatomical shoulders/hips, leg segment lengths and footwear dimensions come from actual reference/component measurements, with authored hidden-joint hypotheses marked as such and uncertainty retained. Source support/body bob is small and leg-driven; do not shift or fit entire images to fabricate walking.

| Frame | Time ms | Hold ms | Key | Anatomical support | Swing / pose requirement |
| --- | ---: | ---: | --- | --- | --- |
| F0 | 0 | 80 | YES | LEFT | LEFT forward contact receives weight; RIGHT behind. Soles, knees and arm counter-swing visibly establish opposite limbs. |
| F1 | 80 | 70 | — | LEFT | Body settles slightly; LEFT accepts weight; RIGHT heel lifts. |
| F2 | 150 | 80 | YES | LEFT | RIGHT knee bends and passes below pelvis, sole airborne with a readable gap; LEFT remains planted. |
| F3 | 230 | 70 | — | LEFT | LEFT finishes support/push; RIGHT swings forward toward contact; controlled body rise. |
| F4 | 300 | 80 | YES | RIGHT | RIGHT forward contact; LEFT behind. This must visibly differ from F0 support. |
| F5 | 380 | 70 | — | RIGHT | Body settles; RIGHT takes weight; LEFT heel lifts. |
| F6 | 450 | 80 | YES | RIGHT | LEFT knee bends and passes beneath pelvis airborne; RIGHT remains planted. |
| F7 | 530 | 70 | — | RIGHT | RIGHT pushes; LEFT advances toward nextF0; no identity/root jump at600ms seam. |

Four key poses F0/F2/F4/F6 are authored and visually validated first. The contact gate is binary: F0/F4 same support rejects the entire cycle. Validate both passing feet as airborne while the declared opposite limb supports. Only then derive F1/F3/F5/F7 from canonical South reference, previous selected actual frame, next selected key and the controlled pose specification. No independent text-only frame invention.

Internal rigs/IK may control pose; every final frame must be a complete finished illustration when paused. Baked paper-puppet joints still fail final art quality. Any illustrated redraw/finish keeps raw sources, prompts and custody; no labels or visible bones enter final frames. Temporary L/R labels belong only in QA overlays/contact sheets.

**Foot contact:** first constrain fixed leg lengths and reachable target/sole range. Do not force1tile stride or imply0.6s nominal timing equals1.26tiles at base speed. For eventual displacement playback, actualworld unit-distance along SE projects vertically by27/√2≈19.092logicalpx (because simulation speed uses Euclidean world distance). One diagonal tile step(1,1) projects27px but travels√2world units. For any measured reachable source stride S, world stride hypothesis is `S*(38/1254)/(27/√2)`. Body travel must be countered by the planted support foot's local stance motion, so world sole position stays approximately fixed. A reviewed stance/contact track, actual grid playback and simulation-following cadence calibration decide that hypothesis; source frames do not bake large world translation.

**Visual gate:** contact sheets at100%,50%,fixed38 whole-canvas; all frames annotated SUPPORT and SWING below the image; nominal600ms loop and a moving grid diagnostic once a reachable stride is recorded. Parent scores Identity,Anatomy,LegPhase,FootPlacement,MotionReadability,ArtQuality,LoopQuality,RTSReadability. All≥8/10 and LegPhase exactly10/10; real independent motion review precedes animation fanout/runtime integration. Metadata/clock tests do not qualify motion.
