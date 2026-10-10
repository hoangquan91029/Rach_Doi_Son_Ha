# Isolated construction API276

`implementation.patch` targets two client modules plus one focused test. Canonical source/public and simulation remain unchanged. Stage: `/tmp/rds-building-state276-stage`.

Live buildings with an actual construction job or visible `underConstruction:true` request only authored `construction`. Death takes precedence, and construction suppresses hit overlays. No idle substitute. Construction is an ambient authored loop at fixed simulation `tick*50`, explicitly looping even if a descriptor declares `loop:false`: this API does not present finite construction progress or completion, because opponents receive only a boolean. The real completion snapshot chooses completed idle. A future finite progress sequence would require a separate honest contract.

Unfinished Wall/Gate use only standalone whole construction metadata mask0; no completed link inference, rotation or assembly. The existing completed topology remains unchanged and excludes construction. Existing completed exact-mask idle/hit selection stays unchanged; dead fortifications remain held because no eligible dead topology contract exists.

19 focused tests passed, including the existing real simulation visibility/private redaction/fog suite and shared renderer/picker topology contract. New fixture descriptors test all ten building families, owner/enemy snapshots, construction timing/looping, death precedence and fallback. Fixtures are not artwork or browser evidence. Current manifest has no construction assets; no art, build, scene, installation or promotion acceptance is claimed.
