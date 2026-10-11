from pathlib import Path
import hashlib,json,stat,os,subprocess,tarfile,re
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');Q=R/'docs/qa/wall-stone-gate-wood-public-381';P=Path.home()/'.local/share/rach-doi-son-ha/releases/381';B=Path('/tmp/rds-gates379-build');S=Path('/tmp/rds-gates379-stage');T=R/'docs/qa/wood-gate-restoration-379';OLD=P.parent/'380';HEAD='e042f0e97e9066c2c25ef7828657631963db593f'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def cmd(*a):return subprocess.check_output(a,text=True)
def entry(p):
 s=p.lstat();assert stat.S_IMODE(s.st_mode)<=0o777 and not p.is_symlink()
 if p.is_dir():return {'type':'directory','mode':stat.S_IMODE(s.st_mode)}
 assert stat.S_ISREG(s.st_mode);return {'type':'file','mode':stat.S_IMODE(s.st_mode),'size':s.st_size,'sha256':sha(p)}
def inv(p):return {'.':entry(p),**{str(x.relative_to(p)):entry(x) for x in sorted(p.rglob('*'))}}
seal=json.loads((T/'seal.json').read_text());binding=json.loads((T/'binding.json').read_text());preflight=json.loads((T/'preflight.json').read_text());metadata=json.loads((OLD/'metadata.json').read_text())
assert sha(T/'binding.json')==seal['bindingSHA256'];assert not P.exists()
def frozen():
 assert cmd('git','rev-parse','HEAD').strip()==HEAD
 for root,key in [(S,'stage'),(B,'build')]:
  actual={str(x.relative_to(root)):sha(x) for x in sorted(root.rglob('*')) if x.is_file()};assert actual==seal[key]
 for p,v in metadata['guards'].items():assert entry(Path(p))==v
 for arc,v in metadata['sourceEntries'].items():
  if arc.startswith('dist367'):p=R/'dist'/arc.removeprefix('dist367').lstrip('/')
  elif arc.startswith('runtime230'):p=P.parent/'230/runtime230'/arc.removeprefix('runtime230').lstrip('/')
  elif arc=='node/bin/node':p=Path.home()/'.nvm/versions/node/v24.15.0/bin/node'
  elif arc=='policy/rach-doi-son-ha.service':p=Path.home()/'.config/systemd/user/rach-doi-son-ha.service'
  elif arc.startswith('policy/rach-doi-son-ha.service.d'):p=Path.home()/'.config/systemd/user/rach-doi-son-ha.service.d'/arc.removeprefix('policy/rach-doi-son-ha.service.d').lstrip('/')
  else:continue
  if v['type']=='symlink':assert p.is_symlink() and os.readlink(p)==v['target'] and stat.S_IMODE(p.lstat().st_mode)==v['mode']
  else:assert entry(p)==v
 assert sha(OLD/'rollback367.tar.gz')=='71653bffd2497de433fcebae4faf9a9e325d0f69fd0f80a671b04642e90f091e'
 pol=metadata['policy'];service=cmd('systemctl','--user','show','rach-doi-son-ha.service','-p','ActiveState','-p','MainPID','-p','WorkingDirectory','-p','FragmentPath','-p','DropInPaths','-p','EnvironmentFiles');assert service==pol['service']
 assert json.loads(cmd('curl','-fsS','http://127.0.0.1:3000/health'))['rooms']==0
 assert cmd('tailscale','serve','status','--json')==pol['funnel'];assert sha('/proc/3229/environ')==pol['environmentSHA256'] and sha('/proc/3229/cmdline')==pol['cmdlineSHA256']
frozen();source=inv(B);base=inv(R/'dist');files={n:v for n,v in source.items() if v['type']=='file'};old={n:v for n,v in base.items() if v['type']=='file'}
changed=[n for n in old if files[n]['sha256']!=old[n]['sha256']];added=sorted(set(files)-set(old));assert set(changed)=={'index.html','assets/art-v1/stone-361-manifest.json','assets/art-v1/fort-202-manifest.json'}
chunk=re.search(r'src="/([^\"]+\.js)"',(B/'index.html').read_text()).group(1)
assert set(added)=={chunk,'assets/art-v1/gate-245/idle.png','assets/art-v1/gate-252/idle.png','assets/art-v1/stone-wall-construction-373/runtime.png'}
assert len(files)==200 and not any('food-099' in n or 'wall-collapse-321' in n for n in files)
rows={}
for n,c in [('stone-361',16),('fort-202',45)]:
 m=json.loads((B/f'assets/art-v1/{n}-manifest.json').read_text());assert len(m['assets'])==c
 gates=[x for x in m['assets'] if 'gate-' in x['id']];assert len(gates)==7;rows[n]=gates
assert rows['stone-361']==rows['fort-202']
for x in preflight['retainedCurrent367ChunksCSS']:assert sha(B/x['path'].removeprefix('public/'))==x['sha256']
P.mkdir(mode=0o700);archive=P/'candidate379.tar.gz'
with tarfile.open(archive,'w:gz',dereference=False) as t:t.add(B,arcname='dist379')
archive.chmod(0o600);proof=P/'candidate-verified';proof.mkdir(mode=0o700);modes=[]
def safe(m,d):
 assert m.name=='dist379' or m.name.startswith('dist379/');rel='.' if m.name=='dist379' else m.name[len('dist379/'):];v=source[rel]
 assert m.mode==v['mode'] and m.mode<=0o777 and (m.isfile() or m.isdir()) and '..' not in Path(m.name).parts
 f=tarfile.data_filter(m,d);assert f.name==m.name;modes.append({'name':m.name,'storedMode':m.mode,'dataFilterMode':f.mode,'extractedMode':m.mode});return f.replace(mode=m.mode,deep=False)
with tarfile.open(archive) as t:
 members=t.getmembers();assert len({m.name for m in members})==len(members)==len(source)
 t.extractall(proof,filter=safe)
assert inv(proof/'dist379')==source;frozen()
dump(Q/'mode-proof.json',modes)
dump(Q/'binding.json',{'sourceHEAD':HEAD,'seal379SHA256':sha(T/'seal.json'),'binding379SHA256':sha(T/'binding.json'),'stage':str(S),'build':str(B),'sourceInventory':source,'baseInventory':base,'changed':changed,'added':added,'originalGateRows':rows,'commonCodePins':{n:seal['stage'][n] for n in ['client/wood-gate.js','client/renderer.js','client/fortification-picking.js','client/fortification-art.js']}})
receipt={'order':381,'status':'PREPARED_AWAIT_ROOT_FULL379_ACTUALSCENEINTAKE_AND_PUBLICATIONGO','sourceHEAD':HEAD,'candidateArchive':str(archive),'candidateSHA256':sha(archive),'files':200,'defaultCount':16,'fortCount':45,'gateRows':7,'newChunk':chunk,'newChunkSHA256':sha(B/chunk),'HTMLSHA256':sha(B/'index.html'),'requiredResponsePins':{n:sha(B/n) for n in ['index.html',chunk,'assets/index-Dx0ueiQl.css','assets/art-v1/stone-361-manifest.json','assets/art-v1/fort-202-manifest.json','assets/art-v1/gate-245/idle.png','assets/art-v1/gate-252/idle.png','assets/art-v1/stone-wall-construction-373/runtime.png']},'pairedRollbackSHA256':sha(OLD/'rollback367.tar.gz'),'safeExactModesPASS':True,'preservationPASS':True,'pid':3229,'rooms':0,'buildBrowserImagePublicationRestartCalls':0,'publicApproval':False,'handles':'CLOSED'}
dump(Q/'receipt.json',receipt);print(json.dumps(receipt))
