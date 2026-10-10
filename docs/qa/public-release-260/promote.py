from pathlib import Path
import json,hashlib,shutil,subprocess,urllib.request,ctypes,os,re,datetime
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');Q=R/'docs/qa/public-release-260';S=Path('/tmp/rds-release258-build');NEXT=R.parent/'rds-public260-next-dist';LIVE=Path.home()/'.local/share/rach-doi-son-ha/releases/230/runtime230';PRIVATE=Path.home()/'.local/share/rach-doi-son-ha/releases/258';URL='https://kieu-hoang-quan-loq-15iax9.tail5247a0.ts.net';U='rach-doi-son-ha.service';h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();inv=lambda b:{str(p.relative_to(b)):h(p) for p in sorted(b.rglob('*')) if p.is_file()}
def write(n,v):(Q/n).write_text(json.dumps(v,indent=2)+'\n')
def ctl(*a):return subprocess.check_output(['systemctl','--user',*a],text=True)
def get(path):return urllib.request.urlopen(URL+path,timeout=20).read()
def health():return json.load(urllib.request.urlopen('http://127.0.0.1:3000/health',timeout=5))
def service():return ctl('show',U,'-p','MainPID','-p','WorkingDirectory','-p','ActiveState')
def policy():return ctl('show',U,'-p','FragmentPath','-p','DropInPaths','-p','EnvironmentFiles','-p','Environment','-p','ExecStart','-p','WorkingDirectory')
assert (Q/'ROOT_GO.json').exists(),'Await root GO; preparation only'
assert json.loads((Q/'ROOT_GO.json').read_text())['authorized'] is True
old=json.loads((R/'docs/qa/release-prepare-258/public241-before.json').read_text());new=json.loads((R/'docs/qa/release-prepare-258/build-pins.json').read_text());assert len(old)==188 and len(new)==192;assert inv(R/'dist')==old and inv(S)==new
intake=json.loads((R/'docs/qa/release-intake-259A/root-intake.json').read_text());assert intake['promotion260Authorized'] is True
assert new['assets/index-z82FayZ6.js']=='add2b4e819d43aff69360158ef7d0b867a078730a4c53135d1a5f5d8ced49e64';assert old['assets/index-z82FayZ6.js']==new['assets/index-z82FayZ6.js']
assert h(PRIVATE/'rollback241.tar.gz')=='21f41cf17fe9e87ec0ab3d1eb8c0dcca632ddd34407eb553e4967c4f5c2bb250';assert inv(PRIVATE/'rollback241/dist')==old
assert h(PRIVATE/'dist258.tar.gz')=='b59664942353a77254d9bb2f8e6ce0bd5a1ad35929b672b63f93edccdbaca510';assert inv(PRIVATE/'dist258')==new
assert json.loads((R/'docs/qa/release-prepare-258/receipt.json').read_text())['status']=='FROZEN_FORT43_CANDIDATE_READY_FIREFOX259_INTAKE_NOT_PROMOTED'
backend={n:inv(LIVE/n) for n in ['shared','server','node_modules']};assert h(LIVE/'shared/sim.js')=='29233a059ec084bc8577d20a1bccfd28ddc3024b9cb9bf4d5598c22f220f748b';assert h(LIVE/'server/index.js')=='4e6a7e82f02d1d856f4ea788863c4836930bc00250be6a5b020ba2bdd8884198';assert json.loads((LIVE/'node_modules/ws/package.json').read_text())['version']=='8.22.0'
for n in ['shared','server','node_modules']:assert inv(PRIVATE/'rollback241/runtime230'/n)==backend[n]
initialService=service();assert 'MainPID=575363' in initialService and str(LIVE) in initialService;assert policy().encode()==(PRIVATE/'rollback241/service-metadata/effective-policy.txt').read_bytes();assert inv(Path.home()/'.config/systemd/user/rach-doi-son-ha.service.d')==inv(PRIVATE/'rollback241/service-metadata/dropins');assert h(Path.home()/'.config/systemd/user/rach-doi-son-ha.service')==h(PRIVATE/'rollback241/service-metadata/unit');funnel=subprocess.check_output(['tailscale','serve','status','--json'],text=True);assert hashlib.sha256(funnel.encode()).hexdigest()==h(PRIVATE/'rollback241/service-metadata/funnel-policy.json')
assert health()=={'ok':True,'rooms':0},'Active room: HOLD, never kick';assert hashlib.sha256(get('/')).hexdigest()==old['index.html'];assert hashlib.sha256(get('/assets/index-z82FayZ6.js')).hexdigest()==old['assets/index-z82FayZ6.js']
m=json.loads((S/'assets/art-v1/fort-202-manifest.json').read_text());assert len(m['assets'])==43;assert new['assets/art-v1/fort-202-manifest.json']=='e26c747a58ca9262edc45b7f87c93b7f6cf8b48d9236fe3a44f909b6bc1434b6'
newPNG=[p for p in new if p.endswith('.png') and any('/'+family+'/' in p for family in ['wall-239','gate-245','corner-248','gate-252'])];assert len(newPNG)==4,newPNG
assert not any('food-099' in p or 'd0-219' in p for p in new);assert all(not re.search('family-216|pilot-213',a['id']) for a in m['assets'])
canonical={n:inv(R/n) for n in ['client','shared','server','public']};assert canonical==json.loads((R/'docs/qa/release-prepare-258/canonical-before.json').read_text())
assert NEXT.exists() and inv(NEXT)==new;assert NEXT.stat().st_dev==(R/'dist').stat().st_dev;assert NEXT.stat().st_mode&0o777==0o755
libc=ctypes.CDLL(None,use_errno=True);fn=libc.renameat2;fn.argtypes=[ctypes.c_int,ctypes.c_char_p,ctypes.c_int,ctypes.c_char_p,ctypes.c_uint];fn.restype=ctypes.c_int
def exchange():
 if fn(-100,os.fsencode(R/'dist'),-100,os.fsencode(NEXT),2):raise OSError(ctypes.get_errno(),'renameat2 RENAME_EXCHANGE failed')
write('prepared.json',{'status':'GUARDS_PASS_READY_ATOMIC_EXCHANGE','sourceHEAD':'1b5950aab363fd63d6ca164e7e751590edbf4a08','actualHEAD':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'candidate':str(S),'nextClone':str(NEXT),'old':old,'new':new,'backendRetained':str(LIVE),'backendPins':backend,'PID':575363,'rollback':str(PRIVATE/'rollback241.tar.gz'),'rollbackSHA256':h(PRIVATE/'rollback241.tar.gz'),'healthBefore':health(),'method':'Linux renameat2 RENAME_EXCHANGE samefilesystem; no two-step gap'})
assert health()=={'ok':True,'rooms':0};assert service()==initialService and inv(R/'dist')==old and inv(NEXT)==new
switched=False
try:
 exchange();switched=True;assert inv(R/'dist')==new and inv(NEXT)==old
 assert hashlib.sha256(get('/')).hexdigest()==new['index.html'];assert hashlib.sha256(get('/assets/index-z82FayZ6.js')).hexdigest()==new['assets/index-z82FayZ6.js'];assert hashlib.sha256(get('/assets/art-v1/fort-202-manifest.json')).hexdigest()==new['assets/art-v1/fort-202-manifest.json'];assert len(json.loads(get('/assets/art-v1/fort-202-manifest.json'))['assets'])==43
 for p in newPNG:assert hashlib.sha256(get('/'+p)).hexdigest()==new[p]
 assert health()=={'ok':True,'rooms':0};assert service()==initialService;assert policy().encode()==(PRIVATE/'rollback241/service-metadata/effective-policy.txt').read_bytes();assert {n:inv(LIVE/n) for n in backend}==backend;assert {n:inv(R/n) for n in canonical}==canonical;assert subprocess.check_output(['tailscale','serve','status','--json'],text=True)==funnel
 write('promotion.json',{'status':'PROMOTED_CLIENT260_192_WITH_UNCHANGED_BACKEND230','deploymentUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sourceHEAD':'1b5950aab363fd63d6ca164e7e751590edbf4a08','publicChunk':'/assets/index-z82FayZ6.js','bundleSHA256':new['assets/index-z82FayZ6.js'],'distFiles':192,'manifestAssets':43,'newWholePNGs':{p:new[p] for p in newPNG},'normalTLSBytesVerified':['index','chunk','manifest43',*newPNG],'backendRuntime':str(LIVE),'PID':575363,'backendRestarted':False,'backendByteIdentical':True,'old188Tree':str(NEXT),'pairedRollback':str(PRIVATE/'rollback241.tar.gz'),'rollbackSHA256':h(PRIVATE/'rollback241.tar.gz'),'unitEnvironmentFunnelUnchanged':True,'canonicalSourceUnchanged':True,'health':health(),'method':'renameat2 RENAME_EXCHANGE','D0Installed':False,'foodCHARInstalled':False,'new239Installed':True,'browserRuns':0,'newBuilds':0,'imageCalls':0,'allOwnedHandlesClosedExceptIntentionalProduction':True,'pending':'normalTLS finite browser intake separate; no final/defaultart/motion/WAN approval'})
except Exception as e:
 write('failure.json',{'error':repr(e),'switched':switched,'timeUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()})
 if switched:exchange()
 assert inv(R/'dist')==old;assert service()==initialService;assert {n:inv(LIVE/n) for n in backend}==backend;write('rollback.json',{'status':'RESTORED_PAIRED241_FRONT_WITH_UNCHANGED230_BACKEND','health':health(),'PID':575363,'blindRetries':0});raise
write('current-public-pins.json',inv(R/'dist'));write('retained-old241-pins.json',inv(NEXT));(Q/'service-after.txt').write_text(service());print((Q/'promotion.json').read_text())
