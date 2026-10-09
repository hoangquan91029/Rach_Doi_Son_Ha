# Khoảng thiếu hiện hành — audit 154

Kế hoạch chính: [PROJECT_PLAN.md](PROJECT_PLAN.md). Bằng chứng và reproduction chi tiết: [audit 154](audit/2026-10-09/README.md). Văn bản cũ được giữ nguyên byte trong [archive](audit/2026-10-09/history/docs/KNOWN_GAPS.md).

| ID | Trạng thái | Khoảng thiếu / gói phụ trách |
|---|---|---|
| G1 | Bug đã xác nhận bằng reproduction tách biệt | Passenger đang embarked bỏ qua tiến trình starvation; C01/GP1 |
| G2 | Bug đã xác nhận bằng reproduction tách biệt | Victim phụ của artillery dùng mitigation của mục tiêu chính; C01/GP2 |
| G3 | Thiếu UX đã xác nhận | Chưa có cảnh báo army food thấp; GP3 |
| G4 | UI sai đã xác nhận | Progress huấn luyện không dùng initial duration đã điều chỉnh; GP3 |
| G5/G6 | Khoảng thiếu policy, chưa chứng minh exploit | Recruitment food toàn cục; đặt building theo terrain ở tâm; GP4 |
| G7 | Bằng chứng một phần | 12 ability contract và việc dùng cùng identity cho hai role; GP4 |
| V1 | Chưa đủ | State minh họa toàn thân, 8 hướng và body của 12 leader; G01–G06 |
| V2 | Chưa nhất quán | Scale family nhìn thấy giữa neutral cũ và action mới; G02 |
| V3 | Chưa đủ | 4 building idle và các trạng thái construction/damage/destruction; W01 |
| V4 | Chưa chấp nhận composition cuối | Bờ sông/biển, forest, mép hill bị cắt, mountain lặp lại và battle đông quân trên cả hai map; W01 |
| R1 | Mặc định vẫn là development | Art đầy đủ nhất cần `?art=camp`; nhân vật food còn chờ ở local; T01/R01 |
| R2 | Chưa đo workload cuối | Hiệu năng browser với đông quân, nhiều room, WAN và thiết bị ngoài; Q01/V01 |
| R3 | Giới hạn vận hành | Host phải online; room trong bộ nhớ mất khi restart; cần đồng bộ generation của manifest/cache; R02 |
| D1 | Đã xử lý bằng tài liệu 154 | Chỉ dẫn cũ và log checkpoint hơn 100 KB đã chuyển vào history nguyên byte; giữ tài liệu hiện hành ngắn gọn |

Bằng chứng crowd 088, public 089/090 và thử nghiệm hẹp 149 vẫn có giá trị trong phạm vi của chúng. Câu cũ “no unit clearance exists” là lịch sử, không được dùng để mở một lượt sửa trùng. Chưa có chấp nhận visual cuối cùng hoặc claim dự án hoàn thành.

Guard decoded atlas 128 MiB không tính các bản sao và cache khác trong browser. Offline sau khi tải không phải reload offline từ cold cache. Food còn chờ review không phải lý do để tạo lại source đã hoàn chỉnh.
