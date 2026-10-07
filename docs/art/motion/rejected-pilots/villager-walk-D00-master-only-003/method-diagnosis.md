# Method diagnosis and proposed revision

## What failed

- Pilot 001 conditioned the F04 edit on both the locked master and selected F00. F04 retained the near/screen-right leading contact. The two-key fixed-38 comparison therefore showed the same ownership at F00 and F04.
- Guided correction 002 added an explicit, color-coded geometry guide, but kept F00 attached for continuity. Its raw output again had the near/right foot forward. The second call exhausted its cap; it is a second failure of phase transfer, not a selected F04.

## Why this is materially revised

The proposed one-call method changes the input conditioning: Image 1 is only the locked neutral identity master; Image 2 is only a new, independently authored geometry guide for F04 contact ownership. The selected F00 is deliberately omitted from all model attachments. It remains review evidence in these notes only. This removes the strongest visual source for repeating F00 while retaining the identity authority and explicit phase geometry. The new guide also keeps the far chain comparable to the master’s apparent limb lengths, avoids a knee-over-knee crossing, and separates the contact points by about 8 px horizontally in the fixed 38 px preview.

This is a testable conditioning change, not proof that identity-motion will transfer the opposite contact. The model can still ignore a guide. Keep the cap at one proposed call and halt on a repeated near/right lead.

## Source lock and model inputs

- Locked identity: `/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha/docs/art/characters/villager-neutral-D00-screen-ESE/raw.png`; SHA-256 `145b976ffd1bdf563cb5da78806547e6849424054f2c26fc297e155a0b366e94`.
- Proposed image input 1: that master, identity/camera/proportion/material authority.
- Proposed image input 2: `/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha-art-lease/villager-walk-D00-master-only-003/F04-model-guide.png`; geometry and phase ownership only, model-only.
- No other reference images are proposed. F00 and rejected F04 images are excluded from the call's attachments.
- Canvas 1254 × 1254; root `(650,1140)`; review transform is the complete canvas at `38/1254`, with the same root placement; no crop, mirror, per-frame fit, or resizing of source frames.

## Call state

`imagegen_calls_made: 0`; `proposed_calls: 1`; `parent_authorized: false`. The revised exact prompt is saved in `F04-proposed-prompt.txt`. Wait for parent to inspect both guide PNGs and the prompt before any ImageGen invocation.
