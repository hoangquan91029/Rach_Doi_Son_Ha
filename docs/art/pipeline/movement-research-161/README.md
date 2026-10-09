# Movement 161 — sửa cách sản xuất sau phản hồi của người dùng

Ngày 2026-10-09. **Research complete; D0 animation chưa đạt.** Không có image call mới trong gói này. Phản hồi người dùng bác bỏ hai frame F2/F6 của 155 vì dị dạng. [Human rejection](../villager-walk-D0-passing-keys-155/human-rejection.json) thay thế quyết định chọn trước đó; receipt cũ và toàn bộ source được giữ. [158 đã dừng](../villager-walk-D0-inbetweens-158/stop-receipt.json), với 0 call.

## Lỗi thực tế và nguyên nhân có thể kiểm soát

Ở cùng phép scale, frame passing có thân cao/hẹp, vai và hông co lại, chân trụ dài thẳng nổi bật, chân nâng cuộn sát chân kia. Chân passing có thể gần nhau hơn contact, nhưng ngực/hông không được biến thành một người khác. Vật liệu vẫn giống mẫu không đủ để giữ identity. Thêm bốn frame trung gian sẽ nối những hình thể không tương thích, không chữa được chúng.

Guide 153 đã mang hình thể gầy/cứng đó; request 155 đặt guide làm PRIMARY và chỉ dùng hai contact làm tham chiếu ngoại hình. Canonical directional master không được đính kèm trực tiếp trong hai call 155. Vì thế bước điều khiển pose chưa đồng thời điều khiển được tỷ lệ thân người. Đây là suy luận từ input/output, không phải khẳng định về cơ chế nội bộ của model. Root đã chọn key quá sớm; phản hồi người dùng là quyết định hiện hành.

Renderer chỉ chọn và vẽ ảnh toàn thân, không làm biến dạng tay/chân. Do đó lỗi này nằm trong source illustrations. Ngoài ra, idle D0 cũ và action D1 mới khác scale; đó là vấn đề runtime riêng, không sửa bằng cách kéo giãn F2/F6. Chi tiết: [nghiên cứu hình thể](worker-research.md), [contract runtime](runtime-motion-contract.md).

## Quyết định thay đổi

Giữ pure 2D minh họa chân thực. Thay **guide rời → repaint từng key → cố nối** bằng:

**Một mẫu D0 → tám bản vẽ nháp toàn thân cùng tỷ lệ → xem trọn vòng → chuẩn hóa hình thể → một thử nghiệm minh họa → các key/inbetween hoàn thiện → atlas → gameplay.**

Mẫu D0 cho gói authoring tiếp theo là `docs/art/characters/villager-neutral-D00-screen-ESE/raw.png`, SHA `145b976ffd1bdf563cb5da78806547e6849424054f2c26fc297e155a0b366e94`. Mẫu 007, hai contact 033/152 và walk D1 là tài liệu đối chiếu; không dùng chúng như các mẫu tỷ lệ ngang quyền. Hai contact cũ chỉ được giữ nếu hợp với cả vòng nháp mới; không buộc hình thể mới phải khớp bằng warp, ghép pixel hoặc fit từng frame.

## Gói kế tiếp hữu hạn: 162, chỉ authoring nháp

| Bước | Việc cụ thể | Output và giới hạn |
|---|---|---|
| A — model drawing | Quan sát mẫu D0; vẽ lại contour toàn thân với độ rộng mũ, vai, ngực, hông, độ dài áo/quần, hình dép và góc camera nhất quán | Một model drawing và landmark sheet nhỏ. Không texture/limb rời; không đo giải phẫu chi li |
| B — chu kỳ | Vẽ original clothed drawings cho tám phase dưới đây; thân/ngực/hông/tay/chân cùng chuyển động, không thay riêng chân vào thân bất động | Tám bản nháp toàn thân, có near/far ownership và ground plane. **0 image call**, không tái sử dụng guide 153/158 làm template hình thể |
| C — xem nháp | Một loop 600 ms với 8 hold bằng nhau làm reference cadence; thêm ghost/onion-skin các hình liền kề để thấy đổi khối; xem ngắn ở size chơi | Đây là authoring preview, không phải art final hoặc ordinary gameplay proof. Sửa lỗi hình thể/pose rõ trong bản vẽ, không polish cloth |
| D — intake | Kiểm cùng một người, chuyển trọng lượng hợp lý, chân qua nhau tự nhiên và F7→F0 liền mạch | Nếu nháp chưa có dáng đi hợp lý thì sửa nháp, không gọi repaint để che nó |

| Frame | Phase | Quan hệ toàn thân cần diễn tả |
|---|---|---|
| F0 | Contact A | Chân trước chạm gót, chân sau kết thúc đẩy; ngực/hông và tay có đối trọng |
| F1 | Down A | Hạ trọng tâm nhẹ, gối nhận tải; giữ nguyên thể tích thân |
| F2 | Passing A | Hông đi qua chân trụ; chân kia gập và vượt qua, không cuộn thành một khối chân bất thường |
| F3 | Up A | Chân trụ đẩy, chân vung mở ra chuẩn bị contact đối diện |
| F4 | Contact B | Hai chân đổi vai trò; cùng chiều dài bước và cùng hình thể với F0 |
| F5 | Down B | Nhận tải bằng chân còn lại |
| F6 | Passing B | Vai trò trụ/vung đổi; vẫn cùng camera, ngực/hông và chiều dài chi |
| F7 | Up B | Chuẩn bị trở lại F0; nối cả tay, thân và chân, không chỉ đặt chân gần giống |

Không nội suy tuyến tính đầu gối giữa hai contact: breakdown quyết định gối đi vòng qua đâu, chân nào ở trước và thời điểm nhấc/đặt dép. Tay có thể gần vị trí trung tính ở passing; cần đánh giá quỹ đạo cả vòng, không ép swing lớn ở mọi frame. Head/torso bounce nhỏ do thay pose, không scale thân lên xuống.

## Sau nháp: một thử nghiệm khả năng giữ hình thể

Sau intake nháp, mở **order mới một call built-in, 0 retry**, chỉ cho passing khó nhất. Đính kèm mẫu canonical làm authority ngoại hình/tỷ lệ, target whole-body drawing làm authority pose và strip toàn chu kỳ nháp làm ngữ cảnh. Yêu cầu một minh họa PNG hoàn chỉnh, không dùng strip AI cắt ra làm frame final.

Xem một lần ở size chơi. Nếu model vẫn đổi hình thể/camera hoặc làm chân dị dạng thì dừng phương pháp thử đó; không gọi passing đối diện hoặc inbetween. Tool reference không phải ràng buộc hình học bảo đảm. Nếu giữ được hình thể, mới mở order hữu hạn cho key đối diện và các frame còn thiếu, bám actual selected neighbors. Một frame đạt không tự chứng minh vòng animation đạt.

Nếu thử mới vẫn không giữ được nhân vật, hướng đáp ứng yêu cầu là vẽ/redraw minh họa toàn frame bằng năng lực họa sĩ thực tế. Không tuyên bố đã có năng lực hay output đó; không tự chuyển sang 3D/cutout/API. Skills giúp tổ chức sản xuất, không thay thế năng lực giữ hình thể của công cụ.

## Kích thước, gameplay và tái sử dụng

Authoring nháp/working ở 256², character height mục tiêu khoảng 192–224 px; runtime cell 128² cho khoảng 96–112 px body, rồi hiển thị khoảng 72–84 logical px với canvas 89 và zoom 1.08. Các số này là dự kiến theo family transform, cần scene thực để chốt. Không sinh nguồn 2K để polish: giữ raw 1254 đã có vì custody và giới hạn output thực tế của tool; downsample toàn canvas một lần, không fit từng pose. Pivot tham chiếu [654,1140]/1254 tương ứng [133.51,232.73]/256; không suy ra mọi sandal phải đặt tại pivot trong mọi phase.

D0 là world +X, chiếu xuống/phải màn hình, không phải South. Walk phase hiện tại dựa trên distancePerCycle 1.26, không đồng hồ toàn cục. 600 ms chỉ là cadence của preview; khi đi thật, phase phụ thuộc quãng đường. Chân trụ trong ảnh phải dịch ngược phần dịch root đã chiếu, trong đoạn còn tiếp đất. Giữ bàn chân cố định trong cell sẽ trượt khi root đi. Không thay speed của simulation để che lỗi; chỉ hiệu chỉnh physical stride metadata của toàn action khi có đo hợp lệ.

Tái sử dụng model/pose specification, phase, near/far convention, timing, exporter, atlas, distance clock và preview cho humanoid khác. Mỗi unit vẫn có contour/tỷ lệ/equipment và whole illustration riêng. Cavalry/wagon/ships cần family riêng. D0 chưa qualified nên chưa mở rộng hướng/unit. Wood032 và iron141 giữ acceptance đúng loop D1 đã xem; food pending độc lập.

## Nguồn nghiên cứu và cách áp dụng

- [Toon Boom — Walk Analysis](https://learn.toonboom.com/modules/walk-cycle-animation/topic/walk-analysis1): contact/down/passing/up và quan hệ toàn thân, không chỉ đổi chân. Dùng nguyên tắc, không sao chép hình mẫu thành asset.
- [Toon Boom — Tie Down Animation](https://docs.toonboom.com/help/game-studio-24/game-asset-editor/paperless-animation/create-tie-down-animation.html): sau rough motion, giữ drawing đúng model và không đổi volume, rồi mới thêm chi tiết. Primary text truy xuất bằng search; một số URL phiên bản khác trả 404.
- [Krita — Animation workflow](https://docs.krita.org/en/user_manual/animation.html), [Onion skin](https://docs.krita.org/en/reference_manual/dockers/onion_skin.html): timeline và neighboring drawings giúp kiểm liền mạch trước/sau. Không cần cài phần mềm chỉ để áp dụng cách làm này; không dùng copy/transform pixel của tutorial làm final art trong project.
- [Adobe — Key poses](https://www.adobe.com/uk/creativecloud/animation/discover/animation-key-poses.html): pose-to-pose và breakdown kiểm soát logic/timing trước khi hoàn thiện inbetween.

Research này đóng việc chẩn đoán và sửa kế hoạch, **không** đóng motion gate. Không có loop D0 mới, image call, runtime install hoặc public promotion từ 161.
