# Gameplay and release audit — 2026-10-09

Read-only source audit at HEAD `77c0ae1`; only this report is authored. Scope: master gameplay sections 3–13,16–29 and `docs/SECTION_81.md`. No runtime edits, image calls, deployments, full matches, quota polling or API access. Exact Sol6.1 Low routing applies. Current AGENTS, NEXT_STEPS and pure2D review priority were read; obsolete historical routing/quota clauses are not applied. Existing receipts were inspected, not rerun or upgraded. No general security scan was performed.

## Assessment

This is an implemented playable development game, with unusually substantial narrow public browser evidence. It is not a completed section81 release. The main remaining gameplay work should close confirmed correctness issues and explicit contract/evidence gaps, rather than rebuild already working economy, networking or naval systems. Final art/map/performance/device acceptance remains separate.

Source evidence below uses repository-relative `file:line` references. Implementation means present code; tests mean existing contracts inspected, not a fresh whole-suite run; browser evidence means the named receipt's exact scope/build only. Latest NEXT_STEPS top entry is145/146, while files also contain later camp148/149 work: the parent audit must reconcile current pins rather than assume the top narrative is the latest public state.

## Requirement matrix

| Requirement | Actual implementation | Existing verification | Remaining acceptance/work |
|---|---|---|---|
| King + General choice, General defeat | `shared/data.js:32`, `shared/sim.js:53`, `shared/sim.js:223`; UI choice `client/main.js:24`, leader status:62 | `tests/sim.test.js:11,20`; public089 ordinary combat victory both maps | Core rule supported. Broad character behavior matrix still incomplete; full illustrated roster separate. |
| One Main Residence; King-only replacement; reservation; healing | `shared/sim.js:193–199`, `shared/sim.js:221`, `shared/sim.js:286`; data `shared/data.js:21` | sim tests12,13,24,49,52; server repair/cancel test67 | No duplicate exploit observed in reviewed code: authoritative synchronous command reserves living construction immediately. Add actual UI destruction→replacement/resume/cancel only if not already in bound acceptance evidence; no reason to redo normal victories. |
| All required building/unit production classes | `shared/data.js:5–29`, production validation `shared/sim.js:165–169`, queue/spawn:284–285 | sim19, naval17/18/43; individual public122/129/142/145 and newer149 receipts | Gameplay roster exists including transport/warship, walls/gates. Full construction/combat/death visuals absent; camp latest pins need reconciliation. |
| Wood/iron strategic delivery, real food inventory | `shared/sim.js:50,152–153,258–267` | sim15,57;120 iron both-map actual+137/142 iron episode/20 deposit | Strategic wood/iron transfer exists. Food node and food character are different assets; food101/106 character remains local/pending motion approval. |
| Finite rations, starvation, Granary, Depot, Wagon | data consumption/capacity; `shared/sim.js:255–276,289–294` | sim13/14/57/66;053 actual load/travel/unload conservation analysis;132 actual HUD | Confirmed passenger starvation exception below. Explicit army low-food alert missing. No evidence of a mandatory full physical recruitment-food chain; see policy decision below. |
| Naval embark/travel/unload; transport destruction | `shared/sim.js:201–204,220,268–276,307–338` | sim17/18/27/43;062 actual Coast naval core analysis | Core mechanics supported.062 is narrow analyzed PASS; original harness remains HOLD. Broad naval battle/long starvation acceptance still open. |
| Distinctive 12 historical identities and tag synergies | data32–51; modifiers `shared/sim.js:11–16`, effects:206–209,95/96/244–251/283–295 | sim20 distinct kinds/terrain/cooldown;49 fortification | Research-inspired interpretations exist; `docs/historical-dossier.md` is source, not proof every promised mechanic executes correctly. Need per-ability mechanical tests; weaknesses sometimes descriptive only. |
| Fog, terrain, deterministic combat | `shared/sim.js:67–96,147–151,225–251,389–395`; data53–59 | sim16/17/72/80–85; navigation/crowd tests | Confirmed secondary splash armor error below. Placement terrain footprint policy unresolved; map final composition/visible crowd readability open. |
| AI economy, army, food, commander protection, naval | `shared/sim.js:339–380`; same human command/cost checks | sim21,23 six map/difficulty victories,27 two naval/logistics scenarios; public090 Coast human easy victory | Not mere stub. Explicit scouting/defending supply lines/adaptive rebuilt barracks are limited; identify scenario need before implementing speculative tactical complexity. |
| Menu/setup/HUD/controls/results | `client/main.js:24–38,49–72,73–118`; selection-state helper |104 M/A,043 selection,145 F2 actual cohort/public lifecycle | Army low-food alert missing; modified training progress incorrect; actual individual artillery click overlap HOLD persists despite group workaround. |
| Authoritative exactly1v1 rooms, ready/reconnect/victory/rematch | `server/index.js:65–111`; online client40–46 | server tests; public089 both maps Chrome/Firefox reload/reconnect/ordinary victory/rematch/menu | Same physical host evidence. Separate device/WAN/long jitter/backlog evidence remains open. No durable match persistence through service restart. |
| Two maps and strategic routes | `shared/sim.js:18–41`; fixed mirrored geometry; data56–59 | sim17/72;089 both-map online;090 Coast offline AI human victory | Both playable mechanical maps exist. Final authored visual composition/bays/shoreline/repetition and strategic human acceptance are open. Seed stored but geometry is fixed; not a random-map promise. |
| Fixed tick, performance, no severe desync | data tick20; sim381–395; server105–111; client50–53 | deterministic hash test9; snapshot hydration server66; delayed065/067/069; narrow08630s45-visible battle | Server wall time can fall behind under heavy work (one step/interval, no elapsed catch-up). This is a load risk, not measured failure. Need current-build concurrent-room + desktop frame measurements, not count old benchmarks as final. |
| Public no-install browser release | section81; normal HTTPS receipts089/090 and later client artwork promotions | Existing public Chrome/Firefox with asset/lifecycle proofs | Complete only after final accepted art/maps and exact final build smoke + external device/performance gates. Audit did not fetch live public server or certify current bytes. |

## Findings

### G1 — Confirmed: boarding disables all starvation progression (priority1)

`shared/sim.js:290–292` subtracts passenger food and then returns for embarked units; starvation/morale/grace/HP attrition begins only at293. Thus a hungry passenger can stay aboard indefinitely without the normal penalty, including a General whose survival controls defeat. Transport loss still kills passengers correctly at220; that does not close this loophole.

Read-only in-memory diagnostic, 600 ordinary steps/30 simulation seconds, zero-food passenger vs zero-food land unit: passenger HP125, food0, `starving` absent, morale95; land spearman HP103.7375, food0, starving30. No live match or production state altered. Synthetic fixture isolates the branch; an ordinary embark contract should accompany a fix.

Fix: run shared physiology before the embark locomotion return; specify whether embarked units may receive finite ship/wagon/store food (current implementation has no ship-food cargo resupply). Preserve coordinate-follow/hidden rendering and transport death semantics. Acceptance: zero-food boarded unit and General accrue grace/attrition; fed passenger behavior and source inventory conservation; General starvation defeat authoritative; existing naval tests stay green.

### G2 — Confirmed: artillery splash ignores each secondary target's armor (priority1)

`shared/sim.js:249` calculates primary target armor/terrain/owner modifiers;251 applies `(damage-armor)*0.35` to every nearby secondary. A secondary's own armor, fortification, hill/ford status and river-defense effect never enter that calculation. Splash also reuses primary target damage bonuses; define explicitly whether building bonus should apply per victim.

Isolated read-only diagnostic at one 11-tick impact, disabling defender attacks to remove morale confounds: secondary firearm armor0 and secondary General armor4 both lose exactly21.279999999999973HP with identical primary target. Existing `tests/sim.test.js:85` checks timing/secondary HP decrease, not per-victim mitigation.

Fix: shared per-target damage/mitigation calculation, with documented splash scale ordering. Acceptance: same secondary suffers same hit independent of primary armor (given fixed splash policy); differing victim armor/terrain effects matter; mixed unit/building bonus policy and no pre-impact damage tested. Do not change range/cooldown/base stats merely to compensate.

### G3 — Confirmed missing required warning: army low on food (priority2)

Master section25 explicitly requests `ARMY LOW ON FOOD`. Current events come from `event` in `shared/sim.js:49`, damage215–223, gathering265, construction283 and abilities209; starvation293 never emits it. `client/main.js:58` shows selected unit rations and60 forwards events, but there is no army aggregate warning. A player can discover starvation only by selecting units or observing damage.

Add a visible own-unit ration warning with data-driven threshold, debounce/hysteresis and reasonable group aggregation. Acceptance: one meaningful low-food warning; recovery clears it; repeated ticks do not spam; enemy cargo/private information remains hidden; offline pause freezes its simulation condition.

### G4 — Confirmed UI calculation mismatch: training progress uses unmodified duration (priority2)

`shared/sim.js:168` stores `remaining = trainTime * modifiers.train`; `client/main.js:58` divides by raw `UNITS[q.unit].trainTime`. With Lê Thánh Tông's0.82 multiplier and Organized Levy0.9 (`shared/data.js:38,48`), a just-queued unit displays roughly26% completed before work. This also obscures ability acceleration.

Store authoritative total duration on queue entry or derive it from the exact binding (prefer total field to avoid hidden modifier reconstruction). Acceptance:0% on enqueue for default/modified leaders,100% only at completion, pauses frozen, mobilization speeds progression naturally, compact snapshots preserved. A tiny pure HUD helper test is sufficient; no full match needed.

### G5 — Confirmed architectural simplification, design decision required: recruitment food can cross the map instantly

`shared/sim.js:152–153` counts all completed friendly stores and drains closest then distant stores regardless of path/range. A frontline Barracks can consume remote Granary food instantly for training. Soldiers then start with full `foodMax` (`shared/sim.js:45`). Meanwhile field ration replenishment correctly uses finite nearby stores/wagons.

This is not labeled an exploit or unconditional violation: master distinguishes strategic recruitment cost from frontline replenishment only implicitly. It matters for the promised supply-denial game because reinforcement production can bypass physically cut routes. Record the rule explicitly before changing it: global recruitment cost retained as an intentional abstraction, or local food requirement/reservation with wagon delivery. If localized, handle queued costs/cancel/destroy/spawn-stalled refunds and AI logistics first; avoid accidental resource creation or rebalancing.

### G6 — Confirmed behavior, policy unresolved: construction validates only center terrain

`shared/sim.js:154–156` tests center bounds/terrain/ford then entity footprint collisions. Movement blockers use rectangular radius+0.15 at70. Diagnostic: legal Granary centered21.5/20.5, radius0.75, adjacent mountain cell22/20 is accepted, though its footprint overlaps that cell. This may be deliberate cell-center building policy, so it is a contract gap rather than confirmed bug. Same question affects shoreline structures and map-edge footprints.

Document ground occupation vs illustration overlap. If full footprint must be legal, check covered cells/bounds while preserving coastal shipyard access/spawn and friendly gates. Tests should use actual blocked ground footprint, not a sprite's decorative overhang. Do not infer a fix from this synthetic reproduction alone.

### G7 — Release evidence gap: character abilities are distinct data, incompletely exercised mechanics

Tests20 checks twelve unique kinds, cooldown and river gating. It does not prove each advertised behavior: inspection gathering/repair, fiscal wood/iron bonus, concentration artillery cooldown, deception visibility, shock order commitment, network range/wagon movement, restore construction/heal or synergy stacking. Many behaviors visibly exist in source; absence of tests is not absence of implementation. Some advertised weaknesses are explanatory text rather than separate mechanics (Minh Mạng unrest, frontier integration, etc.). Dossier concepts are design suggestions, not permission to add court/trade systems unboundedly.

Create a12-row effect contract table from current approved descriptions, mark existing code vs deliberate abstraction, then small mechanics tests. Include chosen-same-character King/General stacking policy: selection allows it and modifiers multiply both passives (`shared/sim.js:11–16,53`; UI24/30), but master does not forbid it. Do not silently disallow an existing player choice without a balance decision.

## Evidence boundaries

- 053 original run remains HOLD for private modifier lookup; separate analysis proves finite physical delivery/conservation with residual≈−1.4e−11.062 original HOLD compares unload with requested rather than actual ship; separate analysis proves actual unload radius2.9534 and real sea travel. Preserve both originals; do not rerun merely to erase them.
- 089 public both-map1v1 has ordinary combat winners571/587, rematch/newmatch/menus and reconnect.090 public Firefox Coast easy human victory4454/offline-after-load/result/menu. These are same-host, pre-current-art full matches; client-only artwork changes do not demand repeating all unchanged simulation scenarios.
- Server uses per-seat filtered `view`/`snapshotView` (`server/index.js:15–20`, `shared/sim.js:389–393`). Opponent fog/cargo/resources make two seats' view JSON intentionally unequal. `hashState` at395 hashes a global state object for reproducibility; `server/benchmark-network.js:18–23` compares pre/post serialization on that global server state. Do not compare seat-filtered hashes as a global desync check or expose the global state hash as a reason to expose fog data. No uniquely named web57 source artifact was located; no verdict is invented for it.
- Save-game persistence is not present: server rooms are a Map (`server/index.js:35`) and client sessionStorage saves reconnect token/name, not simulation. Restart loses matches. Section81 requires reconnect, not durable restart-save; preserve this limitation in operations docs, rather than treating a save system as mandatory new scope.

## Ordered work packages

| Package | Dependency | Concrete output and acceptance | Scope guard |
|---|---|---|---|
| GP1 Physiology correction | G1 policy for aboard resupply | Narrow shared-sim patch + passenger/grace/General defeat/conservation contracts; existing naval tests; one finite ordinary embark/30s-hunger scenario if UI evidence needed | No art, balance reduction, full matches or deployment before review |
| GP2 Per-victim combat damage | Define splash bonus/scale order | One shared mitigation function, mixed armor/terrain/building fixtures, timing contracts; compare deterministic identical seed/command outcomes | Preserve cooldown/range/authoritative impact and original receipts |
| GP3 Player supply warning + queue progress | GP1 physiology settled; queue total field snapshot design | Own visible army warning and correct progress helper; bounded pause/recovery/enqueue UI check | No private state reconstruction; no repeated production/victory loops |
| GP4 Logistics/leadership rule closure | G5, same-choice stacking, footprint policy decisions | Brief explicit rule ledger and12 ability contract rows; targeted mechanics tests for current promises | Optional political/trade/advanced doctrine remains future scope, not blockers |
| GP5 AI regression and targeted intelligence | GP1/GP2/GP4 | Existing six AI/two naval contracts first; then one failed scenario at a time for low-food retreat/rebuilt infrastructure/supply defense | No cheats, weaker guards, omniscient enemy lookup, or broad AI rewrite |
| GP6 Final mechanics release acceptance | Accepted art/map candidate + corrected sim frozen | Exact source/build binding; current-browser render/step/network p50/p95/p99 at20/50/100/200 total units and concurrent active rooms; prolonged match; one separate-device public lifecycle | Profile before rewrite; application delay is not WAN;500 only if practical |
| GP7 Section81 closure | GP1–6 + visual owner's final acceptance | Reconcile ledger to exact accepted final build; normal public clean-browser offlineAI+online lifecycle, resource/general/residence/logistics coverage where missing | Reuse still-valid receipts, retain all HOLDs, no blanket 'all passed' from test count |

Independent artwork can continue under current pure2D gates while GP1–4 proceed. Final art/map acceptance, external device/WAN evidence and performance cannot be closed by this read-only audit. Required completion statement remains **INCOMPLETE**.

## Minimal reproduction record for G1

The diagnostic compares **different starting types**, not equal HP controls: passenger infantry starts125HP; land spearman starts105HP. The claim is absence vs presence of starvation progression, not an absolute cross-type damage comparison. Land HP loss is1.2625 over30s; passenger loss is0. This is the exact isolated diagnostic, runnable from repository root without writing files or contacting production:

```js
// node --input-type=module
import {createMatch,step} from './shared/sim.js';
const s=createMatch(); s.aiPlayer=null;
const u=s.entities.find(e=>e.owner===0&&e.type==='infantry');
const v=s.entities.find(e=>e.owner===0&&e.type==='spearman');
const ship={...u,id:999,type:'transport',x:20.5,y:42.5,
  cargo:{food:0,wood:0,iron:0,units:[u.id]},order:{type:'hold'},food:65,foodMax:65};
s.entities.push(ship); u.embarked=999; u.food=0;
v.x=25.5; v.y=3.5; v.food=0; v.order={type:'hold'};
for(let i=0;i<600;i++)step(s);
console.log({passenger:{hp:u.hp,food:u.food,starving:u.starving??null,morale:u.morale},
  land:{hp:v.hp,food:v.food,starving:v.starving,morale:v.morale}});
```

Observed output: passenger `{hp:125,food:0,starving:null,morale:95}`; land `{hp:103.73749999999971,food:0,starving:30.00000000000029,morale:79.83587499999616}`. This synthetic fixture proves the branch defect; it does not replace an ordinary embark acceptance contract or a full naval match. No new diagnostic was run during the plan consistency review.
