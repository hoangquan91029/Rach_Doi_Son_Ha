# Villager walk D00 contact-key pilot

**Review-only external lease.** Exactly two built-in ImageGen whole-body edit calls were made under the authorized cap: F00 near contact, then F04 intended opposite contact. Both raw 1254x1254 RGBA outputs are preserved. No animation in-betweens, additional variants, runtime edits, manifests, builds, or integration were made.

The immutable identity input is `docs/art/characters/villager-neutral-D00-screen-ESE/raw.png`, SHA-256 `145b976ffd1bdf563cb5da78806547e6849424054f2c26fc297e155a0b366e94`. Exact prompts, generated-output paths, input hashes, alpha measurements, fixed-transform previews and raw hashes are in the per-frame metadata files.

`F00-raw.png` is a provisional near-contact continuity key, SHA-256 `57fe10ac4a0708ff168ce6a0eb1f4b932a98673b4dd34a97aee264f38e55acb4`. Its fixed-transform preview shows a leg stride, though the arm counter-swing is subtle.

`F04-raw.png` is retained unchanged, SHA-256 `2434e2c50a10fba397bda24048065a36b10ee6a2c8fae61d25c6d7f18f12b7fe`. It does not meet its intended opposite contact: the screen-right leg remains forward and the frame closely resembles F00. The two-call cap has been reached; no correction was attempted. Parent review is required before any further work.

`F00-F04-fixed-38px-review.jpg` compares the master and both keys at one whole-canvas scale (38/1254) with the same (650,1140) pivot placement. It does not fit frames by alpha bounds. The 8-frame/800 ms pose plan is documented in `POSE_PLAN.md`; only F00 and F04 were generated.
