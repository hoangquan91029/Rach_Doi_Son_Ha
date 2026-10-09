#201 visible hill partial-edge coverage

Owned client/terrain-props.js and ONLY drawHillGround section of client/raster-slice.js; tests/hill113.test.js/directly affected food-resource115 route expectations; this QA. No sim/data/resources/passability/camera/art source/build production/service/status/commit changes. Runtime source writes finished before202's independent building-eligibility edit. candidate-raster-slice.js captures201 alone; current canonical raster may include202. candidate.patch contains ONLY201 source/test change.

Aligned2×2 placement centers remain x+1/y+1 with unchanged authored scale/pivot. Each placement carries exact in-bounds currently visible hill cells, including partial blocks and odd final rows/columns. Renderer draws one clipping path comprising those projected tile diamonds before the existing rasterAt draw. Nonhill, hidden, explored-only and missing cells never enter clipping. No half-pixel expansion. Missing/not-ready asset returns no overlay and leaves procedural terrain fallback untouched. Original hill111/runtime hash preserved.

focused.tap7/7PASS: partial/odd/fog/immutability/readiness, full-block anchors; actual drawHillGround exact diamond coordinates,3-cell partial clip versus4-cell full clip; identical raster draw rectangle/scale/pivot; old route eligibility and no draws/clips on excluded routes. Only these focused tests run, no full matches/simulation suite.

    node --test tests/hill113.test.js tests/food-resource115.test.js

Literal isolated build: /tmp/hill-edges-201; absolute output /tmp/hill-edges-201-build; explicit /tmp/hill-edges-201/vite.config.js. stage-binding.json binds all frozen client/shared sources and all build files. JS index-DI0kgq1J.js SHA d79215a908c784e6e89b7c588b1a699e59e9158d70825336dacd161873544f33. This snapshot predates202's independent raster change and is not proof of the combined candidate.

ONE ordinary Chromium1280×800 Delta setup/select/right-click infantry move at normal zoom1.08. Read-only diagnostic at tick12 showed one newly visible edge hill tile22/20 and hillDraws1, asset failures0/page errors0. ordinary-hill-edge.png/scene.json retain actual scene. Root inspected it and accepted narrow corner/fog-edge coverage. This is not full-map composition, dense/browser performance or final public release acceptance. No camera/fog/state injection.

Separate synthetic actual-raster/native browser Canvas2D probe: odd3×1 map with hill/plain/hidden-hill, one placement,483 painted pixels,0 leaked beyond allowed projected diamond (pixel-edge antialias tolerance). This diagnostic is not ordinary-gameplay proof. scene.mjs records both scopes separately.

Public guard: all179 active dist file byte hashes unchanged before/after; health remained {ok:true,rooms:0}. No production build or restart. Browser/context and owned preview63001/dev10765 closed; both server handles exit130 after Ctrl-C. Finite package complete, no more source edits/tests/scenes.
