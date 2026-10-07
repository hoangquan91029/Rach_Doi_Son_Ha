# D00 controlled-2D villager walk — art component contract (proposal only)

## Locked reference and limits

The user explicitly selected a controlled 2D rig built from the existing character identity. This supersedes the skill's older identity-frame default for this task. Use the existing D00 villager master only as static identity, material, proportion, and camera reference: `/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha/docs/art/characters/villager-neutral-D00-screen-ESE/raw.png` (SHA-256 `145b976ffd1bdf563cb5da78806547e6849424054f2c26fc297e155a0b366e94`), 1254 × 1254 RGBA. The master is not a cutout/trace source and must not be divided, repaired, repainted, or reused as rig art. Do not attach rejected or review-only motion images.

Keep the elevated screen-ESE three-quarter view, D00 world-east direction, head/hat identity, body volume, face, cloth, sash, wraps, sandals, and palette. Use the source canvas 1254 × 1254, fixed root `(650,1140)`, and one declared world scale `38/1254`. No per-frame bounds fitting, mirroring, crop, or scale/translation changes. No Blender, new identity, extra props, new source schema, or runtime/manifest work.

## Minimal original-part set

Exactly 11 distinct whole-body anatomical components are proposed, one original transparent PNG per component. Arms and legs have persistent joints. Hands stay integrated with the forearms, reducing part count while preserving elbow motion. The feet remain separate from shins so planted soles can hold contact while ankles articulate. No decorative micro-detail request; all overlaps should remain readable at 38/1254 gameplay scale.

| Order / ID | Component | Rest axis and natural landmarks | Materials and joint overlap |
|---|---|---|---|
| 1 `core_head_torso_pelvis` | One rigid head, face, hair/beard, nón lá, neck, tunic, sash, pelvis/seat and upper-trouser core | Root `(650,1140)`; anatomical centerline hat/head → neck → sternum → pelvis; shoulder and hip attachments left as overlapping boundaries, not holes | Exact identity from master; retain complete body volume, garment layering and face. No face redraw or separate hat. Neck/shoulder/hip edges carry enough hidden overlap for articulation. |
| 2 `arm_far_upper` | Far/screen-left upper arm with sleeve | Shoulder → elbow | Pale tunic sleeve; round, naturally covered shoulder/elbow overlap; rest axis follows master. |
| 3 `arm_far_forearm_hand` | Far/screen-left forearm and empty hand | Elbow → wrist/fingertips | Skin and sleeve cuff; overlaps upper arm at elbow; natural wrist connection. |
| 4 `arm_near_upper` | Near/screen-right upper arm with sleeve | Shoulder → elbow | Same material/palette as master; hidden overlap at shoulder and elbow. |
| 5 `arm_near_forearm_hand` | Near/screen-right forearm and empty hand | Elbow → wrist/fingertips | Skin and sleeve cuff; hidden elbow/wrist joins; no prop. |
| 6 `leg_far_thigh` | Far/screen-left trouser thigh from covered hip to knee | Hip → knee | Dark loose trouser fabric; keep unbent rest texture, overlap under tunic at hip and over shin at knee. |
| 7 `leg_far_shin_wrap` | Far lower leg, trouser cuff and pale shin wrap | Knee → ankle | Preserve wrap and knot silhouette; hidden overlap under thigh at knee and over sandal top at ankle. |
| 8 `foot_far_sandal` | Far foot and sandal | Ankle/heel → toe/sole | Preserve sandal straps and foot shape; clear sole edge for planted contact; overlap under wrap at ankle. |
| 9 `leg_near_thigh` | Near/screen-right trouser thigh from covered hip to knee | Hip → knee | Same master material, loose profile; hidden hip/knee overlap; no pre-bent knee crease. |
| 10 `leg_near_shin_wrap` | Near lower leg, trouser cuff and pale shin wrap | Knee → ankle | Same wrap design; hidden overlaps at knee and ankle. |
| 11 `foot_near_sandal` | Near foot and sandal | Ankle/heel → toe/sole | Separate sandal with clear sole/contact edge and ankle overlap. |

## Finite authoring call plan

Maximum 11 original component calls total, one call per listed component, zero automatic retries. Order: core; far upper arm; far forearm/hand; near upper arm; near forearm/hand; far thigh; far shin/wrap; far foot/sandal; near thigh; near shin/wrap; near foot/sandal. Each call attaches the locked master for identity/style/camera only, and requests one isolated component on genuine transparent RGBA. State its component ID, side ownership, proximal/distal landmarks, rest axis, required hidden overlap, and no extra body/limbs/labels/markers. Parent authorized only the first `core_head_torso_pelvis` call (one call, zero retries); that call has now been spent and its raw is pending review. The remaining ten component calls are closed until the parent reviews this core result and explicitly opens another call. A problematic component remains held; do not silently spend a retry or add more pieces.

For every returned raw, preserve original bytes and request metadata. Inspect complete source, alpha, identity and scale. Create a component sidecar with raw byte hash, decoded RGBA hash, actual dimensions, component/order IDs, named proximal/distal landmarks measured on that raw, static transform into rest/source space, and uncertainty. Unknown or hidden centers stay unresolved until visible evidence supports a measurement; do not fill placeholder coordinates. One measured static uniform transform per component is allowed for assembly; joint motion transforms remain the rig programmer's responsibility.

## Landmark convention and measurement

Use natural landmarks rather than colored joint markers: shoulder center, elbow center, wrist center, hip center beneath tunic, knee center under cloth, ankle center at wrap/sandal junction, heel, toe tip, and sole contact line. Each part must include its named proximal and distal endpoint with sufficient overlap that the animator can set the joint center inside the image. The near/far side is defined by screen placement in the inspected D00 master, never inferred from filenames.

Coordinates in `landmarks.json` are rough visual hypotheses on the master canvas, not sidecar/calibration values. Measure final attachment coordinates from actual component raws after approval and authoring; report any ambiguous landmark as unresolved. The hidden hip and shoulder centers have wider uncertainty than visible elbows, ankles, heels and toes.

## Whole-loop motion acceptance target

The rig programmer owns motion curves, contact locking, easing and draw order. Define eight phase keys at 100 ms phase landmarks across an 800 ms loop. Render the persistent track as 24 evenly spaced samples at 33.333 ms (loop duration 800 ms) for the initial normal-speed review, interpolating joints between phase keys rather than holding each key for 100 ms. Review at fixed 38/1254 full-canvas scale. Keep root `(650,1140)` fixed; permit only small natural torso bob and counter-rotation, with no body squash/stretch. Near/far arms counter-swing opposite their legs. World-distance stride and playback cadence remain provisional until measured part reach and no-slide contact motion are reviewed; never stretch bones to force a one-tile stride.

| Frame | Phase | Leg contact and transfer target |
|---|---:|---|
| F00 | 0 ms | Near/right foot flat contact; far/left leg trails. |
| F01 | 100 ms | Down/weight settles over near support; far toe releases. |
| F02 | 200 ms | Near support mid-stance; far leg swings through, foot visibly airborne. |
| F03 | 300 ms | Far leg advances and lowers; near leg moves behind. |
| F04 | 400 ms | Far/left foot makes the opposite flat contact; near/right releases and trails. |
| F05 | 500 ms | Down/weight settles over far support; near toe releases. |
| F06 | 600 ms | Far support mid-stance; near leg swings through, foot visibly airborne. |
| F07 | 700 ms | Near leg advances and lowers toward next F00 contact. |

Review foot ownership at both contacts, the actual lifted-foot gaps in both passing poses, planted-sole stability through stance, natural knee/elbow flexion, body identity/volume, root/camera stability, and F07→F00 seam. A contactA/contactB pair is not a complete loop. No art call, loop claim, qualification, integration, or fanout follows from this proposal alone.
