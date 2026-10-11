from pathlib import Path
import hashlib,json,os,stat,subprocess,tarfile
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');Q=R/'docs/qa/initial-actors-public-402';P=Path.home()/'.local/share/rach-doi-son-ha/releases/402';B=Path('/tmp/rds-actors399-build');S=Path('/tmp/rds-actors399-stage');N=R.parent/'rds-public402-next-dist'
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
head=cmd('git','rev-parse','HEAD').strip();assert head.startswith('63705a6');assert not P.exists() and not N.exists()
binding=json.loads((R/'docs/qa/initial-actors-runtime-399/binding.json').read_text());preflight=json.loads((R/'docs/qa/initial-actors-runtime-399/preflight.json').read_text());assert binding['immutableSealed'] and preflight['status']=='PASS_PREBUILD399'
for root,key in [(B,'buildPins'),(S,'sourcePins')]:
 actual={str(x.relative_to(root)):sha(x) for x in root.rglob('*') if x.is_file()};assert actual=={k:v['sha256'] for k,v in binding[key].items()}
source=inv(B);front=inv(R/'dist');assert sum(v['type']=='file' for v in source.values())==204
old={k:v for k,v in front.items() if v['type']=='file'};new={k:v for k,v in source.items() if v['type']=='file'}
modified=[k for k in old if old[k]!=new[k]];added=sorted(set(new)-set(old));assert modified==['assets/art-v1/fort-202-manifest.json'];assert added==['assets/art-v1/initial-actors-399/king396.png','assets/art-v1/initial-actors-399/spearman400.png','assets/art-v1/initial-actors-399/wagon398.png']
assert len(json.loads((B/modified[0]).read_text())['assets'])==48
rollback=Path.home()/'.local/share/rach-doi-son-ha/releases/401/rollback393.tar.gz';assert sha(rollback)=='2241e2b25f1ce84a6bc0037176dd01d42ed84d27dad751e3f3565f34c59f96e2'
before=policy();P.mkdir(mode=0o700);archive=P/'candidate399.tar.gz'
with tarfile.open(archive,'w:gz',dereference=False) as t:t.add(B,arcname='dist399')
archive.chmod(0o600);extract=P/'verified';extract.mkdir(mode=0o700);proof=[]
def safe(m,d):
 assert m.name=='dist399' or m.name.startswith('dist399/');rel='.' if m.name=='dist399' else m.name[len('dist399/'):];assert rel in source and not m.name.startswith('/') and '..' not in Path(m.name).parts and (m.isfile() or m.isdir());assert m.mode==source[rel]['mode'] and m.mode<=0o777
 f=tarfile.data_filter(m,d);proof.append({'name':m.name,'stored':m.mode,'filtered':f.mode});return f.replace(mode=m.mode,deep=False)
with tarfile.open(archive) as t:
 members=t.getmembers();assert len(members)==len(source) and len(set(m.name for m in members))==len(source);t.extractall(extract,filter=safe)
assert inv(extract/'dist399')==source
import shutil
shutil.copytree(extract/'dist399',N,copy_function=shutil.copy2);N.chmod(0o755);clone=inv(N);assert {k:v for k,v in clone.items() if k!='.'}=={k:v for k,v in source.items() if k!='.'};assert clone['.']['mode']==0o755
assert inv(B)==source and inv(R/'dist')==front and policy()==before and cmd('git','rev-parse','HEAD').strip()==head
pins={k:new[k] for k in ['index.html','assets/index-8telBS7h.js',modified[0]]+added}
receipt={'order':402,'status':'CANDIDATE_PREPARED_CLOSED','archive':str(archive),'archiveSHA256':sha(archive),'ownedNextClone':str(N),'cloneRootMode':755,'files':204,'retainedPublicFiles':201,'modified':modified,'added':added,'TLSRequiredPins':pins,'sourceHEAD':head,'policyBeforeAfter':before,'rollback':str(rollback),'rollbackSHA256':sha(rollback),'safeExactByteModeExtractionPASS':True,'modeProof':proof,'publicationApproval':False,'rootActualSceneGORequired':True,'buildBrowserImageRestartPublicationCalls':0,'guards':'CLOSED','preservationPASS':True}
(Q/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:v for k,v in receipt.items() if k not in ['modeProof','policyBeforeAfter','TLSRequiredPins']}))
