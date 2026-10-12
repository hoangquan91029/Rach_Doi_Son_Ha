# Villager D1 whole-clothed pose control491

Authoring-only pure2D whole clothing contours; no source-raster cuts or transformed limb textures. A=image-right cuff in fixedSouth view, B=image-left; anatomical labels stay unknown. ContactA0/contactB.5 align with historical endpoint intent, not observed ground contact.

Reproduce authoring outputs:

```sh
node scripts/whole-clothed-walk-guide.mjs docs/art/pipeline/villager-pose-control-491/control.json docs/art/pipeline/villager-pose-control-491/guide
python3 scripts/render-clothed-guide.py docs/art/pipeline/villager-pose-control-491/guide
```

The motion formula is reusable; garment contours are VillagerD1-specific, not a universal body or eight-direction image generator. Other units require their own original-bound clothing authoring. Guide raster/phase math does not qualify final art. `guide/revision0` preserves initial contour failure.

ONE built-in wholeF2 call after finiteprepare/claim used target→originalSouth→F0→F4→guide. Actual prompt/input order/output mapping: `claimed.json`, `tool-result.json`. Output `trial-F2-raw.png` is HELD, not selected or installed. The requested passing improvement did not occur at71px. No retry/descendant authorized by this package. `trial-review.json` is independent. Original artwork/public/game source unchanged.

`CHECKPOINT.json` owns results/unknowns/budgets/next dependency. Guide-first illustration is a proposed next mechanism; current finite guard does not support a guide edit target. No new order exists.
