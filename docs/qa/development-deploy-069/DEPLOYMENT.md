#069 prepared development pingfix promotion

Stage /tmp/rds-development069-build byte-identical to tested067final. Source main504528ad…d05ba and sim b4257d74…470d verified; allserver/shared/client/package pins in prepared.json. Defaultplaceholder/optional ?art=work candidate retained. Readonly Gitignored local rollback-before-069.tar.gz preserves actualdist and disk source; installedservice copy retained.

After ROOT approves this concrete preparation, from projectroot:

```sh
node -e "const h=await(await fetch('http://127.0.0.1:3000/health')).json();if(!h.ok||h.rooms!==0)throw Error('Active rooms prohibit restart')"
cp -a /tmp/rds-development069-build dist-069-staged
mv dist dist-before-069
mv dist-069-staged dist
systemctl --user restart rach-doi-son-ha.service
```

Rollback only at rooms0: preserve held newdist, restore dist-before-069, restore archived server/shared/client/package/lock/index/vite if their source pins changed (preserve changes first), restart unchangedservice, verifyold052bundle33da4dd6…7e548/localpublichealth. Archive remains local persistent custody; preserve whenmovingcheckout. No finalvisual/WAN/device claim. Short publicnormalTLS actualmixedbrowser room/start/reload/pongs/ticks will verifypromotion; no fullcombat.
