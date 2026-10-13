# Reusable image instructions — v1

These are recipes for shared templates, not image orders. Current executable templates live in `unit-production/templates/`; exact accepted fields come from `scripts/sprite-prompts.mjs`. Never paste extra fields into a validated payload, drop a failing guard or invent seed/mask/pose parameters. Built-in tool currently exposes prompt, inspected reference paths and transparency; it does not expose a strict skeletal constraint or separate mask argument. A textual request to respect a guide is not deterministic control.

## Shared invariant block

Fill from immutable identity.json: identity/master hash, selectedview, physical limb/equipment ownership, body proportions, face/headwear/costume/palette/materials, camera/light, canvas/pivot/family scale/shadow. A ship uses its verified whole-hull/rigging/assembly lock, not invented weapon hands; idle-only no-held-equipment observations do not define action tools. Missing required values or unresolved placeholders block dispatch.

Variable block: action, engine direction and verified projected label, slot/phase, receiving/support/swing contact, own-lane motion and occlusion, torso/cloth motion, tool interaction, selected neighbors, next-key intent. Specify what changes; do not lock the whole body rigid.

## 1 — Canonical identity (only genuinely missing identities)

```text
Create ONE complete original historical unit identity for [identityId].
Historical/source anchors: [verified sources, uncertainties explicitly listed].
Required role, costume, body proportions and equipment: [approved design scope].
Camera/layout/light: [locked project contract].
Realistic illustrated whole2D, transparent background, complete silhouette.
Do not borrow another leader's face/body or claim undocumented historical facts.
Output is an identity candidate, not an approved view or animation.
```

Existing units never use this to redesign themselves. Warship and missing leader world identities require their own finite identity work order and source review first.

## 2 — Missing directional view

```text
Create ONE missing view of the SAME existing [identityId].
Appearance: [original master]. Adjacent selected view: [actual pin or none].
Target engine direction [D], projected facing [verified label].
Change viewing direction only; keep person/vehicle, costume, proportions,
physical weapon hands, complete equipment, camera, lighting, pivot and scale.
Neutral whole pose, transparent background. No mirror, crop or per-frame fit.
```

Eight-direction reference sheet is deterministic assembly of eight selected view PNGs, not one generated mosaic to cut apart. P1 view dispatch is implemented489; use a registered explicit view order with one slot/no action or phase values. This recipe is not an order or bypass.

## 3 — Action key

```text
Edit the SAME approved unit into ONE [action] key: [slot, phase].
EDIT TARGET: [original/view or legal selected target, actual first input].
APPEARANCE ANCHOR: [canonical original/view, actual input role].
POSE REFERENCE: [original-derived whole-clothed guide, if present].
Physical receiving/support/swing identities: [landmarks, not screen-side labels].
Movement along projected travel/own depth lane: [concrete foot/body path].
Body weight/counter-swing/cloth: [small natural movement].
Equipment interaction/grip: [specific]. Next selected key: [destination].
Keep same identity, proportions, full silhouette, camera/pivot/family scale.
One whole illustrated transparent frame; no labels, floor or guide markings.
```

Walk uses opposing contacts before passing/in-betweens. Attack/work/death/load/unload/ability replace foot instructions with the archetype's actual contact/tool/body requirements. Run key recipe stays NOT_APPLICABLE until a real run action is added by the human; do not create a redundant faster walk bank.

## 4 — Neighbor in-between

```text
Create ONE whole-frame in-between for the SAME [identityId/action/D].
Appearance master: [pin]. Previous selected key: [pin, phase].
Next selected key: [pin, phase]. Current slot/phase: [values].
Advance [physical moving limb/tool] from [previous landmark] toward [next].
Support/contact stays [specific]; occlusion order [specific]; body moves [specific].
Do not duplicate an endpoint, exchange equipment hands or invent a new body.
Keep whole canvas, camera, pivot and scale; finish one transparent illustration.
```

Only selected neighbors from the bound current job are legal. Parallel calls require both endpoints already selected; no in-between depends on an unreturned key.

## 5 — Targeted visible repair

```text
Correct ONE visible defect in [slot]: [observed defect at gameplay size].
First input EDIT TARGET: [legal selected pose pin].
Appearance anchor: [original pin]. Selected neighbors: [actual pins].
Required change: [one concrete correction toward neighboring motion].
Keep identity/equipment/composition and accepted motion outside that correction.
No extra polish, redesign, camera/scale change. One whole transparent output.
```

Clothing repair uses this only if flicker, clipping or changed silhouette is visible while playing. Background/alpha repair uses built-in transparency editing with the exact existing whole frame, unchanged canvas/pivot; confirm the defect first. An alpha decode/packaging bug is a code fix, not an image edit. Neither counts as a new accepted motion phase. Target-first491 and guide-first492 both failed their actual probes; methods CLOSED. No equivalent retry authorization.

## 6 — Export (no image call)

Inputs: existing schema2 job and selected source pins. Use shared sprite-production compiler once; working256/runtime128 directly from raw, fixed family geometry, padding2, no trim/rotate. Use shared action-bank assembler for eight qualified directions. It emits CANDIDATE output; no generated prompt should create atlases, filenames, metadata or QA evidence.

## 7 — Worker assignment

```text
Model: gpt-6.1-sol. Reasoning: low.
Own identity/action/directions/slots: [exact set].
Read: AGENTS + subsystem contract + exact identity/job/receipt.
Allowed references: [pinned roles/order]. Exclusive output directory: [path].
Dependency: [selected endpoints or unresolved blocker].
Call cap: [missing slots], correction cap≤2, durable claim before each call.
Use existing templates/compiler/preview; no new unit or direction outside scope.
Do not edit runtime/common manifest/other worker files/production.
Return outputs, actual call count, held reasons, brief loop review scope,
source-bound receipt, read preflight and next dependency. Never self-approve art.
```

## Record actual tool behavior

A claimed request keeps actual ordered paths, prompt version/text hash, slot/phase, generator name, returned output mapping and raw bytes. Model/seed/timestamp stay null if not supplied by the tool. Never infer a model ID from marketing names or the worker model. A receipt records what was sent/returned, not only what the prompt intended. Helper acceptance does not grant image-call permission by itself.

## Implemented guide-first variant492

Use executable `unit-production/templates/guide_key.txt` only with a registered typed `referenceMode:guide-first` order. Image1 is a source-bound whole-clothed `guidetarget`; image2 is original matching master or selected matching view for appearance. No original walking edit-target is required. Do not promote a held frame, foreign guide or arbitrary primary image into this role. Structured `rds-guide-target/v1` provenance and exact job/phase/pending slot are mandatory; prepareOrder and durableclaim still apply.

Request one whole illustrated original person in the guide pose, with original face, clothing, camera, bodyvolume and material rendering. Guide vector/personstyle is not finalstyle, and its pixels cannot be spliced/warped into runtime art. Actual492probe did **not** follow passing/scale sufficiently; this is a legal reference recipe, not a pose-control guarantee or permission to retry.


##495 mandatory template fields and local conditioning boundary

Every request must supply actual identity anchor, edit target if applicable, selected neighbors when required, action/D/slot, verified projected facing, fixed bodyvolume/face/clothing/equipment/camera/light/pivot/scale, contact/support/swing lanes and occlusion, weight/tool motion and next-key intent. Correction names one observed gameplay-size defect. Unknown required values block generation. One complete transparent realisticillustration; no redesign/cutouts/warps/mirror/fit.

Local2D research is not executable built-in template data. Only a qualified local capability may add real ControlNet structural and IP-Adapter appearance inputs; do not invent built-in tooloptions. Approved new-mechanism pilot maximum2passing outputs+1correction after rootregistration; existing methods remainclosed. Read root task contract and actual model/API version before any request. Prompt output is not evidence that instructions succeeded.
