# 175 narrow loading failure completion

Decode failure now keeps the gameplay loading gate active. Retry clears it only after successful selected-bank decode; explicit menu cancellation clears the gate and disposes decoded art. Online snapshots continue updating actual latest state while the failure panel remains open. The only runtime changes from the prior successful175 source are removal of the catch-path gate reset and a read-only artLoading diagnostic.

28 focused tests passed, including execution of the actual main launch failure/issue/Pause functions with a failing renderer, explicit retry/menu callbacks, and existing lifecycle/cache/hash/deadline/compiler contracts.

One narrow Chromium browser fault/recovery flow passed with two ordinary online peers. The QA decoder flag deliberately makes createImageBitmap reject; it never changes gameplay state/commands/facing/speed. The error gate remained active after Escape/Stop keys, actual server snapshots advanced, successful Retry opened the field using current state, and a reload failure followed by Return to menu released decoded images while preserving encoded bytes. hold-harness-class-assumption.json preserves the first test-harness assertion failure; actual HTML uses game-screen, and the corrected check tests visibility.

receipt.json and source-pins.json/build-pins.json bind the new /tmp/art-bank-runtime-175/build-completion output. Exact baseline sim remains a266e0de5a6719579e48fd8a57888f09509f6af745190cb09b47c5641bab7796;177 work is excluded. The prior /tmp/art-bank-runtime-175/build and all prior source/build/browser receipts remain unchanged. Prior offline both-map/Firefox/new-room flows tested their previous chunk; this completion chunk claims only the new failure proof and focused tests.

All179 public149 files stayed exact. Owned browsers/servers closed with zero rooms. No broad match, deployment, restart, image call, commit or final-release claim.
