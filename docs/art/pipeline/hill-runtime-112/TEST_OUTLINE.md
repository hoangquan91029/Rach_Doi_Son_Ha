# Finite implementation checks after authorization

- Deterministic aligned all-hill2x2 patch produces one center anchor; adjacent eligible block produces next anchor, never one per cell. Same map data yields same order. Partial/one-cell strips, nonhill cells and borders remain grass.
- Notready/absent exact hill asset gives no overlay and no new fallback claim. Ready19 optional terrain route selects111 only; default/work/food routes unchanged.
- Any missing/false visible entry in the four-cell block suppresses overlay. All four visible permits it; fog mutation changes this immediately with no stale cache. No private entity field or explored-only drawing.
- Overlay draw order precedes unit/resource/depthprops; metadata uses declared72 render/pivot unchanged. Underlying tile/navigation/state arrays stay identical before/after draw.
- Existing terrain-cache invalidation tests remain relevant. If caching placements, different exact map content/hash/render/ready invalidates; moving fog still gates each frame.
- Actual BOTH-map UI finite look: unit walks across passable hill, sprite/feet/contact shadows remain above rise; hill source scales coherently against ground and mountains; edges honestly grass; no unknownprops. Ordinary pause/menu,19asset/12portrait/noerrors. No scripted facing, generated scene or fullmatch.

These are an outline, not tests run or acceptance granted.
