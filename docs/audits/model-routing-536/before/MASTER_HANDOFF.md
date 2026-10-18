# MASTER HANDOFF — Rạch Đôi Sơn Hà

**Đọc file này đầu tiên khi chuyển sang chat mới.** Bản bàn giao ngày 13/10/2026, từ chat `01a1159b-f20c-75d2-8030-3f4d27119543`. Đây là bản tổng hợp để tiếp tục công việc, không phải bằng chứng dự án hoàn thành hoặc quyền gọi ảnh không giới hạn.

## 1. Mục tiêu và quyết định mới nhất

Repo: `/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha`.

Mục tiêu: hoàn thiện game RTS lịch sử Rạch Đôi Sơn Hà. Người dùng mở **public HTTPS**, không cài đặt, chơi trọn vẹn **Single Player vs AI** và **Online đúng 1v1**, trên cả hai map. Tất cả critical requirements trong master brief, web brief, historical dossier, sections81–145 và sửa đổi sau này phải đạt. **FULL PROJECT: OPEN / INCOMPLETE.**

Ưu tiên mới nhất, cao hơn mọi đoạn lịch sử mâu thuẫn:

1. **KHÔNG DÙNG BLENDER NỮA.** Người dùng yêu cầu gỡ Blender khỏi máy; task508 thực hiện. Không khôi phục model/rig/render Blender, không cài lại để tiếp tục đồ họa.
2. Root phác và chốt khung chuyển động toàn thân có trang phục, kiểm soát contact/passing/pha/chân trụ/chân vung, camera và scale.
3. **Subagent tạo hình: `gpt-6-luna`, reasoning `high`.** Chỉ dùng imagegen tích hợp. Luna là model của worker; không được suy ra model chạy bên trong công cụ imagegen.
4. Code, tooling và review độc lập: **`gpt-6.1-sol`, reasoning `low`**. Tối đa3worker+root, mỗi worker sở hữu file/slot riêng. Ngoại lệ được người dùng yêu cầu riêng: Luna High gỡ Blender.
5. Đúng nhân vật gốc, đồ họa minh họa chân thực có chiều sâu kiểu RTS2.5D. Không biến thành người mới, mannequin hoặc các khối hình học sơ sài.
6. Chuyển động tự nhiên, mượt ở kích thước chơi quan trọng hơn nếp áo/pixel/chi tiết giải phẫu. Một lượt xem loop ngắn, sửa lỗi nhìn thấy; không audit vi mô nhiều vòng.
7. Không hỏi lại API key. Không có API key; dùng tạo ảnh có sẵn, không API/CLI trả phí hoặc backend khác tự phát.
8. Không polling quota, không dừng theo phần trăm/reset. Lỗi provider thật phải ghi nhận; không giả thành task hoàn thành hoặc đổi model âm thầm.
9. Tường thành **đá**, chỉ thẳng/góc; **cổng gỗ**; các asset gỗ khác giữ nguyên. Xe lương giữ **ngựa+dây kéo+xe+hàng** của whole artwork415.
10. Dân làng mang tài nguyên về dùng walk thường. Không tạo bộ carry riêng.

## 2. Cách tiếp quản — không đọc lại toàn bộ lịch sử

1. Đọc file này, `AGENTS.md`, phần đầu `docs/PROJECT_STATE.md`, `docs/NEXT_STEPS.md`.
2. Kiểm tra `git rev-parse HEAD`, `git status --short`, diff liên quan. **Giữ nguyên toàn bộ dirty/untracked**, không reset/clean/stash.
3. Đọc `docs/agent-read-contract.json`, `docs/AGENT_EXECUTION_CONTRACT.md` và source/receipt đúng phần sẽ làm. Không coi số checkpoint là lệnh đang mở.
4. Kiểm tra task registry, claim chưa settle và process thực. Worker của chat cũ không mặc nhiên là worker của chat mới. Không gọi lại một ảnh vì không nhớ kết quả.
5. Dùng preflight thật: `node scripts/agent-preflight.mjs --task audit --source <repo-relative-file>`; task art/runtime/release theo scope thực. Hash chỉ xác minh bytes.
6. Root đăng ký ownership, input pins, slot/call budget trước dispatch. Không đăng ký retroactively rồi gọi đó là đã kiểm soát từ đầu.
7. Làm bước chưa hoàn tất ở mục7. Không audit lại mọi thứ, viết lại engine hay chạy lại full match chỉ để tạo receipt mới.

Nguồn authoritative sau bàn giao: PROJECT_STATE sở hữu sự thật hiện tại; PROJECT_ROADMAP sở hữu milestone; NEXT_STEPS sở hữu queue; COMPLETION_MATRIX sở hữu requirement trace. File này là snapshot/handoff, không được dùng để phủ nhận source mới đã kiểm chứng. Những đoạn cũ bên dưới các tài liệu vẫn ghi Blender hoặc universal Sol-only là lịch sử đã bị thay thế.

## 3. Git, tiến trình và bằng chứng tại bàn giao

- HEAD quan sát: **`1c7097fc80f94fc87f2fdc97d355e414601c37a4`**.
- Nhiều thay đổi504–507 **chưa commit**, nằm trong checkout này; không phải source ở HEAD. Bao gồm tài liệu, task registry, helper/tests, receipt/profile và Blender thử nghiệm thất bại. Đừng tạo worktree từ HEAD rồi tưởng đã mang theo dirty work.
- Snapshot chi tiết dirty paths và SHA nguồn quan trọng nằm ở phần cuối file này.
- Actual goal tool trong chat cũ báo **paused**. User đã cho tiếp tục foreground và yêu cầu chuyển chat. Không nói background goal ACTIVE khi tool chưa xác nhận. Goal/automation của thread cũ không tự chuyển sang thread mới; không tự tạo duplicate automation.
- Automation311/five-hour schedule vẫn chưa xác minh. Không tuyên bố đã lên lịch, không tái tạo khi chưa inspect.
- Trước task508: Sol capability worker terminal; hai Sol worker code/review kết thúc bằng lỗi usage limit ở follow-up. Root đã tiếp tục các sửa đổi và test liên quan; independent review cuối của key-study code còn thiếu. Không tự suy ra quota/model ở chat mới.
- Production quan sát có process Node immutable230. PID chỉ là snapshot; tuyệt đối không restart PID cũ. Bản public451frontend+230backend là baseline documented, chưa phải release hoàn chỉnh hiện hành đã nghiệm thu.
- MCP Blender là app-owned process; task508 gỡ theo exact ownership. Kết quả gỡ được cập nhật mục14 trước bàn giao; không dùng ghi chú “intentionally running” cũ để tự bật lại.

### Những gì đã có và giới hạn

| Phần | Quan sát | Chưa được suy ra |
|---|---|---|
| Engine | ES modules, Vite, Canvas2D IsoRenderer, shared fixed tick, Node/WebSocket | Không cần rewrite; code presence không chứng minh production |
| Action runtime | Atlas/pivot, distance walk, action clocks, hit/death/attack marker, ability/load/unload metadata | Clip/identity còn thiếu; runtime PASS không là motion PASS |
| Scope art | 21identity, 135actionbank, 1.080clip, 7.104frame positions theo Standard | Đây là workload, không call budget |
| Coverage audit | 3loop,397static fallback,680missing;10world master có nguồn,11thiếu;11/168neutralview có nguồn | Snapshot audit, source availability không là acceptance |
| Villager work | Owner032wood/141iron chấp nhận đúng loopD1 đã cho xem | Không chấp nhận walk,food,8hướng hoặc unit khác |
| Villager walk | Owner từ chối490;491/492held/closed;213/233có technical history | Chưa có owner acceptance mới/stride/world foot lock/fanout |
| Blender501/504 | Runtime/render có chạy; hai model đều sai original và HELD/CLOSED | 0selected model/rig/walk; không retry, nay bỏ route |
| Loader493 | Local on-demand nonidle decode, actual Chrome/Firefox offline-after-menu | Không phải full roster offline hoặc dense LRU qualification |
| Cache496 | requiredOwners sửa lease giữ encoded cache sai qua epoch; scoped tests và actual3map epochs/browser | Chưa chứng minh toàn7104frames/targetGPU |
| Wall495 | Shared degree≤2 ở candidate+neighbors, gồm unfinished; actual line/corner/T rejection | Chưa paired public release; giữ source local |
| Profile504 | Local2human Delta100TOTAL=50/side,60.9s; p95rAF33.2/33.3ms | Không100unit cùng viewport, không dense battle/targetGPU/public/WAN |
| Observer505 | Fix false-positive queue binding; actual11tests pass, replay71accepted/3UNKNOWN | Raw504 từng có5pass1fail dù worker ghi6pass; giữ cả lỗi/claim sai |
| Profile506 | Bị ngắt, không final receipt200; code/log còn | Không complete, không game failure, không tự chạy lại order cũ |
| Key-study507 | Candidate contract mới + model routing; root integrated46checks pass | Chưa gọi imagegen, chưa có joint output/selected frame/loop |

Receipt chính: `docs/audits/continuation-504/root/CHECKPOINT.json`; `docs/qa/online-profile-504/receipt.json`; `docs/qa/online-profile-505/CHECKPOINT.json`; `docs/audits/animation-context-507/root/tests-integrated.log`.

## 4. Phân tích lỗi animation và hướng đang chọn

GPT Image có thể minh họa/biến đổi ảnh nhưng công cụ tích hợp không cung cấp rig, timeline, constraint chân, identity latent cố định hoặc seed/mask control đảm bảo. **Không kết luận đơn giản là quên frames.**491 thực tế đã nhận originalSouth, hai contact neighbors và whole-clothed guide mà vẫn sai passing.492guide-first cũng sai pose/scale.

Một ảnh đẹp không đồng nghĩa hai ảnh nối được thành chuyển động. Thêm “preserve identity” vào prompt không chứng minh output giữ identity. Tooling không đảm bảo hình học; đổi sang Luna cũng không tự chữa motion.

Hướng tiếp theo được user đồng ý: root phác toàn chu kỳ → Luna minh họa dựa trên original và phác đã chốt → key/in-between → loop → game.507 nghiên cứu **một sheet chung bốn key F0/F2/F4/F6**, để model thấy những pose đối nhau trong cùng generation context. Đây là thay đổi so với các call độc lập491/492; **chưa chứng minh hiệu quả**. Không tạo hàng loạt trước pilot.

Nguồn nghiên cứu đã đọc được lưu tại `docs/audits/continuation-504/root/IMAGE_ANIMATION_DECISION.md`:
- OpenAI image generation: reference/multi-turn có hỗ trợ nhưng consistency/composition vẫn có giới hạn. API controls không mặc nhiên dùng được trong builtin.
- AoE official: 2D engine có thể dùng hình render từ3D. Đó là thông tin về game tham khảo, không cho phép quay lại Blender sau quyết định mới.
- Krita: keys/in-between/onion-skin là quy trình tổ chức animation; cài tool không đồng nghĩa có khả năng authoring đã kiểm chứng.

## 5. Workflow tái sử dụng và prompt

### Năm lớp

**Identity → motion → projection → whole illustration → runtime.** Reuse motion rules, job/compiler/preview và cách điều phối; không lấy chân tay/body pixels của unit khác.

Identity giữ original/view, face/bodyvolume, costume/palette, equipment và tay cầm vật lý, camera/light/layout/shadow. Hướng chưa có nguồn vẫn thiếu. Không mirror để lấp8hướng.

Root phác whole-clothed guide của chính unit, không mannequin khác; guide là aid, không final art hoặc proof của foot lock. FootA/B có landmark cố định; tách physical side khỏi screen side. Không khóa cứng torso: cho phép trọng lượng, nhún thân, tay và vải tự nhiên.

### Walk8frame

| Frame | Intent |
|---|---|
|F0|A tiếp đất, bắt đầu nhận trọng lượng|
|F1|Nhận trọng lượng A, thân hạ nhẹ|
|F2|A trụ; B đi qua, nhấc khỏi đất|
|F3|B vươn tới contact tiếp|
|F4|B tiếp đất, đối chân F0|
|F5|Nhận trọng lượng B|
|F6|B trụ; A đi qua|
|F7|A vươn tới F0; seam liền|

Mọi hướng của cùng unit dùng chung pha vật lý. Attack dùng chuẩn bị→contact/fire→hồi; work dùng tác động→theo đà→hồi; death kết thúc nằm yên; ability/load/unload có pose riêng. Không invent gameplay để có ảnh.

### Trình tự một action package

1. Reuse nguồn hợp lệ; loại held/rejected khỏi selected references.
2. Khóa identity/view/camera/equipment/layout và toàn chu kỳ.
3. Phác và kiểm tra hai contact đối chân, rồi passing keys.
4. Giao Luna High bộ nguồn đã pin và finite slot. Không tự giao direction/unit ngoài order.
5. Nhập raw/tool-result đúng mapping; source hash+RGBA hash. Không đoán model/time/seed.
6. Chỉ khi key đạt mới tạo in-between từ hai selected endpoints + immutable original + cycle context. Không chỉ nối tiếp bằng output mới nhất, dễ tích lũy drift.
7. Compiler chung xuất atlas/descriptor/contact sheet/preview; runtime128 và working256 đều trực tiếp từ raw theo một transform family.
8. Một loop10–15s ở gameplay size; sửa visible identity/phase/scale/tool jump/seam/sliding trong budget.
9. Actual Move/turn/PauseResume/assigned-arrival/Stop/idle, rồi action/hit/death liên quan.
10. Root chọn và ghép manifest, cập nhật coverage. Một package một receipt; không checkpoint riêng từng frame.

Một frame thông thường = một whole-frame call. Nhánh507joint-key là exception nghiên cứu đã version riêng: một request, một raw sheet, bốn **candidate cells**, không bốn selected frames. Hoàn tất contract/intake trước gọi. Chỉ crop toàn cell theo grid chung nếu output đủ điều kiện; không ráp limb/warp/fit từng cell. Không hạ counters hoặc đổi tên method để retry.

### Prompt dùng chung cho Luna

```text
TASK: Illustrate the SAME original unit using the root-selected movement guide.
IDENTITY: exact original + selected directional view (actual image inputs).
MOTION: exact whole-clothed guide and slot/phase; named physical A/B landmarks.
CONTINUITY: selected neighboring keys and complete cycle context, if applicable.
KEEP: same face, body volume, hat, costume, palette, equipment ownership,
      camera, light, fixed canvas/pivot/family scale.
CHANGE: the specified contact/support/swing, weight transfer and tool motion.
OUTPUT: one complete illustrated transparent frame (or the explicitly ordered
        joint-key study), no redesign, mirror, limb assembly, warp or frame fit.
Return raw output/tool mapping. Do not self-award motion/runtime/owner approval.
```

Các placeholder phải được điền bằng dữ liệu thật. File thực thi template: `docs/art/pipeline/unit-production/templates/`; chuẩn bị qua `scripts/sprite-prompts.mjs`; claim/settle qua `scripts/sprite-order-run.mjs`. Không tự chế tool parameters.

## 6. Pilot hiện tại: nguồn, layout và phần code dang dở

OriginalD0: `docs/art/characters/villager-neutral-D00-screen-ESE/raw.png`
SHA256 `145b976ffd1bdf563cb5da78806547e6849424054f2c26fc297e155a0b366e94`.

Selected neutralSouth/D1 appearance only: `docs/art/characters/villager-neutral-D01-screen-South-007/raw.png`
SHA256 `68a7fb9a71ae614f7c01432b1270e7a25071975667cfdf082ae02326d97678db`.

Existing root-authored guides: `docs/art/pipeline/villager-pose-control-491/guide/F0.svg`…`F7.svg` cùng PNG/landmarks. Reuse rather than redraw unnecessarily. PhysicalA image-right lane146, B image-left lane116 trong256 guide; anatomical side chưa khẳng định. Reviewer507 khuyến nghị F0/F2/F4/F6 row-major. Tham khảo `docs/audits/animation-context-507/review/MECHANISM.json`.

**Chưa tạo bảng2×2 mới, chưa tạo8frame mới, chưa có Luna worker/output tại thời điểm handoff.** Không biến lời commentary “đang gom” thành output đã có.

Key-study code candidate:
- `scripts/sprite-key-study.mjs`: one request/four-key mapping,256cell, fixed layout, selectedview/original/registeredguide, provenance and physical-motion descriptions.
- `scripts/sprite-prompts.mjs`: branch mới cùng existing action/view/building branches; `preparePrompt` tự do không được dùng cho key-study; trusted `prepareOrder` có guarded check.
- `docs/art/pipeline/unit-production/templates/key_study.txt`.
- `tests/sprite-key-study.test.js`.
- `scripts/agent-task-contract.mjs`: SolLow mặc định; LunaHigh chỉ `workKind:image-generation`, hoặc exact authorized removal508. Model label không cấp call.
- `tests/agent-task-model507.test.js`.

Root đã sửa yêu cầu motion text,256cell và guarded prepare; worker follow-up bị lỗi provider. Root combined46checks actualPASS; receipt worker32checks/output hashes là bản trước một số sửa đổi, **không dùng stale hashes để chứng minh final code**. Independent code review cuối chưa xong; fixture PASS chưa chứng minh dispatch thật.

Layout humanoid: working256/runtime128, padding2, không trim/rotate/fit. Legacy raw1254 giữ nguyên. Guide pivot normalized từ654,1140/1254 →133.51196,232.72727/256. Giá trị render42×zoom1.68=70.56px là **canvas**, không body height; đo body riêng. Runtime/source layout candidate phải bind đúng job, không gán guide provenance giả. Guide600ms/124px travel không phải stride đã đo trên finished art.

## 7. Những việc làm ngay khi tiếp quản

1. Hoàn tất intake task508 gỡ Blender; cập nhật kết quả thật, không cài lại. Giữ tất cả repo art/history.
2. Đọc diff key-study507 và log46checks; independent SolLow review phần còn thiếu. Không viết lại helper/engine. Chỉ chạy lại test nếu có sửa hoặc concern thật.
3. Root chuẩn bị bảng phác2×2 từ whole-clothed guides đã có, thống nhất physical roles và whole-cycle provenance. Kiểm tra ở gameplay size một lần. Không cần hỏi user duyệt từng frame.
4. Chốt đúng typed job/layout/guide pins. Đăng ký LunaHigh task và finite order **một joint-key call, zero correction cho thử nghiệm này** sau khi mọi prerequisite hợp lệ. Chưa có order nào được mở cho study507.
5. **Blocker cụ thể:** global `--task art` preflight hiện từ chối vì2unresolved498claims. `scoped-art-preflight507` chỉ là PLAN_ONLY, đã đóng, chưa dispatch/chưa code. Không nói scope bypass đã tồn tại. Không đổi task art thành audit để gọi ảnh. Giải quyết custody bằng kết quả thật, hoặc thiết kế/review explicit disjoint-task guard preserving old claims nếu được tiếp tục trong scope; không xóa claim hoặc giả settle để thông qua.
6. Nếu study giữ đúng original và contact/passing dùng được, chỉ hoàn thiện slots còn thiếu. Nếu sai giống cũ, hold output và dừng method, không loop prompt/seed vô hạn.
7. Sau loop/travel đạt mới mở hướng/unit; chứng minh reuse trên Infantry và horsewagon/cavalry.
8. Khi art đang phụ thuộc, làm phần game/world/performance chưa có bằng chứng theo scope mới; không replay fullmatch hoặc profile đã hoàn tất.

## 8. Những claim/order không được gọi lại

- Infantry482/483/486, Villager491/492: CLOSED/HELD, consumed; không rename/reorder để làm lại. Owner490 rejection vẫn hiệu lực.
- Infantry469 output đã có: không generate lại.470/477/479 và các source hợp lệ giữ nguyên.
- Blender501/504: failed identity,0selected;506partial code chưa render; nay route bị user bỏ.
- Residence order **`residence-construction-F1-F3-498`**, callsUsed2/remaining0, OPEN custody:
  - slot1 token `c39d4f3a-afe4-4dba-bd98-1e71de33e2c9`;
  - slot3 token `1166301b-86da-497a-a3b7-4787f7c5df22`.
  - Không provider handle hoặc exact output mapping;507bounded lookup không khôi phục được. Filenames/timestamps/ảnh giống không là mapping. Không retry/refund/close theo elapsed time.
  - Ledger SHA quan sát `a687d7b292859ff5ef7b973001c2ae1308ec3fcf1023db160ac1f1792d3ce7b4`, lock absent tại kiểm tra. F0/F2Residence có source nhưng chưa complete clip.

## 9. Toàn bộ kế hoạch còn lại

| Gate | Công việc | Điều kiện đóng |
|---|---|---|
|G0|Chỉ dẫn/ownership/finite orders/provenance/coverage nhất quán; hoàn tất507|Không giao lại việc đã làm; checks đúng scope; không stale claims/false PASS|
|G1|Root-authored2D motion guide → Luna whole illustration pilot mechanism|Actual original-preserving keys usable; không xét cài tool/schema là thành công|
|G2|VillagerD1walk hoàn chỉnh|Đúng identity, loop tự nhiên, measured stride, actual travel/turn/Pause/Stop, owner phản hồi đúng phiên bản nếu cần thay rejection|
|G3|Infantry rồi wholehorsewagon415/cavalry reuse|Motion thật; đo newcalls/first-pass/corrections/held/reuse/time, không tính reused frames là newsuccess|
|G4|Đủ từng identity, action×D0–D7|Source+motion+runtime, mọi alias có chủ đích; static fallback không hoàn tất|
|G5|Building lifecycle, stonewall/woodgate, hai map hoàn thiện|Hình riêng đúng state, readability/occlusion/picking/routes; mechanics tương ứng local+paired release|
|G6|Working set, dense browser, live room capacity|128MiBdecoded/64MiBencoded; profile thật trên hardware mục tiêu; không nới cap hoặc giảm simspeed|
|G7|Accepted default graphics + paired production + final acceptance|BareHTTPS,clean browser,two modes/two maps,full ordinary matches,reconnect/rematch,WAN/device,all critical closed|

G5/G6 độc lập có thể song song G1–G4. Không cần viết lại mechanics đang có nếu chưa tìm thấy gap.

### Action×8hướng bắt buộc

| Identity/archetype | Actions | Frame mặc định/hướng |
|---|---|---|
|Villager|idle,walk,attack,hit,death,wood,food,iron,build/repair|4,8,8,4,8,8,8,8,8|
|Infantry,spearman|idle,walk,attack,hit,death|4,8,8,4,8|
|Firearm|idle,walk,attack gồm aim/fire/reload,hit,death|4,8,8,4,8|
|Cavalry|idle,horse+rider move,attack,hit,death|4,8,8,4,8|
|Artillery|idle,move,fire/recoil/recovery,hit,destroyed|4,8,8,4,8|
|Horsewagon|idle,move,load,unload,hit,destroyed|4,8,8,8,4,8|
|Warship|idle,move,attack,hit,sink|4,8,8,4,8|
|Transport|idle,move,load,unload,hit,sink|4,8,8,8,4,8|
|12leader identities|idle,walk,attack,hit,death,ability,King-onlybuild|4,8,8,4,8,6,8|

Applicability source: `shared/unit-action-spec.js`. Same person shares art between King/General; build role King only. Existing world master thiếu11 là warship+10leaders, không phải11leaders. Portrait không thay world sprite.

12identity IDs: `han_xin`, `xiang_yu`, `napoleon_bonaparte`, `ly_thuong_kiet`, `tran_hung_dao`, `nguyen_hue`, `le_thanh_tong`, `minh_menh`, `nguyen_anh`, `nguyen_phuc_chu`, `tran_nhan_tong`, `trinh_cuong`. Source lịch sử có uncertainties phải ghi rõ. Không sáng tác facts dựa trên portrait.

Thứ tự sau pilot: Villager hoàn chỉnh → Infantry reuse → spear/firearm → horsewagon/cavalry archetype → artillery/transport/warship → lãnh đạo. Unit độc lập có thể parallel sau archetype đạt. Trong một bank, sau view/key locks chia A:D0–D2, B:D3–D5, C:D6–D7; reviewer độc lập hoặc root.

### Game/world còn lại

- AI economy/army/logistics/General protection và ordinary win/lose cả2map cần final exact-release validation; không viết lại từ đầu.
- King/General lựa chọn lịch sử, passive/active/synergy; General chết gây thua. Residence destruction không thua ngay; đúng1Residence gồm construction, chỉKing rebuild sau destruction; villager production/healing radius.
- Villager wood/food/iron, unit production/combat/naval/terrain/fog đều giữ authoritative sim.
- Food consumption/ration/Granary thực inventory/Depot/wagon transport/raid. Woodiron remote deposit theo thiết kế hiện hành; không tự thêm wagonwoodiron.
- Building idle/construction/hit/death và attack khi có mechanics; missingdeath không fallback người/công trình sống đứng yên.
- Stonewall thẳng/góc; chặn newT/cross ở candidate và neighbor ownliving wall/gate kể cảunfinished. Existing không tựdelete. Preview/server cùng quy tắc; reject không mất resource.
- Hai map `delta` River of Two Kingdoms, `coast` Coast of the Mountain Pass: shore/sea/rivers/fords/plains/forest/hills/mountains/ambush/naval/multipleattack/supply routes. Material đã có chưa là final composition.
- HUD/minimap/picking/occlusion/unit family scale ở defaultzoom; không dùng primitive art làm final.

## 10. Runtime, memory và performance

Animation chỉ trình bày simulation. Damage/cargo/cooldown/passengers/outcome do sim quyết định. Walk/wheels theo distance; attackimpact theo authoritative tick; hit/death theo event; finite death giữ finalpose tới corpse removal (hiện4000ms window). Pause/reconnect/tabreturn dùng game time, không cộng frame màn hình bị bỏ lỡ.

Groundstride đo từ cùng physical foot qua stance samples và projection thực. Không lấy guide math làm foot-lock evidence, không copy stride unit khác. Infantry0.15 từng tạo15.33cycles/s ởspeed2.3, không production-qualified. Không đổi speed/facing để che art lỗi.

Giữ128MiBdecoded/64MiBencoded, pages≤2048,padding2,manifest≤2MiB.7.104positions padded≈472MiB chưa tính overhead: stream theo bank, không preload toàn bộ. Test firstuse/actionchange/evict/revisit/map/menu/networkloss với working set thật; warmcache offline khác full reload offline.

Profile target1920×1080,DPR1,defaultzoom; ghi CPU/GPU/RAM/browser thật. Light60FPS, densep95≤33.3ms/p99≤50ms đo60s sauwarmup. Ordinary cohorts20/50/100/200/240 với120/side cap. Server20Hz,1/2/4/8rooms tới admittedcapacity. Synthetic diagnostic không là live-room proof.505queue observer dùng authoritative tick budget; giữ3UNKNOWNoldbindings.506profileinterrupted không tựresume exhaustedorder.

## 11. Kiểm tra và release

- Docs/handoff không fullsuite/fullmatch. Helper change dùng negative tests ownership/stalepins/budget/prerequisite/receipt.
- Một actionbank: integrity/alpha/layout/timing/source + một actualloop. Completedunit: move/turn/Stop/action/hit/death/Pause; Chrome chính,Firefox theo integration.
- Gameplay trial chỉ ordinaryUI và readonly diagnostics. Không inject command/state/facing/winner. Dùng assigned destination và enginearrival0.7, không idealclick0.02.
- Test build ONLY isolated cwd + explicit Viteconfig + absoluteoutDir; không ghi active dist. Freeze trước browser preservation guard; không canonical mutate giữa trial.
- Sharedsim local đã khác public. Future release phải pairedfrontend+backend, exactsource/build/rollback/currentrooms; không kickrooms/historicalPIDrestart.
- Current rollback documented: `docs/qa/paired-release-preparation-496/CHECKPOINT.json`; actual451front209files/50assets +immutable230/ws8.22.0. Archive outsideGit:
  `/home/kieu-hoang-quan/.local/share/rach-doi-son-ha/releases/paired-451-230-496-v4b02zpt/rollback451-230.tar.gz`
  SHA `f6de28c98786c88c7c263500fae2fbe96ca2b4c23247e8d771508154efe895ef`.
- Reinspect live service/Funnel/public URL/rooms before release; no publicHTTPS smoke performed in this handoff. Do not guess current URL from oldchat or claim livehealth from oldreceipt.
- Final4ordinary matches: SP/Online ×Delta/Coast. CleanHTTPSChrome/relevantFirefox; online2realclients/invite/ready/disconnect/reconnect/victorysync/rematch; externaldesktopWAN/device. BareURL uses acceptedart, no experimental query required. All critical matrix rows closed before COMPLETE.

## 12. Evidence, task handoff và chống suy diễn

Evidence states: VERIFIED, DOCUMENTED_ONLY, INFERRED, PROPOSED, UNKNOWN, FAILED. Tách source/technical/motion/runtime/owner/release. Test filename,counter,prompt,PNGdimensions/hash không là motion approval. Samples không là continuousreview; localhost không là WAN; raw tool output không là selectedsource.

Root registers `docs/audits/implementation-495/tasks.json`; inputs/scopedSHA, exclusiveoutputs/slots, actualtools, finitebudget, prerequisites, stopconditions. No overlap kể cả parentdir/symlink. Reviewer khác producer. Unknown output stays unknown. One action package one receipt. Preserve firstfailure andrepair; đừng chạy lại chỉ để có “clean PASS”.

Return mỗi task: actualoutput/hash; command/cwd/log/exit; failures/unknown; calls/held; handles; nextdependency. No claimed automatic protection against every shellwrite or hallucination.

## 13. Tài liệu/source tìm nhanh

- `AGENTS.md`, `docs/PROJECT_STATE.md`, `docs/NEXT_STEPS.md` — current authority/state/queue.
- `docs/PROJECT_ROADMAP.md`, `docs/COMPLETION_MATRIX.md` — plan và trace master/81–145.
- `docs/audits/implementation-495/requirements/source-index.json` — originalbrief custody; không chỉ dựa summary.
- `docs/AGENT_EXECUTION_CONTRACT.md`, `docs/agent-read-contract.json`, taskregistry495 — dispatch.
- `docs/art/pipeline/ANIMATION_CONTRACT.md`, `SPRITE_PRODUCTION_WORKFLOW.md`, `IMAGE_GENERATION_TEMPLATES.md`, `ANIMATION_ARCHETYPES.md`, `ASSET_QA.md` — production.
- `docs/art/pipeline/unit-production/` — identities/jobs/templates/order-ledger.
- `scripts/sprite-production.py`, `sprite-action-bank.mjs`, `sprite-preview.html`, `qa/sprite-preview.mjs`, `qa/unit-walk-scene.mjs`, `unit-art-coverage.mjs` — reuse existingtools; inspect actualCLI first.
- `shared/sim.js`, `shared/data.js`, `shared/unit-action-spec.js`, `shared/visible-action.js`, `shared/fortification-placement.js` — mechanics/spec.
- `client/art-assets.js`, `client/raster-slice.js`, `client/action-presentation.js`, `client/world-presentation.js` — presentation/banks.
- `server/index.js`, `server/DEPLOY.md` — backend; olddeployprose is notcurrentliveproof.
- `docs/audits/animation-context-507/` — latestmethod/contract/custody/rootchecks.
- `docs/audits/blender-removal-508/` — latest removalactual evidence.

## 14. Blender removal508 — actual outcome

**VERIFIED — REMOVAL COMPLETE.** Exact LunaHigh worker completed removal; root independently confirmed all three directories absent and exact config preservation.

Removed:
- `/home/kieu-hoang-quan/.local/share/rach-doi-son-ha/tools/blender500` — isolated Blender executable/dependencies/package archives.
- `/home/kieu-hoang-quan/.local/share/rach-doi-son-ha/tools/mcp501` — dedicated MCP venv/cache/wheels.
- `/home/kieu-hoang-quan/.cache/blender` — disposable Blender cache.
- Only `[mcp_servers.rds_blender501]` from Codex config. Every raw byte outside that table unchanged, unrelated TOML values equal, mode0600 preserved. Exact current private backup retained outside repo.

Worker observed no remaining owned processes/listener19876, PATH binary or installed Blender/blender-data dpkg package. No system package/driver/systemPython/unrelated app removed. All project art, scripts, .blend scenes and history remain; retained .blend is data, not installed Blender or permission to use it. Codex UI may need ordinary config refresh; do not reconnect/reinstall.

Receipt: `docs/audits/blender-removal-508/worker/PHASE2_REMOVAL.json`. Root check: `docs/audits/blender-removal-508/root/intake.json`. Config afterSHA `5a2f9af10233465c6afcbba37efc9cddae5811147a2b88168132f863e20415ca`. Ledger498 unchanged. Full game still OPEN.

## 15. Prompt để dán sang chat mới

```text
Tiếp quản và tiếp tục hoàn thiện Rạch Đôi Sơn Hà tại /home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha.
Đọc MASTER_HANDOFF.md trước, rồi AGENTS.md và trạng thái/source liên quan. Giữ toàn bộ dirty/untracked; đừng làm lại việc đã xong hoặc gọi lại order đã đóng/chưa rõ kết quả.
Quyết định mới nhất: không dùng Blender; root phác/chốt whole-clothed motion guides, subagent gpt-6-luna reasoning high tạo ảnh qua imagegen tích hợp; code/review dùng gpt-6.1-sol reasoning low. Giữ đúng artwork gốc, ưu tiên chuyển động tự nhiên ở game size. Không API key, không quota polling, không fanout trước pilot.
Hãy kiểm tra bàn giao508, hoàn tất bước507 còn dở và tiếp tục kế hoạch toàn game. Tôi cho phép làm song song trong phạm vi đã nêu; chỉ hỏi khi thực sự thiếu quyết định. Nếu thread này chưa có goal thì đặt goal hoàn thiện toàn bộ project theo handoff. Không tuyên bố hoàn thành cho tới khi public HTTPS chơi trọn cả Single Player và Online1v1 trên hai map cùng mọi critical requirement.
```

## 16. Snapshot bytes/checks tại thời điểm chuyển chat

Root kiểm tra lại **440 protected files đều giữ nguyên** so với baseline504. Snapshot không bao gồm lời khẳng định public/WAN hay chất lượng animation. Tests507 integrated46pass (actual log), tests508model/ownership13pass (actual log); không fullsuite/fullmatch. Ledger vẫn giữ2claims chưa settle.

| File | SHA256 |
|---|---|
| `scripts/sprite-key-study.mjs` | `4e9d9e45d6d1dffdfbeb8da7f1e8a5211b57666d210c0220ad32f9d88d8130e1` |
| `scripts/sprite-prompts.mjs` | `7f0311c91371ce989bdaf852169c641017367b911f094086762b607d4aecc2a7` |
| `scripts/agent-task-contract.mjs` | `ab70ec1dc9e99293a54ea2873cb802ab2745d62942ff80c6fa0cb714ae0a60b1` |
| `scripts/agent-preflight.mjs` | `c39ac0bcd8392b6f995982aa7d0598d67acc8114ebf2e6800a2c44c2126082fe` |
| `docs/art/pipeline/unit-production/templates/key_study.txt` | `65e498f07f6dfa2f0e592a86f27d2e176f2a529a870daa31c0195d89b7b015e9` |
| `tests/sprite-key-study.test.js` | `ffe2c71f41297c4fb54d42866d2c2954c02c8fff704991c92b254fbaa370f364` |
| `tests/agent-task-model507.test.js` | `1f9d330653ec5cc499814779e6644bbd21a9723cf53665169bba2418d4effa91` |
| `docs/art/pipeline/unit-production/order-ledger.json` | `a687d7b292859ff5ef7b973001c2ae1308ec3fcf1023db160ac1f1792d3ce7b4` |
| `scripts/qa/train-observation504.mjs` | `0538fc1723dc2314288310445454362a2532311bb5fe8a41fb93b9b029235780` |
| `shared/sim.js` | `c9a01adba8630e89e1c3f195c1b98c08c32e74468d389a55891c664e3906e562` |
| `server/index.js` | `4e6a7e82f02d1d856f4ea788863c4836930bc00250be6a5b020ba2bdd8884198` |

Dirty snapshot (trước final508 receipt và update bàn giao; không phải danh sách file được phép xóa):

```text
 M AGENTS.md
 M docs/AGENT_EXECUTION_CONTRACT.md
 M docs/ARCHITECTURE_DECISIONS.md
 M docs/NEXT_STEPS.md
 M docs/PROJECT_ROADMAP.md
 M docs/PROJECT_STATE.md
 M docs/art/pipeline/ANIMATION_CONTRACT.md
 M docs/art/pipeline/IMAGE_GENERATION_TEMPLATES.md
 M docs/art/pipeline/SPRITE_PRODUCTION_WORKFLOW.md
 M docs/audits/implementation-495/tasks.json
 M scripts/agent-task-contract.mjs
 M scripts/sprite-prompts.mjs
?? MASTER_HANDOFF.md
?? docs/art/pipeline/blender-villager-504/
?? docs/art/pipeline/blender-villager-506/
?? docs/art/pipeline/unit-production/templates/key_study.txt
?? docs/audits/animation-context-507/
?? docs/audits/blender-removal-508/
?? docs/audits/blender-runtime-500/mcp/isolated-runtime-config/
?? docs/audits/blender-runtime-502/connection/runs/1260828fa04e48d6b4dd4775df70a070/
?? docs/audits/blender-runtime-502/connection/runs/205e1735a77f4da89c1c68e8ea65e287/
?? docs/audits/blender-runtime-502/connection/runs/31ad1b9cef624041b54d0f9c8a10476d/
?? docs/audits/blender-runtime-502/connection/runs/628b44df2ea64e469a62f7ee7622fa68/
?? docs/audits/blender-runtime-502/connection/runs/78c7c0ef24864151b4c4d2afff9a984a/
?? docs/audits/blender-runtime-502/connection/runs/9271d344564342a6936296c576fe3d2a/
?? docs/audits/blender-runtime-502/connection/runs/b48a76aec35e4695bac1f9640e59774c/
?? docs/audits/blender-runtime-502/connection/runs/b5405e4f3c6b478e873a7b95b67b73ed/
?? docs/audits/blender-runtime-502/connection/runs/c91a741082bc4c908a1c4921f6384989/
?? docs/audits/blender-runtime-502/connection/runs/db8bf054007f48c2b60b78d0b6890c95/
?? docs/audits/blender-runtime-502/connection/runs/dff8df9cb52d4a8a8c325f5634ba5dd1/
?? docs/audits/blender-runtime-502/connection/runs/eed04592d0234d6ca9c691fa7308ceb1/
?? docs/audits/blender-runtime-502/connection/runs/f6f9d57ba9e04eae868eff267f8c2333/
?? docs/audits/continuation-504/
?? docs/qa/online-profile-504/
?? docs/qa/online-profile-505/
?? docs/qa/online-profile-506/
?? scripts/blender/villager504.py
?? scripts/blender/villager506.py
?? scripts/qa/online-profile504.mjs
?? scripts/qa/online-profile506.mjs
?? scripts/qa/train-observation504.mjs
?? scripts/sprite-key-study.mjs
?? tests/agent-task-model507.test.js
?? tests/sprite-key-study.test.js
?? tests/train-observation504.test.js
```

Không có commit mới được tạo trong lượt bàn giao này. File MASTER_HANDOFF và các thay đổi vẫn nằm trong working tree; chat mới dùng **cùng thư mục này**. Không giả định có thể checkoutHEAD ở nơi khác để lấy đủ chúng.
