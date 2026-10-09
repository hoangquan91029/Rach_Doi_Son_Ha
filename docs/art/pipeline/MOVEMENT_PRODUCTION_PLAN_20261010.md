# Movement production — kế hoạch hiện hành232, nghiên cứu212 / preview213

Ngày 10/10/2026. **D0 vẫn là candidate, chưa đủ điều kiện sản xuất hàng loạt.** Mục tiêu là một người dân có vóc dáng nhất quán, bước tự nhiên và mượt ở kích thước chơi; giữ phong cách minh họa chân thực của canonical.

## 1. Chẩn đoán gắn với asset thực tế

Human bác bỏ hai passing frame155 vì dị dạng. [Research161](movement-research-161/README.md) chỉ ra guide153 đã có thân gầy/cứng và call155 không đính kèm canonical trực tiếp. Guide bị dùng làm authority hình thể trong khi contact chỉ giữ vật liệu. Vai/ngực/hông đổi khối, chân thẳng dài và chân nâng cuộn lại. Đây là lỗi ngay trong whole PNG, không phải renderer bóp méo ảnh. Suy luận từ input/output không bảo đảm biết cơ chế bên trong model.

Có lỗi điều khiển pose riêng:152 được gọi là contact đối diện nhưng actual legpaths giống033;188 cũng lặp bố cục đó. Không dùng tên file/prompt thay quan sát pose. Whole clothed guides189 → guide illustration191 → whole identity correction192 mới tạo được contact khác. Cách này có ích cho một pose khó, chưa đủ chứng minh batch.

Sau đó F3 và F4 khác khối thân/tay so với neighbors.205 sửa F3 whole-body;211 sửa F4 whole-body. Root thấy211 có thân rộng hơn và tay đối trọng rõ hơn192 ở89px. **Không suy motion PASS từ ảnh so sánh.** [Research212](movement-research-212/README.md) nối nguyên tắc animation với nguồn thực tế, không mở thêm image calls.

## 2. Chu kỳ thực tế hiện hành

[Preview213](pure2d-walk-D0-preview-213/actual-output/playback/actual-eight-frame-loop.png) giữ208 và thay ONLY F4 bằng211.208 đã thay ONLY F3 của195 bằng205. Các original/held và preview cũ giữ nguyên byte.

| Phase | Whole source | Vai trò trong vòng thử |
|---|---|---|
| F0 contact A |188 raw |Requested F4 thất bại; được reassign công khai chỉ sang F0 |
| F1 down A |193 F01 |Nhận tải, down còn subtle |
| F2 passing A |185 raw |Passing candidate, không standalone motion approval |
| F3 up A |205 raw |Whole correction phục hồi face/upperbody, giữ closefoot pose |
| F4 contact B |211 raw |Whole correction từ192, giữ opposite-contact layout và sửa torso/arms |
| F5 down B |194 F05 |Inbetween candidate |
| F6 passing B |182 raw |Passing candidate đã hạ footlift |
| F7 up B |194 F07 |Chuẩn bị nối F0 |

Actual whole source1254² được giữ vì custody/output của builtin tool. Working256², runtime128² và preview89² dùng cùng phép scale toàn canvas, sourcepivot654,1140. **Không fit/shift/warp từng frame.** Tám hold75ms =600ms cho preview; playback thật dùng distance clock theo entity, không đồng hồ chung hoặc đổi simulation speed.

## 3. Quy trình sửa để tránh tiếp tục đổi hình thể

**Một canonical → complete rough cycle cùng hình thể → illustrated keys → illustrated inbetweens → một loop → actual travel.**

1. **Một nguồn hình thể.** Canonical D0 `docs/art/characters/villager-neutral-D00-screen-ESE/raw.png` (SHA145b976ffd1bdf563cb5da78806547e6849424054f2c26fc297e155a0b366e94) giữ mặt, nón, vai/ngực/hông, chiều dài áo, camera và ánh sáng. Poseguide giữ contact/near-far/đường chi. Không cho guide generic thay vóc dáng. Không cần vẽ texture tay/chân riêng.
2. **Chốt cả chuyển động nháp trước chi tiết.** Tám hình có trang phục dùng cùng model drawing; contact/down/passing/up và đối trọng tay–thân–chân. Xem rough loop một lần để sửa volume/phase rõ. Guide là authoring reference, không asset runtime hoặc giấy chứng nhận motion.
3. **Minh họa key có điều kiện.** Canonical trực tiếp làm appearance authority; target whole drawing làm pose authority. Nếu tham chiếu whole pose cũ kéo chân trở lại sai, dùng guide-only rồi whole appearance edit như191/192, chỉ khi cần. Không mặc định hai call cho mọi frame. Mỗi order hữu hạn; pose lặp hoặc biến dạng rõ phải HOLD, không cùng prompt retry vô hạn.
4. **Inbetween nối hai nguồn thật.** Attach selected predecessor và next key với vai trò tách bạch, cộng canonical khi cần. Không tự sinh tám ảnh độc lập; không dùng held source làm authority hoặc đổi nhãn để giả đạt. Swing đi theo cung và occlusion; không tuyến tính nối đầu gối giữa hai contact.
5. **Tie-down trước material polish.** Giữ silhouette/volume và identity trước. Biến đổi pose có thể làm áo che chân khác nhau nhưng không làm thân trở thành người khác. Whole-frame edit sửa lỗi thấy rõ; không cutout/limb rotation/source-pixel splice/3D.
6. **Compile và xem sớm.** Tái dùng017 atlas adapter,012 APNG exporter, actual browser preview và một ledger tám nguồn. Một contact sheet +10–15 giây loop ở gameplay size đủ để lập danh sách ngắn các lỗi nhìn thấy. Không xét cloth/pixel li ti hoặc tạo nhiều tốc độ/nền để audit.

Krita mô tả keyframes trước rồi inbetween, dùng onion-skin của frame trước/sau để kiểm quan hệ và xem rough trước khi mở rộng. Áp dụng cách tổ chức này bằng tooling hiện có; không cần cài hoặc rewrite engine. [Nguồn primary](https://docs.krita.org/en/user_manual/animation.html), [onion-skin](https://docs.krita.org/en/reference_manual/dockers/onion_skin.html). Toon Boom nhấn mạnh contact/down/passing/up và rough torso/legs; primary search hỗ trợ nội dung nhưng một số full page403/404, xem retrieval notes212. Không chép sample art vào project.

## 4. Việc gần nhất, theo phụ thuộc

| Gói | Việc cụ thể | Kết quả cần có |
|---|---|---|
|213, không imagecall |Actual atlas/APNG thay ONLY F4, bảo toàn208/211; technical browser8frames/Pause/Play |Root intake và vòng thật hiển thị, không tự gán naturalness |
|Brief loop look |Xem cả người ở89cell/600ms, chỉ lưu lỗi nhảy thân/phase/seam thấy rõ |Nếu lỗi rõ, finite whole-frame correction đúng slot; không blind call tiếp |
|D0 idle family |Dùng whole canonical với một family transform khớp walk; tránh oldidle38→walk89 pop |Candidate scale/anchor, không fit từng frame |
|D0 runtime trial |Reuse atlas/state/direction API và distance phase; actual UI D0 travel → Pause/Resume → Stop/idle/menu |Cùng người, transition hợp lý và practical foot contact; actual sim direction |
|Villager expansion |Sau pilot đủ tốt: hoàn thành direction references/walk/actions theo finite matrix |Không fanout từ riêng211contact hoặc checksum |

Pending human question cũ scoped195; không tự suy reply ấy chấp nhận213 và không hỏi lại liên tục. Owner032wood và141iron chỉ áp dụng đúng các D1 loop đã xem. Food101 pending riêng. Loadedgoods luôn ordinarywalk.

### Thực thi216/219/225

216 export nguyên wholecanonical qua uniform128/89, zeroimagecalls. Sharedpivot giúp anchor nhưng idlebody hẹp hơnwalk/bakedshadow khác, chưatransitionapproval.219 runtimecandidate có29asset vàdistancePerCycle1.26 nhưng boot bịrejecthai rootabsolutepaths; zeroactualtravel.225 là NEWfiniteorder sửaONLYhai relativepaths trong isolatedcopy, validateactual loader vàONEofflineDeltaUI trial. OnlinePause intentionallycontinuesfield nên dùngoffline đểkiểmfreeze, khôngđổi hànhvi pause. Đọc receipt225actual trướcnextorder; failedguards phải lưu state/toast/screens/cleanup, không blindrepeat hoặc fakefacing.

## 5. Foot contact và runtime: hai gate khác nhau

Stationary loop phát hiện shape/seam, không chứng minh chân bám đất khi nhân vật tiến. D0 là world+X chiếu xuống/phải màn hình. Runtime root tiến trong khi chân trụ trong hình phải lùi tương ứng; chân cố định trong cell sẽ trượt ngoài world. Existing distancePerCycle1.26 là metadata provisional, không phải số đã được hình ảnh chứng minh.

Sau trial thật, nếu thấy trượt rõ thì dùng một vài contact/position samples để hiệu chỉnh stride metadata của **cả action**, giữ simulation speed/collision/pathing. Không đòi zero pixel sliding từ tám static frames; không biến bài test hình học thành motion acceptance. [Contract hiện có](movement-research-161/runtime-motion-contract.md) giữ công thức và source mapping.

## 6. Tái sử dụng và giới hạn thực tế

Tái sử dụng model specification, phase/ownership conventions, timing/stride metadata, exporter/manifest, preview, atlas banking và runtime controller. Whole illustration của mỗi unit vẫn riêng; spear/firearm/commander/horses/wagons/ships có silhouette và motion family tương ứng. Không reuse chân hoặc tay PNG.

Khả năng giữ anatomy/volume qua nhiều image calls chưa được bảo đảm. Skill/tool reference chỉ giúp tổ chức và hướng dẫn, không ràng buộc hình học tuyệt đối. Nếu một finite method vẫn trả pose lặp/dị dạng, ghi HOLD và thay cách điều khiển whole drawing; không hứa sản xuất hàng nghìn frame bằng workflow chưa qualified. Đo throughput từ action hoàn chỉnh được chấp nhận, không từ số calls/files.

Full project **INCOMPLETE**. Public230 optionalfort28 hiện hành, chưa chứa D0;207 là lịch sử. Previous active plan byte-preserved tại `docs/checkpoints/checkpoint209-entrypoints/`; mọi source/rejection/custody tiếp tục bảo toàn. Builtin imagegen/Sol6.1Low/pure2D, không API/key/quota/3D/cutouts.

##7. Runtime232 — actualscope và nexttransition

228 actualD0all8/64samples/Pausefreeze500ms/Resume đãđạt kỹ thuật trênfrozen225build. Engineordinaryarrival.7, không dùngQA.3 đểgọi navigationfail. Stop vềidleD7 sauendpointturn; matchingD0/menu chưađạt. Original219/225/226/228 failures/captures/clip retained; no furtherblindcampaignchain. Nextspecifictransition trial mustStopwhileactualD0segment remains, ordinaryUI only, no fakefacing/speed/phase/scale changes. Matchingidlebody/bakedshadow vàmixedlegacyfamily scale vẫnopen; no motion/owner/worldfootlock/fanout approval fromtests. Clip thật đãhiển thị. Public230chỉpromote acceptedWallGate/constructioncode, KHÔNGD0/foodCHAR;207historical.
