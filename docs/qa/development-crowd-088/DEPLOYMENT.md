#088 promoted;089 browser proof pending

Actualpromotion installed formatted087test10/10PASS; external canonicalbackup docs088/sim-before-088.js. PID157023/publicf85…ea3e7/healthrooms0. promotion-receipt.json authoritative; original preparation below retained as custody.

#088 concrete promotion preparation — DO NOT execute until root intake approval

Preparedexacttested085 stage `/tmp/rds-crowd088-7ykc1g7o`, parent084a9bd…9821f, canonicalnormalizedsim28e37b…609c, testedfrontendbundlef85cdd…ea3e7. All085inputs copied/pinned; server/client unchanged from085matchedtree. Public069 remains9a7e…ceff5/PID137146.086actualdense and087durabletests/rootintake gateactualpromotion; novisual/performancePASS inferred. DefaultPLACEHOLDER_ONLY/optionalCANDIDATE unchanged.

Root-approved integration must first install/review087durabletests and review resulting test-inputdrift. Existing pinned test files must remain unchanged; any drift in preflight is a stop requiring concrete new review. Adding087test file does not alter prepared livebeforepins. Do not use archive restoration to delete later legitimate work. Use checkoutroot workingdirectory for commands below.

Concrete reversible source/dist installation after approval:

```sh
node docs/qa/development-crowd-088/preflight.mjs
cp -a /tmp/rds-crowd088-7ykc1g7o/dist dist-088-staged
cp /tmp/rds-crowd088-7ykc1g7o/sim.js shared/sim-088-staged.js
sha256sum shared/sim-088-staged.js dist-088-staged/assets/index-ByZVQkbs.js
# Immediate rooms0 guard again, adjacent to actual install/restart.
node -e "const h=await(await fetch('http://127.0.0.1:3000/health')).json();if(!h.ok||h.rooms!==0)throw Error('Active rooms prohibit promotion')"
cp shared/sim.js docs/qa/development-crowd-088/sim-before-088.js
mv shared/sim-088-staged.js shared/sim.js
mv dist dist-before-088
mv dist-088-staged dist
systemctl --user restart rach-doi-son-ha.service
curl --fail http://127.0.0.1:3000/health
systemctl --user show rach-doi-son-ha.service -p MainPID -p ActiveState -p ActiveEnterTimestamp
```

ExpectedsharedsimSHA28e37b63ee39bbe1440741fa0afed3d9f20797831f666c0ff03d8299a8eb609c/bundlef85cdd520aa1fc133fe98eb2542a917600206fa27fa9dd16ca1e591fef3ea3e7. This deliberately installs matchingbackend/offlinefrontend logic before restart. Record newPID/start/publicHTTPSservedbundle and health; separatefinitepublic normalTLS browser proof required afterpromotion. Sourceupdates withoutrestart cannotbindloadedbackend. No deploymentcommandexecuted under088.

Concrete rollback after approval if candidateacceptancefails, with rooms0 guard before restart:

```sh
node -e "const h=await(await fetch('http://127.0.0.1:3000/health')).json();if(!h.ok||h.rooms!==0)throw Error('Active rooms prohibit rollback')"
mv dist dist-held-088
mv dist-before-088 dist
mv shared/sim.js shared/sim-held-088.js
cp docs/qa/development-crowd-088/sim-before-088.js shared/sim.js
systemctl --user restart rach-doi-son-ha.service
curl --fail http://127.0.0.1:3000/health
sha256sum shared/sim.js dist/assets/index-CtalOIcs.js
```

Expectedoldsim b4257d74b1684efdd7a8fc7d2fbc273494f9fb63304e217a6ab8693ba240470d/069bundle9a7e0e1bd744063a86c065bcf1089c75dbc26c4ad6f0297ffade6fe9922ceff5. Heldsource/build preserved. Archive `rollback-before-088.tar.gz` is readonly/Gitignored locally SHAabb20bd32fa889ad5cd764d871923b99a1d9b29ef05ab4b57cf4841fa92667c8; preservesactualbefore dist/server/shared/client/tests/packages/index/vite/service receipts. If renamebackup missing, extract archive into a NEW ownedtempdir, verify pins, then install onlyreviewedrelevantfiles; neverblindlyoverwrite currentproject or087tests. Old052/069archives/directories and Funnel untouched.

In-memory honesty: observedPID/start/ExecStart matches069 verifiedrestart andpublicfrontendhash. Node's loadedsim bytes cannot be directly rehashed throughthis read-only preparation. Currentdisk pinned; this ishistoricalbinding pluslivePID corroboration, notnewin-memorysimulationproof. No browser/fullmatch/externalWANclaim.
