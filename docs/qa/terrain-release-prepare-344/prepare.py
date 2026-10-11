from pathlib import Path,PurePosixPath
import json,hashlib,shutil,subprocess,stat,os,tarfile,re,urllib.request
R=Path.cwd();Q=R/'docs/qa/terrain-release-prepare-344';P=R/'docs/qa/terrain-publicscope-342';T=R/'docs/qa/terrain-public-trial-343';PRIVATE=Path.home()/'.local/share/rach-doi-son-ha/releases/344';S=Path('/tmp/rds-terrain-public342-stage');B=Path('/tmp/rds-terrain-public342-build');L=Path.home()/'.local/share/rach-doi-son-ha/releases/230/runtime230';RB=Path.home()/'.local/share/rach-doi-son-ha/releases/325'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text());write=lambda n,v:(Q/n).write_text(json.dumps(v,indent=2)+'\n');inv=lambda p:{str(f.relative_to(p)):h(f) for f in sorted(p.rglob('*')) if f.is_file()};ctl=lambda *a:subprocess.check_output(['systemctl','--user',*a],text=True)
def tree(b):
 out={}
 for p in [b,*sorted(b.rglob('*'))]:
  k=str(p.relative_to(b));s=p.lstat();m=stat.S_IMODE(s.st_mode)
  if p.is_symlink():out[k]={'type':'symlink','target':os.readlink(p),'mode':m}
  elif p.is_dir():out[k]={'type':'directory','mode':m}
  elif p.is_file():out[k]={'type':'file','sha256':h(p),'bytes':s.st_size,'mode':m}
  else:raise AssertionError('special file')
 return out
src=read(P/'source-bindings.json');bb=read(P/'build-binding.json');old=src['oldPublic'];new=read(P/'build-pins.json');assert read(T/'root-intake.json')['status'].startswith('NARROW');trial=read(T/'browser-receipt.json');assert trial['status'].startswith('PASS343') and trial['cleanup']=={'rooms':[0,0],'listening':[False,False],'browsersClosed':True};assert not PRIVATE.exists()
assert inv(R/'dist')==old and inv(B)==new;assert {n:inv(R/n) for n in src['canonical']}==src['canonical'];assert {n:inv(S/n) for n in src['stage']}==src['stage'];assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==src['sourceHEAD'];assert len(new)==207 and len(old)==205;assert set(new)-set(old)=={bb['bundlePath'],'assets/art-v1/rocky-ground-338/ground.webp'};assert {n for n in old if old[n]!=new[n]}=={'index.html','assets/art-v1/fort-202-manifest.json'};assert 'pass 4' in (P/'publication-contracts.txt').read_text()
svc=ctl('show','rach-doi-son-ha.service','-p','MainPID','-p','WorkingDirectory','-p','ActiveState');pid=int(re.search(r'MainPID=(\d+)',svc).group(1));assert pid>0 and str(L) in svc and 'ActiveState=active' in svc;health=json.load(urllib.request.urlopen('http://127.0.0.1:3000/health',timeout=5));assert health=={'ok':True,'rooms':0}
ri=read(R/'docs/qa/wall-collapse-rollback-325/source-inventories.json');archive=RB/'rollback309.tar.gz';assert h(archive)=='62c1e5356c8f71fd4f4a76cfa76fa53c2754d9f3d0ec4ad7ffbb1b6c88da10b3';assert tree(R/'dist')==ri['public309'];assert tree(L)==ri['immutableRuntime230'];assert h(Path.home()/'.config/systemd/user/rach-doi-son-ha.service')==ri['unitSHA256'];assert tree(Path.home()/'.config/systemd/user/rach-doi-son-ha.service.d')==ri['dropins'];assert h(Path(os.readlink(f'/proc/{pid}/exe')))==ri['node']['sha256']
policy=ctl('show','rach-doi-son-ha.service','-p','FragmentPath','-p','DropInPaths','-p','EnvironmentFiles','-p','Environment','-p','ExecStart','-p','WorkingDirectory');assert hashlib.sha256(policy.encode()).hexdigest()==ri['policySHA256'];assert hashlib.sha256(subprocess.check_output(['tailscale','serve','status','--json'])).hexdigest()==ri['funnelSHA256'];assert all(h(Path(e['reference']))==e['sha256'] for e in read(RB/'rollback309/service-metadata/environment-references.json'))
expected=read(R/'docs/qa/wall-collapse-rollback-325/archive-inventory.json')
with tarfile.open(archive) as t:
 members=t.getmembers();entries={str(Path(m.name).relative_to('rollback309')):m for m in members};assert set(entries)==set(expected)
 for k,v in expected.items():
  m=entries[k];n=PurePosixPath(m.name);assert not n.is_absolute() and '..' not in n.parts and n.parts[0]=='rollback309';assert m.isfile() or m.isdir() or m.issym();assert not m.islnk();assert m.mode==v['mode']
  if v['type']=='file':assert m.isfile() and hashlib.sha256(t.extractfile(m).read()).hexdigest()==v['sha256']
  elif v['type']=='directory':assert m.isdir()
  else:assert m.issym() and m.linkname==v['target'] and not PurePosixPath(m.linkname).is_absolute() and os.path.normpath(str(n.parent/m.linkname)).startswith('rollback309')
assert tree(RB/'verify-rollback309/rollback309')==expected
PRIVATE.mkdir(mode=0o700);D=PRIVATE/'dist344';shutil.copytree(B,D,copy_function=shutil.copy2);assert inv(D)==new;ct=tree(D);ca=PRIVATE/'dist344.tar.gz'
with tarfile.open(ca,'w:gz') as t:t.add(D,arcname='dist344',recursive=True)
ca.chmod(0o400)
with tarfile.open(ca) as t:
 members=t.getmembers();entries={str(Path(m.name).relative_to('dist344')):m for m in members};assert set(entries)==set(ct)
 for k,v in ct.items():
  m=entries[k];n=PurePosixPath(m.name);assert not n.is_absolute() and '..' not in n.parts and n.parts[0]=='dist344';assert m.mode==v['mode'] and (m.isfile() or m.isdir());
  if m.isfile():assert hashlib.sha256(t.extractfile(m).read()).hexdigest()==v['sha256']
 E=PRIVATE/'verify-candidate';E.mkdir(mode=0o700);t.extractall(E,filter='data')
 for m in members:
  if m.isfile():(E/m.name).chmod(m.mode)
 for m in sorted(members,key=lambda m:len(Path(m.name).parts),reverse=True):
  if m.isdir():(E/m.name).chmod(m.mode)
assert tree(E/'dist344')==ct
for name in ['source-bindings.json','build-binding.json','build-pins.json']:shutil.copy2(P/name,Q/name)
write('candidate-tree.json',ct);write('public309-before.json',old);write('receipt.json',{'status':'READY344_STATIC_TERRAIN54_SEPARATE_PROMOTION_UNCALLED','sourceHEAD':src['sourceHEAD'],'candidateArchive':str(ca),'candidateArchiveSHA256':h(ca),'candidateBytesModesSafeExtractionVerified':True,'candidateFiles':207,'manifestAssets':54,'bundlePath':bb['bundlePath'],'bundleSHA256':bb['bundleSHA256'],'manifestSHA256':bb['manifestSHA256'],'rollbackArchive':str(archive),'rollbackSHA256':h(archive),'pairedRollback':'Exactcurrentpublic309 frontend205 and immutable230 runtime/node/ws/unit/env/Funnel from325, current bytes/modes/entries/extractedtree reverified','rollbackBytesModesSafeExtractionVerified':True,'PID':pid,'service':svc,'policyInventory':'../wall-collapse-rollback-325/source-inventories.json','rootIntakeSHA256':h(T/'root-intake.json'),'sourceBindingsSHA256':h(Q/'source-bindings.json'),'health':health,'promotions':0,'builds':0,'browsers':0,'testsRerun':0,'imageCalls':0,'guards':'All343 handlesCLOSED'});assert inv(R/'dist')==old and inv(B)==new and {n:inv(R/n) for n in src['canonical']}==src['canonical'];assert ctl('show','rach-doi-son-ha.service','-p','MainPID','-p','WorkingDirectory','-p','ActiveState')==svc;assert tree(L)==ri['immutableRuntime230'];print('READY344 exact342 build reused; candidate and pairedcurrent309 rollback verified, no promotion')
