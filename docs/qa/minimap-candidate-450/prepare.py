exec(open('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha/docs/qa/minimap-rollback-449/prepare.py').read().split("HEAD=cmd('git'")[0])
import shutil
Q=R/'docs/qa/minimap-candidate-450';P=Path.home()/'.local/share/rach-doi-son-ha/releases/450';B=Path('/tmp/rds-minimap446-build');S=Path('/tmp/rds-minimap446-stage');N=R.parent/'rds-public450-next-dist'
head=cmd('git','rev-parse','HEAD').strip();assert head=='39e3eb08a18479ffce671a4b3e8994ba4159bee2';assert not P.exists() and not N.exists()
pins=json.loads((R/'docs/qa/minimap-viewport-446/build-pins.json').read_text());source=inv(B);front=inv(R/'dist');assert sum(v['type']=='file' for v in source.values())==209
assert {k:v['sha256'] for k,v in source.items() if v['type']=='file'}==pins
old={k:v for k,v in front.items() if v['type']=='file'};new={k:v for k,v in source.items() if v['type']=='file'}
assert len(old)==208;assert set(old)<=set(new);changed=[k for k in old if old[k]!=new[k]];added=sorted(set(new)-set(old));assert changed==['index.html'];assert added==['assets/index-CU9fIOQr.js']
assert not any('food-099' in k for k in new)
intake=json.loads((R/'docs/qa/minimap-viewport-446/root-intake.json').read_text());assert intake['status']=='LOCAL_CANDIDATE_ACCEPTED'
pre=json.loads((R/'docs/qa/minimap-viewport-446/preflight.json').read_text())
for n,expected in pre['stagePins'].items():assert {k:v['sha256'] for k,v in inv(S/n).items() if v['type']=='file'}==expected
core={str(p):sha(p) for root in [R/'client',R/'shared',R/'server',R/'public'] for p in root.rglob('*') if p.is_file()}
before=policy();P.mkdir(mode=0o700);archive=P/'candidate446.tar.gz'
with tarfile.open(archive,'w:gz',dereference=False) as t:t.add(B,arcname='dist446')
archive.chmod(0o600);extract=P/'verified';extract.mkdir(mode=0o700)
def safe(m,d):
 assert m.name=='dist446' or m.name.startswith('dist446/');rel='.' if m.name=='dist446' else m.name[len('dist446/'):];assert rel in source and not m.name.startswith('/') and '..' not in Path(m.name).parts and (m.isfile() or m.isdir());assert m.mode==source[rel]['mode'] and m.mode<=0o777
 f=tarfile.data_filter(m,d);return f.replace(mode=m.mode,deep=False)
with tarfile.open(archive) as t:
 members=t.getmembers();assert len(members)==len(source) and len(set(m.name for m in members))==len(source);t.extractall(extract,filter=safe)
assert inv(extract/'dist446')==source
shutil.copytree(extract/'dist446',N,copy_function=shutil.copy2);N.chmod(0o755);clone=inv(N);assert {k:v for k,v in clone.items() if k!='.'}=={k:v for k,v in source.items() if k!='.'};assert clone['.']['mode']==0o755
assert inv(B)==source and inv(R/'dist')==front and policy()==before and cmd('git','rev-parse','HEAD').strip()==head
for p,v in core.items():assert sha(p)==v
r={'status':'PREPARED_CLOSED_WAIT_FIREFOX_AND_ROOT_RELEASE','sourceHEAD':head,'archive':str(archive),'archiveSHA':sha(archive),'stage':str(S),'build':str(B),'ownedNextClone':str(N),'files':209,'oldFiles':208,'modified':changed,'added':added,'scope':'Minimap code only; every old image/manifest/chunk retained byte/mode exact; immutable backend230 unchanged.','policy':before,'canonicalPins':core,'guards':'CLOSED','publicationCalls':0,'archiveSafeExactByteModeExtraction':True}
dump(Q/'receipt.json',r);print(json.dumps({k:r[k] for k in ['status','archiveSHA','files','modified','added']}))
