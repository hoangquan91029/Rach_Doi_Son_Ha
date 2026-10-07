# Guided F04 correction — prepared, not generated

**Status:** model-only pose-guide package for parent inspection. No ImageGen call has been made. If approved, the package contains one planned correction call only. The rejected F04 raw from pilot 001 is explicitly excluded as an image input and must never be used as conditioning.

## Locked inputs

- Identity master: `/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha/docs/art/characters/villager-neutral-D00-screen-ESE/raw.png`, SHA-256 `145b976ffd1bdf563cb5da78806547e6849424054f2c26fc297e155a0b366e94`.
- F00 appearance/motion continuity reference: `/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha-art-lease/villager-walk-D00-pilot-001/F00-raw.png`, SHA-256 `57fe10ac4a0708ff168ce6a0eb1f4b932a98673b4dd34a97aee264f38e55acb4`.
- Rejected pilot-001 F04 is excluded; no rejected bitmap is embedded or attached.
- Direction: engine D00/world east, visible screen ESE.

## Measured F00 landmarks and F04 guide landmarks

Coordinates refer to the locked 1254×1254 full canvas. F00 measurements are approximate visual landmarks from the inspected raw; they are recorded to anchor the mannequin and preserve framing, not asserted as runtime skeleton data.

- F00 hat bounds about `(508,67)` to `(838,264)`; head center about `(682,204)`; shoulder center about `(672,351)`; belt/pelvis center about `(650,581)`; leg root/hips around `(580,730)` far and `(700,735)` near.
- F00 near screen-right leg currently leads: knee about `(700,870)`, ankle `(748,1035)`, foot contact near `(830,1145)`. F00 far screen-left leg trails: knee `(548,870)`, ankle `(495,1000)`, foot near `(466,1030)`.
- F04 must reverse these ownership roles. Far leg, drawn behind, leads down-right: far hip `(580,730)` → knee `(650,900)` → leading ankle `(755,1050)` → planted foot center `(820,1148)`, toe toward `(866,1168)`.
- Near screen-right leg trails upper-left: near hip `(700,735)` → knee `(560,865)` → trailing ankle `(500,1015)` → foot center `(465,1090)`, toe toward `(495,1100)`.
- Near arm swings forward while its same-side near leg trails: near shoulder `(790,355)` → elbow `(830,420)` → wrist `(875,500)`. Far arm swings back while the far leg leads: far shoulder `(520,355)` → elbow `(450,410)` → wrist `(395,475)`.
- Torso centerline and hat/head guide stay aligned to F00 framing; the nominal root marker remains near `(650,1140)`. This is source-guide geometry, not a calibrated runtime root.

## Fixed review transform

Keep all generated art on a 1254×1254 canvas. For 38px review, scale the entire canvas by `38/1254` and use the same root placement for every comparison. Do not fit each pose by its alpha bounds, crop, mirror, resize, or move the source pixels. The guide is MODEL_ONLY geometry, not painted artwork, not a generated frame, and not motion evidence.
