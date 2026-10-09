# Release and performance audit — 2026-10-09

Read-only audit by exact `gpt-6.1-sol`, reasoning `low`. Only this document was written. No runtime/build/deployment/service/image/API changes, no full matches or usage-limit queries. Existing dirty151 install and150/152/153 source work were preserved. Evidence collected on the project host is deliberately separated from external-device evidence.

**Conclusion:** the HTTPS development playtest is live and narrowly validated. A normal user can open the link without installing the game, but that link does not show the latest illustrated slice by default, and final public-link completion is not established. Visual coverage, external machines/WAN, realistic dense-load performance, durable availability and release-source reproducibility remain gates.

**Tóm tắt:** bản chơi thử HTTPS đang chạy; link mặc định vẫn dùng hình thủ tục, còn26 asset ứng viên chỉ bật bằng `?art=camp`. Kiểm tra cùng máy chủ không chứng minh máy ngoài mạng, hiệu năng trận đông quân hoặc bản phát hành cuối cùng.

## Exact present state and evidence

| Surface | Verified state | Limits |
|---|---|---|
| Public HTTPS root | GET200, HTML4459 bytes, SHA `caa893338db5c86cb7cdd99c75fb80bfe39e70baf9958a7e3a626e9ed153fae1` | HTTP read only; no new browser gameplay |
| Public149 JS | `/assets/index-05PkH4eu.js`,154296 bytes, SHA `70808200c04fa3547aa4204a0baa6e04546f6d9206c93667ee4c3edf7556883b` | Matches149 receipt; no inferred final approval |
| Public149 manifest | `/assets/art-v1/camp-148-manifest.json`,75011 bytes, SHA `b9ccd2b7bb68e11bdc9bacfdd31d56dcc05579c2950c01e650f0827ef1cbc134` |26 optional candidate assets |
| Pending food character | Public `/assets/art-v1/food-099-manifest.json`404 | Intended exclusion; not broken public food node |
| Health/service | `/health`200 `{"ok":true,"rooms":0}`; activePID157023,NRestarts0, MemoryCurrent53440512 bytes | A point-in-time idle service reading, not capacity/uptime proof |
|149 browser receipts | Chromium andFirefox26ready,12portraits; actual newCamp build→idle→select→ONEcavalry train/spawn→Pause/Resume→F2 exact currentliving militarygroup→Stop/menu; errors/failures0 | No isolated spawned-cavalry click claim, no dense or full match |
|151 canonicalLOCAL | Terminal exact148 source install; pendingLOCAL food preserved | Public stage differs intentionally by foodCHAR3exclusions; working tree is dirty/untracked |

Primary local sources: `server/index.js`, `client/main.js`, `client/renderer.js`, `client/raster-slice.js`, `client/art-assets.js`, `client/terrain-cache.js`, `client/terrain-transitions.js`, `client/visual-picking.js`; `docs/qa/cavalry-camp-public-149/{public-receipt,source-bindings}.json`, `EXECUTION_CHECKPOINT.md`; `docs/art/pipeline/cavalry-camp-canonical-151/{receipt.json,CHECKPOINT.md}`; `docs/qa/asset-memory-093/CHECKPOINT.md`; `docs/qa/checkpoint/ground-cache-performance.json`.

Earlier089/090 online/offline victories remain useful simulation/lifecycle evidence, but they exercised earlier public bundles.149 client changes have narrow ordinaryUI proofs rather than repeated full matches. This audit does not invalidate those proofs or upgrade them into current final visual/performance acceptance.

## Default experience versus optional slice

`createRasterSlice` enables only explicit art query values. RootURL therefore preloads no raster slice; portraits are a separate12-item boot system. CurrentLOCAL recognizes pilot/walk/work/food/terrain/iron/workshop/camp; public149 deliberately excludes pending foodCHAR route, manifest and atlas. `?art=camp` is the richest public26-asset route; README's pilot example describes an older smaller preview.

Exact authored state/direction is required. Unsupported unit types, directions, movement/combat/hit/death, building construction and other missing states use original procedural drawing. That fallback is honest but still visibly incomplete. Successful decode/custody,26ready, and approved Southwood/iron motion do not prove whole-roster realism or consistent final visuals. A final-link plan must choose and review one default illustrated manifest, explicitly account for fallback coverage, and enable it only after its acceptance gates; silently enabling all candidate art would bypass those gates.

`index.html` and `resizeCompatibility` present a desktop strategy notice on narrow/touch devices. Commands rely heavily on rightclick, keyboard M/A/Esc/F2/control groups, pointer selection and wheel. A responsive notice is not touch gameplay support. Desktop-first release is realistic; mobile should be clearly unsupported unless a separate accessible touch-command package is authorized.

## Architecture and concrete operational risks

Vite builds a static client; NodeHTTP/ws serves `dist`, runs authoritative online matches, and offline simulation runs in the browser.20Hz server interval steps each connected playing room; state snapshots every fourth tick are nominal5Hz. A single process shares simulation, JSON serialization, filesystemHTTP work and compression across rooms. Default8room/64connection code limits differ from recorded production service's32connections; the live service properties above were queried, its current full unit/environment was not re-read. Do not mistake admission caps for tested capacity.

Rooms are in-memory. Restart, power/sleep/network loss can destroy matches despite60second seat reconnect and systemd Restart=on-failure. Recorded069 unit binds127.0.0.1:3000 through TailscaleFunnel, user-owned workingdirectory, Node24.15.0; host availability remains an explicit player dependency. Health reports processresponse/roomcount only, without exactbuild identity, tickdelay, memory pressure or dependency availability. Idle rooms0 is safe for promotion at that instant, not a future deployment lock. Existing atomic promotions/old chunk retention/read-only rollback archives are valuable; recovery must still be rehearsed on an isolatedhost/port.

Server protects WS payload16KiB,40messages/s/socket, maxconnections/rooms, origin and commandshape; it terminates sends above1MiB `bufferedAmount`, and uses15second protocol heartbeat. These reduce abuse and stale sockets but do not prove representative multiroom CPU/network stability. `perMessageDeflate` is explicitly enabled with concurrency4 and no-contexttakeover. [The ws maintainer documentation](https://github.com/websockets/ws#websocket-compression) warns compression adds CPU/memory cost and recommends representative workload testing. Measure compressed bytes, serialization/step latency andRSS before tuning compression; no blanket disable/engine migration is justified.

HTTP reads whole files into memory for each request; it does not implement conditional304/ETag, range delivery or explicit staticcompression. LiveHTTP observed HTML `no-cache`; JS and manifest `public,max-age=3600`, no Content-Encoding/ETag for the observed ordinaryPython GET. That request did not negotiate gzip, so the observation alone is not a complete compressionnegotiation test. Source contains no compressionpath. Health has noCache-Control. Hash-versioned JS could use longimmutable caching, while mutablemanifest URLs should revalidate or become contentversioned; a onehour mutablemanifest can mix generations with overwrittenassetpaths. Current hashguards expose mismatch rather than drawing unknownbytes, but stale caches can still prevent boot. Keep old chunks through the compatible-cache horizon and make manifest/asset promotion a coherent transaction.

No serviceworker implementation was found in the inspected file inventory. Offline-before-setup means an alreadyloaded page with preloaded assets survives disconnection; it does not mean a newcold offlinevisit or browser restart is supported. Product wording should preserve that distinction.

TailscaleFunnel is a useful playtest route but depends on this node and has non-configurable bandwidthlimits; the officialdocs do not supply a guaranteedthroughput value. [TailscaleFunnel](https://tailscale.com/docs/features/tailscale-funnel). An external WAN trial is necessary before claiming thehost meets a chosen player load. Durable24/7 hosting should preserve WS upgrades, singleauthoritative-room ownership, TLS and draineddeployments; scaling replicas without routing/persistence design would lose roomownership.

## Performance evidence and budget

Present149 raster decodedRGBA is16942592bytes (~16.16MiB), substantially below loader128MiB defaultbudget.093 explicitly states thatbudget excludes portraits, compressedbuffers, derivedcells, alpha-readback, canvas/backingstorage andGPU copies. It is therefore not totalbrowsermemory. `visual-picking.js` lazily reads and caches entireatlasRGBA perimage; those arrays can add anotherdecodedcopy for pickedassets. Terraincache is capped8millionpixels (~30.5MiB RGBA); transitions cap2millionpixels (~7.6MiB). A1920×1080 worldcanvas at cappedDPR2 costs ~31.6MiB for oneRGBA surface before browser/GPU duplication. These independent costs explain why128MiB loaderheadroom is not permission for unbounded rosterfanout.

Existing terraincache performance receipt uses localhost/headless 1440×900,4second samples,17initialentities and separate1Hz diagnosticreads. One baseChromiumframeCost sample set contains only3readings; rivercadencep95 reaches33.4ms. It explicitly excludesdense battle. Later08645unit30second viewportcheck is narrow and projectedfordoverlap remains samples-only. Neither establishes current149 sustainedfps, memorygrowth, low-end device or multiroomcapacity.

Renderer culls terrain byviewport when uncached, retainsstatic terrain/transitioncaches, capsDPR2 and usesdepthsorting. However everyrender buildsmap-content cachekeys, derives/materialselects, scans visiblefog/map/forest props and sorts the entity/prop/resource depthqueue. Offlineframecost includes simulation/view; online JSON parse/interpolation/compression timing is elsewhere. The single `app.frameCost` is useful diagnosticworktime, not displaycadence, inputlatency or complete memory. Preserve currentcaches; profile before optimization. [MDNCanvas guidance](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Optimizing_canvas) supports reused/offscreen drawing and measured optimization, without requiring a newrenderengine.

The following are **proposed acceptance targets**, not currentpassclaims. Bind thehardware/browser/map/entitycount/art manifest/network and collect at least three repetitions perrepresentativecase; revise targets explicitly if evidence reveals an unrealistic tier.

| Measure | Initialdesktop target / acceptance method |
|---|---|
| Menu usability | Cold online ready≤5s on 25 Mbps/100msRTT;≤10s on 5 Mbps/150msRTT; explicitRetry/failure afterloaderdeadline |
| Menu webmetrics | Aim fieldp75 LCP≤2.5s,INP≤200ms,CLS≤0.1; canvasgameplay needs separatemetrics |
| Gameplay cadence | Supportedbaseline laptop1080p,DPR1/2: median≥55fps, p95frameinterval≤33.4ms, p99≤50ms; low tier declared30fps minimum |
| Worktime | Per frame simulation+renderp95≤16ms for60fps tier; p95≤28ms for30fps tier; report main thread long tasks separately |
| Input feedback | Local selection/ordermode feedbackp95≤100ms; network authoritativeorder outcome measured separately againstRTT+snapshot/tickcadence |
| Memory | LoaderuniqueRGBA≤128MiB; proposed full art browser working budget≤256MiB attributable asset/canvas storage and≤512MiB total renderer process onbaseline 4–8 GiB device; observable no monotonicgrowth across10menu/replay cycles |
| Server | Maxconfigured8rooms candidate: p95whole20Hzlooptime≤25ms,p99≤40ms,no sustainedlag/backpressuredisconnect; proposedRSS≤512MiB andstable30minute soak |
| WAN | 50/150/300msRTT+jitter and boundedloss cases; no staleorders/results/reconnectregression; bytes/s andsnapshot age documented |

Webmetrics targets follow [GoogleWebVitals](https://web.dev/articles/vitals); remainingnumbers are project proposals. Browserprocessmemory is engine/platformspecific, so record measurementmethod and avoid mixing JSheap with totalRSS. A densecase should include both maps, actual populations spanning45/100/legalmaximum or nearest reachablelimit, crowdedford/forest/shore, artilleryeffects, camera/zoom/selection and pause/replay. Recordbackingdimensions and actualcount; do not inject impossibleworld states to claim ordinary UI coverage.

[MDNrAF](https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame) notes callbacks usuallypause in background tabs. Offline simulation isframe-driven anddtclamped; hidden-tab elapsedtime must be defined and tested. Online server keepsrunning while an attachedhiddenbrowser may receive messages without rendering. [MDNWebSocket](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket) notes theclassicbrowserAPI lacks receive backpressure. Test tabhide20–60seconds, minimize/sleep/wake, stale view recovery and full page reload; do not treat rAFpause as authoritativeonlinepause.

## Prioritized finite work packages and release criteria

1. **P0 exactreleaseledger/docs:** Rootarchives stale topdocs byte-for-byte and supplies concise149PUBLIC/151LOCAL/foodexclusions/currentpendingart pointers. Produceone reproducible public stage from a frozencommit plus explicit3foodexclusions, with source/sim/manifest/buildhashes and rollbackpins. Existing151dirtysource is retained until deliberatelycommitted, never discarded. Criterion: rootURL/chunk/manifest/serviceidentity resolve to thesame boundcandidate; documentation names its desktopdevelopment scope.
2. **P0 user-visible slice:** Finishreviewed representativeunit/direction/action/buildingstate/mapcomposition coverage. Define whichcandidate becomesdefault; keeppending food motion and unsupportedstates open. Criterion: human actualgameplay-size continuousvisualacceptance on exactrelease candidate; missing state ledgerresolved or deliberatelyaccepted, finalqualityflags remaintruthful.
3. **P1 performanceinstrumentation:** QA-only bounded lightweightcadence/framecost/longtask/snapshot age/stepduration/bytes/memorysampling; no frequentworldclones or screenshotstorms. Run isolatedcurrentcandidate profiling at tiers above before optimization. Criterion: pinnedraw data, crediblecounts/durations, acceptancebudget and bottleneckexplanation; no more passes based solely on3samples/4seconds.
4. **P1 realexternal desktop/WAN:** Separatephysicaldesktop withouttailnet/clientinstallation, differentnetwork (e.g. home vs mobilehotspot), cold cache HTTPS plus invitation and actual1v1/reconnect/result/menu on both maps. Include normalChrome/Firefox; SafariMac either tested or explicitlyunsupported. Browserautomation on theserver cannot satisfy thisgate. Criterion: device/OS/browser/network/build pin, measuredload/frame/networkbehavior and uservisible outcomes; no claim of external coverage from injectedlatency.
5. **P1 hosting/cache hardening:** Isolated304/immutable/mutablemanifest/versioncoherence and negotiatedcompression checks; healthbuild identity and ticklagdiagnostic; drainedpromotion/rollbackrunbook; uptime/suspendrisk addressed via always-on host or explicitplaytestavailability. Criterion: cold/warm/mixed cache bootPASS, restartloss honestlydescribed, monitoring/backuprestoreproof, ownedcleanup and no active room restart.
6. **P2 release candidate lifecycle:** Afterart/default/perfbinding, run focused end-to-end normal user flows offline-after-load and onlineboth maps on exactfinalbundle, longmatch/multiroomsoak, background tab/reload/disconnect/expiry/capacity cases. Reuse earlier89/90contracts for unchangedcore and rerunaffectedpaths only. Criterion: errors0, deterministicauthoritativeoutcomes, noleakingrooms/assets/sessions, signedacceptanceledger including what remainsunsupported.

No mandatoryengine rewrite, hostingmigration, broadartfanout or immediateproductionloadtest follows from this audit. Each package should have a finite order, stable inputs, raw receipts and an explicit gate; performstress/rollback experiments on isolatedcandidate infrastructure before any approvedpublicpromotion.
