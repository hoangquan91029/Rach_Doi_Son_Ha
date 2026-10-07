==================================================
115. FRAME-BY-FRAME SPRITE ANIMATION IS THE
MANDATORY FINAL CHARACTER ANIMATION STYLE
==================================================

HARD REQUIREMENT:

All visible character/unit animation must use:

FRAME-BY-FRAME 2D SPRITE ANIMATION

The intended visual principle is similar to:

traditional cel animation
comic-book panels
flipbook animation

Each frame is a complete illustrated image of the character at a specific moment.

When these images are played sequentially:

FRAME 01
FRAME 02
FRAME 03
FRAME 04
...

the character appears to move.

THIS IS THE REQUIRED FINAL VISUAL METHOD.

Do NOT use visible runtime skeletal animation as the primary final character style.

Do NOT make the player see a character constructed from:

head sprite
torso sprite
upper leg sprite
lower leg sprite
arm sprite

rotating independently like a paper puppet.

That is not the desired aesthetic.

The final rendered character must look like a complete illustrated sprite in every frame.

==================================================
116. IMPORTANT DISTINCTION:
AUTHORING METHOD VS FINAL OUTPUT
==================================================

Internal production tools MAY use:

- 2D rigs
- pose skeletons
- stick figures
- 3D models
- mannequins
- IK
- bone systems
- pose guides

BUT ONLY AS AUTHORING TOOLS.

They may be used to guarantee:

- anatomy
- foot placement
- weapon consistency
- perspective
- direction
- body rotation
- animation timing

Afterward:

BAKE / RENDER / REDRAW

the result into finished 2D sprite frames.

The final game should consume finished frame animation.

Conceptually:

INTERNAL RIG / POSE GUIDE
        ↓
KEY POSE
        ↓
FINISHED ILLUSTRATED FRAME
        ↓
SPRITE SEQUENCE
        ↓
TEXTURE ATLAS
        ↓
WEB GAME

The internal rig is NOT the final visual product.

==================================================
117. DO NOT CONTINUE THE CURRENT UNCONTROLLED
"ONE PROMPT = ONE PNG" METHOD
==================================================

The previous workflow has repeatedly failed to correctly alternate the supporting leg.

Therefore:

STOP generating every animation frame independently from text.

Forbidden workflow:

prompt:
"villager walking frame 1"

then independently:

"villager walking frame 2"

then independently:

"villager walking frame 3"

This causes:

- left/right leg confusion
- support-leg failure
- identity drift
- clothing changes
- weapon changes
- body proportion changes
- camera changes
- lighting changes

Instead use a CONTROLLED SEQUENCE WORKFLOW.

==================================================
118. CANONICAL CHARACTER IDENTITY
==================================================

Before animating any unit:

create a CANONICAL CHARACTER MASTER.

The master defines:

- exact face
- body proportions
- height
- clothing
- armor
- hairstyle
- headgear
- footwear
- weapon
- equipment
- palette
- lighting
- camera perspective
- sprite scale

Create an eight-direction turnaround:

N
NE
E
SE
S
SW
W
NW

These images are the CHARACTER IDENTITY LOCK.

Every animation frame must preserve this identity.

Do not redesign the character while animating it.

==================================================
119. FRAME CONTINUITY RULE
==================================================

Every new animation frame must be derived from:

1. canonical character reference
2. previous frame
3. next key pose when available
4. animation pose specification

Do NOT generate a frame from text alone.

For frame N:

REFERENCE:

canonical identity
+
frame N-1
+
target keyframe N+X when applicable

Then produce frame N.

This should behave more like an animator drawing an in-between frame than an image generator inventing a new character.

==================================================
120. WALK CYCLE MUST USE EXPLICIT LEG PHASES
==================================================

The supporting-leg problem must be solved structurally.

Every walking cycle MUST explicitly define:

LEFT LEG
RIGHT LEG

and exactly which leg:

- supports body weight
- moves forward
- moves backward
- passes the other leg
- contacts the ground

Do not rely on the image model to infer this.

Use a standard eight-phase walking cycle.

FRAME 0
LEFT CONTACT

Left foot:
forward
contacts ground

Right foot:
behind

FRAME 1
LEFT DOWN / WEIGHT ACCEPTANCE

Left leg:
SUPPORT LEG

Right heel:
lifting

FRAME 2
RIGHT PASSING

Left leg:
SUPPORT LEG

Right leg:
passes underneath body

FRAME 3
LEFT UP / PUSH

Left leg:
finishing support

Right leg:
moving forward

FRAME 4
RIGHT CONTACT

Right foot:
forward
contacts ground

Left foot:
behind

FRAME 5
RIGHT DOWN / WEIGHT ACCEPTANCE

Right leg:
SUPPORT LEG

Left heel:
lifting

FRAME 6
LEFT PASSING

Right leg:
SUPPORT LEG

Left leg:
passes underneath body

FRAME 7
RIGHT UP / PUSH

Right leg:
finishing support

Left leg:
moving forward

LOOP BACK TO FRAME 0.

Mandatory invariant:

FRAME 0 and FRAME 4 must NOT have the same supporting leg.

Frames 0–3 belong primarily to one half-cycle.

Frames 4–7 must be the complementary half-cycle.

==================================================
121. WALK CYCLE VALIDATION
==================================================

Before accepting a walk animation:

inspect it as a contact sheet:

F0 F1 F2 F3 F4 F5 F6 F7

Explicitly label under each frame:

SUPPORT:
LEFT

or

SUPPORT:
RIGHT

Also label:

SWING:
LEFT

or

SWING:
RIGHT

If the support leg does not alternate correctly:

REJECT THE ENTIRE WALK CYCLE.

Do not attempt to hide the error by increasing playback speed.

==================================================
122. TEMPORARY LEG DEBUG MARKERS
==================================================

During animation production ONLY:

the agent may create temporary debug overlays.

For example:

LEFT LEG = L
RIGHT LEG = R

or use temporary distinct debugging markers.

These debug markers exist only in animation QA/reference images.

They MUST NOT appear in final sprites.

The purpose is to prevent the image model from accidentally swapping limbs.

==================================================
123. KEYFRAME-FIRST PRODUCTION
==================================================

Do not immediately generate every frame.

For each animation:

FIRST AUTHOR KEYFRAMES.

Example WALK:

KEY A
Left Contact

KEY B
Right Passing

KEY C
Right Contact

KEY D
Left Passing

Validate these first.

Only after they are correct:

generate intermediate frames.

Workflow:

KEYFRAMES
    ↓
POSE VALIDATION
    ↓
IN-BETWEEN FRAMES
    ↓
CONTACT SHEET
    ↓
LOOP PREVIEW
    ↓
CORRECTION
    ↓
FINAL SPRITES

==================================================
124. IN-BETWEEN FRAME METHOD
==================================================

Generate in-between frames based on TWO neighboring poses whenever possible.

Example:

KEYFRAME A
        ↓
INBETWEEN 1
        ↓
INBETWEEN 2
        ↓
KEYFRAME B

The model must understand:

start pose
end pose
motion direction

rather than inventing an arbitrary intermediate pose.

Preserve:

- anatomy
- clothing
- weapon
- accessories
- light
- perspective

==================================================
125. DO NOT FORCE EVERY ANIMATION TO USE
THE SAME NUMBER OF FRAMES
==================================================

Different animations may require different frame counts.

Suggested starting targets for RTS gameplay:

IDLE
4–8 frames

WALK
8–12 frames

RUN
8–12 frames

MELEE ATTACK
8–14 frames

SPEAR ATTACK
8–14 frames

FIREARM ATTACK
8–16 frames

RELOAD
10–20 frames

HIT
3–6 frames

DEATH
8–16 frames

GATHER
6–12 frames

BUILD
6–12 frames

CARRY
8–12 frames

These are starting ranges.

Adjust based on visual quality.

Do NOT generate unnecessary frames simply to hit a large number.

Strong poses and good timing matter more.

==================================================
126. GAME FPS != ANIMATION FPS
==================================================

The browser may render at:

60 FPS
120 FPS
or another display refresh rate.

Sprite animation does NOT need one new painted image for every rendered frame.

Example:

GAME RENDER:
60 FPS

WALK ANIMATION:
12 FPS

ATTACK ANIMATION:
16 FPS

The renderer displays each painted sprite frame for the appropriate duration.

This dramatically reduces:

- asset count
- memory
- download size
- production time

while maintaining a high-quality illustrated appearance.

==================================================
127. ANIMATION TIMING
==================================================

Do not play every animation at identical frame duration.

Support timing metadata.

Example:

walk_contact:
80 ms

walk_down:
70 ms

walk_pass:
80 ms

walk_up:
70 ms

Attack animation may use:

anticipation
slower

strike
fast

impact
brief hold

recovery
slower

This produces much better animation than mechanically cycling PNG files at identical speed.

==================================================
128. EIGHT DIRECTION REQUIREMENT
==================================================

Primary gameplay characters use:

8 DIRECTIONS

N
NE
E
SE
S
SW
W
NW

Do NOT require 32 directions for this project.

Eight directions are an intentional balance between:

- visual quality
- production cost
- download size
- animation workload
- web performance

But every direction must look polished.

==================================================
129. DIRECTION PRODUCTION ORDER
==================================================

Do not generate all eight directions simultaneously at first.

For each new unit:

STEP 1
finish SOUTH walking animation

STEP 2
validate animation pipeline

STEP 3
finish EAST

STEP 4
finish NORTH

STEP 5
finish diagonals

Only after the first directions are good:

scale to all eight directions.

This prevents multiplying a broken animation workflow eight times.

==================================================
130. MIRRORING POLICY
==================================================

Mirroring may be used ONLY when visually valid.

For generic symmetrical units:

E and W may sometimes share mirrored animation.

NE/NW
SE/SW

may sometimes be mirrored.

BUT:

do NOT mirror when it causes incorrect:

- shield hand
- weapon hand
- asymmetric armor
- clothing
- banners
- scabbards
- historical equipment

Kings and Generals should receive special scrutiny.

If mirroring damages historical identity:

create the real direction.

==================================================
131. FRAME-BY-FRAME COMIC QUALITY
==================================================

Each frame should be visually strong enough that:

if paused,

it still resembles a finished historical illustration.

The desired impression is:

"animated illustrated historical RTS"

not:

"bone puppet"

and not:

"3D character disguised with an outline shader."

Frames may have a slightly hand-painted / illustrated quality,
as long as all units remain readable at normal RTS zoom.

==================================================
132. SILHOUETTE IS MORE IMPORTANT THAN
TINY DETAIL
==================================================

Remember that RTS units are viewed from a distance.

Prioritize:

- posture
- weapon
- helmet
- clothing outline
- horse shape
- banner
- movement

over tiny details that disappear at normal camera zoom.

Every class should remain recognizable by silhouette.

==================================================
133. FRAME CONSISTENCY TEST
==================================================

Create a contact sheet for every completed animation.

Example:

WALK SOUTH

F0 | F1 | F2 | F3
F4 | F5 | F6 | F7

Review at:

100%
50%
actual in-game scale

Check:

- head size
- shoulder width
- torso length
- leg length
- weapon size
- clothing
- lighting
- ground position

If the character appears to:

grow
shrink
change outfit
change weapon
change body

the sequence fails.

==================================================
134. PIVOT LOCK
==================================================

All animation frames must share a stable ground pivot.

Recommended conceptual point:

between the feet on the ground plane.

Do not center every frame by image bounding box.

Otherwise walking may cause the character to visually:

jump
slide
shake
float

even if the drawings themselves are correct.

Store explicit pivot metadata where necessary.

==================================================
135. FOOT SLIDING TEST
==================================================

When a foot is the SUPPORT FOOT:

it should remain approximately planted relative to the ground until push-off.

Do not allow the support foot to slide backward while the body is supposedly standing on it.

Preview animation over a grid.

If planted feet slide noticeably:

fix the frames or movement timing.

==================================================
136. ROOT MOTION POLICY
==================================================

The sprite animation should primarily represent body motion.

Actual world movement is controlled by game simulation.

Do not bake large world translation into sprite frames.

Animation:

legs move
body bobs
clothes move

Simulation:

unit changes world position

This avoids double movement.

==================================================
137. SPRITE SOURCE VS RUNTIME FORMAT
==================================================

Keep high-quality individual source frames during production.

Example:

villager/
    walk/
        south/
            000.png
            001.png
            002.png
            ...
        southeast/
        east/
        ...

These are MASTER ART SOURCES.

For runtime web deployment:

pack frames into:

SPRITE SHEETS
or
TEXTURE ATLASES

where technically appropriate.

Do not issue hundreds of independent network requests for individual tiny PNGs during gameplay.

AUTHORING FORMAT and RUNTIME FORMAT are different concerns.

==================================================
138. TEXTURE ATLAS PIPELINE
==================================================

Build an automated atlas pipeline.

INPUT:

individual high-quality animation frames

OUTPUT:

optimized runtime atlas
+
animation metadata

Metadata should contain:

- animation name
- direction
- frame index
- frame rectangle
- pivot
- duration
- event markers

Do not manually hard-code atlas coordinates.

==================================================
139. ANIMATION EVENTS
==================================================

Gameplay must not assume:

"damage happens when animation begins."

Support animation events.

Examples:

MELEE ATTACK:

FRAME 0
anticipation

FRAME 4
weapon contact

EVENT:
DEAL_DAMAGE

FIREARM:

FRAME 3

EVENT:
FIRE_PROJECTILE

EVENT:
MUZZLE_FLASH

SUPPLY WAGON:

specific loading frame

EVENT:
TRANSFER_RESOURCE

This keeps visual timing synchronized with gameplay.

==================================================
140. VISUAL ANIMATION MUST NOT CONTROL
AUTHORITATIVE MULTIPLAYER STATE
==================================================

Important for online 1v1:

animation is a VISUAL REPRESENTATION
of authoritative simulation.

Do not allow different browser animation FPS to alter:

- damage
- movement distance
- food consumption
- victory
- resource gathering

Simulation remains fixed-tick.

Animation follows simulation.

==================================================
141. HISTORICAL LEADER ANIMATION
==================================================

Kings and Generals should receive higher-quality frame sequences.

At minimum support:

IDLE
WALK
ATTACK where appropriate
HIT
DEATH
ABILITY / COMMAND

Optional:

COMMANDING
POINTING
RALLYING
MOUNTED

These animations should communicate personality.

Example:

Nguyễn Huệ:
decisive forward motion

Trần Hưng Đạo:
controlled command posture

Xiang Yu:
heavy aggressive movement

Han Xin:
command/deployment emphasis

Napoleon:
command gesture / battlefield observation

Do not make every commander reuse exactly the same animation personality.

==================================================
142. VILLAGER ANIMATION PIPELINE RESTART
==================================================

The current villager walking animation has failed the supporting-leg test.

DO NOT continue producing additional villager frames using the same failed method.

Restart the walk animation using:

CANONICAL IDENTITY
+
EXPLICIT LEFT/RIGHT LEG LABELS
+
4 KEY POSES
+
8-FRAME TEST CYCLE
+
CONTACT SHEET
+
LOOP PREVIEW

Only after the SOUTH-direction walk passes:

SUPPORT-LEG ALTERNATION
FOOT-SLIDE
IDENTITY
PIVOT

tests may production continue.

==================================================
143. FIRST REQUIRED WALK PROTOTYPE
==================================================

Create exactly ONE validated animation first:

VILLAGER
WALK
SOUTH
8 FRAMES

Required order:

F0 LEFT CONTACT
F1 LEFT SUPPORT / DOWN
F2 LEFT SUPPORT / RIGHT PASSING
F3 LEFT PUSH / RIGHT FORWARD

F4 RIGHT CONTACT
F5 RIGHT SUPPORT / DOWN
F6 RIGHT SUPPORT / LEFT PASSING
F7 RIGHT PUSH / LEFT FORWARD

Preview:

F0 → F1 → F2 → F3 →
F4 → F5 → F6 → F7 →
F0

Do NOT proceed to the other seven directions until this loop clearly works.

==================================================
144. ANIMATION AUDIT GATE
==================================================

The parent model must visually audit animation before scale-up.

For every prototype assign:

IDENTITY CONSISTENCY: /10
ANATOMY: /10
LEG PHASE: /10
FOOT PLACEMENT: /10
MOTION READABILITY: /10
ART QUALITY: /10
LOOP QUALITY: /10
RTS READABILITY: /10

Any score below 8/10:

REQUIRES REWORK.

Leg Phase below 10/10:

AUTOMATIC REJECTION.

Supporting-leg correctness is binary.

It is either correct or incorrect.

==================================================
145. FINAL ANIMATION PRINCIPLE
==================================================

The goal is NOT to minimize the number of images.

The goal is to produce:

BEAUTIFUL
CONSISTENT
READABLE
FRAME-BY-FRAME
HISTORICAL RTS ANIMATION.

Think:

"illustrations coming alive"

rather than:

"parts of a puppet being rotated."

If an internal rig helps produce correct frames:

use it internally.

If a 3D pose guide helps:

use it internally.

But the final visible animation remains:

A SEQUENCE OF FINISHED 2D ILLUSTRATED FRAMES.