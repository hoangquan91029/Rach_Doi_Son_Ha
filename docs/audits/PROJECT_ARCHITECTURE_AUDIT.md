# Kiểm toán kiến trúc dự án — workflow488

Ngày: 2026-10-12. Vai trò A; GPT-6.1-sol / low. HEAD đọc được: `d26cf7555f634b1bfcf65153c22e503d95e14ce7`. Phạm vi: kiểm tra mã và tài liệu hiện có; không chạy game, browser, build, test suite, image generation hay thao tác production. **Tests thực chạy trong audit: NONE.** Đây không phải chứng nhận runtime hoặc hoàn tất RTS.

## Preflight và quy tắc chứng cứ

Đã đọc AGENTS.md, NEXT_STEPS.md, PROJECT_STATUS.md, docs/PROJECT_PLAN.md, phần vai trò A trong attachment `67e8182e-9b4e-4cfb-9fce-5b607dec7943/Pasted text.txt`, và các directive `docs/art/pipeline/MOVEMENT_PRODUCTION_PLAN_20261010.md`, `PURE_2D_CHARACTER_PIPELINE.md`, `REVIEW_PRIORITY_20261008.md`. Chỉ sở hữu report này. Git ban đầu có thay đổi486 tại AGENTS/NEXT_STEPS/PROJECT_STATUS/PROJECT_PLAN, movement plan, identity/ledger, sprite-prompts, test tương ứng và thư mục infantry-F4-target-edit-486; không sửa chúng.

- **VERIFIED**: thấy trực tiếp trong mã/file hoặc phép đếm chỉ đọc của audit; không đồng nghĩa chạy thành công.
- **DOCUMENTED_ONLY**: receipt/tài liệu đã ghi, chưa tái hiện trong audit này.
- **INFERRED**: suy luận từ mã, cần thực nghiệm.
- **PROPOSED**: hướng xử lý chưa được triển khai/duyệt.
- **UNKNOWN**: chưa có phép kiểm chứng đủ phạm vi.
- **FAILED**: thất bại có chứng cứ lịch sử; không phải lỗi mới phát hiện qua chạy test.

## Kiến trúc đã xác minh bằng source

| Thành phần | Chứng cứ chính xác | Kết luận và giới hạn |
|---|---|---|
| Ngôn ngữ/build | `package.json:1`; `vite.config.js:1-2` | VERIFIED: JavaScript ES modules, Vite build target ES2022, CSS/HTML web client; dependency ws và Playwright. Script dev/build/start/test tồn tại. Không thấy engine thương mại/framework scene được dùng trong các entrypoint đã đọc. |
| Renderer | `client/renderer.js:33-36,66-70`; `client/main.js:51,56` | VERIFIED: Canvas2D main/minimap, camera, raster pipeline, terrain cache, render theo requestAnimationFrame; còn nhánh hình vẽ procedural khi không có art. Runtime hiệu năng/độ đẹp UNKNOWN. Không phải WebGL batching engine. |
| Zoom thực khi launch | `client/world-presentation.js:4`; `client/main.js:51`; `client/renderer.js:33` | VERIFIED: launch đặt NORMAL_ZOOM=1.68; constructor zoom=1 không phải mặc định gameplay cuối cùng. |
| Scene/entity | `shared/sim.js:43-65,398-410` | VERIFIED: plain-object match state, entity array, kind unit/building, IDs, order/path/cargo/queue, vòng tick và view lọc fog. Không phải ECS framework. |
| Roster/building/maps | `shared/data.js:5-29,32-44,53-58` | VERIFIED: 11 unit roles gồm King/General; 12 character definitions; hai map64×48; terrain tác động navigation; building definitions/training/healing/storage. 9 ordinary +12 leader art identities khác với số entity/role chiến trường. |
| Combat/defeat | `shared/sim.js:222-270,398-406` | VERIFIED: damage/armor/terrain, pending attack windup/impact/recovery; resolve impact sau movement/visibility; General chết đặt winner đối thủ tại231. Kết quả cân bằng và tất cả tình huống combat UNKNOWN. |
| King/General | `shared/sim.js:46,53,192-216,231`; `shared/data.js:32-44` | VERIFIED: character selection, passive/ability cooldown/effects; King thay residence, General là điều kiện thua. Không kết luận đủ sprite12 leaders từ gameplay code. |
| Economy/logistics | `shared/sim.js:50,154-155,172-175,274-301,307,316` | VERIFIED: wood/iron tài nguyên người chơi, food tổng từ stores, gather/carry/deposit, food supply/starvation, wagon chuyển food, production queue/build/repair. Animation không được quyết định cargo hoặc tiến độ. |
| Naval/transport | `shared/data.js:15-16`; `shared/sim.js:67,157,208-212,283-294,326-360` | VERIFIED: naval terrain constraints, coastal shipyard, embark/unload/capacity, AI landing state machine. Không suy ra warship art hoàn chỉnh hoặc mọi landing đã pass. |
| Single Player AI | `shared/sim.js:51-53,326-399`; `client/main.js:53-56` | VERIFIED: shared step dùng offline, AI economy/military/logistics/naval và difficulty branch tồn tại. UNKNOWN: khả năng hoàn tất match, chất lượng chiến thuật, dense stress hiện tại. |
| Online 1v1 | `server/index.js:7-8,22-31,62-111` | VERIFIED: hai seats, lobby/ready/configure/commands/rematch, server gọi command/step authoritative; 20Hz tick từ data:2 và snapshot mỗi4ticks (~5Hz), gửi view riêng theo player. Không truyền animation-frame stream. |
| Reconnect/bảo vệ | `server/index.js:35,52-61,73-88,97,104-119`; `client/main.js:45` | VERIFIED: random token rotation, grace/pause/disconnect defeat, rate/payload/connection/room bounds, backpressure, path/origin checks. Đây không phải security penetration audit; các giới hạn có code không chứng minh vận hành an toàn toàn diện. |
| Asset loading | `client/art-routes.js:13-19`; `client/art-bank.js:3-11`; `shared/art-bank.js:10-23`; `client/art-assets.js:53-58,64-94,127-129` | VERIFIED: bareURL chọn fort/world; encoded64MiB và decoded128MiB, checksum, timeout, epoch/dispose và opt-in deferred/LRU. Recipe dùng toàn manifest rồi lọc scope; scope gồm mọi unit/building và selected leaders. Không phải mọi source asset luôn được chọn bất kể scope; vẫn là conservative bank, chưa load theo action/visible roster. |
| Testing/performance tools | `tests/` có69 file qua `rg --files tests | wc -l`; `scripts/profile-simulation.mjs:28-47`; `scripts/benchmark-simulation.mjs`; `scripts/browser-performance.mjs`; `server/benchmark-network.js` | VERIFIED: hạ tầng test và profiling CPU/shared sim/network/browser hiện hữu. Không chạy chúng nên không có PASS mới, FPS mới, memory thực hay rooms load mới. |
| Deployment | `server/index.js:35-50,121-124`; `vite.config.js:2`; `server/DEPLOY.md` | VERIFIED code: Node phục vụ dist và /ws, dev proxy /ws,/health. DOCUMENTED_ONLY: public451 và immutable230 theo entrypoint; PID3408 là historical observation, chưa inspect live. Không đồng nhất source hiện tại với production binary. |

## Coverage và ngân sách: phép đo chỉ đọc

VERIFIED: đọc `public/assets/art-v1/fort-202-manifest.json` bằng Node cho51assets,41unique runtime path+SHA images và19,301,888bytes RGBA (`sum(width×height×4)` mỗi unique image); đây không phải41atlases hoặc bộ nhớ browser thực. `public/assets/art-v1/manifest.json` là route pilot14assets, không được dùng để đếm canonical fort. `client/art-routes.js:13-19` xác định khác biệt này.

DOCUMENTED_ONLY: `docs/art/pipeline/unit-coverage-472/COVERAGE.md:3,7` ghi1080 applicable slots/7104frames,3exact animations/397static fallbacks/680missing, full target495,120,384bytes trước slack và non-unit assets. Report coverage không được chạy lại vì CLI có ghi output. VERIFIED phép đọc manifest: cả51assets có `asset.loadPolicy` undefined,0`on-demand`,0`eager` khai báo tường minh; mặc định pipeline là eager. Code deferred tồn tại nhưng policy hiện tại chưa bật. UNKNOWN: peak decoded/encoded/GPU/canvas overhead và offline availability full roster. Không cộng inventory raw thành download/VRAM budget.

## Đã có, chưa hoàn thiện, thất bại và điều cần giữ

**VERIFIED code exists:** core RTS economy/combat/logistics/naval/AI/online đã hiện hữu; không có cơ sở đề xuất thay engine hoặc viết lại gameplay. Animation framework, registry, timing và cache là lớp mở rộng quanh shared simulation.

**DOCUMENTED_ONLY partial:** PROJECT_STATUS.md ghi controls479/480/484 và focused tests lịch sử thành công, nhưng continuous motion/contact/stride vẫn mở; all-action×D0–D7 chưa hoàn thành. Warship và10world leader identities còn thiếu theo active plan. Không có live visual audit trong lượt này để xác nhận lại hình ảnh.

**FAILED historical:** orders482/483/486 HELD/CLOSED do contact/leg exchange,0selected. Correction caps và one-call authorization đã tiêu thụ theo AGENTS/current receipts. Không mở lại order hoặc biến sửa validator chưa gọi thành một lần imagegen đã thành công. Không phát hiện lỗi runtime mới bằng thực thi trong audit này.

**UNKNOWN:** current live rooms/process/public hash, external WAN desktop, dense full roster, cả hai mode/map end-to-end, gameplay edge cases, complete asset page recovery. Không thể ghi “works” cho các mục này chỉ từ source hoặc receipt cũ.

**PROPOSED preservation:** giữ Canvas2D/sharedsim20Hz/server authority, immutable original artwork, same identity/direction idle fallback rules, deferred cache budgets, whole-family pivot/scale, command ownership/fog filters, historical HELD custody, production451+230. Không thay tốc độ combat/movement để che cadence; không inject state/facing/command để tạo test đẹp.

## Rủi ro kiến trúc và bước tiếp theo

1. **INFERRED — full roster không thể eager preload:** target RGBA vượt128MiB; scope bank hiện còn conservative. **PROPOSED:** chọn page unit/action và dense visible working-set test dưới ngân sách cũ, gồm cold hit/death/load/unload; không nâng budget cho qua.
2. **INFERRED — central sim/main/renderer dễ gây coupling:** nhiều gameplay/UI/render branches chung file. **PROPOSED:** adapter nhỏ cho presentation/asset metadata; không rewrite gameplay trong phase audit. Episode/timing từ sim là nguồn chân lý, visual chỉ lấy mẫu.
3. **DOCUMENTED_ONLY — reusable production chưa chứng minh:** technical compiler/browser controls không chứng minh contact hoặc reuse qua hai identities. **PROPOSED:** trước fanout, qualifying existing same-original pilot bằng brief game-size loop; giữ failed order closed. Villager demonstration theo yêu cầu mới cần parent reconcile với active infantry gate và explicit one-call consumption; không tự khởi chạy generation.
4. **INFERRED — source/public khác phiên bản:** shared cosmetic metadata478 đòi paired release theo current instructions. **PROPOSED:** future isolated exact build, source/build seal và paired rollback451+230; chưa deploy trong phase này.
5. **UNKNOWN — scale acceptance:** test scripts tồn tại nhưng không có mới đo. **PROPOSED:** sau candidate đủ art, runtime tests đúng scenes, dense browser+rooms, pause/reconnect/arrival và memory lifetime; một pass hẹp không đóng full RTS.

## Lệnh đã thực chạy và giới hạn

Read-only: `git status --short`, `git rev-parse HEAD`, `cat`/`sed`/`nl -ba` entrypoints/directives/source, `rg --files`, `rg -n` với tên hệ thống, `rg --files tests | wc -l`, Node inline chỉ parse/đếm manifest. Một search dùng `src/` thất bại vì repo dùng `client/`; đã sửa discovery, không suy ra source thiếu. Các output dài bị truncate đã được theo bằng reads ngắn trọng điểm. Chỉ tạo report này bằng heredoc; không chạy test/build/browser/server, không sửa gameplay/asset/manifest/dirty486, không commit/deploy. Evidence đọc mã cho kết luận architecture có độ tin cậy cao; behavior/performance live và visual acceptance vẫn UNKNOWN hoặc DOCUMENTED_ONLY như ghi trên.
