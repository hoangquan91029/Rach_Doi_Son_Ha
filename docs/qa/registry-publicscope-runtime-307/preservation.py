from pathlib import Path
import json,hashlib,subprocess,urllib.request,sys
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');Q=R/'docs/qa/registry-publicscope-runtime-307';B=json.loads((Q/'binding.json').read_text());assert B['rootAuthorized'] and B['runGO']
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def inv(p):
 return {str(f.relative_to(p)):{'sha256':h(f),'mode':oct(f.stat().st_mode&0o777)} for f in sorted(p.rglob('*')) if f.is_file() and 'node_modules' not in f.relative_to(p).parts and '.git' not in f.relative_to(p).parts}
def ctl(*a):return subprocess.check_output(['systemctl','--user',*a],text=True)
L=Path('/home/kieu-hoang-quan/.local/share/rach-doi-son-ha/releases/230/runtime230');service=ctl('show','rach-doi-son-ha.service','-p','MainPID','-p','WorkingDirectory','-p','ActiveState');assert 'MainPID=3229' in service and 'ActiveState=active' in service and str(L) in service
health=json.load(urllib.request.urlopen('http://127.0.0.1:3000/health',timeout=5));assert health=={'ok':True,'rooms':0}
state={'stage':inv(Path(B['stage'])),'build':inv(Path(B['build'])),'canonical':{n:inv(R/n) for n in ['client','shared','server','public','tests']},'public':inv(R/'dist'),'backend':{n:inv(L/n) for n in ['server','shared']},'service':service,'policy':ctl('show','rach-doi-son-ha.service','-p','FragmentPath','-p','DropInPaths','-p','EnvironmentFiles','-p','Environment','-p','ExecStart','-p','WorkingDirectory'),'funnel':subprocess.check_output(['tailscale','serve','status','--json'],text=True),'health':health}
for n,sha in B['expectedResponseSHA256'].items():assert h(Path(B['build'])/n)==sha,n
if sys.argv[1]=='before':
 assert not (Q/'before-inventories.json').exists(),'Never overwrite original before custody'
 (Q/'before-inventories.json').write_text(json.dumps(state,indent=2)+'\n')
else:
 (Q/'after-inventories.json').write_text(json.dumps(state,indent=2)+'\n');before=json.loads((Q/'before-inventories.json').read_text());assert state==before,'Exact before/after preservation failed';(Q/'post-preservation.json').write_text(json.dumps({'status':'PASS_EXACT_BEFORE_AFTER','health':health},indent=2)+'\n')
print('PASS307 preservation '+sys.argv[1])
