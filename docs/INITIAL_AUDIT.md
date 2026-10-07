# Initial audit — 2026-10-07
No Git repository, game source, engine, scene graph, rendering/animation runtime, AI, pathfinding, combat, data/maps, save system, UI, build, tests, server, or deployment existed at intake. Existing leadership directory: 207 MB, 134 PNGs plus custody/review metadata, 12 characters. Selected candidate identity references contain 8 static directions each; latest B02 used where present. Source candidate metadata says unaudited; it does not certify animations or production acceptance.

Architecture selected from empty starting point: plain ES module shared simulation, browser Canvas2D isometric view + accessible DOM HUD, Vite production build, Node HTTP/ws authoritative exactly-two-seat server. Local AI uses the shared simulation in-browser and requires no match server after loading. Online client sends intent commands and receives filtered authoritative views at 5Hz, independent 20Hz simulation.

Networking alternatives: lockstep would require identical cross-browser runtime behavior and expose full match information. Authoritative server + fog-filtered snapshots is selected for straightforward ownership, economy, victory, reconnect, and hidden-information enforcement. No client has authority over HP/resources/entity creation.

Asset preservation: source files read-only; web derivatives are compressed full-canvas downscales, immutable source/output hashes in manifest; static leader images are not claimed as motion frames. Original procedural unit/terrain/building art is a development pipeline; final animation quality must be audited separately.

Public route: investigate available HTTPS hosting first. Existing Tailscale account/node has Funnel capability and no existing Serve/Funnel config; isolated game port can expose both production client and WebSocket without installation on player devices. This is machine-hosted and depends on its uptime; document exact limitation. Portable container deployment also required.
