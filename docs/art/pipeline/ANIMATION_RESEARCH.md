# Animation research — primary sources, 12 October 2026

Purpose: select a practical pure2D workflow for THIS repository, not copy another game's assets or assert unknown frame counts. No newly researched local generator has been installed or benchmarked. Supersedes the current-direction claims in PRIMARY_SOURCE_RESEARCH.md; that document remains history.

## Verified lessons and limits

| Primary source | Verified relevant lesson | What it does not establish |
|---|---|---|
|[Krita animation manual](https://docs.krita.org/en/user_manual/animation.html)|Raster frame animation, keys before in-betweens, onion-skin comparison and short rough animatics; frames consume memory|Not an AI identity guarantee, installed-tool proof or RTS frame budget|
|[Blizzard: behind StarCraft Remastered](https://news.blizzard.com/en-us/article/20726732/behind-the-scenes-of-starcraft-remastered)|Artists discuss recognizable silhouettes and recovery/reworking of existing art/tooling|No general8direction/frame-count rule or license to use their artwork|
|[AoEII DE update99311](https://www.ageofempires.com/news/age-of-empires-ii-definitive-edition-update-99311/)|Sprite .smx/.sld startup validation and handling corrupt/unreadable mods|No universal production workflow, frame/direction count or aesthetic approval|
|[Stronghold DE official press sheet](https://fireflyworlds.com/press/sheet.php?p=Stronghold+Definitive+Edition)|Official product/art reference for a remake preserving its visual identity|No verified per-action sprite counts or detailed motion pipeline from this sheet|
|[EA C&C Remastered source repository](https://github.com/electronicarts/CnC_Remastered_Collection)|Official source is available for game-specific technical investigation|This audit did not trace unit animation tables; no count or mirroring claim adopted|
|[Cossacks3 official site](https://www.cossacks3.com/)|Describes contemporary3D graphics|Not evidence for a pure2D sprite authoring method; older Cossacks production details UNKNOWN here|
|[TexturePacker settings](https://www.codeandweb.com/texturepacker/documentation/texture-settings)|Padding separates neighboring samples; documentation recommends at least2px for OpenGL bleeding avoidance|This project uses Canvas2D; the principle supports existingpadding2, not a claim that TexturePacker is installed|
|[ControlNet paper](https://arxiv.org/abs/2302.05543)|Spatial conditioning can use edges/pose/segmentation alongside text|Not exact limb geometry, cross-frame identity or local hardware feasibility guarantee|
|[IP-Adapter paper](https://arxiv.org/abs/2308.06721)|Image conditioning can combine with text and structural controls|Not proof of original-unit fidelity or animation coherence in this project|

All sources above were accessed during the audit. Papers were read at abstract/method-summary scope, not reproduced experimentally. No copied game art, unofficial frame table, guessed count or GPU benchmark is used. A failed earlier Krita render-animation URL is not a cited source. Source availability and product details can change; record the access date with future findings.

## Comparison and selected architecture

1. Independent AI frames from unrelated prompts: easy dispatch, weak continuity control; reject as default.
2. Canonical whole illustration + controlled keys + selected neighbor in-betweens: fits existing tools; preferred structure but pose reliability still unqualified.
3. Temporary original-derived whole2D pose guide / layers / mask, then finished illustration: makes constraints explicit; optional capability branch. A guide itself can be anatomically wrong or ignored.
4. Layered warp/cutout animation: useful to examine control concepts, but final warped/cutout pixels violate current project constraints and risk seams. Do not ship it.
5. Archetype-specific hybrid of permitted2D controls: humans, horses, wheels and ships need distinct contact plans; final atlas interface stays shared.

These tradeoffs are INFERRED, not measured success rates. Separate pose conditioning from appearance conditioning. The current built-in interface has no explicit seed/skeleton/mask parameter; textual guide adherence is not deterministic. Thus “better prompt” alone cannot be represented as solved temporal geometry.

## Local2D branch: bounded feasibility, not an installed pipeline

Observed: Python/Pillow/ffmpeg/jsonschema present; Krita/GIMP/Inkscape absent; torch/diffusers absent; nvidia-smi absent. PCI sees NVIDIA RTX2050 and IntelUHD. This does not establish usableCUDA, VRAM capacity, memory available to inference, licensing or generation speed.

Next capability task: verify actual driver/runtime/VRAM/storage, choose one legal2D authoring route, document exact versions/capabilities and isolate dependencies. Prefer a whole-clothed guide bound to original landmarks first; Krita can be considered for authored layers/masks, while ControlNet+image-conditioning is a research candidate only after feasibility. Do not install many frameworks or download model weights blindly.

If a distinct route is feasible, finite trial has two opposing contact slots plus at most one visible correction. Keep exact raw output/conditioning pins and measure identity/contact success at game size. A failure is useful evidence: hold it and stop that branch, not another equivalent prompt series. No3D, paidAPI key or changed unit identity. Installing a program alone does not give the agent a usable drawing/automation capability.

## Project-specific conclusion

Keep engine/runtime/atlas tooling. Fix the concrete order/reference gaps, make motion/projection separate from identity, qualify existing Villager then measure reuse on Infantry. Frame budgets come from this game's action contract and observed smoothness, not inferred commercial-game standards. Final body motion, foot contact and identity must be assessed on the actual moving unit.
