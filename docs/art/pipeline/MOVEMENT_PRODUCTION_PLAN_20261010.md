# Kế hoạch movement — 10 October 2026

Mục tiêu trước mắt là **một vòng đi D0 tám frame thực sự tự nhiên**, giữ phong cách minh họa chân thực hiện có. Chưa mở thêm hướng hoặc unit. Kế hoạch này dựa trên ảnh đã trả về; các bản giữ lại không được tính là thành phẩm.

## Kết luận nghiên cứu trên asset của project

Có hai vấn đề riêng.155 làm lệch hình thể và bị người dùng bác bỏ. Ở các thử nghiệm sau, camera/thân đã cải thiện nhưng bước đối diện vẫn không xuất hiện: ảnh152 được gắn nhãn đối diện trong khi đường chân nhìn thấy vẫn giống033.188 sửa camera rồi tiếp tục sao chép bố cục chân đó. [Đối chiếu đường chân](villager-walk-D0-contact-188/POST_INTAKE_PATHS.md) và [phân tích](movement-research-161/CONTACT_OWNERSHIP_188.md) giữ nguyên bằng chứng.

189 dùng hai hình nháp **toàn thân có trang phục**, phân biệt chân A/B bằng đường nối hông–gối–sandal và thứ tự che khuất, thay tên trái/phải không được xác minh. Guide không phải asset hiển thị và không phải limb texture.

190 đính kèm guide cùng ảnh toàn thân cũ vẫn lặp pose.191 chỉ đính kèm guide: đường chân thay đổi nhưng nón che mặt và camera/hình thể lệch.192 dùng chính191 làm **ảnh đích toàn thân**, canonical làm nguồn diện mạo; bản trả về giữ đường chân mới và khôi phục mặt/nón. Root chọn192 làm key thử F4. Đây là bằng chứng một bước sửa có ích, **chưa chứng minh workflow sản xuất hàng loạt hoặc chuyển động mượt**.

## Nguồn hiện hành

| Vị trí | Whole PNG thực tế | Quyết định |
|---|---|---|
| F0 contact |188 |Requested F4 thất bại; explicit reassignment chỉ sang F0 giữ nguyên raw, thay033 để đồng bộ dáng thân.|
| F2 passing |185 |Chọn cho vòng pilot; không suy motion PASS từ ảnh tĩnh.|
| F4 contact đối diện |192 |Root thấy đường chân khác188 và mặt/nón được khôi phục; chọn cho vòng pilot.|
| F6 passing |182 |Bản hạ footlift từ181; chọn cho vòng pilot.|
| F1 |193 |Root chọn cho vòng thử; down subtle, original worker warning giữ nguyên.|
| F3 |197 sau guide196 |Root chọn provisional để xem đủ vòng; body/head/phase warnings giữ nguyên.193F3 nonfamily không dùng.|
| F5/F7 |194 |Hai whole PNG được chọn cho vòng thử, chưa motion approval.|

[Ledger bốn key](villager-walk-D0-contact-192/current-keys.json) bind raw/hash/slot. Các raw155/152/188-requestedF4/190/191 và mọi hold giữ nguyên.191 chỉ là edit target, không approved continuity source. Không lật ảnh hoặc lấy nhãn prompt thay đường chân thực tế.

## Quy trình thực thi ngắn

1. **Giữ identity và camera:** canonical hiện có là nguồn diện mạo/tỷ lệ; không tạo limb textures hoặc model3D. Guide toàn thân chỉ xác định pose/ownership.
2. **Khi tham chiếu ảnh cũ kéo pose về sai:** tách bước render guide thành whole illustration và bước sửa diện mạo trên chính ảnh đó. Không ghép pixel/parts; cả hai đầu ra đều là PNG minh họa toàn thân. Đây là cách vừa kiểm chứng ở191/192, chưa mặc định cần hai call cho mọi frame.
3. **Bốn inbetween:** mỗi frame dùng predecessor và next key thực tế, với vai trò rõ. F1 chịu tải sau F0; F3 chuyển sang contact đối diện; F5 chịu tải sau F4; F7 chuẩn bị trở lại F0.193/194 chạy song song vì ownership file độc lập. Không retry một slot lỗi bằng prompt nguyên trạng.
4. **Export195:** chỉ nhận đủ tám source thực tế được root chọn, đúng hash. Tái sử dụng exporter atlas/APNG hiện có; thiếu/held input phải dừng, không lặp key để giả đủ tám frame.
5. **Một vòng xem ngắn:** đúng600ms (8×75ms), cell89 ở preview và cùng transform cả family. Xem chuyển động liên tục, F7→F0, đổi chân trụ, dáng người và silhouette. Chỉ sửa lỗi nhìn thấy ở kích thước gameplay; không anatomy/cloth/pixel scoring lặp.
6. **Tích hợp candidate:** atlas D0 walk qua API state/direction hiện có; phase theo quãng đường entity, không can thiệp simulation speed. Actual UI đi đúngD0, Pause/Resume/Stop và idle transition. Preview đứng yên không chứng minh world foot lock.
7. **Mở rộng sau pilot:** thống nhất idle/walk/work family scale; hoàn thành villager directions/actions, rồi một infantry pilot và một complex family. Tái sử dụng pose plans/timing/export/atlases/runtime, nhưng mỗi frame cuối vẫn là minh họa riêng. Không mở toàn roster bằng checksum hoặc technical PASS.

## Kích thước và kiểm tra vừa đủ

Working/export whole canvas256; runtime128; preview cell89 tương ứng body nhỏ hơn cell, gần mục tiêu unit64–96px khi trình bày đúng. Raw builtin1254 bắt buộc bởi đầu ra tool được lưu custody, không nạp vào game. Dùng một transform toàn canvas/pivot source654,1140 cho cả chu kỳ, không fit/shift từng frame. Atlas tám128cell chứa512KiB RGBA trước padding/copies; chỉ bank cần dùng được decode. Kiểm tra hash/alpha/đủ frame/atlas, browser load và lỗi cơ bản; không lấy chúng thay visual acceptance.

Family idle/walk/work scaleG02 vẫn cần scene thật. Pose sở hữu chân đúng là điều kiện để làm vòng thử, không phải footlock/motion approval. Nếu loop có lỗi rõ thì sửa một danh sách ngắn trước directions/units. Không thay tốc độ game, dùng blur hoặc thu nhỏ để che lỗi.

## Trạng thái tổng thể

Full game **INCOMPLETE**. Public149 chưa nhận các frame này. Root giữ các receipt gameplay186 và merged browser183/187 riêng; chúng không chứng minh animation. Builtin imagegen, Sol6.1Low; không API key, quota polling, Blender, cutout, limb textures hay source-pixel splicing. Đồ mang về dùng walk thường.

## Kết quả preview195 và việc tiếp theo

[APNG thực tế](pure2d-walk-D0-preview-195/actual-output/playback/actual-eight-frame-loop.png) và [receipt](pure2d-walk-D0-preview-195/root-intake.json) đã xuất từ đúng tám nguồn. Browser chạy F0–F7 qua ba vòng600ms,zeroerrors; all source/output hashes được bind. Gói195 không tạo ảnh mới và không cài runtime.

Root đã hiển thị vòng thật và hỏi một lần về naturalness/mượt; chưa có câu trả lời. F3/F4 torso/arms khác neighbors là cảnh báo rõ, không bị technical PASS che đi. Nếu continuous look cho thấy giật thì sửa đúng các frame đó, giữ phần đã tốt và bảo toàn loop195. Nếu đủ tốt thì candidate D0 runtime với canonical idle cùng scale, rồi actual UI travel/Pause/Stop. Không mở thêm directions/units trước pilot runtime intake.

Hai-stage guide render → whole identity edit vừa giúp tạo contact192, nhưng chưa chứng minh sản xuất hàng loạt. Không mặc định thêm hai call cho từng frame; chỉ dùng khi thực sự cần kiểm soát pose/diện mạo. Chỉ đo throughput/qualified output sau ít nhất hai cycle được chấp nhận, không dự báo ngày hoàn thành từ số file.
