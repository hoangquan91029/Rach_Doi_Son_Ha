# Pure2D character pipeline — chuẩn thực thi 154

Đọc [graphics plan](GRAPHICS_PRODUCTION_PLAN.md), [master directive](PURE_2D_MASTER_DIRECTIVE_20261008.txt) và [review priority](REVIEW_PRIORITY_20261008.md). Bản spec trước audit được giữ [nguyên byte](../../audit/2026-10-09/history/docs/art/pipeline/PURE_2D_CHARACTER_PIPELINE.md).

## Contract một action

Mỗi job ghi identity, role, action, engine direction 0–7, canonical/reference hashes, selected neighbors, guide roles, finite call slots, source canvas/pivot, runtime cell/render scale, frame durations, loop/terminal mode và simulation state/event. Giữ rõ các trạng thái `prepared / called / returned / selected / held / interrupted`; output thiếu không được bù bằng frame khác mà không có quyết định phase thật.

Engine direction dựa trên world XY; projection 54×27 biến world SE/D1 thành screen South, world E/D0 thành screen ESE. Luôn ghi cả engine integer lẫn tên screen view; không đổi entity.dir để phù hợp artwork.

Giữ nguyên ảnh minh họa toàn thân gốc; guide vector có trang phục chỉ là công cụ xây dựng pose. Keys được chọn trước inbetweens. Không source pixel splice, cutout, limb texture, 3D, warp repair hoặc mirror không được duyệt. Các thí nghiệm cũ giữ làm lịch sử.

## Reusable runtime

- Exporter017 và preview098: actual source sequence → alpha/layout checks → rectangles/contact sheet/APNG/atlas/manifest. Không fill missing sources.
- `client/art-assets.js`: exact manifest validation/hash/decode/state/direction; decoded-image budget 128 MiB.
- `client/sprite-timing.js`: duration-based sampling, loop/nonloop terminal hold, cosmetic markers.
- `client/locomotion-phase.js`: per entity distance-driven walk phase; never changes game speed.
- `client/action-presentation.js`: gather episode, attack timeline and pause. Simulation alone determines damage/resources/victory.
- `client/raster-slice.js`: exact rendered families/states/directions; chưa hỗ trợ toàn bộ unit types chỉ bằng cách thêm manifest. T01 sẽ thêm declarative registry.
- `client/visual-picking.js`: alpha picking cần dùng đúng cell/pivot/scale/offset cùng renderer.

Các thành phần nền tảng này có thể tái sử dụng cho mọi loại unit. Guides và illustration phải khác theo topology/equipment/identity; cavalry không phải humanoid chỉ thay ngoại hình.

## Family transform và export

Existing villager family raw 1254² / pivot [654,1140] → uniform 128² → render canvas 89; đây là cấu hình hiện tại, không bảo đảm phần thân nhìn thấy cao 89 px. Recent buildings raw 1254² / pivot [627,1010] → 256², declared render 96/112. G02 sẽ chốt mixed scene family scale trước batch; không sửa từng frame cho vừa bbox.

Bản làm việc 256² trong tương lai là bản dẫn xuất có metadata; giữ nguyên ảnh gốc. Cho phép canvas lớn hơn hoặc hình chữ nhật khi phạm vi chuyển động lớn, nhưng camera/pivot/family calibration phải rõ. Runtime atlas giữ uniform cells hiện tại. Nếu về sau trim, phải giữ sourceSize / trim offset / pivot và picking; packing không đổi visible pose. Không đổi codec/packing để che lỗi frame.

## Mapping tối thiểu cần hoàn thiện

| Family | Presentation cần gắn hành vi thật |
|---|---|
| Villager | Idle, walk (cả goods return), wood/food/iron gather, build/repair, attack/hit/death |
| Infantry/spear | Idle/walk/attack/hit/death, equipment riêng |
| Firearm | Attack có aim/fire/reload phases, authoritative impact; hit/death |
| King/General | Identity riêng, idle/walk/attack nếu có, command/ability, hit/death; General death authoritative |
| Cavalry | Horse+rider coherence, movement/attack/hit/death; charge chỉ khi mechanic cần |
| Artillery | Equipment/crew move, fire/recoil/reload, hit/destroyed; deploy nếu cần |
| Wagon | Idle/move, actual load/unload feedback, hit/destroyed |
| Ships | Idle/move/fire nếu warship, embark/unload nếu transport, damage/sink |

Số frame theo từng hành động (idle 4–8, walk 8–12, hit 3–6, death 8–16 là khoảng khởi đầu từ brief); không ép 8 mọi thứ. Giữ nguyên pilot 8 frame hiện có nếu chuyển động tự nhiên. Idle một frame có thể tạm lấp chỗ thiếu; không tự coi đó là hoạt ảnh idle hoàn chỉnh.

## Review và release

Một contact sheet, một vòng chuyển động ngắn ở kích thước thật và một kiểm tra di chuyển/hành động thực tế. Sửa phase sai, loop jump, scale/pivot jump, sliding rõ, identity/tool flicker; không chặn bằng cloth pixel nhỏ. Technical pass / visual intake / owner feedback / public release là bốn trường riêng.

Nguồn current: walk 014/D1, wood 026/owner 032, iron 136/owner 141; food 101 local pending; D0 selected 033 F0 + 152 F4 / 153 guide prep. Không mở call sinh ảnh trong audit 154. Tiếp theo theo [NEXT_STEPS.md](../../../NEXT_STEPS.md).
