# Independent review: deterministic villager D07 walk pilot

**Verdict: `INDEPENDENT_MOTION_FAIL_NARROW`.** This verdict applies only to the eight-frame D07 screen-East/world-NE walk pilot at the inspected 64, 80 and 96 px character sizes. Do not fan out directions or other actions from this result.

## Custody and technical checks

The frozen renderer and all eight frames were verified against the READY hashes. I imported the pinned `pilot.py`, rendered the eight phases once into this review directory, and compared each result against its frozen original. All eight PNG files and all eight decoded RGBA buffers matched exactly. The copy in the repository checkout also matches the frozen lease for `pilot.py`, `spec.json`, `animation.json`, `receipt.json` and F0–F7.

The continuous-rig geometry check passes numerically over 501 samples: maximum upper/lower segment error is below 3.4e-16 units and maximum stance toe speed is 5.6e-10 units per phase. That does not pass the held-sprite movement gate. The actual 60 Hz held-cel comparison reports 3.9088 px maximum same-contact toe slip against the declared 2 px limit, so actual held-frame contact fails.

## Visual review

I reviewed the 64/80/96 contact sheets, the canonical front and side appearance references, and the fixed-root/scrolling-ground browser-capture screenshots at 1x. I also inspected the live local preview at 80 declared character pixels at 1x and at its available 0.5x diagnostic rate with the engine sprite timing sampler; contact markers were toggled during the slower diagnostic. At 80 declared character pixels, the complete 256px source canvas is displayed at about 87.9 CSS px, the character is 80 px tall, and the source-to-screen scale is 80/233 = 0.34335. The browser capture used a 1280x720 viewport, 1024 CSS-pixel preview canvas and device pixel ratio 1. The preview exposes no 1.5x rate or continuous zoom control.

F0 and F4 show opposite leading-foot contact poses. The loop reads as a brisk walk at all three inspected sizes, but the 325ms cycle feels hurried and somewhat mechanical. In the moving-ground view, the feet do not stay anchored through the held cels; the measurable 3.91px slip exceeds the gate. I did not see a gross scale pulse, outfit pop or obvious F7-to-F0 silhouette flash at these sizes, but that does not offset the contact failure.

The broad conical hat, cream top, brown lower garment and sandal cues match the canonical silhouette and palette. The mesh render is much flatter and less textured than the painterly canonical references; face, body volume and garment details remain visually unapproved.

The camera elevation is 26.565 degrees, giving a 0.4472 ground vertical-to-horizontal ratio versus the runtime grid's 0.5. That reconciliation is still open. The review preview does not establish runtime integration.

## Separate dispositions

- **Technical custody:** PASS; exact frozen source reproduced.
- **Continuous rig contact:** PASS, numeric only.
- **Held-cel contact and independent motion:** FAIL for this eight-frame pilot.
- **Identity/style:** pending visual owner review.
- **View mapping:** East D07 mapping inspected; camera/grid reconciliation remains open.
- **Human owner approval:** pending.
- **Runtime integration:** not integrated.
- **Production:** not accepted; no other direction or action reviewed.

The corrected live preview was used. The legacy travel APNG/GIF was excluded because its background scroll and sprite movement compound relative velocity. No new art, source edits, production flags or additional directions were created by this review.
