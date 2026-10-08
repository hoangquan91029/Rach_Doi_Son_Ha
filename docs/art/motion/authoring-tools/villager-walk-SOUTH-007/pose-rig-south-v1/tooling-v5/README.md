# Partial rest inspector v5

Preparation only. Actual upper-arm original and measured landmark/calibration proposal are pending. No coordinates, calibration or source sidecar are authored by this tool before original inspection. No art call or runtime change.

Run from this directory:

```
python3 -B -m unittest -v test_partial.py
python3 -B inspect_partial.py arm_right_upper /absolute/sidecar.json /existing/parent/new-output --order arm_right_upper,core_head_torso_pelvis --purpose ACTUAL_SOURCE_PROPOSAL
```

The sidecar uses sealed v4 `south-bitmap-rig-sidecar/v3`: immutable raw byte/decoded RGBA custody; observed proximal/distal coordinates with evidence and uncertainty; one uniform raw-to-unforeshortened bone-plane calibration; full nonzero-alpha semantic coverage. Core remains the approved actual core. Original/source pixels are never rewritten. Endpoint_similarity returns a numerical fit proposal only after supplied inspected landmarks; it is not an anatomical measurement.

Right upper arm is 200 model units before the single camera projection. Neutral partial-rest screen length is approximately173.33px. Calibrating the raw directly to173.33 and projecting again is refused because the sidecar distal must map to200. All four existing key geometries are validated without producing key PNGs or altering the plan. The stationary inspection undoes only the F0 body weight shift/bob for the relevant limb; it is not F0 finished key artwork.

Occlusion order must be supplied explicitly and remains a proposal for visual review; anatomical LEFT/RIGHT does not imply fixed near/far. Integrated lowerleg/sandal parts are excluded from this small rigid-limb inspector. No foot geometry changes. Existing trailing-foot flat lifted12px hypothesis remains unqualified: actual toe-grounded heel-rise needs original-foot landmark/rigid-roll review before four finished key acceptance.

Outputs are native1254RGBA, whole-canvas38RGBA and separate labelled QA PNG, plus byte/decodedRGBA custody receipt. Status is PARTIAL_REST_INSPECTION_REQUIRES_SOURCE_REVIEW; candidate/full-character/finished-key/motion/final-art flags are false. Missing7 originals are explicitly disclosed. Existing output refuses overwrite; all validation precedes staging; publication uses sealed v4 atomic no-replace rename (not a power-loss durability claim). Five tests use temporary NON_ART numeric texture only and remove outputs afterwards. Technical success does not qualify art, contact or motion.
