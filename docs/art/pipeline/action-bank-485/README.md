# Shared eight-direction action packaging485

This adds the missing shared action-bank assembly step; it does not create artwork, install a bank, grant motion approval or release the game. Current infantry cannot satisfy it because D1–D7 and qualified movement are missing.

## Reusable commands

- `node scripts/sprite-order-run.mjs claim /absolute/request.json`: reserve one trusted finite pending slot atomically before builtinimagegen dispatch. Retain its token/prepared request; only the trusted project ledger is used by the CLI.
- Invoke builtinimagegen with that prepared prompt and actual pinned references, under the existing source/pose gate. No CLI/API image generation is introduced.
- `node scripts/sprite-order-run.mjs settle /absolute/result.json`: consume the matching actual output/failure into held custody. It cannot select a frame or grant approval. Root performs the existing brief review/selection separately. Unknown dispatch stays consumed; do not reset a lock, retry or change counters merely because time elapsed.
- `python3 scripts/sprite-production.py /absolute/direction-job.json --mode selected`: package existing selected whole frames. Schema2 may separate `identityMaster` (canonical original) from `master` (selected directional view); both retain hashes, and master preview shows the canonical source. Legacy jobs remain valid.
- `node scripts/sprite-action-bank.mjs /absolute/bank-config.json`: validate and copy eight existing clips into a new portable candidate folder, manifest, output pins and existing eight-cell preview. Canonical/public manifests are never edited.

The bank config contains `identity`, canonical `action`, `outDir`, exactly eight `clips` and necessary `dependencies`. Each clip has SHA-pinned `descriptor`, `job`, `receipt` objects (`path`, `sha256`); each shadow dependency has `id` and a pinned `descriptor`. Config input paths resolve against its directory; trusted registry paths resolve against the project root. Optional `aliases` declare shared clips permitted by actionSpec (repair/build, return/walk, destroyed/death, sink/death), without drawing duplicate clips. An extraFrameReason is required for a clip over the initial frame budget.

## Package contract

Each direction must have a selected registered view and the same original identity anchor. No static fallback, diagnostic/held frames, excluded source path or hash can complete it. Actual encoded/decodedRGBA, source dimensions/path, ordered phases, timing/events, fixed128cells, padding2/slot132, camera/family/pivot/render and the registered original baked-or-separate shadow policy, plus explicit loop policy are checked. Attack has one contact marker; death is nonlooping and at most4s. Source hashes and byte-bound compiler receipts retain custody. Unique runtime pages plus shadow must fit128MiBdecoded/64MiBencoded; manifest must fit2MiB. Budgets are not raised.

The resulting eight-direction package is CANDIDATE, with visualApproval/runtimeQualified/installAuthorized false. Root still needs actual gameplay-size loop and changed-scene intake, measured land stride before production, plus separate release qualification. Tests use transparent colored compiler fixtures only; they are not replacement art or synthetic gameplay proof.

Original spear/firearm/cavalry/artillery/transport PNG references were recovered without modifying any image. Whole-canvas Lanczos exactly reproduces each retained current derived source. Their custody receipt is ../original-identities-485/receipt.json. Equipment-side bindings still marked unresolved remain unresolved, and no missing view/action is silently selected.

Eight ordinary identity registries now retain a layoutLock derived from the current 51-asset manifest. This is source/layout custody, not visual approval. Baked originals do not gain a separate shadow; infantry/spearman retain their explicit separate shadow. Missing warship and unresolved leadership sources remain missing.
