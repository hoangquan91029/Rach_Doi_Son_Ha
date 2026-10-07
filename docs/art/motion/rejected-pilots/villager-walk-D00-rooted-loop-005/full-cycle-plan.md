# Finite D00 walk-cycle plan

## Bounds and timing

The 004 raw is handed off unchanged as current-job selected F01 at 100 ms, classified REVIEW_ONLY_EARLY_SWING_DIAGNOSTIC. Its original producer name F02 is retained in source metadata; the 005 selection record defines this sequence slot. This is not motion approval or runtime acceptance. The proposed work therefore authors the other seven frames: maximum seven ImageGen calls total, exactly one per slot, no retries. The first new call authors F04 at 400 ms from F01 at 100 ms and must pass parent review before any later call. A failed key ends the attempt.

The canonical sequence is F00–F07 at 100 ms each (800 ms total). Generation is key-first, then in-betweens. The selected F01 is the actual unchanged 004 raw and is not regenerated.

| Slot | Time | Phase and contact ownership | Call order / proposed attachments |
|---|---:|---|---|
| F00 | 0 ms | Near/right contact, near foot lower-right and flat; far leg trails | Key call 2: master + selected F01 predecessor + selected F04 next key + new F00 model-only guide. Do not attach pilot-001 F00. |
| F01 | 100 ms | Early swing: near/right support; far/left leg raised, source raw from 004 | Imported selected review-only key; unchanged raw, original source label F02. No ImageGen call. |
| F02 | 200 ms | Near/right support; far/left leg swings forward through passing, foot airborne near body; arms counter-swing | Key call 3: master + selected F00 predecessor + selected F04 next key + new F02 guide. This is newly authored 005 F02. |
| F03 | 300 ms | Up transition; far leg lowers toward contact | In-between call 5: master + selected F02 predecessor + selected F04 next key + F03 guide. |
| F04 | 400 ms | Far/left contact lower-right; near/right leg trails with heel lifted | First new call: master + selected F01 predecessor (unchanged 004 raw) + new F04 bridge guide. |
| F05 | 500 ms | Down after far contact; settle onto far support | In-between call 6: master + selected F04 predecessor + selected F06 next key + F05 guide. |
| F06 | 600 ms | Far/left support; near/right leg swings forward, foot airborne; arms counter-swing | Key call 4: master + selected F04 predecessor + selected F00 next key across the wrap + new F06 guide. |
| F07 | 700 ms | Up transition; near leg advances toward F00 | In-between call 7: master + selected F06 predecessor + selected F00 next key + F07 guide. |

## Attachment rules for the bounded proposal

The master is attached to every new call as the sole identity, appearance, proportion, palette and camera authority. Each target uses a model-only phase guide for ownership/contact/timing, never body proportions. Current-job selected predecessor and next key are attached when available, as shown above.

The only inherited frame in the current sequence is the unchanged 004 raw selected as F01; its parent review status is REVIEW_ONLY_EARLY_SWING_DIAGNOSTIC. The proposed first F04 call uses it as the selected F01 predecessor, not as an unselected exception. It is not reattached after F04. The old pilot-001 F00 and all rejected F04s from 001/002/003 remain review evidence only and are never attached. The F01 support foot offset (~85 source px / 2.6 gameplay px right of root) is preserved and disclosed. Keep canvas and body root fixed; no crop, translation, mirror, resize or bbox fit. Stop if whole-body root drift is visible.

## Completion gate

After seven new calls and eight selected frames exist, review the actual 800 ms loop at 100 ms/frame and fixed 38/1254 full-canvas scale with root (650,1140). Check support transfer, both passing poses, limb continuity, head/torso/root stability, camera and F07→F00 seam. A complete timing plan or a set of raw PNGs is not a reviewed loop. Fanout/runtime integration remain outside this proposal.
