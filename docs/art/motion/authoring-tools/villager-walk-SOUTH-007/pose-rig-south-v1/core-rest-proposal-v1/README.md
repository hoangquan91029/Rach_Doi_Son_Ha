# South core rest proposal v1

Status: MODEL_ONLY / PARTIAL_REST_INSPECTION, unsealed and pending parent review.

This packet proposes one static uniform calibration for the preserved core original. The source is immutable. Previews are diagnostic, not a whole-character assembly, accepted key, runtime rig, or approval.

## Calibration

Use the reported four-visible-feature similarity fit: scale 0.672919808, rotation -0.000318866 rad, translation (206.170592, 16.511619). Approximate visible correspondences and source hashes are in `proposal.json`. The fixed full-character root remains (654,1140); the core is not translated to its bottom edge. No anisotropic scaling, bbox normalization, source edit, or per-frame fit. The reported residual range is 2.96–6.40 px, so calibration remains provisional.

## Proposed attachment semantics

The shoulder points are authored arm-underlap conventions placed on visible cloth caps. They are not measured anatomical joints. The two hips are explicitly hidden-joint hypotheses under the tunic/sash, with broad uncertainty; they must be reviewed before any sidecar can be sealed. Existing overly wide shoulder targets are excluded.

## Views

- `partial-rest-core-native.png`: uniformly mapped core on its fixed 1254 canvas.
- `partial-rest-core-fixed-38px.png` and `...-3x.png`: exact full-canvas 38 px scale and enlarged inspection view.
- `partial-rest-comparison-south-native-QA.png`: diagnostic overlay against canonical South with proposed points and fixed root marker.
- `partial-rest-comparison-south-fixed-38px-QA.png`: same comparison at 38 px.
- `source-landmarks-QA-only.png`: source-space point annotation; raw image is untouched.

No v3 inspector was run because prior rest anchors were inconsistent; this proposal requests parent review of the model targets before a truthful sidecar is authored.
