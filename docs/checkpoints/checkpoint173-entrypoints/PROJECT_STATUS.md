# Trạng thái dự án — checkpoint173, ngày 2026-10-10

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
| Lỗi và thiếu sót đã xác nhận | Passenger starvation và splash đã có fix local; GP3 đã sửa local163; policy/ability contracts còn mở |
| Đồ họa unit | Camp manifest có 26 asset entry và 47 frame rectangle; chỉ villager D1 có loop walk/wood/iron. Phần lớn 11 loại unit và 12 leader còn thiếu action hoặc direction |
| Building và map | Public có idle cho6/10; local165 có7/10, còn thiếu3 idle và các trạng thái construction/hit/death. Hai map chơi được nhưng chưa đạt composition cuối cùng |
| Scale | Canvas render 89 px không có nghĩa body cao 89 px. Unit cũ và mới khác scale; cần thống nhất trong scene thực có cả hai |
| Public release | Còn mở: đồ họa mặc định, asset bank theo match, cache/version, hiệu năng bản hiện tại khi đông quân, thiết bị/mạng ngoài và nghiệm thu cuối cùng |

Ba audit con tách riêng tình trạng triển khai, bằng chứng test, chấp nhận visual và public release. Audit154 là snapshot chỉ tài liệu; các gói156–161 bên trên ghi thay đổi sau audit. Rejection/research không đóng visual gate; local tests không chứng minh bản public đã nhận fix.

## Điều phối

Dùng frame toàn thân pure 2D, imagegen tích hợp và đúng `gpt-6.1-sol`/`low` cho worker code/art. Được phép làm song song. Không theo dõi quota, không dùng API key, 3D hoặc texture chân tay rời. Đồ mang về dùng walk thường. Tất cả source, bản held/rejected và receipt vẫn được giữ nguyên.

Lịch sử trước audit được giữ nguyên byte: [history inventory](docs/audit/2026-10-09/history/inventory.json). Tài liệu lịch sử không phải lệnh để tiếp tục task cũ. Chỉ ghi COMPLETE khi mọi tiêu chí quan trọng đã được đóng trên bản release cuối cùng.

## Cập nhật162–168

- [162](docs/art/pipeline/villager-walk-D0-rough-cycle-162/root-intake.json): tám original whole-clothed rough drawings, fixed family transform và authoring loop;0 image call. Chưa phải minh họa final/motion acceptance.
- [166](docs/art/pipeline/villager-walk-D0-capability-166/root-intake.json):1 built-in call,0retry. Body/identity gần canonical hơn nhưng support/passing phase chưa được xác lập; **HELD**, không selectedF02, không F6/inbetween/runtime/fanout. [Follow-up](docs/art/pipeline/movement-research-161/FOLLOWUP_162_166.md) ghi hướng tiếp theo.
- [163](docs/qa/logistics-ui-163/root-intake.json): lưu actual total duration sau modifiers; HUD progress đúng, persistent own-army low-ration warning bao gồm embarked.22 focused tests và ordinary Chromium training/pause/resupply UI PASS. Không đổi food/speed/balance.
- [164/165](docs/qa/shipyard-idle-165/root-intake.json):1 whole illustrated Shipyard idle; optionalLOCAL `?art=shipyard`27assets. Actual Coast xây→idle/chọn→transport queue/spawn→Pause/Resume/Stop/menu;18 focused contracts. Construction/hit/death vẫn fallback, không completed building animation.
- [167](docs/qa/merged-candidate-167/README.md): merged source/build binding;27 focused contracts và ordinary Chromium/Firefox Coast flow. Không full-match/public promotion claim.
- Incident167: candidate build vô tình ghi vào active dist. [Restoration](docs/qa/merged-candidate-167/public149-restoration.json) đã khôi phục đúng179 file public149, giữ accident output riêng. [168](docs/qa/public149-restoration-168/receipt.json) kiểm normalTLS fresh Chrome/Firefox, exact old149 chunk,26art/12portraits/0errors. Service157023 không restart. Public không nhận local163/165 hoặc pending food.

Code/art/QA mới là candidate local; public149 và full goal vẫn INCOMPLETE. Không dùng bảng snapshot154 để mở lại155/158 hoặc báo các finding đã sửa là chưa sửa.

## Cập nhật169–173

- [169](docs/art/pipeline/villager-walk-D0-reconcile-169/root-intake.json) sửa hai whole rough passing drawings,0call; ankle từng trailing so với own depthlane, không chỉ screenx giữa hai chân. [172](docs/art/pipeline/villager-walk-D0-capability-172/root-intake.json)1call/0retry cải thiện forwardfoot nhưng phaseHELD. [173](docs/art/pipeline/movement-pose-research-173/README.md) nghiên cứu authority mới; photo sequence chưa được visually intake, không activeguide. Không finalD0loop/runtime/fanout.
- [170](docs/qa/art-catalog-170/root-intake.json):9sharedlegacyrecipes/28deduplicatedexactdefinitions, deterministicselectedmanifest compiler, portrait/shadow dependencies, pendingrelease refusal và missingfamilies. Standalone loader-format output giữ relativepaths nên serve cùng asset layout.33focused tests +18Nodefollowup; actualstaged Chrome/Firefox Coast build/select/menu27art12portrait0errors. Dynamicmatch loading/defaultrelease vẫn mở.
- [171](docs/qa/performance-baseline-171/root-intake.json):bothmaps1/5/8world normalAI, realstep +exactcompactview/JSON;39naturalunits/world. Delta stepcohortp95≈11.8/54.6/87.0ms; Coast≈6.5/32.0/53.0ms. AIphase đồng bộ và CPU không độc quyền; online không cóAI. Không productionheadroom/dense200/network/browser PASS, chưa optimization. Cần profile các tick đắt rồi đo đúng workload.
- Public149 vẫn nguyên179files/oldchunk/service; tất cả worker, imagecalls và testhandles terminal. Full goal vẫn INCOMPLETE.
