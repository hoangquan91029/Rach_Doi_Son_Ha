# Kế hoạch đồ họa — movement213, 10/10/2026

Kế hoạch toàn game: [PROJECT_PLAN.md](../../PROJECT_PLAN.md). Phạm vi và bằng chứng chi tiết: [art-animation-audit.md](../../audit/2026-10-09/art-animation-audit.md). Bản kế hoạch trước audit được giữ [nguyên byte](../../audit/2026-10-09/history/docs/art/pipeline/GRAPHICS_PRODUCTION_PLAN.md).

**Movement hiện hành:** [plan213](MOVEMENT_PRODUCTION_PLAN_20261010.md), [research212](movement-research-212/README.md), [actual213loop](pure2d-walk-D0-preview-213/actual-output/playback/actual-eight-frame-loop.png).213 giữ208 chỉ sửaF4=211wholebody/arms; technicalplaybackPASS, motion/owner/worldfootlock/runtime/fanoutOPEN. Các mục181/195 phía dưới là lịch sử nguồn, không currentNEXT. Public207fort28/185files thay149; fullgoal INCOMPLETE. Local210 wall/gateadjacencyfixed, renderer/topologyartunfinished. No moreblindcalls; briefwholeloop→samefamilyidle→actualD0travel, thenqualifiedfanout. Previousplanbytearchive209.

## Integration224

Local215/222/223 đã sửa projectedWallGate fallbacktopology và vùng chọn, actualfivebuild/X/Y/corner/Gatetravel/PauseStopmenu acceptednarrow.214 wholeWallX ONEbuiltin candidate vẫn HOLDspan/worldalignment, khôngcài; finishedbuildingart còn thiếu.217 visibleconstructionboolean giữprivatejob/fogfilter, actual221 flag/redaction/completion verified nhưng overallscoutreturnHOLD; khôngclaim authoredcompletionscreenshot. Public207khôngđổi.

216 wholecanonicalD0idle uniform128/89/pivot cùng213 prepared; bodyvolume/bakedshadow/Stoptransition cònopen.219 sealedHOLDboot hai pathrootabsolute;225 NEWfinite isolatedcopy sửaONLYruntimepathrelative trướcONEofflineD0travel/PauseResumeStop. Xem actual225receipt để chọnnextorder, khôngfanout hoặc suy motionapproval từtechnicaltests. Khôngcallảnhthêmtrongmovementtrial.

## Mục tiêu hình ảnh

Minh họa lịch sử chân thực/bán chân thực, có khối và chiều sâu, chuyển động tự nhiên ở kích thước chơi RTS. Giữ mũ, trang phục, màu áo, dải thắt lưng (sash) và vật liệu theo mẫu nhân vật chuẩn (canonical). Không dùng nhân vật hình khối, 3D, cutout hay texture tay/chân riêng làm thành phẩm.

Thứ tự đánh giá: chuyển động đúng và liền mạch → silhouette/readability → identity nhất quán → chi tiết bề mặt. Xem một vòng chuyển động ngắn ở kích thước chơi thật; chỉ sửa lỗi thấy rõ. Việc audit kỹ kế hoạch không thay đổi ưu tiên kiểm tra hình ảnh ngắn gọn này.

## Hiện tại có gì

| Hạng mục | Đã có | Còn thiếu |
|---|---|---|
| Villager D1 | Idle, walk 014, wood 026/owner 032, iron 136/owner 141; food 101 local | Build/repair, attack/hit/death và độ phủ hướng; food còn chờ phản hồi riêng |
| Villager D0 | Whole eight-frame candidate213, corrected F3/F4;155 rejected originals retained | Brief continuous intake, same-family idle and actualtravel/Stop; no batch qualification |
| Quân đội | Một số identity idle D0 | Phần lớn hành động và hướng nhìn cho infantry, spear, firearm, cavalry, artillery, wagon và hai tàu |
| Leaders | 12 portrait và nguồn identity gốc | Hoạt ảnh toàn thân, hành động theo vai trò và 8 hướng; chỉ một general có idle candidate |
| Buildings | Public207 includes8/10 completed-idle families; local210 wall/gate placementfix | Wall/Gate finishedart/topology; all construction/damage/destruction and applicable attackstates |
| World | Ground/water/ford/shore candidates, forest, hill/mountain, food/iron nodes | Composition hai map, bờ/edge/repetition và scene đông quân |
| Framework | Export017/APNG012, distance phase, alpha picking,170catalog/compiler,175matchbanks and bounded browser receipts | Accepted fullcoverage/default release and final visual/performance validation |

Public207 `?art=fort` có28 asset entries; đây không phải28animation hoặc roster hoàn chỉnh. URL trần vẫn fallback. Public149 scope chỉ là lịch sử, không bản đang chạy.

## Quy trình chuẩn cho một action

1. **Chốt identity và runtime mapping.** Ghi `identity/action/engineDirection`, nguồn canonical, camera/light, equipment, cycle/terminal state và simulation event liên quan. Không tạo run/carry/deploy nếu gameplay không cần.
2. **Chốt cả chu kỳ.** Dùng clothed 2D guides có near/far ownership, contact/passing phases, fixed pivot và timing. Walk 8 frame: F0/F2/F4/F6 trước, rồi inbetweens. Không dựa vào bốn prompt rời rạc.
3. **Sinh whole illustrated keys.** Builtin imagegen, exact Sol 6.1 Low worker. Canonical duy nhất giữ authority về hình thể/camera/identity; whole-body guide điều khiển pose, strip cả chu kỳ cho temporal context. Không để generic guide thay tỷ lệ canonical. Giữ raw và tool receipt. Key sai rõ ràng thì dừng slot, không đổi nhãn để che lỗi.
4. **Hoàn thiện inbetweens.** Sau khi keys được chọn, mỗi frame bám hai key lân cận; số call hữu hạn. Không ghép nguồn pixel, xoay limb texture hoặc fit từng frame.
5. **Compile và xem loop.** Một transform cho toàn family, alpha/cell/pivot/duration validation, atlas/manifest/contact sheet/loop tự sinh. Xem 10–15 giây tại kích thước chơi; sửa những lỗi nhìn thấy.
6. **Trial thật và đưa vào catalog.** Đi/đứng/đổi hướng hoặc work/stop/pause trong game, đúng hướng do mô phỏng xác định. Ghi technical/visual/owner/public riêng. Chỉ mở đợt sản xuất tiếp sau khi pilot tương ứng đạt yêu cầu.

Gộp công việc theo từng hành động, không tạo một dự án quản trị cho từng frame. Mỗi package có một ledger, một preview và một receipt gọn. Bản lỗi và original vẫn được giữ; build/rollback đầy đủ ở ranh giới release.

## Tái sử dụng và sản xuất hàng loạt

Tái sử dụng pose specification, guides, timing, camera, export, atlas schema, preview, asset banking và runtime API. Thành phẩm của mỗi nhân vật vẫn phải là một minh họa toàn thân riêng. Humanoid generic, spear, firearm, commander, cavalry, artillery crew, wagon và ship là các motion family khác nhau.

- Bước 1: hoàn thiện D0 walk để chứng minh quy trình dùng guide có trang phục qua cả chu kỳ.
- Bước 2: thống nhất visible scale của idle/walk/work trong một scene thật, rồi hoàn thành villager tám hướng và action cần thiết.
- Bước 3: một infantry pilot trọn trạng thái; sau đó spear/firearm. Song song làm world/building, không mở cả roster ảnh.
- Bước 4: từng complex family (horse/rider, wagon/animal, crew/gun, ships) có pilot riêng trước batch.
- Bước 5: một premium leader pilot; chốt 12 identity dùng shared role family hay role-specific artwork trước khi ước tính/call hàng loạt.
- Bước 6: accepted release manifest + match banks + final map composition + performance và public validation.

Worker có thể chạy song song các package độc lập, tối đa 3 worker + root. Frame phụ thuộc phải đợi key đã được tạo và chọn thực tế. Không lật ảnh tự động: villager sash, tay cầm vũ khí, leaders và ánh sáng bất đối xứng cần hướng thật. Nếu một generic family đối xứng đủ để mirror, phải ghi mapping được duyệt và thêm hỗ trợ renderer trước; hiện vẫn dự trù đủ 8 hướng.

## Kích thước và bộ nhớ

Mục tiêu visible humanoid 64–96 logical px tại default zoom, không phải canvas cao 89 px. Scene hiện tại có idle cũ render 38/42/51 và action mới 89; đây là chênh lệch cần sửa bằng thang kích thước nhất quán cho từng nhóm nhân vật. Đo opaque height đủ để giải quyết khác biệt nhìn thấy, không audit từng pixel.

Raw hiện tại 1254² được giữ nguyên. Bản working/export đề xuất 256², khoảng 224 px body; runtime 128², khoảng 112 px body trước scale xuống màn hình. Đây là baseline dự kiến cho output chuẩn hóa, không tuyên bố raw đã sinh 256 px. Dùng transform chung và pivot chuyển đổi đúng; horse/spear/ship có canvas riêng nếu cần. Không regenerate asset tốt chỉ để đổi độ phân giải.

128² RGBA = 64 KiB/frame; 64 frame = 4 MiB trước padding/copies. Inventory tham khảo 5.600–6.024 frame có thể chiếm 350–376,5 MiB nếu nạp toàn bộ 128 cells, chưa gồm world/portrait/caches. Vì vậy cần selected-map/roster banks, giải phóng bank khi rời trận, dedup theo content hash. Guard 128 MiB hiện có chưa tính toàn bộ bộ nhớ trình duyệt.

Không hứa ngày hoàn tất trước khi đo số frame được chấp nhận trên mỗi call và thời gian làm việc thực để hoàn thành ít nhất hai chu kỳ. Số lượng trong audit là giả định để lập kế hoạch; không phải lệnh tự động sinh hàng nghìn ảnh. Không ép tất cả hành động dùng 8 frame: hit/death/attack/idle theo thời lượng và độ mượt cần thiết.

## Gate tiếp theo cụ thể

G01 hiện theo [kế hoạch movement20261010](MOVEMENT_PRODUCTION_PLAN_20261010.md) và [preview195](pure2d-walk-D0-preview-195/root-intake.json). Có tám whole illustrated PNG và technical playback, chưa continuous naturalness/runtime acceptance. Một brief actual-size loop look đã được yêu cầu; F3/F4 body warning giữ nguyên. Sửa visible issue nếu cần, rồi candidate D0 travel/Pause/Stop và canonical idle cùng family scale. Không mở directions/units hoặc dùng historical162/173/181 order như current instructions. Original guides chỉ authoring, các failed/held/source labels giữ nguyên trong custody.
Đưa asset mới vào default release sau coverage và actual-scene acceptance; không bật toàn bộ candidate rồi gọi finished. Full project vẫn **INCOMPLETE**.

## Follow-up162–168

[162 rough](villager-walk-D0-rough-cycle-162/root-intake.json) đã hoàn thành reference trọn vòng; không final art. [166 illustration](villager-walk-D0-capability-166/root-intake.json) cải thiện khối người nhưng HELD support phase;1call/0retry/exhausted. [Hướng tiếp](movement-research-161/FOLLOWUP_162_166.md) là reconcile ownership/occlusion,0call, không mở F6/inbetween.165 Shipyard idle accepted narrow actual Coast scene, local27assets; public149 vẫn26. Code163/merged167 không cấp motion acceptance.

169/172/173 bổ sung: trailingankle trong originalrough đã sửa; newillustration giữbody nhưng phaseHELD, không finalsource selected. [173](movement-pose-research-173/README.md) chuyển đề xuất sang verifiedwholeaction/tonalwholepose authority; photo metadata chưa phải visuallyqualifiedreference.170 catalog/compiler đã triển khai và validatednarrowUI, dynamicmatchbanks/defaultrelease còn mở. Không dùng các tool đó để mởfanout khi movement chưađạt.

## Movement sau180/181 — lịch sử thực thi

Root đã bỏ155 deformedframes và chưa chọn166/172/181 làm finalwalk key.174/178 không lấy được photographicsequence; không dùng mô tả catalog làm bằng chứng chuyển động. Nguồn nguyên lý: [Toon Boom Walk Analysis](https://learn.toonboom.com/modules/walk-cycle-animation/topic/walk-analysis1), dùng contact/down/passing/up và quan hệ toàn thân, không chỉ hướng bàn chân. Directpage403; primary searchtext retrieved, không photo observation claim.

Sửa quan trọng ở180: tại passing, đùi có thể tiến trong khi chân dưới gập về sau; không ép sandal phải vượt idlex. Guide169/179 từng thiên về đặt ankle và rút ngắn chân, dễ dẫn tới chân gần duỗi chuẩn bị contact hoặc sai khối.180 vẽ lại wholepants/body contours, không limbtexture hay recolor-only.

181 thử1builtincall/0retry với solecanonical +180wholeF6 guide. [Actual89 comparison](villager-walk-D0-capability-181/comparison89.png) giữ broadrealisticidentity và tạo chân gập rõ; liftedfoot còn cao/back nên vẫn candidate. Tiếp theo là **ONE correction toàn thân có mục tiêu hạ biên độ bước**, dùng actual181 như edit target và canonical như appearance authority, giữ support/hip/knee/arm progression. Không mở một dự án guide mới hoặc auditmicrofoot; thay control cụ thể cho visibledefect, không prompt nguyên trạng.

Sau correction có pose đúng rõ: hoàn thiện bốnkey cùng một identity/camera/family scale → bốninbetween dựa neighbor thực → export/600ms preview → một brief real-size look → actualD0travel/Stop/pause. Nếu loop còn lỗi nhìn thấy thì sửa đúng lỗi đó. Technicalhash/still không cấp naturalness; chỉ mở directions/units khi pilot hoàn chỉnh đạt. Không bắt buộc giữ contacts033/152 nếu chúng lệch hình thể mới.

175 đã cài actualmenu/match encoded/decoded ownership, budget/cache/release/retry; không accepteddefaultrelease.177 giảm repeatedcell checks trong path mà không đổi motion/path contracts. Hai gói không thay sourceanimation hoặc đóng movement gate. Fullgoal INCOMPLETE.

## Movement182–190 — lịch sử thực thi

[Nghiên cứu actual paths](movement-research-161/CONTACT_OWNERSHIP_188.md) xác định nguồn lỗi concrete:152 labelledopposite nhưng exposedhip→knee→sandal vẫn cùngphase033.188 sửa camera/thân rồi lặpđúng nguồnpose sai. Giữ requestedF4HOLD; **reassign actual188 wholePNG chỉ F0candidate** thay old033, không sửa pixel/giả phase.182/185 chỉ currentpassing candidates, chưa qualifiedloop.

189 đúnghai completeclothed tonal drawings/0calls, cố định legA outerhip/foreground và legB innerhip/background. F4 Aback/Bfront ngược actual188. Tones/labels chỉ guide; finishedillustration giữ canonicalrealisticidentity/proportions, không angularvector/shortleg surfaces.190 NEW ONEbuiltin/0retry đang chạy với guideFIRST pose-only, canonical appearanceauthority và188F0bodycontinuity; bỏ anatomicalleft/right ambiguity và152control. Inspect live call trước tiếp tục, không duplicate/retryblind.

Sau actualoppositecontactintake mới mở fourwholeillustratedinbetweens theo actualneighbors, existingatlas/APNG600ms và onebriefcontinuouslook ở game size; actualD0travel/Pause/Stop sau integration. Không thêm direction/unit khi chưa pilot. Source/guide hoặc stillhash không cấp support/footlock/motionapproval. Family scaleG02 vẫn open.

## Movement hiện hành: complete-source pilot195

F0=188 explicitreassignment; F2=185; F4=192 whole correction giữ actual opposite legpaths; F6=182. F1/F5/F7 là actual193/194. F3=197 sau sole whole guide196, provisional với appearance/phase warning; original193F3 wrongcanvas/bodyjump loại. [Ledger](villager-walk-D0-contact-192/pilot-sequence-195.json) bind tất cả raw/tool receipts,1254wholecanvas/pivot và uniform128cell, không fit/mirror/pixelsplice.195 exporter tái dùng017/014, atlas1024×128 và APNG89cell/600ms. Actual Chromium támframes/ba vòng/zeroerrors là technical playback only.

Root đã hiển thị actual APNG và hỏi một lần về chuyển động; chưa trả lời, chưa motion PASS. F3/F4 body khác neighbors cần continuous judgment; không xử lý bằng repeated still scoring hoặc đổi playback/game speed. Khi đủ tốt, D0 candidate runtime và same-family idle + ordinary UI movement/Pause/Stop kiểm tra practical contact/transition. Stationary preview không chứng minh world footlock. No fanout/defaultrelease/publicpromotion trong gói này.

Current runtime update225/226:225 actualloader29PASS, livingownD0travel observed but town detour/D1 and partial samples causedHOLD; PauseResumeStop/menu unperformed. This is not proof of skipped renderer frames or bad motion.226 NEWsamefrozen225build uses an actualclear outside-towncorridor and25ms observations, ONEofflineUI/160s/no retry. Inspect actual226receipt; no approval/installation/fanout or perframefit/scale/speedchanges.227 release preparation-only for accepted215/217/222/210 code; public207 still unchanged.
