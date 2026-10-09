/** Existing opt-in preview recipes only. The unqueried/unknown default stays disabled. */
export const ART_ROUTES = Object.freeze({
 pilot:Object.freeze({manifestUrl:'/assets/art-v1/manifest.json',world:false}),
 walk:Object.freeze({manifestUrl:'/assets/art-v1/walk-014-manifest.json',world:false}),
 work:Object.freeze({manifestUrl:'/assets/art-v1/gather-026-manifest.json',world:false}),
 food:Object.freeze({manifestUrl:'/assets/art-v1/food-099-manifest.json',world:false}),
 terrain:Object.freeze({manifestUrl:'/assets/art-v1/terrain-127-manifest.json',world:true}),
 iron:Object.freeze({manifestUrl:'/assets/art-v1/iron-137-manifest.json',world:true}),
 workshop:Object.freeze({manifestUrl:'/assets/art-v1/workshop-144-manifest.json',world:true}),
 camp:Object.freeze({manifestUrl:'/assets/art-v1/camp-148-manifest.json',world:true}),
 shipyard:Object.freeze({manifestUrl:'/assets/art-v1/shipyard-165-manifest.json',world:true})
});
export function artRoute(search=globalThis.location?.search||''){
 const name=new URLSearchParams(search).get('art');
 const recipe=Object.hasOwn(ART_ROUTES,name)?ART_ROUTES[name]:null;
 return {name,enabled:Boolean(recipe),manifestUrl:recipe?.manifestUrl||ART_ROUTES.pilot.manifestUrl,world:recipe?.world||false};
}
