# Fog-region correction — 7 October 2026

The previous normal-zoom captures showed a geometric grid inside fog. Each tile was filled separately, causing antialiased shared edges to remain lighter. The renderer now builds a single path for explored fog and another for unexplored fog, filling each region once. Current visibility membership, simulation coordinates and enemy filtering remain unchanged.

The parent inspected `artifacts/art-v1/fog-region-correction/normal-zoom.png` in the actual production client: the internal fog grid is removed. Normal UI starts a match and selects the General at zoom1.08; all ten candidate assets decode with zero page errors. Receipt retained beside that screenshot. 48/48 tests and production build pass (`index-tTsUjQtg.js`, 122.90kB / 41.15kB gzip).

This closes only the fog seam defect. Minimap information, terrain transitions, unfinished world assets and motion remain separate open gates. The overall visual release still fails.
