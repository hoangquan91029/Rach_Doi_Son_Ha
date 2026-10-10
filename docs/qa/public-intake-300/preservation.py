from pathlib import Path
import json,hashlib,subprocess,urllib.request,sys
R=Path.cwd();Q=R/'docs/qa/public-intake-300';h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();inv=lambda p:{str(f.relative_to(p)):h(f) for f in sorted(p.rglob('*')) if f.is_file()};read=lambda p:json.loads(p.read_text());ctl=lambda *a:subprocess.check_output(['systemctl','--user',*a],text=True)
P=read(R/'docs/qa/public-release-299/promotion.json');B=read(Q/'binding.json');S=read(R/'docs/qa/release-prepare-298/source-bindings.json');L=Path(P['backendRuntime'])
assert h(R/'docs/qa/public-release-299/promotion.json')==B['promotionReceiptSHA256'];assert read(R/'docs/qa/public-release-299/call-state.json')['state']=='PROMOTED_CLOSED';assert h(Path(P['pairedCurrentRollback286']))==B['currentPairedRollbackSHA256'];assert inv(R/'dist')==read(R/'docs/qa/public-release-299/current-public-pins.json');assert {n:inv(R/n) for n in S['canonical']}==S['canonical']
svc=ctl('show','rach-doi-son-ha.service','-p','MainPID','-p','WorkingDirectory','-p','ActiveState');assert 'MainPID=3229' in svc and 'ActiveState=active' in svc and str(L) in svc
health=json.load(urllib.request.urlopen('http://127.0.0.1:3000/health',timeout=5));assert health=={'ok':True,'rooms':0}
state={'canonical':{n:inv(R/n) for n in S['canonical']},'public':inv(R/'dist'),'backend':{n:inv(L/n) for n in ['server','shared','node_modules']},'service':svc,'policy':ctl('show','rach-doi-son-ha.service','-p','FragmentPath','-p','DropInPaths','-p','EnvironmentFiles','-p','Environment','-p','ExecStart','-p','WorkingDirectory'),'funnel':subprocess.check_output(['tailscale','serve','status','--json'],text=True),'health':health}
if sys.argv[1]=='before':
 for n,sha in B['expectedResponseSHA256'].items():assert h(R/'dist'/n)==sha
 (Q/'before-inventories.json').write_text(json.dumps(state,indent=2)+'\n')
else:
 before=read(Q/'before-inventories.json');assert state==before;(Q/'after-inventories.json').write_text(json.dumps(state,indent=2)+'\n');(Q/'post-preservation.json').write_text(json.dumps({'status':'PASS_EXACT_BEFORE_AFTER','canonicalPublicBackendPolicyFunnelUnchanged':True,'health':health},indent=2)+'\n')
print('PASS300 preservation '+sys.argv[1])
