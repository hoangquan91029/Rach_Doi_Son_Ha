# Rạch Đôi Sơn Hà — kế hoạch thực thi sau audit 154

Cập nhật ngày 2026-10-10, múi giờ Asia/Ho_Chi_Minh. **Trạng thái: INCOMPLETE.** Đây là kế hoạch hiện hành cho toàn dự án; `NEXT_STEPS.md` chỉ giữ hàng đợi gần nhất. Hồ sơ cũ được giữ nguyên byte tại `docs/audit/2026-10-09/history/`.

Latest execution237 ở mục23 và active movement plan thay các next-step lịch sử; source/receipt cũ giữ nguyên.

## 1. Mục tiêu và cách đọc kết quả

Người dùng nhận **một URL HTTPS**, mở trình duyệt desktop mà không cần cài đặt, rồi chơi trọn Single Player với AI hoặc Online đúng 1v1 trên cả hai map. Tất cả yêu cầu master, web, lịch sử, visual và các section 81–145 vẫn áp dụng, theo những điều chỉnh mới nhất của người dùng.

Không dùng phần trăm hoàn thành giả. Mỗi hạng mục được theo dõi theo bốn phần độc lập: triển khai, bằng chứng kỹ thuật, chấp nhận visual và public release. Test PASS của một contract không đóng cả hệ thống; một loop được duyệt không có nghĩa cả roster được duyệt. Chỉ giữ gate có tác dụng thực tế, không lặp audit giải phẫu hoặc pixel.

**Ràng buộc hiện hành:** frame toàn thân pure 2D và imagegen tích hợp. Mọi worker code/art dùng đúng `gpt-6.1-sol`/`low`; tối đa ba worker song song cộng root. Không dùng API key, Luna, 3D, texture chân tay rời hoặc cutout. Không theo dõi quota. Đồ mang về dùng walk thường. Giữ nguyên nguồn leadership, raw, bản held/rejected và receipt.

## 2. Kết luận audit

Nền game đã có simulation chung 20 Hz, AI, kinh tế/hậu cần, room do server giữ simulation authoritative và các trận public thành công. Có thể hoàn thiện trên nền này mà không cần viết lại engine. Khoảng cách lớn nhất tới bản hoàn chỉnh là **độ phủ đồ họa/animation và trải nghiệm mặc định nhất quán**, tiếp theo là lỗi gameplay cụ thể, hiệu năng có số đo và vận hành public.

Public 149 có 26 asset ở `?art=camp`, với ba action 8 frame của villager D1: walk, thu thập wood và thu thập iron. Bản này cũng có một số identity tĩnh, sáu building idle và world asset. Hướng/trạng thái thiếu vẫn dùng fallback. Food có loop local nhưng chưa được duyệt độ tự nhiên; D0 mới chọn F0/F4, còn F2/F6 là guide. Chưa hoàn tất bộ animation có thể sản xuất hàng loạt.

Tài liệu cũ trộn chỉ dẫn hiện hành với hơn 100 KB lịch sử trong mỗi file status/next, thậm chí còn chỉ về API key hoặc rig đã bỏ. Audit 154 tách lịch sử và tạo tài liệu đầu vào ngắn để tránh tiếp tục sai checkpoint.

Bằng chứng chi tiết:

- [Gameplay, AI, logistics và multiplayer](audit/2026-10-09/gameplay-audit.md).
- [Đồ họa, coverage và workload](audit/2026-10-09/art-animation-audit.md).
- [Release, vận hành và hiệu năng](audit/2026-10-09/release-performance-audit.md).
- [Nghiên cứu và quyết định kỹ thuật](audit/2026-10-09/RESEARCH.md).

## 3. Chuẩn hóa production và phần được tái sử dụng

Tái sử dụng đặc tả motion, pose guide theo archetype, quy ước direction/camera, timing, compiler, manifest, preview, loader, playback theo simulation authoritative, picking và test harness. Không tái sử dụng chân/tay cắt rời hoặc gắn loop villager lên cavalry hay leader.

Một gói việc gồm **một action hoàn chỉnh, một direction và một identity**, với source đầu vào, số call tối đa, output và tiêu chí kết thúc. Không mở mỗi frame thành một dự án riêng. Với walk 8 frame: chọn 4 key → tạo 4 inbetween → xuất một lần → xem loop → sửa lỗi thấy rõ → thử trong game. Key phải có phase đúng; không đổi nhãn để biến lỗi thành kết quả đúng.

Pipeline asset: `canonical → consistency spec → clothed 2D guides → illustrated keys → illustrated inbetweens → whole PNG → atlas/manifest → actual game`. Guide chỉ là hướng dẫn. Imagegen tích hợp không bảo đảm pose hoặc pixel lock; mỗi lần fail phải ghi lý do và thay đổi điều khiển cụ thể trước order mới. Không thử lại vô hạn.

Mỗi gói chỉ cần một `job.json` hoặc ledger liên kết original/reference/tool output/selection, một preview và một receipt ngắn. Giữ hồ sơ cũ, nhưng không nhân bản toàn dự án và nhiều inventory giống nhau cho từng source art. Snapshot/rollback đầy đủ nằm ở ranh giới release; pin file liên quan ở ranh giới action.

## 4. Thứ tự công việc và phụ thuộc

| ID | Ưu tiên / gói | Phạm vi cụ thể | Đầu ra / tiêu chí hoàn thành | Phụ thuộc |
|---|---|---|---|---|
| P00 | P0 — hợp nhất trạng thái | Ghi đúng public 149, local 151, key 152 và prep 153; bảo toàn phần chưa commit và receipt; giữ tài liệu hiện hành ngắn | Audit 154, kế hoạch và history nguyên byte; không mất source | Audit hiện tại |
| G01 | P0 — làm lại movement đúng mẫu | Theo [research161](art/pipeline/movement-research-161/README.md):155 bị bác bỏ,158 dừng0call; một master D0 → tám rough drawings đúng hình thể → brief loop → một repaint trial hữu hạn trước khi hoàn thiện key/inbetween | 8 frame toàn thân, atlas, loop tự nhiên ở size thật và di chuyển/Stop thực tế ở D0; không giả heading | P00; intake source mỗi phase |
| G02 | P0 — thống nhất scale và action registry | Đo chiều cao body opaque của idle/walk/work ở cùng camera/zoom mặc định; khai báo một scale mỗi family; bảng mapping thực tế | Không đổi size đột ngột giữa idle và walk/gather; chốt working 256/runtime 128 hoặc ngoại lệ có lý do; giữ runtime hiện tại đến khi xác minh | Có thể bắt đầu từ frame hiện có khi G01 đang làm; nghiệm thu scene hỗn hợp cuối sau G01 |
| C01 | P0 — sửa lỗi gameplay đã xác nhận | Finding có reproduction trong gameplay audit; mỗi patch sửa một invariant | Repro trước/sau và test tập trung; chạy regression shared sim nếu đổi mechanics | Bằng chứng audit; mục 5 |
| G03 | P1 — villager đủ 8 hướng | Khóa identity 8 view; dùng D1/D0 làm mẫu; mở từng cặp direction sau khi đủ pilot | Idle/walk đủ 8 hướng; build/repair/gather/attack/hit/death theo hành vi thật | G01, G02 và cầu nối runtime |
| T01 | P1 — catalog và release manifest | Sinh manifest từ registry thay vì cộng chain query route thủ công; kiểm coverage; phân biệt candidate được chấp nhận | Một manifest release có coverage, hash và bank; giữ URL thử cũ tương thích | G02; làm song song G03 |
| G04 | P1 — quân bộ | Pilot infantry attack/hit/death và movement 8 hướng; tiếp spear/firearm với tool/action riêng | Equipment/readability đúng; impact theo tick server; mapping aim/fire/reload | Workflow G03 được qualified; T01 |
| G05 | P1 — topology phức tạp | Cavalry, wagon, artillery, warship và transport dùng archetype riêng | Mỗi family có pilot trước khi hoàn tất scope action/direction; load/unload/embark khớp mechanics | Một pilot humanoid đầy đủ; làm tuần tự từng family |
| G06 | P1 — leadership | Đối chiếu 12 ID trong data với nguồn/dossier leadership; action theo role King/General | 12 identity × 8 view; action set theo role; costume/equipment/ability visual riêng | Template G04, T01; kiểm roster trước call |
| W01 | P1 — building và world | Shipyard/fort/wall/gate; construction/hit/destroyed cho 10 building; composition bờ sông/biển/forest/hill/mountain | Hai map thống nhất scale/light; route/ford/supply dễ đọc; không lặp pattern nổi bật | Có thể song song G01; không sửa shore đang held bằng thử mù |
| R01 | P1 — loading và art mặc định | Asset bank theo map/roster; manifest release được chấp nhận làm mặc định; Retry/fallback rõ | URL không có query mở đúng art release; cache/version và lỗi asset được xử lý an toàn | T01 và đủ art được chấp nhận; không publish phần pending |
| Q01 | P1 — đo hiệu năng | 20/50/100/200 unit, 500 nếu đạt được thực tế; 1/5/tối đa 8 room theo cap hiện tại; Chrome/Firefox. Chỉ thử 10 room trên staging với cap được khai báo riêng | Trace, memory, network và budget tick; xác định bottleneck rồi sửa theo số đo | Đo baseline sớm; lặp khi final art đổi đáng kể |
| R02 | P1 — vận hành release | Binding build/source bất biến, health, drain room, rollback, cache và lựa chọn host luôn hoạt động | Build từ checkout sạch cho đúng gói public; diễn tập rollback trên staging | R01; không mua host khi chưa có quyết định |
| A01 | P2 — cân bằng, UX và lịch sử | Bắt buộc: nguồn lịch sử, hướng dẫn controls và cue cần thiết; tách phần polish tùy chọn | Người mới hiểu General defeat, Residence và logistics; claim về leader có nguồn đọc được. Nghiệm thu phần bắt buộc trước V01; polish tùy chọn không chặn release | C01 và một visual slice cuối có thể chơi |
| V01 | P0 trước phát hành — kiểm định cuối | Cùng bản release trên hai map/hai mode; thiết bị/mạng ngoài; reconnect/victory/rematch | Đóng checklist §81 trên cùng release; 0 lỗi nặng; ghi rõ giới hạn còn lại | G03–G06, W01, R01–R02, Q01, C01 và phần bắt buộc của A01 |

Ưu tiên không có nghĩa phải dừng art cho đến khi mọi P0 xong. Ba lane chạy song song: **art motion**, **code/correctness và catalog**, **world/release/performance**. Root tổng hợp và kiểm kết quả thực. Không để hai worker cùng sửa một file hoặc dùng chung order ảnh.

## 5. Gameplay và mạng: phạm vi xử lý

Giữ kiến trúc authoritative snapshot; không chuyển sang lockstep chỉ để có “determinism”. Tái sử dụng code/test hiện có cho MainResidence uniqueness, General death, food hữu hạn, AI, room hai chỗ, reconnect và rematch. Finding mới phải có trigger tái hiện và hành vi mong đợi rõ trước patch; rủi ro chưa tái hiện được ghi INVESTIGATE.

Thứ tự C01:

1. **GP1:** sửa starvation của passenger đang embarked.
2. **GP2:** tính mitigation/splash cho từng victim.
3. **GP3:** thêm cảnh báo army food thấp và sửa progress huấn luyện để dùng total duration thực.
4. **GP4:** chốt policy recruitment food toàn cục, footprint building và việc dùng cùng character cho King/General trước khi thay đổi. Đây là quyết định thiết kế, chưa phải exploit đã xác nhận. Lập bảng 12 dòng cho mechanical effect của từng ability, với contract và test tập trung tương ứng.
5. **GP5:** tái sử dụng 6 regression AI và 2 regression naval hiện có; chỉ sửa scenario thất bại cụ thể, không thay đổi rộng khi chưa có lỗi tái hiện.

GP1/GP2 đã có reproduction trong bộ nhớ, không phải suy đoán. Mỗi patch gameplay chạy repro tập trung và regression AI/naval/path/logistics liên quan. Không chạy lại hai full match public chỉ vì thêm ảnh building idle.

Server tick 20 Hz phải giữ headroom; browser nhận snapshot và nội suy presentation. Hash phía client cần scope rõ: view của hai người có fog khác nhau không thể so như hash toàn world. Reconnect phải nhận epoch/state hiện tại và bỏ command cũ. Server restart là failure mode riêng, không được nhầm với reload tab. Chỉ yêu cầu lưu match bền vững nếu chọn thêm scope; mục tiêu tối thiểu hiện tại là maintenance/drain và thông báo gián đoạn trung thực.

## 6. Ngân sách đồ họa và hiệu năng đề xuất

Các con số sau là **mục tiêu nghiệm thu đề xuất, chưa phải PASS**:

- Desktop mặc định 1080p; ghi rõ DPR 1 và DPR 2. Chiều cao nhìn thấy của nhân vật bộ binh mục tiêu là 64–96 logical px ở zoom mặc định. Đo bbox opaque, không dùng cell size thay cho body height. Kiểm mật độ/readability sau khi đổi scale; không tự tăng camera zoom để giả đạt.
- Working/export source 256², với nhân vật khoảng 224 px khi phù hợp; runtime 128², body khoảng 112 px. Giữ nguyên raw 1254² hiện có. Chuẩn hóa cả family bằng một transform có metadata, không fit từng frame. Horse/spear/artillery/ship có canvas rộng hoặc lớn riêng khi silhouette cần.
- Mỗi atlas page mục tiêu không quá 2048², tương đương 16 MiB RGBA/page. Giữ guard 128 MiB hiện có và bổ sung budget asset bank theo match trước khi mở roster lớn. Guard loader không phải giới hạn tổng bộ nhớ browser vì còn canvas, cache và alpha mask.
- Trên máy benchmark đã ghi CPU/GPU/browser, mục tiêu là 60 FPS. Với 200 unit, p95 frame interval không quá 33,3 ms và không freeze quá 250 ms khi pan, chọn hoặc ra lệnh. Đo cả workload thường và stress. 500 unit là mục tiêu mở rộng theo brief, không phải lý do đổi population balance.
- Server 20 Hz: p95 tick work không quá 25 ms, p99 dưới 50 ms cho 1/5 room và tối đa 8 room theo cap hiện tại; không tăng backlog liên tục. Thử 10 room là workload staging riêng theo brief, chỉ làm sau khi khai báo cap thử nghiệm, không ngầm đổi cap production. Báo snapshot byte/giây và send queue, không chỉ thời gian sim step.
- Startup mục tiêu: menu trong 5 giây, match ready trong 10 giây ở 20 Mbps/RTT 100 ms trên máy định danh. Đo cold cache và warm cache riêng. Nếu khảo sát máy mục tiêu khác, chọn lại threshold và ghi lý do trước khi đánh PASS.

## 7. Các mốc giao sản phẩm

**M0 — kế hoạch có thể tiếp tục ngay:** có audit 154, trạng thái đã sửa, ID/phụ thuộc task và hồ sơ trước sửa còn nguyên. Không tạo art mới trong lượt audit.

**M1 — visual slice villager nhất quán:** walk D0/D1 đầy đủ; scale idle/action khớp; giữ sự chấp nhận wood/iron. Xem food ngắn khi có phản hồi, không hỏi lại liên tục. Build/repair/hit/death và một pilot attack được map đúng. Một scene thật thể hiện đi → làm → về → bị đánh → chết để đánh giá framework.

**M2 — đủ 8 hướng và một quân bộ hoàn chỉnh:** tái sử dụng template đã qualified; export/manifest bằng một command; tách candidate và release. Đo số frame được chấp nhận trên mỗi call và thời gian làm việc thực cho mỗi action hoàn chỉnh để dự báo phần còn lại.

**M3 — đủ roster, building và map:** xử lý family phức tạp và leader theo số lượng thực. Kiểm battle ở kích thước chơi một lần cho mỗi family/map thay vì audit từng pixel. Major unit không thiếu 5 state lõi; action riêng theo role không bị ép giống nhau.

**M4 — release candidate:** URL mặc định hiển thị đúng art, có asset bank và load budget; bug xác nhận đã sửa; hiệu năng/load/network có số đo. Trước mốc này, public vẫn là development.

**M5 — nghiệm thu toàn bộ:** trận Single Player và online hoàn tất trên đúng release candidate, ở cả hai map; có bằng chứng thiết bị/mạng ngoài, reconnect/rematch và chấp nhận visual cuối. Chỉ ghi COMPLETE và dừng automation khi mọi tiêu chí quan trọng đã đóng.

Inventory minh họa trong art audit ước tính khoảng 5.600–6.024 frame unit nếu mọi action được budget 8 hướng và 12 leader dùng chung family giữa hai role. Art riêng cho từng role có thể thêm 3.552 frame. Đây không phải số ảnh phải gọi ngay hoặc số frame cuối, và chưa gồm mọi FX/world variant. Idle 1 frame chỉ là coverage tối thiểu; dùng idle động 4–8 frame khi thiết kế cần. Chỉ chốt scope từng action sau khi map runtime.

**Không hứa ngày xong khi chưa có throughput đáng tin.** Ước lượng bằng `remaining selected frames / observed accepted frames per workday`, cộng dự phòng tích hợp và sửa lỗi nhìn thấy. Không lấy số call đã khởi động làm số frame hoàn thành. Hàng nghìn frame là workload đáng kể; worker song song giảm thời gian phối hợp nhưng không bỏ được phụ thuộc giữa key.

## 8. Cách nghiệm thu nhẹ nhưng đủ

Art: kiểm source thật, alpha, cell, pivot và timing không thiếu → xem contact sheet một lần → xem loop 10–15 giây ở size chơi → thử travel hoặc action ngắn trong game. Sửa lỗi rõ: đổi identity, nhảy root/scale, sai phase chân chịu lực, trượt chân lớn, tool bật hoặc biến mất, seam loop. Chi tiết cloth/pixel nhỏ không chặn. Chỉ xem native khi cần chẩn đoán lỗi đã thấy.

Code: test invariant tập trung; actual UI cho luồng bị ảnh hưởng; build vào output staging tách khỏi `dist/` đang phục vụ. Release cần root intake, ID source/build chính xác, rollback và smoke test Chrome/Firefox. Full match dùng khi mechanics đổi hoặc ở release candidate cuối, không chạy cho từng asset.

Chấp nhận wood 032 và iron 141 tiếp tục có hiệu lực đúng loop người dùng đã xem. Food pending không chặn việc độc lập. Không suy ra chấp nhận của người dùng từ still hoặc test. Chỉ mở rộng roster sau khi pilot family đúng, không mở batch từ một candidate F4.

## 9. Quyết định giữ và thay đổi chủ động

- Giữ Canvas 2D/Vite/Node/ws/shared sim. Chỉ tách module khi giúp catalog, hiệu năng hoặc correctness; không rewrite lớn.
- Giữ pure 2D. Không tải thêm skill chỉ để có thêm tool; skill hiện có đủ cho authoring. Chất lượng pose phải được chứng minh trong pilot.
- Thay checkpoint chồng chất bằng tài liệu hiện hành và archive; dùng một backlog chính thay cho nhiều chỉ dẫn “NEXT” mâu thuẫn.
- Thay chain opt-in làm sản phẩm chính bằng release catalog có trạng thái chấp nhận. URL preview cũ tiếp tục là công cụ development.
- Tách source custody khỏi deploy. Giữ original lớn ở offline; runtime chỉ chứa export cần dùng.
- Nguồn lịch sử phải có URL, tác giả và nội dung được áp dụng, không chỉ citation chat khó tra cứu. Không đổi 12 ID leader theo ví dụ trong directive trước khi đối chiếu dossier và nguồn gốc.

## 10. Trạng thái kế hoạch

Audit và lập kế hoạch không tự cấp visual PASS, sửa gameplay, triển khai release hoặc tạo thêm frame. Ba audit con có mức độ và reproduction chi tiết của finding. `NEXT_STEPS.md` quyết định gói mở tiếp; khi kết thúc gói, cập nhật receipt và trạng thái ngắn. Không tiếp tục hồ sơ lịch sử như một lệnh mới.

## 11. Quy tắc hợp nhất audit

Báo cáo con là snapshot tại `77c0ae1` cộng phần 151 chưa commit, trước khi tài liệu được rút gọn. Nhận xét “NEXT_STEPS còn 145/146” mô tả thời điểm audit, không phải chỉ dẫn hiện hành.

Ngân sách ở mục 6 là baseline của kế hoạch. Con số khác trong báo cáo release là phương án tham khảo chưa áp dụng; không yêu cầu đạt cả hai bộ threshold. Host luôn hoạt động là lựa chọn để tăng độ tin cậy, không có nghĩa §81 bắt buộc mua cloud hosting. Một thiết bị/mạng ngoài là gate bằng chứng thận trọng cho final release; kết quả hai browser trên cùng máy hiện có vẫn được giữ nguyên.

## 12. Cập nhật thực thi 156–161

Human rejection của155 F2/F6 thay selection cũ;158 không được chạy. Nguyên nhân nhìn thấy là đổi hình thể toàn thân, guide generic và các authority tỷ lệ không thống nhất. [Research161](art/pipeline/movement-research-161/README.md) là đặc tả movement hiện hành: gói162 zero-call authoring một chu kỳ nháp đúng canonical trước một single-call capability test. Thứ tự key trước final inbetween còn giữ, nhưng rough breakdown được hoạch định trọn vòng trước finish. Không ép giữ033/152 nếu chúng không hợp canonical/rough mới.

156/159 đã sửa local GP1/GP2; exact staged suite140/140 PASS có repro baseline, AI/naval và full source binding.157 coverage/read-only đã có,160 cập nhật route tests giữ eligibility/fog/custody. Không có build/deploy hoặc trận browser mới từ các gói này. Public149 còn nguyên. GP3/GP4/T01, đồ họa đủ roster/map và các gate release vẫn mở. Không đọc phần mô tả snapshot154 phía trên như một lệnh mở lại155/158.

## 13. Cập nhật162–168

G01 đã có rough cycle162 (0call) và capability166 (1call/0retry).166 giữ body tốt hơn155 nhưng support/passing relationship chưa đúng rõ; không được chọn F02. [Follow-up](art/pipeline/movement-research-161/FOLLOWUP_162_166.md) yêu cầu reconcile whole-cycle ownership/occlusion trước một phương pháp điều khiển khác; không retry/fanout. Đây là vấn đề motion chính, không cloth/pixel gate.

GP3 triển khai local163: actual total training duration và cảnh báo quân thiếu ration dùng threshold hiện hành.22 focused contracts/ordinary Chromium resupply flow; không đổi economics. W01 có Shipyard idle164/165, optionalLOCAL27; actual Coast narrow idle/picking/transport flow. Merged167 có27 focused contracts và Chrome/Firefox ordinary scene; public promotion vẫn riêng. Local7/10 building idle không có nghĩa construction/hit/death hoàn chỉnh.

Incident167 overwrite dist đã được khôi phục đúng179file public149;168 kiểm normalTLS boot trên exact149 hash, service không restart. Build guard hiện hành yêu cầu literal isolatedworkdir, absoluteoutdir, viteconfig đúng và root intake. Các receipt giữ nguyên failure và accident output local. Không lấy smoke restoration làm full-match proof hoặc lấy staged build làm public release.

## 14. Cập nhật169–173

G01:169 sửa own-depthlane ankle trajectory bằng completeoriginal rough drawings.172 onecall/0retry giữ realisticbody và forwardfoot nhưng phaseHELD;173 yêu cầu wholeaction authority được nhìn thật và newtonal wholebody authoring trước order khác. Source/licensing metadata không đủ để dùng photo chưa xem làm poseguide. Không qualifiedD0batch/runtime/fanout.

T01:170 có sharedruntime route registry,9legacyrecipes/28deduplicated definitions và deterministiccompiler ra standalone manifests/bankdependencies.33focused/18Nodefollowup và stagedChrome/Firefox UI scope PASS; runtime vẫn dùng full legacyroute manifests, dynamicbank lifecycle và default acceptedrelease còn mở. Không dùng compiledcandidate thay acceptance hoặc fullcoverage.

Q01:171 baseline bounded đo actualstep/normalAI và exactserver compactview+JSON,1/5/8world trên2map sau90simseconds normalgrowth.39units/world; step/AI tail lớn hơn serialization,5/8world workload có tickcost đáng profile. Không exclusiveCPU/liveonline/sendqueues/browser/densearmy test; đây là bottleneck direction, không headroom verdict hoặc balancechange. Profile trước optimization và đo actualbrowser/roomworkloads tiếp.

## 15. Cập nhật174–181 — lịch sử thực thi

G01:174/178 externalreference retrievals fail, không visuallyqualifiedphoto.179 originalwholetonal rough vẫn chưaqualifiedpassing;180 sửa hai completeposes, bỏ quy tắc ép ankleahead-idle và làm rõ lowerlegfold/weight-bearing support.181 ONEbuiltin/0retry giữ realisticcanonical body và chân gập rõ nhưng footlift cao/back: candidate, chưafinalF6/loop/runtime. Next là finitewholeposecorrection của visibledefect rồi completekeys/inbetweens/briefloop/actualD0travel; không auditmicroanatomy/retryunchangedprompt hoặc fanout. [181rootintake](art/pipeline/villager-walk-D0-capability-181/root-intake.json) và activegraphicsplan govern.

T01/R01:175dynamicmenu/match banks cài local, uses shared170selection/alllegalroster+buildings/bothleaderfamilies/shadowclosure. Encodedhashbytes giữ offline; decoded/private/terrain refs giải phóng khi menu. Prior1fc4… build có27contracts +normalChrome/Firefoxofflinebothmaps/online2peerreload/newroom; final007f… completion có28contracts +actualChromium decoderfaultfailuregate/Retry/lateststate/menu. Không gọi broadproof của chunk cũ là proof chunk mới. Completedcombatrematch/defaultacceptedrelease/fullcoverage còn mở;175builds loại177.

Q01:1762024samples phân biệt actualAI1.68% với navigationnormalstep tail.177 query-local exactcell-pass memo preservesterrain/owner/gate/corners/fractionalground/crowd/ties/range/retry/speed;82contractsPASS inclpairedstatehash/AI/naval. One matchedunprofiledDelta5 diagnostic p95step52.934→11.924ms nhưngmax≈64ms còn, nonexclusive/order caveats. Localoptimization accepted; không productioncapacity hoặc mergedbrowseracceptance. Nextmerged175/177 exactstagedsource/build/relevantUI intake trước promotion, không repeatbaseline/profile.

Public149179files/service157023 giữ nguyên. Broadcompletedmatch089/090 evidence scope vẫn giữ; currentlocalchanges không public. Allworkers/calls terminal tại checkpoint, history173entrypoints riêng; futureworker inspect live receipts, do not duplicate calls. Fullmaster/web/historical/visual/81–145 vẫn INCOMPLETE.

## 16. Cập nhật182–189 — lịch sử thực thi

G01 hiện theo [actualcontact research](art/pipeline/movement-research-161/CONTACT_OWNERSHIP_188.md).182/185 giữ realisticbody nhưng không motionapproved.188 bodycamera tốt hơn152, vẫn lặp033 legpaths.152 labelopposite không established; không tiếp tục coi đó là poseauthority.188 originalF4HOLD giữ nguyên, raw được explicitreassignF0candidate.189 đúnghai originalwholeclothed guides/0calls cố định A/Bhip/depth và đổi vai; chỉ authoring.190 finiteONEwholeillustration đang chạy, actualintake trước key/inbetween. Hoàn thiện một loop thật sớm, xem briefgame-size, sửa lỗi nhìn thấy; không microscopic scoring, fanout hoặc claim smoothness từstill.

183/187 đã bind merged175/177 exactstage/chunk80a85…5fba8/simc95e… và actual relevant offlinebothmaps/combatresult/rematch banklifecycle. Không lặp fullmatches/tests đã xong.186 local first-strike runtime closure dùng serializedprivateunitmarkers/oneimpact splashboolean,29focused/82regressions PASS; current sim4aa2… khác frozen183, cần binding riêng khi promotion.186 không đổi mô tả/speed/duration/cooldown;184 mismatchhistorical giữ nguyên.

Public149 vẫn optionalcamp26, chưa deploycandidate. Fullart/fullcoverage/defaultrelease/performancecapacity/externaldesktop/WAN/finalrelease gate mở. Các receipt/read-only audits hoặc guide counts không thay final acceptance.

## 17. Hiện hành: movement pilot195 / checkpoint197

[Kế hoạch movement gắn asset thực tế](art/pipeline/MOVEMENT_PRODUCTION_PLAN_20261010.md) thay các next-order lịch sử. Root phát hiện nguồn152 labelledopposite sai; guide-only191 và whole correction192 cho actual opposing contact.195 đã có tám illustrated sources, atlas/APNG600ms và technical Chromium playback; original193F3 nonfamily canvas bị loại,197 là source thay thế provisional. F3/F4 body/arms còn warning. Actual APNG đã hiển thị, một human continuous-look question pending; chưa motion/runtime/worldfootlock/fanout approval. Sửa lỗi nhìn thấy ở full-loop/gameplay size, không quay lại exhaustive static anatomy audit. Next candidates: specific loop fix nếu cần, rồi D0 runtime + same-family idle/travel/Pause/Stop.

186 first-strike mechanics local accepted29/82 tests;183/187 merged bank/navigation offline/combat/rematch proof hoàn tất nhưng bind c95, không include1864aa source. Candidate release needs exact newbuild/relevant ability scene/rollback; không repeat completed full matches absent concern. Public149 vẫn unchanged, full objective INCOMPLETE.

## 18. Thực thi198–203 — hiện hành

G01 không thay: actual195loop/human continuous feedback pending, F3/F4 bodywarnings remain, chưa runtime/fanout. Không tạo character mới trong gói này. W01 có [198](art/buildings/fort-idle-198/root-intake.json) wholeFortidle và [202](qa/fort-idle-202/root-intake.json) optionalLOCALfort28,32 targetedcontracts/ordinaryDelta build-idle-select-Pause-Resume-Stop-menu; fixed112/sourcepivot627,1010. Building construction/attack/hit/death vẫn procedural fallback. [201](qa/hill-edges-201/root-intake.json) sửa partial/odd hillground với visibletile clipping,7focused + narrowordinaryscene; synthetic nativeCanvas leakage probe tách rõ. Không đóng mapcomposition gate.

[203](qa/tempo-browser-203/root-intake.json) exact1864aa ordinaryChromium/Firefox NguyễnHuệ UIcast/first-second impacts cho adjustedratio1.3, second stillrecentmovement33ticks nhưng khôngrepeatboost. Frozen199bundle8b64…62f1 khác202mergedbundle796ff…d83f5; source/buildclaims tách riêng.199toast/200selectiongroup harnessfailures được giữ. Public149179files/service không thay, allownedhandlesclosed. Next concrete release needs exactcandidate/rollback/normalTLS intake; fullgame/defaultart/visual/performance/externaldevice gates remain open.

## 19. Thực thi204–209 — hiện hành

G01:205 ONE whole F3body correction,208 exacteightloop changingONLYF3,195bytepreserved. Face/upperbody closerfamily; F4quietarms/bodydifference remains. New APNG displayed, technical8frames/3loopsPASS but motion/owner/worldfootlock/runtime/fanout remainopen. Olderpendingquestion scoped195, no inference for208.

R01:204 source/service/rollback audit found202 pendingfoodrecipe/bytes.206 derivedpublicstage removesonlyrecipe+099manifest/atlas,4scopecontracts,newchunk74eb…c873.207 pairedimmutable server4aa/runtime206 and185dist atomicpromotion, originalunit/env/Funnel preserved; complete179old149+oldserver28e+currentfrozenws archive208entries verified, canonicalunchanged. [209 actualTLS](qa/public-intake-209/root-intake.json) Chrome/Firefox firststrike + ONE DeltaFortflow/menu cache0/defaultunknownfoodboot acceptednarrow. GuestordinaryresultMenu NOTperformed; expectedOpponentleftresult and originalcleanupHOLD retained, ownedroomexistinggrace cleanup. No fullmatch/rematch/performance/externaldesktop/WAN/defaultart/motion approval. Fullgoal INCOMPLETE, allownedhandlesclosed; production207 runs intentionally. Next realunfinishedgraphics/buildingstates/maps/denseperformance work uses newfiniteorders; don't repeat completed suites/matches or resume historical149/202promotionorders.

## 20. Hiện hành210–213 — movement nghiên cứu lại và adjacencylocal

[Movementplan](art/pipeline/MOVEMENT_PRODUCTION_PLAN_20261010.md) đã viết lại gắn canonical/actualsources/research212. Wholebodyvolume/camera/neighborcontinuity là lỗi chính, khôngmicrodetail.211 ONEwholeF4edit/0retry phục hồi torso/arms;213 exact208eight ONLYF4replacement, zeroimagecalls/8×75ms600ms/128atlas/89preview. ActualChromium8/3cycles/PausePlay/errors0, rootbriefsheet và actualAPNGdisplayed; motion/owner/worldfootlock/runtime/fanoutOPEN. Pendingquestion195 khôngapprove213. Nextbrieflooplook→samefamilyidle→actualD0travel/PauseResumeStop; no blindcalls/batchclaims.

210 fixeslocalorthogonalWall/Gate adjacency by removingonlytheirpairsetback0.4.33focused+3existingcontracts andONEactualvillagerUI line/friendlyGatecrossPASS; KingreplacementResidence role/otherguards unchanged. Localcanonicalsim b9f903…35f48 differspublicimmutable2074aa. Rendererhorizontalprocedural/topology remainsunfinished, no publicpromotion. Existing207/209 production/evidence/rollback stand; no repeatedfullmatches orprooftests withoutnewconcern. All210–213 handlesclosed atcheckpoint; checkactualstate before work. Fullgoal INCOMPLETE; history209 entrypoints bytepreserved.

## 21. Hiện hành214–224 — integration topology/picking/construction

W01:215 procedural fallback dùng visible-only sameowner completed four-neighbors, exactprojectedhalfcell joins/X/Y/corner/T/cross.222 picking theo đúng faces/rails/posts/header, không chặn khoảng trống cổng.36 focusedcontracts và223 ONEordinaryDeltaUI five completed structures/twoaxes/corner/exactselection/PauseResume/friendlyGatecross/Stop/menu decoded0/errors0 acceptednarrow. [Root223](qa/fortification-picking-browser-223/root-intake.json). FinishedillustratedWall/Gate art chưađạt:214 ONEbuiltin raw/candidate HOLD endpointalignment, không pixelrepair/install. Original215/220 holds bytepreserved.

217 visible publicconstructionboolean saufogfilter không lộ job; ownjob và enemyredaction giữ nguyên.9focusedcontracts và221 actualtwopeer visibleunderConstruction/completion/privacy accepted.221overallHOLD scoutreturn; nofogreturn/menu/authoredcompletionscreenshotclaim. Localcanonicalsim29233a…748b khácpublicimmutable4aa; không deploy.

G01/G02:216 zero-call wholecanonical uniform128/89/pivot6541140 prepared; Stop/bodyvolume transition chưaverified.219 HOLDboot rootabsolutepaths;225 NEWfinite isolatedcopy sửaONLYtwo relativepaths→ONEoffline actualD0 trial, kết quả riêng trước nextorder.213 candidate không tựqualified từ technicaltests. Fullgoal INCOMPLETE. Public207 optionalfort28/185/PID510490 và pairedrollback giữ nguyên; không replaycompletedmatches hoặcblindcalls. Currententrypoints213 bytepreserved trong checkpoint213-entrypoints.

Current runtime update225/226:225 actualloader29PASS, livingownD0travel observed but town detour/D1 and partial samples causedHOLD; PauseResumeStop/menu unperformed. This is not proof of skipped renderer frames or bad motion.226 NEWsamefrozen225build uses an actualclear outside-towncorridor and25ms observations, ONEofflineUI/160s/no retry. Inspect actual226receipt; no approval/installation/fanout or perframefit/scale/speedchanges.227 release preparation-only for accepted215/217/222/210 code; public207 still unchanged.

## 22. Hiện hành226–232 — actual movement và paired public230

G01/G02:226 guard.3 thất bại nhưng engineordinaryarrival.7; sourcecontractread→228 actualD0 đủ8/64samples/Pausefreeze500ms/Resume PASStechnical. StopidleD7 afterendpointturn nên matchingD0/menu OPEN, actualclipdisplayed, no naturalness/owner/worldfootlock/fanout approval.213frames/canonical/originals unchanged, zeroimagecalls. No blindcampaignchain; nextspecificStoptransition order stopswhileactualD0segment remains withoutfakefacing/speed/scale/phase changes. Mixedlegacyfamily scale remainsopen.

R01/R02:227 frozenpair/rollback207 preparation,4scopecontracts;229 exactnewchunk479b…b4cf TWOjoinedWallGate/select/PauseResumeStop/menu0 plusfourcleanChromeFirefoxbare/disabledfoodboots PASS.230 rooms0guardedatomicdist+immutable runtime230/sim29233/PID575363 pairedpromotion,186files inclold207chunk; readonly extractedmode repair receiptpreserved. FoodCHAR/D0excluded; complete207rollback private23044a92…759f, older149archive preserved.

[231publicTLS](qa/public-intake-231/root-intake.json) ONEChromium/Firefox room/Wallbuild, visibleenemyunderConstruction/privacy/ownjob/ordinary400HPcompletion/Stopactors/menus/expectedOpponentleft/errors0/healthrooms0 acceptednarrow. Exact28readycount/menuDecoded/optionalboots/pick not independentlyasserted; don'treplay forcleanreceipt. No finalart/WAN/fullmatch/defaultacceptedrelease claim. Public207nowhistory, neverrestart510490 ascurrent. Fullgoal INCOMPLETE; allownedhandlesclosed, production230intentionalruns. Bytearchive224entrypoints; activeAGENT/NEXT/status nowconcise232.

## 23. Thực thi233–237 — D0 transition và whole-wall trial

[233](qa/villager-D0-runtime-233/root-intake.json) đóng actual D0 Pause/Resume/Stop idle/order-null/dir0 và menu cache0 trên frozen225 build; ONE campaign/0retry/zero frame changes. Motion/owner/worldfootlock vẫn mở, clip đã hiển thị. Không replay chỉ để làm receipt đẹp hơn.

[234](art/buildings/wall-x-idle-234/root-intake.json) ONE built-in whole-wall illustration/0retry, uniform128/fixed pivot627,900/logical42.3225. Root thấy hình đọc tốt ở gameplay size và cho phép finite actual join trial; worker geometryHOLD và214 giữ nguyên. [235](qa/fortification-art-235/root-intake.json) thêm exact visible mask/state whole-art selection, same topology context cho renderer và alpha picking;42 focused contracts PASS. Không xoay/ghép/mirror PNG. API chỉ dùng living completed wall/gate; finalconstruction/death vẫn thiếu.[236 actual scene](qa/wall-x-runtime-236/root-intake.json) đã đạt narrow X joins/selection/PauseResumeStop/menu0; [237](qa/wall-x-install-237/receipt.json) cài local cleaned32 manifest + unchanged PNG, all28old descriptors preserved và render-bearing fields bằng exacttested236. Public chưađổi, fullWallGate chưađạt. New finite release preparation/intake/rollback là next.

Public230 không thay. Full realistic roster/directions/actions/12leaders/family scale/buildingstates/mapcomposition/densebrowser+rooms performance/defaultacceptedart/externaldesktopWAN/finalbothmapsSingle+1v1 vẫn INCOMPLETE.232 entrypoints được giữ nguyên byte trước cập nhật.
