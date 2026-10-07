# Character neutral identity pilots

This directory contains two neutral cutout candidates only: one villager and one General, Trần Hưng Đạo. These are identity/style pilots, not approved final art. Do not generate animation, additional directions, or batch variants until the parent reviews both in game-scale previews and the browser slice.

## World direction and screen projection

The engine stores eight compass directions in world-tile coordinates. The orthographic dimetric projection is proportional to:

```text
screenX = worldX - worldY
screenY = worldX + worldY
```

Positive screen Y points downward. Therefore, an engine direction name is not the same as the visible screen heading. In particular, D00 is world east but appears toward the screen’s lower-right (ESE); D01 is world southeast and appears straight down (S).

| Engine frame | World direction vector | Screen projection | Screen heading |
|---|---:|---:|---|
| D00 | (+1, 0) | (+1, +1) | ESE |
| D01 | (+1, +1) | (0, +2) | S |
| D02 | (0, +1) | (−1, +1) | WSW |
| D03 | (−1, +1) | (−2, 0) | W |
| D04 | (−1, 0) | (−1, −1) | WNW |
| D05 | (−1, −1) | (0, −2) | N |
| D06 | (0, −1) | (+1, −1) | ENE |
| D07 | (+1, −1) | (+2, 0) | E |

The current neutral infantry material/style source is named `infantry-neutral-se`, but its visible pose heads ESE on screen, which is a D00 trial under this projection. Do not silently relabel it or treat its filename as proof of engine direction. These two pilots use an explicit **D00 / screen-ESE trial** label pending parent review.

## Reference sources inspected

- **Material and figure-rendering reference only:** [`public/assets/art-v1/units/infantry-neutral-se.png`](../../../public/assets/art-v1/units/infantry-neutral-se.png). Its warm painted material treatment is a style cue, not a subject-design template. Original file SHA-256: `f93740e8f1b6b90ff754c7bc3f6e488f60eb3456850c95985425db57629a7e84`.
- **Building-palette and brushwork reference only:** [`public/assets/art-v1/residence/candidate-02.png`](../../../public/assets/art-v1/residence/candidate-02.png). Parent selected it for the slice trial, not as final building approval. Original file SHA-256: `f617c3540680cafff467358bab1adb01bf735417563f2cba86ab8af523b07dcc`.
- **Trần Hưng Đạo identity lock:** [`leadership/tran_hung_dao/candidates/TN-LD-TRAN-HUNG-DAO-B01/identity-reference/tran_hung_dao-identity-D00.png`](../../../leadership/tran_hung_dao/candidates/TN-LD-TRAN-HUNG-DAO-B01/identity-reference/tran_hung_dao-identity-D00.png). SHA-256: `6ab3825af8ead29f7630be4c0539afe19c50df0664924c05e0df2366f69b1aeb`, matching `docs/leadership-source-hashes.json`. This source shows his profile, tied topknot with a narrow metal hairpiece, beard, dark-red cape/robe, gray lamellar armor, and sword at the hip. It does not show a full helmet. Preserve the identity source unchanged; the generator may reinterpret paint/material rendering but must not invent different headwear, armor, weapon, or face.

The selected Residence candidate and infantry reference are style references, never edit targets. The leadership D00 is an identity reference, never an edit target. All generated images are new neutral views on transparent backgrounds. Preserve every prompt, raw generation, hash, and alpha measurement. A generated image does not grant animation, direction, or release approval.

## Neutral candidates

- **Villager:** [`villager-neutral-D00-screen-ESE/`](villager-neutral-D00-screen-ESE/) — raw SHA-256 `145b976ffd1bdf563cb5da78806547e6849424054f2c26fc297e155a0b366e94`. Its metadata records the raw, prompt, alpha measurements, and padded convenience derivative. Parent review is pending.
- **Trần Hưng Đạo General:** [`tran-hung-dao-neutral-D00-screen-ESE/`](tran-hung-dao-neutral-D00-screen-ESE/) — raw SHA-256 `21e7d7c160fc27b52f8e9475702914e73a628752a5c2b5a4c290d9c7b466d553`. Review the untouched [`raw.png`](tran-hung-dao-neutral-D00-screen-ESE/raw.png) first; [`metadata.json`](tran-hung-dao-neutral-D00-screen-ESE/metadata.json) records its prompt, reference hashes, alpha measurements, and separate 1024px padded derivative. The thresholded raw silhouette reaches within about 1.4% of the top and bottom edges, so it misses the requested 5% vertical clearance. The padded image is only a convenience derivative, not a correction or approved runtime asset.

Both remain one-view source candidates. No direction fanout, animation, runtime integration, or final art approval has occurred.
