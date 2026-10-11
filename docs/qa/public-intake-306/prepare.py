from pathlib import Path
import json,hashlib
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');Q=R/'docs/qa/public-intake-306';old=R/'docs/qa/roster-runtime-303';h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
B=json.loads((old/'binding.json').read_text());B.update(rootAuthorized=False,runGO=False,promotion305Verified=False,publicURL='https://kieu-hoang-quan-loq-15iax9.tail5247a0.ts.net/?art=fort',promotionReceiptSHA256=None,currentPairedRollback299=None,currentPairedRollbackSHA256=None)
(Q/'binding.json').write_text(json.dumps(B,indent=2)+'\n')
s=(old/'browser.prepared.mjs').read_text().replace("import {chromium}","import {firefox}")
a=s.index("const {createGameServer}");b=s.index("const r=",a)
s=s[:a]+"""assert.equal(B.promotion305Verified,true);assert.ok(B.publicURL.startsWith('https://'));assert.ok(B.promotionReceiptSHA256);assert.ok(B.currentPairedRollbackSHA256);
await writeFile(new URL('call-state.json',out),JSON.stringify({status:'CLAIMED_ONE_BROWSER',campaigns:1,retries:0,startedAt:new Date().toISOString()},null,2)+'\\n',{flag:'wx'});
const browser=await firefox.launch({headless:true}),ctx=await browser.newContext({viewport:{width:1280,height:800},ignoreHTTPSErrors:false,recordVideo:{dir:new URL('clips/',out).pathname}}),p=await ctx.newPage();
"""+s[b:]
s=s.replace('ONE303 ordinary Chrome offlineDelta','ONE306 ordinary Firefox normalTLS offlineDelta').replace('await p.goto(`http://127.0.0.1:${game.server.address().port}/?art=fort`)','await p.goto(B.publicURL)').replace('PASS303_ACTUAL','PASS306_NORMALTLS_ACTUAL')
s=s.replace("await game.close();r.cleanup={rooms:game.rooms.size,serverListening:game.server.listening,browserClosed:true};await save();", "r.cleanup={browserClosed:true,contextClosed:true};await save();await writeFile(new URL('call-state.json',out),JSON.stringify({status:r.status.startsWith('PASS')?'TERMINAL_PASS_CLOSED':'TERMINAL_HOLD_CLOSED',campaigns:1,retries:0,completedAt:new Date().toISOString()},null,2)+'\\n');")
(Q/'firefox.prepared.mjs').write_text(s)
p=(old/'preservation.py').read_text().replace("docs/qa/roster-runtime-303","docs/qa/public-intake-306").replace("print('PASS303 preservation '","print('PASS306 preservation '")
pos=p.index("state={'stage'")
p=p[:pos]+"""P=R/'docs/qa/public-release-305/promotion.json';assert h(P)==B['promotionReceiptSHA256'];promotion=json.loads(P.read_text());assert promotion['status'].startswith('PROMOTED');assert json.loads((P.parent/'call-state.json').read_text())['state']=='PROMOTED_CLOSED'
assert h(Path(B['currentPairedRollback299']))==B['currentPairedRollbackSHA256']
"""+p[pos:]
p=p.replace("for n,sha in B['expectedResponseSHA256'].items():assert h(Path(B['build'])/n)==sha,n", "for n,sha in B['expectedResponseSHA256'].items():\n assert h(Path(B['build'])/n)==sha,n\n assert h(R/'dist'/n)==sha,n\nassert {n:v['sha256'] for n,v in inv(R/'dist').items()}==json.loads((R/'docs/qa/roster-install-302/candidate-pins.json').read_text())")
(Q/'preservation.py').write_text(p)
(Q/'preparation-receipt.json').write_text(json.dumps({'status':'PREP_ONLY_BROWSER_UNCALLED_WAIT305_ROOT_GO','sourceScene':'303 actual initial KingTHD GeneralTHD idleD0 exactpicks PauseResume Stop menu0','sceneRetries':0,'browserCalls':0,'firefoxPreparedSHA256':h(Q/'firefox.prepared.mjs'),'preservationSHA256':h(Q/'preservation.py'),'promotionRollbackBindingsPending':True,'scope':'ONE first Firefox normalTLS fouractualresponsepins/53ready12portraits; no fullmatch/motion/rosterart acceptance'},indent=2)+'\n')
