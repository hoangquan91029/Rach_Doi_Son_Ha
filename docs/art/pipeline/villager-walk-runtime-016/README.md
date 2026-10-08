# Real runtime walk check — eight-direction navigation

The cardinal-only navigation hold from runtime015 is resolved in local code. Shared authoritative navigation now searches eight directions with cardinal/diagonal distance costs and deterministic insertion ties. Both route planning and actual movement reject diagonals through blocked terrain/building side cells. AI, SP and online use the same implementation; no sprite-facing relabel or gameplay-speed adjustment.

Picking reuses the renderer’s exact family/state/direction and distance-phase sample, then tests the actual alpha silhouette. This includes the new80px villager hat rather than the old30px fallback box.

All78 tests pass, including navigation corner/dynamic-blocker coverage, both-map AI/naval/logistics, authority/reconnect/rematch and frame sampling. The temporary production build passes; deployeddist and running3000service are untouched.

Actual UI Chromium and Firefox at normalzoom1.08/DPR1 each loaded16 candidate assets, displayed all8D1 frames during ordinary movement, froze simulation/frame/distance on pause, drew matchingD1 idle after stop and selected the worker via its hat. Both report0 captured errors. The helper only reads diagnostics; no forceddirection, fakeunit or simulation mutation. Four initial harness failures are preserved: integer-goal endpoint assumptions and contextual resource commands were repaired by choosing a corridor valid for all four potential arrivals and using the actual arrived position.

Recorded full sessions contain the real walk around4.5–7seconds. Screenshots prove sampled appearance only; neither video capture nor technical tests alone proves continuous naturalness or world foot lock. The1.26worldunits/cycle distance remains provisional. Only one villager direction is authored; other directions/actions/units, owner/final art acceptance and final publicproduction validation remain open.

Independent review is in `independent-review/`: samples-only, coherent recognizable appearance, no new frame correction justified. Continuous perceived naturalness/seam/foot lock remain unverified because the reviewer could not open the recorded video. The new80px pilot is taller than nearby oldunits; bring other final assets into a declared consistent family/world scale rather than silently fitting or reverting this pilot.

Chromium recording: `chromium/page@d749c60e2842a73b3b59a919deeb37ec.webm`, walk4.452–6.952seconds. Firefox recording: `firefox/page@c3f704da7bfa30ba073b612e3b3e84f4.webm`, walk approximately4.62–7.12seconds. These are ordinary real SP game sessions, not synthetic controls.
