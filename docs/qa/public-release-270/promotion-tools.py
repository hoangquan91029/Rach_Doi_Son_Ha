from pathlib import Path
import json,hashlib,shutil,subprocess,urllib.request,ctypes,os,stat,datetime
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');Q=R/'docs/qa/public-release-270';S=Path('/tmp/rds-corners266-build');STAGE=Path('/tmp/rds-corners266-stage');NEXT=R.parent/'rds-public270-next-dist';LIVE=Path.home()/'.local/share/rach-doi-son-ha/releases/230/runtime230';PRIVATE=Path.home()/'.local/share/rach-doi-son-ha/releases/269';URL='https://kieu-hoang-quan-loq-15iax9.tail5247a0.ts.net';U='rach-doi-son-ha.service';CHUNK='assets/index-z82FayZ6.js';MANIFEST='assets/art-v1/fort-202-manifest.json';PNG=[f'assets/art-v1/corner-{n}/idle.png' for n in (263,264,265)];RB_SHA='84e116f6adb9340ade2e9a17b2d8f2c33e015392da839e75e3ee77137cf6f4a6'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inv(b):return {str(p.relative_to(b)):h(p) for p in sorted(b.rglob('*')) if p.is_file()}
def modeinv(b):
 out={'.':{'type':'directory','mode':stat.S_IMODE(b.stat().st_mode)}}
 for p in sorted(b.rglob('*')):
  assert not p.is_symlink(),'Symlink in client tree';out[str(p.relative_to(b))]={'type':'file' if p.is_file() else 'directory','mode':stat.S_IMODE(p.stat().st_mode)}
 return out
def write(n,v):(Q/n).write_text(json.dumps(v,indent=2)+'\n')
def read(n):return json.loads((Q/n).read_text())
def ctl(*a):return subprocess.check_output(['systemctl','--user',*a],text=True)
def health():return json.load(urllib.request.urlopen('http://127.0.0.1:3000/health',timeout=5))
def service():return ctl('show',U,'-p','MainPID','-p','WorkingDirectory','-p','ActiveState')
def policy():return ctl('show',U,'-p','FragmentPath','-p','DropInPaths','-p','EnvironmentFiles','-p','Environment','-p','ExecStart','-p','WorkingDirectory')
def head():return subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
def policy_pins():
 meta=PRIVATE/'rollback260/service-metadata';refs=json.loads((R/'docs/qa/release-prepare-269/private-policy-references.json').read_text());assert hashlib.sha256(policy().encode()).hexdigest()==refs['effectivePolicySHA256'];assert h(Path.home()/'.config/systemd/user/rach-doi-son-ha.service')==refs['unitSHA256'];assert inv(Path.home()/'.config/systemd/user/rach-doi-son-ha.service.d')==refs['dropinInventory'];assert hashlib.sha256(subprocess.check_output(['tailscale','serve','status','--json'])).hexdigest()==refs['funnelPolicySHA256'];assert h(meta/'effective-policy.txt')==refs['effectivePolicySHA256'];return refs

def backend_pins():
 assert h(LIVE/'shared/sim.js')=='29233a059ec084bc8577d20a1bccfd28ddc3024b9cb9bf4d5598c22f220f748b';assert h(LIVE/'server/index.js')=='4e6a7e82f02d1d856f4ea788863c4836930bc00250be6a5b020ba2bdd8884198';assert json.loads((LIVE/'node_modules/ws/package.json').read_text())['version']=='8.22.0';b={n:inv(LIVE/n) for n in ['shared','server','node_modules']}
 for n in b:assert inv(PRIVATE/'rollback260/runtime230'/n)==b[n]
 for n in ['package.json','package-lock.json']:
  if (LIVE/n).exists():assert h(LIVE/n)==h(PRIVATE/'rollback260/runtime230'/n)
 assert 'MainPID=575363' in service() and str(LIVE) in service() and 'ActiveState=active' in service();assert str(LIVE/'server/index.js') in Path('/proc/575363/cmdline').read_bytes().decode().replace('\x00',' ');return b

def guards():
 old=json.loads((R/'docs/qa/public-release-260/current-public-pins.json').read_text());new=json.loads((R/'docs/qa/wall-corners-runtime-266/build-pins.json').read_text());assert len(old)==192 and len(new)==195;assert inv(R/'dist')==old;assert inv(S)==new;assert old[CHUNK]==new[CHUNK]=='add2b4e819d43aff69360158ef7d0b867a078730a4c53135d1a5f5d8ced49e64';assert set(new)-set(old)==set(PNG);assert [f for f in old if old[f]!=new[f]]==[MANIFEST];assert len(json.loads((S/MANIFEST).read_text())['assets'])==46
 b=json.loads((R/'docs/qa/wall-corners-runtime-266/binding.json').read_text())
 for group,files in b['stageInventories'].items():assert inv(STAGE/group)==files
 assert h(PRIVATE/'rollback260.tar.gz')==RB_SHA;assert inv(PRIVATE/'rollback260/dist')==old;backend=backend_pins();pol=policy_pins();assert health()=={'ok':True,'rooms':0},'Active room: HOLD; never kick rooms';return old,new,backend,pol

def prepare():
 assert not (Q/'promotion.json').exists() and not (Q/'prepared.json').exists();old,new,backend,pol=guards();assert not NEXT.exists(),'Owned next clone already exists; inspect, never overwrite';shutil.copytree(S,NEXT,copy_function=shutil.copy2);os.chmod(NEXT,0o755);assert inv(NEXT)==new;sourceModes=modeinv(S);cloneModes=modeinv(NEXT);assert {k:v for k,v in cloneModes.items() if k!='.'}=={k:v for k,v in sourceModes.items() if k!='.'};assert cloneModes['.']['mode']==0o755;assert NEXT.stat().st_dev==(R/'dist').stat().st_dev
 canonical={n:inv(R/n) for n in ['client','shared','server','public']};write('prepared.json',{'status':'PREPARATION_ONLY_ZERO_PROMOTIONS_WAIT269_READY_AND_EXPLICIT_ROOT_GO','sourceHEAD':head(),'candidate':str(S),'stage':str(STAGE),'nextClone':str(NEXT),'old':old,'new':new,'cloneModes':cloneModes,'sourceModes':sourceModes,'canonical':canonical,'backendPins':backend,'policyReferences':pol,'service':service(),'pairedRollback':str(PRIVATE/'rollback260.tar.gz'),'rollbackSHA256':RB_SHA,'healthAtPreparation':health(),'fortDescriptors':46,'promotions':0,'method':'Linux renameat2 RENAME_EXCHANGE; next root755; old public260 retained at owned nextclone after exchange','browserRuns':0,'builds':0,'imageCalls':0});write('nextclone.json',{'status':'OWNED_CLONE_BYTES_MODES_BOUND_ROOT755','path':str(NEXT),'files':195,'rootMode':0o755,'inventory':new,'modes':cloneModes});write('call-state.json',{'state':'PREPARED_NOT_EXECUTED','promotions':0,'maximumPromotions':1,'awaiting':'269 sealed ready receipt and explicit root run signal'});print('Prepared owned195/46 nextclone root755; ZERO promotions; current public260 unchanged')

def execute():
 assert (Q/'ROOT_GO.json').exists(),'Await explicit root run signal';go=read('ROOT_GO.json');assert go['authorized'] is True and go['preparedSHA256']==h(Q/'prepared.json');assert not (Q/'promotion.json').exists() and not (Q/'attempt.json').exists(),'One promotion attempt already consumed';prep=read('prepared.json');ready=Path(go['ready269Receipt']);assert ready.is_relative_to(R/'docs/qa/release-prepare-269');assert h(ready)==go['ready269ReceiptSHA256'];sealed=json.loads(ready.read_text());assert sealed['status']=='FROZEN_FORT46_FROZEN266_CANDIDATE_READY_ROOT266B_267B_ACCEPTED_NOT_PROMOTED';assert sealed['candidateArchive']['archiveBytesModesInventoryVerified'] and sealed['candidateArchive']['dataFilterExtractionThenExactModeRepairVerified'];sources=R/'docs/qa/release-prepare-269/source-bindings.json';assert h(sources)==sealed['sourceBindingSHA256'];binding=json.loads(sources.read_text());assert binding['sourceHEAD']==head();assert binding['canonical']==prep['canonical'];assert binding['stagePath']==str(STAGE) and binding['outDir']==str(S);
 for group,files in binding['stage'].items():assert inv(STAGE/group)==files
 for f,digest in binding['rootFiles'].items():assert h(R/f)==digest
 for f,digest in binding['rootIntakePins'].items():assert h(R/f)==digest
 assert sealed['rollback260SHA256']==RB_SHA;assert sealed['buildBinding']['manifestAssets']==46 and sealed['buildBinding']['candidateFiles']==195;assert h(S/MANIFEST)==sealed['buildBinding']['manifestSHA256'];assert h(R/'docs/qa/wall-corners-runtime-266/build-pins.json')==sealed['buildBinding']['buildPinsSHA256'];assert json.loads((R/'docs/qa/release-prepare-269/build-pins.json').read_text())==prep['new'];assert Path(go['candidate269Path']).is_relative_to(PRIVATE);assert inv(Path(go['candidate269Path']))==prep['new'];assert h(Path(go['candidate269Archive']))==go['candidate269ArchiveSHA256'];old,new,backend,pol=guards();assert old==prep['old'] and new==prep['new'];assert inv(NEXT)==new and modeinv(NEXT)==prep['cloneModes'];assert {n:inv(R/n) for n in prep['canonical']}==prep['canonical'];assert backend==prep['backendPins'] and pol==prep['policyReferences'];assert service()==prep['service'];assert NEXT.stat().st_dev==(R/'dist').stat().st_dev;assert stat.S_IMODE(NEXT.stat().st_mode)==0o755
 
 for f in ['index.html',CHUNK,MANIFEST]:assert hashlib.sha256(urllib.request.urlopen(URL+'/'+('' if f=='index.html' else f),timeout=20).read()).hexdigest()==old[f],f
 sourceHEAD=head();currentService=service();initialHealth=health();assert initialHealth=={'ok':True,'rooms':0};write('attempt.json',{'status':'ONE_AUTHORIZED_CLIENT_EXCHANGE_START','sourceHEAD':sourceHEAD,'preparedSourceHEAD':prep['sourceHEAD'],'canonicalInventoriesBound':True,'healthBefore':initialHealth,'timeUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()});libc=ctypes.CDLL(None,use_errno=True);fn=libc.renameat2;fn.argtypes=[ctypes.c_int,ctypes.c_char_p,ctypes.c_int,ctypes.c_char_p,ctypes.c_uint];fn.restype=ctypes.c_int
 def exchange():
  if fn(-100,os.fsencode(R/'dist'),-100,os.fsencode(NEXT),2):raise OSError(ctypes.get_errno(),'renameat2 RENAME_EXCHANGE failed')
 def get(f):return urllib.request.urlopen(URL+'/'+f,timeout=20).read()
 switched=False
 try:
  assert health()=={'ok':True,'rooms':0};assert service()==currentService and inv(R/'dist')==old and inv(NEXT)==new;exchange();switched=True;assert inv(R/'dist')==new and inv(NEXT)==old
  for f in ['index.html',CHUNK,MANIFEST,*PNG]:assert hashlib.sha256(get('' if f=='index.html' else f)).hexdigest()==new[f],f
  assert len(json.loads(get(MANIFEST))['assets'])==46;assert service()==currentService;assert backend_pins()==backend;assert policy_pins()==pol;assert {n:inv(R/n) for n in prep['canonical']}==prep['canonical'];assert health()=={'ok':True,'rooms':0}
  write('promotion.json',{'status':'PROMOTED_CLIENT270_195_FORT46_UNCHANGED_BACKEND230','deploymentUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sourceHEAD':sourceHEAD,'preparedSourceHEAD':prep['sourceHEAD'],'sourceInventoryBinding':'prepared.json canonical + frozen266 stageInventories','distFiles':195,'manifestAssets':46,'bundleSHA256':new[CHUNK],'manifestSHA256':new[MANIFEST],'newWholePNGs':{f:new[f] for f in PNG},'normalTLSBytesVerified':['index',CHUNK,MANIFEST,*PNG],'backendRuntime':str(LIVE),'PID':575363,'backendRestarted':False,'backendByteIdentical':True,'old192Public260Tree':str(NEXT),'pairedRollback':str(PRIVATE/'rollback260.tar.gz'),'rollbackSHA256':RB_SHA,'unitEnvironmentFunnelUnchanged':True,'canonicalSourceUnchanged':True,'health':health(),'method':'ONE renameat2 RENAME_EXCHANGE','promotions':1,'builds':0,'browserRuns':0,'imageCalls':0,'pending':'Separate finite normalTLS root intake; no character/defaultart/fullmatch/WAN/final acceptance'});write('current-public-pins.json',inv(R/'dist'));write('retained-old260-pins.json',inv(NEXT));(Q/'service-after.txt').write_text(service());write('call-state.json',{'state':'PROMOTED_CLOSED','promotions':1,'retries':0});print('PROMOTED270 exact195/46 normalTLS bytes verified, backend230 unchanged')
 except Exception as e:
  write('failure.json',{'error':repr(e),'switched':switched,'timeUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()})
  if switched:exchange()
  assert inv(R/'dist')==old;assert service()==currentService;assert backend_pins()==backend;assert policy_pins()==pol;write('rollback.json',{'status':'RESTORED_PUBLIC260_FRONT_WITH_UNCHANGED_PAIRED230_BACKEND','health':health(),'PID':575363,'blindRetries':0});write('call-state.json',{'state':'FAILED_ROLLBACK_CLOSED','promotions':int(switched),'retries':0});raise
if __name__=='__main__':
 import sys
 assert len(sys.argv)==2 and sys.argv[1] in ['prepare','execute'];prepare() if sys.argv[1]=='prepare' else execute()
