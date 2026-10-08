# Internal four-slot split diagnostic only

Run:
`PYTHONDONTWRITEBYTECODE=1 python3 ABS_BASE/tooling-v7/diagnose_split.py ABS_FOREARM_PROPOSAL ABS_HAND_PROPOSAL ABS_ORDERS_JSON ABS_NEW_OUTPUT_DIR`

Both proposals have exact keys `schema, partId, status, purpose, raw, endpoints, calibration, sourceEvidence`.

Forearm: schema `south-right-forearm-proposal/v1`, partId `arm_right_forearm`, endpoints `elbow,wrist`, target local [0,0]/[0,180].

Hand: schema `south-right-hand-proposal/v1`, partId `hand_right_palm`, endpoints `wrist,fingertip`, target local [0,0]/[0,65]. Nominal65 is a pending assembly hypothesis, not accepted hand proportions.

Both status `UNSEALED_DIAGNOSTIC`; purpose `ACTUAL_ORIGINAL` or explicit `NON_ART_TEST_FIXTURE`.

Raw exact fields `{path:absoluteOriginal,sha256:byteHash,rgbaSha256:decodedRGBAHash,width:1254,height:1254}`.

Each endpoint exact fields `{xy:[inspectedRawX,inspectedRawY],method,uncertaintyPx,evidence,anatomicalJointMeasured:false,observableAnatomicalEvidence:null}`. Proximal elbow/hand wrist may use `authored_hidden_hypothesis`; otherwise `observed_original` describes a visible contour convention. Distal wrist/fingertip use observed_original. Hidden hypotheses remain false/null. A true anatomical flag requires observed_original plus separate nonempty observableAnatomicalEvidence; schema verification does not establish visual anatomy. Numeric fit tolerance1e-6 is calculation consistency only, not inspection precision.

Calibration exact fields `{scale:positiveUniformNumber,rotationRad:number,translation:[tx,ty]}`. Compute once after actual source inspection using v5 `inspect_partial.endpoint_similarity(proximalXY,distalXY,180)` for forearm or65 for hand. No source coordinates supplied/invented by this tool.

SourceEvidence exact fields `{callRecord:{path:absolute,sha256:hash},rawReview:{path:absolute,sha256:hash}}`. Byte custody checked; parent separately verifies actual original authoring provenance, component ownership and visual quality. No approval inferred from purpose or review-file existence. Three held combined-lower byte hashes forbidden. Different slots require unique byte and decodedRGBA hashes.

Orders JSON exact fields `{schema:"south-four-part-orders-proposal/v1",layerOrderByPose:{REST:[...],F0:[...],F2:[...],F4:[...],F6:[...]},evidenceByPose:{REST:"reason",F0:"reason",F2:"reason",F4:"reason",F6:"reason"}}`. Every order is an explicit back-to-front permutation of core_head_torso_pelvis,arm_right_upper,arm_right_forearm,hand_right_palm. No defaults. RIGHT wrist model depth +10/-100/-210/-100 for F0/F2/F4/F6; body baseline-100. Equal depths require authored reasoning and actual assembly review; forearm can cross body depth, so one-part layer order remains a visible-review proposal. These are four-part orders, not full11 acceptance.

Sealed v4 dependencies and v4-hand-split contract hash63859443aad0ec34c44672315b52e45823c03d294bffe74741733f0e43322083 are pinned; upper original/sidecar/review/seal and core remain unchanged. New forearm uses exact sealed projected_vertex with its own partId (v4 arm classifier naturally resolves elbow/wrist180). New hand projector explicitly anchors RIGHT wrist, worldX width, downZ long axis65, then fixed camera once. Raster helper uses sealed affine_inverse and the same premultiplied-alpha indexed-triangle partition overwrite; no monkeypatch or sealed-sidecar masquerade. Full original canvas quad retains all alpha. No crop/mirror/aniso/staticfit-per-pose/cleanup.

REST neutralizes F0 body shift/bob on a private copy only. Original poseplan unchanged. Both attachment conventions meet the same projected wrist, tips remain wrist+[0,0,-65]; numerical handoff does not prove painted seam quality. Native1254/half627/fixed38 PNGs for REST/F0/F2/F4/F6 plus labeled side-by-side sheets at all three sizes (18PNG outputs) state PARTIAL4/MISSING7/NOT KEY. Receipt includes separate bounds perpose, source custody, proposal orders/evidence, semantics and wrist/handplane reports. No full11 baker, finished key, loop, animation/contact qualification, runtime or repo changes.

Tests: `PYTHONDONTWRITEBYTECODE=1 python3 ABS_BASE/tooling-v7/test_split.py`. Twenty NON_ART tests cover distinct schema/slot IDs, held-source and byte/decoded duplicate rejection, diagonal uniform calibration, mirrors/aniso/crop/missing fields, anatomy truthfulness, allpose explicit order/duplicates, nooverwrite, bounds, wrist handoff/fixed facing, source/RGBA custody, exact sealed forearm projection/raster equivalence and full temporary NON_ART diagnostic publication/receipt (fixture output removed on exit). No fixture is actual new art evidence. Parent must review code and actual-original outputs before seals.
