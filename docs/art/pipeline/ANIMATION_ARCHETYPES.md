# Motion archetypes — version1 design

These are reusable specifications, **not qualified motion clips**. Store measured per-view landmarks/contact coordinates with the actual job; do not fabricate a universal skeleton or claim one2D view projects into eight finished images. The machine-readable library below is planning data until P2 binds actualposes.

| Archetype | Members | Movement / action-specific constraints |
|---|---|---|
|HUMANOID_GENERIC|Villager, infantry|Two physicalleg contacts alternate; stance foot countersroottravel; torso/arms counter-swing; infantry shield/sword ownership fixed|
|HUMANOID_SPEAR|Spearman|Same walking phase schema, different arm grip/shaftclearance; thrust/contact/recovery, no inventedbraceaction|
|HUMANOID_FIREARM|Firearm|Weaponweight and persistentgrip; aim→fire→recoil→reloadwithinattack; no independent reload bank|
|COMMANDER|12historicalidentities|Sameperson acrossroles, costume/weapon-specificmotion; distinctabilitypose; Kingbuild usesrealgameplayevent|
|CAVALRY|Horse+rider|Four-hoof gait, diagonal/lateral pairing chosenfromactualgait, rider/pelvisweight and reins coherent; no humanwalk transplant|
|ARTILLERY_CREW|Artillery|Currentwholegun/crewifpresent; wheelprogress whilemoving; fire/recoil/recovery. Do not inventcrew missingfromcanonicalart|
|SUPPLY_WAGON|Whole415|Horse/harness/cart/cargo together; fourhooves, harness tension, wheels with traveleddistance; load/unload authoredwholeposes|
|SHIP|Transport447, separatewarshipidentity|Hull/water/sail/crew ifpresent; no footcadence. Move/attack orload/unload pertype; hit/sink distinctive|

## Humanoid walk key recipe

F0contactA →F1acceptA →F2BpassingA →F3Breach →F4contactB →F5acceptB →F6ApassingB →F7Areach. Contacttransition may have doublesupport; labelreceivingfoot separatelyfromsupport. Persistphysical A/B landmark throughocclusion. Screenleft/right is only viewdescription, never identity.

Perframe: phase, receiving/support/swing limb, groundcontact interval, footlane, pelvis/shoulderintent, toolgrip, nextkey, occlusionorder. Amplitudes come fromactualunit atgameplayzoom, not arbitrary sharedpixelcoordinates.

Other recipes: attack preparation/contact/recovery; work ready/impact/followthrough/recovery; death lossbalance/fall/contact/rest; load/unload and ability enter/mainoperation/recover. Natural motion can reuse these phase graphs, but actualposes/framecounts/eventpositions must bind simulation behavior. No generic horse/spear/ship key created before itscanonical view is selected.

[motion-archetypes.json](motion-archetypes.json) stores these planning phases/projection labels with status PROPOSED_NOT_QUALIFIED and no qualifiedSource. Current runtime/order dispatcher does not consume it yet; P2 supplies measured bindings before reuse is claimed.
