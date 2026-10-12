# Shared compiler identity anchor — 485

Schema 2 jobs may supply `identityMaster` as an encoded and decoded RGBA SHA-pinned whole original image, using the same fixed canvas as the directional `master`. The existing `master` / `masterSHA` still bind the directional input and remain mandatory. Schema 1 rejects the new field; jobs without it use their existing master as both anchors.

Descriptors emit `identityMasterSHA` for the original anchor and `directionalMasterSHA` for the directional master. Receipts retain both pinned images. The master preview shows the canonical identity master when supplied, with legacy fallback to master. Whole raw source custody, uniform working/runtime resize, fixed pivot/layout and memory checks remain in place.

Optional preview-bank entries compare their original identity anchor, allowing genuinely different directional masters to share a bank. Production qualification records must also bind `identityMasterSHA` whenever the explicit original pin is supplied, in addition to existing directional master/action/frame bindings.

This is packaging support, not generation permission, directional-reference qualification, motion approval, installation permission or an action-bank completeness claim. The separate assembler must enforce registered identity/view locks and exactly eight directions. Existing selected infantry sources and held 482/483 results were not modified or compiled.

Validation: `node --test tests/sprite-production471.test.js` passed 15 tests, including distinct original/directional anchors and cross-direction preview, encoded/decoded pin tampering, wrong canvas/schema, explicit production identity binding, legacy compatibility, canonical preview pixels and original baked shadow preservation. Fixtures were temporary synthetic compiler inputs, not candidate artwork. No browser, deployment or full-suite execution.

Grounded jobs preserve the original shadow policy: baked, or separate with an explicit nonempty asset ID. Unknown/none policies remain rejected; no image pixels are changed.
