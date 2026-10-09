# Nghiên cứu movement212 — chỉ đọc, 0 image call

## Kết luận áp dụng

Nên kiểm soát **một hành động toàn thân xuyên suốt vòng**, rồi hoàn thiện hình minh họa trên hành động đó. Không tiếp tục coi tám prompt riêng lẻ là một walk cycle đã được ràng buộc. Root đã export/display213 dùng211; 212 chưa xem loop213. Ưu tiên tiếp theo: brief loop213 ở89px; sau đó idle cùng family và một lần đi D0 thật. Chưa mở direction/unit khác.

## Bằng chứng đã xem và giới hạn

- Human đã bác155 vì dị dạng; [161](../movement-research-161/worker-research.md) ghi thay đổi khối vai/ngực/hông và tỷ lệ giữa các ảnh dù trang phục còn nhận diện được. Đây là kết quả quan sát, không phải bằng chứng về cơ chế nội bộ của model.
- Đã xem [sheet162](../villager-walk-D0-rough-cycle-162/rough-sheet89.png): cùng camera và hình khối khá đều, nhưng tay/thân ít chuyển động và passing bị che. Guide thống nhất nét vẽ vẫn có thể thống nhất **một chuyển động chưa tốt**. Các sửa169/180 cho thấy chỉ đẩy ankle về trước không đủ: cần đường hông→đùi→gối→cẳng chân, chân chịu tải và che khuất rõ.
- Đã xem [208 actual89](../pure2d-walk-D0-preview-208/actual-eight89.png): F3=205 gần family hơn; F4=192 thân/tay yên và hẹp hơn các frame bên cạnh. Đây là body transition nhìn thấy, không cần chấm vi giải phẫu.
- Đã xem [211 comparison89](../villager-walk-D0-contact-correction-211/comparison89.png): thân rộng và tay đối ứng rõ hơn F4 cũ, bố trí chân contact trái-sau/phải-trước còn. **211 là torso/arm improvement candidate, chưa motion-qualified**, chưa tự thay vào208.
- Trong nghiên cứu212 chỉ xem sheet/comparison, không xem liên tục loop; không tuyên bố smoothness hay world foot lock. [Motion plan](../MOVEMENT_PRODUCTION_PLAN_20261010.md) và review priority giữ các giới hạn này.

Suy luận có cơ sở: mỗi whole-frame generation phải tự dựng lại nhiều biến cùng lúc (camera, khối người, pose, quần áo). Reference giúp mô tả nhưng không khóa quan hệ thời gian hoặc leg ownership. Guide generic làm giảm thông tin về khối ngực/hông, chịu tải và che khuất; ảnh có thể giữ “nông dân mặc đồ giống” mà đổi cấu trúc người. Lịch sử190→191→192 cũng cho thấy nhiều fullbody reference có thể cạnh tranh pose; guide-only giữ đường chân tốt hơn nhưng đổi đầu/thân, whole edit có mục tiêu mới khôi phục appearance. Không kết luận một cơ chế input sẽ luôn bảo đảm pose.

## Nguồn chính và điều rút ra

[Toon Boom Walk Analysis](https://learn.toonboom.com/modules/walk-cycle-animation/topic/walk-analysis1): trích đoạn official search xác minh contact gồm heel/toe; contact đối diện đổi chân; passing có chân đi tới gập; down thấp hơn, up đẩy thân lên. Mở trực tiếp trả403, **không đọc được toàn trang/ảnh**, không dùng nguồn này để khẳng định ESE projection hay quan sát photographic gait.

[Toon Boom Creating Rough Animation](https://docs.toonboom.com/help/harmony-21/essentials/getting-started/animation.html): official search trích rõ bắt đầu torso/legs, thử rough action rồi thêm head/arms/clothes; thêm chi tiết quá sớm tốn sửa và có thể cứng. URL mở trực tiếp404; bằng chứng là snippet, không full-page fetch. [Tie Down](https://docs.toonboom.com/help/harmony-21/premium/paperless-animation/create-tie-down-animation.html) snippet official mô tả đưa drawing về model/volume sau rough, dùng onion skin và playback.

[Krita Animation](https://docs.krita.org/en/user_manual/animation.html) và [Onion Skin](https://docs.krita.org/en/reference_manual/dockers/onion_skin.html) đọc được toàn trang: frame-by-frame, key poses trước inbetweens, rough ở độ phân giải thấp trước line art. Onion skin so sánh frame trước/sau, chỉnh opacity và màu; cần nền trong suốt. Tutorial còn nhấn mạnh occlusion để phân biệt chân gần/xa. Đây là công cụ đối chiếu, không tự tạo natural motion. Chu kỳ tại chỗ và tốc độ di chuyển trong world cần kiểm tra riêng.

## Một workflow thực tế, không viết lại tooling

1. Khóa canonical D0 ESE, camera và body envelope: hat/head, vai/ngực/hông, chiều dài chân và vật liệu. Giữ source1254/pivot6541140, uniform128/89; không fit từng ảnh. Envelope là giới hạn quan sát, không khung cứng cấm thân lên/xuống tự nhiên.
2. Tác giả vẽ **tám rough whole-clothed drawings trong cùng timeline**: contact/down/passing/up × hai bước. Dựng torso/pelvis/load cùng chân; chân swing gập tự nhiên và clearance thấp; tay đối ứng, quần/tunic che khuất nhất quán. Dùng onion trước/sau để sửa cả pose, không sửa riêng ankle hay ghép limbs. Guide có màu depth chỉ phục vụ authoring, không là final style.
3. Xem một loop89px/600ms ngắn, sửa một lỗi hành động thấy rõ. Rough được chọn mới đưa về canonical volume và hoàn thiện whole illustrations. Reference từng frame cần phân vai rõ: whole target giữ pose, canonical giữ appearance; neighbor pair là continuity context, không ba pose cạnh tranh ngang nhau. Built-in image edit vẫn chỉ tạo candidate, không bảo đảm giữ pose/khối.
4. Reuse export/preview hiện có, root chọn actual outputs; xem một vòng ngắn. Nếu còn body pop/phase sai, sửa whole target đó hữu hạn, không blind reroll. Khi loop đủ tốt mới ghép idle cùng family rồi ordinary D0 travel để kiểm tra transition/contact; không đổi simulation để che lỗi.

Đây là workflow đề xuất, **không khẳng định worker đã có năng lực vẽ đạt chuẩn animator hoặc guarantee imagegen**. Một guide sai không trở thành đúng nhờ shading đẹp; một technical playback PASS không thay motion intake.

## Công cụ tái dùng và custody

- [208 exporter](../pure2d-walk-D0-preview-208/export.py), kế thừa [195 exporter](../pure2d-walk-D0-preview-195/export.py): ledger tám actual whole sources, canvas/hash/call closure và fixed transform.
- [208 browser preview](../pure2d-walk-D0-preview-208/browser-preview.mjs): kiểm tra chạy đủ8frames/3cycles/errors; chỉ technical.
- [162 authoring preview](../villager-walk-D0-rough-cycle-162/preview.html): Pause/Step/onion controls có sẵn; Krita timeline/onion là lựa chọn authoring nếu dùng ứng dụng hiện có, không yêu cầu cài hay viết hệ thống mới.
- Canonical: `docs/art/characters/villager-neutral-D00-screen-ESE/raw.png`, SHA256 `145b976ffd1bdf563cb5da78806547e6849424054f2c26fc297e155a0b366e94`.
- 211 raw SHA256 `38ca064c11b145b2fd9e621d375e103e92f9e04ea565c663e18fa786584eccda`; chỉ candidate, giữ mọi original/hold.

212: 0 generation, 0 source/runtime/status/plan changes. Không3D, limb textures, cutouts, source-pixel splice, warps hoặc audit lặp vi chi tiết.
