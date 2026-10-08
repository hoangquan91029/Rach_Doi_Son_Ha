# Villager walk runtime integration — navigation hold

`?art=walk` loads the corrected South/D1 illustrated walk and matching canonical idle through the existing raster API. Original14 assets, `?art=pilot` and default presentation remain available. Walk and idle share1254source/128runtime/89logical canvas and fixedpivot[654,1140]. The manifest remainsCANDIDATE.

New reusable `client/locomotion-phase.js` observes actual entity positions before sprite selection. Explicit locomotion metadata maps travelled distance to cycle phase; stationary/pause freezes, stop chooses idle, rewind/reuse/teleport reset. Assets without metadata retain existing timing. Distance1.26worldunits/cycle is provisional (2.1×0.6); no measured foot-lock claim.

Nine targeted timing/interpolation/locomotion tests pass. Producer reports packaging validation and temporary-output Vite build pass. Actual localhost Chromium loaded16 assets with0 failures, accepted UI movement, froze simulation on pause and accepted stop. The full South animation check FAILED: `shared/sim.js:path()` explores only four cardinal neighbors, so the real diagonal UI order follows dir0/2. `chromium/failure.json` preserves the original assertion failure; the subsequent receipt explicitly remainsLOCAL_GAME_NAVIGATION_HOLD with no8frame observation and no phasePauseVerified claim. Technical checks do not qualify this motion.

Next implement proper eight-direction navigation with terrain/building corner safety and deterministic costs/ties. Do not relabel South as a cardinal direction, modify facing artificially, or substitute a synthetic scene for actual gameplay. Then rerun this browser harness; only an actual8frame observation plus practical loop look can advance this pilot. No direction/unit fanout yet.

No simulation/server/productiondist or leadership/original artwork change in this checkpoint; no image call, deployment or service restart. Local Vite5173 was used for this check. Full game NOT COMPLETE.
