# Viewer source repair535

VERIFIED13 focused source tests PASS: tests-viewer-repair.log (11 integration plus2 updated boot tests). Old boot expectations preserved exact in before-boot-tests.js; all earlier receipts/logs retained.

Preview-only startPixelPreviewEpisode aligns a fresh selected episode to simulation tick boundary and clears prior episode fields. Ability/load/unload/build receive started/endTick and clip loop; attack receives started/impact/ready derived from actual selected clip duration and contact marker; hit receives five-tick origin; gather gets proper resource/startedTick. No game simulation entity or commands touched. First preview frame suppresses elapsed delta to showF0. Looping preview episodes extend their local endTick; finite episodes use actual clip duration. Stop requests idle even if absent and reports explicit missing. UI preview still uses synthetic clocks, cannot establish actual game transitions.

Renderer bank draw accepts an already sampled result. Viewer samples once then draws/displays that exact result, preserving markers. Menu close removes dialog DOM; animation callback stops on closed host. No active character assets added.

Default allPASS review values are trusted declarations, not authenticity guarantees. Root must run actual atlasQA against exact atlasbytes before admission and record process/hash receipt. Registry still clips[]/strides[], zero admitted artwork. No extra schema fields or fake automated approval added.

No browser/runtime/art/owner/release qualification from these checks; root owns next private browser review.
