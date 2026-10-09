# Trạng thái dự án — movement research 161, ngày 2026-10-09

**INCOMPLETE.** Kế hoạch hiện hành: [docs/PROJECT_PLAN.md](docs/PROJECT_PLAN.md). Hàng đợi: [NEXT_STEPS.md](NEXT_STEPS.md). Báo cáo: [audit 154](docs/audit/2026-10-09/README.md).

## Trạng thái đã đối chiếu

- Checkpoint `64f7090` đã bảo toàn Camp151 và art/receipt147–153 sau audit154. Nghiên cứu161 và các gói local156/157/159/160 bổ sung bên dưới; không đổi public149.
- PUBLIC 149: [bản chơi thử với 26 asset](https://kieu-hoang-quan-loq-15iax9.tail5247a0.ts.net/?art=camp), JS `index-05PkH4eu.js`, SHA `70808200c04fa3547aa4204a0baa6e04546f6d9206c93667ee4c3edf7556883b`. Audit chỉ đọc đã xác nhận HTTPS và hash hiện tại. Service đang chạy với PID 157023; có 0 room lúc đo. URL không có query vẫn dùng đồ họa dự phòng của bản development.
- LOCAL 151 đã cài đúng code và asset của Camp 26 từ bản 148; vẫn giữ phần nhân vật thu thập food ở local. Receipt 151 tái sử dụng bằng chứng của đúng bản 148, không được gọi là một lượt test mới trong audit.
- Bằng chứng 149 trên Chromium và Firefox xác nhận: xây Camp → hiển thị idle và chọn Camp → huấn luyện cavalry → Pause/Resume → chọn nhóm bằng F2 → Stop → menu. Có 26 asset đồ họa, 12 portrait và 0 lỗi. Bằng chứng online trên cả hai map của 089 và chiến thắng AI offline trên public của 090 vẫn có giá trị trong phạm vi đã thử; chúng không chứng minh đồ họa cuối cùng.
- Người dùng đã chấp nhận độ tự nhiên của loop D1 thu thập wood ở 032 và iron ở 141. Loop food 101 và runtime local đã có, nhưng còn chờ phản hồi. Candidate South walk 014 đã chạy thực tế; không chuyển sự chấp nhận wood/iron sang walk.
- D0: actual155 F2/F6 **bị người dùng bác bỏ vì dị dạng**. [Rejection](docs/art/pipeline/villager-walk-D0-passing-keys-155/human-rejection.json) thay quyết định root trước đó, giữ nguyên history/source.158 chỉ có prep và đã dừng,0call.033F0/152F4 vẫn là contact candidates, chưa có loop đạt. [Nghiên cứu161](docs/art/pipeline/movement-research-161/README.md) đổi sang cả chu kỳ nháp đúng một canonical trước khi thử minh họa hữu hạn. Không có image call mới trong nghiên cứu.
- LOCAL gameplay: [156](docs/qa/passenger-physiology-156/root-intake.json) sửa physiology/starvation của passenger; [159](docs/qa/per-victim-splash-159/root-intake.json) tính bonus/armor/terrain cho từng splash victim. Exact staging suite **140/140 PASS** gồm AI/naval và test hiện hành; source canonical được đối chiếu đúng binding. Không có browser/full-match/deploy mới từ các gói này; public149 còn dùng simulation cũ.
- [157 coverage](docs/art/pipeline/art-coverage-157/README.md) kiểm manifest/hash và coverage thật, không cấp visual PASS. [160](docs/qa/world-art-route-contracts-160/README.md) thay hai assertion route terrain-only lỗi thời bằng contract hiện hành, không đổi runtime guards.
## Khoảng thiếu quan trọng

| Nhóm | Trạng thái |
|---|---|
| Core Single Player, online, kinh tế và hậu cần | Đã triển khai, có contract và trận thật; hai lỗi xác nhận đã sửa local156/159, chưa promote public |
| Lỗi và thiếu sót đã xác nhận | Passenger starvation và splash đã có fix local; còn thiếu cảnh báo food thấp và progress huấn luyện đúng duration modifier; policy/ability contracts còn mở |
| Đồ họa unit | Camp manifest có 26 asset entry và 47 frame rectangle; chỉ villager D1 có loop walk/wood/iron. Phần lớn 11 loại unit và 12 leader còn thiếu action hoặc direction |
| Building và map | Có idle cho 6/10 building; còn thiếu 4 idle và các trạng thái construction/hit/death. Hai map chơi được nhưng chưa đạt composition cuối cùng |
| Scale | Canvas render 89 px không có nghĩa body cao 89 px. Unit cũ và mới khác scale; cần thống nhất trong scene thực có cả hai |
| Public release | Còn mở: đồ họa mặc định, asset bank theo match, cache/version, hiệu năng bản hiện tại khi đông quân, thiết bị/mạng ngoài và nghiệm thu cuối cùng |

Ba audit con tách riêng tình trạng triển khai, bằng chứng test, chấp nhận visual và public release. Audit154 là snapshot chỉ tài liệu; các gói156–161 bên trên ghi thay đổi sau audit. Rejection/research không đóng visual gate; local tests không chứng minh bản public đã nhận fix.

## Điều phối

Dùng frame toàn thân pure 2D, imagegen tích hợp và đúng `gpt-6.1-sol`/`low` cho worker code/art. Được phép làm song song. Không theo dõi quota, không dùng API key, 3D hoặc texture chân tay rời. Đồ mang về dùng walk thường. Tất cả source, bản held/rejected và receipt vẫn được giữ nguyên.

Lịch sử trước audit được giữ nguyên byte: [history inventory](docs/audit/2026-10-09/history/inventory.json). Tài liệu lịch sử không phải lệnh để tiếp tục task cũ. Chỉ ghi COMPLETE khi mọi tiêu chí quan trọng đã được đóng trên bản release cuối cùng.
