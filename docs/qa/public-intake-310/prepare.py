from pathlib import Path
import json,hashlib
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');Q=R/'docs/qa/public-intake-310';old=R/'docs/qa/registry-publicscope-runtime-307';h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
B=json.loads((old/'binding.json').read_text());B.update(rootAuthorized=False,runGO=False,promotion309Verified=False,publicURL='https://kieu-hoang-quan-loq-15iax9.tail5247a0.ts.net/?art=fort',promotionReceiptSHA256=None,currentPairedRollback299='/home/kieu-hoang-quan/.local/share/rach-doi-son-ha/releases/304/rollback299.tar.gz',currentPairedRollbackSHA256='2a88dcd0a9315a7b7b1f27ad4e7643943918ced61ef131f784e0a6e168a7ec5a')
(Q/'binding.json').write_text(json.dumps(B,indent=2)+'\n')
s=(old/'browser.prepared.mjs').read_text().replace('import {firefox}','import {chromium}');a=s.index('const {createGameServer}');b=s.index('const r=',a)
s=s[:a]+"""assert.equal(B.promotion309Verified,true);assert.ok(B.promotionReceiptSHA256);assert.ok(B.publicURL.startsWith('https://'));
await writeFile(new URL('call-state.json',out),JSON.stringify({status:'CLAIMED_ONE_BROWSER',campaigns:1,retries:0,startedAt:new Date().toISOString()},null,2)+'\\n',{flag:'wx'});
const browser=await chromium.launch({headless:true}),ctx=await browser.newContext({viewport:{width:1280,height:800},ignoreHTTPSErrors:false,recordVideo:{dir:new URL('clips/',out).pathname}}),p=await ctx.newPage();
"""+s[b:]
s=s.replace('ONE307 ordinary Firefox offlineDelta','ONE310 ordinary Chrome normalTLS correctedPUBLIC offlineDelta').replace('`http://127.0.0.1:${game.server.address().port}/?art=food`',"B.publicURL.replace('?art=fort','?art=food')").replace('`http://127.0.0.1:${game.server.address().port}/?art=fort`','B.publicURL').replace('PASS307_ACTUAL','PASS310_NORMALTLS_ACTUAL')
s=s.replace("let food=await snap();", "await wait(s=>s.bootUi.ready===12);let food=await snap();")
s=s.replace("r.status='PASS310_NORMALTLS_ACTUAL", "assert.ok(!r.requestedPaths.some(x=>x.includes('food-099')));r.status='PASS310_NORMALTLS_ACTUAL")
s=s.replace("await game.close();r.cleanup={rooms:game.rooms.size,serverListening:game.server.listening,browserClosed:true};await save();", "r.cleanup={browserClosed:true,contextClosed:true};await save();await writeFile(new URL('call-state.json',out),JSON.stringify({status:r.status.startsWith('PASS')?'TERMINAL_PASS_CLOSED':'TERMINAL_HOLD_CLOSED',campaigns:1,retries:0,completedAt:new Date().toISOString()},null,2)+'\\n');")
(Q/'chrome.prepared.mjs').write_text(s)
p=(R/'docs/qa/public-intake-306/preservation.py').read_text().replace('public-intake-306','public-intake-310').replace('public-release-305','public-release-309').replace('roster-install-302/candidate-pins.json','registry-publicscope-305/build-pins.json').replace('PASS306','PASS310');(Q/'preservation.py').write_text(p)
(Q/'preparation-receipt.json').write_text(json.dumps({'status':'PREP_ONLY_WAIT307_ACCEPTANCE_309_CLOSED_ROOT_GO','browserCalls':0,'campaignLimit':1,'retries':0,'chromePreparedSHA256':h(Q/'chrome.prepared.mjs'),'preservationSHA256':h(Q/'preservation.py'),'promotionReceiptBindingPending':True,'publicURL':B['publicURL'],'scope':'Cold unknownfood menu asynchronous12portrait enabledfalse no099 requests; correctedPUBLIC fort53 KingTHD/GeneralTHD initialidleD0/picks/PauseResume/Stop/menu0 fouractualpins','supersedesUncalled306':True},indent=2)+'\n')
