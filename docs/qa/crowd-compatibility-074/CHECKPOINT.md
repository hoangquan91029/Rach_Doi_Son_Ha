#074 compatibility gates prepared only

ExactSol6.1Low; scope thisdirectoryonly. Authoritative six240simulationsecondAIvictories and two240secondnavalsorties are tests/sim.test.js23/27–41. Rejection001 reportsall8failure;002 stoppedbeforethesechecks. Currenttests preserveexact seeddefaults, mapsdelta/coast, difficultieseasy/normal/hard, winner1/EnemyGeneraldefeated/livingAIgeneral. Navalfixture's durableenemyGeneral1e9 is existinglegitimateunitfixture, notbrowseracceptance: retains >=2embarked/landed, navalLandings>=1, physicalfoodTransported>0, ownGeneral>.8hp/nonnegativeeconomy. Nohistoricaltestedited.

Frozen current sim/navigation tests and sourcepins retained. run.mjs changes importURLs ONLY to configurable QA_SIM_PATH; data usesexactcurrentpinnedshareddata. QA_RUN_ID mustbenew; mkdirrefusesoverwrite. BaselineprepareSHA b4257d74b1684efdd7a8fc7d2fbc273494f9fb63304e217a6ab8693ba240470d; runner/wrapperssyntaxPASS. NoAI/candidate/fullmatch rununderthisorder.

Afterrootqualifies073admission/prerequisites, runserially oncepernewfiniteorder; stopfirstfailure:

```sh
QA_SIM_PATH=docs/qa/crowd-admission-073/sim-draft.js QA_GATE=navigation QA_RUN_ID=draft-navigation node docs/qa/crowd-compatibility-074/run.mjs
QA_SIM_PATH=docs/qa/crowd-admission-073/sim-draft.js QA_GATE=combat QA_RUN_ID=draft-combat node docs/qa/crowd-compatibility-074/run.mjs
QA_SIM_PATH=docs/qa/crowd-admission-073/sim-draft.js QA_GATE=ai QA_RUN_ID=draft-ai node docs/qa/crowd-compatibility-074/run.mjs
QA_SIM_PATH=docs/qa/crowd-admission-073/sim-draft.js QA_GATE=naval QA_RUN_ID=draft-naval node docs/qa/crowd-compatibility-074/run.mjs
QA_SIM_PATH=docs/qa/crowd-admission-073/sim-draft.js QA_GATE=all QA_RUN_ID=draft-fullsimnav node docs/qa/crowd-compatibility-074/run.mjs
```

Pathsareproposedrootassigneddraftpath, confirmactual073pathbeforeexecuting. Nodepattern filtersoriginaltestnames; tests/seeds/240simulationsecondcaps/assertionsunchanged. Gateall coversallcurrent sim+navigation, notentirenpmtest; live npmtest is node --test tests/*.test.js. Rootintegration laterrequiresall relevanttests, view/privacy, determinism, opposingford900ticks, spatialhash/fairbudget/performance gates; theseareunexecutedhere. Noautomaticretry/fanout or weakenedwinnerguard.

DenseordinaryUIrecipe forlaterseparateorder: frozen scripts/browser-dense-baseline.mjs normalonline2clients1440×900/deviceScale1, create/joinDelta ordinaryUI, discoveredresourcegather/traininfantry usingfiniteeconomy,22army each, F2/rally29/35, normalzoomcenter32/24, viewportmilitary>=40 screenshot thenordinaryopposingattackmove and30secondsbattle. Existing max720000ms cap/default650000 retained. NumericRAF/read-onlyfiltereddiagnostics only; no entity/resource/command injection. Baseharnessart=pilot ishistorical; laterreviewedwrapper may choosework opt-in and061guardedacquisition/preload, retainingeconomy/count/cap/ordinaryUI assertions. Do NOT execute frozen relocatedsource directlyuntil relativepaths/output andownedserverrecipe reviewed.

Requiredlater actualcapture: pinexactcandidatebundle, ownedephemeralserver/browser lifecycle,17art12portraits/errorlist, normalzoomcamera and actualdense screenshot/continuousclip duringcombat; evaluate distinctvisible silhouettes/naturalmotion ratherthan projectedcounts. Stopifviewport40cannotbereachedwithinfinitecap ornormalUIguardfails. No artificialprojectionoffset/syntheticcrowd/playerstate-injection. SamehostUI doesnotproveexternaldevice/WAN/fullvisualacceptance.072fixtures unchanged; noactualsim/livehistoricaltest/art/service/deploy/topdocs/commit changes.
