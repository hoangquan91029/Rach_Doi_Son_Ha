from pathlib import Path
import json,hashlib,shutil,subprocess,urllib.request,os,re,stat,tarfile
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');Q=R/'docs/qa/release-prepare-238';S=Path('/tmp/rds-release238-stage');BUILD=Path('/tmp/rds-release238-build');B=Path.home()/'.local/share/rach-doi-son-ha/releases/238';LIVE=Path.home()/'.local/share/rach-doi-son-ha/releases/230/runtime230';U='rach-doi-son-ha.service'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def inv(p):return {str(f.relative_to(p)):h(f) for f in sorted(p.rglob('*')) if f.is_file()}
def write(n,v):(Q/n).write_text(json.dumps(v,indent=2)+'\n')
def ctl(*args):return subprocess.check_output(['systemctl','--user',*args],text=True)
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()=='1b5950aab363fd63d6ca164e7e751590edbf4a08'
assert not S.exists() and not BUILD.exists() and not B.exists();S.mkdir();B.mkdir(mode=0o700)
service=ctl('show',U,'-p','MainPID','-p','WorkingDirectory','-p','ActiveState');assert 'MainPID=575363' in service and str(LIVE) in service; (Q/'service-before.txt').write_text(service)
health=json.load(urllib.request.urlopen('http://127.0.0.1:3000/health',timeout=5));assert health=={'ok':True,'rooms':0};write('health-before.json',health)
public=inv(R/'dist');assert len(public)==186;assert public['assets/index-D5hSY7R3.js']=='479b4ad8b2806e6ed14f13e4b7c1314648faccd915a37be3cd6e744657dbb4cf';write('public230-before.json',public)
canonical={n:inv(R/n) for n in ['client','shared','server','public']};write('canonical-before.json',canonical)
for n in ['shared','server']:assert inv(R/n)==inv(LIVE/n),(n,'immutable backend mismatch')
assert h(R/'shared/sim.js')=='29233a059ec084bc8577d20a1bccfd28ddc3024b9cb9bf4d5598c22f220f748b';assert h(R/'server/index.js')=='4e6a7e82f02d1d856f4ea788863c4836930bc00250be6a5b020ba2bdd8884198';assert json.loads((LIVE/'node_modules/ws/package.json').read_text())['version']=='8.22.0'
for n in ['client','shared','server','public']:shutil.copytree(R/n,S/n)
for n in ['index.html','package.json','package-lock.json','vite.config.js']:shutil.copy2(R/n,S/n)
(S/'node_modules').symlink_to(R/'node_modules',target_is_directory=True)
p=S/'client/art-routes.js';before=p.read_text();line=" food:Object.freeze({manifestUrl:'/assets/art-v1/food-099-manifest.json',world:false}),\n";assert before.count(line)==1;p.write_text(before.replace(line,''))
removed={}
for n in ['assets/art-v1/food-099-manifest.json','assets/art-v1/food-099/atlas.png']:
 f=S/'public'/n;removed[n]=h(f);f.unlink()
assert not (S/'client/art-routes.js').read_text().find(' d0:')>=0
m=json.loads((S/'public/assets/art-v1/fort-202-manifest.json').read_text());assert len(m['assets'])==32;assert h(S/'public/assets/art-v1/fort-202-manifest.json')=='c2a6eb5791e6d2d70aecc3197b02ac33a7f205153891200aecec6abe777487a7'
old=json.loads((R/'docs/qa/wall-x-install-237/fort28-original-manifest.json').read_text());assert m['assets'][:28]==old['assets'];assert all(a in m['assets'] for a in old['assets'])
for n in ['shared','server']:assert inv(S/n)==canonical[n]
write('source-bindings.json',{'canonical':canonical,'stage':{n:inv(S/n) for n in ['client','shared','server','public']},'removedPendingFood':removed,'backendByteIdenticalCurrent230':True,'wsVersion':'8.22.0','fortAssets':32,'D0Absent':True,'stagePath':str(S),'outDir':str(BUILD),'config':str(S/'vite.config.js')})
# Private paired current230 rollback. Preserve original link policy as metadata; portable paired link is data-filter safe.
RB=B/'rollback230';RB.mkdir();shutil.copytree(R/'dist',RB/'dist');runtime=RB/'runtime230';runtime.mkdir()
for n in ['server','shared','node_modules']:shutil.copytree(LIVE/n,runtime/n,symlinks=True)
for n in ['package.json','package-lock.json']:
 if (LIVE/n).exists():shutil.copy2(LIVE/n,runtime/n)
(runtime/'dist').symlink_to('../dist',target_is_directory=True)
meta=RB/'service-metadata';meta.mkdir();shutil.copy2(Path.home()/'.config/systemd/user/rach-doi-son-ha.service',meta/'unit')
drop=Path.home()/'.config/systemd/user/rach-doi-son-ha.service.d';shutil.copytree(drop,meta/'dropins')
(meta/'effective-policy.txt').write_text(ctl('show',U,'-p','FragmentPath','-p','DropInPaths','-p','EnvironmentFiles','-p','Environment','-p','ExecStart','-p','WorkingDirectory'))
(meta/'runtime-dist-link.json').write_text(json.dumps({'original':os.readlink(LIVE/'dist'),'archivePortableLink':'../dist','pairedDistSHAInventory':'public230-before.json','restorationMustBindDistAndRuntimeTogether':True},indent=2))
# Environment-file custody if configured: raw bytes remain private, never printed.
envpolicy=ctl('show',U,'-p','EnvironmentFiles','--value');envs=[]
for f in re.findall(r'(/[^\s;]+)',envpolicy):
 path=Path(f.rstrip(')')); 
 if path.is_file():dest=meta/'environment-files'/path.name;dest.parent.mkdir(exist_ok=True);shutil.copy2(path,dest);envs.append({'reference':str(path),'sha256':h(path),'privateArchiveCopy':str(dest.relative_to(RB))})
(meta/'environment-references.json').write_text(json.dumps(envs,indent=2))
funnel=subprocess.run(['tailscale','serve','status','--json'],capture_output=True,text=True,timeout=10);assert funnel.returncode==0;(meta/'funnel-policy.json').write_text(funnel.stdout)
# Candidate backend snapshot (future client-only promotion can retain current immutable230 backend).
RT=B/'runtime238';RT.mkdir()
for n in ['server','shared','node_modules']:shutil.copytree(LIVE/n,RT/n,symlinks=True)
for n in ['package.json','package-lock.json']:
 if (LIVE/n).exists():shutil.copy2(LIVE/n,RT/n)
for tree in [RB,RT]:
 for f in tree.rglob('*'):
  if not f.is_symlink():f.chmod(0o555 if f.is_dir() else 0o444)
 tree.chmod(0o555)
write('private-policy-references.json',{'unitSHA256':h(meta/'unit'),'dropinInventory':inv(meta/'dropins'),'effectivePolicySHA256':h(meta/'effective-policy.txt'),'funnelPolicySHA256':h(meta/'funnel-policy.json'),'environmentFilesCount':len(envs),'rawPolicyPrivateOnly':True,'originalRuntimeDistLinkRecorded':True})
print('238 stage prepared, current backend byteidentical, paired rollback copied privately; no production mutations')
