# Audit154 — Rạch Đôi Sơn Hà

Ngày:9/10/2026. Yêu cầu người dùng: audit lại kỹ và lập kế hoạch chi tiết gắn với project. Baseline source: `77c0ae1` cộng thay đổi151 và hồ sơ147–153 chưa commit. Không triển khai, sửa gameplay hoặc tạo ảnh trong lượt này.

## Tài liệu chính

- [Kế hoạch toàn project](../../PROJECT_PLAN.md): ưu tiên, packageIDs, phụ thuộc, ba lane song song, milestone và tiêu chí nghiệm thu.
- [Gameplay audit](gameplay-audit.md): implementation/test matrix,7findings, hai reproduction lỗi đã xác nhận và các quyết định thiết kế chưa chốt.
- [Art/animation audit](art-animation-audit.md): coverage thực,11unit types/10buildings/12leaders, pipeline reuse, scale và workload giả định.
- [Release/performance audit](release-performance-audit.md): current public hash/health, default experience, vận hành/cache và measurement gaps.
- [Nghiên cứu kỹ thuật](RESEARCH.md): nguồn chính thức và lý do giữ/chỉnh kiến trúc.
- [Lịch sử trước sửa](history/inventory.json):8tài liệu giữ nguyên byte cùngSHA256; không xóa asset hay receipt cũ.

## Kết luận có tác động lớn

1. Core game đã có nhiều mechanics và public match proofs. Không cần viết lại engine; finalgame vẫn chưa hoàn tất.
2. G1: passenger lên tàu bỏ qua starvation progression. G2: splash dùng mitigation của primary cho secondary. Hai lỗi được cô lập trong bộ nhớ, chưa sửa ở audit này.
3. Current camp26 chỉ có47frame rectangles, phần lớn là ảnh tĩnh; ba loop8frame đều ở villagerD1. Static identity8views không phải8animated directions.
4. D0 đã tiến tới hai contact candidates033/152;153guide chưa gọi ảnh. Đóng trọn cycle là critical path trước fanout.
5. Oldidle và newaction khác family scale.89px rendercanvas không tương đương89px visiblebody.
6. DefaultURL vẫn dùng development fallback;26asset slice opt-in và foodlocal là các trạng thái khác nhau. Finalrelease cần catalog/defaultmanifest/banks.
7. Final dense performance, physical external desktop/WAN và finalmap/roster acceptance chưa có bằng chứng đủ. Host online vẫn là điều kiện để publiclink hoạt động.

## Phương pháp và giới hạn

Ba worker exact `gpt-6.1-sol`/`low` audit độc lập gameplay, art và release. Root đối chiếu yêu cầu, đọc các source/receipts liên quan, xem một actual scene149, nghiên cứu tài liệu chính thức và hợp nhất kế hoạch. Worker gameplay tái hiện hai branch trong isolated in-memory fixtures; release worker GET publicHTTPS/health đọc-only. Không chạy lại fullmatch/testsuite, không giả định báo cáo là regressionPASS.

Các reproduction ghi trong gameplay report là diagnostic source findings, không phải ảnh hưởng đo được trên một trận ordinaryUI. Hai policy questions (global recruitmentfood, center-only terrain placement) không bị gọi thànhbug nếu chưa có rule quyết định. Không có securityscan tổng quát hoặc khẳng định không cònbug.

Bản master plan thống nhất thứ tự và ngân sách đề xuất; báo cáo con giữ snapshot audit với những đề xuất chi tiết. Các dòng nói topdocs còn145/146 là mô tả trước lần rút gọn154. Final completecriteria không thay đổi. Lượt kế tiếp tiếp tục từNEXT_STEPS; không có artcall nào mở bởi audit154.
