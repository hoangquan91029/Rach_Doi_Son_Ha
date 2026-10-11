from pathlib import Path
import hashlib,json,os,stat,subprocess,tarfile
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');Q=R/'docs/qa/unit-scale-public-432';P=Path.home()/'.local/share/rach-doi-son-ha/releases/432';B=Path('/tmp/rds-unit-scale426-build');S=Path('/tmp/rds-unit-scale426-stage');N=R.parent/'rds-public432-next-dist'
def cmd(*a):return subprocess.check_output(a,text=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def entry(p):
 s=p.lstat();assert not p.is_symlink();assert stat.S_ISREG(s.st_mode) or stat.S_ISDIR(s.st_mode)
 return {'type':'file' if p.is_file() else 'directory','mode':stat.S_IMODE(s.st_mode),**({'size':s.st_size,'sha256':sha(p)} if p.is_file() else {})}
def inv(p):return {'.':entry(p),**{str(x.relative_to(p)):entry(x) for x in sorted(p.rglob('*'))}}
def policy():
 rt=Path.home()/'.local/share/rach-doi-son-ha/releases/230/runtime230';pid=3229
 service=cmd('systemctl','--user','show','rach-doi-son-ha.service','-p','ActiveState','-p','MainPID','-p','WorkingDirectory','-p','FragmentPath','-p','DropInPaths','-p','EnvironmentFiles');assert 'MainPID=3229' in service and 'ActiveState=active' in service
 health=json.loads(cmd('curl','-fsS','http://127.0.0.1:3000/health'));assert health['rooms']==0
 return {'service':service,'health':health,'funnel':cmd('tailscale','serve','status','--json'),'exe':os.readlink('/proc/3229/exe'),'cwd':os.readlink('/proc/3229/cwd'),'cmdline':sha('/proc/3229/cmdline'),'environment':sha('/proc/3229/environ'),'distlink':os.readlink(rt/'dist'),'runtimePins':{str(p):sha(p) for p in [rt/'shared/sim.js',rt/'server/index.js',rt/'node_modules/ws/package.json',Path(os.readlink('/proc/3229/exe'))]}}
intake={'status':'PENDING_ROOT430_ACTUAL_CLEAR_TRAVEL_INTAKE','publicationForbidden':True}
core={str(p):sha(p) for root in [R/'client',R/'shared',R/'server',R/'public'] for p in root.rglob('*') if p.is_file()}
head=cmd('git','rev-parse','HEAD').strip();assert head.startswith('3a2ab48');assert not P.exists() and not N.exists()
binding=json.loads((R/'docs/qa/unit-scale-runtime-426/binding.json').read_text());preflight=json.loads((R/'docs/qa/unit-scale-runtime-426/preflight.json').read_text());assert binding['immutableSealed'] and preflight['status']=='PASS_PREBUILD426_WAIT_ROOT_BUILD'
for root,key in [(B,'buildPins'),(S,'sourcePins')]:
 actual={str(x.relative_to(root)):sha(x) for x in root.rglob('*') if x.is_file()};assert actual=={k:v['sha256'] for k,v in binding[key].items()}
source=inv(B);front=inv(R/'dist');assert sum(v['type']=='file' for v in source.values())==208
old={k:v for k,v in front.items() if v['type']=='file'};new={k:v for k,v in source.items() if v['type']=='file'}
modified=[k for k in old if old[k]!=new[k]];added=sorted(set(new)-set(old));allowed=set(preflight['modifiedPublicManifests'])-{'assets/art-v1/food-099-manifest.json'};assert set(modified)==allowed|{'index.html'} and len(allowed)==9;assert added==['assets/index-DOrSNC3u.js']
for k in allowed:
 a=json.loads((R/'dist'/k).read_text());b=json.loads((B/k).read_text());assert len(a['assets'])==len(b['assets'])
 for x,y in zip(a['assets'],b['assets']):
  xx=dict(x);yy=dict(y);xx.pop('render',None);yy.pop('render',None);assert xx==yy
 aa=dict(a);bb=dict(b);aa.pop('assets');bb.pop('assets');assert aa==bb
manifest=json.loads((B/'assets/art-v1/fort-202-manifest.json').read_text());assert len(manifest['assets'])==50
assert not any('food-099' in k for k in new)
rollback=Path.home()/'.local/share/rach-doi-son-ha/releases/428/rollback423.tar.gz';assert sha(rollback)=='fe37d0f1d339ae5ef3219ef7d2ddb68b5a2093f388a235b3f905e7e4600173fb'
before=policy();P.mkdir(mode=0o700);archive=P/'candidate426.tar.gz'
with tarfile.open(archive,'w:gz',dereference=False) as t:t.add(B,arcname='dist426')
archive.chmod(0o600);extract=P/'verified';extract.mkdir(mode=0o700);proof=[]
def safe(m,d):
 assert m.name=='dist426' or m.name.startswith('dist426/');rel='.' if m.name=='dist426' else m.name[len('dist426/'):];assert rel in source and not m.name.startswith('/') and '..' not in Path(m.name).parts and (m.isfile() or m.isdir());assert m.mode==source[rel]['mode'] and m.mode<=0o777
 f=tarfile.data_filter(m,d);proof.append({'name':m.name,'stored':m.mode,'filtered':f.mode});return f.replace(mode=m.mode,deep=False)
with tarfile.open(archive) as t:
 members=t.getmembers();assert len(members)==len(source) and len(set(m.name for m in members))==len(source);t.extractall(extract,filter=safe)
assert inv(extract/'dist426')==source
import shutil
shutil.copytree(extract/'dist426',N,copy_function=shutil.copy2);N.chmod(0o755);clone=inv(N);assert {k:v for k,v in clone.items() if k!='.'}=={k:v for k,v in source.items() if k!='.'};assert clone['.']['mode']==0o755
assert inv(B)==source and inv(R/'dist')==front and policy()==before and cmd('git','rev-parse','HEAD').strip()==head
for p,v in core.items():assert sha(p)==v,p
pins={k:new[k] for k in sorted(set(modified+added+['assets/index-8telBS7h.js','assets/index-Dx0ueiQl.css']))}
receipt={'order':432,'status':'CANDIDATE_PREPARED_CLOSED','archive':str(archive),'archiveSHA256':sha(archive),'ownedNextClone':str(N),'cloneRootMode':755,'files':208,'retainedPublicFiles':207,'modified':modified,'added':added,'TLSRequiredPins':pins,'sourceHEAD':head,'policyBeforeAfter':before,'rollback':str(rollback),'rollbackSHA256':sha(rollback),'safeExactByteModeExtractionPASS':True,'modeProof':proof,'publicationApproval':False,'rootActualSceneIntake':intake,'rootSeparatePromotionGORequired':True,'buildBrowserImageRestartPublicationCalls':0,'guards':'CLOSED','preservationPASS':True}
(Q/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:v for k,v in receipt.items() if k not in ['modeProof','policyBeforeAfter','TLSRequiredPins']}))
