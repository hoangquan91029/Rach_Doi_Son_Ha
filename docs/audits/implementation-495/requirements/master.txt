# MASTER AUTONOMOUS DEVELOPMENT PROMPT
# Project: 2.5D Historical RTS inspired by Age of Empires
# Working title: Rạch Đôi Sơn Hà RTS

You are the LEAD AUTONOMOUS GAME DEVELOPMENT AGENT.

Your responsibility is to inspect the existing project, understand its current state, create a production plan, delegate work to specialized subagents, integrate their output, test everything, audit the result, and continue iteratively until the game is complete or the available model/tool quota is exhausted.

DO NOT merely produce a design document.
ACTUALLY BUILD THE PROJECT.

Do not stop after one feature, one plan, one prototype, or one vertical slice unless you have reached a hard tool/quota limitation.

==================================================
0. PRIMARY GOAL
==================================================

Build a real-time strategy game inspired by Age of Empires, but centered almost entirely around:

- armies
- soldiers
- civilians
- kings
- generals
- logistics
- terrain
- naval movement
- food supply
- tactical maneuver

The game should use a 2.5D visual presentation similar in readability to classic Age of Empires-style RTS games.

Do NOT create a direct clone of Age of Empires assets, UI, copyrighted art, sounds, maps, or code.

Use original assets and systems.

Historical inspiration is allowed, but visuals must be original.

==================================================
1. PROJECT INSPECTION FIRST
==================================================

Before changing anything:

1. Inspect the entire repository.
2. Identify:
   - engine/framework
   - current scene hierarchy
   - rendering pipeline
   - animation pipeline
   - AI systems
   - pathfinding
   - combat system
   - data architecture
   - map architecture
   - save system
   - UI
   - existing assets
   - test infrastructure
3. Inspect this directory carefully:

/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha/leadership

It contains historical ruler/general folders such as:

han_xin
le_thanh_tong
ly_thuong_kiet
minh_menh
napoleon_bonaparte
nguyen_anh
nguyen_hue
nguyen_phuc_chu
tran_hung_dao
tran_nhan_tong
trinh_cuong
xiang_yu

Do NOT overwrite useful existing assets without checking them.

Reuse, repair, redraw, or replace assets when necessary.

==================================================
2. SUBAGENT MODEL ASSIGNMENT
==================================================

You are the orchestration model.

Delegate work aggressively.

VISUAL / ART / UI / SPRITES / ANIMATION TASKS:

Use subagents configured as:

GPT Luna High 6

for:

- unit concept art
- sprite sheets
- 8-direction characters
- building art
- terrain
- icons
- UI
- HUD
- menus
- minimap art
- visual effects
- animation planning
- animation frame generation
- portraits
- map visual design
- texture work
- visual consistency auditing

CODE / ARCHITECTURE / LOGIC TASKS:

Use subagents configured as:

GPT Sol 6.1 Light
thinking effort: low

for:

- gameplay programming
- architecture
- ECS/components
- state machines
- combat
- pathfinding
- economy
- logistics
- AI
- serialization
- UI logic
- map systems
- animation controllers
- unit controllers
- performance optimization
- tests
- debugging
- tooling

If those exact model identifiers are unavailable in the environment:
use the closest available model with the same intended division of responsibility.

The orchestrator must review ALL subagent output before integration.

Never blindly merge generated code.

==================================================
3. CORE MATCH STRUCTURE
==================================================

Each player selects:

1 KING
+
1 GENERAL

before the match starts.

The King and General are different strategic roles.

GENERAL DEATH RULE:

If a player's selected General dies permanently:

THAT PLAYER IMMEDIATELY LOSES THE MATCH.

Therefore:

- generals are extremely important
- generals must not behave like ordinary disposable units
- AI understands their strategic value
- UI clearly displays general HP/status
- enemy general location should not always be perfectly known without scouting

Do NOT make destruction of the Main Residence an automatic defeat.

==================================================
4. MAIN RESIDENCE / PALACE SYSTEM
==================================================

Each faction may have only ONE Main Residence at any moment.

Rules:

- maximum active Main Residence per player = 1
- it produces Villagers
- it acts as the political/logistical heart of the faction
- friendly units inside its healing radius regenerate HP
- healing must be configurable/data-driven
- the King is allowed to construct a replacement Main Residence ONLY if the previous Main Residence has been completely destroyed

Important state logic:

MainResidenceExists = true:
    player CANNOT build another Main Residence

MainResidenceExists = false:
    King gains permission to construct one new Main Residence

Once construction begins / completes:
    prevent duplicate Main Residences

Handle multiplayer/race-condition edge cases correctly.

Do not allow Main Residence duplication exploits.

==================================================
5. BUILDINGS
==================================================

Required buildings:

MAIN RESIDENCE
- villager production
- healing aura
- strategic core

BARRACKS
Produces:
- Spearman
- Arquebusier / Musket infantry

CAVALRY CAMP
Produces:
- cavalry units

ARTILLERY WORKSHOP
Produces:
- artillery

SHIPYARD
Produces naval units.

At minimum create a viable MVP naval roster with:
- transport vessel
- combat vessel

The architecture must support future ship classes.

FORT
- strong defensive military structure

WALL / FORTIFICATION SYSTEM
- wall segments
- gates where appropriate
- chokepoint control

SUPPLY DEPOT
- temporary resource storage
- logistics transfer point
- creates Supply Wagons

GRANARY
- stores food
- resupplies nearby soldiers/civilians
- acts as a local food logistics node

==================================================
6. RESOURCE SYSTEM
==================================================

The three strategic resources are:

WOOD
FOOD
IRON

WOOD:

Gathered by villagers.

If close enough to Main Residence:
deliver to Main Residence.

If far away:
villagers may deliver wood to a Supply Depot.

Wood deposited into a Supply Depot is automatically transferred/teleported to the faction's Main Residence/global strategic stockpile.

IRON:

Same strategic delivery model as wood.

Iron delivered to:
- Main Residence
OR
- Supply Depot

Iron stored in Supply Depot is automatically credited to the faction's central strategic stockpile.

FOOD IS DIFFERENT.

Food must have a REAL logistics chain.

Do NOT simply teleport all frontline food.

==================================================
7. FOOD / RATION SYSTEM
==================================================

Every human unit continuously consumes food.

Examples:

- villagers
- infantry
- cavalry
- generals
- kings
- appropriate crewed military units

Each unit should have something equivalent to:

foodReserve / ration meter

Food reserve gradually decreases over time.

Effects of low food should be data-driven.

Suggested states:

NORMAL
LOW SUPPLY
STARVING

Do NOT make starvation immediately kill units unless later balancing proves that necessary.

Recommended penalties:

LOW SUPPLY:
- slower stamina recovery
- small movement/combat penalty

STARVING:
- morale penalty
- slower movement
- reduced combat efficiency
- possible gradual HP attrition after a configurable grace period

All values must be configurable.

==================================================
8. GRANARY RESUPPLY
==================================================

Granaries contain physical food inventory.

If a friendly unit enters a configurable radius around a Granary:

and

Granary.food > 0

then the unit automatically replenishes its ration reserve.

The food must actually be removed from the granary inventory.

NO infinite-food aura.

Show clear UI feedback.

Examples:

resupply icon
food transfer indicator
ration meter

==================================================
9. SUPPLY DEPOT
==================================================

Supply Depot acts as:

- temporary food storage
- local logistics hub
- wood transfer point
- iron transfer point
- Supply Wagon production building
- frontline transshipment center

Villagers can transport food to Supply Depots.

Supply Wagons can take food from Supply Depots and move it toward the army.

==================================================
10. SUPPLY WAGON
==================================================

Supply Wagon is created from Supply Depot.

Primary role:

transport food from rear logistics to frontline forces.

Implement:

- food cargo
- limited cargo capacity
- movement speed
- loading
- unloading
- resupply radius or explicit resupply interaction
- vulnerability to raids
- destruction/capture behavior according to game balance
- UI cargo indicator

A frontline army should become vulnerable when its supply chain is cut.

This is a KEY FEATURE of the game.

Terrain, cavalry raids, river crossings and ambushes must make logistics tactically meaningful.

==================================================
11. HISTORICAL KING / GENERAL SYSTEM
==================================================

Recreate the historical rulers and generals found in:

/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha/leadership

Do not reduce them to generic attack bonuses.

Their bonuses must be based on the provided historical research dossier.

The important distinction is:

historical evidence
vs
gameplay interpretation.

All gameplay abilities must be represented as game mechanics rather than claims that the numeric values themselves are historical facts.

Implement the roster as data-driven character definitions.

Required initial roster:

Han Xin
Xiang Yu
Napoleon Bonaparte
Lý Thường Kiệt
Trần Hưng Đạo
Nguyễn Huệ / Quang Trung
Lê Thánh Tông
Minh Mạng / Minh Mệnh
Nguyễn Ánh / Gia Long
Nguyễn Phúc Chu
Trần Nhân Tông
Trịnh Cương

==================================================
12. CHARACTER GAMEPLAY IDENTITIES
==================================================

Use the historical dossier as the source of truth.

Target gameplay identities:

HAN XIN
Role:
maneuver / deception

Concepts:
- Backs to the River
- False Crossing
- powerful flanking / deception
- strong when manipulating enemy positioning

Weakness:
political / strategic vulnerability rather than raw battle weakness

XIANG YU
Role:
shock / morale commander

Concepts:
- Break the Cauldrons
- extremely powerful direct assault
- morale shock
- troops resist routing near him

Weakness:
poor prolonged coalition stability / strategic sustainability

NAPOLEON
Role:
operational concentration

Concepts:
- March Separately, Fight Together
- Central Position
- coordinated separated formations
- rapid concentration

Weakness:
overextension and logistics

LÝ THƯỜNG KIỆT
Role:
preemptive offense + fortified defense

Concepts:
- Preempt the Invasion
- Như Nguyệt Line
- river defense
- attack enemy preparations before invasion

Weakness:
long deep occupation

TRẦN HƯNG ĐẠO
Role:
defense in depth / logistics denial

Concepts:
- Deny the Granaries
- Preserve the Army
- prepared killing grounds
- river warfare
- ambush
- starving invading armies

Weakness:
less dominant when unexpectedly forced into battle before preparation

NGUYỄN HUỆ / QUANG TRUNG
Role:
tempo / surprise

Concepts:
- Tết Thunderbolt
- Multi-Axis Advance
- rapid movement
- offensive momentum
- surprise

Weakness:
prolonged static warfare

LÊ THÁNH TÔNG
Role:
institutional / mobilization ruler

Concepts:
- Hồng Đức Institutions
- State Mobilization
- recruitment efficiency
- stronger economy-to-military conversion

Weakness:
new territory requires administration

MINH MẠNG
Role:
centralization ruler

Concepts:
- Provincial Centralization
- Imperial Inspection
- administrative efficiency

Weakness:
centralization pressure / unrest

NGUYỄN ÁNH / GIA LONG
Role:
resilience / logistics / comeback

Concepts:
- Return from Defeat
- Southern Arsenal
- strong naval/logistics potential
- rebuilding after setbacks

Weakness:
slow start

NGUYỄN PHÚC CHU
Role:
frontier / maritime / expansion

Concepts:
- Southern Frontier Network
- Maritime Envoys
- settlement/trade integration

Weakness:
frontier integration complexity

TRẦN NHÂN TÔNG
Role:
unity / morale / national resilience

Concepts:
- Diên Hồng Consensus
- Reconstruction Edict
- strong synergy with generals
- national morale

Weakness:
less direct tactical power

TRỊNH CƯƠNG
Role:
fiscal / bureaucracy

Concepts:
- Fiscal Reorganization
- administrative efficiency
- cheaper military upkeep
- strong economy

Weakness:
dual legitimacy / political constraints

==================================================
13. KING + GENERAL SYNERGY SYSTEM
==================================================

The King and General must be separate choices.

Create a flexible synergy architecture.

Examples:

Trần Nhân Tông + Trần Hưng Đạo

should create exceptional:
- national morale
- defensive resilience
- logistics denial
- recovery

Nguyễn Huệ should create:
- rapid offensive tempo

Nguyễn Ánh should create:
- survival/reconstruction/logistics

Han Xin should:
- manipulate position/information

Xiang Yu should:
- dominate direct engagements

Do NOT hard-code only these combinations.

Use tags and modifiers so new King/General synergies can be added later.

Example tags:

DEFENSE_IN_DEPTH
LOGISTICS
MORALE
SHOCK
MANEUVER
DECEPTION
NAVAL
ADMINISTRATION
ECONOMY
SURPRISE
FORTIFICATION
SUPPLY_DENIAL
MOBILIZATION

==================================================
14. VISUAL STYLE
==================================================

Target:

2.5D RTS

inspired by the readability of classic Age of Empires.

Requirements:

- original visual identity
- top-down / angled camera
- terrain readable at a glance
- units clearly distinguishable
- buildings readable from gameplay zoom
- good silhouette language
- optimized sprite batching/atlas system where appropriate

Characters must have 8 directional states:

N
NE
E
SE
S
SW
W
NW

At minimum for units such as:

Villager
King
General
Infantry
Spearman
Arquebusier
Cavalry

Animation architecture should support:

idle
walk
attack
hit
death

Additional states as necessary:

gather
carry
build
repair
reload
special ability
mount
unmount

Do not manually duplicate animation logic for every character.

Create reusable animation/state architecture.

==================================================
15. HISTORICAL CHARACTER ART
==================================================

Use the material in:

/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha/leadership

as visual reference.

Recreate each ruler/general with:

- original sprites
- readable historical silhouette
- recognizable clothing/armor concepts
- faction/era distinction
- 8 directions
- consistent scale
- consistent palette rules
- portrait icon
- selection icon
- unit card

Do not simply create one sprite and mirror it blindly if asymmetrical historical details make that visually incorrect.

The Luna art agents should generate:
- visual references
- sprites
- sprite sheets
- portrait assets
- animations

Then the orchestrator must verify alignment with the runtime sprite pipeline.

==================================================
16. MAPS
==================================================

Create TWO complete maps.

Both maps must contain:

- sea
- rivers
- plains
- hills
- mountains
- forests
- resource zones
- strategic chokepoints
- multiple viable routes
- naval pathways
- crossing points
- ambush opportunities
- defensible positions

Maps must not look like random noise.

They should support strategic decision-making.

==================================================
17. MAP 1 DESIGN PHILOSOPHY
==================================================

Create one map focused on:

RIVER + DELTA WARFARE

Possible design principles:

- wide navigable river
- tributaries
- river crossings
- ford zones
- bridge opportunities if supported
- floodplain
- forest near crossings
- hill overlooking strategic river
- coastal access
- naval flanking

The map must enable:

- blocking crossings
- river ambush
- supply interception
- naval transport
- artillery on elevated positions
- defensive river lines

==================================================
18. MAP 2 DESIGN PHILOSOPHY
==================================================

Create one map focused on:

COAST + MOUNTAIN + FOREST WARFARE

Include:

- coastline
- bays
- mountain passes
- forest corridors
- hidden movement opportunities
- multiple supply routes
- coastal landing opportunities
- chokepoints
- open plains for cavalry

The map should allow:

- amphibious flanking
- mountain-pass defense
- forest ambushes
- supply-line raids
- cavalry battles on plains

==================================================
19. TERRAIN GAMEPLAY
==================================================

Terrain must affect tactics.

Examples:

FOREST:
- lower detection
- ambush bonus
- cavalry movement penalties where appropriate

HILL:
- vision advantage
- ranged/artillery advantage
- movement cost

MOUNTAIN:
- mostly impassable
- creates chokepoints

RIVER:
- movement restriction
- crossing vulnerability

SEA:
- requires ships

PLAIN:
- fast movement
- cavalry-friendly

Do not overcomplicate early implementation.

Build a clean, extensible terrain modifier system.

==================================================
20. FOG OF WAR
==================================================

Implement proper RTS:

- unexplored
- explored but currently unseen
- visible

Scouting must matter.

Ambush systems depend on incomplete information.

King/general location should not be freely visible through fog of war.

==================================================
21. COMBAT
==================================================

Create a deterministic and readable RTS combat architecture.

Support:

- melee
- ranged
- cavalry
- firearms
- artillery
- naval combat
- structures

Avoid excessive RNG.

Any RNG must be controlled and reproducible with seeds where practical.

Core stats should be data-driven.

Examples:

HP
armor
damage
range
attack cooldown
movement speed
vision
food capacity
food consumption
morale
mass
collision radius

==================================================
22. MORALE
==================================================

Implement a lightweight morale system.

Morale may be influenced by:

- General nearby
- King nearby
- starvation
- commander death
- flank attack
- artillery shock
- allies routing
- historical abilities

Do NOT let morale replace understandable combat.

UI must communicate morale state.

==================================================
23. FORMATIONS
==================================================

If architecture permits, support basic formations:

- line
- column
- box / defensive formation

Do not spend the entire project on sophisticated Total War-style formation simulation.

Start simple.

Formation system must remain performant with large unit counts.

==================================================
24. PATHFINDING
==================================================

Pathfinding must support:

- many units
- structures
- forests
- impassable mountains
- rivers
- coast
- ships
- formation movement where possible

Prevent:
- unit deadlocks
- doorway congestion
- permanent oscillation
- extremely expensive per-frame recalculation

Use hierarchical/nav-grid/flow-field approaches if appropriate for the engine and current codebase.

Profile before rewriting.

==================================================
25. USER INTERFACE
==================================================

Create a functional RTS HUD.

Must show:

- wood
- food
- iron
- population if used
- selected unit
- HP
- ration level
- morale
- orders
- abilities
- building production queue
- King status
- General status
- Main Residence status
- minimap
- alerts

Important warnings:

GENERAL UNDER ATTACK

GENERAL LOW HP

GENERAL DEAD

SUPPLY LINE DISRUPTED

ARMY LOW ON FOOD

MAIN RESIDENCE DESTROYED

KING MAY REBUILD MAIN RESIDENCE

==================================================
26. SELECTION AND CONTROLS
==================================================

Support standard RTS interaction:

- click selection
- drag box selection
- shift-add/remove if supported
- right click move
- right click attack
- attack move
- patrol if useful
- stop
- hold
- control groups
- camera pan
- zoom
- minimap navigation

==================================================
27. AI
==================================================

Create functional enemy AI.

AI must understand:

- gathering
- economy
- training
- construction
- general survival
- King survival
- Main Residence replacement
- food logistics
- Supply Depot
- Supply Wagon
- Granary
- scouting
- attacking supply lines
- defending supply lines
- naval movement
- terrain
- retreat
- rebuilding

GENERAL RULE:

AI must avoid suiciding its General.

But it should still use the General meaningfully.

==================================================
28. PERFORMANCE TARGET
==================================================

Optimize for large RTS battles.

Create performance benchmarks.

Test:

20 units
50 units
100 units
200 units
500 units if practical

Track:

FPS
frame time
pathfinding cost
AI cost
render cost
animation cost

Avoid allocating large temporary objects every frame.

Pool objects where beneficial.

==================================================
29. DATA-DRIVEN DESIGN
==================================================

Do not scatter balance numbers throughout source code.

Use centralized data definitions/resources/config.

Create definitions for:

UnitData
BuildingData
CharacterData
AbilityData
ResourceData
TerrainData
MapData
FactionData

Historical character buffs should be editable without rewriting core engine logic.

==================================================
30. DEVELOPMENT ORDER
==================================================

Do NOT attempt everything simultaneously.

Use milestone development.

Recommended sequence:

MILESTONE 0
Repository audit + architecture plan

MILESTONE 1
Core RTS controls + camera + selection

MILESTONE 2
Villager + gathering + resource storage

MILESTONE 3
Buildings + production

MILESTONE 4
Combat vertical slice

MILESTONE 5
General death defeat condition

MILESTONE 6
King + Main Residence rebuild rules

MILESTONE 7
Food consumption + granary

MILESTONE 8
Supply Depot + Supply Wagon logistics

MILESTONE 9
Terrain + fog of war + ambush

MILESTONE 10
King/general character system

MILESTONE 11
Historical passive/active abilities

MILESTONE 12
Naval gameplay

MILESTONE 13
Two finished maps

MILESTONE 14
AI

MILESTONE 15
Visual replacement / final sprite pipeline

MILESTONE 16
UI/UX polish

MILESTONE 17
Performance optimization

MILESTONE 18
Balance + bug fixing

MILESTONE 19
Complete playable match validation

However:
adapt this order based on what already exists in the repository.

==================================================
31. DEFINITION OF DONE FOR EACH FEATURE
==================================================

A feature is NOT done because code was written.

It is done only when:

- integrated
- runnable
- visually/functionally testable
- errors fixed
- edge cases checked
- regression tested
- documented sufficiently
- no placeholder implementation remains unless explicitly tracked

==================================================
32. TESTING
==================================================

Create automated tests where practical.

Also create scenario tests.

Mandatory scenarios:

TEST A:
General dies -> player loses.

TEST B:
Main Residence exists -> King cannot construct second one.

TEST C:
Main Residence destroyed -> King may construct replacement.

TEST D:
Replacement completed -> cannot build another.

TEST E:
Unit consumes food over time.

TEST F:
Unit near stocked Granary replenishes food.

TEST G:
Empty Granary cannot resupply.

TEST H:
Supply Wagon loads food.

TEST I:
Supply Wagon transports food.

TEST J:
Wood delivered to Supply Depot reaches central resource pool.

TEST K:
Iron delivered to Supply Depot reaches central resource pool.

TEST L:
Fog of war hides enemy General.

TEST M:
Naval units cannot travel over land.

TEST N:
Land units cannot cross deep sea without transport.

TEST O:
AI can build a functioning economy.

TEST P:
AI protects its General reasonably.

==================================================
33. VISUAL SUBAGENT WORKFLOW
==================================================

For each visual batch:

1. Orchestrator defines technical constraints:
   - size
   - frame count
   - directions
   - pivot
   - naming
   - alpha requirements
   - atlas arrangement

2. Luna High 6 generates/refines assets.

3. Orchestrator checks:
   - clipping
   - scale
   - readability
   - direction consistency
   - pivot alignment
   - historical distinction
   - runtime compatibility

4. Integrate.

5. Test in-game.

Never generate thousands of assets before validating the sprite pipeline.

First create ONE complete vertical-slice character.

Recommended first complete animated unit:
generic infantry or villager.

Then validate pipeline.

Then scale to other units.

==================================================
34. CODE SUBAGENT WORKFLOW
==================================================

For each engineering task:

1. give Sol 6.1 Light a narrowly defined implementation task
2. require it to inspect relevant source files
3. require it to state files changed
4. require tests
5. orchestrator reviews the diff
6. run build/tests
7. fix errors
8. integrate

Avoid assigning the entire game to one subagent call.

==================================================
35. AUDIT LOOP
==================================================

After EVERY meaningful milestone:

Produce an AUDIT PACKAGE containing:

STATUS
- what works

IMPLEMENTED
- completed features

TESTED
- tests executed
- results

KNOWN BUGS

TECH DEBT

PERFORMANCE

ASSET STATUS

GAMEPLAY STATUS

NEXT PRIORITIES

FILES CHANGED

Then let the CURRENT PARENT MODEL / CURRENT CHAT MODEL audit the state.

The audit model should:

1. inspect implementation
2. identify architectural problems
3. identify missing requirements
4. identify bugs
5. identify performance risks
6. identify gameplay problems
7. create the next execution plan

Then resume implementation.

Repeat:

BUILD
-> TEST
-> AUDIT
-> PLAN
-> BUILD
-> TEST
-> AUDIT
-> PLAN

until project completion.

==================================================
36. DO NOT STOP EARLY
==================================================

Do NOT stop merely because:

- one milestone is complete
- a vertical slice works
- code compiles
- first map works
- first unit works
- an audit has been written

Continue automatically with the next highest-priority task.

Do not repeatedly ask the user:
"Should I continue?"

Assume continuation is authorized.

==================================================
37. QUOTA / CONTEXT LIMIT HANDLING
==================================================

Continue working until:

A. project is complete

OR

B. hard quota/tool/model/context limitation prevents further progress.

If quota is close to exhaustion:

DO NOT begin a huge risky refactor.

Instead:

1. finish current atomic task
2. make repository runnable
3. run tests
4. preserve all generated assets
5. write/update PROJECT_STATUS.md
6. write/update NEXT_STEPS.md
7. write/update ARCHITECTURE.md
8. record known bugs
9. record exact next task
10. record subagent work that remains
11. save/commit working state if git is available

Then stop safely.

The next agent must be able to resume without rediscovering the entire project.

==================================================
38. GIT SAFETY
==================================================

If repository uses git:

Before major work:

git status

Do not destroy existing uncommitted user work.

Do not use destructive commands such as:

git reset --hard
git clean -fd

unless absolutely necessary and explicitly justified.

Use small meaningful commits.

Suggested commit pattern:

feat(rts):
feat(logistics):
feat(combat):
feat(ai):
feat(ui):
feat(map):
feat(leadership):
fix:
perf:
test:
docs:

==================================================
39. PROJECT DOCUMENTATION
==================================================

Maintain:

README.md
ARCHITECTURE.md
GAME_DESIGN.md
PROJECT_STATUS.md
NEXT_STEPS.md

Also create where useful:

docs/
    economy.md
    logistics.md
    combat.md
    leadership.md
    maps.md
    ai.md
    animation_pipeline.md

==================================================
40. IMPORTANT GAME-DESIGN PRINCIPLE
==================================================

This game's identity is NOT:

"Age of Empires but with different skins."

Its identity is:

TACTICAL RTS
+
HISTORICAL LEADERSHIP
+
SUPPLY-LINE WARFARE
+
TERRAIN
+
AMBUSH
+
KING/GENERAL ASYMMETRY
+
LOGISTICS

The gameplay loop should naturally produce situations such as:

- cavalry raiding enemy food wagons
- an invading army starving far from depots
- troops recovering around the Main Residence
- forests hiding an ambush
- artillery controlling a river crossing
- warships supporting a coastal landing
- a General becoming the strategic target
- a King retreating after the Main Residence falls
- the King establishing a replacement headquarters elsewhere
- Trần Hưng Đạo deliberately trading territory for logistical advantage
- Nguyễn Huệ exploiting speed and surprise
- Nguyễn Ánh surviving and rebuilding
- Han Xin using deception
- Napoleon concentrating separated forces
- Xiang Yu forcing a brutal decisive battle

==================================================
41. FIRST ACTION RIGHT NOW
==================================================

Do not immediately write random code.

Start by:

1. inspect repository
2. inspect /home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha/leadership
3. inspect existing game scenes/assets/code
4. inspect git status
5. determine existing engine architecture
6. identify which requested systems already exist
7. identify broken/incomplete systems
8. create PROJECT_STATUS.md
9. create an implementation plan based on ACTUAL repository state
10. start implementing the highest-priority missing vertical slice

After the first working milestone:

run the audit loop.

Then continue automatically.

==================================================
42. COMPLETION CRITERIA
==================================================

The project is considered COMPLETE only when a user can launch the game and play a full match containing:

- map selection
- King selection
- General selection
- both required maps
- villagers
- resource gathering
- wood
- food
- iron
- buildings
- army production
- combat
- cavalry
- infantry
- firearms
- artillery
- ships
- Main Residence
- Main Residence healing
- Main Residence replacement by King after destruction
- exactly one Main Residence at once
- food consumption
- Granary resupply
- Supply Depot
- Supply Wagon
- real frontline food logistics
- fog of war
- terrain effects
- historical leader buffs
- AI opponent
- general-death defeat condition
- victory/defeat screen
- functional UI
- 2.5D visual presentation
- 8-direction important unit animations
- acceptable performance
- no major game-breaking bugs

Until these conditions are met:

THE PROJECT IS NOT FINISHED.

Start now.