#217 visible construction state

Visible buildings now expose only `underConstruction: boolean` after the existing fog filter. Own construction job remains private to its owner; enemy construction job/order/cooldown/queue/cargo redaction stays intact. Hidden buildings remain omitted. Completed damaged buildings remain completed; no HP heuristic. This view-only addition does not change authoritative entities, economy or navigation. Raster eligibility uses the flag as well as the legacy own job, keeping unfinished enemy buildings on fallback.

Baseline4fail/2pass; candidate6new +3existing Fort contracts PASS. Initial fixture forgot to refresh visibility before the ordinary build command; both failed fixture receipts are retained. Corrected fixture observes existing visibility guard, without weakening it. Exact source hashes in source-pins.json.

Actual two-peer evidence221 verifies visible enemy flag, owner job, redaction and normal completion on frozen215 bundle2f42ffff…406eb. Overall221 remains HOLD: later scout-return guard failed, scout absent; no fog-return/menu proof. Root viewed unfinished/completed screenshots; both show a procedural Fort form, so completed authored art is NOT accepted from those images. No replay needed for the already demonstrated flag contract. Public207 unchanged; final authored construction/destruction remains unfinished.
