from pathlib import Path
import json,hashlib,shutil,subprocess,urllib.request,stat
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');Q=R/'docs/qa/release-prepare-269';S=Path('/tmp/rds-corners266-stage');BUILD=Path('/tmp/rds-corners266-build');B=Path.home()/'.local/share/rach-doi-son-ha/releases/269';LIVE=Path.home()/'.local/share/rach-doi-son-ha/releases/230/runtime230';U='rach-doi-son-ha.service'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def inv(p):return {str(f.relative_to(p)):h(f) for f in sorted(p.rglob('*')) if f.is_file()}
def write(n,v):(Q/n).write_text(json.dumps(v,indent=2)+'\n')
def ctl(*args):return subprocess.check_output(['systemctl','--user',*args],text=True)
assert S.resolve()==Path('/tmp/rds-corners266-stage') and BUILD.resolve()==Path('/tmp/rds-corners266-build')
assert not (B/'dist269').exists()
assert inv(R/'dist')==json.loads((Q/'public260-before.json').read_text())
assert ctl('show',U,'-p','MainPID','-p','WorkingDirectory','-p','ActiveState')==(Q/'service-before.txt').read_text()
assert json.load(urllib.request.urlopen('http://127.0.0.1:3000/health',timeout=5))=={'ok':True,'rooms':0}
assert h(B/'rollback260.tar.gz')=='84e116f6adb9340ade2e9a17b2d8f2c33e015392da839e75e3ee77137cf6f4a6'
meta=B/'rollback260/service-metadata'
assert ctl('show',U,'-p','FragmentPath','-p','DropInPaths','-p','EnvironmentFiles','-p','Environment','-p','ExecStart','-p','WorkingDirectory')==(meta/'effective-policy.txt').read_text()
assert h(Path.home()/'.config/systemd/user/rach-doi-son-ha.service')==h(meta/'unit')
assert inv(Path.home()/'.config/systemd/user/rach-doi-son-ha.service.d')==inv(meta/'dropins')
assert subprocess.check_output(['tailscale','serve','status','--json'],text=True)==(meta/'funnel-policy.json').read_text()
for e in json.loads((meta/'environment-references.json').read_text()):assert h(Path(e['reference']))==e['sha256']
canonical={n:inv(R/n) for n in ['client','shared','server','public']};stage={n:inv(S/n) for n in canonical}
for n in ['shared','server']:assert canonical[n]==stage[n]==inv(LIVE/n)
food=" food:Object.freeze({manifestUrl:'/assets/art-v1/food-099-manifest.json',world:false}),\n"
expectedClient=canonical['client'].copy();route=(R/'client/art-routes.js').read_text();assert route.count(food)==1;expectedClient['art-routes.js']=hashlib.sha256(route.replace(food,'').encode()).hexdigest();assert stage['client']==expectedClient
assert ' d0:' not in (S/'client/art-routes.js').read_text()
removed={n:canonical['public'][n] for n in ['assets/art-v1/food-099-manifest.json','assets/art-v1/food-099/atlas.png']};expectedPublic={n:v for n,v in canonical['public'].items() if n not in removed};assert stage['public']==expectedPublic
for n in ['index.html','package.json','package-lock.json','vite.config.js']:assert h(R/n)==h(S/n)
mp='assets/art-v1/fort-202-manifest.json';manifest=json.loads((S/'public'/mp).read_text());assert len(manifest['assets'])==46 and h(S/'public'/mp)=='2600c650eb4a87b848dfac2f073a87f94d25296800434d32fc7c8b557fc855d0'
assert manifest['assets'][:43]==json.loads((R/'dist'/mp).read_text())['assets']
pinfile=R/'docs/qa/wall-corners-runtime-266/build-pins.json';assert h(pinfile)=='cbd23280b4118c895689966212232e9433bda0216a66268039c6ceb2f1e0bfa6';pins=json.loads(pinfile.read_text());assert inv(BUILD)==pins and len(pins)==195
for n,v in expectedPublic.items():assert pins[n]==v
assert pins['assets/index-z82FayZ6.js']=='add2b4e819d43aff69360158ef7d0b867a078730a4c53135d1a5f5d8ced49e64'
for n in removed:assert n not in pins
for f in ['docs/qa/wall-corners-runtime-266b/root-intake.json','docs/qa/wall-corners-firefox-267b/root-intake.json']:assert json.loads((R/f).read_text())['status'].startswith('ROOT_ACCEPTED_NARROW')
assert json.loads((R/'docs/qa/wall-corners-install-268/receipt.json').read_text())['frozenBuildExact']
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip();dirty=subprocess.check_output(['git','status','--porcelain=v1','-z'],cwd=R).decode().split('\0')
write('source-bindings.json',{'sourceHEAD':head,'dirtyStatus':dirty,'canonical':canonical,'stage':stage,'rootFiles':{n:h(R/n) for n in ['index.html','package.json','package-lock.json','vite.config.js']},'removedPendingFood':removed,'D0Absent':True,'fortAssets':46,'stagePath':str(S),'outDir':str(BUILD),'config':str(S/'vite.config.js'),'backendByteIdenticalCurrent230':True,'policyByteIdenticalPhaseA':True,'rootIntakePins':{f:h(R/f) for f in ['docs/qa/wall-corners-runtime-266b/root-intake.json','docs/qa/wall-corners-firefox-267b/root-intake.json','docs/qa/wall-corners-install-268/receipt.json']}})
write('build-binding.json',{'sourceHEAD':head,'cwd':str(S),'config':str(S/'vite.config.js'),'outDir':str(BUILD),'reusedExactTestedFrozenBuild':True,'builds':0,'stageCopies':0,'candidateFiles':195,'manifestAssets':46,'manifestSHA256':h(BUILD/mp),'bundleSHA256':pins['assets/index-z82FayZ6.js'],'buildPinsSHA256':h(pinfile),'finalCanonicalPublicScopeByteEquivalent':True})
write('build-pins.json',pins)
shutil.copytree(BUILD,B/'dist269')
for p in (B/'dist269').rglob('*'):
 if not p.is_symlink():p.chmod(0o555 if p.is_dir() else 0o444)
(B/'dist269').chmod(0o555);assert inv(B/'dist269')==pins
print('PhaseB exact frozen build binding and private read-only copy verified')
