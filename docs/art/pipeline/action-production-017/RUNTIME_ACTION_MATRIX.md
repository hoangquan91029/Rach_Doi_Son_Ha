# Action templates and real game state mapping

This matrix comes from current shared/sim.js, shared/data.js and client/raster-slice.js. It describes production scope, not completed artwork. Every source remains a whole finished 2D illustration with a fixed family canvas, pivot, scale and camera. A generic exporter accepting an action name does not mean the game already selects that action.

| Group | Real current states | Artwork needed / reusable planning |
| --- | --- | --- |
| Villager | idle, walk, gather, carry, build, attack; hit overlay; death | Shared human walk/contact planning. Gathering needs distinct wood, food and iron tools/poses. Build includes repair. Carry currently appears at resource unload, while movement uses walk; meaningful carried-load presentation still needs a mapping. |
| King | idle, walk, build, attack; hit; death | Human timing/export tools; separate leader identity, historical outfit and abilities. Construction/repair appears as build. |
| General and infantry/spearman/firearm | idle, walk, attack; hit; death | Human pose templates, separate weapons/outfits and attack contacts. Firearm reload is currently part of the attack/recovery timing, not a separate authoritative state. |
| Cavalry | idle, walk, attack; hit; death | Own horse/rider anatomy and motion template; reuse export, timing, custody and preview tools. |
| Supply Wagon | idle, walk, carry while loading; hit; death | Own wheel/body/load template. No combat attack state because damage is zero. |
| Artillery | idle, walk, attack; hit; death | Own crew/wheel/recoil template and authoritative projectile contact. |
| Warship | idle, walk, attack; hit; death | Own vessel/water-motion template; exporter is shared, human gait is not. |
| Transport | idle, walk; hit; death | Own vessel/loading presentation. Embarked units are not individually rendered. No combat attack state because damage is zero. |

The renderer currently supports raster families for villager, infantry, cavalry and the Trần Hưng Đạo General, plus selected buildings. Kings, other Generals, spear/firearm/artillery/wagon/ships need explicit raster-family routing when their actual art is produced. Do not claim a complete roster from the new exporter.

Actual illustrations currently available for the new pipeline: one South/D1 eight-frame villager walk014 and its matching single-frame canonical idle. Other states and directional animations remain open. The static eight-direction identity seal is a reference set, not eight animated directions.

Upcoming resource-specific work mapping must use visible public action information consistent with authoritative simulation. Do not infer an enemy's private order target or make cosmetic markers decide resources, damage or victory. Current hit/death timing uses hitUntil/deadTick; attack contact uses authoritative start/impact/recovery ticks. Cosmetic markers stay cosmetic.

Frame count and timing are chosen for each action, rather than forcing every action into eight frames. Walk remains eight frames for the first pilot; death is nonlooping and holds its last pose. Do not relabel the existing walk as hit/death to invent finished actions. One brief gameplay-size loop look and a fix of visible problems are sufficient under the latest human review priority; tiny cloth/pixel differences do not block production.
