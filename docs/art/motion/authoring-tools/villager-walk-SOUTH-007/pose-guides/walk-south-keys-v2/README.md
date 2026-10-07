# MODEL_ONLY South four-key geometry v2

PREPARATION_ONLY / NON_ART / NOT_ANIMATION. Parent guide audit pending. V1 is preserved byte-for-byte: verifier rechecks its sealed file hashes. No art/image calls, finished illustration, motion approval or runtime change. Eight-static-view finished-frame gate remains closed.

V2 corrects the center-aligned body of v1 with an authored lateral weight-transfer hypothesis. F0 pelvis/torso/head shift+25sourcepx toward anatomical LEFT (viewer-right), F2+55; F4−25 toward RIGHT (viewer-left), F6−55. The root remains(654,1140),1254canvas/whole-canvas38logicalpx. Torso/head/hat/shoulder vertices follow actual skeleton coordinates; no SVG image translation, crop, bbox fit or scale change shifts the entire image. Both ankle/heel/toe contact tracks retain v1 coordinates exactly.

General3D two-bone IK projects a forward-depth pole perpendicular to the actual hip–ankle vector, handling lateral hip motion while ankleX stays locked. Thigh260/shin240, upperarm200/forearm180 and sole160depth×64width remain fixed. The support leg inclines under the shifted pelvis; both knees stay at least30sourcepx below the coarse cloth hem. QA floor-foot outlines and gap arrows show passing sole80sourcepx above its own orthographic ground plane; trailing contact-key swing sole remains12px aboveground. F0/F4 are weight-arrival contacts rather than symmetric neutral stance. These are model hypotheses, not measured anatomical landmarks, mass distribution, equilibrium or finished walking poses.

Body axes are679/709 at F0/F2 and629/599 at F4/F6; sole centers remain754(anatomicalLEFT) and554(RIGHT). Shift is toward support, not a claim that the exact unknown whole-body center of mass falls inside a measured sandal polygon. Reference identity, soft tissue, cloth motion and natural body lean require later finished-art review. All source appearances will come from the actual master, not these capsules/colors.

South forward=(0,+depth); anatomicalLEFT=(forward.depth,-forward.x)=(+X,0)=viewerRIGHT. Game2:1 affine ground projection`(654+x,1140+.5depth−z)` stays fixed;26.565° is its ground-slope convention, not an exact physical perspective-camera calibration. Accepted South SHA68a7fb9a71ae614f7c01432b1270e7a25071975667cfdf082ae02326d97678db is inspected only for gross proportions; original pixels unchanged and not copied/traced/extracted.

Contact table/sole endpoints are identical to v1: support local backward depth exactly cancels nominal world-root travel. Reach-first full stride remains320projectedsourcepx /9.69697logicalpx /0.5079106Euclideanworld units.600ms nominal review implies0.8465world/s, whereas base2.1 would imply241.862ms. Actual distance/cadence and real illustrated motion/contact must be reviewed before sealing runtime playback; no1tile stride forced.

Runnable numerical and Chromium-only geometry rendering:

- `python3 build-guides.py`: emits numerical plan/contact table and four plain+QA stillSVGs.
- `python3 verify-guides.py`: checks original sourceSHA, v1 sealed hashes, fixed3D lengths, side/support labels, unchanged soles/contact table, lateral skeleton offsets, exposed knees and stride/cadence math.
- `node render-guides.mjs`: renders eight1254PNGs,50%QA contact sheet, whole-canvas38still strip and numerical world-contact plot. No character animation export or proxy motion qualification.

Final native F2/F4,50%sheet and fixed38strip inspected. Technical checks PASS; parent guide/anatomy/identity/motion/art acceptance remains pending. Treat sealed outputs as immutable evidence; no further v1/v2 writes until parent requests a new version.
