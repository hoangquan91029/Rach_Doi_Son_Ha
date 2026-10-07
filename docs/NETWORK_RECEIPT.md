# Network receipt — 2026-10-07

Implemented immutable map-once snapshots: each initial start and reconnect start carries the complete map; periodic state packets carry map id, width, height and current fog-filtered resource nodes. The client must hydrate incoming maps by merging into its previous map. Terrain and name are never mutated during a match. Tick, entities, fog, resources and winner remain authoritative server state. No client online simulation added.

WebSocket permessage-deflate is enabled with a 1024-byte threshold, client/server no-context-takeover, 15-bit server maximum window with the protocol default client window, zlib memLevel 7, and concurrency limit 4. Node client negotiation was verified; browsers negotiate compression natively. Packet rate remains 5 Hz and simulation 20 Hz. Start packets remain full.

Reproduce with: `node server/benchmark-network.js`.

Fixture: seeded delta map, 20/100/200 units **per player**, plus four buildings per player, idle for 200 ticks. Each side's distant opponent remains hidden by fog. 200 units per side is an artificial stress fixture above the 120 population cap; it is not obtainable through production commands. Repeated infantry fixtures compress well and these bytes are not a worst-case moving battle estimate. Gzip is indicative only; WebSocket permessage-deflate uses raw deflate with framing rather than gzip.

| Units per player | Viewer | Tick | Visible entities | Full raw bytes | Compact raw bytes | Saved | Full gzip bytes | Compact gzip bytes | State hash |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 20 | 0 | 200 | 24 | 67392 | 43509 | 35.4% | 1711 | 1373 | a2667aef |
| 20 | 1 | 200 | 24 | 67394 | 43511 | 35.4% | 1704 | 1363 | a2667aef |
| 100 | 0 | 200 | 104 | 88441 | 64558 | 27% | 2103 | 1762 | 12f3f25b |
| 100 | 1 | 200 | 104 | 88514 | 64631 | 27% | 2092 | 1751 | 12f3f25b |
| 200 | 0 | 200 | 204 | 114831 | 90948 | 20.8% | 2493 | 2148 | 8de310ed |
| 200 | 1 | 200 | 204 | 114904 | 91021 | 20.8% | 2488 | 2144 | 8de310ed |

At 5 Hz per connected player, raw serialized snapshots fall from approximately 337–575 KB/s to 218–456 KB/s across these fixtures before transport compression. The immutable map removes 23,883 raw bytes per snapshot. The measured gzip savings are only about 338–345 bytes per snapshot because repeated terrain strings already compress well; raw savings percentages must not be presented as compressed wire savings. Fog booleans remain a significant raw payload; bit packing would require a separate protocol/client change and is not part of this change.

Verification: `node --test tests/server.test.js` — twelve tests pass, including negotiated compression, full start map, compact state map, hydrated/full view deep equality, matching ticks and unchanged authoritative hash during serialization, two-sided reconnect, expired/rotated tokens, public-command General death, fog-target rejection, rate/payload limits and HTTP path/Origin protection. Public repair/cancel command tests verify construction resumption and wrong-owner cancellation rejection. Repeated concurrent close calls share one completion promise. Every test awaits graceful server close, including active compressed sockets. No deployment performed.

CLI capacity is finite and environment-configurable: defaults 8 rooms, 64 simultaneous sockets and 60 seconds grace; bounded parsing and invalid-value fallback are tested. A global connection cap preserves shared-NAT compatibility and does not trust forwarded IP headers.

Firefox handshake compatibility correction: removed explicit clientMaxWindowBits because a bare permessage-deflate offer does not advertise that optional parameter. Raw Firefox-style handshake now returns101; see [diagnosis](FIREFOX_WEBSOCKET_DIAGNOSIS.md). All other compression limits remain.
