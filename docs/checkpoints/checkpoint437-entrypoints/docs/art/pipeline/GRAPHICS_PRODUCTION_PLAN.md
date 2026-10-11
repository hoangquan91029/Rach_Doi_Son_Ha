# Kế hoạch đồ họa hiện hành — checkpoint419 / public417

[Full project plan](../../PROJECT_PLAN.md) · [Status](../../../PROJECT_STATUS.md) · [Next](../../../NEXT_STEPS.md) · [Movement pilot](MOVEMENT_PRODUCTION_PLAN_20261010.md). Bản407 và mọi nội dung376 cũ giữ nguyên tại `docs/checkpoints/checkpoint419-entrypoints/`. Không dùng các next-step lịch sử làm order hiện hành.

## Thứ tự theo yêu cầu mới nhất

1. **Xe lương có ngựa kéo.** Whole2D415 đã tạo đúng một lần, giữ bản398 cũ. Tiếp theo finite420 thay activewagon idle bằng toàn bộ ensemble ngựa+xe; original398 PNG vẫn ở custody. Một actualscene chọn/loadfood/move/pause/resume/stop/menu trước install/publication. Không tách ngựa thành entity riêng hoặc xoay texture chân để giả chuyển động. Game vẫn có cùng wagon HP, cargo, logistics, tốc độ, collision và simulation; phần minh họa thay đổi.
2. **Scale nhất quán.** Chốt scene mixedunits/buildings trước thêm animation. Cùng một family có một kích thước render cho idle/walk/work, một sourcecanvas/pivot đã khai báo, không fit từng frame. Giữ tỷ lệ thế giới giữa người, ngựa, nhà và cây; camera góc54×27 không đổi. Thông số dưới đây là proposal cần thử, không phải runtime hiện hành.
3. **Animation unit còn thiếu.** Sau scale chốt, một action/direction pilot hoàn chỉnh trước fanout: whole clothed rough cycle cùng vóc dáng → illustratedkeys → wholeillustratedinbetweens → atlas/manifest → một briefloop và actualtravel/action/stop. Ưu tiên infantry/spearman/firearm đi bộ; horse+cart gait/rollingwheels và cavalry có cycle riêng. Attack/hit/death rồi hướng còn thiếu theo archetype. Frame hoàn chỉnh 2D, không cần3D/Blender/parttextures/cutout. Không cho tests/stills thay motion judgement, không đổi tốc độ game để che lỗi.
4. **Coverage còn lại.** Naval transport/warship và10leader identities cần wholeRTS art; buildingconstruction/hit/death/attack, mapshore/forest/mountain và densecombat/performance vẫn mở. Làm song song khi có ownership độc lập và không xung đột liveguards. Không tiếp tục thư viện wallvariants.

## Scale: số đo và phương án thử

Ở defaultzoom hiện tại1.08, visible alpha của firstframe cho villagerD0 khoảng37.5px, D1idle/wood87.1px và D1walk/iron89.4px. Infantry41.2px, THD44px, TNN41.8px, spearman40.8px, cavalry52.6px. Đây là phép đo trình bày từ runtime thật để chọn scale; không phải anatomy/footlock approval.

Proposal đầu tiên: tất cả assetvillagerD0/D1 idle/walk/wood/iron dùng **một logicalrender42**, đồng thời thử uniform defaultworldzoom **1.68** để humanoid visible khoảng64–70px, cavalry khoảng80px. Tỷ lệ building/terrain cũng phóng đồng nhất theo camera; không phóng người một mình khiến nhà quá nhỏ. Người chơi vẫn zoomout/pan/minimap được. Firearm/spearman/infantry/leaders cùng logical42; cavalry giữ51. Horsewagon415 render112 chỉ là candidate cần cân đối trong scene, không tuyên bố đã chốt.

Thử trong isolated candidate: mixedinitialscene ở defaultzoom, visiblefoot/anchor/selection, một actualD1walk→idle và woodwork episode, pause/resume/stop. Chỉ sửa pop/jump hoặc occlusion/readability thấy rõ; không nhiều nền, nhiều tốc độ hoặc pixel/cloth audits. Nếu proposal không phù hợp thì sửa một bộ family/world numbers từ scene, không perframe fitting. Source/pivot/atlas bytes và simulation giữ nguyên. Mọi thay đổi asset.render áp toàn family/action; clock locomotion vẫn dựa distance của entity.

Raw builtin1254 được giữ nguyên vì custody; working256 và runtime128, characterheight gần192–256 ở working. Originalleadership1024×1536 có camera/background tham chiếu, không thả thẳng vào world. Unit sources không sinh ở512–2048 để đánh bóng ởzoom lớn. Final unit nhìn ởgameplay64–96px; atlas uniform128cells/noautofit. Shadow/picking dùng cùng transform thật; neverclaimworldfootlock từ loopstationary.

## Public và sources đang có

Public417 defaultfort/worldtrue50assets/206files giữ mọi illustration cũ và thêm gun408/cannon409 D0static. Walls **STONE X362/Y364/corner365**, gates **WOOD245/252**. Stoneconstruction373 static riêng; allanimatedbuildingstates còn thiếu. Không còn yêu cầu xóa cổng gỗ: chỉ woodenwall graphics bị loại khỏi activebank; nguồn/history/rollback vẫn giữ.

408409 ONEbuiltin0retry mỗi nguồn, working256/runtime128.412 rootbuild literalstagecwd/unchangedJS352a,50schema/twoidentitycontracts.412 actualfirearm controls,414 actualcannon F2clearance→singlepick→Move/PauseResume/arrival/Stop/menu PASS.410wrongcwd/412occludedpick/413global-lastdraw guardfailure giữ nguyên. Globalrendererlastdraw không nhận dạng peractor khi nhiều unit được vẽ.418 Firefox normalHTTPS50ready12portraits/57pins/new2PNGs/ordinaryfirearmqueue/spawn/select/controls/menu0/errors0. Chấp nhận hẹp staticcoverage, không phải finishedanimation/fullroster.

415 horsewagon source/descriptor/raw/112preview ở `../units/supply-wagon-horse-415/`, ONEwholeedit0retry, rootselectedforactualsceneONLY. Chưa installed/public, không có horsewalkframes.398 originalcart giữ nguyên. Currentpairedrollback public405+backend230/private411; actualpublic417 immutablebackend230PID3229 không restart. All408–418call/testguards CLOSED trước entrypoint419.

Movement213 tám wholeframes/216idle/233actualD0technicaltravel vẫn giữ và chưa ownernaturalness/runtime/fanoutapproved. Wood032/iron141 chỉ duyệt vòng D1 đã xem, food101 riêng. Loadedgoods luôn ordinarywalk, không tạo carrycycle riêng.

## Framework sản xuất dùng lại

Sharedunit-art registry chọn identity thật; raster selection dùng state/direction simulation, exact authored art trước STATIC_ILLUSTRATION sameidentity khi livingstate thiếu. Đây là interimcoverage, không animation. Death/construction không mượn livingidle. Atlas/manifest256→128 với source/runtime SHA và declaredlanczos, fixedpivot/wholecanvas. Sprite timing, distancewalk phase, actionepisode và pause có thể dùng lại; damage/resource/victory server-authoritative.

Mỗi finiteorder có canonical/referencepins, camera/layout, action/direction, selectedneighbors, callcap và sourceledger. Keys0/2/4/6 cho 8framewalk, rồi1/3/5/7 theo neighbors. Preserveallraw/held/rejected. Không trả lời bằng poseguide/rig thay artwork. Một continuousgame-size loop và actualengineaction/travel đủ để sửa visibleproblem; không fanout khi một pilot đang bị hold rõ ràng.

Mọiworker exactSol6.1Low. Builtin imagegen, không API/key/CLI/quota/Luna. Rootsource/baseline guard đóng trước canonical/HEAD mutation. Literalisolatedcwd/absoluteoutDir/exactconfig, separatelyinspectpreflight→ONEbuild→seal→ordinaryUI. Publication riêng exactsource/build/actualscene/currentpairedrollback/rooms0/ROOT755nextclone. Never altersealedsource duringtrial, restartproduction duringtests, injectcommands/state/facing/outcome, weaken guards hoặc đổi balance/speed. Không replay completedfullmatches chỉ vì client-onlyart thay đổi.

**Full goal INCOMPLETE:** fullroster/eightdirections/actions/12leaders/family scale/buildingstates/maps/defaultacceptedart/densecombat+roomsperf/externaldesktopWAN/finalpublicbothmapsbothmodes. Nativeautomation311missinghumanchoicepending, không ACTIVE5hclaim; fullgoal tiếp tục.
