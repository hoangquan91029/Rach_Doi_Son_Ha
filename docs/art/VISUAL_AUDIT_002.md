# Parent visual audit 002 — 7 October 2026

**Verdict: REJECT as a completed vertical slice. All integrated artwork remains CANDIDATE / PLACEHOLDER_ONLY.**

The parent inspected actual browser captures at 1440 × 900 and normal zoom 1.08, including `artifacts/art-v1/eight-assets-chromium/general-hud.png`, `nine-assets-firefox/trained-cavalry.png`, and `nine-assets-chromium-river-centered/scouted-river.png`. These captures use the real simulation and normal UI production orders. No substitute map, injected units, hidden placeholder layer, or altered match state was used. The cavalry was built and trained with normal resource costs.

| Category | Rating / 10 | Reason and next correction |
|---|---:|---|
| Characters | 5 | Curated villager, infantry, cavalry and Trần Hưng Đạo neutral candidates improve material and silhouettes. Other leaders and troop roles still use primitives; directions and motion remain incomplete. |
| Buildings | 4 | Residence variant 02 is a promising individual 8/10 illustration at normal size. The other buildings, construction and damage still use procedural shapes. An individual candidate does not qualify the category. |
| Terrain | 5 | Grass B is quieter and broadleaf foliage is illustrated. Repeated identical trees, hard shores, undifferentiated ford water, missing cliffs/undergrowth/roads and flat geographic composition remain visible. Water B is a source refinement awaiting a new integrated capture. |
| UI | 7 | Larger text, face portraits, persistent leader commands and a coherent jade/brass frame improve play. Unit/ability/resource artwork and production icons remain unfinished. |
| Animation | 3 | Missing exact states return explicit placeholders. Two villager walking keys fail the required opposite contact; no complete raster cycle is accepted. |
| VFX | 3 | An independent authored contact-shadow candidate grounds the refined infantry. Combat smoke, impact, recoil, damage and naval effects remain unfinished. |
| Style consistency | 5 | Painted neutral candidates fit the palette better, but still coexist with obvious procedural world objects. |
| Historical plausibility | 6 | The General preserves the supplied identity and the Residence uses researched timber/tile language. Other architecture and equipment need contextual review. These are plausible game interpretations, not certified reconstructions. |
| Gameplay readability | 7 | Shared scale, readable leaders and sprite-body selection improve navigation and control. Ford, dense combat, terrain boundaries and unfinished silhouettes require refinement. |

Every major category is below 8/10. The screenshot still reads as a development build. It is unsuitable as a finished-game marketing image. Do not expand to hundreds of assets or mark sections 108/114 complete.

## Measured presentation corrections

The first 34 × 17 trial drew a roughly 126-pixel Residence above a 74.8-pixel gameplay footprint and crowded soldiers at their existing world spacing. One shared presentation configuration now uses 54 × 27 tiles, unchanged 2:1 projection and normal zoom 1.08. The Residence footprint is 118.8 logical pixels before zoom. Simulation positions, costs, footprints and navigation were not changed. Tile art is centered at `(x + 0.5, y + 0.5)` to agree with the simulation's floor-indexed cells.

Raw candidates are retained. Runtime packaging is a documented constant full-canvas resize or pixel-preserving WebP copy. Separate artist-padded convenience derivatives are not the runtime sources. Alpha-fringe warnings remain open for tree and Residence; successful packaging and decoding grant no visual approval.

## Walking pilot 001

External source lease: `/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha-art-lease/villager-walk-D00-pilot-001`.

Exactly two built-in ImageGen calls produced separate 1254-square RGBA frames. The parent inspected both raw images and their common 38-pixel full-canvas comparison. F00 is a usable review-only stride key; F04 retains the same screen-right leading foot and weak arm counter-swing. It is rejected as the opposite contact. The job closed at its two-call cap. There is zero accepted complete walking-cycle coverage and no runtime integration of these keys. A separately prepared pose guide may address the measured phase failure; it is diagnostic geometry, not painted art or motion evidence.

Technical browser receipts explicitly record `visualApproval: false`. The final placeholder ledger remains unresolved.
