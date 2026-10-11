from pathlib import Path
import hashlib,json,os,stat,subprocess,tarfile
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');Q=R/'docs/qa/horse-wagon-public-422';P=Path.home()/'.local/share/rach-doi-son-ha/releases/422';B=Path('/tmp/rds-horsewagon420-build');S=Path('/tmp/rds-horsewagon420-stage');N=R.parent/'rds-public422-next-dist'
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
intake=json.loads((R/'docs/qa/horse-wagon-runtime-420/root-intake.json').read_text());assert intake['status']=='ACCEPTED_SCOPED_STATIC_HORSE_WAGON_AND_ACTUAL_UI'
core={str(p):sha(p) for root in [R/'client',R/'shared',R/'server',R/'public'] for p in root.rglob('*') if p.is_file()}
head=cmd('git','rev-parse','HEAD').strip();assert head.startswith('3a2ab48');assert not P.exists() and not N.exists()
binding=json.loads((R/'docs/qa/horse-wagon-runtime-420/binding.json').read_text());preflight=json.loads((R/'docs/qa/horse-wagon-runtime-420/preflight.json').read_text());assert binding['immutableSealed'] and preflight['status']=='PASS_PREBUILD420_WAIT_ROOT_BUILD'
for root,key in [(B,'buildPins'),(S,'sourcePins')]:
 actual={str(x.relative_to(root)):sha(x) for x in root.rglob('*') if x.is_file()};assert actual=={k:v['sha256'] for k,v in binding[key].items()}
source=inv(B);front=inv(R/'dist');assert sum(v['type']=='file' for v in source.values())==207
old={k:v for k,v in front.items() if v['type']=='file'};new={k:v for k,v in source.items() if v['type']=='file'}
modified=[k for k in old if old[k]!=new[k]];added=sorted(set(new)-set(old));assert modified==['assets/art-v1/fort-202-manifest.json'];assert added==['assets/art-v1/wagon-horse-420/idle.png']
oldRows=json.loads((R/'dist/assets/art-v1/fort-202-manifest.json').read_text())['assets'];newRows=json.loads((B/'assets/art-v1/fort-202-manifest.json').read_text())['assets'];changedRows=[(a,b) for a,b in zip(oldRows,newRows) if a!=b];assert len(changedRows)==1 and all(a['family']=='unit.wagon' for pair in changedRows for a in pair)
manifest=json.loads((B/modified[0]).read_text());assert len(manifest['assets'])==50
for a in [changedRows[0][1]]:
 assert a['runtime']['derivation']=={'method':'resize','filter':'lanczos','sourceSha256':a['source']['sha256']}
 assert sha(R/a['source']['path'])==a['source']['sha256'] and sha(B/'assets/art-v1'/a['runtime']['path'])==a['runtime']['sha256']
assert not any('food-099' in k for k in new)
rollback=Path.home()/'.local/share/rach-doi-son-ha/releases/421/rollback417.tar.gz';assert sha(rollback)=='53ae347b8e61014ad27fdfbc565ac6885ec369c21d3b4099390cdc3ac983e2da'
before=policy();P.mkdir(mode=0o700);archive=P/'candidate420.tar.gz'
with tarfile.open(archive,'w:gz',dereference=False) as t:t.add(B,arcname='dist420')
archive.chmod(0o600);extract=P/'verified';extract.mkdir(mode=0o700);proof=[]
def safe(m,d):
 assert m.name=='dist420' or m.name.startswith('dist420/');rel='.' if m.name=='dist420' else m.name[len('dist420/'):];assert rel in source and not m.name.startswith('/') and '..' not in Path(m.name).parts and (m.isfile() or m.isdir());assert m.mode==source[rel]['mode'] and m.mode<=0o777
 f=tarfile.data_filter(m,d);proof.append({'name':m.name,'stored':m.mode,'filtered':f.mode});return f.replace(mode=m.mode,deep=False)
with tarfile.open(archive) as t:
 members=t.getmembers();assert len(members)==len(source) and len(set(m.name for m in members))==len(source);t.extractall(extract,filter=safe)
assert inv(extract/'dist420')==source
import shutil
shutil.copytree(extract/'dist420',N,copy_function=shutil.copy2);N.chmod(0o755);clone=inv(N);assert {k:v for k,v in clone.items() if k!='.'}=={k:v for k,v in source.items() if k!='.'};assert clone['.']['mode']==0o755
assert inv(B)==source and inv(R/'dist')==front and policy()==before and cmd('git','rev-parse','HEAD').strip()==head
for p,v in core.items():assert sha(p)==v,p
pins={k:new[k] for k in ['index.html','assets/index-8telBS7h.js',modified[0]]+added}
receipt={'order':422,'status':'CANDIDATE_PREPARED_CLOSED','archive':str(archive),'archiveSHA256':sha(archive),'ownedNextClone':str(N),'cloneRootMode':755,'files':207,'retainedPublicFiles':206,'modified':modified,'added':added,'TLSRequiredPins':pins,'sourceHEAD':head,'policyBeforeAfter':before,'rollback':str(rollback),'rollbackSHA256':sha(rollback),'safeExactByteModeExtractionPASS':True,'modeProof':proof,'publicationApproval':False,'rootActualSceneIntake':intake,'rootSeparatePromotionGORequired':True,'buildBrowserImageRestartPublicationCalls':0,'guards':'CLOSED','preservationPASS':True}
(Q/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:v for k,v in receipt.items() if k not in ['modeProof','policyBeforeAfter','TLSRequiredPins']}))
