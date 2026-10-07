# South finished-frame atlas tooling

Preparation only: zero new image calls, zero selected South frames, zero atlases compiled from actual finished originals, zero runtime integration. `../POSE_GUIDE.md` supplies the corrected anatomicalLEFT/RIGHT four-key-first sequence. `../job-proposal.json` has unresolved reference/custody/review fields and deliberately fails preflight.

BEFORE animation authoring, complete actual N/NE/E/SE/S/SW/W/NW full-body static originals with fixed camera/canvas and one sealed review binding all eight hashes. Then obtain the inspected South directional reference and four validated key poses. Only afterward, fill the job with eight original finished whole-character RGBA paths, immutable hashes and authoring receipts. Bind the actual four keyframe hashes to a parent review receipt. Source canvas1254, a single sealed ground pivot and uniform whole-canvas presentation scale remain fixed. Metadata checks authenticate declarations; they never infer correct anatomy, contact or identity from labels.

```
python3 tooling/atlas.py preflight job.json
python3 tooling/atlas.py compile job.json --out compiled --cell 256
python3 -m unittest discover -s tooling -p 'test_*.py'
```

Compiler output:

- PNG atlas: four columns/two rows, uniform complete-canvas runtime cells. Originals remain unchanged. `--cell1254` selects pixel-preserving full source cells; default256 performs a declared common whole-canvas Lanczos reduction before packing.
- `animation.json`: animation/state walk, numeric direction1, explicit SOUTH/D01/worldSE mapping, computed x/y/width/height and rectangle, fixed source/cell pivot, duration80/70/80/70x2, precise timestamps, original byte/decodedRGBA custody and frame events.
- Events are optional declarative presentation metadata. Current walk contacts emit `FOOT_CONTACT_LEFT` atF0 and `FOOT_CONTACT_RIGHT` atF4, each `offsetMs:0`. No browser event callback can change authoritative movement, damage, resources or victory. Simulation remains fixed-tick.
- Contact sheets atnative/half/wholecanvas38px, labeled anatomical support/swing below each actual frame. Normal nominal600ms GIF preview.
- Optional moving grid GIF only after `qaStrideWorldTiles` is a disclosed reachable contact hypothesis. Without it compiler writes explicit pending-grid status, never inventing motion evidence. SE unit-distance projection is27/√2px, preserving simulation's Euclidean distance semantics.

Whole illustrated PNGs are the only runtime inputs. No original runtime body parts, visible joints or proxy skeleton are emitted. The final metadata remains CANDIDATE_REVIEW_ONLY with independentMotionReview PENDING and runtimeIntegrated false. Parent visible review and the binary contact gate remain mandatory.

Grid stride is validated during preflight before any output write. Existing nonempty compilation output is refused; choose a fresh directory. Tests generate explicitly NON_ART numeric fixture PNGs in temporary directories only; their technical results cannot qualify motion or artwork.
