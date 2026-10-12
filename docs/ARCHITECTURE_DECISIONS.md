# Architecture decisions — audit488

| ID | Decision | Reason / limit |
|---|---|---|
|01|Keep Canvas2D/shared simulation/networking|Existing playback supports the required representation; no evidence warrants an engine rewrite|
|02|Immutable original identity, pure whole2D|Latest human requirement; temporary2D guides allowed, final cutouts/warps/3D/mirrors forbidden|
|03|Five layers: identity → motion → projection → finished frames → runtime|Reuse motion constraints without borrowing another unit's body pixels|
|04|Villager qualification A, then Infantry reuse B|Latest audit directive supersedes infantry-first queue; preserve candidates and accepted work loops|
|05|All applicable action×8dirs, Standard7104 positions|Possible run/charge/deploy examples do not create mechanics or reduce explicit scope|
|06|Built-in current provider; optional local2D feasibility|User selected research branch; availability and quality need actual evidence, not an installation claim|
|07|Separate source/technical/motion/runtime/owner/release|Checksums and static fallback cannot become visual approval|
|08|Extend existing compiler/finite runner|Fix view dispatch, per-job references and equipment locks; evidence schema wraps existing runtime descriptors|
|09|Fixed family layout, current128cell/padding2|Larger/rectangular extension only after measured clipping; never fit individual frames|
|10|Per-match/action pages under128MiBdecoded/64MiBencoded|Whole target472.18MiB padded minimum; don't raise caps to pass|
|11|One state, roadmap and queue|Historical receipts preserved, conflicting active instructions removed|
|12|Root integration; three exclusive Sol6.1/Low workers|No duplicate slots/calls, independent review|

A motion record is a semantic plan, not a means to reconstruct every view from one picture. Occlusion and clothing still require whole-frame authorship. A schema only enforces its implemented checks.

Current source/local qualification/public release are distinct. Future shared changes require pairedfrontend/backend release with verified451frontend+230backend rollback. This audit edits docs and verification helpers only.
