from pathlib import Path
import hashlib,json,subprocess,urllib.request,os,stat
R=Path.cwd();Q=R/'docs/qa/release-prepare-304'; B=Path.home()/'.local/share/rach-doi-son-ha/releases/304'; L=Path.home()/'.local/share/rach-doi-son-ha/releases/230/runtime230'; C=B/'rollback299/runtime230'
def inv(p):
 return {str(f.relative_to(p)):{'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'mode':stat.S_IMODE(f.stat().st_mode)} for f in sorted(p.rglob('*')) if f.is_file()}
for n in ['server','shared','node_modules']:assert inv(L/n)==inv(C/n)
for n in ['package.json','package-lock.json']:
 if (L/n).exists():assert (L/n).read_bytes()==(C/n).read_bytes() and stat.S_IMODE((L/n).stat().st_mode)==stat.S_IMODE((C/n).stat().st_mode)
pub={str(f.relative_to(R/'dist')):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted((R/'dist').rglob('*')) if f.is_file()};assert pub==json.loads((Q/'public299-before.json').read_text())
service=subprocess.check_output(['systemctl','--user','show','rach-doi-son-ha.service','-p','MainPID','-p','WorkingDirectory','-p','ActiveState'],text=True);assert service==(Q/'service-before.txt').read_text();assert json.load(urllib.request.urlopen('http://127.0.0.1:3000/health'))=={'ok':True,'rooms':0}
a=json.loads((Q/'archives.json').read_text())['rollback299']

N=R/'docs/qa/release-prepare-308';P=Path.home()/'.local/share/rach-doi-son-ha/releases/308';assert P.exists()
meta=B/'rollback299/service-metadata'; h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert h(Path(a['path']))=='2a88dcd0a9315a7b7b1f27ad4e7643943918ced61ef131f784e0a6e168a7ec5a'
assert subprocess.check_output(['tailscale','serve','status','--json'],text=True)==(meta/'funnel-policy.json').read_text()
assert h(Path.home()/'.config/systemd/user/rach-doi-son-ha.service')==h(meta/'unit');assert inv(Path.home()/'.config/systemd/user/rach-doi-son-ha.service.d')==inv(meta/'dropins')
assert subprocess.check_output(['systemctl','--user','show','rach-doi-son-ha.service','-p','FragmentPath','-p','DropInPaths','-p','EnvironmentFiles','-p','Environment','-p','ExecStart','-p','WorkingDirectory'],text=True)==(meta/'effective-policy.txt').read_text()
assert all(h(Path(e['reference']))==e['sha256'] for e in json.loads((meta/'environment-references.json').read_text()))
node=json.loads((Q/'private-policy-references.json').read_text());assert h(Path(node['nodeExecutable']))==node['nodeSHA256']
print('Current rollback/public/runtime/policy still exact')
