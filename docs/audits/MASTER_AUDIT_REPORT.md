# Báo cáo audit tổng hợp — 488, 12/10/2026

**Kết luận: giữ engine và công cụ đóng gói; sửa cách kiểm soát pose, tham chiếu và tổ chức sản xuất trước khi nhân rộng.** Workflow tạo chuyển động chưa được chứng minh chỉ vì đã có compiler, atlas hay tám PNG. Full RTS vẫn chưa hoàn tất.

Bốn vai trò độc lập đều chạy đúng `gpt-6.1-sol`, reasoning `low`, tối đa ba worker cùng root. A/B/D chạy trước, C chạy sau; phạm vi file riêng. Root đọc báo cáo, đối chiếu các điểm quyết định với source và sửa sai khác; không chỉ ghép báo cáo. Audit chỉ đọc source/tài sản/receipt, không tạo ảnh hoặc replay game. Sau audit, A/B bổ sung helper/schema theo quyền sở hữu riêng.

| Vai trò | Báo cáo | Phạm vi / giới hạn |
|---|---|---|
|A Kiến trúc|[PROJECT_ARCHITECTURE_AUDIT](PROJECT_ARCHITECTURE_AUDIT.md)|Renderer, simulation, AI, logistics, online, cache, test/build/performance; source tồn tại không đồng nghĩa runtime PASS|
|B Animation|[ANIMATION_PIPELINE_AUDIT](ANIMATION_PIPELINE_AUDIT.md)|Identity/custody, các contact thất bại, projection, timing, compiler; không tự gán continuous review|
|C Sản xuất/reuse|[ASSET_PRODUCTION_AUDIT](ASSET_PRODUCTION_AUDIT.md)|Counts, frame/memory budgets, view/finite-order mismatch, job binding, phương pháp và chi phí chưa đo|
|D Tài liệu|[DOCUMENTATION_INTEGRITY_AUDIT](DOCUMENTATION_INTEGRITY_AUDIT.md)|Mâu thuẫn3D/2D, README cũ, trạng thái lặp, read contract và giới hạn chứng cứ|

## A. Hiện trạng có bằng chứng

VERIFIED source: JS ES modules/Vite, Canvas2D, shared simulation20Hz, online hai chỗ với snapshot mỗi4tick, command authority ở server. Gameplay có economy/army/logistics/naval/AI/King-General/Residence và hai map. Audit này không xác nhận mới một full match, WAN hay hiệu năng đông quân. Bằng chứng cụ thể và giới hạn nằm trong bảng của A.

VERIFIED census:21identity =9unit thường+12nhân vật;135action bank,1080clip theo hướng,7104vị trí frame Standard. Manifest local51asset/41ảnh runtime riêng,19,301,888byte RGBA và4,608,899byte encoded. Có3loop đúng action/hướng,397static fallback,680ô thiếu. Những con số này mô tả availability, không mô tả độ đẹp hoặc approval.

DOCUMENTED_ONLY lịch sử: public451/immutable230;350tests của462; controls479/480/484; nav/transport459/466. Root chỉ nhìn process runtime230 PID3408 trong lượt này, không kiểm tra HTTPS/rooms hay restart. Không biến source hiện tại thành public hiện tại.

## B. Lỗi và nguyên nhân

1. **VERIFIED:** view template không nhận action nhưng finite guard lại yêu cầu action và số frame của action. Chưa thể dispatch view đúng qua chuỗi guard hiện tại. Sửa jobKind riêng; không bỏ guard.
2. **VERIFIED/INFERRED:** selected-neighbor tra một currentJob duy nhất. Các action/hướng cùng identity không thể đồng thời khớp binding đó. Chuyển sang job bất biến theo action/direction/variant, có order pin.
3. **VERIFIED:**19/21identity chưa có equipment ownership,0view registry được đánh dấu selected. Có file tĩnh không tự tạo quyền sản xuất animation.
4. **FAILED theo receipt:** infantry482/483/486 giữ identity nhưng chưa đạt đổi chân đúng.486 đã dùng hết một call được duyệt,0selected. Fix target-first mới chưa gọi, không được nói đã hiệu quả.
5. **INFERRED:** câu “chân đối diện” chưa ràng buộc đường hip/knee/ankle/sole, lane và che khuất. Một số guide169 nhập nhằng phía sau theo chiều sâu với lùi theo hướng đi. Không thể quy mọi lỗi cho model, hoặc hứa thêm prompt sẽ chữa được.
6. **VERIFIED:** stride0.15 ở tốc độ2.3 tạo15.33chu kỳ/giây; preview720ms không phải timing runtime. Phải đo theo projection và contact, không đổi tốc độ gameplay.
7. **VERIFIED:** tài liệu3D cũ tự gọi là hiện hành; README còn nói original chưa phục hồi và cache chưa có. Đã chuyển lịch sử về đúng phạm vi và tạo một nguồn state/queue.

## C. Những kết luận được root chỉnh lại

- Default gameplayzoom là1.68 từ `client/main.js` launch và `world-presentation.js`; constructor1 không phải kết quả cuối.42×1.68=70.56px là canvas, không phải chiều cao cơ thể.
- Bank không chọn vô điều kiện mọi source: `shared/art-bank.js` lọc scope nhưng scope vẫn gồm mọi unit/building và leader đã chọn. Cần working-set nhỏ hơn, không nói hệ thống chưa có lọc nào.
- Field policy đúng là `asset.loadPolicy`. Root đọc lại:51undefined,0on-demand,0explicit eager; default hiện tại eager.
- Low budget tính đúng4944, Standard7104, Premium10560. Không nhân đôi ability King/General vì simulation chọn cùng ability theo character; build chỉ King.
- Không phải mọi thử nghiệm chân Villager đều thất bại: South009 có receipt hai contact đối nhau; đó chưa là full-loop approval. Wood032/iron141 chỉ đúngD1 đã được xem.
- Latest master brief yêu cầu Villager qualification trước, rồi Infantry reuse. Kế hoạch cũ Infantry-first được thay về thứ tự, không xóa công việc đã có hoặc mở lại order thất bại.

## D. Kiến trúc sản xuất được chọn

Năm lớp: **identity bất biến → motion archetype → projection/occlusion → whole-frame illustration → runtime atlas/timing**. Reuse phase/contact/tool intent và máy đóng gói, không reuse chân tay cắt từ unit khác. Giữ compiler/order runner/loader/picking/action clocks. Chi tiết có tại [contract](../art/pipeline/ANIMATION_CONTRACT.md) và [workflow](../art/pipeline/SPRITE_PRODUCTION_WORKFLOW.md).

Key trước, neighbor in-between sau; đối chiếu silhouette và contact ở kích thước chơi. [Nghiên cứu nguồn chính thức](../art/pipeline/ANIMATION_RESEARCH.md) phân biệt điều Krita/Blizzard/AoE/TexturePacker xác nhận với thông số chưa biết. ControlNet/IP-Adapter là hướng nghiên cứu spatial/appearance conditioning, không là bằng chứng công cụ có sẵn hoặc animation đúng.

Nhánh2D cục bộ đã được người dùng chọn để nghiên cứu. Máy có RTX2050 qua PCI nhưng chưa xác minh driver/VRAM/inference; chưa có Krita/GIMP/Inkscape/torch/diffusers. Chưa cài hoặc gọi model cục bộ. Chỉ mở finite capability trial khi có công cụ và cách điều khiển khác rõ ràng. Giữ pure2D và whole-frame; không API key, không3D.

## E. Hệ thống tài liệu và framework đã tạo

- [AGENTS](../../AGENTS.md) là điểm đọc bắt buộc; CLAUDE chỉ dẫn về đó. Read contract chọn tài liệu theo subsystem.
- [PROJECT_STATE](../PROJECT_STATE.md), [PROJECT_ROADMAP](../PROJECT_ROADMAP.md), [NEXT_STEPS](../NEXT_STEPS.md) là ba nguồn duy nhất cho state/milestone/queue. Root entrypoint cũ thành liên kết; chín bản cũ được giữ nguyên, bao gồm486 chưa commit.
- Art direction, contract, archetypes, prompt recipes, workflow, QA và research được tách theo mục đích; không nhân bản queue.
- Preflight thực thi chỉ đọc: hash tài liệu/source, Git và claim/lock. Không giả vờ có global hook hoặc chứng minh agent đã hiểu.
- JSON Schema strict cho evidence envelope; validator nối candidate tới canonical/job/descriptor/frame/atlas. Không thay runtime schema1 hoặc compiler. Đường production của envelope mới chưa có trusted adapter nên từ chối; không phong approval qua một chuỗi PASS tự điền.
- Provenance JSONL có3record seed thật, phạm vi ghi rõ; model/thời gian thiếu đểnull. Motion-archetypes JSON là PROPOSED, chưa nói đã tạo ra chuyển động.

## F. Kế hoạch và rủi ro

P1 sửa view job/currentJob/equipment → P2 hai contact và projection Villager → P3 loop/travel Villager → P4 reuse Infantry đo effort → P5 horse/wagon pilot → P6 đầy đủ action×8hướng → P7 map/buildings/working-set → P8 public nghiệm thu. [Roadmap](../PROJECT_ROADMAP.md) có dependency, owner và exit evidence từng gói. Các việc map/building/performance độc lập có thể tiến hành khi motion còn held.

Không tạo lại frame đã có; tối đa2correction/action/hướng, lỗi cùng loại lặp thì đổi cơ chế điều khiển, không đổi tên order. Một sheet,10–15giây loop, một cảnh liên quan; không audit nếp áo/pixel nhiều vòng, không fullmatch từngảnh, không hỏi người dùng từngframe.

Standard fullroster tối thiểu472.18MiB padded trước overhead, vượt128MiB decoded. Có loader deferred/LRU nhưng còn phải áp dụng và đo working-set thực. Năng suất/chi phí gọi ảnh chưa có số đo đáng tin;7.104vị trí không phải7.104call được phép.

## G. Validation và giới hạn bàn giao

Kết quả chính xác và preservation pins ghi ở [VALIDATION](audit-488/VALIDATION.json) sau integration. Chỉ chạy tests của helper/schema, parse/link/provenance checks và candidate custody của479. Không build game, replay browser/fullmatch, tạoảnh, cài tool hoặc triển khai. Runtime/public/source art và thay đổi486 được so hash với baseline.

Đợt này hoàn tất **audit + tài liệu bắt buộc + thiết kế workflow/framework và helper nền**. Nó không hoàn tất motion pilot, lỗiP1, nhánh2Dlocal, fullroster hay fullgame. Bước tiếp theo phải là công việc trong queue, không lặp audit tổng quát hoặc tạo thêm lớp giấy tờ.
