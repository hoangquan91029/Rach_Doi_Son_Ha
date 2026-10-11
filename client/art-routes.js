/** BareURL selects only realistic stone fortifications. Unknown explicit art routes stay disabled. */
export const ART_ROUTES = Object.freeze({
 stone:Object.freeze({manifestUrl:'/assets/art-v1/stone-361-manifest.json',world:false}),
 pilot:Object.freeze({manifestUrl:'/assets/art-v1/manifest.json',world:false}),
 walk:Object.freeze({manifestUrl:'/assets/art-v1/walk-014-manifest.json',world:false}),
 food:Object.freeze({manifestUrl:'/assets/art-v1/food-099-manifest.json',world:false}),
 work:Object.freeze({manifestUrl:'/assets/art-v1/gather-026-manifest.json',world:false}),
 terrain:Object.freeze({manifestUrl:'/assets/art-v1/terrain-127-manifest.json',world:true}),
 iron:Object.freeze({manifestUrl:'/assets/art-v1/iron-137-manifest.json',world:true}),
 workshop:Object.freeze({manifestUrl:'/assets/art-v1/workshop-144-manifest.json',world:true}),
 camp:Object.freeze({manifestUrl:'/assets/art-v1/camp-148-manifest.json',world:true}),
 shipyard:Object.freeze({manifestUrl:'/assets/art-v1/shipyard-165-manifest.json',world:true}),
 fort:Object.freeze({manifestUrl:'/assets/art-v1/fort-202-manifest.json',world:true})
});
export function artRoute(search=globalThis.location?.search||''){
 const params=new URLSearchParams(search),name=params.has('art')?params.get('art'):'stone';
 const recipe=Object.hasOwn(ART_ROUTES,name)?ART_ROUTES[name]:null;
 return {name,enabled:Boolean(recipe),manifestUrl:recipe?.manifestUrl||ART_ROUTES.pilot.manifestUrl,world:recipe?.world||false};
}
