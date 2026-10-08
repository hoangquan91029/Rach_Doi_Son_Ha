# Internal UNSEALED_DIAGNOSTIC only

CLI: `PYTHONDONTWRITEBYTECODE=1 python3 tooling-v6/diagnose_lower.py ABS_PROPOSAL_JSON ABS_NEW_OUTPUT_DIRECTORY`

Proposal exact keys:
- schema: `south-lower-diagnostic-proposal/v1`
- status: `UNSEALED_DIAGNOSTIC`
- purpose: `ACTUAL_ORIGINAL` (or clearly synthetic `NON_ART_TEST_FIXTURE`)
- raw: {path: absolute original, sha256: byte hash, rgbaSha256: decoded hash, width:1254, height:1254}
- endpoints: {elbow:{xy:[measured x,y],method:"observed_original",uncertaintyPx:measured uncertainty,evidence:inspection evidence},wrist:same fields}
- calibration: {scale:positive uniform number,rotationRad:number,translation:[tx,ty]}; compute once with `inspect_partial.endpoint_similarity(elbowXY,wristXY,180)` after inspection. No source coordinates invented here. Numeric correspondence tolerance 1e-6 verifies calculation only; it does NOT assert anatomical measurement precision.
- layerOrderProposal: ["arm_right_lower_hand","arm_right_upper","core_head_torso_pelvis"]
- ownershipClarification: {path:absolute BASE/component-ownership-clarification-v1.json,sha256:"9a874ebd63262f54a99df53c84fd4404c354ba0f9290e32ac4888d9dde363076"}

Uses sealed v4 math and sealed core-v3/upper-v1. New lower is held unsealed internally and never passed off as a sealed sidecar. Additive ownership clarification binds bare forearm/hand and upper sleeve cuff without editing v3. Full original canvas quad preserves all source alpha, one uniform fit, directed 180 bone, camera once, root654/1140. Rest combines RIGHT shoulder/elbow/wrist from unchanged F0 angles with only body shift/bob neutralized. Output: rest +F0/F2/F4/F6 at1254/627/fixed38 whole canvas, plus labeled QA. Proposed lower-behind-upper/core order remains unapproved for nine parts. Six originals absent: no finished keys, loop or qualification.

Tests: `PYTHONDONTWRITEBYTECODE=1 python3 tooling-v6/test_diagnostic.py` (8 passing NON_ART tests: independent diagonal angle/scale oracle, fullcanvas fringe coverage topology, endpoint mismatch, asymmetric scale field refusal, unsealed-only status, custody mismatch, duplicate source slot, existing output refusal). These tests are not graphics or art approval evidence. Actual source integration awaits parent original/proposal; projected fullcanvas bounds can truthfully refuse a source requiring out-of-canvas mesh.
