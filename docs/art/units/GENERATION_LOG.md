# Unit raster pilot generation log

## Infantry neutral SE

Attempt 01 (`attempts/infantry-01-rejected.png`) was rejected for this pilot: the tall crest, dense plated skirt and dark ornamental armor read as an elite generic East Asian warrior rather than ordinary Vietnamese infantry; the pose is more posed than neutral. Original prompt and raw PNG are retained. No output-level edits were made.

Attempt 02 is `public/assets/art-v1/units/infantry-neutral-se.png`, with the full generated original in `sources/infantry-neutral-se-imagegen-raw.png`. It has stronger cream/jade material separation and a quieter stance. It is a candidate only. At 36 logical pixels tall, the preview is approximately 17 pixels wide and loses weapon and armor detail; historical plausibility and parent quality rating remain open. See `infantry-neutral-se.json` and `infantry-neutral-se-prompt.txt` for bounds, hashes, and exact prompt.

## Cavalry neutral SE

One built-in ImageGen call produced `public/assets/art-v1/units/cavalry-neutral-se.png`; the raw 1254x1254 RGBA output remains at `sources/cavalry-neutral-se-imagegen-raw.png`. The infantry pilot was used only as a style/material reference. At 48 logical pixels tall the preview reads as mounted cavalry with four grounded legs and a coherent rider silhouette, while fine tack and sword detail collapse. This remains a candidate pending historical-plausibility and parent quality review. Exact prompt, hash, and alpha bounds are recorded in `cavalry-neutral-se.json` and `cavalry-neutral-se-prompt.txt`.
