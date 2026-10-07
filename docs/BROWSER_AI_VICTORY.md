# Production browser AI victory receipt — 2026-10-07

Both requested easy AI matches completed in a real Chromium browser against the production client at `http://127.0.0.1:3000`. The test used ordinary menu, nickname/map/difficulty controls, Canvas mouse input, action buttons and keyboard/control groups. `window.rtsDiagnostics.snapshot()`, `point()` and `entityPoint()` were read-only observations for visible entity positions and assertions. No simulation state was mutated; no command API, cheat global, resource gift, speed-up, difficulty weakening or injected victory was used. The production server/build was not changed or restarted by this QA task.

| Map | Winner | End condition | Tick | Simulation time | Player General |
|---|---|---|---:|---:|---|
| delta | Player 0 | Enemy General defeated | 2420 | 121.0 s | 360 HP; x11, y25.5 |
| coast | Player 0 | Enemy General defeated | 2504 | 125.2 s | 353.6/360 HP; x11, y25.5 |

Both runs had zero page errors. The result screen appeared, and clicking its return control restored the main menu. These are gameplay/victory checks; visible prototype art is not accepted as final visual quality by these receipts.

## Evidence

- [Aggregate verified receipt](../artifacts/production-ai-winning/verified-victories.json)
- [Delta actual result screenshot](../artifacts/production-ai-winning/delta-attempt-03/delta-victory.png) and [timeline/receipt](../artifacts/production-ai-winning/delta-attempt-03/delta-receipt.json)
- [Coast actual result screenshot](../artifacts/production-ai-winning/coast-attempt-01/coast-victory.png) and [timeline/receipt](../artifacts/production-ai-winning/coast-attempt-01/coast-receipt.json)

Filtered diagnostics showed the living enemy General before the decisive final attack, followed by the authoritative winner/reason and result UI. After death an unseen enemy General is not exposed by filtered diagnostics, so its hidden corpse is not invented as additional evidence.

## Reproduction

```sh
node scripts/browser-ai-winning.mjs
# One map and separate immutable attempt folder:
QA_MAP=delta QA_OUTPUT=artifacts/production-ai-winning/NEW-DELTA-ATTEMPT node scripts/browser-ai-winning.mjs
```

The script bounds each match at approximately four wall-clock minutes and asserts Player 0 victory by enemy General death. A timeout, defeat or browser automation error exits unsuccessfully and retains its own screenshot and receipt. Default runs execute both maps sequentially.

Winning UI strategy: start six workers on wood/food/iron, two each; queue eight firearms and four additional villagers; save worker/control groups; keep the General holding at home; construct two paid forts at UI tile targets `(11,27)` and `(7,18)` (simulation placement centers `(11.5,27.5)` and `(7.5,18.5)`); return completed builders to gathering; advance the military at about 90 simulation seconds; continue firearm production and ordinary F2/attack-move reinforcement orders every two seconds; aim at the visible enemy General when discovered; move the food wagon behind the front and load from friendly stores when necessary. All costs, fog, navigation, AI and damage rules remain production rules.

The recorded winning attempt's early action log says “General held behind residence.” Its immediate hold superseded an attempted reposition: authoritative snapshots show the General remained at the original home position `(11,25.5)` throughout these victories. The script now describes and directly performs that actual home hold, avoiding a misleading placement claim.

## Retained failures and input findings

The first delta attempt stopped at about 67 simulation seconds because a moving/overlapping worker ground-point click selected another worker. Its error screenshot/filtered snapshot are retained in `artifacts/production-ai-winning/delta-error.png` and `delta-error.json`. It is not a match completion or victory. The parent subsequently supplied read-only `entityPoint(id)` for actual visible-body UI picking; later runs used that coordinate, plus player control groups saved before workers moved.

A fort attempted at `(12,27)` was correctly rejected: placement snaps to `(12.5,27.5)` and overlaps the existing depot at `(13.5,28.5)`. This is a valid footprint constraint, not a click or path bug. Free sites were chosen through normal placement inputs.

The second delta attempt sent a small army at 40 seconds before the eight-firearm queue completed and left completed fort builders idle, reducing wood income. That run timed out at tick4806 with no winner; the General survived. Its screenshot and receipt remain under `artifacts/production-ai-winning/delta-attempt-02/`. It is explicitly not a pass. Waiting for the stronger force and restoring builder income produced the two measured victories above.

## Public HTTPS relay boundary

The same UI strategy also completed both easy maps at `https://kieu-hoang-quan-loq-15iax9.tail5247a0.ts.net/`, resolving that hostname to relay `103.84.155.153` using Chromium's host resolver rule. TLS verification remained enabled: neither `ignoreHTTPSErrors` nor a certificate-error bypass was used. Both navigation responses recorded HTTP 200, remote address `103.84.155.153:443`, TLS 1.3, issuer `YE1`, and the exact hostname certificate subject. This verifies the public HTTPS delivery boundary; these single-player AI matches simulate locally in the production browser and do not establish multiplayer WSS coverage.

| Public map | Winner / end condition | Tick | Simulation time | Home General HP |
|---|---|---:|---:|---:|
| delta | Player 0 / Enemy General defeated | 2421 | 121.05 s | 360/360 |
| coast | Player 0 / Enemy General defeated | 2453 | 122.65 s | 360/360 |

Both successful runs verified the visible result screen and return to the main menu, with zero page errors. [Public aggregate receipt](../artifacts/production-ai-winning-public-relay/verified-victories.json), [delta receipt](../artifacts/production-ai-winning-public-relay/delta-receipt.json), [delta screenshot](../artifacts/production-ai-winning-public-relay/delta-victory.png), [coast receipt](../artifacts/production-ai-winning-public-relay/coast-attempt-02/coast-receipt.json), and [coast screenshot](../artifacts/production-ai-winning-public-relay/coast-attempt-02/coast-victory.png) remain separate from the local evidence.

The first public coast match also reached Player 0 victory at tick2454, but its result modal intercepted a pending minimap click, producing an automation timeout before the menu assertions. Its error screenshot and snapshot are retained at the public folder root and are not counted as a clean pass. A script-only guard now ignores a blocked world/minimap click only when the read-only snapshot confirms the match has ended; otherwise the original error propagates. The clean second attempt is reported above.

```sh
GAME_URL=https://kieu-hoang-quan-loq-15iax9.tail5247a0.ts.net QA_RESOLVE_IP=103.84.155.153 QA_OUTPUT=artifacts/production-ai-winning-public-relay/NEW-ATTEMPT node scripts/browser-ai-winning.mjs
```
