# Finite building key API497

No registry/order/image was created by this worker. This API extends existing `prepareOrder` and durable runner; all legacy unit guards remain in their branches.

Trusted registry location: `docs/art/pipeline/building-production/[known BUILDINGS type]/identity.json`. Schema `rds-building-identity/v1`, kind `building`, buildingType, masterAuthority `original`, master `{path,sha256}`, descriptor `{path,sha256}`, layout `{family,pivot,render,contactShadow}`, assemblyLock `{source:{path,sha256},statement}`, jobs `[{id,path,sha256}]`, productionOrders `[orderId]`, excludedReferencePaths array. Source/descriptor/job pin paths use existing absolute pin convention. Descriptor is the actual original asset JSON with source SHA, kindbuilding and null direction. Layout must equal its family/pivot/render/shadow.

Job schema `rds-building-job/v1`: id, kindbuilding, buildingType, state, directionnull, frameCount4, originalMaster `{path,sha256}`, descriptorSHA, exactlayout, frames four `{frame,phase:frame/4,status:pending|selected|held,input?:{path,sha256}}`. New missing target must remain pending. Selected neighbors bind exact job/frame/phase/input; held/excluded references fail.

Order: id, jobKind `building-state`, kindbuilding, buildingType, state `construction|hit|death|attack`, directionnull, statusOPEN, job `{id,path,sha256}`, callLimit1/callsUsed0/correctionCap0/correctionsUsed0 for first root probe, four slots `{frame,phase,status:pending,kind:initial,template:building_key}`, existing enforcementv1 from495. Attack only applies to BUILDINGS with positive actual damage. Helpers support explicit finite budgets up to4+max2 corrections; root first-probe registration remains1/0 and does not reopen failed unit walk methods.

Values fields exactly: buildingType, state, direction string `none`, phase string `0` for F0, master originalSHA, assemblyLock exactstatement, invariants explicit whole-structure/state requirements. References first originalmaster pin, then optional selected exact-job neighbor pins. No fake D0, unit/mannequin borrowing, guide/held borrowing or silent original replacement.

`prepareOrder(orderId,slotIndex,'building_key',values,references,{taskId,expectedInputs})` loads trusted registry and task index, hashes inputs, validates lineage/prerequisites/accounting/owned slot. Runner `claim` receives existing request plus taskId/expectedInputs and forwards sixth context; no dispatch occurs. `prepareOrderWithRegistry` is isolated fixture API: validates binding/enforcement declaration but not trusted task index. Root production must use trusted prepareOrder/runner.

FrameCount4 is planning scope only. Returned prompt is not permission. Durable claim precedes an actually authorized built-in call; independent source review precedes selection. Runtime/compiler extension deliberately deferred. Four complete frames, state acceptance, runtime integration, owner and release must be separately established.

Descriptor family must equal the known buildingType directly or with one `building.` prefix, e.g. residence/building.residence. Rehashing a foreign fort descriptor and consistent layout/job cannot authorize a Residence order. Focused33/33 checks pass; original32-test output retained in tests-before-family-guard.txt.
