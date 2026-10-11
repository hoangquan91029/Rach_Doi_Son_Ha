# Kế hoạch đồ họa — checkpoint372 / public367, 11/10/2026

[Full project plan](../../PROJECT_PLAN.md) · [Status](../../../PROJECT_STATUS.md) · [Movement plan](MOVEMENT_PRODUCTION_PLAN_20261010.md). Bản kế hoạch cũ checkpoint232 được lưu nguyên byte tại `docs/checkpoints/checkpoint371-entrypoints/docs/art/pipeline/GRAPHICS_PRODUCTION_PLAN.md`. Chỉ phần hiện hành này điều khiển công việc tiếp theo; không tiếp tục order lịch sử.

## Tường thành hiện hành: đá chân thực, chỉ ba mẫu

Yêu cầu người dùng: bỏ toàn bộ hình tường/cổng gỗ khỏi game đang chơi; chỉ làm tường đá ngang X, dọc Y và góc, không mở thư viện biến thể lớn. Tài nguyên gỗ, cây và các công trình khác không thuộc thay đổi vật liệu tường thành.

- Whole painted X362 dùng masks0/1/2/3, Y364 dùng4/8/12, corner365 dùng5. Ba PNG riêng, không quay/lật/ghép ảnh để tạo hướng khác.
- Mỗi ảnh được tạo bằng đúng một builtin imagegen call, không retry; raw1254/pivot627900, uniform runtime128/render42.3225. Đây là ba ảnh hoàn chỉnh cho completed-idle, không phải ba animation.
- Mask khác, cổng và state chưa có tranh dùng nativeSTONE fallback. Không sinh thêm bộ T/cross/mixedGate bằng gỗ hoặc một thư viện góc đồ sộ.
- 15 public wooden payloads/25 descriptors và extraLOCAL woodcollapse321 đã được lưu byte-custody rồi gỡ khỏi active bank. Original/raw/held/rejected/rollback vẫn giữ.

[Selected sources366](../buildings/stone-wall-production-366/README.md), [actual Chrome368](../../qa/stone-raster-route-fix-368/root-intake.json), [actual public Firefox370](../../qa/stone-public-runtime-370/root-intake.json) bind đúng ba mẫu. Root xem một scene ở defaultzoom1.08 và chấp nhận hẹp vật liệu đá, độ đọc và các mối nối X/Y/corner completed-idle. Không suy ra allbuilding/animation acceptance.

## Bản web hiện tại

PUBLIC367 URL trần nạp stone8/worldfalse; optional `?art=fort` nạp37 descriptors gồm29 non-wall/gate giữ nguyên và8 stone mappings dùng3 PNG. Bản196 files/newJS `index-eaEH6Li-.js` đã triển khai từ SAMEsealed368. Backend230 giữ nguyên, không restart. LOCAL pendingfood recipe còn riêng, PUBLIC không có foodCHAR/D0/woodcollapse321.

370 Firefox normalHTTPS ordinary three-wall scene đạt8ready/3decodedPNGs/12portraits,1884actualrasterdraws, masks5/2/8 và cả3opaque picks; Pause/Resume/Stop/menu,7 responsepins và errorsnetworkHTTP0. Toàn bộ handle đóng;522byte-mode preservation pins/public196/backend230 giữ nguyên. Không replay scene đã đạt chỉ để có thêm receipt. Paired rollback hiện hành là public345/private353 + immutable230; xem PROJECT_STATUS trước promotion.

## Những gate vẫn mở

| Hạng mục | Nguồn/evidence hiện hành | Việc còn thiếu |
|---|---|---|
| Villager D1 | Walk014/runtime016; wood032 và iron141 owner accepted đúng vòng đã xem | Hướng khác và action theo gameplay; food101 chờ riêng |
| Villager D0 | Eight whole frames213 + idle216; actual travel/Pause/Resume/Stop233 technical closure | Owner naturalness, worldcontact, bodyvolume/shadow và family scale; runtime install/fanout còn mở |
| Roster và leaders | Registry302 có9 types và12 historical IDs; portrait/source custody giữ nguyên | Finished realistic whole sprites,8 hướng và actions; registry không phải artwork |
| Stone fortifications | Ba completed-idle whole images và nativeSTONE fallback | Construction/hit/destruction phù hợp ba-shape scope; cổng vẫn fallback |
| Other buildings | Các completed-idle tranh đã qualified hẹp; wholebuilding compiler359 | Construction/hit/death/attack artwork cần thiết, không thay bằng idle để che thiếu |
| World | Terrain340/345 receipts; original forest/shore/hill/mountain sources | Composition hai map, shore/forest/mountain repetition và dense-unit scene |
| Production | Defaultstone public367 và nhiều proof gameplay/network trước đó | Accepted full art/default coverage, densecombat+rooms performance, external-device WAN và finalbothmaps/twomodes |

Pending question195 không phê duyệt213. Không replay Stop233, gọi character blind hoặc audit still/anatomy nhiều lần. Hàng mang về dùng ordinarywalk; không cần thêm carry cycle. Old wooden collapse331/332 là lịch sử, không đưa trở lại active production.

## Quy trình sản xuất và thứ tự tiếp theo

1. **Tường đá:** giữ đúng ba mẫu đã có. Tiếp theo chỉ một pilot state thực sự còn thiếu, bắt đầu từ canonical stone source, work order hữu hạn và whole illustration. Không mở topology library mới. State/event phải nối với simulation-authoritative API, death precedence và fallback giữ đúng.
2. **Movement:** một brief actual-size continuous look cho candidate hiện hành và sửa lỗi thấy rõ nếu cần. Whole clothed rough action → keys → neighbor illustrated inbetweens → atlas/loop → same-family idle → actualUI movement/stop. Không coi technical playback là owner naturalness.
3. **Family scale:** thống nhất visible height idle/walk/work trong scene thật trước character fanout. Sau pilot đạt mới mở villager directions/actions rồi infantry, spear/firearm; horse/rider, wagon, crew/gun và ships có pilot family riêng.
4. **Maps và buildings độc lập:** có thể làm song song các package không dùng chung file/guard. Mỗi package có selected-source ledger, one actual-size preview và receipt; không biến mỗi frame thành dự án quản trị riêng.
5. **Release:** relevant actual scene + exact source/build + current paired rollback trước promotion. Không bật toàn bộ pending candidate rồi gọi full art finished.

Reuse camera, pose specifications, timing, export/compiler, atlas schema, alpha picking, banks và runtime API. Mỗi final frame vẫn là whole illustration; không xoay texture tay/chân, cắt ghép nguồn pixel hoặc fit từng frame. Không mirror tự động. Builtin imagegen only; mọi code/art worker exactSol6.1Low, tối đa3worker+root với ownership độc lập.

## Kích thước, bộ nhớ và kiểm tra

Humanoid mục tiêu visible64–96px ở default zoom. Raw1254 originals giữ nguyên; working/export khoảng256 và runtime128, dùng một transform/pivot cho toàn family. Những action hiện tại render89 không tự chứng minh cùng visible scale với idle cũ. Stone runtime128/render42.3225 là footprint công trình đã kiểm tra thực tế, không áp humanoid scale cho tường.

128²RGBA là64KiB/frame;64 frames là4MiB trước padding/copies. Dùng selected-map/roster banks, dedup và release khi rời trận; không nạp toàn roster khi chưa cần. Baseline350 ordinary1/5/8rooms/~20ticks/sec không phải densecombat/WAN/finalperformance; không tối ưu suy đoán khi chưa có concern đo được.

Một brief gameplay-size look và sửa visible issues; không microanatomy/cloth/pixel audit. Giữ provenance và lightweight browser/state checks. Candidate build phải isolatedcwd/absoluteoutDir/exactViteconfig, source retention/preflight trước seal; không thay nguồn giữa trial. Chờ mọi preservationguard đóng rồi mới sửa canonical/HEAD. Public service intentionallyrunning, không ghi đè active dist/restart khi test.

Full master/web/historical/visual81–145 và later goal vẫn **INCOMPLETE**. Không tuyên bố lịch5hACTIVE khi automation311 native schedule còn thiếu; quiet continuation intent giữ nguyên.
