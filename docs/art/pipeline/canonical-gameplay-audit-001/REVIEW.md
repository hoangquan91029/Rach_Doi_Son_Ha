# Canonical appearance audit at gameplay size

**Disposition: current pilot appearance remains HELD.** This is a parent diagnostic using existing images, not newly generated art, an independent motion review or final approval.

The captured browser plate compares the D07 identity reference with pilot 003 F0/F24 contacts and F12 passing pose at nominal 80/96 px on neutral, light and dark backgrounds. Images are drawn with fixed whole-canvas scales and their preserved pivots at CSS/backing ratio 1. The reference is neutral; the pilot is walking. Different leg positions are not scored as identity defects.

## Visible findings

| Feature | Existing identity reference | Current pilot | Next whole-character correction |
|---|---|---|---|
| Tunic | Long wrapped garment, hanging panels and soft folds remain visible at 80 px | Short compact top exposes a large dark hip/thigh shape; the long wrapped garment reads poorly | Restore the garment's length, overlapping panels and low-frequency folds, with coherent deformation around the moving legs |
| Trousers | Loose brown cloth and gathered knee/cuff forms | Simplified dark hip mass and narrow pale lower legs read closer to shorts/tights | Restore loose trouser volume and clear cloth-to-leg-wrap transitions; retain the actual stance/swing tracks |
| Hat | Tilted brim, readable underside and asymmetric profile | Broad, comparatively symmetric conical form with uniform facets | Match the brim tilt/profile and underside shading; fine weave is secondary |
| Materials | Soft textile highlights, warmer skin, clear cloth/sash/hat separation | Large flat tonal regions and primitive surface transitions | Use coherent whole-model material/texture and soft shading once, reused across frames |
| Identity consistency | Ivory wrap, dark sash, brown trousers, conical hat | Broad colors are consistent but do not preserve sufficient garment/profile fidelity | Keep the existing colors and anatomical sash ownership; qualify the whole appearance against this plate before fanout |

These are observable gameplay-size differences. They do not justify separate limb textures, veins, enlarged-frame polish or default AI repaint of every frame. Face, weave and stitch detail are subordinate to silhouette, garment construction and readable materials. Static pose differences and individual magnified joints are not rejection reasons here.

## Calibration and limitations

The historical reference is still the original 1254 px image; it is not a newly authored source frame. Its alpha>0 bounds are [43,19,1230,1214], enlarged by low-alpha fringe. For this diagnostic only, alpha>=32 bounds [510,55,819,1185] give a 1130 px reference body height. The original pixels and pivot [654,1140] are unchanged. No crop, alpha repair or source replacement was applied. This measurement is not a production crop contract.

The pilot uses its unchanged 128 px runtime cells, pivot [64,118.5] and reference height 116.5. At nominal 80 px, the reference body is 80 px and the three pilot alpha>=32 bodies measure approximately 78.28/78.28/79.66 px. This small variation is recorded rather than removed by per-frame fitting. It does not explain the garment and material differences visible on the plate. The calibration is fixed for both rows and all backgrounds.

Browser screenshots prove the comparison was rendered at the declared sizes. They do not establish motion, canonical owner acceptance, camera reconciliation, crowd readability or production-game acceptance. The original reference is sealed identity/authoring evidence, not a completed animated unit. Existing colored-fringe warnings remain preserved.

## Exact next authoring task

One D07 complete-character appearance revision only. Preserve the pilot 003 motion functions, 1.28 stride, 0.84 hip, 649.579324 ms cycle, world speed 2.1, anatomical ownership and fixed pivots/scales. Improve the whole garment geometry, hat profile and coherent material appearance from the original identity reference. Cloth must deform as complete geometry around the unchanged clip; do not rotate cutout textures or conceal motion defects. Author source characters at 192–256 px, runtime characters at 96–128 px, and review the actual 64–96 px result.

Start with complete opposite-contact images before committing to the full 48-frame export. The current blocky model is not a production template. No other direction/unit is opened. AI repaint remains an optional fallback only after a canonical-faithful whole-model result is actually reviewed. Final motion must be reviewed again if changed garment geometry obscures support or introduces clipping. Exact camera, production manifest/gutters and engine distance-clock gates remain open.

## Reproduce this diagnostic

From the repository root, serve locally with `python3 -m http.server 8767 --bind 127.0.0.1`, then open `/docs/art/pipeline/canonical-gameplay-audit-001/preview.html`. For capture, run `capture.mjs` with that localhost URL and a NEW output directory under `flock /tmp/tn-heavy-gate.lock`. The capture refuses an existing output directory. Stop only the server you started.

No source sprite, production code, service or simulation was changed. The full game remains NOT COMPLETE.
