# Art direction — immutable identity, readable motion

Final style: realistic illustrated whole2D matching existing artwork. Preserve face, body volume, age, costume, palette, headwear, sash, equipment and physical weapon hands. Motion may shift weight, bend the torso and move cloth naturally; locking the torso rigid is not identity preservation. No generic geometric units as accepted final art.

The identity registry `pipeline/unit-production/<identity>/identity.json` pins masters/views/layout/exclusions. Original infantry084845…0517f remains sole identity. Wagon415 is the complete horse/harness/cart/cargo ensemble. Spear/firearm/cavalry/artillery/transport originals were recovered485; do not redesign them. Missing warship/leader identities need historical source/identity work, not a reused portrait on another body. Preserve supplied historical dossier and source custody.

## Camera and screen contract

Source `client/world-presentation.js`: tile54×27, dimetric2:1, nominal elevation26.565°, defaultzoom1.68. Actual source painting is the reference for perceived camera/light; numeric metadata does not prove a painting exactly matches that elevation.

| Engine direction | World vector | Projected label |
|---|---|---|
|D0|(1,0)|ESE|
|D1|(1,1)|South|
|D2|(0,1)|WSW|
|D3|(-1,1)|West|
|D4|(-1,0)|WNW|
|D5|(-1,-1)|North|
|D6|(0,-1)|ENE|
|D7|(1,-1)|East|

Normalize vectors when measuring distance; they label world octants, not anatomical sides. Project `(x,y)` as `(27(x-y),13.5(x+y))`. Never relabel a source to satisfy a runtime check. No mirrored directions.

## Scale, canvas and shadow

Use existing identity.layoutLock, one whole-canvas transform per family, and fixed source pivot. Infantry source1254²/pivot(653,1057), runtime128²/logicalrender42²:70.56px canvas at defaultzoom. Villager/other family sizes come from their own locks; old preview89px is not current universal presentation size. Measure alpha/body height separately, excluding weapon/hat if reporting torso height; record the definition.

Raw originals remain full resolution for custody; working256 and runtime128 are independently derived from raw, not chained resampling. The tool may return1254px; do not invest in invisible microtexture. A256working character fits current small presentation with editing margin;128runtime is above the typical64–96px displayed body envelope. It is not permission to downscale a horse into a humanoid silhouette.

Long weapons, horses, wagons and hulls may need a larger or rectangular family envelope. Current compiler only supports square128. First measure clipping in the full action; then version the layout and extend tests before adopting it. Do not crop gear or fit frames separately. Preserve baked/separate shadow locks; do not add a second shadow to baked art.

World art policy remains stone walls, wooden gates; other wooden buildings/resources stay. Draw natural weight, clear stance and broad material/color differences. Tiny vein/skin/fold polishing is lowest priority. One gameplay-size loop, correct visible problems, then continue.
