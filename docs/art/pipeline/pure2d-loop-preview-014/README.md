# Corrected eight-frame illustrated villager walk

Eight actual whole-character 2D source illustrations, source order and immutable pins in `atlas-job.json`. Frame F7 is the one South013 spacing correction; all other frames match loop012. Loop012 and its crossed F7 remain preserved.

`playback/actual-eight-frame-loop.png` is the actual eight-frame APNG:75ms per frame,600ms cycle, nominal80px. Runtime atlas cells are128px; one uniform full-canvas transform and pivot[654,1140] apply to every frame. Existing authored contact shadow is separate.

Real localhost Chromium playback saw all eight frames across three cycles with zero reported errors. Brief80px sheet review confirms the visible F7 calf crossing is removed. Latest human instruction favors natural smooth motion and minimal checking; no native detail audit or repeated contact polishing was performed. Screenshot sampling does not establish continuous naturalness or world foot lock. This candidate is ready for practical engine integration and movement/stop review; it is not a production-approved animation or a completed game.

Serve `playback/` with a local HTTP server and open `preview-v3.html`, or view the APNG directly. Existing helpers in `pure2d-atlas-adapter-009/` and `pure2d-loop-preview-012/` produced these files without source edits, per-frame fitting, cutout parts or3D.

Parent-owned preview was left running at http://127.0.0.1:8791/preview-v3.html (execsession48362); inspect its live state before starting another server. Prior loop012 server8790 was stopped. No production service was changed.
