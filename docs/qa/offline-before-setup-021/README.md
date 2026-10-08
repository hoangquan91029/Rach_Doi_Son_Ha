# Offline before single-player setup — local candidate check

A clean Chromium context loaded all 16 `?art=walk` raster assets and entered the menu online. The context then went offline before opening single-player setup and stayed offline throughout both map flows.

Delta and Coast both accepted actual King/General choices (Xiang Yu/Napoleon), launched, advanced ticks and returned to menu. Delta also accepted an ordinary villager wood-gather order and simulation pause/resume. No page errors were captured. This is a bounded local gameplay check, not a completed match or production/offline reload certification.

Lazy leader portraits were unavailable after disconnection. Both setup screenshots show empty portrait wells; match commander portraits are unavailable too. Twelve `/assets/leadership/<id>/portrait.webp` paths failed; full paths and DOM image state are retained in `chromium/receipt.json`. One late Google DM Sans font request also failed. Map cards are text controls and remained usable; no failed map UI image request was observed. There were 27 failed network requests across the flow and 52 unavailable visible image instances across the four recorded UI inventories; those counts include repeated portrait instances.

Only these QA artifacts were written. The browser closed and the check's own Vite process on port 5175 (exec session 57833) was stopped normally. No implementation, production service or deployment changes.
