# Review repair535

VERIFIED local source/tests; visual and actual engine qualification OPEN.

Root changed ANIMATION_SPEC before repair to exact registry {schema,clips,strides}. Existing REPORT-before-review.md and outputs-before-review.json preserve original receipt; tests-initial-failure.log remains unchanged.

- validatePixelRegistry now checks exact stride records: identity, positive distancePerCycle, evidence path/SHA256, review PASS, unique identity. Animators resolve stride per exact identity; missing stride remains explicit unqualified frame0. No automatic stride measurement or footlock claim.
- Default bank requires structural/visual/runtime PASS. Explicit private allowCandidates true allows structural PASS and visual/runtime PASS or UNKNOWN, rejects FAIL/null, reports CANDIDATE and qualifiedfalse. No query switch or active registry promotion.
- Real IsoRenderer accepts third options argument {pixelOptions}; stores it and constructs bank with it. releaseArt resets retained bank with same options/stride lookup. Viewer mount accepts optional {bankOptions}. Normal game/menu passes no candidate mode.
- Actual simulation begins attackStartedTick before pendingAttack impact, retains attackImpactTick and attackReadyTick in public view. Bank now reuses attackAnimationTime with pixel event/frame adapters, maps WEAPON_CONTACT/DEAL_DAMAGE/FIRE_PROJECTILE to authoritative windup/impact/recovery. Episode finite duration similarly reuses episodeAnimationTime with actual total clip duration. No simulation writes.
- New active registry remains clips[]/strides[]; no generated/fabricated final assets.

Validation:9 focused tests PASS in tests-repair.log, including two different measured strides, missing stride, reset, candidate/default review gating, pending attack contact/recovery and actual IsoRenderer construction/options after release. Fixtures are metadata/decoder stubs for source tests only, never artwork or qualified stance evidence. Syntax bank/viewer/renderer checked. Repair audit preflight retained. No browser/full suite/build/deploy/generation.
