# 051 bounded production-readiness evidence

Read-only inspection on 9 October 2026, exact gpt-6.1-sol / low worker. No tests, art calls, deployment, restart, top-document changes or commits. Root owns live049/050 QA; their results are intentionally pending here.

## Existing public service

`systemctl --user show rach-doi-son-ha.service` returned active/running, MainPID3358, start09:26:54+07. `tailscale funnel status` reported enabled443 and8443, each proxying127.0.0.1:3000. Stable configured URL: https://kieu-hoang-quan-loq-15iax9.tail5247a0.ts.net . Local GET `/health` returned `{ok:true,rooms:0}`. This inspection did not claim a new public remote-client acceptance.

`deploy/rach-doi-son-ha.service` runs Node24.15.0 `server/index.js`, production environment, loopback3000,8rooms/32connections, Restart=on-failure. `server/index.js:35–56` serves `dist/`, offers health, validates same-host WebSocket origins. `deploy/README.md` describes machine-hosted Funnel; uptime depends on this computer and user session. `server/DEPLOY.md` and Dockerfile provide portable container/reverse-proxy deployment; active rooms are in memory and restart destroys them.

`dist/index.html` currently references `index-ClW3IlNb.js`; SHA256 ca8e6428603c0033ccd9926fdb69daa5d78cee28fef4259607946530fe02e08b. This exactly matches `docs/ACTION_TIMING_DEPLOYMENT_RECEIPT.json`, the7October action-timing public receipt. It is distinct from the043 candidate33da4dd6348b742f8f83bb241c4e01c892dba850668160368a1dadfff047e548. Thus current client source improvements are not bundled in production dist.

Backend caveat: disk `shared/sim.js` now hashes b4257d74b1684efdd7a8fc7d2fbc273494f9fb63304e217a6ab8693ba240470d, versus0613dad6…7318 in the historical deployment receipt. `shared/data.js` still matches ffc3f45a…81e1. The running process started today; health does not identify its loaded module hash. Do not infer a historical backend merely from old client dist. Next release must bind backend/client source together.

## Concrete existing coverage and remaining debt

| Scope | Actual file evidence | Next missing proof/work |
|---|---|---|
| Core defeat/rebuild | shared/sim.js:117–176; tests/sim.test.js:11–12 cover General death, surviving residence destruction, King-only replacement and duplicate reservation | Keep invariants; no core rewrite justified by current evidence |
| Logistics | shared/sim.js:208–232; tests/sim.test.js:13–18 cover finite rations/Granary, physical wagon conservation/delivery, wood/iron depot credit, transport | Later one ordinary UI supply-wagon/transport scenario tied to final candidate; no new carry-walk artwork per human instruction |
| Leadership | shared/data.js:32–51 defines12characters, abilities/passives and5tag synergies; shared/sim.js:11–16 and ability path; docs/leadership-source-hashes.json | Preserve originals; world-state eight-direction/action identity art remains missing, static portraits do not close this |
| Maps/AI | shared/data.js:56–59 two maps;044 actual Delta human victory;030/031 offline losses/menu both maps; root050 handles next Coast victory | Intake050 finite result, preserve failed045, avoid duplicate match |
| Multiplayer | server/index.js;028 earlier local both-map full lifecycle;048 diagnostics synchronization hold; root049 owns fix and fresh attempt | Intake049 complete latest candidate two-engine both-map lifecycle before promoting; external physical-device/WAN latency and dense performance remain open |
| Visuals | docs/VISUAL_PLACEHOLDERS.md releaseFAIL; docs/KNOWN_GAPS.md crowd stacking and terrain/roster debt; owner-motion-review-032/review.json narrow South gather acceptance | D0 opposite-contact source, then complete pilot; representative browser vertical slice before fanout, not repeated still audits |

Candidate additions absent from current dist include navigation016/040, boot portrait preload021, action/export017 and gathering018/019/026 presentation, selection/group043. 047 and049 change QA harnesses, not game balance. `client/raster-slice.js:12` preserves opt-in `?art=pilot`, `?art=walk`, `?art=work`; default remains development placeholders. Optional candidates cannot be silently labeled final APPROVED.

## Authorization versus acceptance

`docs/web.md:633–662` (§63) makes deployment part of the goal. §78 at1153 onward says “Do NOT wait until the entire game is complete before attempting browser deployment” and “Then deploy the prototype.” §79 requires clean-browser production-URL testing. `docs/master.md` §36 says continue automatically with the next highest-priority task. No blanket human-confirmation requirement for each development deployment was found in these clauses. §64 requires build/deploy/environment/rollback documentation; current deploy README lacks a concrete release rollback procedure.

AGENTS current finite QA orders explicitly prohibit public deployment within those orders. The present051 assignment explicitly forbids deployment and restart. Neither owner032 motion acceptance nor041 API authorization grants final visual/public completion approval. Root must apply the actual current human scope before a later deployment; do not invent an approval requirement from unresolved final-art gates. A clearly labeled development update and final release/completion are separate milestones.
