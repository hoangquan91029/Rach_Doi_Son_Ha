from pathlib import Path
import hashlib,json,os,stat,subprocess,tarfile,inspect
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');Q=R/'docs/qa/minimap-rollback-449';P=Path.home()/'.local/share/rach-doi-son-ha/releases/449';RT=P.parent/'230/runtime230';NODE=Path.home()/'.nvm/versions/node/v24.15.0/bin/node';HEAD='39e3eb0'
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
HEAD=cmd('git','rev-parse','HEAD').strip();assert HEAD=='39e3eb08a18479ffce671a4b3e8994ba4159bee2';assert not P.exists()
core={str(p):sha(p) for root in [R/'client',R/'shared',R/'server',R/'public'] for p in root.rglob('*') if p.is_file()}
front=inv(R/'dist');assert sum(v['type']=='file' for v in front.values())==208
assert front['assets/index-DOrSNC3u.js']['sha256']=='c64cd58ef1b6c7e9fe56f5e988579b6ee79828f61b29c285f4890fb9afc2d2a5'
for n,c in [('stone-361',16),('fort-202',50)]:assert len(json.loads((R/f'dist/assets/art-v1/{n}-manifest.json').read_text())['assets'])==c
assert sha(R/'dist/assets/art-v1/fort-202-manifest.json')=='42425c68d448f89047ea15fe6e108ec2b25393d34312ae0adb37ff1d9be282fa'
before=policy();assert before['runtimeDistLink']==str(R/'dist')
roots={'dist433':R/'dist','runtime230':RT,'node/bin/node':NODE,'policy/rach-doi-son-ha.service':Path.home()/'.config/systemd/user/rach-doi-son-ha.service','policy/rach-doi-son-ha.service.d':Path.home()/'.config/systemd/user/rach-doi-son-ha.service.d'}
# Pin canonical inputs and historical custody without copying or changing them.
guards={}
for old in [P.parent/'428/rollback423.tar.gz']:
 assert old.is_file();guards[str(old)]=entry(old)
source={}
for arc,p in roots.items():
 for rel,v in (inv(p) if p.is_dir() else {'.':entry(p)}).items():source[arc if rel=='.' else arc+'/'+rel]=v
P.mkdir(mode=0o700);snap=P/'policy-snapshot';snap.mkdir(mode=0o700)
for n,b,m in [('current.json',(json.dumps(before,indent=2)+'\n').encode(),0o600),('process-environment.bin',Path('/proc/3229/environ').read_bytes(),0o400),('process-cmdline.bin',Path('/proc/3229/cmdline').read_bytes(),0o400)]:
 p=snap/n;p.write_bytes(b);p.chmod(m);roots['policy/'+n]=p;source['policy/'+n]=entry(p)
archive=P/'rollback433.tar.gz'
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
assert policy()==before
assert cmd('git','rev-parse','HEAD').strip()==HEAD
for p,v in core.items():assert sha(p)==v,p
for p,v in guards.items():assert entry(Path(p))==v,p
for arc,p in roots.items():
 current=inv(p) if p.is_dir() else {'.':entry(p)}
 assert current=={('.' if n==arc else n[len(arc)+1:]):v for n,v in source.items() if n==arc or n.startswith(arc+'/')}
dump(P/'metadata.json',{'sourceHEADSnapshot':HEAD,'canonicalHEADGuarded':True,'policy':before,'sourceEntries':source,'guards':guards})
dump(Q/'mode-proof.json',modeproof)
(Q/'stdlib-data-filter.txt').write_text(inspect.getsource(tarfile.data_filter)+inspect.getsource(tarfile._get_filtered_attrs))
receipt={'order':449,'status':'BACKUP_PREPARATION_PASS_CLOSED','sourceHEADSnapshot':HEAD,'canonicalHEADGuarded':True,'rollbackArchive':str(archive),'rollbackSHA256':sha(archive),'archiveBytes':archive.stat().st_size,'frontFiles':208,'default':'fort','world':True,'defaultAssets':50,'fortAssets':50,'bundleSHA256':front['assets/index-DOrSNC3u.js']['sha256'],'runtimeSimSHA256':sha(RT/'shared/sim.js'),'runtimeServerSHA256':sha(RT/'server/index.js'),'nodeSHA256':sha(NODE),'wsPackageSHA256':sha(RT/'node_modules/ws/package.json'),'pid':3229,'rooms':0,'sourceEntries':len(source),'extractedEntries':len({x['name'] for x in modeproof}),'filterInvocations':len(modeproof),'safeExactModesPASS':True,'symlinkExcludedAsserted':{'name':link.name,'target':link.linkname},'privateRootMode':stat.S_IMODE(P.stat().st_mode),'guardFiles':len(guards),'preservationPASS':True,'buildBrowserImagePublicationRestartCalls':0,'prior377UnqualifiedRetained':True,'publicApproval':False,'handles':'CLOSED'}
dump(Q/'receipt.json',receipt);print(json.dumps(receipt))
