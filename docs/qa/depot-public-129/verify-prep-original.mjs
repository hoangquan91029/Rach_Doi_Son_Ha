import {readFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
// No browser import/launch before actual terminal127 plan and root dispatch bind this preparation.
const dispatch=JSON.parse(await readFile(new URL('dispatch.json',import.meta.url),'utf8'));
assert.equal(dispatch.status,'AUTHORIZED_FINITE_PUBLIC129');
assert.equal(dispatch.expectedTerrainAssets,23);
assert.equal(dispatch.expectedOldSHA,'4ce3127451d77e7fb12a7cba023ab8a58603125207244bf2395d31c493582a3a');
assert.equal(dispatch.depotPlan?.status,'ROOT_ACCEPTED_TERMINAL127_UI_PLAN');
throw Error('Preparation guard: terminal127 tested realUI Depot helper/sourcepins must be wired before any browserlaunch');
