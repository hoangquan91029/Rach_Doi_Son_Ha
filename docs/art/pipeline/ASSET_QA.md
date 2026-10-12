# Asset QA — enough evidence, no repeated micro-audits

One contact sheet, one10–15s continuous gameplay-size loop, one relevantactualscene. Eight-direction actionbank uses eight synchronizedcells; absent directions visiblymissing. Humanreview is required for visible motion; agent review may record it only if actually able to watch. Samplingstills is SAMPLES_ONLY, never continuousPASS.

| Gate | Mechanical check | Required observation / limit |
|---|---|---|
|Identity|master/viewhash, excludedsourceguard, body/equipment locks|Same person/vehicle atgameplay size|
|Source|existence, decodedPNG/RGBA/alpha, raw+RGBAhash, stablecanvas|Missingbodypart/croppedgear/changedcharacter block|
|Sequence|frames/phase/durations, duplicate detection, explicitlooppolicy|Footalternation, coherenttool/body, seam andrhythm|
|Layout|fixedpivot/family, bboxdiagnostic, atlasbounds/padding, memory|No body/scale wobble or visibleclipping; bboxvariance alone notfailure|
|Runtime|actualaction/direction/tick/distance selection, PauseResume/Stop|Contact during travel, sameidleidentity, event/preemption/death|
|Release|exactsource/build/rollback/browser loading|Only scopedpublicscene is claimed; no localhost→WAN inference|

Block visible identity change, wrong supportphase, torso/weapon jump, added/missinglimb, clipping, obvious seam or sliding. Minor folds/pixels do not block. Do not perform repeated nativeanatomy scoring or extra fullmatches forartchanges. A named frame or prompt instruction is not proof of its pose.

Commands actually available: `node scripts/agent-preflight.mjs --task art --source scripts/sprite-prompts.mjs`; `python3 scripts/validate-animation-record.py /absolute/record.json --root /absolute/repo`. Existing compiler/preview/coverage/order tools retain their own CLIs; inspect beforeuse. Evidence envelope checker only validates declared candidate metadata/custody; it cannot grant production approval.

The release adapter for the new evidence envelope is still PROPOSED. Newvalidator production requests failclosed until its trusted qualification/stride adapter exists. Existing runtime/compiler validators remain in force. This is not evidence that existing historicalapprovedart was revoked.

## Recording a result

State sourceavailability, technical, motion, runtime, owner, release separately. Include exactartifacthashes, scene, browser/version ifobserved, method and limitations. A reviewer differentfromproducer records whether theywatchedtheloop. Owneracknowledgment referencesactualhumanreply and shownartifact, never guessedacceptance.

Automatedapproved-status checks are mechanical references, not authenticity verification of arbitrary prose. Keep uncertainty explicit; do not create evidence merely to satisfyfields. Fullunitcompletion needs applicableaction×8directions integrated, not idlefallback. Keep failedtrial receipts unchanged.

Provenance seed format `rds-provenance-seed/v1` records source/output pins, decoded hash, referenceAssetIds, actual known tool/model/prompt/pose/time, sourceState and separate validation limits. It indexes only3real retained infantry sources in this audit; no inference about missing legacy metadata. `audit-488/infantry479-candidate.record.json` is a real existing clip wrapped as UNREVIEWED for this new validator, not a fabricated fixture or new approval.
