# Art direction — Rạch Đôi Sơn Hà

**Version 1 · 7 October 2026**  
This document is binding for every visual contributor. Sections 82–114 of [visual-quality-requirements.md](visual-quality-requirements.md) are hard acceptance requirements. Existing procedural game art is **PLACEHOLDER_ONLY** and rejected for release. Do not create a large asset batch before the parent reviews and accepts the browser visual slice.

## Visual identity

Create an original, richly illustrated historical RTS set among Vietnamese riverlands. Use warm, worn timber; mossed masonry; muted jade water; lush tropical woodland; ochre earth; and restrained vermilion and aged gold. Aim for painterly realism, clear silhouettes at gameplay scale, readable material planes, and soft contact shadows. Avoid pixel art, flat-vector final art, toy miniatures, plastic-looking 3D, fantasy architecture, and copied commercial RTS artwork.

## Locked production conventions

### Camera and world scale

- Use an orthographic dimetric camera with **2:1 ground diamonds** and a camera elevation of **26.565 degrees**. Keep vertical walls vertical. Show the front/south and east faces. Do not use perspective vanishing points, lens blur, or per-asset camera changes.
- Keep the simulation map at **64 × 48**. Preserve every world position, navigation rule, physics value and footprint semantic. The global presentation trial uses **54 × 27 logical pixels per tile** at normal zoom **1.08**, retaining the same 2:1 camera and elevation. `client/world-presentation.js` supplies this shared scale to renderer and raster material projection. A 2.2-tile Main Residence ground footprint is approximately **119 logical pixels** before zoom, compared with about 75 at the former scale. Asset render dimensions and fixed source pivots remain unchanged; unchanged unit spacing occupies more screen pixels. This is a global placement trial pending actual browser visual review, never a per-asset fit or simulation change.
- If presentation scale needs refinement, make it deliberately in one shared configuration. Do not apply independent camera corrections to individual assets.

### Unit and building scale

- Ordinary humans should appear **32–38 logical pixels** tall; leaders **36–42 logical pixels**; horse and rider together **44–50 logical pixels**. Give units distinct equipment silhouettes without making leaders oversized. Keep the feet or hoof ground pivot fixed across directions and states.
- At normal zoom, target a grounded Main Residence about **110–130 pixels wide and 95–115 pixels high**, a Barracks about **100 × 80 pixels**, and a Granary about **85 × 70 pixels**. Measure each anchor against its ground footprint so paths and selection remain truthful. Roofs may overhang walls. No sprite may occupy several unblocked tiles invisibly.

### Sprite and animation conventions

- Use an immutable **1024 × 1024** source raster for a normal isolated asset, with ample transparent margin. Record runtime derivative sizes, visible bounds, and pivots in a manifest.
- Unit animation authoring cells must be **256 × 256 pixels or larger**, with a fixed cell and pivot. Do not fit each frame independently to its bounds.
- Author eight directions in this order: **E, SE, S, SW, W, NW, N, NE** (engine frames D00–D07). Required states are **idle, walk, attack, hit, death**. Review pilot keys before producing full frame sets. Atlasing is packaging; it does not replace review of the original frames.

### Lighting, shadows, and palette

- Use a soft sun from the screen’s upper-left/northwest. Light upper and left-facing surfaces; fill with warm gray. Do not mix opposing backlights or hide art in black shadow.
- Cast soft ground shadows toward the lower-right/southeast and add short, dark contact shadows beneath feet and foundations. Prefer a separate ground-shadow layer or consistent baked alpha. Avoid opaque halos and floating sticker-like sprites.
- Keep this shared palette: foliage jade **#355D43**, moss **#73895D**, water teal **#386E6E**, shallow water **#69948A**, earth ochre **#9B835D**, timber **#665039**, weathered terracotta roof **#8F5040**, warm-gray stone **#8B8A7C**, parchment cloth **#D6D0AE**, vermilion **#9F4039**, and aged gold **#C39637**. Jade and vermilion team trims must remain small and readable. Do not recolor historical identity indiscriminately.

### Materials and environment

- Render painted wood grain and planks, layered tiles, woven cloth, dull iron, worn stone, sacks, and rice bundles. Texture must support the silhouette. Avoid random pseudo-detail, unreadable glyphs, and plastic gloss.
- Use seamless painted grass and soil, natural shore and forest transitions, and no visible gridlines in final play. Make landmarks and resource zones coherent. Map data determines water and blocked mountains; artwork must agree with those gameplay regions.
- Water should be subdued turquoise with reflective paint, shallow brown-green edges, small shoreline foam, current cues, and low-amplitude waves. Gentle animation and wakes must not obscure units or navigation routes.
- Illustrate broadleaf trees, bamboo, and palms appropriate to riverlands. Establish at least **three unique vegetation clumps or species** before expanding the set. Vary density and scale under the common light. Use undergrowth, reeds, fallen branches, and rocks in moderation. Forest conceals but remains passable; mountains block movement.

### Architecture and characters

- Use plausible Vietnamese timber post-and-beam construction, courtyards, layered clay tiles, and restrained curved eaves. Military and storage buildings should be modest and show functional props. The political Residence needs a formal axis, layered roof, and banners. Avoid a generic fantasy Chinese palace or samurai castle. Each building’s gameplay role should be immediately legible.
- Premium historical leaders must follow inspected supplied references and dossiers, not a generic Asian-warrior design. For the Trần Hưng Đạo pilot, use a mature Vietnamese commander in gray lamellar iron, a dark-red robe or cape, restrained helmet and beard, and one continuous weapon.
- Keep a villager’s woven hat and undyed cloth; infantry’s padded or lamellar coat and single blade or shield; a long spear shaft; a historically appropriate matchlock; and believable cavalry anatomy and gait. Keep scale, materials, and light consistent across units.

### Effects, UI, and portraits

- Keep VFX historically restrained: muzzle flash and smoke, artillery recoil and impact debris, melee impact, ship wake and splash, and progressive building damage. Effects must be timed to the action and must not use fantasy glows or particle fog to conceal weak art.
- Give the UI a parchment, aged-bronze, and jade identity with clear hierarchy. It must include the game HUD, leader portraits, resources, rations, queues, and usable tooltips while keeping the combat viewport dominant. Avoid a SaaS dashboard. Typography must be readable at **1280 × 800** and **1920 × 1080**.
- Paint icons as functional item silhouettes such as a wood bundle, rice basket, iron ore, production item, or ability. Use a shared border, light, and scale. Geometric markers are permitted for selection, health, and navigation, but not as substitutes for visible units or buildings.
- Inspect existing premium historical portrait sources before use. Preserve their identity and files; do not casually regenerate identities. Derivative manifests must name their source and review status. King and General cards should show actual portraits, not text alone.

## Architectural research anchors

Use these as evidence for design decisions, not as images to copy. The Imperial Citadel of Thăng Long’s official Kinh Thiên Palace account describes a timber palace recorded in late-19th-century photographs, with two connected building masses, two storeys, eight curved roofs, and a courtyard. The 2025 excavation report documents palace column foundations and the shared-foundation, connected-hall form of Long Thiên Palace. UNESCO’s Huế monument record describes the deliberate relationship among the citadel, palaces, and natural setting. These sources support a formal axis, elevated masonry foundation, timber structure, tiled roof, and courtyard; they do not establish that every historical residence shared one exact form.

- [Kinh Thiên Palace — Imperial Citadel of Thăng Long](https://hoangthanhthanglong.vn/en/kinh-thien-palace-the-heart-of-the-imperial-citadel-of-thang-long/)
- [2025 archaeological excavation at the Kinh Thiên Palace foundation](https://hoangthanhthanglong.vn/en/preliminary-report-on-the-results-of-the-2025-archaeological-excavation-at-the-foundation-area-of-kinh-thien-palace/)
- [Complex of Huế Monuments — UNESCO World Heritage Centre](https://whc.unesco.org/en/list/678)

## First visual slice and review gate

Build one polished riverbank section with grass and soil, forest, water and shoreline; one beautiful Main Residence; a villager, infantry unit, cavalry unit, and Trần Hưng Đạo; consistent contact shadows; real movement, attack, hit, and death animation; controlled VFX; and finished HUD elements. Run the slice in the actual browser client without changing simulation coordinates or commands. A concept illustration or mock screenshot is not a playable slice.

Save every generation attempt, prompt, hash, and specific rejection reason. Treat generated images as raw candidates. Inspect anatomy, alpha, weapon continuity, viewpoint, scale, lighting, and normal-zoom integration. Do not automatically accept the first output or expand production before review.

The parent reviews normal-zoom screenshots and actual animation before inspecting source or provenance. Rate Characters, Buildings, Terrain, UI, Animation, VFX, Style Consistency, Historical Plausibility, and Gameplay Readability on a **1–10** scale. Every major category must reach **8/10**; anything below **8/10** is rejected for refinement. Do not fan out hundreds of assets before the slice passes this gate.

## Direction convention and tile anchors

Terrain cell `(x, y)` covers world `[x, x+1) × [y, y+1)` and is drawn at `(x+0.5, y+0.5)`. Entity pivots retain their actual simulation coordinates. Engine directions are world directions; screen headings follow the dimetric projection.

| Engine | World | Screen vector at zoom 1 | Heading |
|---|---|---|---|
| D00 | E | (+27, +13.5) | ESE |
| D01 | SE | (0, +27) | S |
| D02 | S | (-27, +13.5) | WSW |
| D03 | SW | (-54, 0) | W |
| D04 | W | (-27, -13.5) | WNW |
| D05 | NW | (0, -27) | N |
| D06 | N | (+27, -13.5) | ENE |
| D07 | NE | (+54, 0) | E |

Do not interpret a file's informal screen-SE name as engine D01 coverage. Current neutral sprites are explicitly D00 trials, not accepted eight-direction packages.
