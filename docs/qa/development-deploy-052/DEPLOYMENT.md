#052 prepared development mechanics promotion

New stage `/tmp/rds-development052-build` exactly matches every file of tested043 tree. Source main/sim match044 pins,049 real online lifecycle passes bothmaps. This is a development mechanics update: default PLACEHOLDER_ONLY, all art opt-in; no final-art or fullgoal acceptance.

Read `/health` immediately before promotion; require rooms0. Preserve installed service/Funnel; production replacement and restart occur only after root approves this preparation.

From project root, concrete promotion commands:

```sh
node -e "const h=await(await fetch('http://127.0.0.1:3000/health')).json();if(!h.ok||h.rooms!==0)throw Error('Active rooms prohibit restart')"
cp -a /tmp/rds-development052-build dist-052-staged
mv dist dist-before-052
mv dist-052-staged dist
systemctl --user restart rach-doi-son-ha.service
curl --fail http://127.0.0.1:3000/health
```

Read-only tar `rollback-before-052.tar.gz` preserves prepromotion actual disk dist/server/shared/client/package/lock/index/vite source; SHA in prepared.json. Backend3358 loaded hash is unknown. Rollback restores observed disk source and old dist, not an unverifiable historical in-memory backend.

Concrete rollback from project root if public acceptance fails:

```sh
node -e "const h=await(await fetch('http://127.0.0.1:3000/health')).json();if(!h.ok||h.rooms!==0)throw Error('Active rooms prohibit restart')"
mv dist dist-held-052
mv dist-before-052 dist
# Source unchanged during052; if hashes differ, restore exact disk source from preserved tar before restarting.
systemctl --user restart rach-doi-son-ha.service
curl --fail http://127.0.0.1:3000/health
sha256sum dist/assets/index-ClW3IlNb.js
```

Expected old bundle ca8e6428603c0033ccd9926fdb69daa5d78cee28fef4259607946530fe02e08b. Restart binds current pinned disk backend/client, eliminating release052 loaded-code uncertainty. Postpromotion one actual publicHTTPS Chromium/Firefox candidate online lifecycle attempt per map, Delta then Coast, stop any failure, normalTLS. Same-machine public endpoint coverage is not external-device/WAN proof.
