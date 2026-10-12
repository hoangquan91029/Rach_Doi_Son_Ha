# Lượt thử F4/465 — 486

Người dùng chọn **“Thử một edit trên F4/465”**. Đã thực hiện đúng một call imagegen tích hợp, không API và không retry. Request, prompt, token claim, settlement và raw được giữ nguyên. Các lệnh477/482/483 không mở lại.

Kết quả **HELD**: chân phía khiên lại dẫn trước xuống phải, chân phía kiếm lùi lên trái. Nhân vật vẫn nhận ra đúng original, nhưng không giữ được ContactB của465. Sheet dùng canvas71px đồng nhất (42logical ×1.68), không fit theo từng frame. Không ghép loop, đo stride mới, cài runtime hoặc triển khai.

Một lỗi tổ chức reference được sửa sau lượt thử: trước đây validator buộc appearance master đứng đầu. Nay key/correction có thể khai báo **edittarget** đầu tiên và appearance anchor thứ hai. Target phải là đúng wholeframe selected của current job/phase/action/direction; held/excluded/foreign không được dùng. `prepareOrder` trả thứ tự `referenced_image_paths` đã kiểm tra để chuyển trực tiếp cho tool. Legacy không thay đổi. Tám tests tập trung PASS; không fullsuite/browser lại cho thay đổi prompt này.

Lượt thực tế486 vẫn dùng originalmaster trước và465 thứ hai theo request được lưu; không sửa lịch sử thành target-first. Thứ tự mới chưa được gọi ảnh và chưa chứng minh điều khiển pose. Không thể xác định thứ tự input là nguyên nhân duy nhất của thất bại.

ONE call đã hết. Không tự gọi lại, reset budget hoặc mở fanout. Pilot cần key ContactB dùng được; một thử nghiệm mới phải có phạm vi và giới hạn mới được người dùng chọn. Artwork gốc và toàn bộ held được bảo toàn; public451/backend230 không đổi.
