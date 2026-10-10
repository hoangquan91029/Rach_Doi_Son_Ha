from pathlib import Path
import json,hashlib,shutil,subprocess,urllib.request,os,re,stat,tarfile
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');Q=R/'docs/qa/release-prepare-269';S=Path('/tmp/rds-release238-stage');BUILD=Path('/tmp/rds-release238-build');B=Path.home()/'.local/share/rach-doi-son-ha/releases/269';LIVE=Path.home()/'.local/share/rach-doi-son-ha/releases/230/runtime230';U='rach-doi-son-ha.service'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def inv(p):return {str(f.relative_to(p)):h(f) for f in sorted(p.rglob('*')) if f.is_file()}
def write(n,v):(Q/n).write_text(json.dumps(v,indent=2)+'\n')
def ctl(*args):return subprocess.check_output(['systemctl','--user',*args],text=True)
assert B.exists() and not (B/'rollback260').exists();assert stat.S_IMODE(B.stat().st_mode)==0o700
service=ctl('show',U,'-p','MainPID','-p','WorkingDirectory','-p','ActiveState');assert 'MainPID=575363' in service and str(LIVE) in service; (Q/'service-before.txt').write_text(service)
health=json.load(urllib.request.urlopen('http://127.0.0.1:3000/health',timeout=5));assert health=={'ok':True,'rooms':0};write('health-before.json',health)
public=inv(R/'dist');assert len(public)==192;assert public['assets/index-z82FayZ6.js']=='add2b4e819d43aff69360158ef7d0b867a078730a4c53135d1a5f5d8ced49e64';assert public==json.loads((R/'docs/qa/public-release-260/current-public-pins.json').read_text());write('public260-before.json',public)
assert h(LIVE/'shared/sim.js')=='29233a059ec084bc8577d20a1bccfd28ddc3024b9cb9bf4d5598c22f220f748b'
assert h(LIVE/'server/index.js')=='4e6a7e82f02d1d856f4ea788863c4836930bc00250be6a5b020ba2bdd8884198'
assert json.loads((LIVE/'node_modules/ws/package.json').read_text())['version']=='8.22.0'
assert h(R/'dist/assets/art-v1/wall-234/idle.png')=='58b99e4bd8bb4f6ecc3dcbb34d64a7999dbfef804aca9ba7e60e73fb508a100a'
assert len(json.loads((R/'dist/assets/art-v1/fort-202-manifest.json').read_text())['assets'])==43
# Private paired current230 rollback. Preserve original link policy as metadata; portable paired link is data-filter safe.
RB=B/'rollback260';RB.mkdir();shutil.copytree(R/'dist',RB/'dist');runtime=RB/'runtime230';runtime.mkdir()
for n in ['server','shared','node_modules']:shutil.copytree(LIVE/n,runtime/n,symlinks=True)
for n in ['package.json','package-lock.json']:
 if (LIVE/n).exists():shutil.copy2(LIVE/n,runtime/n)
(runtime/'dist').symlink_to('../dist',target_is_directory=True)
meta=RB/'service-metadata';meta.mkdir();shutil.copy2(Path.home()/'.config/systemd/user/rach-doi-son-ha.service',meta/'unit')
drop=Path.home()/'.config/systemd/user/rach-doi-son-ha.service.d';shutil.copytree(drop,meta/'dropins')
(meta/'effective-policy.txt').write_text(ctl('show',U,'-p','FragmentPath','-p','DropInPaths','-p','EnvironmentFiles','-p','Environment','-p','ExecStart','-p','WorkingDirectory'))
(meta/'runtime-dist-link.json').write_text(json.dumps({'original':os.readlink(LIVE/'dist'),'archivePortableLink':'../dist','pairedDistSHAInventory':'public260-before.json','restorationMustBindDistAndRuntimeTogether':True},indent=2))
# Environment-file custody if configured: raw bytes remain private, never printed.
envpolicy=ctl('show',U,'-p','EnvironmentFiles','--value');envs=[]
for f in re.findall(r'(/[^\s;]+)',envpolicy):
 path=Path(f.rstrip(')')); 
 if path.is_file():dest=meta/'environment-files'/path.name;dest.parent.mkdir(exist_ok=True);shutil.copy2(path,dest);envs.append({'reference':str(path),'sha256':h(path),'privateArchiveCopy':str(dest.relative_to(RB))})
(meta/'environment-references.json').write_text(json.dumps(envs,indent=2))
funnel=subprocess.run(['tailscale','serve','status','--json'],capture_output=True,text=True,timeout=10);assert funnel.returncode==0;(meta/'funnel-policy.json').write_text(funnel.stdout)
write('private-policy-references.json',{'unitSHA256':h(meta/'unit'),'dropinInventory':inv(meta/'dropins'),'effectivePolicySHA256':h(meta/'effective-policy.txt'),'funnelPolicySHA256':h(meta/'funnel-policy.json'),'environmentFilesCount':len(envs),'rawPolicyPrivateOnly':True,'originalRuntimeDistLinkRecorded':True})

write('canonical-phase-a.json',{'sourceHEAD':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'inventory':inv(R/'public/assets/art-v1'),'role':'Actual current canonical tree at PhaseA; not final candidate binding'})
