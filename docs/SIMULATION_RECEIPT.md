# Simulation acceptance receipt — 2026-10-07

Status: implemented and tested simulation candidate; **not final project completion**. This receipt covers local Node simulation/server tests and source inspection. Production browser play, public HTTPS hosting, visual acceptance and long-term multiplayer acceptance remain separate gates owned by the parent audit.

## Exact audited sources

| File | SHA-256 |
| --- | --- |
| `shared/data.js` | `6196a5e9044e016e2ae13c92ad7d4c663ba507f23764da500a4aea95ec998e36` |
| `shared/sim.js` | `f0af3ecb7627ea784e0f46397b7757f400cdf02d57e833ed4359c03f8147b4d6` |
| `tests/sim.test.js` | `0a615f8d07285fbedcc79fc6990ff86f5c048e6dd990082877f3a2017463f12f` |
| `tests/server.test.js` | `bdb0e44ed513c6d8e80f0808b942d9bd903f4d0e4e352d88a8b6b3e421125656` |

The initial combined suite had 42 tests. A server Firefox compression regression increased that to 43. During this acceptance audit the parent explicitly lifted the production freeze for a narrow coast crossing repair: add ford tiles at x=30, y=7–9 so the central crossing spans x=30–33 symmetrically. Two map reflection regressions were added. The final audited run of `node --test tests/*.test.js` passed **45/45**, comprising 33 simulation tests and 12 server tests, with no skipped tests. No unrelated shared rules or map geometry changed during this final audit.

## What the automated tests establish

| Area | Actual exercised behavior |
| --- | --- |
| Simulation clock and reproducibility | 20 Hz fixed tick; identical seed, commands and 60-second AI scenario produce identical full state hashes. Online clients consume authoritative snapshots rather than running competing lockstep worlds. |
| Command authority | Unknown commands, invalid coordinates, prototype-name building keys and enemy unit ownership are rejected without resource spending. Queue costs and population reservations are authoritative. Kings and Generals cannot be trained as ordinary units. |
| Victory | Actual attacks kill a General, immediately select a winner and freeze subsequent progression. An embarked General dies when combat destroys its transport, causing defeat. |
| Main Residence | Existing or reserved Residence prevents another. Only King can replace it after destruction. A stopped build can be resumed; cancellation releases reservation with bounded refund. Repeated cancellation cannot create wood or iron. Construction footprints cannot trap units. Residence healing is exercised. Some lifecycle fixtures directly destroy the first Residence to isolate rebuilding; these are not substitutes for a complete production siege. |
| Economy | Villagers gather and deliver resources. Remote-depot wood and iron credit the strategic stockpile. AI earns resources and produces workers and armies without resource cheats. |
| Food | Consumption, low supply, starvation and delayed attrition are exercised. Stocked and empty Granaries behave differently. Wagon load, travel, unload and automatic nearby resupply transfer finite cargo. Conservation fixtures verify that depleted Granaries and Wagons cannot create ration reserves. |
| Fog | Unseen enemy General and private stockpiles are absent from player views; unseen attack targets are rejected. Private enemy orders are omitted. Enemy death playback remains visible where fog permits. Unseen resource quantities are remembered from last observation. |
| Terrain and navigation | Both maps allow cross-map land movement while preventing land travel on deep sea and naval travel across land. Every terrain tile and resource opportunity has a reflected counterpart after the narrow coast repair. |
| Leadership | Twelve data-driven characters have distinct ability kinds. Cooldown, terrain gating, tag synergy and completed fortification HP modifier are exercised. This is not exhaustive effect-by-effect balance validation of every ability. |
| AI outcomes | AI completes ordinary combat victories against an idle human on both maps at easy, normal and hard difficulties; AI General remains alive. |
| AI naval/logistics | Cost-paid AI economy builds a coastal Shipyard, trains a Transport, musters ordinary raiders, embarks them, sails to the opposing coast, unloads and sends them against supply nodes. Tests observe actual passengers and actual landings; King and General are excluded. Physical frontline wagon delivery is positive. |
| Server integration | Exactly two seats, readiness, ownership, malformed/rate/size/origin rejection, disconnect pause/timeouts, token reconnect rotation, consensual rematch, authoritative combat victory, compact snapshots, repair/cancel ownership, room expiry, health/static serving and Firefox compression negotiation are tested locally. |

These tests do not establish zero bugs, competitive balance, final visual quality, real-world latency behavior, or a completed match through the public production UI.

## Complete AI loss and human win scenarios

The default ruler/commander pairing in these scenarios is Trần Nhân Tông + Trần Hưng Đạo. The following AI victories use normal starting health, positions, stockpiles and rules. The human is idle; no General-health fixture is used.

| Map | Easy AI wins at | Normal AI wins at | Hard AI wins at |
| --- | --- | --- | --- |
| Delta | 169.55 s | 150.00 s | 158.30 s |
| Coast | 164.45 s | 152.25 s | 152.80 s |

The timings are observations from the audited development simulation. Difficulty changes decision cadence and attack timing, not inflated unit damage. Hard is not guaranteed to win faster than normal; naval allocation and pathing influence the result. This needs human balance testing.

A separate scripted **human victory** strategy uses only public commands and ordinary costs, with no health/position/entity/resource fixtures:

1. Assign six starting villagers: two wood, two food, two iron, using each worker's closest initially discovered resource patch of the selected type.
2. Queue eight Firearm infantry in the starting Barracks. Their total cost is 280 wood, 360 food and 240 iron. Starting strategic stockpiles are 550 wood, 810 stored food and 260 iron. The queue limit is eight.
3. Leave King and General near the Main Residence. Starting army is three Infantry plus one Spearman.
4. At 40 seconds, send ordinary soldiers and available Firearm infantry by Attack Move toward the opposing starting base, and send newly produced idle soldiers as reinforcements every two seconds.
5. Every five seconds, add another Firearm infantry if the production queue has fewer than three orders and authoritative resource spending permits it. Move the starting Wagon toward the army's rear at approximately (45.5, 26.5).

| Map | Easy: human wins at | Normal: human wins at | Hard: human wins at |
| --- | --- | --- | --- |
| Delta | 117.50 s | 119.35 s | 118.15 s |
| Coast | 138.40 s | 114.70 s | 111.35 s |

All six outcomes were enemy General combat deaths; human General remained at 360 HP and strategic stockpiles stayed nonnegative. Additional easy launches at 50/60 seconds also won: delta 135.35/144.10 seconds, coast 115.80/116.80 seconds. These are scripted simulation matches, **not browser/UI victories**. Earlier one-hit General fixtures establish terminal-state mechanics only and are not counted as ordinary victories here.

## Physical food and measured shortage timing

At match start each side has 430 food in Residence, 260 in Granary and 120 in Depot: 810 spendable stored food. The starting Wagon carries another 100; wagon cargo is excluded from strategic spendable food until unloaded into a store. Units also start with ration reserves. Food resource nodes are finite and villagers physically deliver gathered cargo.

`player.resources.food` is the sum of completed, living friendly stores' `cargo.food`, not an independent replenishing balance. Training deducts food from real stores. Granary/residence/wagon ration transfer deducts actual source inventory; no infinite food aura exists. Wood and iron deliveries to remote Depots intentionally credit the strategic pool. Fiscal bonus delivery creates its declared economic multiplier; it is an ability, not an accidental inventory duplication.

Default isolated Infantry has a 40-point reserve and consumes `0.16 × 0.90 × 0.92 = 0.13248` per second under the default leadership pairing. With no resupply and no combat:

| Observed state | Time |
| --- | --- |
| Below 25% rations / low supply | 226.45 s |
| Empty reserve / starving | 301.95 s |
| First delayed HP attrition | 326.90 s |

Low supply reduces movement and combat efficiency. Starvation reduces morale, speed and damage; HP attrition begins after the configured 25-second grace period. A short two-minute match does not strongly exercise food denial. This is a measured balance limitation, not a reason to claim logistics final. Consumption was deliberately left unchanged pending human playtests.

Food transfer itself is conserved in tests after accounting for consumption. This should not be read as a proof of whole-world food mass conservation through production: training creates a unit with its configured initial ration reserve while charging the configured food cost, and those two numbers need not match. Production also spends side-wide stored food rather than requiring explicit transport of its recruitment cost to each production building. Existing armies still require local finite resupply. Spatial recruitment-food rules and long naval crew supply remain balance/design review items.

## Actual naval AI observations

For these longer observations only, the enemy General's HP/maxHP are set to 1 billion so the match does not end before inspecting ships. AI units, buildings, resources, paths and passengers are otherwise produced by ordinary validated commands. This fixture is expressly **not a normal completed-match victory**.

| Map | First observed embark | First observed enemy-coast landing | Completed landings by 240 s | Actual wagon food delivered by 240 s |
| --- | --- | --- | --- | --- |
| Delta | 76.25 s | 101.25 s | 1 | 157.89 |
| Coast | 78.10 s | 103.50 s | 1 | 239.28 |

The Transport crosses the connected southern sea from its home coastal muster to the enemy coastal landing. Raiders then leave the beach and attack discovered supply nodes or their expected region. The state machine supports returning and repeated sorties. Earlier 650-second development diagnostics observed four landings on each map; the current exact-source recheck above is bounded to 240 seconds and confirms one complete route per map. Leaders are never selected as AI raid passengers.

The naval AI is basic: it uses a fixed southern coastline route, does not comprehensively evaluate enemy fleets or alternative landing risk, and has no dedicated coastal Granary construction/resupply policy for prolonged ship crew starvation. Those remain gameplay acceptance concerns.

## Map topology acceptance

Both maps are 64×48, with two mirrored spawn/resource opportunities and no extra player slots. A four-neighbor flood-fill over terrain-only navigation found one connected land component per map. This excludes dynamic buildings, which can intentionally block routes.

| Terrain | Delta tiles | Coast tiles after repair |
| --- | --- | --- |
| Plain | 2038 | 1928 |
| Forest | 284 | 308 |
| Hill | 48 | 30 |
| Mountain | 30 | 102 |
| River | 124 | 162 |
| Ford | 36 | 30 |
| Sea | 512 | 512 |
| Traversable land component | 2406 | 2296 |

Delta: navigable central river joins the southern sea in one 672-tile water component. Three separate ford bands at y=9–11, 22–24 and 34–36 give three attack/supply crossing routes. Forest banks enable concealment; hills overlook approaches; mountains are present primarily near outer northern corners rather than controlling the main delta routes.

Coast: central mountain barrier leaves passes at y=18–21 and y=29–32, plus northern/southern bypasses. Northern river has three crossing areas and its own 192-tile water component. Southern sea is a separate 512-tile component and supports tested coastal transport routes. The northern river does **not** connect to the southern sea, so ships launched on one cannot navigate to the other. Separate shipyards can serve each basin.

Forests lower detection and slow cavalry; hills increase vision/range/armor and slow movement; mountains block land movement; ford crossings slow units and reduce armor. Forest concealment, multiple passes/crossings and offset resource expansions create ambush and supply-line opportunities. Both maps contain every required terrain category and tested alternatives. Their geometry remains simple, with a straight southern shoreline and no developed bay/tide/bridge system. Topological correctness does not establish the user's requirement for **two finished, playtested maps**.

## Remaining acceptance work and limits

- Complete full production browser human victories/losses, 1v1 victory, reconnect and rematch through actual UI; simulation/server tests are supporting evidence only.
- Conduct two-player and human-vs-AI balance playtests, especially supply denial lasting beyond five minutes, artillery concentration, cavalry raids, General retreat and shoreline logistics.
- Validate every character ability's actual effect and counterplay, not just twelve distinct identifiers and selected ability tests. Political/diplomatic/territorial-integration systems from the larger dossier are not implemented; present abilities are tactical/economic gameplay interpretations.
- Validate maps visually and strategically before calling them finished. The corrected center crossing now has terrain/resource reflection tests.
- Unit movement allows troop overlap, uses grid BFS and a simple multi-selection offset rather than robust formation collision. Unreachable movement orders approach their nearest reachable endpoint and can remain pending. Stress/playtest walls, gates and dense armies.
- Measure rendering, full browser frame time and real production bandwidth. Earlier Node-only synthetic movement/fog benchmarks were 0.205/0.256/0.606/1.639/8.533 ms per tick for 20/50/100/200/500 units, respectively; these are not browser FPS measurements and predate the final map-only correction.
- Eight-direction state and animation hooks exist in simulation, but original artwork/animation quality and all idle/walk/attack/hit/death visual coverage require the separate asset/browser audit.

No measured severe resource-duplication, General-victory or Residence-reservation failure was found in the exercised scenarios. That is bounded evidence, not a claim that no severe bugs exist. The local simulation is reviewable and playable; section 81 completion still depends on all production, browser, visual and gameplay acceptance gates.
