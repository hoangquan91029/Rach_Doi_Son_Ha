# Package 157 — read-only art coverage and scale inventory

Run `node scripts/art-coverage.mjs` for the actionable identity table; add `--json` for JSON on stdout or `--output /absolute/report.json` to save it. No files are written without `--output`. `--root`, `--local-root`, `--public-root` support another checkout/snapshot; `--no-alpha` skips Pillow decoding. Missing/hash-invalid selected routes return exit 1. Normal successful inventory returns exit 0 even with missing authored actions: coverage gaps are reported, not treated as program failures.

Inputs are only current client-selected manifests under `public/assets/art-v1` and the `dist` public149 snapshot. Historical/preparation/rejected directories are never scanned. The public snapshot client chunk is bound to receipt149's SHA; its actual referenced manifest paths determine exclusions. The absent public food099 route is local-only, explicitly excluded, and never promoted into public coverage. This is disk custody verification, not a new network or browser proof.

`report.json` and `summary.txt` are the actual tool outputs. Tests: `node --test tests/art-coverage.test.js` — 6 passed. They cover static versus animated presence, absent directions, failed/rejected images, deduplication and conflicting metadata, actual roster counts, unavailable routes, and explicit noncombatant attack exceptions.

| Finding | Actual result | Action |
|---|---|---|
| Local union of opt-in routes | 27 images; 17,500,160 decoded RGBA bytes | Keep food pending, not public approved |
| Public149 union | 26 images; 16,942,592 decoded RGBA bytes | Preserve optional camp route; default URL still fallback |
| Camp bank | 26 images; 16,942,592 decoded RGBA bytes | Bank-specific budgets are separate from route union |
| Villager core | idle D0/D1, animated walk D1 only: 3/40 slots | Complete qualified D0 walk, then remaining actions/directions |
| Infantry / cavalry | 1/40 idle slot each | Author separate family pilot before fanout |
| Leader Trần Hưng Đạo | one D0 idle, general runtime mapping only | Role-sharing decision remains open; King is not covered |
| Other leader IDs / remaining unit types | no authored core slots | Preserve 12 actual IDs and 11 unit types as separate scopes |
| Buildings | 6 idle; 4 missing idle; all construction/hit/death absent | Shipyard/fort/wall/gate, then changed-state pilots |
| Scale at default zoom 1.08 | villager D0 alpha 38.96px; D1 idle90.11; walk91.61–93.12 | Scene intake should resolve old/new scale mismatch |

Alpha measurement decodes actual frame cells and computes `(alpha bbox height / cell height) × render height × NORMAL_ZOOM`, without fitting individual frames or changing pixels. These bounds include contact shadows/equipment, so they are visible-alpha extents, not anatomical body height. Raw canvas, render cell, runtime canvas, fixed pivot and every frame bbox remain in JSON. This formula evidence does **not** replace the required actual mixed gameplay scene intake. Package157 makes no scene acceptance claim and no scale edit.

Coverage requires an existing hash-matching runtime file. A one-frame idle counts as minimum static idle; a one-frame attack/walk/hit/death is STATIC_ONLY, never animation. Hash dedup uses actual encoded SHA across aliases/environments; it estimates unique RGBA image storage, excluding browser canvases, masks and caches. Per-route and cross-route budgets are retained separately.

Owner032/141 explicit receipts are attached only to matching villager D1 gather action. The original shown-loop subject hash is verified. Runtime equivalence is not inferred from action names or differing export hashes; owner naturalness acceptance stays scoped to the loop shown. Manifest review declarations remain declarations. No visual, owner release, full roster or public final-release PASS is granted.

Runtime behavior mapping is documented separately from expected coverage: villager/infantry/cavalry, general tran_hung_dao, six buildings; building world routes remain gated; hit/death override exact state; gather uses resource-specific lookup then generic gather. Loaded return travel already uses walk. Simulation's brief carry transfer state has no authored carry raster remapping. The mapping includes its raster-source hash and must be rechecked when runtime mapping changes. The expected matrix intentionally records five core actions × eight directions for each of 11 types and 12 IDs; wagon/transport attack is NON_APPLICABLE because actual damage is zero, with load/unload presentation tracked separately when mapping is decided. Generic King/General rows describe role indirection, not additional identities to sum with the 12 leader rows. Shared versus separate King/General art remains an explicit planning decision.

No runtime/assets, active dist, deployment, full match, image call, or scale change was made. The project remains INCOMPLETE.
