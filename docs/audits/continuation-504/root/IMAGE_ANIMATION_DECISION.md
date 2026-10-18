# Sprite animation route review — 13 October 2026

The human wants original 2D images with a three-dimensional illustrated appearance, comparable to Age of Empires. This review changes the next research decision; it does not authorize a new image call, select a model, relax artwork requirements or declare the full game complete.

## What the evidence establishes

- OpenAI's image-generation guide supports image-reference and multi-turn editing, and explicitly lists recurring-character consistency and precise composition as limitations. API conversation-state controls are not automatically controls of the built-in tool.
- The actual built-in tool exposes prompt, reference images and transparency. No strict rig, motion timeline, persistent latent identity, seed or pixel-preservation control is exposed here. Always pass actual images; a filename or “remember the previous frame” is insufficient.
- Project491/prepared.json supplied an edit target, original South, both contact neighbors and a clothed passing guide. Its trial review found broadly preserved appearance but failed foot/phase control. Project492/prepared.json supplied the guide and original and also failed. Missing references alone therefore do not explain the observed failures. Neither closed method can be renamed and retried.
- Blender501 and504 generated valid PNGs but failed the original appearance gate. A working MCP or a controllable rig cannot make a poorly matched model into the canonical unit. Simplified rounded garment geometry is not an accepted replacement.
- World's Edge describes Age of Empires: Definitive Edition as a 2D engine using images rendered from 3D models. A 3D-looking sprite does not require a real-time3D browser engine, nor does that establish that every similar project needs Blender.

## Options, with honest limits

| Route | Strength | Limitation / current decision |
|---|---|---|
| Independent GPT edits of individual frames | Attractive original-style illustration, existing tool | Existing pose-control trials failed; no temporal guarantee. Do not repeat them. |
| Joint four-key image proposal for one complete cycle | Lets one generation see contactA, passingB, contactB, passingA together; may reduce between-call visual drift | PROPOSED experiment, not verified improvement or production route. Exact contacts/pivot/layout still may fail. Existing one-frame order contract must explicitly version this package before a call. |
| Authored whole-frame2D animation with neighboring-frame/onion-skin review | Explicit pose, body volume and contact decisions while retaining illustrated appearance | Requires actual drawing/authoring capability and work; software names do not supply that skill. No transformed cutout pixels as final sprites under current rules. |
| Qualified faithful3D model rendered to2D | Reusable rig/actions and eight views; deterministic geometry | Up-front model/material fidelity is essential. Current501/504 models failed; no rig/fanout or further parameter retry. |

## Recommended next experiment with currently available illustration tools

Prefer a bounded joint-key investigation over more independent frame calls or further simplistic neutral models. Keep the existing original as the sole identity authority. A possible package contains four whole-body keys in one regular sheet: F0 contactA, F2 passingB, F4 contactB, F6 passingA. Supply an original-derived full-cycle guide and explicit physical-leg roles. This is a proposed change in generation context, not a promise that GPT controls geometry.

Before executing: review a materially different method, account for all old consumed/closed and unresolved claims, version the current one-frame slot contract, and issue a finite root order. No image call is opened by this document. Keep raw output. If a sheet is eventually tested, extract complete cells only with a common transform; never stitch limbs, fit frames or use image resampling to hide errors.

If the four keys fail identity or phase, retain them and stop that method. If they work, create only the missing whole-frame in-betweens using the immutable original, selected endpoints and the complete cycle as actual inputs. Do not edit only the latest output recursively; that can propagate drift. Review one actual gameplay-size loop and practical travel/Stop before any direction or unit fanout.

For a reliable full-roster route, the unresolved dependency remains actual animation authoring: either a faithful illustrated2D sequence or a faithful rigged source model. GPT Image can help appearance and frame illustration, but prompt/history management alone has not demonstrated reliable motion in this project.

## Primary sources actually opened

- [OpenAI image generation](https://developers.openai.com/api/docs/guides/image-generation): multi-turn image context; consistency and composition limitations.
- [OpenAI image prompting](https://developers.openai.com/api/docs/guides/image-prompting): reference roles, separate changes/invariants, previous outputs as edit inputs.
- [World's Edge: Age of Empires is2D or3D](https://www.ageofempires.com/news/age-empires-definitive-edition-3d-2d-game/): 3D models rendered as2D images.
- [Krita animation manual](https://docs.krita.org/en/user_manual/animation.html): whole-frame raster animation, keyframes, in-betweens and onion skins. Krita execution/authoring is not claimed here.

No image calls, model downloads, new renders, runtime installs or production changes were performed for this review.
