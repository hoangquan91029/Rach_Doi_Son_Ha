# Machine-hosted HTTPS playtest

## Current088 development crowd mechanics

Root approved085 full88/88 (sixAI/twoNaval unchanged),087 durable10/10 and086 dense45 viewport/30s combat narrow proof. Public bundle index-ByZVQkbs.js SHA f85cdd520aa1fc133fe98eb2542a917600206fa27fa9dd16ca1e591fef3ea3e7; canonical simSHA28e37b63ee39bbe1440741fa0afed3d9f20797831f666c0ff03d8299a8eb609c. NewPID157023/restart14:55:37+07 binds matching offline/backend code. Default placeholders/optionalCANDIDATE unchanged. Dense ford overlap remains; SAMPLES_ONLY/no final art or performance approval;089 public browser proof pending.

Rollback069dist dist-before-088 and oldsim docs/qa/development-crowd-088/sim-before-088.js preserved Gitignored; read-only archiveSHAabb20bd32fa889ad5cd764d871923b99a1d9b29ef05ab4b57cf4841fa92667c8. Guard rooms0 immediately; restore source/build together and restart unchangedservice. See [088 commands/receipt](../docs/qa/development-crowd-088/DEPLOYMENT.md). Old052/069archives/backups/Funnel unchanged; do not interrupt active rooms.


Production Vite client and authoritative Node server run on this computer. A user systemd unit restarts the process on failure. Tailscale Funnel exposes ONLY this HTTP/WebSocket server on HTTPS ports 443 and 8443. Players do not need Tailscale or any installed software. No source folders, credentials, or developer server are served: the Node static root is `dist/`.

This is a real public build served over HTTPS, but it is **not an always-on cloud deployment**. The link depends on this computer being awake, connected, with its user service running. Node restart loses active rooms. User service begins with user sessions; no privileged system service or login lingering is configured.

Historical development release069 introduced the monotonic ping fix, retained in current088: [play](https://kieu-hoang-quan-loq-15iax9.tail5247a0.ts.net/) or [optional candidate art](https://kieu-hoang-quan-loq-15iax9.tail5247a0.ts.net/?art=work). Default art remains placeholders; optional art remains CANDIDATE. This is not final artwork, full-roster completion or external-device/WAN acceptance. Earlier052 both-map normal-TLS lifecycle evidence is retained;069 adds one short actual Chromium/Firefox150ms-each-direction room/reload/tick/pong proof (measured311–377ms), errors0. See [069 checkpoint](../docs/qa/development-deploy-069/CHECKPOINT.md).

The installed `rach-doi-son-ha.service` runs Node24.15.0 from this checkout on loopback port3000, with8rooms/32connections. Existing Funnel443/8443 both proxy that port. Release069 restarted the service at2026-10-09 14:18:36+07 (PID137146 at release), binding verified server/shared/client disk source. Served `index-CtalOIcs.js` SHA256 is `9a7e0e1bd744063a86c065bcf1089c75dbc26c4ad6f0297ffade6fe9922ceff5`; [prepared pins](../docs/qa/development-deploy-069/prepared.json) and [promotion receipt](../docs/qa/development-deploy-069/promotion-receipt.json) bind it. Prior052 restart/sourcebinding and the unknown pre052 in-memory backend remain documented in052 custody.

Enable after the tested production build:
```sh
mkdir -p ~/.config/systemd/user
cp deploy/rach-doi-son-ha.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now rach-doi-son-ha.service
tailscale funnel --bg --https=443 http://127.0.0.1:3000
```
Disable only this game endpoint (preserve any other endpoints):
```sh
tailscale funnel --https=443 off
tailscale funnel --https=8443 off
systemctl --user disable --now rach-doi-son-ha.service
```

Portable cloud/container alternative in `server/Dockerfile` and `server/DEPLOY.md`. A user-provided permanent domain and hosting account can replace this transport while preserving game architecture. No hosting purchase has been made.

## Updates and rollback

Before replacing `dist/` or restarting, require an empty server. Run from the project root:

```sh
node -e "const h=await(await fetch('http://127.0.0.1:3000/health')).json();if(!h.ok||h.rooms!==0)throw Error('Active rooms prohibit restart')"
```

If rooms are active, defer maintenance. Build into a distinct directory, preserve old dist and actual disk source, compare the staged bundle/source against the tested release, then swap dist and restart the user service. Restart binds backend source and client together; copying dist alone does not. Keep Funnel and candidate labels unchanged. Verify health, exact served bundle and clean public-browser lifecycle afterward. [052 deployment commands](../docs/qa/development-deploy-052/DEPLOYMENT.md) record the completed promotion.

Release052 keeps local `dist-before-052/` and read-only `docs/qa/development-deploy-052/rollback-before-052.tar.gz`. The archive is intentionally Git-ignored local custody; preserve it separately when moving this checkout. Its hash and contents are recorded in prepared.json. It contains predeployment dist/server/shared/client/package/lock/index/vite source; the installed-service snapshot is alongside it.

To roll back052, first repeat the rooms0 guard, verify the archive's recorded SHA and ensure `dist-held-052` does not already exist. With runtime source still matching052 pins:

```sh
mv dist dist-held-052
mv dist-before-052 dist
systemctl --user restart rach-doi-son-ha.service
curl --fail http://127.0.0.1:3000/health
sha256sum dist/assets/index-ClW3IlNb.js
```

Expected old bundle: `ca8e6428603c0033ccd9926fdb69daa5d78cee28fef4259607946530fe02e08b`. If disk runtime source changed since052, preserve those changes first and restore the matching predeployment source before restart:

```sh
tar -xzf docs/qa/development-deploy-052/rollback-before-052.tar.gz server shared client package.json package-lock.json index.html vite.config.js
```

Restore package dependencies if the preserved lock differs from the installed dependencies. If the old dist folder is unavailable, recover the archive's `dist/` into a separate staging directory and verify old pins before swapping it. Recheck local/public health and served hashes after rollback; restarting always loses volatile rooms.

For the current069 release rollback, use the same rooms0 maintenance guard above, preserve current dist as `dist-held-069`, restore `dist-before-069`, then restart unchangedservice. This recovers052 bundle `index-Doi9i9JT.js` SHA256 `33da4dd6348b742f8f83bb241c4e01c892dba850668160368a1dadfff047e548`. If disk source differs from069 recorded pins, preserve changes and restore matching pre069 source from local read-only `docs/qa/development-deploy-069/rollback-before-069.tar.gz` first. Archive is Git-ignored persistent custody; hash in prepared.json. Earlier052 archive and `dist-before-052/` remain preserved. [069 commands/custody](../docs/qa/development-deploy-069/DEPLOYMENT.md) supplement the historical052 procedure above.
