# D00 walk timing proposal

Eight frames at 100 ms each; total cycle 800 ms. The only proposed call is F02 at 200 ms. It tests a distinct passing pose with one planted support and one visibly raised swing foot. It is not a direct swap between two grounded contacts and is not a completed loop.

| Frame | Time | Phase | Expected pose | Status |
|---|---:|---|---|---|
| F00 | 0 ms | Near contact | Near/right foot leads lower-right; far leg trails | Selected F00 from the closed failed pilot-001 cycle; review evidence only, not a 004 source or attachment |
| F01 | 100 ms | Down | Weight settles onto near/right support | Not generated |
| F02 | 200 ms | Passing | Near/right sandal planted under root; far/left knee bent and sandal clearly raised near `(750,1020)`; far arm back, near arm forward | One call made; far foot is airborne, while its screen-forward placement differs from the guide; parent review pending |
| F03 | 300 ms | Up | Far leg continues forward, small body rise | Not generated |
| F04 | 400 ms | Far contact | Far foot lands lower-right; near leg trails | Prior F04 attempts failed and remain evidence only; no 004 generation planned |
| F05 | 500 ms | Down | Settle onto far support | Not generated |
| F06 | 600 ms | Passing | Near foot swings forward; far/left support remains planted | Not generated |
| F07 | 700 ms | Up / seam | Near leg advances toward F00; close the planned timing seam | Not generated |

F02 should flow from the F01 near-support down pose toward the later far contact, with F07 returning toward F00. The returned F02 raw is a single diagnostic frame only; no full-loop continuity has been established. The F01/F03/F04/F07 continuity is a phase plan only. No other frame, in-between, fanout, integration, or loop-quality claim is authorized here.
