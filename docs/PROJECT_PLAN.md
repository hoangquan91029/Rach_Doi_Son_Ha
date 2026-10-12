# Kế hoạch sản xuất animation — workflow481

Mục tiêu toàn game **CHƯA HOÀN THÀNH**. Mỗi unit chỉ được tính hoàn chỉnh khi giữ đúng artwork gốc, đủ action áp dụng × tám hướng và chạy đúng trong game. Đây là kế hoạch hiện hành, thay các hàng đợi cũ lưu nguyên bản trong `checkpoints/checkpoint476-entrypoints/`. Receipt lịch sử chỉ có hiệu lực cho đúng nguồn và cảnh đã thử.

## Phạm vi đủ bộ

Registry có9 loại unit thường và12 identity lãnh đạo. Cùng nhân vật dùng chung artwork giữa King/General; build chỉ áp dụng khi làm King. Tất cả action trong bảng cần D0–D7, không mirror.

| Nhóm | Action bắt buộc | Frame/hướng |
|---|---|---|
| Villager | idle, walk, attack, hit, death, gather_wood, gather_food, gather_iron, build | 4,8,8,4,8,8,8,8,8 |
| Infantry, spearman, firearm, cavalry | idle, walk, attack, hit, death | 4,8,8,4,8 |
| Artillery | idle, walk, attack, hit, death/destroyed | 4,8,8,4,8 |
| Wagon có ngựa | idle, walk, load, unload, hit, death/destroyed | 4,8,8,8,4,8 |
| Warship | idle, walk/move, attack, hit, death/sink | 4,8,8,4,8 |
| Transport | idle, walk/move, load, unload, hit, death/sink | 4,8,8,8,4,8 |
|12 leader identities | idle, walk, attack, hit, death, ability; build khi King | 4,8,8,4,8,6,8 |

Build/repair dùng chung clip khi thao tác giống nhau. Dân làng mang tài nguyên về dùng walk. Ngắm/bắn/nạp, recoil/hồi phục là các pha trong attack. Ability/load/unload cần pose riêng. Không thêm hành động gameplay chưa tồn tại. Idle1ảnh và fallbackD0 vẫn là thiếu animation.

`shared/unit-action-spec.js` là contract dùng chung. Coverage sinh từ registry/manifest/evidence tại `art/pipeline/unit-coverage-472/COVERAGE.md`:1080ô áp dụng,7104vị trí frame theo ngân sách;3ô có animation trong manifest hiện tại,397ô dùng static fallback,680ô thiếu. Những số này không tính candidate chưa cài thành hoàn thành. Các alias chia sẻ có chủ đích không tăng số frame cần vẽ.

## Trạng thái hiện tại

PUBLIC451 giữ50assets/bareURL fort/worldtrue và backend immutable230. Localmanifest51 có transport447 idle và navigation455 đã qualified459/466; chưa public. Fullsuite350 của462 là kết quả lịch sử hợp lệ; không lặp qualification466 hoặc ghi349/16failure cũ thành lỗi hiện hành.

Infantry dùng duy nhất master084845…0517f.468passing keys và469inbetweens đã nhập nguyên output, không gọi lại. F3cũ và474held được giữ;475là correction thứ2/2, sources470/477 đủ8wholeframes.479 đã dùng sharedcompiler, sameoriginal idle128 và walk128 trong isolatedcandidate52; actualChrome D0 Move/Pause/Resume/arrival/Stop/menu thấy đủ8frame, errors/network0, bảo toànsource/build/public và đónghandles.

**Pilot vẫn chưa motion-qualified:** review chỉSAMPLES_ONLY; owner477 chưa trả lời. Stride thử0.15 dựa trên projection chân làm cadence15.33cycles/s ở speed2.3, không phù hợp production. Không đổi speed để che lỗi, không cài canonical/public hay fanout từtechnicalPASS. Cần xem clip thực và làm rõ contact geometry theo D0 trước một order mới có giới hạn. F3correctioncap đã hết, không retry.

Wood032/iron141 chỉ được người dùng chấp nhận đúng loopD1 đã xem. Food101/những chuyển động khác không được hưởng phạm vi chấp nhận đó. Warship và10worldleader identities chưa có; portrait/reference không phải worldanimation.

## Workflow dùng chung

1. **Identity:** mỗi identity có `identity.json` trong `art/pipeline/unit-production/`. Giữ master/viewselected, camera, canvas, pivot, scale, physical equipment ownership và excludedrefs. Original infantry và wholehorse/cart/harness/cargo415 không được thiết kế lại. Chỉ tạo view còn thiếu; đối chiếu view liền kề.
2. **Action bank:** một action đủ8hướng; mỗi hướng một job. Hướngpilot làm key trước rồi inbetween. WalkF0contactA/F1downA/F2passingB/F3reachB/F4contactB/F5downB/F6passingA/F7reachA. Giữ normalizedphase qua các hướng, cho phép chuyển trọng lượng/thân/tay tự nhiên.
3. **Whole frames:** builtinimagegen edit đúngoriginal/lockedview +selectedneighbor +optionalwholeclothedoriginalderivedguide. Một call/frame còn thiếu, tối đa2correction/action/hướng. Nếu lỗi cùng loại tiếp tục: heldorder, đổi cách điều khiển pose trước gói mới. Pure2D, không3D/Blender/limbtexture/cutout/warp/mirror/pixelsplice/perframefit.
4. **Pack:** shared `scripts/sprite-production.py` xuất atlas/descriptor/contact/APNG/genericpreview một lệnh. Raw giữ nguyên; working256 vàruntime128 đều trực tiếp từraw bằng transformwholecanvas thống nhất. Pivot/familyscale cố định, padding2, khôngtrim/rotate. Newjob schema2 bắt buộcloop. Page<=2048px, budget128MiB không nâng đểtestqua.
5. **Review:** một sheet và10–15sloop normal-size;8ôhướng đồng bộ, missinghướng ghi rõ. Sửa lỗi thấy được: khácidentity, sai pha, giậtthân/scale/tool, missingpart, seam, trượtchân. Không auditcloth/anatomy/pixel nhiều vòng hay userapproval từngframe. TechnicalPASS không motionPASS.
6. **Runtime:** một cảnh thực tế cho unitbank: Move/turn/Stop; actionđặctrưng/hit/death; Pause/Resume; transitiongiữidentity/scale. Chrome chính, Firefox theođợttíchhợp. Fullmatch chỉ khi mechanicschange hoặc releasequalification.

Người đi, ngựa kéo xe, kỵbinh, bánhpháo vàthuyền có key/gait riêng. Không lấy walk bộbinh ghép vào ngựa. Guides chỉ authoringtools; visibleframe là wholeillustration.

## Prompt và phân việc

Nămtemplate view/key/inbetween/correction/worker_order ở `art/pipeline/unit-production/templates/`. `scripts/sprite-prompts.mjs` kiểmtra placeholder, identity/view/refroles/hash/selectedneighbor/guideprovenance và finiteorder trước call. Prompt không chứng minh output đúng.

Tối đa3workerSol6.1Low cộngroot. A sởhữu artpilot; B compiler/runtime; C review/viewlocks. Sau khipilotqualified, action đanglàm chia A:D0–D2,B:D3–D5,C:D6–D7. Chỉ cấpslot khi inputsselected; reviewchéo/root, khôngselfPASS. Root duy nhất ghépmanifest/release. Không haiworker cùngsửafile hoặc gọi cùngslot. Root/canonicalwrites chỉ saupreservationguardsCLOSED.

Sau infantry đủbộ: villager; spear/firearm; horsewagon trước cavalry; artillery/transport/warship;12leaders. Independentunits chỉparallel khiarchetypequalified. Hoànthành theo unitbank được nghiệmthu, khôngtheo sốcall/fileđãtạo.

## Runtime và bộ nhớ

Engine hiện có được giữ: identityregistry, atlasloader, picking, distancephase, attack/hit/death/gatherclocks.478bổsung authoritativecosmetic episodes cho ability/positivecargo load/unload/build/repair. Publicpayload chỉkind/start/end/looppolicy; khôngcargo/target/passengerleak. Damage/cargo/cooldown/outcome vẫnsimulation. Walk preemptposekhidịchchuyển; hit/death/attack vàneworder cancelstaleepisode. Finiteclip theoauthoritativeinterval; sustainedwork repeats. Missingaction dùng diagnosed sameidentityidle, không tínhcoverage.

Fulltarget7104paddedcells ít nhất472.18MiB trướcpageslack/non-unitart, vượt128MiB. Cần opt-in deferredatlas theo nhu cầu, boundedLRU và giữeageridle/world/shadow; encodedcache64MiB vẫncógiớihạn. Việc cài paging phải có focusedresource/disposaltests và actualbrowsercoldaction/fallback/cachedreturn; không suyra đôngunit/performancefullroster từfixture. Trạng thái implementation xem receipt480; chưa ngân sách/releasefinalrosterqualified.

## Đợt triển khai và release

| Gói | Kết quả | Phần còn mở |
|---|---|---|
| Framework471/478 | Compiler/preview, identity/action registry,5prompttemplates,coverage,actionepisodes | Artwork đaaction/đa hướng chưa tạo |
| Infantry470/477/479 |8wholeframes candidate,actualtravelcontrols | Continuousnaturalness/contact/stride/owner/fanout |
| Paging480 | Tải atlas theo nhu cầu khi được khai báo | Densebrowser/fullroster/offlineallbankqualification |
| Infantry hoànchỉnh |5actions×8directions chạy đúng | Chỉ mở saupilotqualified |
| Roster/leader tiếp theo | Đủaction8hướng cho từngidentity | Missingmasters/views/actionart/runtimeeventscene |
| FullRTS | Buildingsstates/maps/densecombat+rooms/defaultacceptedart/WAN/public2modes2maps | Tất cả tiêu chí chưađóng vẫngiữopen |

Build isolatedcwd/absoluteoutDir/exactViteconfig, preflight trướcbuild, seal trongtrial, actualUI/read-onlydiagnostics. Không mutate production khi test. Release mới cần exactsource/build/relevantscene/rooms0/current451frontend+230backendrollback. Navigation455 và478sharedmetadata đổisharedsim: pairedfrontend/backend mới; khôngclientonlyexchange/backendrestartPIDcũ. Fullgame chỉcompletekhi người dùng mởHTTPS chơi được cảhai mode/hai map và toàn bộcriticalcriteria đạt.

Continuation482/483 (12October): projectedcontact repair used3actual builtin calls (482initial+1correction;483completewholeclothedguide initial). All retain originalidentity but failphysicallegexchange, independentlyHELD. BothordersCLOSED/methodfailure,0newselectedframes,0dependentcalls; no stridefix/install/fanout. Currentselectedreferencejob remains470. Need a usable wholeoppositecontact source or demonstrably different pure2Dpose control; do not create equivalentorders/resetcaps. Sevenprompt/finiteguardtestsPASS; public451/backend230/sealed479/480 preserved. Evidence: docs/art/pipeline/infantry-projected-contact-482 and infantry-whole-pose-483.

Continuation484: local offline tick interpolation and bounded deferred encoded LRU implemented;32focused tests PASS, SAMEsealed candidate actualChrome+Firefox ordinaryMove/PauseResume/assignedarrival/Stop/menu PASS with sub-tick positions/errornetwork0/allpins preserved/ownedhandlesCLOSED. First protocol-sampling HOLD preserved; corrected read-only in-page rAF observation proves sub-tick movement. Public451/immutable230 unchanged. NO newimagecall, no newselectedframe, no pilot/fanout/motionapproval. Stride0.15 remains unqualified;482/483 CLOSED_HELD. Next art prerequisite is a usable whole same-original ContactB or demonstrated different pure2D control, not equivalent prompt retries. Evidence: docs/art/pipeline/offline-smoothing-484/CHECKPOINT.json and art-encoded-cache-484/receipt.json.
