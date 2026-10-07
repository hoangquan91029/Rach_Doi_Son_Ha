==================================================
82. VISUAL QUALITY IS A HARD REQUIREMENT
==================================================

NON-NEGOTIABLE REQUIREMENT:

THE FINAL GAME MUST LOOK BEAUTIFUL.

This project must NOT visually resemble:

- a programming prototype
- a debug visualization
- a student assignment using primitive shapes
- rectangles representing buildings
- circles representing soldiers
- colored capsules representing units
- cubes assembled into fake architecture
- geometric blocks pretending to be historical buildings
- placeholder silhouettes used as final assets
- flat programmer art
- random AI-generated sprites with inconsistent styles

DO NOT treat graphics as secondary to gameplay.

VISUAL QUALITY IS ONE OF THE CORE PRODUCT REQUIREMENTS.

The final game should immediately look like a real polished historical RTS.

==================================================
83. NO PRIMITIVE-SHAPE FINAL ART
==================================================

Primitive geometry may ONLY be used internally for:

- collision boxes
- navigation
- debugging
- pathfinding visualization
- temporary development diagnostics
- invisible gameplay hitboxes

Primitive shapes must NOT appear as final visible artwork.

FORBIDDEN FINAL VISUAL EXAMPLES:

Soldier =
red circle

Cavalry =
large triangle

King =
yellow square

Tree =
green circle + brown rectangle

House =
rectangle + triangle roof

Fortress =
several gray cubes

Mountain =
stacked polygons with no artwork

Ship =
brown rectangle floating on water

Supply Wagon =
box + two circles

These are unacceptable.

If such placeholders are temporarily required during development,
they must be explicitly tagged:

PLACEHOLDER_ONLY

and must be replaced before that milestone passes visual acceptance.

==================================================
84. VISUAL ACCEPTANCE GATE
==================================================

A milestone is NOT visually complete merely because:

- the sprite exists
- an image loads
- the unit is recognizable
- the animation technically works

Every final visual asset must pass a VISUAL QUALITY REVIEW.

Evaluate:

- silhouette
- anatomy
- historical character
- material readability
- lighting
- shading
- texture detail
- perspective
- scale consistency
- animation quality
- color harmony
- faction readability
- environment integration
- UI readability
- professional polish

If an asset looks cheap, generic, inconsistent, unfinished or obviously generated:

REJECT IT.

Regenerate or manually refine it.

==================================================
85. TARGET VISUAL IMPRESSION
==================================================

The visual target is:

BEAUTIFUL
POLISHED
HISTORICAL
ATMOSPHERIC
READABLE
TACTICAL
COHESIVE

The game should visually evoke the quality expectations of polished 2.5D RTS games.

Age of Empires can be used as a reference for:

- readability
- scale hierarchy
- unit clarity
- building readability
- terrain composition
- battlefield density

BUT:

Do NOT copy copyrighted Age of Empires artwork.

Create an original visual identity.

==================================================
86. ART DIRECTION BEFORE MASS ASSET CREATION
==================================================

Before generating hundreds of assets:

CREATE AN ART DIRECTION BIBLE.

Document:

1. camera perspective
2. world scale
3. unit scale
4. building scale
5. sprite dimensions
6. lighting direction
7. shadow direction
8. color palette
9. material rendering
10. terrain style
11. architectural language
12. character rendering style
13. water rendering
14. vegetation style
15. VFX style
16. UI visual language
17. icon style
18. portrait style

Save as:

docs/ART_DIRECTION.md

All Luna visual subagents MUST read and follow this document.

Do not allow every subagent to independently invent a different style.

==================================================
87. HISTORICAL CHARACTER ART QUALITY
==================================================

Kings and generals are PREMIUM ASSETS.

They must receive significantly more attention than generic soldiers.

Each King/General should have:

- recognizable silhouette
- historically inspired clothing
- historically appropriate armor where applicable
- distinctive headwear
- distinctive weapon or symbolic object
- unique palette accents
- unique portrait
- high-quality selection icon
- readable in-game sprite
- polished animation
- eight directional views

Avoid making every Asian historical character wear the same generic fantasy armor.

Avoid generic:

"Chinese warrior"
"samurai-like armor"
"fantasy emperor"
"European knight"

when those designs are historically inappropriate.

The art team must inspect historical references before designing characters.

==================================================
88. 8-DIRECTION CHARACTER QUALITY
==================================================

Eight-direction sprites must look like actual views of the SAME CHARACTER.

Required consistency:

N
NE
E
SE
S
SW
W
NW

Check:

- clothing consistency
- armor consistency
- weapon location
- body proportions
- headgear
- color
- lighting
- scale
- equipment

AI generation sometimes changes details between directions.

THIS IS NOT ACCEPTABLE.

If one direction has:

a spear

and another suddenly has:

a sword

without gameplay reason:

the asset fails review.

==================================================
89. ANIMATION QUALITY
==================================================

Animations must not merely change frames.

They need:

- believable weight
- anticipation
- impact
- readable action
- consistent timing
- clean foot placement
- weapon continuity
- proper direction
- good silhouettes

For example:

CAVALRY

must show:

- horse gait
- rider movement
- momentum
- attack follow-through

not simply:

"static horse image moving across screen."

INFANTRY:

walking must show actual locomotion.

ATTACK:

must have readable attack preparation and impact.

DEATH:

must not look like the sprite simply disappears.

==================================================
90. BUILDING QUALITY
==================================================

Buildings must look like real architecture.

Do NOT create them by visibly stacking generic geometry.

Each structure needs:

- foundation
- walls
- roof
- doors
- structural detail
- material variation
- shadows
- wear
- functional visual elements

Examples:

BARRACKS
should visually communicate a military compound.

ARTILLERY WORKSHOP
should show craft/forge/artillery-related details.

SHIPYARD
should clearly interact with the shoreline.

GRANARY
should visually read as food storage.

SUPPLY DEPOT
should contain visible logistical elements such as:
- sacks
- crates
- carts
- covered storage
- loading area

FORTRESS
must feel substantial and defensible.

MAIN RESIDENCE
must visually communicate political importance.

==================================================
91. ERA / CULTURE ARCHITECTURE
==================================================

Avoid building one generic Asian house and reusing it for everything.

Where feasible, architecture should reflect:

- culture
- historical period
- faction identity
- climate
- strategic function

However:

game readability remains more important than museum-level architectural reconstruction.

Use historical research to create plausible, recognizable architecture.

==================================================
92. TERRAIN MUST BE BEAUTIFUL
==================================================

Terrain must NEVER look like:

green rectangle = grass
blue rectangle = water
brown rectangle = dirt

Terrain should have:

- texture variation
- natural transitions
- terrain decals
- rocks
- vegetation
- grass variation
- shoreline detail
- dirt roads
- erosion
- cliffs
- terrain blending
- environmental storytelling

A screenshot of the map with no units should still look attractive.

==================================================
93. FORESTS
==================================================

Forests must not look like repeated identical tree stamps.

Use variation in:

- species
- size
- rotation
- density
- canopy
- undergrowth
- fallen branches
- rocks

Forests still need excellent gameplay readability.

Player must understand:

FOREST BOUNDARY
PASSABLE AREA
BLOCKED AREA
AMBUSH AREA

without sacrificing visual beauty.

==================================================
94. MOUNTAINS AND HILLS
==================================================

Mountains must look like geographic terrain,
not giant triangles.

Use:

- cliffs
- rock faces
- elevation transitions
- vegetation changes
- erosion
- shadow
- layered silhouettes

Mountains should help frame the map visually while also creating strategic barriers.

==================================================
95. WATER QUALITY
==================================================

Sea and rivers are important to this game.

Water must receive significant visual attention.

Include where technically appropriate:

- animated water surface
- shoreline foam
- shallow-water transition
- waves
- reflected light
- wake trails
- ship movement effects
- river current cues
- environmental variation

Avoid excessive effects that reduce RTS readability.

==================================================
96. MAP COMPOSITION
==================================================

Maps must be ART-DIRECTED.

Do not simply generate terrain using noise and call it finished.

Use visual composition:

- major landmarks
- silhouettes
- sight lines
- terrain framing
- memorable river bends
- mountain ranges
- forest masses
- villages
- ruins where appropriate
- coastal forms

Each map should have recognizable locations.

Player should eventually be able to say:

"fight near that mountain pass"

or

"ambush at that river bend"

rather than every location looking interchangeable.

==================================================
97. ENVIRONMENTAL DETAIL
==================================================

Add tasteful environmental props:

- rocks
- shrubs
- grass
- fallen logs
- reeds
- docks
- carts
- crates
- barrels where historically/contextually appropriate
- bridges
- fishing structures
- small paths
- farmland
- fences
- banners
- damaged structures
- battlefield debris

Do NOT overcrowd the map.

Gameplay information must remain readable.

==================================================
98. VFX QUALITY
==================================================

Combat VFX should be attractive but controlled.

Examples:

FIREARMS:
- muzzle flash
- smoke
- projectile / hit effect where appropriate

ARTILLERY:
- muzzle blast
- smoke cloud
- recoil
- ground impact
- debris

MELEE:
- subtle hit effect
- weapon motion

BUILDING DAMAGE:
- smoke
- fire
- progressive visual damage where feasible

SHIPS:
- cannon effects
- splash
- wake

Avoid excessive fantasy particle spam.

This is a historical RTS.

==================================================
99. LIGHTING AND SHADOWS
==================================================

Lighting must be consistent across:

- characters
- buildings
- terrain
- props

Sprite art should follow the same primary light direction.

Use contact shadows so units do not appear to float.

Buildings must feel grounded in the environment.

Do not mix:

one sprite lit from left

with

another sprite lit from right

unless intentionally required.

==================================================
100. UNIT GROUNDING
==================================================

All units require convincing ground contact.

Use:

- contact shadows
- consistent pivots
- proper foot placement
- correct scale

No unit should look like a sticker floating above terrain.

==================================================
101. UI MUST ALSO LOOK PROFESSIONAL
==================================================

Do not create programmer UI consisting of:

plain HTML buttons
random gray boxes
unstyled text fields

as the final UI.

The UI must have a coherent historical RTS identity.

Design:

- resource panel
- unit card
- ability bar
- building menu
- production queue
- minimap frame
- King portrait
- General portrait
- alerts
- lobby
- main menu
- result screen

All should share one design language.

However:

do not sacrifice usability for decoration.

==================================================
102. WEB UI POLISH
==================================================

Because the game runs in a web browser:

the game should NOT visually resemble a normal website.

During gameplay:

UI should feel like a GAME HUD.

Avoid excessive:

website cards
generic SaaS buttons
dashboard layouts

The player should feel they launched a strategy game,
not an administration website.

==================================================
103. VISUAL HIERARCHY
==================================================

At gameplay zoom:

the player must instantly distinguish:

KING
GENERAL
VILLAGER
SPEARMAN
FIREARM INFANTRY
CAVALRY
ARTILLERY
SUPPLY WAGON

Do not depend only on tiny UI icons.

Use:

- silhouette
- equipment
- animation
- proportions
- palette accents

to communicate unit identity.

==================================================
104. KING AND GENERAL VISUAL IMPORTANCE
==================================================

Because General death causes defeat:

the General must be visually identifiable.

But do not create an enormous unrealistic character.

Use subtle markers such as:

- banner
- special base indicator
- unique silhouette
- distinctive armor
- UI marker
- command aura indicator when selected

King also needs immediate visual recognition.

==================================================
105. VISUAL CONSISTENCY OVER RAW DETAIL
==================================================

A visually consistent 8/10 asset is preferable to:

one 10/10 asset
next to
one 4/10 asset.

The whole game must look like ONE ART TEAM created it.

Visual agents must not independently introduce:

- different camera angles
- different line styles
- different proportions
- different shading models
- incompatible palettes

==================================================
106. AI ART REQUIRES CURATION
==================================================

Never assume generated artwork is automatically usable.

AI-generated images must be treated as RAW MATERIAL.

Inspect for:

- malformed anatomy
- extra limbs
- broken weapons
- asymmetric errors
- incorrect armor
- distorted hands
- duplicated objects
- strange text
- perspective errors
- inconsistent lighting
- inconsistent sprite directions
- transparent-edge artifacts

Bad generated assets must be:

REGENERATED
or
FIXED.

Do not ship obvious AI artifacts.

==================================================
107. NO FAKE DETAIL
==================================================

Do not hide bad art by:

- excessive bloom
- extreme darkness
- heavy fog
- giant particle effects
- extreme color filters

Good art must remain good when viewed clearly.

==================================================
108. VISUAL VERTICAL SLICE
==================================================

Before generating all visual assets,
create ONE HIGH-QUALITY VISUAL VERTICAL SLICE.

It must contain:

- one polished section of terrain
- forest
- water
- one beautiful building
- one villager
- one infantry unit
- one cavalry unit
- one King or General
- shadows
- movement
- combat animation
- VFX
- finished UI elements

Run it in the actual browser build.

Then capture screenshots.

Ask:

"Would a player seeing this screenshot believe this is a serious historical RTS?"

If the answer is NO:

DO NOT scale asset production yet.

Improve the art direction first.

==================================================
109. SCREENSHOT QUALITY TEST
==================================================

At each major visual milestone:

capture screenshots from normal gameplay zoom.

Review screenshots WITHOUT looking at source code.

Check:

- Does it look attractive?
- Does the terrain look natural?
- Are units readable?
- Do buildings look professionally illustrated?
- Is the scene cohesive?
- Does lighting match?
- Is it obviously a prototype?
- Are there visible primitive placeholders?
- Would this screenshot be acceptable on a public game page?

If it still visually reads as a prototype:

THE VISUAL MILESTONE FAILS.

==================================================
110. PLACEHOLDER DEBT TRACKING
==================================================

Maintain:

docs/VISUAL_PLACEHOLDERS.md

Every temporary visual placeholder must be listed there.

For each placeholder record:

- asset
- location
- reason
- replacement requirement
- status

Before release:

VISUAL_PLACEHOLDERS.md must contain ZERO unresolved gameplay-visible placeholder assets.

==================================================
111. LUNA HIGH 6 ART RESPONSIBILITY
==================================================

GPT Luna High 6 subagents are specifically responsible for pushing visual quality.

Do not ask Luna agents merely:

"make a soldier."

Give proper art direction including:

- historical context
- camera angle
- sprite dimensions
- eight-direction requirements
- lighting
- materials
- palette
- silhouette
- animation requirements
- surrounding asset style
- existing references

Generate several candidates when necessary.

The parent/orchestrator selects the best one.

Do not automatically accept the first generation.

==================================================
112. CURRENT MODEL VISUAL AUDIT
==================================================

After each major visual production batch,
the CURRENT PARENT MODEL must perform a visual audit.

Audit:

CHARACTERS
BUILDINGS
TERRAIN
UI
ANIMATION
VFX
STYLE CONSISTENCY
HISTORICAL PLAUSIBILITY
GAMEPLAY READABILITY

Assign ratings:

1–10

Any major final asset category below:

8/10

must receive another refinement pass.

The target is not perfection,
but obviously unfinished or low-quality artwork is unacceptable.

==================================================
113. GRAPHICS ARE NOT OPTIONAL POLISH
==================================================

IMPORTANT:

Do NOT postpone all visual quality until the end.

Bad workflow:

build entire game with circles and rectangles
→ attempt to replace everything in final week

FORBIDDEN.

Instead use:

FUNCTIONAL SYSTEM
→ HIGH-QUALITY REPRESENTATIVE ART
→ VALIDATE PIPELINE
→ EXPAND SYSTEM
→ EXPAND ART

Gameplay and visuals should mature together.

==================================================
114. FINAL VISUAL DEFINITION OF DONE
==================================================

The project cannot be considered complete while any major gameplay-visible object is represented by:

- simple geometric primitive
- debug mesh
- temporary colored block
- placeholder icon
- temporary AI image
- unfinished sprite
- inconsistent animation
- visually broken generated asset

Release quality requires:

BEAUTIFUL TERRAIN

BEAUTIFUL WATER

BEAUTIFUL BUILDINGS

POLISHED HISTORICAL UNITS

POLISHED KINGS AND GENERALS

GOOD ANIMATIONS

GOOD VFX

COHESIVE UI

CONSISTENT ART DIRECTION

The game must look intentionally designed.

"FUNCTIONAL BUT UGLY"

IS NOT AN ACCEPTABLE FINAL STATE.