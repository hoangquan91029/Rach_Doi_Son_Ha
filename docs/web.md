==================================================
43. WEB-FIRST GAME REQUIREMENT — HARD REQUIREMENT
==================================================

THIS GAME MUST BE PLAYABLE DIRECTLY IN A MODERN WEB BROWSER.

The final product must NOT require the normal player to:

- clone the repository
- install the game
- install an engine
- install Node/Python
- compile source code
- configure a local server
- download an executable

The normal user experience must be:

1. receive a URL
2. open the URL
3. game loads
4. choose Single Player or Online
5. play

Examples of supported desktop browsers:

- Chrome / Chromium
- Firefox
- Edge

Linux, Windows and macOS desktop browsers should all be supported where technically practical.

The architecture is therefore WEB-FIRST.

If the current project uses an engine/framework that already supports reliable web export,
preserve it unless there is a strong technical reason to change.

Before making architectural changes:

1. inspect the current engine
2. verify its current web-export capability
3. benchmark the existing build in browser
4. identify browser-specific limitations
5. only migrate architecture if genuinely necessary

Do NOT rewrite the entire project merely because another web framework exists.

==================================================
44. WEB RENDERING
==================================================

Rendering must use browser-compatible technology appropriate to the existing engine.

Possible technologies include:

- WebGL
- WebGL2
- Canvas where appropriate
- WebAssembly where supported by the existing engine
- browser-compatible engine export

The game should prioritize desktop browsers.

Mobile browser support is NOT a primary target for the initial project because RTS controls,
large battles and complex UI are desktop-focused.

However, the website itself should fail gracefully on unsupported devices.

Display a useful compatibility message rather than crashing.

==================================================
45. WEB PERFORMANCE
==================================================

Because the game runs in a browser:

pay special attention to:

- memory consumption
- texture atlas size
- sprite batching
- draw calls
- JavaScript/WASM garbage generation
- pathfinding CPU usage
- AI CPU usage
- animation processing
- network serialization
- loading time
- browser tab throttling behavior
- asset compression
- cache behavior

Do not load every asset in the entire project before reaching the main menu.

Implement staged loading where appropriate.

Recommended flow:

BOOT
-> minimal core assets
-> MAIN MENU
-> game configuration
-> selected map/character assets
-> MATCH

Use compressed web-friendly assets.

Avoid unnecessarily huge texture files.

==================================================
46. MAIN MENU
==================================================

Create a proper web-game landing/menu flow.

Required main menu:

PLAY

    SINGLE PLAYER

    ONLINE 1 VS 1

OPTIONAL:
    SETTINGS
    HOW TO PLAY
    CREDITS

Keep the interface simple.

Do NOT build unnecessary MMO/community/social systems.

==================================================
47. SINGLE PLAYER MODE
==================================================

Single Player means:

PLAYER
VS
AI

Flow:

1. select Single Player
2. select map
3. select King
4. select General
5. optionally choose AI difficulty
6. start match

Recommended AI difficulty presets:

EASY
NORMAL
HARD

Do not create fake difficulty by simply multiplying enemy damage by extreme values.

Difficulty should preferably influence:

- reaction speed
- economy efficiency
- scouting
- tactical decision quality
- aggression
- retreat logic
- supply management

Single Player must work WITHOUT connecting to the multiplayer game server after the client has loaded,
unless the current architecture has a strong reason to do otherwise.

Prefer running the AI locally in the browser.

==================================================
48. ONLINE MULTIPLAYER — EXACTLY TWO PLAYERS
==================================================

The online multiplayer scope is deliberately SMALL.

The game supports:

1 human
VS
1 human

Maximum human players in a multiplayer match:

2

DO NOT design infrastructure for:

- 4 players
- 8 players
- 16 players
- MMO
- persistent worlds
- clans
- guilds
- tournaments
- spectating infrastructure
- huge matchmaking systems

unless required much later.

Optimize networking architecture specifically for TWO PLAYERS.

==================================================
49. ONLINE USER EXPERIENCE
==================================================

The multiplayer UX should be extremely simple.

ONLINE 1 VS 1:

CREATE ROOM

or

JOIN ROOM

CREATE ROOM:

Player clicks:

CREATE ROOM

Server creates something similar to:

Room code:
Q7K9XZ

and ideally also provides a shareable link similar to:

https://game.example.com/join/Q7K9XZ

The player sends either:

- room code
OR
- room URL

to the other player.

Second player opens the link.

The game joins the room.

No complicated lobby browser is necessary.

==================================================
50. NO ACCOUNT REQUIRED FOR BASIC PLAY
==================================================

Basic 1v1 multiplayer should NOT require account registration unless later requirements make accounts necessary.

Default experience:

Enter nickname

CREATE ROOM

or

JOIN ROOM

This reduces friction.

The goal is:

LINK -> GAME

Do not add:

- email verification
- password system
- social login
- profile backend

unless explicitly requested later.

==================================================
51. TWO-PLAYER LOBBY
==================================================

Lobby contains exactly TWO player slots:

PLAYER 1
PLAYER 2

Each player selects:

- nickname
- King
- General

Host may select:

- map

Both players have:

READY / NOT READY

Match starts when:

playerCount == 2
AND
player1.ready == true
AND
player2.ready == true

Prevent accidental duplicate start.

Show connection state.

Examples:

CONNECTED

WAITING FOR OPPONENT

OPPONENT CONNECTED

OPPONENT DISCONNECTED

RECONNECTING

==================================================
52. MULTIPLAYER NETWORK ARCHITECTURE
==================================================

Choose the simplest architecture that remains reliable for a competitive RTS.

Because only TWO players exist, avoid over-engineering.

Preferred approach:

WEB CLIENT
       |
       | WebSocket
       |
LIGHTWEIGHT MATCH SERVER
       |
       +-- Room A: Player 1 + Player 2
       +-- Room B: Player 1 + Player 2
       +-- ...

Use a lightweight authoritative or simulation-coordinating server.

Do not synchronize every sprite animation frame.

Synchronize GAME STATE / COMMANDS.

Examples of network commands:

MOVE
ATTACK
ATTACK_MOVE
BUILD
TRAIN
GATHER
LOAD_SUPPLY
UNLOAD_SUPPLY
USE_ABILITY
CHANGE_FORMATION

The renderer remains local.

==================================================
53. SERVER AUTHORITY
==================================================

Do NOT blindly trust clients for critical state.

Critical rules such as:

- General death
- victory
- resource counts
- building creation
- unit creation
- Main Residence uniqueness
- damage
- food transfer
- Supply Wagon cargo
- player defeat

must be validated by the authoritative simulation/server architecture.

A modified browser client must not be able to simply send:

give_me_100000_iron

and succeed.

However:

do NOT create a massive anti-cheat platform.

Use sensible server validation appropriate to a 2-player indie RTS.

==================================================
54. RTS NETWORK SYNCHRONIZATION
==================================================

The networking model must be intentionally designed.

Investigate two viable approaches:

A. deterministic command / lockstep simulation

or

B. authoritative server simulation with client prediction/interpolation where needed

Choose based on the ACTUAL existing simulation architecture.

For RTS with many units and only two players:

prefer sending compact COMMANDS rather than sending the full position of every unit every frame.

Example:

BAD:

send positions of 400 units at 60 Hz without need

BETTER:

Player 1:
unitIds=[15,16,17,18]
MOVE x=1250 y=770
simulationTick=14520

Both simulations then execute the command deterministically
or the authoritative server validates and applies it.

==================================================
55. FIXED SIMULATION TICK
==================================================

Multiplayer simulation should use a FIXED simulation tick independent from rendering FPS.

Example concept:

simulation:
20–30 ticks/sec

rendering:
up to display refresh rate

The exact value must be benchmarked.

Do NOT bind game logic directly to browser rendering FPS.

This is essential for:

- networking
- reproducibility
- debugging
- synchronization
- replays later if desired

==================================================
56. DETERMINISM
==================================================

If deterministic lockstep is selected:

all gameplay-affecting randomness must come from synchronized seeded RNG.

Do NOT use uncontrolled:

Math.random()

or equivalent calls inside multiplayer game simulation.

The following must behave consistently:

- damage variation
- targeting
- AI if relevant
- ability proc
- random map behavior
- projectile simulation where gameplay-relevant

Build a determinism test.

Example:

same seed
+
same commands
+
same initial state

must produce the same simulation hash.

==================================================
57. STATE HASH / DESYNC DETECTION
==================================================

If using deterministic simulation:

periodically calculate a compact game-state hash.

Example:

tick 5000

Player A hash:
0xA832...

Player B hash:
0xA832...

MATCH

If they diverge:

detect DESYNC.

Log useful diagnostics.

Never silently allow two completely different matches to continue indefinitely.

==================================================
58. NETWORK LATENCY
==================================================

The online game must remain playable under realistic internet conditions.

Test approximately:

20 ms
50 ms
100 ms
150 ms
200 ms

Do not optimize only for localhost.

Because the game is RTS rather than a twitch FPS,
small command buffering is acceptable.

Prefer stability and synchronization over pretending network latency does not exist.

==================================================
59. DISCONNECTION / RECONNECTION
==================================================

Implement a minimal reconnect system.

If Player 2 temporarily loses connection:

do not instantly destroy the match.

Show:

OPPONENT DISCONNECTED

Allow a configurable reconnect window.

For example:

30–90 seconds

Choose a reasonable default after testing.

If opponent reconnects:

restore the match connection.

If reconnect timeout expires:

remaining player wins by disconnect/forfeit.

==================================================
60. PAUSE ON CONNECTION LOSS
==================================================

Because multiplayer has ONLY TWO players,
it is acceptable and desirable to pause or temporarily halt authoritative progression during a short connection interruption.

This greatly simplifies fairness.

Do not design complex majority-consensus networking intended for many players.

There are only two players.

==================================================
61. ROOM LIFECYCLE
==================================================

A room should have simple states:

WAITING
READY
STARTING
IN_MATCH
FINISHED
CLOSED

Empty rooms should automatically expire.

Finished rooms should not remain in server memory forever.

Do not build permanent room persistence unless required.

==================================================
62. MULTIPLAYER SECURITY
==================================================

Implement reasonable baseline web security.

Examples:

- validate room IDs
- validate command payloads
- validate unit ownership
- validate resource spending
- rate-limit obviously abusive requests
- limit message sizes
- reject invalid simulation commands
- prevent a player from commanding enemy units
- prevent spawning arbitrary entities
- sanitize nickname display

Do NOT trust arbitrary JSON from browsers.

==================================================
63. PUBLIC DEPLOYMENT
==================================================

Deployment is part of the project.

The project is NOT finished merely because localhost works.

There must be a deployable production configuration.

Final target:

PUBLIC HTTPS URL

Example:

https://rach-doi-son-ha.example.com

The exact provider/domain may vary.

Suitable architecture may use:

STATIC / WEB CLIENT HOSTING
+
LIGHTWEIGHT WEBSOCKET SERVER

Potential deployment platforms may be evaluated based on the actual stack.

Do NOT tightly couple gameplay code to one hosting provider unless necessary.

Provide deployment documentation.

==================================================
64. DEPLOYMENT PIPELINE
==================================================

Create a production build workflow.

Recommended result:

git push
        |
        v
build
        |
        +--> web client
        |
        +--> multiplayer server
        |
        v
deployment

If CI/CD is practical in the repository, configure it.

At minimum document:

- build command
- client deployment
- server deployment
- environment variables
- WebSocket URL
- production configuration
- rollback procedure

==================================================
65. LOCAL DEVELOPMENT
==================================================

Developers should still be able to test locally.

Provide an easy command or script.

Example concept:

./dev.sh

or equivalent.

It should start:

web client
+
multiplayer backend

with as little manual configuration as practical.

Provide:

.env.example

NEVER commit real secrets.

==================================================
66. MULTIPLAYER SIMULATION TESTS
==================================================

Add these mandatory tests:

TEST Q:
Player creates room.

TEST R:
Second player joins room.

TEST S:
Third player cannot join a full 2-player room.

TEST T:
Both players select King and General.

TEST U:
Match cannot start until both players are ready.

TEST V:
Both clients begin with identical world state.

TEST W:
Player cannot command enemy units.

TEST X:
Player cannot create resources through invalid network messages.

TEST Y:
General death is synchronized and produces the same winner for both players.

TEST Z:
Main Residence destruction is synchronized.

TEST AA:
King can rebuild Main Residence only after previous one is destroyed.

TEST AB:
Both players see the same replacement Main Residence.

TEST AC:
Supply Wagon cargo remains synchronized.

TEST AD:
Granary food inventory remains synchronized.

TEST AE:
Unit food consumption remains synchronized.

TEST AF:
Fog-of-war information does not accidentally leak hidden enemy information through UI/network messages.

TEST AG:
Temporary network disconnection triggers reconnect flow.

TEST AH:
Reconnect restores player to correct match.

TEST AI:
Reconnect timeout causes appropriate forfeit.

TEST AJ:
100–200 ms simulated latency does not corrupt game state.

TEST AK:
Multiplayer match can reach victory and return both players to result screen.

==================================================
67. MULTIPLAYER LOAD TEST SCOPE
==================================================

Do NOT waste time simulating a 64-player server.

Relevant server tests are:

1 match
2 players

5 matches
10 players

10 matches
20 players

then increase only if inexpensive.

The important performance question is:

Can many independent TWO-PLAYER rooms coexist cheaply?

not:

Can one huge match support hundreds of human players?

==================================================
68. SINGLE PLAYER AND MULTIPLAYER MUST SHARE GAME RULES
==================================================

Do not create two completely different game implementations.

Core gameplay simulation should be reusable.

Conceptually:

CORE GAME SIMULATION
        |
        +------------------+
        |                  |
SINGLE PLAYER          ONLINE 1v1
        |                  |
LOCAL AI              NETWORK INPUT
        |                  |
        +------same rules--+

Systems such as:

- combat
- movement
- resources
- food
- logistics
- King
- General
- buildings
- abilities
- victory

must use the same core rules.

This prevents single-player and multiplayer balance from diverging.

==================================================
69. MULTIPLAYER MAP RULE
==================================================

Both required maps must work in:

SINGLE PLAYER

and

ONLINE 1 VS 1

Map spawn layout must be reasonably symmetrical in competitive opportunity even if geography is visually asymmetric.

Both players need viable access to:

- wood
- food
- iron
- defensible terrain
- naval access where applicable
- expansion opportunities

Do not place one player into an obviously superior starting position.

==================================================
70. 1v1 MAP DESIGN
==================================================

Because multiplayer is always 1v1:

design map flow specifically around TWO factions.

Do not leave six unused spawn locations.

Each map should have:

Player 1 territory

Player 2 territory

contested center / strategic region

secondary routes

naval route

raid routes

supply-line routes

Terrain should create several strategic choices rather than a single mandatory chokepoint.

==================================================
71. ONLINE GAME FLOW
==================================================

Target complete UX:

USER OPENS WEBSITE

        ↓

MAIN MENU

     ↙         ↘

SINGLE PLAYER      ONLINE 1v1

     ↓                 ↓

Map              Create / Join Room
King                    ↓
General          Player 1 + Player 2
AI Difficulty           ↓
     ↓              Select King
START               Select General
     ↓                   ↓
VS AI                 READY
                         ↓
                      START
                         ↓
                       1v1

After match:

RESULT

WIN / LOSS

Statistics:

- match duration
- units killed
- units lost
- resources gathered
- food transported
- supply wagons destroyed
- buildings destroyed
- General status
- major ability usage

Buttons:

PLAY AGAIN / REMATCH where practical

MAIN MENU

==================================================
72. REMATCH
==================================================

Because the game is only 1v1,
add a lightweight REMATCH system after multiplayer match completion.

Both players choose:

REMATCH

If both accept:

return to lobby or restart configuration.

Do not require both users to manually create a brand-new room after every match.

==================================================
73. SHAREABLE ROOM LINK
==================================================

One of the highest-value web multiplayer features is a shareable invitation URL.

When Player 1 creates a room, generate:

ROOM CODE

and

SHAREABLE JOIN URL

Example concept:

https://game.domain/join/AB12CD

Opening that URL should take Player 2 directly to the join flow for that room.

If the room:

does not exist
expired
already has 2 players

show an understandable error and return to Online menu.

==================================================
74. WEB REFRESH BEHAVIOR
==================================================

Handle browser refresh gracefully.

Single player:

a refresh may end the match in the initial MVP if persistence is not yet implemented,
but this behavior must be clear.

Online:

refresh should attempt to reconnect using the current session identity rather than always treating the user as a third player.

Do not accidentally duplicate player slots on refresh.

==================================================
75. BROWSER TAB BEHAVIOR
==================================================

Browsers can throttle inactive tabs.

Detect relevant visibility/focus events where appropriate.

Do not let an inactive browser tab silently cause impossible simulation divergence.

For online mode, authoritative simulation/network architecture must remain safe even if one player's rendering tab temporarily slows down.

==================================================
76. NETWORK DEBUG OVERLAY
==================================================

Create a DEVELOPMENT-ONLY network diagnostics overlay.

Show:

ping
simulation tick
server tick
command queue
desync status
room ID
reconnect status

Optional:

packet/message rate
bandwidth

This overlay must be easy to disable in production.

It will be extremely useful during development.

==================================================
77. WEB DEVELOPMENT PRIORITY CHANGE
==================================================

Update milestone priority.

NEW RECOMMENDED DEVELOPMENT ORDER:

MILESTONE 0
repository + web compatibility audit

MILESTONE 1
browser build successfully launches

MILESTONE 2
camera / selection / RTS controls in browser

MILESTONE 3
core simulation architecture

MILESTONE 4
villager + resource gathering

MILESTONE 5
buildings + production

MILESTONE 6
combat vertical slice

MILESTONE 7
General death victory condition

MILESTONE 8
King + Main Residence lifecycle

MILESTONE 9
food / Granary / logistics

MILESTONE 10
Supply Depot + Supply Wagon

MILESTONE 11
Single Player AI

MILESTONE 12
basic 2-player networking

MILESTONE 13
online room create/join

MILESTONE 14
1v1 synchronized complete match

MILESTONE 15
reconnect / disconnect handling

MILESTONE 16
historical King + General abilities

MILESTONE 17
fog / terrain / ambush

MILESTONE 18
naval systems

MILESTONE 19
two final 1v1 maps

MILESTONE 20
final 8-direction visual pipeline

MILESTONE 21
UI polish

MILESTONE 22
network/performance optimization

MILESTONE 23
public deployment

MILESTONE 24
production URL validation

MILESTONE 25
balance / bug fixing / final audit

Adapt this list according to existing implementation.

==================================================
78. WEB MVP MUST COME EARLY
==================================================

Do NOT wait until the entire game is complete before attempting browser deployment.

Very early in development create a WEB VERTICAL SLICE.

It should contain:

- browser launch
- one map
- several units
- unit selection
- movement
- simple combat

Then deploy the prototype.

This validates the architecture before hundreds of assets and systems depend on it.

Later create an ONLINE VERTICAL SLICE:

Browser A
vs
Browser B

with:

- room creation
- joining
- movement
- combat
- synchronized death

Only after this works reliably should multiplayer complexity increase.

==================================================
79. PUBLIC URL IS PART OF DEFINITION OF DONE
==================================================

The final game is NOT finished if it only works at:

localhost

or

127.0.0.1

Completion requires a real deployment accessible through HTTPS.

The final audit must test the production URL from a clean browser session.

Test:

- initial loading
- Single Player
- room creation
- join link
- 1v1 match
- disconnect
- reconnect
- victory
- rematch
- return to menu

==================================================
80. KEEP MULTIPLAYER SIMPLE
==================================================

IMPORTANT DESIGN CONSTRAINT:

MULTIPLAYER IS ONLY TWO HUMAN PLAYERS.

Whenever choosing between:

A complex generic multiplayer system

and

a much simpler robust 1v1 implementation

CHOOSE THE SIMPLE ROBUST 1v1 IMPLEMENTATION.

Avoid speculative architecture.

Do not implement features merely because other RTS games have them.

We need:

excellent 1v1

NOT:

unfinished 8-player multiplayer.