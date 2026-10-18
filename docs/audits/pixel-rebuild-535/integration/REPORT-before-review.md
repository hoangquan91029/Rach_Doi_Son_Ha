# Pixel integration535 source receipt

VERIFIED source integration; visual/runtime/owner/release remain OPEN. No artwork fabricated.

Checkpoint supplied by root: refs/checkpoints/pixel-rebuild-535-before / 59278221d693a37bf8c90d7b1981a707cc86efeb. No commit/stage/reset by worker.

## Detached active character loading/drawing

- client/art-assets.js removes unit and portrait entries from every loaded route manifest before bank configuration, preload, cache warming, or paging. Original manifest files remain untouched. Buildings/terrain/props/vfx/UI retained.
- client/renderer.js dispatches living units only to new pixel bank. Legacy vector character routines remain archival source with no active renderer call. Living health bars, selection and world/minimap HP0 filtering retained.
- client/boot-ui-assets.js does not request leadership portraits. client/main.js keeps accessible leader names and explicit missing portrait marks; no leadership image URLs remain in client code.
- New registry public/assets/pixel-v1/registry.json has zero clips, zero accepted poses. Missing unit marker is deliberately unqualified.
- Menu opens a bundled in-engine dialog viewer via dynamic import; standalone client/pixel-sprite-viewer.html is a dev convenience. Both use same bank/controller; all8 direction controls, action/Pause/Stop and honest missing/GIF states.

## Manifest inventory

Exact entry source/runtime provenance in legacy-inventory.json. Counts below refer to original files, not accepted pixel coverage.

| Manifest | Original units | Original portraits | Retained other entries |
|---|---:|---:|---:|
| public/assets/art-v1/camp-148-manifest.json | 8 | 0 | 18 |
| public/assets/art-v1/food-099-manifest.json | 8 | 0 | 10 |
| public/assets/art-v1/fort-202-manifest.json | 14 | 0 | 37 |
| public/assets/art-v1/gather-026-manifest.json | 7 | 0 | 10 |
| public/assets/art-v1/iron-137-manifest.json | 8 | 0 | 16 |
| public/assets/art-v1/manifest.json | 4 | 0 | 10 |
| public/assets/art-v1/shipyard-165-manifest.json | 8 | 0 | 19 |
| public/assets/art-v1/stone-361-manifest.json | 0 | 0 | 16 |
| public/assets/art-v1/terrain-113-manifest.json | 7 | 0 | 12 |
| public/assets/art-v1/terrain-115-manifest.json | 7 | 0 | 13 |
| public/assets/art-v1/terrain-120-manifest.json | 7 | 0 | 14 |
| public/assets/art-v1/terrain-122-manifest.json | 7 | 0 | 15 |
| public/assets/art-v1/terrain-127-manifest.json | 7 | 0 | 16 |
| public/assets/art-v1/walk-014-manifest.json | 6 | 0 | 10 |
| public/assets/art-v1/workshop-144-manifest.json | 8 | 0 | 17 |

## Reference custody

108 legacy leadership PNG/WebP copies retained ONLY under docs/art/pixel-references; exact paths/SHA256 in index.json. These include12 leader portraits and available directional identity images; not proof of historically correct costume or selected reference quality. Ordinary unit imagery not copied into the dedicated reference bank. All original files, raw candidates, previous manifests and claims remain preserved.

## Controller and limitations

pixelAction uses current authoredActionStates; villager gather_wood alone aliases chop_tree. Identity is ordinary type or exact King/General character. Clock inputs reuse bounded renderer visual time, visibleAction startedTick, attackStartedTick/lastAttack, hitUntil−5 and measured createLocomotionPhase travel. Event markers are presentation-only; no simulation writes. First authoritative elapsed sample is primed at0; idle/Stop enters F0. All atlas cells128; fixed64 logical size and anchor64,112; imageSmoothingEnabled false; integer placement. Reviewed stride absent => explicit unqualified walk.

No real pixel atlas exists, so runtime loading/8facings/contact/seams/transitions/hit/Pause/Chrome/Firefox, independent visual review and public qualification all remain OPEN. Registry all-PASS admission cannot itself authenticate review prose or visual quality. GIF links become relevant only when actual compiled files exist.

## Checks/errors

- audit preflight retained preflight.txt.
- Initial shell python command failed command-not-found; reran same guard/edit using python3 before source mutation.
- Initial focused test expected manifest cache rejection; actual candidate-only manifest correctly skipped unavailable candidates without rejection. Initial4PASS/1FAIL preserved tests-initial-failure.log; corrected expectation.
- Final5 focused checks PASS in tests.log. Syntax checks main.js, bank, viewer PASS. No install, full suite, active build, runtime scene, generation, deploy or public mutation.
