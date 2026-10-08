# Pilot 003: villager walk cadence

**Current blocky appearance is HELD as final art. The user requires realistic graphics matching the existing approved assets. This pilot is motion evidence, not official graphics.**

This is one candidate walk for D07 (screen East). A complete clothed 3D character is rendered into 2D sprites. No AI calls, limb cutouts, repaint, additional directions or other units were used. The producer completed exactly one build; pilots 001/002 remain unchanged.

The cycle lasts **649.579324 ms** at the unchanged game speed of **2.1 world units/s**. Stride changes from 0.64 to 1.28 model units. Hip rest height changes from 0.90 to 0.84, with the entire upper body carried down by 0.06. Fixed leg lengths, toe-ground heel roll, mesh clearance and reach pass a 501-phase preflight. F0 has the leading LEFT contact; F24 has the leading RIGHT contact. These correspond to F0/F4 of the eight pose keys. Phase 1 reproduces F0's complete RGBA buffer. Numerical consistency does not establish natural gait.

The 48 complete frames retain 13.532903 ms holds after doubling the cycle. At nominal 96 px, the theoretical held-toe error is at most 1.40635 px plus 0.5 px of integer paste rounding. Four-cycle traces sampled at 60 Hz measure maximum errors of 1.404/1.509/1.611 px at nominal 64/80/96 px. This tracks the original mesh sole landmark, not optical flow. There is no frame-pivot adjustment or world-speed workaround.

The resolution choices follow the user's scope:

- Each 256×256 source contains a character 216–230 px tall, within the required 192–256 px.
- Each 128×128 runtime cell contains a character 108–115 px tall, within 96–128 px.
- The immutable 233 px reference maps nominal 80 px to an actual 74.16–78.97 px character. This proposed default meets the 64–96 px gameplay target. Nominal 64/96 are comparison zoom levels; actual heights are 59.33–63.18 and 89.00–94.76 px. Frames are never individually fitted.
- The 1024×768 atlas aggregates 8×6 runtime cells. It is not a 1024 px individual source frame. It occupies 394,265 PNG bytes and 3,145,728 decoded RGBA bytes (3 MiB). Full-roster memory budgets remain open.

The browser preview draws the actual runtime atlas with the real `client/sprite-timing.js` sampler, continuous ground travel and a fixed pivot. Chromium and Firefox pass playback at all three sizes without captured loading or JavaScript errors. See `browser-capture/browser-receipt.json`. This local preview does not establish production-game acceptance. Independent visible motion, canonical identity and exact camera reconciliation are separate gates.

From the repository root:

```sh
python3 -m http.server 8766 --bind 127.0.0.1
```

Open http://127.0.0.1:8766/docs/art/pipeline/deterministic-villager-003/preview.html . Controls provide 64/80/96 px, 1/0.5/1.5 playback rates, dark/light/neutral backgrounds, contact landmarks and scrubbing. Stop only your own server. `capture-preview.mjs` takes the localhost URL and a NEW output directory; run it under `flock /tmp/tn-heavy-gate.lock`. The public service on port 3000 is unaffected.

`READY.json` and `receipt.json` bind source outputs and tools. The build refuses existing frames or a receipt. Reproduce only into a NEW sibling lease using `reproduce-new-lease.txt`; never build in a frozen original. Inherited contact sheets incorrectly label 24 samples despite containing 48 frames. Their bytes remain preserved beside additive corrected sheets and `qa-header-correction-receipt.json`. One pinned interpreter cache is preserved solely as byte custody, not as an authoring source or runtime asset; see `cache-custody-note.json`.

The full game remains **NOT COMPLETE**. `parent-review.json` and the independent review record the narrower disposition. No fanout, art flag or deployment approval is inferred.

Independent review now records **PASS_NARROW for D07 screen East walk motion only**. The original review mistakenly says South; its bound amendment corrects the label without changing source bytes or the motion result. Parent accepts the clip as motion evidence. Canonical identity/realism remains **HUMAN_VISUAL_HELD**; other directions, production and integration remain unapproved.
