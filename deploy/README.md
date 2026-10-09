# Machine-hosted HTTPS playtest

Production Vite client and authoritative Node server run on this computer. A user systemd unit restarts the process on failure. Tailscale Funnel exposes ONLY this HTTP/WebSocket server on HTTPS ports 443 and 8443. Players do not need Tailscale or any installed software. No source folders, credentials, or developer server are served: the Node static root is `dist/`.

This is a real public build served over HTTPS, but it is **not an always-on cloud deployment**. The link depends on this computer being awake, connected, with its user service running. Node restart loses active rooms. User service begins with user sessions; no privileged system service or login lingering is configured.

Current development mechanics release052: [play](https://kieu-hoang-quan-loq-15iax9.tail5247a0.ts.net/) or [optional candidate art](https://kieu-hoang-quan-loq-15iax9.tail5247a0.ts.net/?art=work). Default art remains placeholders; optional art remains CANDIDATE. This is not final artwork, full-roster completion or external-device/WAN acceptance. Normal-TLS Chromium/Firefox public lifecycle checks passed both maps; see [052 checkpoint](../docs/qa/development-deploy-052/CHECKPOINT.md).

The installed `rach-doi-son-ha.service` runs Node24.15.0 from this checkout on loopback port 3000, with 8 rooms/32 connections. Existing Funnel ports 443/8443 both proxy that port. Release052 restarted the service at 2026-10-09 13:13:04+07 (PID106497 at release), binding the verified server/shared/client disk source to the served client. Previous PID3358's loaded backend hash was unknown; the backup preserves observed disk source, not an inferred in-memory version. The served `index-Doi9i9JT.js` SHA256 is `33da4dd6348b742f8f83bb241c4e01c892dba850668160368a1dadfff047e548`; [prepared pins](../docs/qa/development-deploy-052/prepared.json) and [promotion receipt](../docs/qa/development-deploy-052/promotion-receipt.json) bind the exact release.

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
