# Static South contact diagnostic

READY tooling only. No actual job has been run, no source generated, and no F4 image existence or approval is claimed.

Requires Python3 + Pillow and Node + Playwright/Chromium (use the existing local capture runtime). `build.py JOB.json NEW_OUTPUT_DIR` refuses an existing output. Parent supplies actual absolute source paths and independently verified lowercase SHA256 values in this explicit shape:

```json
{
  "sources": {
    "canonicalSouth": {"path": "/actual/canonical.png", "encodedSha256": "ACTUAL_SHA256", "rgbaSha256": "ACTUAL_RGBA_SHA256"},
    "oldSelectedF0": {"path": "/actual/F0.png", "encodedSha256": "ACTUAL_SHA256", "rgbaSha256": "ACTUAL_RGBA_SHA256"},
    "newF4ActualRaw": {"path": "/actual/F4-raw.png", "encodedSha256": "ACTUAL_SHA256", "rgbaSha256": "ACTUAL_RGBA_SHA256"}
  }
}
```

RGBA hash is SHA256 of Pillow `convert('RGBA').tobytes()` in row-major order. Sources require PNG with an existing alpha channel. A requested family canvas other than actual 1254×1254 is held: metadata records actual dimensions/hashes, exits nonzero with HELD_CANVAS and produces no derivative/preview. No crop, reposition, alpha threshold, fringe cleanup or source writes occur. All three runtime images use the same full-canvas 128/1254 LANCZOS transform. Metadata records source and derivative dimensions, alpha statistics/bounds, encoded/RGBA hashes, global source reference height1130/pivot[654,1140] and scaled runtime calibration.

Run only after actual F4 custody exists:

```sh
python3 /home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha-art-lease/pure2d-contact-preview-008/build.py /absolute/job.json /absolute/new-review-output
python3 -m http.server 8788 --bind 127.0.0.1 --directory /absolute/new-review-output
```

In another terminal, with Playwright resolvable in the selected Node runtime:

```sh
node /home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha-art-lease/pure2d-contact-preview-008/capture.mjs http://127.0.0.1:8788/preview.html /absolute/new-capture-output
```

Capture uses a real localhost page at DPR1, saves neutral/light/dark views with three actual runtime images at nominal64/80/96 character heights and stable shared anchors, records browser/page errors, state and capture hashes, and closes its own browser in `finally`. Stop the HTTP server afterward. No deployment. The page is intentionally static: STATIC_CONTACT_DIAGNOSTIC_NOT_MOTION_APPROVAL. Parent must inspect identity/contact/anchor quality; no visual, owner, runtime or production acceptance follows from this diagnostic. No two-frame walk, atlas or controller is produced.
