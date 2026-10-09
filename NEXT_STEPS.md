# Bước tiếp theo — audit 154

Đọc [kế hoạch chi tiết](docs/PROJECT_PLAN.md) và [trạng thái hiện hành](PROJECT_STATUS.md). Snapshot trước 154 nằm trong `docs/audit/2026-10-09/history/`; không tiếp tục các chỉ dẫn “NEXT” cũ trong đó.

## Lượt thực thi tiếp theo

1. **P00 — checkpoint source hiện có:** kiểm tra Git và các handle đang chạy; bảo toàn hồ sơ 147–153 và phần cài đặt 151 chưa commit. Đọc receipt public 149, local 151, parent selection 152 và checkpoint 153. Sau intake, commit source/art hiện có thành checkpoint riêng, không gộp vào tài liệu audit. Public 149 vẫn chạy; không tự build đè lên `dist/`.
2. **Lane A — G01, walk D0:** xem nhanh guide 153 và hai contact đã chọn của 152. Viết một order hữu hạn cho tối đa 2 call imagegen tích hợp, tạo frame toàn thân F2/F6, với 0 retry. Chỉ làm 4 inbetween sau khi các key thực tế được intake. Xuất loop 8 frame, xem ngắn ở kích thước chơi rồi thử di chuyển và Stop thực tế ở D0. Không giả hướng, ghép bộ phận, mirror hoặc sửa warp; không tiếp tục phương pháp 150 đã HELD.
3. **Lane B — C01/GP1:** tái hiện starvation của passenger bằng contract embark thông thường. Sửa physiology trong shared đúng phạm vi, giữ finite food, transport death và General defeat; chạy test naval tập trung. Sau đó xử lý GP2: splash theo từng victim. Theo [gameplay audit](docs/audit/2026-10-09/gameplay-audit.md), không đổi balance để che bug.
4. **Lane C — G02/T01:** tạo catalog coverage và ma trận action/state/direction từ manifest thật. Đo một scene có cả asset cũ/mới để thống nhất chiều cao nhìn thấy và scale idle/walk. G02 có thể bắt đầu từ frame hiện có khi G01 đang làm; nghiệm thu scene hỗn hợp cuối sau G01. Chỉ triển khai registry/compiler khi có order code hữu hạn; không chỉnh scale từng frame. Chuẩn bị ngân sách asset bank theo match và composition cho release mặc định.

Ba worker dùng đúng `gpt-6.1-sol`/`low`; root review và tích hợp. Không để hai worker cùng sửa một file. Khi thiếu đầu vào phụ thuộc, làm việc độc lập trong kế hoạch thay vì tạo output giả.

## Sau những gói trên

- G03: villager đủ 8 hướng/action đã được qualified → G04: infantry/spear/firearm → G05: các family phức tạp → G06: leader.
- W01 có thể làm song song: shipyard/fort/wall/gate, construction/damage/ruin, bờ sông/biển, forest và composition map theo gameplay thực.
- GP3: cảnh báo và progress huấn luyện. GP4: rule/policy và bảng 12 ability với mechanical effect contract/test riêng. Recruitment food và footprint là câu hỏi policy, không tự gán là exploit. GP5: tái sử dụng 6 regression AI và 2 regression naval; chỉ sửa scenario thất bại cụ thể.
- Q01: đo battle đông quân với art hiện tại và room server trên staging. R01: manifest được chấp nhận làm mặc định và lazy bank. R02: release có version, cache và rollback.
- V01: kiểm tra bản cuối trên hai map, hai mode, desktop/mạng ngoài và nghiệm thu visual, sau khi phần bắt buộc của A01 về nguồn lịch sử, controls và cue đã được chấp nhận. Polish tùy chọn không chặn release. Toàn bộ mục tiêu vẫn **INCOMPLETE**.

## Không mở lại

Không mở lại việc chờ API key 041, các phương pháp D0 đã hết order hoặc bị dừng ở 033/035/036/038/094/150, hướng 3D/limb texture/rig, kiểm tra quota, full match chỉ vì thêm building idle, hoặc review giải phẫu/pixel kéo dài.

Food 101 chờ phản hồi riêng; không hỏi lại hoặc chặn mọi lane. Sự chấp nhận wood 032 và iron 141 còn hiệu lực đúng loop đã xem. Đồ mang về dùng walk thường.
