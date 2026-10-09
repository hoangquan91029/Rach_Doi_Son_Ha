# Trạng thái dự án — audit 154, ngày 2026-10-09

**INCOMPLETE.** Kế hoạch hiện hành: [docs/PROJECT_PLAN.md](docs/PROJECT_PLAN.md). Hàng đợi: [NEXT_STEPS.md](NEXT_STEPS.md). Báo cáo: [audit 154](docs/audit/2026-10-09/README.md).

## Trạng thái đã đối chiếu

- Trước audit, Git ở HEAD `77c0ae1`, với thay đổi Camp 151 và hồ sơ 147–153 chưa commit. Audit không xóa, reset hoặc gộp ngầm phần việc này.
- PUBLIC 149: [bản chơi thử với 26 asset](https://kieu-hoang-quan-loq-15iax9.tail5247a0.ts.net/?art=camp), JS `index-05PkH4eu.js`, SHA `70808200c04fa3547aa4204a0baa6e04546f6d9206c93667ee4c3edf7556883b`. Audit chỉ đọc đã xác nhận HTTPS và hash hiện tại. Service đang chạy với PID 157023; có 0 room lúc đo. URL không có query vẫn dùng đồ họa dự phòng của bản development.
- LOCAL 151 đã cài đúng code và asset của Camp 26 từ bản 148; vẫn giữ phần nhân vật thu thập food ở local. Receipt 151 tái sử dụng bằng chứng của đúng bản 148, không được gọi là một lượt test mới trong audit.
- Bằng chứng 149 trên Chromium và Firefox xác nhận: xây Camp → hiển thị idle và chọn Camp → huấn luyện cavalry → Pause/Resume → chọn nhóm bằng F2 → Stop → menu. Có 26 asset đồ họa, 12 portrait và 0 lỗi. Bằng chứng online trên cả hai map của 089 và chiến thắng AI offline trên public của 090 vẫn có giá trị trong phạm vi đã thử; chúng không chứng minh đồ họa cuối cùng.
- Người dùng đã chấp nhận độ tự nhiên của loop D1 thu thập wood ở 032 và iron ở 141. Loop food 101 và runtime local đã có, nhưng còn chờ phản hồi. Candidate South walk 014 đã chạy thực tế; không chuyển sự chấp nhận wood/iron sang walk.
- D0: F0 từ 033 và F4 từ 152 là hai candidate tiếp đất bằng chân đối diện đã được chọn. Cặp 150 ở trạng thái HELD. F2/F6 của 153 mới là guide, với 0 image call; chưa có loop D0. Tại thời điểm audit, không còn call hoặc worker production nào đang mở; ba worker audit đã kết thúc.

## Khoảng thiếu quan trọng

| Nhóm | Trạng thái |
|---|---|
| Core Single Player, online, kinh tế và hậu cần | Đã triển khai, có contract và trận thật; hai lỗi mới đã xác nhận cần sửa |
| Lỗi và thiếu sót đã xác nhận | Starvation của passenger đang embarked bị bỏ qua; splash dùng armor của mục tiêu chính cho mục tiêu phụ; thiếu cảnh báo food thấp; progress huấn luyện sai khi có modifier |
| Đồ họa unit | Camp manifest có 26 asset entry và 47 frame rectangle; chỉ villager D1 có loop walk/wood/iron. Phần lớn 11 loại unit và 12 leader còn thiếu action hoặc direction |
| Building và map | Có idle cho 6/10 building; còn thiếu 4 idle và các trạng thái construction/hit/death. Hai map chơi được nhưng chưa đạt composition cuối cùng |
| Scale | Canvas render 89 px không có nghĩa body cao 89 px. Unit cũ và mới khác scale; cần thống nhất trong scene thực có cả hai |
| Public release | Còn mở: đồ họa mặc định, asset bank theo match, cache/version, hiệu năng bản hiện tại khi đông quân, thiết bị/mạng ngoài và nghiệm thu cuối cùng |

Ba audit con tách riêng tình trạng triển khai, bằng chứng test, chấp nhận visual và public release. Audit 154 chỉ sửa tài liệu và kế hoạch; không sửa bug, tạo art, build, deploy hoặc chạy full match. Kế hoạch không tự đóng bất kỳ gate nào.

## Điều phối

Dùng frame toàn thân pure 2D, imagegen tích hợp và đúng `gpt-6.1-sol`/`low` cho worker code/art. Được phép làm song song. Không theo dõi quota, không dùng API key, 3D hoặc texture chân tay rời. Đồ mang về dùng walk thường. Tất cả source, bản held/rejected và receipt vẫn được giữ nguyên.

Lịch sử trước audit được giữ nguyên byte: [history inventory](docs/audit/2026-10-09/history/inventory.json). Tài liệu lịch sử không phải lệnh để tiếp tục task cũ. Chỉ ghi COMPLETE khi mọi tiêu chí quan trọng đã được đóng trên bản release cuối cùng.
