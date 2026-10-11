import {TILE_WIDTH, TILE_HEIGHT} from './world-presentation.js';

// Ground-plane footprint of the screen, in perimeter order. Use CSS pixels,
// matching IsoRenderer.project; device pixel ratio must not enlarge this area.
export function cameraGroundCorners(camera, width, height) {
 const dx=width/(TILE_WIDTH*camera.zoom),dy=height/(TILE_HEIGHT*camera.zoom);
 return [[-dx,-dy],[dx,-dy],[dx,dy],[-dx,dy]].map(([x,y])=>({
  x:camera.x+(x+y)/2,y:camera.y+(y-x)/2
 }));
}
