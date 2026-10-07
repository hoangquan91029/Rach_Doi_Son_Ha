# Villager locomotion contact-key pilot

**Status:** setup only; two built-in ImageGen whole-body edit calls are authorized, with one F00 and one F04 key. Stop after the second key for parent review. No in-betweens or further calls are authorized by this work order.

## Locked source and view

- Identity master: `docs/art/characters/villager-neutral-D00-screen-ESE/raw.png`
- SHA-256: `145b976ffd1bdf563cb5da78806547e6849424054f2c26fc297e155a0b366e94`
- Source canvas: 1254 x 1254 RGBA. Preserve it; do not resize, crop, clean alpha, or edit the master.
- Trial direction: engine D00 / world east, which projects screen ESE. Keep the master's camera and right-facing screen-ESE view.
- Review-only fixed frame transform: full 1254 x 1254 canvas, no per-frame fit; fixed ground/root anchor `(650, 1140)` in source-canvas coordinates. For the requested game-size contact comparison, apply one whole-canvas scale of `38 / 1254` to every frame and place the same root at the same preview coordinate. This is a proposed review transform, not runtime calibration.
- Character invariants: same adult Vietnamese villager, face, woven nón lá, pale undyed wrap tunic, dark waist sash, loose dark trousers, pale shin wraps, straw sandals, proportions, paint/material language, northwest light, and localized ground shadow.
- Near/far ownership for this D00 view: the nearer leg/arm are those on the screen-right side of the torso in the master; the farther leg/arm are on screen-left. Preserve consistent ownership through both keys.

## 8-frame cycle plan (100 ms per frame; 800 ms total)

| Frame | Phase | Pose intent | Generation status |
|---|---|---|---|
| F00 | 0 ms, near contact | Near screen-right foot planted ahead toward screen-ESE; far leg trails behind. Opposing arm swing. | Generate first; pending |
| F01 | 100 ms | Downward weight acceptance after near-foot contact; knees soften, center settles slightly. | Not generated |
| F02 | 200 ms, passing | Far foot passes underneath the body; near foot supports; arms reverse through midpoint. | Not generated |
| F03 | 300 ms | Upward transition as far leg advances. | Not generated |
| F04 | 400 ms, opposite contact | Far screen-left foot planted ahead toward screen-ESE; near leg trails. Opposing arm swing. | Generate second; pending |
| F05 | 500 ms | Downward weight acceptance after far-foot contact. | Not generated |
| F06 | 600 ms, opposite passing | Near foot passes underneath the body; far foot supports; arms reverse through midpoint. | Not generated |
| F07 | 700 ms | Upward transition as near leg advances, returning toward F00. | Not generated |

## Review gates

Compare the two generated originals at one identical full-canvas transform, with a 38 px visible-figure height and stable pivot; no per-frame bbox fit. Confirm visible opposite leg contacts and counter-swinging arms at game size, stable hat/face/outfit, consistent camera and root, genuine transparency, and no framing drift. Preserve raw files and exact prompts/input hashes. The two contact keys are a review pilot only; they do not establish a complete loop, motion approval, runtime calibration, or permission to fill other frames.
