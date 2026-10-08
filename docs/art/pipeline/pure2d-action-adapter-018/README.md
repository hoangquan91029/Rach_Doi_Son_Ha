# Additive action exporter v4

Use `python3 export-v4.py JOB.json NEW_OUTPUT` with the017 generic whole-frame job contract. Frozen017 files/receipts remain unchanged. Preview-v4 is byte-identical to017 preview-v3; exporter changes only its preview filename and locomotion eligibility.

Positive finite numeric `locomotion.distancePerCycle` is now allowed on walk, carry and carry_* states, matching client018. All other states reject locomotion metadata; nonpositive/nonfinite/boolean distance is rejected. Resource-specific gather_* remains ordinary declared-clock action when exported without locomotion. No source state relabeling or new art: callers still supply actual selected whole-frame action sources/custody. No actual carry/gather demo is claimed here.

One bounded test group passes using temporary NON_ART_TEST_ONLY fixtures deleted afterward: carry_wood candidate packaging with1.26distance, invalid distances and gather/attack locomotion rejected, gather_wood without locomotion accepted. Existing authoritative packaging validator is reused. No public/client/shared/runtime changes or motion/owner approval. Base pins and narrow diff are in READY.json.
