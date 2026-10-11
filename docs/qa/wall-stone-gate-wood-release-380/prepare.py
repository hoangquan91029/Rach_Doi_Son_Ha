from pathlib import Path
import hashlib,json,os,stat,subprocess,tarfile,inspect
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');Q=R/'docs/qa/wall-stone-gate-wood-release-380';P=Path.home()/'.local/share/rach-doi-son-ha/releases/380';RT=P.parent/'230/runtime230';NODE=Path.home()/'.nvm/versions/node/v24.15.0/bin/node';HEAD='e042f0e97e9066c2c25ef7828657631963db593f'
def cmd(*a):return subprocess.check_output(a,text=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def entry(p):
 s=p.lstat();m=stat.S_IMODE(s.st_mode);assert m<=0o777
 if p.is_symlink():return {'type':'symlink','mode':m,'target':os.readlink(p)}
 if p.is_dir():return {'type':'directory','mode':m}
 assert stat.S_ISREG(s.st_mode);return {'type':'file','mode':m,'size':s.st_size,'sha256':sha(p)}
def inv(p):return {'.':entry(p),**{str(x.relative_to(p)):entry(x) for x in sorted(p.rglob('*'))}}
def policy():
 s=cmd('systemctl','--user','show','rach-doi-son-ha.service','-p','ActiveState','-p','MainPID','-p','WorkingDirectory','-p','FragmentPath','-p','DropInPaths','-p','EnvironmentFiles');pid=int(next(x.split('=')[1] for x in s.splitlines() if x.startswith('MainPID=')));assert pid==3229 and 'ActiveState=active' in s and str(RT) in s
 h=json.loads(cmd('curl','-fsS','http://127.0.0.1:3000/health'));assert h['rooms']==0
 assert os.readlink(f'/proc/{pid}/exe')==str(NODE);assert os.readlink(f'/proc/{pid}/cwd')==str(RT)
 return {'service':s,'pid':pid,'health':h,'funnel':cmd('tailscale','serve','status','--json'),'cmdlineSHA256':sha(f'/proc/{pid}/cmdline'),'environmentSHA256':sha(f'/proc/{pid}/environ'),'runtimeDistLink':os.readlink(RT/'dist')}
assert cmd('git','rev-parse','HEAD').strip()==HEAD and not P.exists()
front=inv(R/'dist');assert sum(v['type']=='file' for v in front.values())==196
assert front['assets/index-eaEH6Li-.js']['sha256']=='1dd1e2694658bcb797e17dccdd5686cdf68ccd75adc07f780ec580c92bebd2e0'
for n,c in [('stone-361',8),('fort-202',37)]:assert len(json.loads((R/f'dist/assets/art-v1/{n}-manifest.json').read_text())['assets'])==c
before=policy();assert before['runtimeDistLink']==str(R/'dist')
roots={'dist367':R/'dist','runtime230':RT,'node/bin/node':NODE,'policy/rach-doi-son-ha.service':Path.home()/'.config/systemd/user/rach-doi-son-ha.service','policy/rach-doi-son-ha.service.d':Path.home()/'.config/systemd/user/rach-doi-son-ha.service.d'}
# Pin canonical inputs and historical custody without copying or changing them.
guards={str(p):entry(p) for folder in ['client','shared','server','public'] for p in sorted((R/folder).rglob('*')) if p.is_file()}
for old in [P.parent/'353/rollback345.tar.gz',P.parent/'377/rollback367.tar.gz']:
 assert old.is_file();guards[str(old)]=entry(old)
source={}
for arc,p in roots.items():
 for rel,v in (inv(p) if p.is_dir() else {'.':entry(p)}).items():source[arc if rel=='.' else arc+'/'+rel]=v
P.mkdir(mode=0o700);snap=P/'policy-snapshot';snap.mkdir(mode=0o700)
for n,b,m in [('current.json',(json.dumps(before,indent=2)+'\n').encode(),0o600),('process-environment.bin',Path('/proc/3229/environ').read_bytes(),0o400),('process-cmdline.bin',Path('/proc/3229/cmdline').read_bytes(),0o400)]:
 p=snap/n;p.write_bytes(b);p.chmod(m);roots['policy/'+n]=p;source['policy/'+n]=entry(p)
archive=P/'rollback367.tar.gz'
with tarfile.open(archive,'w:gz',dereference=False) as t:
 for arc,p in roots.items():t.add(p,arcname=arc)
archive.chmod(0o600)
extract=P/'rollback-verified';extract.mkdir(mode=0o700)
modeproof=[]
def safe(m,dest):
 assert m.name in source and m.mode==source[m.name]['mode'] and m.mode<=0o777
 assert not m.name.startswith('/') and '..' not in Path(m.name).parts and (m.isfile() or m.isdir())
 f=tarfile.data_filter(m,dest);assert f.name==m.name
 modeproof.append({'name':m.name,'storedMode':m.mode,'dataFilterMode':f.mode,'extractedMode':m.mode})
 return f.replace(mode=m.mode,deep=False)
with tarfile.open(archive) as t:
 members=t.getmembers();assert len({m.name for m in members})==len(members) and set(m.name for m in members)==set(source)
 links=[m for m in members if m.issym() or m.islnk()];assert len(links)==1
 link=links[0];assert link.issym() and link.name=='runtime230/dist' and link.linkname==str(R/'dist') and link.mode==0o777
 # Never extract the production-targeting absolute symlink.
 t.extractall(extract,members=[m for m in members if m not in links],filter=safe)
for n,v in source.items():
 if v['type']=='symlink':assert not (extract/n).exists();continue
 assert entry(extract/n)==v,n
assert policy()==before and cmd('git','rev-parse','HEAD').strip()==HEAD
for p,v in guards.items():assert entry(Path(p))==v,p
for arc,p in roots.items():
 current=inv(p) if p.is_dir() else {'.':entry(p)}
 assert current=={('.' if n==arc else n[len(arc)+1:]):v for n,v in source.items() if n==arc or n.startswith(arc+'/')}
dump(P/'metadata.json',{'sourceHEAD':HEAD,'policy':before,'sourceEntries':source,'guards':guards})
dump(Q/'mode-proof.json',modeproof)
(Q/'stdlib-data-filter.txt').write_text(inspect.getsource(tarfile.data_filter)+inspect.getsource(tarfile._get_filtered_attrs))
receipt={'order':380,'status':'BACKUP_PREPARATION_PASS_CLOSED','sourceHEAD':HEAD,'rollbackArchive':str(archive),'rollbackSHA256':sha(archive),'archiveBytes':archive.stat().st_size,'frontFiles':196,'defaultAssets':8,'fortAssets':37,'bundleSHA256':front['assets/index-eaEH6Li-.js']['sha256'],'runtimeSimSHA256':sha(RT/'shared/sim.js'),'runtimeServerSHA256':sha(RT/'server/index.js'),'nodeSHA256':sha(NODE),'wsPackageSHA256':sha(RT/'node_modules/ws/package.json'),'pid':3229,'rooms':0,'sourceEntries':len(source),'extractedEntries':len({x['name'] for x in modeproof}),'filterInvocations':len(modeproof),'safeExactModesPASS':True,'symlinkExcludedAsserted':{'name':link.name,'target':link.linkname},'privateRootMode':stat.S_IMODE(P.stat().st_mode),'guardFiles':len(guards),'preservationPASS':True,'buildBrowserImagePublicationRestartCalls':0,'prior377UnqualifiedRetained':True,'publicApproval':False,'handles':'CLOSED'}
dump(Q/'receipt.json',receipt);print(json.dumps(receipt))
