# Kế hoạch đồ họa — checkpoint168, 10/10/2026

Kế hoạch toàn game: [PROJECT_PLAN.md](../../PROJECT_PLAN.md). Phạm vi và bằng chứng chi tiết: [art-animation-audit.md](../../audit/2026-10-09/art-animation-audit.md). Bản kế hoạch trước audit được giữ [nguyên byte](../../audit/2026-10-09/history/docs/art/pipeline/GRAPHICS_PRODUCTION_PLAN.md).

## Mục tiêu hình ảnh

Minh họa lịch sử chân thực/bán chân thực, có khối và chiều sâu, chuyển động tự nhiên ở kích thước chơi RTS. Giữ mũ, trang phục, màu áo, dải thắt lưng (sash) và vật liệu theo mẫu nhân vật chuẩn (canonical). Không dùng nhân vật hình khối, 3D, cutout hay texture tay/chân riêng làm thành phẩm.

Thứ tự đánh giá: chuyển động đúng và liền mạch → silhouette/readability → identity nhất quán → chi tiết bề mặt. Xem một vòng chuyển động ngắn ở kích thước chơi thật; chỉ sửa lỗi thấy rõ. Việc audit kỹ kế hoạch không thay đổi ưu tiên kiểm tra hình ảnh ngắn gọn này.

## Hiện tại có gì

| Hạng mục | Đã có | Còn thiếu |
|---|---|---|
| Villager D1 | Idle, walk 014, wood 026/owner 032, iron 136/owner 141; food 101 local | Build/repair, attack/hit/death và độ phủ hướng; food còn chờ phản hồi riêng |
| Villager D0 | 033/152 contact candidates;155 F2/F6 đã bị người dùng bác bỏ,158 dừng0call | Rough162 đã có; capability166 HELD phase. Còn reconcile support/occlusion, final loop và actual travel/stop |
| Quân đội | Một số identity idle D0 | Phần lớn hành động và hướng nhìn cho infantry, spear, firearm, cavalry, artillery, wagon và hai tàu |
| Leaders | 12 portrait và nguồn identity gốc | Hoạt ảnh toàn thân, hành động theo vai trò và 8 hướng; chỉ một general có idle candidate |
| Buildings | Public6/10, local7/10 completed-idle | Fort/Wall/Gate; construction/damage/destruction |
| World | Ground/water/ford/shore candidates, forest, hill/mountain, food/iron nodes | Composition hai map, bờ/edge/repetition và scene đông quân |
| Framework | Export017, preview098, timing, locomotion phase, gather episodes, alpha picking, manifest loader | Coverage registry, composition compiler, match banks, default release |

Public149 `?art=camp` có 26 asset entries / 47 frame rectangles. Đó không phải 26 animation hay bộ roster hoàn chỉnh. URL trần chưa dùng slice này mặc định.

## Quy trình chuẩn cho một action

1. **Chốt identity và runtime mapping.** Ghi `identity/action/engineDirection`, nguồn canonical, camera/light, equipment, cycle/terminal state và simulation event liên quan. Không tạo run/carry/deploy nếu gameplay không cần.
2. **Chốt cả chu kỳ.** Dùng clothed 2D guides có near/far ownership, contact/passing phases, fixed pivot và timing. Walk 8 frame: F0/F2/F4/F6 trước, rồi inbetweens. Không dựa vào bốn prompt rời rạc.
3. **Sinh whole illustrated keys.** Builtin imagegen, exact Sol 6.1 Low worker. Canonical duy nhất giữ authority về hình thể/camera/identity; whole-body guide điều khiển pose, strip cả chu kỳ cho temporal context. Không để generic guide thay tỷ lệ canonical. Giữ raw và tool receipt. Key sai rõ ràng thì dừng slot, không đổi nhãn để che lỗi.
4. **Hoàn thiện inbetweens.** Sau khi keys được chọn, mỗi frame bám hai key lân cận; số call hữu hạn. Không ghép nguồn pixel, xoay limb texture hoặc fit từng frame.
5. **Compile và xem loop.** Một transform cho toàn family, alpha/cell/pivot/duration validation, atlas/manifest/contact sheet/loop tự sinh. Xem 10–15 giây tại kích thước chơi; sửa những lỗi nhìn thấy.
6. **Trial thật và đưa vào catalog.** Đi/đứng/đổi hướng hoặc work/stop/pause trong game, đúng hướng do mô phỏng xác định. Ghi technical/visual/owner/public riêng. Chỉ mở đợt sản xuất tiếp sau khi pilot tương ứng đạt yêu cầu.

Gộp công việc theo từng hành động, không tạo một dự án quản trị cho từng frame. Mỗi package có một ledger, một preview và một receipt gọn. Bản lỗi và original vẫn được giữ; build/rollback đầy đủ ở ranh giới release.

## Tái sử dụng và sản xuất hàng loạt

Tái sử dụng pose specification, guides, timing, camera, export, atlas schema, preview, asset banking và runtime API. Thành phẩm của mỗi nhân vật vẫn phải là một minh họa toàn thân riêng. Humanoid generic, spear, firearm, commander, cavalry, artillery crew, wagon và ship là các motion family khác nhau.

- Bước 1: hoàn thiện D0 walk để chứng minh quy trình dùng guide có trang phục qua cả chu kỳ.
- Bước 2: thống nhất visible scale của idle/walk/work trong một scene thật, rồi hoàn thành villager tám hướng và action cần thiết.
- Bước 3: một infantry pilot trọn trạng thái; sau đó spear/firearm. Song song làm world/building, không mở cả roster ảnh.
- Bước 4: từng complex family (horse/rider, wagon/animal, crew/gun, ships) có pilot riêng trước batch.
- Bước 5: một premium leader pilot; chốt 12 identity dùng shared role family hay role-specific artwork trước khi ước tính/call hàng loạt.
- Bước 6: accepted release manifest + match banks + final map composition + performance và public validation.

Worker có thể chạy song song các package độc lập, tối đa 3 worker + root. Frame phụ thuộc phải đợi key đã được tạo và chọn thực tế. Không lật ảnh tự động: villager sash, tay cầm vũ khí, leaders và ánh sáng bất đối xứng cần hướng thật. Nếu một generic family đối xứng đủ để mirror, phải ghi mapping được duyệt và thêm hỗ trợ renderer trước; hiện vẫn dự trù đủ 8 hướng.

## Kích thước và bộ nhớ

Mục tiêu visible humanoid 64–96 logical px tại default zoom, không phải canvas cao 89 px. Scene hiện tại có idle cũ render 38/42/51 và action mới 89; đây là chênh lệch cần sửa bằng thang kích thước nhất quán cho từng nhóm nhân vật. Đo opaque height đủ để giải quyết khác biệt nhìn thấy, không audit từng pixel.

Raw hiện tại 1254² được giữ nguyên. Bản working/export đề xuất 256², khoảng 224 px body; runtime 128², khoảng 112 px body trước scale xuống màn hình. Đây là baseline dự kiến cho output chuẩn hóa, không tuyên bố raw đã sinh 256 px. Dùng transform chung và pivot chuyển đổi đúng; horse/spear/ship có canvas riêng nếu cần. Không regenerate asset tốt chỉ để đổi độ phân giải.

128² RGBA = 64 KiB/frame; 64 frame = 4 MiB trước padding/copies. Inventory tham khảo 5.600–6.024 frame có thể chiếm 350–376,5 MiB nếu nạp toàn bộ 128 cells, chưa gồm world/portrait/caches. Vì vậy cần selected-map/roster banks, giải phóng bank khi rời trận, dedup theo content hash. Guard 128 MiB hiện có chưa tính toàn bộ bộ nhớ trình duyệt.

Không hứa ngày hoàn tất trước khi đo số frame được chấp nhận trên mỗi call và thời gian làm việc thực để hoàn thành ít nhất hai chu kỳ. Số lượng trong audit là giả định để lập kế hoạch; không phải lệnh tự động sinh hàng nghìn ảnh. Không ép tất cả hành động dùng 8 frame: hit/death/attack/idle theo thời lượng và độ mượt cần thiết.

## Gate tiếp theo cụ thể

G01 hiện theo [movement research161](movement-research-161/README.md): một canonical master → complete on-model rough cycle162 (0call) → brief look → một whole-illustration capability trial (order mới,0retry) → key/inbetween thật → loop → actual D0 travel/Stop. Guide153/158 và key155 không được dùng làm parent production. Không giữ hai contact cũ bằng mọi giá khi lệch hình thể. Hình nháp là công cụ authoring, không final art. Wood032/iron141 acceptance đứng riêng; food pending không chặn lane độc lập. Các phương pháp exhausted/held không thử lại mù.

Đưa asset mới vào default release sau coverage và actual-scene acceptance; không bật toàn bộ candidate rồi gọi finished. Full project vẫn **INCOMPLETE**.

## Follow-up162–168

[162 rough](villager-walk-D0-rough-cycle-162/root-intake.json) đã hoàn thành reference trọn vòng; không final art. [166 illustration](villager-walk-D0-capability-166/root-intake.json) cải thiện khối người nhưng HELD support phase;1call/0retry/exhausted. [Hướng tiếp](movement-research-161/FOLLOWUP_162_166.md) là reconcile ownership/occlusion,0call, không mở F6/inbetween.165 Shipyard idle accepted narrow actual Coast scene, local27assets; public149 vẫn26. Code163/merged167 không cấp motion acceptance.
