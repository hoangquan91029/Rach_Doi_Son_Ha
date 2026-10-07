# Visible placeholder debt — 7 October 2026

**Release gate: FAIL.** Every unresolved item below remains **PLACEHOLDER_ONLY**. Release requires zero unresolved gameplay-visible placeholders.

| Asset | Current location | Why it remains a placeholder | Replacement requirement | Status |
|---|---|---|---|---|
| Plain, forest, and hill ground | `client/renderer.js`, `drawTile` | Default procedural terrain; optional Grass B raster trial lacks natural transitions and final review | Painted ground textures, natural transitions, and authored map composition | **UNRESOLVED — PLACEHOLDER_ONLY** |
| River, sea, and ford | `client/renderer.js`, `drawTile` | Default procedural water; optional Water B and distinct shallow Ford A are candidates, with hard tile-boundary shores and no animated shore/current | Natural painted shores, animation and current cues, final gameplay-scale review | **UNRESOLVED — PLACEHOLDER_ONLY** |
| Trees and undergrowth | `client/renderer.js`, `tree` and `drawResource` | Default geometric vegetation; optional single broadleaf candidate repeats visibly and retains a faint alpha-fringe warning | Curated, varied illustrated forest clumps and reeds with readable boundaries | **UNRESOLVED — PLACEHOLDER_ONLY** |
| Hills, mountains, and iron | `client/renderer.js`, `rock`, `drawTile`, and `drawResource` | Primitive polygon rocks | Illustrated cliffs, elevation, erosion, and grounded ore | **UNRESOLVED — PLACEHOLDER_ONLY** |
| Food nodes | `client/renderer.js`, `drawResource` | Circle crop icon | Illustrated rice or forage patches with a readable harvest state | **UNRESOLVED — PLACEHOLDER_ONLY** |
| Ten building types | `client/renderer.js`, `drawBuilding`; Main Residence candidates in `docs/art/residence/variant-01/` and `variant-02/` | Procedural roof and wall geometry. Residence variant 02 is integrated only in the optional candidate pilot; other structures, construction and damage remain procedural. | Curated, grounded historical architecture sprites with functional details, damage, and construction visuals | **UNRESOLVED — PLACEHOLDER_ONLY; Residence trial integrated; full building category rejected** |
| Villager, infantry, spearman, and firearm infantry | `client/renderer.js`, `drawFoot` | Neutral villager and refined infantry trial rasters are integrated only for exact idle D00; other roles, directions and action states remain geometric | Curated raster art in eight directions with believable idle, walk, attack, hit, and death states and continuous equipment | **UNRESOLVED — PLACEHOLDER_ONLY** |
| Cavalry | `client/renderer.js`, `drawCavalry` | One neutral cavalry candidate is in the pilot; gait, other directions and combat remain placeholders | Anatomically sound horse and rider with gait, momentum, and attack | **UNRESOLVED — PLACEHOLDER_ONLY** |
| Artillery, wagon, and ships | `client/renderer.js`, `drawArtillery`, `drawWagon`, and `drawShip` | Geometric vehicle art | Curated painted vehicles with functional motion, wrecks, and wakes | **UNRESOLVED — PLACEHOLDER_ONLY** |
| Twelve King and General world rigs | `client/renderer.js`, `LEADER_STYLE` and `drawFoot` | Trần Hưng Đạo neutral D00 candidate is in the pilot; remaining leaders and all action/directional coverage are unfinished | Premium, reference-grounded historical identities with eight consistent directions and polished motion | **UNRESOLVED — PLACEHOLDER_ONLY** |
| Combat, impact, and damage VFX | `client/renderer.js`, `drawUnit` and `drawBuilding` | Rudimentary colored flashes and wrecks | Restrained historical smoke, impact, recoil, fire, and splash | **UNRESOLVED — PLACEHOLDER_ONLY** |
| HUD resource and ability icons and unit cards | `client/main.js` | Readable live leader face portraits and framing exist; resource/ability/production artwork remains unfinished | Finished functional painted icons, cards, and portrait HUD in the shared art direction | **UNRESOLVED — PLACEHOLDER_ONLY** |

Selection rings, health bars, minimap markers, and collision/navigation data are information overlays, not art substitutes; assess their readability separately. Static leadership portraits are candidate source derivatives, not certified animation frames. Original leadership files remain untouched.

The optional `?art=pilot` preview is not final art. See `docs/art/VISUAL_AUDIT_002.md`. The default public playtest remains explicitly labeled as development art.
