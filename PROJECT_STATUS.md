# Trạng thái — checkpoint384 / local382 / public382

**INCOMPLETE.** [Full plan](docs/PROJECT_PLAN.md) · [Next](NEXT_STEPS.md) · [Movement](docs/art/pipeline/MOVEMENT_PRODUCTION_PLAN_20261010.md). Các entrypoint cũ từ e042 giữ byte nguyên tại docs/checkpoints/checkpoint384-entrypoints/.

## Tường đá, cổng gỗ — đã có trên link mặc định

[Game HTTPS](https://kieu-hoang-quan-loq-15iax9.tail5247a0.ts.net/) hiện dùng ba mẫu tường đá chân thực X362/Y364/corner365 và cổng gỗ original X245/Y252. Bảy descriptor cổng dùng hai ảnh gốc, không quay/lật/ghép ảnh; unsupported wall states dùng nativeSTONE, unsupported gate states dùng nativeWOOD. Cây, resourcewood, nhà, economy/simulation không đổi. Static construction373 mask0 cũng được phát hành; không phải animatedconstruction hay allbuilding states.

[379 actual candidate](docs/qa/wood-gate-restoration-379/receipt.json) kiểm tra Chrome cả hai trục: xây wall-gate-wall/chọn đúng cổng/dân làng đi qua/PauseResumeStop/menu,16assets/12portraits/zeroerrors. Root brief gameplay-size scenes chấp nhận narrow completedidle joins. [Local382](docs/qa/wood-gate-install-382/installation.json) cài exact10common files;13 focusedcanonicaltestsPASS. LOCAL food recipe/payload vẫn giữ riêng; PUBLIC food099 excluded. Original raw, oldwall/gate art, failures và leadership custody giữ nguyên.

[Public382 release](docs/qa/wall-stone-gate-wood-release-382/receipt.json) phát hành đúng frozen379/381200files/default16/fort45: index-DLWMD8Y7.js SHA773152beb73437dc5ea8f8addf383701f5289b10ad9550cede28c2012464a729, defaultmanifest a028bc8c2e100d28b5bf3c572038117c09cefacc1c9ce4d8ccbf14fec3bca627, fortmanifest4485087fb50a6633c943fbbba96f6cced6a009e70f68451b97f6ecdff385a048. ONEatomic frontendexchange/8normalTLS pins exact;oldJS/currentCSS/unrelatedpayload retained. No build/backend restart during publication.

[383 actual publicFirefox](docs/qa/wood-gate-public-383/receipt.json): bareURL Xwoodgate+stonewalls masks1/3/2,2579actualrasterdraws/16ready/12portraits/exactopaquegatepick/ordinaryfriendlytransit/enginearrival<=.7/PausefreezeResume/Stop/menu0/23responsepins/errorsnetworkHTTP0. [Root brief scene intake](docs/qa/wood-gate-public-383/root-intake.json) accepts these completedidle joins.422preservationpins PASS; all ownedhandles closed/productionrooms0. Y source and actual joins qualified379Chrome. No fullmatch/WAN/allstate/defaultfullart inference.

## Backend và rollback

Backend230 giữ nguyên immutable releases/230/runtime230, sim29233a059ec084bc8577d20a1bccfd28ddc3024b9cb9bf4d5598c22f220f748b/server4e6a7e82f02d1d856f4ea788863c4836930bc00250be6a5b020ba2bdd8884198/ws8.22/node/PID3229/unit/env/Funnel unchanged. Canonical source edits không thay running backend.

Rollback hiện hành là367frontend +230backend: private380/rollback367.tar.gz SHA71653bffd2497de433fcebae4faf9a9e325d0f69fd0f80a671b04642e90f091e, old367tree rds-public382-next-dist.380/381 safeentries/exactbytes/modes verified. Prior353rollback345 và failed377partials chỉ là history; không dùng làm currenttarget.378 wrongatlas/preflight failure/unqualified build và382 preexchange allowlist failure retained; corrections applied before qualified379build/382exchange.

## Phần chưa hoàn tất

Stone wall hit/destruction, construction motion và các trạng thái khác; wooden gate unsupported states; fullroster/eightdirections/actions/12leaders/familyscale/mapcomposition/densecombat+roomsperformance/defaultacceptedfullart/externaldesktopWAN/finalpublicbothmapsbothmodes vẫn OPEN.350 samehost idle room baseline không phải densecombat/WAN; không có căn cứ tối ưu suy đoán hoặc lặp baseline.

Movement213/216/233 owner naturalness/worldcontact/bodyvolume/shadow/familyscale/runtime/fanout OPEN; pending195 không approve213. Owner032wood/141iron chỉ shownD1, food101 riêng, loadedgoods ordinarywalk. Terrain340/registry302 retained. Strict purewhole2D/builtinimagegen/Sol6.1Low remains; no API/key/CLI/quota/3D/limbtextures/cutouts/pixelsplices/warp/mirror/perframefit. Không repeated motion audits/blind calls.

Automation311 native schedule missing/human choice pending; không claim5hACTIVE/recreation. Full goal active; quiet continuation intent preserved.
