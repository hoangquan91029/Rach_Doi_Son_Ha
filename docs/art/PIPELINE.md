# Raster custody and runtime pipeline

This is packaging validation, **not visual quality approval**. Current primitive rendering remains **PLACEHOLDER_ONLY**. Successful hashes, alpha checks, decoding and drawing do not turn an unreviewed candidate into final art. Only the parent’s recorded visual review can authorize APPROVED status. Follow [ART_DIRECTION.md](../ART_DIRECTION.md) and [visual-quality-requirements.md](../visual-quality-requirements.md); no source creation, pixel repair, background removal or release approval is performed by this pipeline.

## Manifest contract

The parent owns `public/assets/art-v1/manifest.json`. Schema version 1 has `status` CANDIDATE or APPROVED, camera `{projection:"dimetric",ratio:[2,1],tile:[54,27],elevation:26.565}`, and `assets` array. An empty manifest remains PLACEHOLDER_ONLY and cannot pass the release check. IDs are unique ASCII letters/digits/underscore/dot/hyphen. Paths below refer to the manifest directory unless the validator receives `--source-root`; immutable source paths may also be absolute. Runtime paths must be relative PNG/WebP paths inside the manifest directory, including resolved symlink containment.

Each asset contains:

| Field | Contract |
|---|---|
| `id` | Unique raster/animation variant ID, e.g. `residence-static` or `infantry-walk-D00` |
| `family` | Optional lookup family; every declared family locks source canvas, runtime cell, pivot and logical render dimensions across all states/directions |
| `kind` | unit, building, prop, vfx, terrain, ui or portrait |
| `state`, `direction` | Exact state string; D00–D07 numeric 0–7, or null for nondirectional art. No direction substitution/mirroring |
| `source` | `{path,sha256,rgbaSha256,width,height,bbox?,alphaExtrema?}`. SHA256 pins encoded immutable original and decoded row-major RGBA bytes |
| `runtime` | Same raster metadata plus `derivation:{method,sourceSha256,filter?}`. Methods copy, resize, atlas; resize/atlas use common `filter:"lanczos"` |
| `cell` | `{width,height}` fixed runtime frame canvas, never tight-fit per frame |
| `pivot` | `{x,y,space:"source"}` absolute source pixels; fixed feet/hoof/foundation ground anchor across frames and variants |
| `render` | `{width,height}` full runtime **cell** size in logical screen pixels; preserves cell aspect ratio |
| `loop` | Optional boolean; defaults false for death and true for other states; nonlooping animation holds its final cell |
| `frames` | One or more `{x,y,width,height,durationMs,source?,pivot?}` cells in runtime sheet pixels; no overlap, clipping or per-frame pivot changes |
| `alphaPolicy` | transparent for cutouts; opaque permitted only for explicit terrain material textures, including water |
| `contactShadow` | `{mode:"baked"}` or `{mode:"separate",assetId:"..."}`. none permitted for material/UI/VFX/portrait assets; grounded units/buildings/props require shadow |
| `review` | `{status:"CANDIDATE"|"APPROVED"|"REJECTED"|"PLACEHOLDER_ONLY",reviewer?,receipt?}` |
| `candidate` | Explicit boolean; APPROVED requires false plus named reviewer and receipt. A receipt is a recorded declaration, not verification that review occurred |

Every multi-frame atlas cell identifies its own original `frames[i].source` with encoded/decoded hashes and the same immutable source dimensions. Top-level source identifies the canonical first/reference original; derivative sourceSha256 pins it. Atlasing is deterministic packaging of individually authored frames; it is not a substitute for authored/reviewed animation. Static assets use one frame and top-level source only. Transparent cutout source/runtime images require genuine RGBA and actual alpha. Only explicitly opaque terrain materials may retain RGB source PNG or RGB runtime WebP with implicit alpha 255; their rgbaSha256 hashes the decoded RGB converted to RGBA for validation without changing the retained original file.

For copy, runtime decoded RGBA must exactly equal source. For resize/atlas, the validator reconstructs every cell from its retained source using Pillow Lanczos and compares **all runtime RGBA bytes**. Use lossless WebP with exact transparent RGB preservation (Pillow `lossless=True, exact=True`) or PNG; lossy output cannot pass this exact derivative check. Originals are never resized/cropped/recentered/overwritten. Encoded source hashes are checked again after decoding. No automatic alpha extraction, checkerboard removal, component deletion, recoloring or equipment mirroring exists. Raw opaque/matte attempts are retained for review rather than repaired by this script.

## Coordinates and camera

World simulation stays 64×48. Baseline ground projection is `screenX=(worldX-worldY)*27`, `screenY=(worldX+worldY)*13.5`: each 54×27 logical tile is a 2:1 diamond, camera elevation 26.565 degrees. Camera pan/zoom and devicePixelRatio are applied once by the renderer. Art already depicts this same camera; assets cannot receive individual perspective/anisotropic corrections.

Source pivot converts to runtime cell coordinates as `pivot.x*cell.width/source.width`, `pivot.y*cell.height/source.height`. Draw the chosen runtime cell at projected ground anchor minus pivot scaled by `render.width/cell.width`, `render.height/cell.height`. This anchor stays fixed during animation and direction changes. Do not anchor at changing alpha bbox or visually fit every frame. Normal zoom is 1.08. Apparent painted human height targets 32–38 logical pixels; leaders 36–42; horse+rider 44–50. Full transparent canvas render size is larger than visible body height; measure visible bbox at gameplay scale during review. Building overhang/pivot must preserve truthful world footprints.

Opaque grass/water materials are repeated world texture art and must be reviewed for seams/lattice. They are not transparent props and cannot replace passable/blocked simulation geography. Their static frame/pivot metadata still declares the coordinate anchor; contactShadow none is appropriate.

## Browser integration

```js
import {createArtAssetPipeline} from './art-assets.js';
const art = createArtAssetPipeline({
  manifestUrl:'/assets/art-v1/manifest.json',
  allowCandidates:true, // explicit development vertical-slice preview only
  onStatus:stats => console.info('Raster custody',stats)
});
await art.preload();
const raster = art.get('infantry',{state:'walk',direction:0,timeMs:animationTime});
if (raster.image) {
  const {render,pivot}=raster;
  const dx=groundX-pivot.x*render.width/raster.sw;
  const dy=groundY-pivot.y*render.height/raster.sh;
  ctx.drawImage(raster.image,raster.sx,raster.sy,raster.sw,raster.sh,dx,dy,render.width,render.height);
}
```

`allowCandidates` defaults false. Candidate preview remains CANDIDATE; it never returns approved=true. Approved loads require both manifest and asset APPROVED, noncandidate flag and explicit reviewer/receipt. Rejected/placeholder assets are skipped. Missing/error/unavailable states return `{image:null,status:"PLACEHOLDER_ONLY",reason}`; renderer fallback must visibly remain a declared placeholder, never silently a final-art substitute. Exact direction/state lookup does not mirror weapons or silently borrow another animation. `get` returns runtime cell coordinates, locked cell pivot, logical render size, shadow declaration and original metadata. Separate shadow drawing requires exact referenced asset lookup. `dispose()` releases decoded image bitmaps.

Loading fetches manifest then four rasters at a time, caches identical runtime file/hash pairs, verifies encoded runtime SHA256 with browser WebCrypto, and checks decoded dimensions (32 million decoded pixels maximum per raster). Missing secure-context WebCrypto, mismatched hashes, malformed metadata, family pivot drift or decoding failures yield PLACEHOLDER_ONLY with stats. Use HTTPS or localhost for the browser preview. Browser decoding verifies neither anatomy nor hidden RGBA pixels; the offline validator supplies decoded pixel custody. Candidate assets still need visual/animation review before final eligibility. Renderer/main files are integrated separately by the parent.

## Read-only packaging check

```sh
python3 scripts/validate-art-assets.py public/assets/art-v1/manifest.json
python3 scripts/validate-art-assets.py public/assets/art-v1/manifest.json --source-root /ABSOLUTE/SOURCE/LEASE
python3 scripts/validate-art-assets.py public/assets/art-v1/manifest.json --require-approved --output /NEW/receipt.json
```

Default checks candidate packaging honestly. `--require-approved` only checks **recorded** approval fields; it does not grant approval or measure art quality. Output receipts must be new files. Exit 0 means packaging PASS; invalid, empty or missing packages exit 1. The validator reads hashes, source/runtime dimensions, alpha extrema/bboxes, transparent margins, each frame cell, family anchor/scale consistency, derivation pixel equality and metadata. It never modifies images or manifest.

Alpha-zero margins reject full opaque backgrounds/checkerboards. For CANDIDATE assets only, a nonzero border with maximum alpha <=16 may produce CANDIDATE_WARNING when the alpha>16 body bbox still has clear margins. Every original pixel and hash is retained; no fringe is deleted or masked. Stronger edge alpha or body clipping fails. APPROVED assets and --require-approved still require strict alpha-zero margins; candidate warning is never release approval. Pixel metrics cannot certify that a partly opaque illustration contains no painted checkerboard, halo, anatomy defect, fake detail or historical mismatch; those remain parent visual review gates. Hidden RGB beneath alpha zero is included in custody hashes but is not itself a visible background defect. Keep attempt provenance, prompts, timestamps, original outputs and specific reject reasons with the parent-owned asset ledger. Packaging PASS, candidate preview, motion review and final visual acceptance remain separate.

Technical fixture verification (temporary synthetic byte grids, no game art): exact PNG source copy and lossless WebP Lanczos derivative pass; runtime hash corruption, incorrect bbox, per-frame pivot, candidate masquerading as approved, family pivot drift, opaque cutout, overlapping atlas cells and candidate release check fail as expected. Individually retained-source atlas and explicit opaque terrain WebP pass. Loader mocks verify default candidate exclusion, explicit candidate preview, reviewer/receipt eligibility, exact direction fallback, pivot scale and corrupted runtime rejection. Input source bytes remain unchanged. These are packaging regressions, not visual/art acceptance.

Actual-game candidate adapter: `client/raster-slice.js` exports `createRasterSlice`. It is disabled unless `?art=pilot` or explicit enabled:true. Ground uses authored materials repeated on one world-anchored dimetric plane with invisible coverage clips and no grid strokes; forest props remain attached to actual forest/fog data and expose x+y depth ordering. Buildings/units use actual entity anchors and exact authored state/direction/leader identity. Missing walking/combat/death art returns false and remains PLACEHOLDER_ONLY; idle keys never substitute for animation. The parent owns renderer/main hook integration and browser visual acceptance.

Actual retained package smoke: six parent-owned candidates pass read-only packaging with explicit low-alpha edge warnings on forest/residence; grass/water retain original RGB opaque source bytes and hash their implicit-alpha RGBA decode. An ephemeral localhost Canvas test in Chromium and Firefox decoded all six actual WebP files with matching runtime SHA256 and exercised projected material patterns, forest/building/unit anchored draws and missing-walk false returns (ready=6, failed=0). No gameplay screenshot or visual approval was inferred; parent integration into the actual simulation renderer and normal-zoom placement review remain separate.

Global presentation trial: client/world-presentation.js exports TILE_WIDTH=54, TILE_HEIGHT=27 and NORMAL_ZOOM=1.08. Renderer and raster material projection share this scale. A 2.2-tile Residence ground footprint measures approximately119 logical pixels before zoom; all simulation coordinates, physics, source pixels, asset render sizes and fixed pivots remain unchanged. Camera manifest/validator locks follow54×27. Packaging verification is technical only; parent normal-zoom placement review remains required.
