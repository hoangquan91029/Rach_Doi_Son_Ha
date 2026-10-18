# TASK: Complete 2D Pixel Art Sprite System Rebuild

## Objective

Completely rebuild the character sprite and animation system for the Trinh–Nguyen RTS project.

All character sprites must be newly created as authentic 2D pixel art. Existing character sprites must not be reused, recolored, rescaled, traced mechanically, or used as final runtime assets.

The only permitted legacy references are existing Ruler and Commander character images, which may be used solely to preserve character identity, costume, and historical appearance. These characters must also be recreated from scratch as 2D pixel art.

## Non-negotiable Requirements

1. Every sprite frame must be exactly **128×128 pixels**.
2. Every animation must support **8 distinct directions**: S, SW, W, NW, N, NE, E, SE.
3. Every direction must have **at least 8 real animation frames**.
4. Every unit must support `idle`, `walk`, and its relevant interactions.
5. Use genuine **2D pixel art only**: hard pixel edges, consistent pixel density, a coherent palette, and transparent backgrounds.
6. No 3D models, smooth vector art, blurry textures, anti-aliased character edges, or interpolated pseudo-frames.
7. Walking must alternate both legs with correct weight transfer and ground contact.
8. Interactions must show meaningful body movement, correct tool handling, and identifiable action phases.
9. Maintain consistent visual identity, scale, ground anchors, equipment, and lighting across all frames and directions.
10. All generated sprites must pass automated and visual validation before integration.

## Phase 1: Repository Audit and Asset Reset

- Inspect the existing sprite assets, rendering code, animation loaders, and references.
- Create a recoverable Git checkpoint before removing legacy content.
- Preserve only Ruler and Commander reference images in a dedicated reference directory.
- Remove all existing character sprites from the active game asset pipeline.
- Eliminate outdated imports, hardcoded paths, and legacy sprite references.
- Do not delete unrelated game systems, buildings, or source code.
- Produce an audit report identifying what was removed, what was retained for reference, and what must be rebuilt.

## Phase 2: Define a Unified Pixel Art Standard

Create and enforce `docs/PIXEL_ART_STYLE_GUIDE.md`.

Specify:
- RTS 3/4-view visual language.
- Character proportions and world-scale consistency.
- Pixel density and outlines.
- Color palette and lighting direction.
- Costume and equipment consistency.
- Historical visual-reference requirements.
- Transparent background and alpha handling.
- Sprite positioning and ground anchors.

All future characters must comply with this guide.

## Phase 3: Build the Sprite Atlas Framework

Use separate 1024×1024 pixel atlases for each animation.

Atlas layout:
- 8 columns: frame indices 0–7.
- 8 rows: directions S, SW, W, NW, N, NE, E, SE.
- Every cell is 128×128 pixels.
- All frame positions are deterministic.

Implement reusable animation metadata, animation loading, direction selection, frame timing, anchor positioning, and non-looping interaction events.

Create `docs/ANIMATION_SPEC.md` and `docs/SPRITE_PIPELINE.md`.

## Phase 4: Produce a Complete Worker Pilot

Create a fully new 2D pixel art Worker with:
- `idle`: 8 directions × 8 frames.
- `walk`: 8 directions × 8 frames.
- `chop_tree`: 8 directions × 8 frames.

The walk animation must demonstrate alternating left and right foot contact, body weight transfer, and believable slow locomotion.

The axe-cutting animation must demonstrate preparation, raising the axe, swing, impact, and recovery.

Do not move to mass production until this character passes quality review.

## Phase 5: Rebuild Ruler and Commander

Use retained reference images for visual identity only.

Rebuild each character in authentic 2D pixel art.

Preserve recognizable facial features, silhouette, costume, ornaments, rank distinctions, and dignified movement.

Required animations:
- Idle.
- Walk.
- Sword attack or character-specific interaction.

All animations must have 8 directions and at least 8 frames per direction.

## Phase 6: Rebuild All Remaining Character Units

Apply the approved production workflow to other units, including workers, infantry, musketeers, cavalry, commanders, and appropriate crew characters.

Implement class-specific interactions instead of one generic interaction animation.

Allow additional actions such as harvesting, mining, building, reloading, firing, and attacking where needed.

Reuse the newly designed architecture and workflow, never the deleted legacy sprite artwork.

## Phase 7: Automated Quality Assurance

Implement validation for:
- File existence and expected naming.
- Atlas dimensions.
- Exact 128×128 cell sizes.
- 8 supported directions.
- Minimum 8 frames per direction.
- Transparency and alpha validity.
- Character visibility within frame boundaries.
- Anchor consistency.
- Missing or duplicated animation frames.
- Metadata correctness.
- Interaction events.
- No legacy asset dependencies.

Also perform visual review for walking mechanics, animation continuity, costume consistency, perspective accuracy, and pixel art integrity.

Generate preview GIFs and an in-engine animation viewer showing all 8 directions.

## Mandatory Agent Documentation

Create or update `AGENTS.md` so every AI agent must read:

1. `docs/PIXEL_ART_STYLE_GUIDE.md`
2. `docs/SPRITE_PIPELINE.md`
3. `docs/ANIMATION_SPEC.md`
4. `docs/SPRITE_QA_CHECKLIST.md`

These documents are authoritative. Agents must not invent missing character specifications, directions, animation states, frame layouts, or metadata fields. Unverified assumptions must be recorded explicitly.

## Deliverables

- New pixel art sprite atlases.
- Consistent per-unit animation metadata.
- GIF previews.
- Reusable atlas generation and validation scripts.
- Integrated animation controller.
- Documentation and agent workflow instructions.
- Repository asset audit and replacement report.
- In-engine validation results.

## Completion Rules

A character is complete only when all required directions and frames exist, its animations are visually coherent, its atlas passes structural validation, and the character works correctly in the game engine.

Do not declare an animation complete based solely on successful image generation.

Never fabricate missing frames, silently duplicate poses to meet the minimum frame count, or report unverified visual quality as passed.

**Priority: animation correctness and consistent authentic 2D pixel art over production speed.**