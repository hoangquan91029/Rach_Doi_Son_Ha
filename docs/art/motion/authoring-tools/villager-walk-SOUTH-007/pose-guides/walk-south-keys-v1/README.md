# MODEL_ONLY South four-key geometry guide

Status: PREPARATION_ONLY / NON_ART / NOT_ANIMATION / parent guide audit pending. No image calls, character-pixel edits, completed illustration, animation export, runtime integration or motion approval. Eight actual static identities are still incomplete, so finished walk-frame authoring stays closed. Historical diagonal-v1 anatomical labels are not reused: South forward=(0,+depth), anatomical LEFT=(forward.depth,-forward.x)=(+X,0), viewer RIGHT.

Inputs: the inspected parent-accepted South full-body original SHA25668a7fb9a71ae614f7c01432b1270e7a25071975667cfdf082ae02326d97678db supplies gross proportions only. Hidden hips/knees are authored hypotheses, with ±60sourcepx uncertainty, not measured anatomy. No pixels are traced/extracted/copied. Source/root/canvas stay1254×1254/(654,1140); whole-canvas review size38logicalpx. The game2:1 affine ground transform is used;26.565° denotes its ground-slope convention and does not assert an exact physical perspective camera.

Four still keys: F0/F2 LEFT support (viewer-right), F4/F6 RIGHT support (viewer-left). F0/F4 trailing swing sole12modelpx aboveground; F2/F6 passing sole80px aboveground. Sole dimensions160depth×64width are fixed. Thigh260/shin240 and upper arm200/forearm180 stay constant in3D. Sagittal IK is constrained first; projected knees can look almost straight from South because depth flexion is foreshortened. The numbers, not a front-view painted knee bend, describe this hypothesis. Coarse front cloth masks pelvis/proximal thighs; both knees/shins/feet remain readable. Capsule/colors are structural guide marks, not finished parts or final art.

Support ankle local depth is `-100+160-640*(timeWithinHalfCycle/600)`. Root/world depth advances`640*time/600`. Their sum, including both heel/toe endpoints, stays constant during each support half. All eight nominal phase timestamps and the600ms seam are checked numerically; only four still key guides are rendered. No proxy full-body animation is produced. `world-contact-grid.png` is a coordinate plot, not character playback.

Reach first: leg length500, worst vertical separation440 allows theoretical depth reach237.49; selected excursion160 retains margin. This produces a full-cycle projected source stride320px (9.69697logicalpx), or0.5079106Euclideanworld units alongSE using27/√2logicalpx per world unit. Nominal600ms gives0.8465world/s. Actual villager base2.1 would require241.862ms; this faster cadence is disclosed, not sealed. Eventual playback must use actual traveled Euclidean distance after terrain/supply modifiers and must receive real illustrated contact/grid/motion review. Do not force1tile or claim these guides solve that visual calibration.

Runnable, using existing Python and Playwright Chromium only:

- `python3 build-guides.py` emits coordinate/contact plans and eightSVG guides (4keys×plain/QA), checks inputSHA and numerical reach.
- `python3 verify-guides.py` checks source preservation, fixed segments, viewer ownership, binary support, all phase stance counter-travel and cadence math; PASS is technical only.
- `node render-guides.mjs` renders eight1254PNGs,50%QA contact sheet, fixed38 still strip and numerical contact-gridPNG.

Actual PNGs inspected locally after correcting one SVG whitespace parsing defect. Final contact sheet has a connected torso/head, expected side ownership, support transfer and lifted passing sole; fixed38 stills preserve one whole-canvas scale. It does not establish identity/art/motion quality. Sealed hashes bind final builder/plan/rendered guides only; parent must audit before any painting. Rerunning tools changes custody outputs, so treat this sealed package as immutable evidence.
