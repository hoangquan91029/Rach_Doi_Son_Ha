# Q01 room baseline350

One finite ordinary UI campaign used a single isolated `createGameServer({port:0,distDir:'/tmp/rds-room-load350-build'})` from immutable230, preserving its default cap8. No rebuild: all207 current public345 files copied and hashed before launch. Eight independent rooms have two real Chromium Playwright human-seat connections each, established with actual create/join/map/ready UI. No gameplay commands were sent. Maps alternate Coast/Delta, starting with Coast.

| Rooms | Live connections | Living entities | Window seconds | Per-room ticks/sec | Render cost median / p95 ms | Loop delay p95 ms | Combined RSS MiB |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 2 | 34 | 25.865 | 19.950 | 3.4 / 5.4 | 10.60 | 224.0 |
| 5 | 10 | 170 | 25.465 | 19.870 | 4.8 / 8.8 | 18.15 | 341.3 |
| 8 | 16 | 272 | 25.614 | 19.911 | 4.7 / 8.0 | 23.31 | 380.9 |

No concrete simulation bottleneck is demonstrated: all rooms continued near20Hz. Loop delay and memory rise with load, but server and Playwright coordinator share one process. At8 rooms event-loop utilization was0.282 and the maximum loop delay90.05ms; these values do not isolate simulation, snapshot serialization, browser automation, or OS scheduling. This supports an idle room baseline only. Initial armies remain idle; no combat, dense-unit, final performance, external desktop or WAN acceptance follows.

`frameMs` is renderer execution cost sampled via read-only diagnostics, not RAF interval or FPS. All sampled document visibility states were `visible`; headless multi-page visibility does not establish real desktop tab scheduling. Diagnostics clone displayed state, adding measurement overhead. Raw samples, pings (including original nulls), tick advances, living counts and response pins are in `receipt.json`; aggregate data is in `summary.json`.

Every sampled client had54 art descriptors ready/0failed and12 portraits. Page/network/HTTP errors0;952 exact response body pins; gameplay commands0. Ordinary menu departure reduced rooms/connections to0 before closing all16 pages/contexts, browser and isolated server. Source/public/runtime/copied-build bytes remained exact; production PID3229 intentionally runs with healthrooms0. The copied build remains retained at its literal `/tmp` path; all original receipts remain retained.

An inventory error reading a symlink directory occurred before server/browser creation; its original error and bounded correction are retained in `prelaunch-failure.json`. The live campaign launched once without retry. An aggregate-only null-ping sorting error is retained in `summary-original-failure.json`; the correction filters nulls only for aggregate ping statistics, preserving raw data and performing no browser replay.
