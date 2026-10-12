import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {ART_ROUTES,artRoute} from '../client/art-routes.js';

test('bare game selects existing 45-asset illustrated world and retains stone walls / wood gates',()=>{
 for(const search of ['', '?map=coast', '?mode=online'])assert.deepEqual(artRoute(search),{name:'fort',enabled:true,...ART_ROUTES.fort});
 const manifest=JSON.parse(readFileSync(new URL('../public'+artRoute('').manifestUrl,import.meta.url)));
 assert.equal(manifest.assets.length,45);
 for(const family of ['grass','water','forest','mountain','hill','food','iron','infantry','cavalry','villager','residence','granary','building.barracks','building.depot','building.fort'])assert.ok(manifest.assets.some(a=>a.family===family),family);
 const fortifications=manifest.assets.filter(a=>a.family==='building.wall'||a.family==='building.gate');
 assert.deepEqual([...new Set(fortifications.map(a=>a.family))].sort(),['building.gate','building.wall']);
 assert.equal(fortifications.filter(a=>a.family==='building.wall').length,9);
 assert.equal(fortifications.filter(a=>a.family==='building.gate').length,7);
 for(const asset of fortifications)assert.equal(asset.material,asset.family==='building.wall'?'stone':'wood');
 assert.deepEqual(artRoute('?art=stone'),{name:'stone',enabled:true,...ART_ROUTES.stone});
 for(const name of ['','unknown','constructor','__proto__'])assert.deepEqual(artRoute('?art='+name),{name,enabled:false,manifestUrl:ART_ROUTES.pilot.manifestUrl,world:false});
 for(const [name,recipe] of Object.entries(ART_ROUTES))assert.deepEqual(artRoute('?art='+name),{name,enabled:true,...recipe});
});
