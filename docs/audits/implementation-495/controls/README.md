# G0 agent controls495

Purpose: extend existing preflight/finite runner with optional scoped mechanical gates. No image call, production art-ledger mutation, game source edit, build or deployment by this worker. `scripts/sprite-prompts.mjs` remains unchanged.

## Actual outputs and checks

Owned changes: `scripts/agent-preflight.mjs`, `scripts/sprite-order-run.mjs`, new `scripts/agent-task-contract.mjs`, `tests/agent-preflight.test.js`, new `tests/agent-task-contract.test.js`, this directory. Root owns common documents and task registration. Other workers' concurrent game/art changes are outside this assignment.

VERIFIED: `node --test tests/agent-task-contract.test.js tests/agent-preflight.test.js tests/sprite-order-run.test.js tests/sprite-order-run485.test.js tests/sprite-prompts.test.js` exits0,35/35. Actual output: `focused-tests.txt`. Negative cases include directory/slot/symlink overlap, path escapes, input drift, stale/missing snapshot, unowned slot/output, renamed closed method, unsupported failed parent, false qualification, held/stale/foreign prerequisite, settled-claim counter reset/token mismatch, false rerun/PASS/still/owner/public claims, unknown handles, missing claim handle binding, and repeated closure. All mutations in these tests target isolated temporary fixtures. Existing24 tests remain compatible; eleven new tests include the preflight and output-settlement integrations.

Initial explicit audit preflight succeeded at clean HEAD2187c0a with ledger41befce3 unchanged. Later refresh FAILED during concurrent root integration because new read-contract referenced missing `docs/COMPLETION_MATRIX.md`; original failure remains retained in `preflight-refresh-failure.json`. After root completed required docs, final refresh succeeded at HEAD2187c0a; `preflight.json` pins current reads including matrix `e10eb3b7dd1c289383a047027097bb4773218cd3b55550347eb5b9836079dd1c` and read-contract `3063b312cbde80b414c7718a17f308f53cab8e7714b944e49657cf62b160c093`. Current ledger hash is `48cdd19d3148b0d0838500dce65fa94bc47bf5970d636adbce1dcad873bb3f50`, unlocked with0 unresolved claims. Root intentionally updated nextDependencies only; its preservation receipt owns the historical-order byte comparison. This worker made no ledger mutation and does not claim the full ledger retained its old hash. No missing-read bypass. Hashes establish bytes, not understanding. No fullsuite/fullmatch rerun. Source review and `git diff --check` performed; root owns integrated review.

## Root registration API

One trusted root-owned file: `docs/audits/implementation-495/tasks.json`:

```json
{"schema":"rds-agent-tasks/v1","tasks":[{
 "schema":"rds-agent-task/v1","id":"unique-task","status":"ACTIVE",
 "purpose":"Concrete scoped work",
 "worker":{"id":"actual-worker-id","model":"gpt-6.1-sol","reasoningEffort":"low"},
 "outputs":["repository-relative-file-or-directory"],
 "slots":[{"orderId":"future-order-id","slotIndex":0}],
 "inputs":[{"path":"repository-relative-source","sha256":"64-lowercase-hex"}]
}]}
```

`CLOSED` contracts retain metadata but no longer exclude concurrent outputs/slots. Closing registration requires root's actual handle/claim inspection; no expiry is implemented. Root output declarations must name its exclusive files rather than an ancestor directory containing a worker's output. Tool cannot determine actor authenticity or enforce arbitrary filesystem writes.

Worker role may be omitted or `WORKER`; workers require exact `gpt-6.1-sol`/`low`. Root alone registers `worker:{role:"ROOT",id:"/root",model:null,reasoningEffort:null}` because root model/effort are not tool-reported. A different ID cannot claim ROOT role; model/effort must remain null. These fields are declarations, not proof of actor identity. Negative fixtures cover forged ROOT IDs, invented root model, `/root` presented as ordinary worker, unknown role and wrong worker model.

Exports: `validateTaskContracts(root,tasks)` validates ownership/model/shape; `validateTaskSnapshot(root,tasks,taskId,expectedInputs)` rehashes only registered scoped inputs; `validateTaskReceipt(root,receipt)` checks declared evidence relationships; `validateOwnedOutput(root,task,absoluteOutput)` checks output containment. Existing and nonexistent output ancestors resolve real symlinks. No registration write API is exposed: root edits the one index and validates it.

Optional preflight invocation:

```text
node scripts/agent-preflight.mjs --task audit --source scripts/agent-task-contract.mjs --task-id unique-task --inputs /absolute/scoped-inputs.json
```

The snapshot file contains the exact input-pin array. Programmatic `agentPreflight` accepts `taskId`/`expectedInputs`. Assignment-free existing invocations remain compatible and explicitly do not enforce ownership.

## Future guarded orders only

Root may register an optional field on a genuinely authorized future order:

```json
{"enforcement":{
 "version":1,"taskId":"unique-task",
 "baseline":{"callsUsed":0,"correctionsUsed":0},
 "method":{"family":"root-defined-control-family","parentOrderIds":[]},
 "prerequisites":[{"job":{"path":"relative-job.json","sha256":"64-hex"},
   "frame":0,"phase":0,"input":{"path":"relative-key.png","sha256":"64-hex"}}]
}}
```

`claim` additionally receives `taskId`/`expectedInputs`. It verifies task registration, scoped hashes, owned slot, method lineage, prerequisite job/selected frame/source and durable counter accounting under existing ledger lock. `settle` checks guarded output ownership while preserving consumed calls and held status. Source selection and approval remain separate.

Closed family cannot reopen by renamed order. Failed/closed parents in a new family require `method.differenceEvidence:{path,sha256}` pinning `{schema:"rds-method-difference/v1",family,decision:"MATERIALLY_DIFFERENT",reviewer,changedControl,parentOrderIds}`; reviewer must differ from registered producer. This is a declared independent assessment, not algorithmic proof of material difference. Parent list must match exactly.

Qualified family reuse after closure requires root-pinned `method.qualification:{path,sha256}` containing a task-bound receipt with VERIFIED independent motion and explicit owner approval. Custody closure alone does not qualify it. Only relevant parent/same-family qualification records are validated.

`baseline` is explicit migration accounting, not permission to reset history. New orders should start0/0; root must substantiate any nonzero migration. Existing orders without `enforcement` retain existing checks/counts; none are retrospectively described as guarded. A dishonest baseline or omitted semantic ancestry is outside mechanical detection and must be rejected at root registration.

## Receipt and safe closure

Receipt schema `rds-agent-receipt/v1`: `taskId`, `checks`, `handles`, and separate `technical`, `motion`, `runtime`, `owner`, `release` stages. Checks include actual command, absolute cwd, method, state, execution boolean, exitCode, observation and evidence pin array. Non-UNKNOWN checks need pinned evidence; VERIFIED cannot have nonzero exit. Each stage contains state and limitation; VERIFIED includes observation/evidence. Motion requires `method:CONTINUOUS_LOOP`, distinct reviewer/producer. Owner requires `decision:APPROVED` and `humanReply` binding. Release requires scopePUBLIC, URL/buildSHA/backendPin/rollbackPin. Pinned evidence paths are repository-relative.

`node scripts/sprite-order-run.mjs close /absolute/request.json` accepts `{expectedLedgerSHA,orderId,taskId,receipt}`. Only OPEN guarded order of ACTIVE registered task can close. Every durable claim must be settled and its claim token represented by CLOSED handle. Any UNRESOLVED handle blocks closure. INTENTIONALLY_RUNNING handles may describe preserved production. Closure sets CLOSED with receipt hash; it grants no approval/refund and does not inspect or kill OS/browser handles.

## Limitations and remaining integration

All checks above are mechanical custody/scope checks. They cannot authenticate test observation/human prose, eliminate hallucination, discover undeclared aliases of method semantics, prove comprehension, qualify tools or authorize image calls. Root registration, independent actual review and live-handle inspection remain mandatory. Receipt URL metadata does not prove WAN behavior. Stage fields do not replace actual evidence.

No existing runtime/compiler validators were replaced. No current production order was migrated or opened. Canonical code task ownership must be exercised through the optional preflight API; arbitrary writes outside this runner are not intercepted. Safe build isolation remains a project instruction, not newly implemented command interception. The default trusted task index currently uses this495 path and must be intentionally maintained/migrated by root when future task batches replace it.

Worker used no owned browser/server/tool call needing shutdown. Tests completed; no worker test process left running. Production deliberately untouched. Next dependency: root independent review, register mutually exclusive assignments in one index, validate scoped pins, then integrate docs/current queue without claiming new art/runtime/public approval.
