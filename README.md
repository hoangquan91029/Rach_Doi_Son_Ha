# Rạch Đôi Sơn Hà

Original browser RTS about historical leadership, terrain and physical food logistics. **In development; NOT COMPLETE under sections 81–114. Visual quality gate failed.** Existing source art in `leadership/` is preserved read-only.

Public desktop-browser playtest: https://kieu-hoang-quan-loq-15iax9.tail5247a0.ts.net/ — single player and online 1v1, no player installation. Hosting requires this machine to remain awake and connected. The optional `?art=pilot` preview uses original raster candidates over the actual match; missing art is explicitly PLACEHOLDER_ONLY. Neither preview nor default development art is final approved art.

## Development
Requires Node.js 22.12+ or 24.x for developers only. Players need only a desktop browser and the public HTTPS URL.

```sh
npm ci
npm run dev
```
Run `npm start` in a second terminal for online rooms during Vite development. Vite proxies `/ws` and `/health`. Single-player simulation runs locally after loading.

## Production
```sh
npm run build
npm start
```
Node serves `dist/` and `/ws` on the same origin. `HOST` and `PORT` configure listening. A reverse proxy must terminate HTTPS and forward WebSocket upgrades. Portable container: `docker build -f server/Dockerfile -t rach-doi-son-ha .` then publish container port 3000 behind HTTPS.

## Verification
```sh
npm test
python3 scripts/verify-assets.py
node scripts/benchmark.mjs
```
Browser acceptance evidence and known gaps are tracked in `PROJECT_STATUS.md` and `docs/SECTION_81.md`. `docs/CONTRACT.md` describes integration APIs. The source briefs and historical dossier are retained in `docs/`.

## Controls
Click or drag to select, Shift adds to selection; right-click moves, attacks or gathers. A arms attack move; S stops; H holds. Ctrl+1–9 saves groups; 1–9 recalls. WASD/arrows pan, mouse wheel zooms, minimap navigates. HUD supplies building/training/leader/supply actions. The General's death ends the match. Destroying the Main Residence does not; only the surviving King may rebuild it, and only one may exist including construction.

## Asset custody
`public/assets/leadership/manifest.json` pins sources and 96 compressed directional derivatives. Derivatives preserve full-canvas alignment; no source edits. They are static identity images, not certified idle/walk/attack/hit/death animation sets. Original procedural rendering supports development, with final motion/art quality an open gate. Numeric leadership modifiers are gameplay interpretations of the supplied historical dossier.
