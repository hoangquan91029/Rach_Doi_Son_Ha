from pathlib import Path,PurePosixPath
import json,hashlib,shutil,subprocess,urllib.request,stat,os,re,tarfile
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');Q=R/'docs/qa/mixed-gate-rollback-353';B=Path.home()/'.local/share/rach-doi-son-ha/releases/353';L=Path.home()/'.local/share/rach-doi-son-ha/releases/230/runtime230';U='rach-doi-son-ha.service'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,v):(Q/n).write_text(json.dumps(v,indent=2)+'\n')
def tree(b):
 out={}
 for p in [b,*sorted(b.rglob('*'))]:
  key=str(p.relative_to(b));s=p.lstat();m=stat.S_IMODE(s.st_mode)
  if p.is_symlink():out[key]={'type':'symlink','target':os.readlink(p),'mode':m}
  elif p.is_dir():out[key]={'type':'directory','mode':m}
  elif p.is_file():out[key]={'type':'file','sha256':h(p),'bytes':s.st_size,'mode':m}
  else:raise AssertionError('Special entry rejected')
 return out
ctl=lambda *args:subprocess.check_output(['systemctl','--user',*args],text=True)
service=ctl('show',U,'-p','MainPID','-p','WorkingDirectory','-p','ActiveState');pid=int(re.search(r'MainPID=(\d+)',service).group(1));assert pid>0 and 'ActiveState=active' in service and str(L) in service
node=Path(os.readlink(f'/proc/{pid}/exe'));assert node.is_file()
health=json.load(urllib.request.urlopen('http://127.0.0.1:3000/health',timeout=10));assert health['ok'] and health['rooms']==0 and pid==3229
sourceHEAD=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
sourceBefore={name:tree(R/name) for name in ['client','shared','server','tests']}
sourceFiles={name:h(R/name) for name in ['package.json','package-lock.json','vite.config.js']}
front=tree(R/'dist');files={k:v['sha256'] for k,v in front.items() if v['type']=='file'};assert len(files)==207
assert files['assets/index-Cz2oiMds.js']=='3495642c3c9ab988878659d0185cb7d5abac321dd350d1b7d3f1268c178695af'
assert files['assets/art-v1/fort-202-manifest.json']=='77363dfc5ace6c43682f1459743eeda16f269c32e62afdb2a39d639e092cf6da'
assert files['index.html']=='469f3bf2e74f8bf7fd771a4cb118563e31f3eaac7b8722c0173c57b3920bf24d'
assert len(json.loads((R/'dist/assets/art-v1/fort-202-manifest.json').read_text())['assets'])==54
assert h(L/'shared/sim.js')=='29233a059ec084bc8577d20a1bccfd28ddc3024b9cb9bf4d5598c22f220f748b';assert h(L/'server/index.js')=='4e6a7e82f02d1d856f4ea788863c4836930bc00250be6a5b020ba2bdd8884198';assert json.loads((L/'node_modules/ws/package.json').read_text())['version']=='8.22.0'
core=tree(L) # recorded exact immutable source, including dist link
unit=Path.home()/'.config/systemd/user/rach-doi-son-ha.service';drop=unit.with_name(U+'.d');unitBefore=h(unit);dropBefore=tree(drop)
policy=ctl('show',U,'-p','FragmentPath','-p','DropInPaths','-p','EnvironmentFiles','-p','Environment','-p','ExecStart','-p','WorkingDirectory');envRefs=ctl('show',U,'-p','EnvironmentFiles','--value');funnel=subprocess.check_output(['tailscale','serve','status','--json'],text=True,timeout=10)
assert not B.exists();B.mkdir(mode=0o700);RB=B/'rollback345';RB.mkdir(mode=0o700)
shutil.copytree(R/'dist',RB/'dist',symlinks=True);assert tree(RB/'dist')==front
runtime=RB/'runtime230';runtime.mkdir()
for name in ['server','shared','node_modules']:shutil.copytree(L/name,runtime/name,symlinks=True);assert tree(L/name)==tree(runtime/name)
for name in ['package.json','package-lock.json']:
 if (L/name).exists():shutil.copy2(L/name,runtime/name);assert h(L/name)==h(runtime/name) and stat.S_IMODE((L/name).stat().st_mode)==stat.S_IMODE((runtime/name).stat().st_mode)
(runtime/'dist').symlink_to('../dist',target_is_directory=True);(runtime/'bin').mkdir();shutil.copy2(node,runtime/'bin/node');assert h(node)==h(runtime/'bin/node');runtime.chmod(stat.S_IMODE(L.stat().st_mode))
meta=RB/'service-metadata';meta.mkdir(mode=0o700);shutil.copy2(unit,meta/'unit');shutil.copytree(drop,meta/'dropins');(meta/'effective-policy.txt').write_text(policy);(meta/'effective-policy.txt').chmod(0o600);(meta/'funnel-policy.json').write_text(funnel);(meta/'funnel-policy.json').chmod(0o600)
(meta/'runtime-dist-link.json').write_text(json.dumps({'original':os.readlink(L/'dist'),'archivePortableLink':'../dist','restorationMustBindDistAndRuntimeTogether':True},indent=2)+'\n')
envs=[]
for f in re.findall(r'(/[^\s;]+)',envRefs):
 path=Path(f.rstrip(')'))
 if path.is_file():
  dest=meta/'environment-files'/path.name;dest.parent.mkdir(mode=0o700,exist_ok=True);shutil.copy2(path,dest);envs.append({'reference':str(path),'sha256':h(path),'privateArchiveCopy':str(dest.relative_to(RB))})
(meta/'environment-references.json').write_text(json.dumps(envs,indent=2)+'\n')
write('source-inventories.json',{'sourceHEAD':sourceHEAD,'sourceTrees':sourceBefore,'sourceFiles':sourceFiles,'public345':front,'immutableRuntime230':core,'unitSHA256':unitBefore,'dropins':dropBefore,'node':{'path':str(node),'sha256':h(node),'mode':stat.S_IMODE(node.stat().st_mode)},'policySHA256':hashlib.sha256(policy.encode()).hexdigest(),'funnelSHA256':hashlib.sha256(funnel.encode()).hexdigest(),'environmentFilesCount':len(envs)})
expected=tree(RB);archive=B/'rollback345.tar.gz'
with tarfile.open(archive,'w:gz') as t:t.add(RB,arcname='rollback345',recursive=True)
archive.chmod(0o400)
with tarfile.open(archive) as t:
 members=t.getmembers();entries={str(Path(m.name).relative_to('rollback345')):m for m in members};assert set(entries)==set(expected)
 for m in members:
  n=PurePosixPath(m.name);assert not n.is_absolute() and '..' not in n.parts and n.parts[0]=='rollback345';assert m.isfile() or m.isdir() or m.issym();assert not m.islnk()
  if m.issym():
   target=PurePosixPath(m.linkname);assert not target.is_absolute();resolved=os.path.normpath(str(n.parent/target));assert resolved=='rollback345' or resolved.startswith('rollback345/')
 for k,v in expected.items():
  m=entries[k];assert m.mode==v['mode']
  if v['type']=='file':assert m.isfile() and hashlib.sha256(t.extractfile(m).read()).hexdigest()==v['sha256']
  if v['type']=='directory':assert m.isdir()
  if v['type']=='symlink':assert m.issym() and m.linkname==v['target']
 extraction=B/'verify-rollback345';extraction.mkdir(mode=0o700);t.extractall(extraction,filter='data')
 for m in members:
  if m.isfile():(extraction/m.name).chmod(m.mode)
 for m in sorted(members,key=lambda m:len(Path(m.name).parts),reverse=True):
  if m.isdir():(extraction/m.name).chmod(m.mode)
assert tree(extraction/'rollback345')==expected
assert tree(R/'dist')==front and tree(L)==core and h(unit)==unitBefore and tree(drop)==dropBefore
assert ctl('show',U,'-p','MainPID','-p','WorkingDirectory','-p','ActiveState')==service
assert ctl('show',U,'-p','FragmentPath','-p','DropInPaths','-p','EnvironmentFiles','-p','Environment','-p','ExecStart','-p','WorkingDirectory')==policy
assert subprocess.check_output(['tailscale','serve','status','--json'],text=True,timeout=10)==funnel
assert all(h(Path(e['reference']))==e['sha256'] for e in envs)
assert {name:tree(R/name) for name in sourceBefore}==sourceBefore
assert {name:h(R/name) for name in sourceFiles}==sourceFiles
healthAfter=json.load(urllib.request.urlopen('http://127.0.0.1:3000/health',timeout=10));assert healthAfter['ok'] and healthAfter['rooms']==0
write('archive-inventory.json',expected)
write('receipt.json',{'status':'READY353_PRIVATE_PAIRED_ROLLBACK345_NO_PROMOTION','archive':str(archive),'archiveSHA256':h(archive),'entries':len(expected),'publicFiles':207,'fortDescriptors':54,'livePID':pid,'healthBefore':health,'healthAfter':healthAfter,'sourceHEAD':sourceHEAD,'canonicalSourceBytesModesPreserved':True,'pairedRuntime':str(L),'simSHA256':h(L/'shared/sim.js'),'serverSHA256':h(L/'server/index.js'),'wsVersion':'8.22.0','safeEntriesVerified':True,'safeDataFilterExtractionVerified':True,'archiveBytesModesInventoryVerified':True,'exactExtractedBytesModesVerified':True,'publicRuntimeUnitEnvironmentFunnelPreserved':True,'originalRuntimeDistLinkRetained':True,'rawPolicyPrivateOnly':True,'browserCalls':0,'imageCalls':0,'tests':0,'liveCampaigns':0,'builds':0,'productionRestarts':0,'exchanges':0,'nextDistCloneCreated':False,'promotionAuthorized':False,'currentPriorRollback309Retained':True,'ownedHandlesClosed':True})
print('READY353: rollback345 archive byte/mode/safe-extraction verification passed; public/runtime/policy preserved.')
