# Kiến trúc hiện hành — audit 154

## Runtime

- `shared/data.js` định nghĩa 11 loại unit, 10 loại building, 12 identity leader, tag/synergy, terrain, hai map 64×48 và `TICK_RATE = 20`.
- `shared/sim.js` kiểm tra intent, ownership và cost của command; chạy economy/logistics/AI/combat/navigation theo fixed step; tạo view lọc theo fog và hash cho test deterministic. Single Player offline dùng cùng rule ở local; online do Node giữ simulation.
- `server/index.js` phục vụ `dist` production qua HTTP và WebSocket cùng origin bằng `ws`. Room có đúng hai người, với ready, reconnect grace, rematch, cleanup và giới hạn payload/rate/backpressure. Room nằm trong bộ nhớ, mất khi restart. Simulation danh định 20 Hz; snapshot gửi mỗi 4 tick.
- `client/main.js` xử lý menu, setup, boot portrait, lobby, input và HUD; dùng accumulator local hoặc state từ server. `renderer.js` vẽ world/minimap/camera/depth bằng Canvas 2D. `presentation.js` nội suy vị trí mà không lộ entity bị che. Simulation quyết định damage, resource và victory.

## Art và animation

Pipeline pure 2D: canonical → key được điều khiển → inbetween minh họa toàn thân → PNG → atlas. Xem [kế hoạch đồ họa](docs/art/pipeline/GRAPHICS_PRODUCTION_PLAN.md). Không dùng 3D, texture chân tay rời hoặc puppet runtime. Kiến trúc cũ và thử nghiệm rig được giữ trong [lịch sử](docs/audit/2026-10-09/history/ARCHITECTURE.md); chúng không phải dependency hiện hành.

`art-assets.js` kiểm tra manifest, hash, layout, state và direction; tải ảnh có giới hạn và tính decoded RGBA. Guard 128 MiB không phải giới hạn tổng bộ nhớ process. `raster-slice.js` hiện chọn manifest opt-in pilot/walk/work/food/terrain/iron/workshop/camp; public loại phần nhân vật food đang chờ. Module chỉ vẽ đúng state/direction có source và dùng fallback khi thiếu. T01/R01 sẽ thay composition thủ công bằng registry/manifest release; phần này mới là kế hoạch, chưa triển khai.

`sprite-timing.js` xử lý loop theo duration, giữ frame cuối và presentation event. `locomotion-phase.js` điều khiển phase walk bằng quãng đường thực của từng entity. `action-presentation.js` dùng clock của episode tiếp xúc khi gather, căn impact attack theo simulation authoritative và xử lý Pause. Marker trang trí không thực thi combat hoặc thay đổi resource. `visual-picking.js` chọn theo alpha nhìn thấy hoặc fallback của candidate; alpha array và cell canvas dùng thêm bộ nhớ ngoài budget loader.

`world-presentation.js` dùng projection chung 54×27; camera zoom độc lập với canvas asset và chiều cao body. `terrain-cache.js` giới hạn ground tĩnh ở 8 triệu backing pixel; `terrain-transitions.js` giới hạn cache blend. Fog, resource và unit vẫn động. Scale family unit mới còn cần nghiệm thu scene hỗn hợp ở G02.

## Gameplay contract

General chết thì thua; MainResidence bị phá không gây thua. Mỗi bên chỉ có một Residence đang sống hoặc xây dựng; chỉ King được xây lại. Food store và wagon chuyển food hữu hạn; unit dùng ration riêng. Wood/iron được giao về kho chiến lược. Recruitment cost có thể lấy food từ store xa theo cách tính toàn cục: đây là hành vi đã ghi nhận, còn chờ chốt policy, chưa bị gọi là exploit. Các sửa pathing 8 hướng, crowd admission, contact và arrival đã ở simulation public hiện tại; không khôi phục draft lịch sử đã bị từ chối.

Audit 154 xác nhận bug starvation của passenger đang embarked và mitigation sai cho splash victim phụ; [gameplay report](docs/audit/2026-10-09/gameplay-audit.md) có trigger tái hiện. Chúng chưa được sửa sau lượt audit tài liệu.

## Deployment và bằng chứng

Public 149 dùng JS SHA `70808200…6883b`, với 26 asset ở route camp tùy chọn. Local 151 vẫn giữ food đang chờ. Trạng thái/pin nằm trong [PROJECT_STATUS.md](PROJECT_STATUS.md) và receipt 149/151. Build staging không được ghi đè `dist/` đang phục vụ. Runtime content, manifest và version cache phải được promote đồng bộ; các archive rollback vẫn còn. Funnel cung cấp HTTPS public, nhưng host phải luôn sẵn sàng. Chưa có claim về match sống qua restart hoặc mở trang offline từ cold cache.

Công việc tiếp theo: [PROJECT_PLAN.md](docs/PROJECT_PLAN.md). Toàn bộ dự án vẫn chưa hoàn thành.
