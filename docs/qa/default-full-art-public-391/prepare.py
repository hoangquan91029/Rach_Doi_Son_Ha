from pathlib import Path
import hashlib,json,stat,os,subprocess,tarfile,shutil,re
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');Q=R/'docs/qa/default-full-art-public-391';P=Path.home()/'.local/share/rach-doi-son-ha/releases/391';OLD=P.parent/'390';T=R/'docs/qa/default-full-art-runtime-389';B=Path('/tmp/rds-fullart389-build');S=Path('/tmp/rds-fullart389-stage');NEXT=R.parent/'rds-public391-next-dist';HEAD='2b16979393716bc056e205f8fc50eaea07db0593'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def cmd(*a):return subprocess.check_output(a,text=True)
def entry(p):
 s=p.lstat();m=stat.S_IMODE(s.st_mode);assert m<=0o777
 if p.is_symlink():return {'type':'symlink','mode':m,'target':os.readlink(p)}
 if p.is_dir():return {'type':'directory','mode':m}
 assert stat.S_ISREG(s.st_mode);return {'type':'file','mode':m,'size':s.st_size,'sha256':sha(p)}
def inv(p):return {'.':entry(p),**{str(x.relative_to(p)):entry(x) for x in sorted(p.rglob('*'))}}
def filepins(p):return {n:{'sha256':v['sha256'],'mode':oct(v['mode'])} for n,v in inv(p).items() if v['type']=='file'}
binding=json.loads((T/'binding.json').read_text());meta=json.loads((OLD/'metadata.json').read_text());pre=json.loads((T/'preflight.json').read_text());assert binding['immutableSealed'] and pre['default']=='fort' and pre['world'] is True and pre['assets']==45
assert not P.exists() and not NEXT.exists();initialBinding=sha(T/'binding.json');source=inv(B);base=inv(R/'dist');canonical={str(p):entry(p) for f in ['client','shared','server','public'] for p in (R/f).rglob('*') if p.is_file()}
def frozen():
 assert cmd('git','rev-parse','HEAD').strip()==HEAD and sha(T/'binding.json')==initialBinding
 assert filepins(S)==binding['sourcePins'] and filepins(B)==binding['buildPins']
 for p,v in canonical.items():assert entry(Path(p))==v,p
 assert sha(OLD/'rollback382.tar.gz')=='897f3408b0b442e369deafc1c3fe9a0f8a7ddf7dda85f59ecc695d260c626295'
 for arc,v in meta['sourceEntries'].items():
  if arc.startswith('dist382'):p=R/'dist'/arc.removeprefix('dist382').lstrip('/')
  elif arc.startswith('runtime230'):p=P.parent/'230/runtime230'/arc.removeprefix('runtime230').lstrip('/')
  elif arc=='node/bin/node':p=Path.home()/'.nvm/versions/node/v24.15.0/bin/node'
  elif arc=='policy/rach-doi-son-ha.service':p=Path.home()/'.config/systemd/user/rach-doi-son-ha.service'
  elif arc.startswith('policy/rach-doi-son-ha.service.d'):p=Path.home()/'.config/systemd/user/rach-doi-son-ha.service.d'/arc.removeprefix('policy/rach-doi-son-ha.service.d').lstrip('/')
  else:continue
  assert entry(p)==v
 pol=meta['policy'];assert cmd('systemctl','--user','show','rach-doi-son-ha.service','-p','ActiveState','-p','MainPID','-p','WorkingDirectory','-p','FragmentPath','-p','DropInPaths','-p','EnvironmentFiles')==pol['service'];assert cmd('tailscale','serve','status','--json')==pol['funnel'];assert sha('/proc/3229/environ')==pol['environmentSHA256'] and sha('/proc/3229/cmdline')==pol['cmdlineSHA256'];assert json.loads(cmd('curl','-fsS','http://127.0.0.1:3000/health'))['rooms']==0
 for p,v in meta['guards'].items():assert entry(Path(p))==v
frozen();files={n:v for n,v in source.items() if v['type']=='file'};old={n:v for n,v in base.items() if v['type']=='file'};added=sorted(set(files)-set(old));changed=[n for n in old if files[n]!=old[n]]
assert len(files)==201 and len(old)==200 and added==[binding['bundle']] and changed==['index.html'];assert binding['bundleSHA256']=='352a4aa4ae36f2a6d44c5d073298a4056438a050414f9703e045d5317c39de61'
assert not any('food-099' in n or 'wall-collapse-321' in n for n in files)
P.mkdir(mode=0o700);archive=P/'candidate389.tar.gz'
with tarfile.open(archive,'w:gz',dereference=False) as t:t.add(B,arcname='dist389')
archive.chmod(0o600);proof=P/'candidate-verified';proof.mkdir(mode=0o700);modes=[]
def safe(m,d):
 assert m.name=='dist389' or m.name.startswith('dist389/');rel='.' if m.name=='dist389' else m.name[len('dist389/'):];v=source[rel]
 assert m.mode==v['mode'] and m.mode<=0o777 and (m.isfile() or m.isdir()) and '..' not in Path(m.name).parts
 f=tarfile.data_filter(m,d);assert f.name==m.name;modes.append({'name':m.name,'storedMode':m.mode,'dataFilterMode':f.mode,'extractedMode':m.mode});return f.replace(mode=m.mode,deep=False)
with tarfile.open(archive) as t:
 members=t.getmembers();assert len({m.name for m in members})==len(members)==len(source);t.extractall(proof,filter=safe)
assert inv(proof/'dist389')==source
shutil.copytree(B,NEXT,copy_function=shutil.copy2);NEXT.chmod(0o755);expected=dict(source);expected['.']={'type':'directory','mode':0o755};assert inv(NEXT)==expected;frozen()
dump(Q/'mode-proof.json',modes);dump(Q/'binding.json',{'sourceHEAD':HEAD,'binding389SHA256':initialBinding,'testedStage':str(S),'testedBuild':str(B),'sourceInventory':source,'currentBaseInventory':base,'canonicalPins':canonical,'changed':changed,'added':added})
receipt={'order':391,'status':'PREPARED_AWAIT_ROOT_FULL389_ACTUALSCENEINTAKE_AND_PUBLICATIONGO','sourceHEAD':HEAD,'candidateArchive':str(archive),'candidateSHA256':sha(archive),'files':201,'default':'fort','world':True,'assets':45,'newChunk':binding['bundle'],'newChunkSHA256':binding['bundleSHA256'],'pairedRollback390SHA256':sha(OLD/'rollback382.tar.gz'),'ownedNextClone':str(NEXT),'nextRootMode':0o755,'safeExactModesPASS':True,'preservationPASS':True,'pid':3229,'rooms':0,'buildBrowserImageExchangeRestartCalls':0,'publicApproval':False,'handles':'CLOSED','requiredResponsePins':{n:sha(B/n) for n in ['index.html',binding['bundle'],'assets/index-Dx0ueiQl.css','assets/art-v1/stone-361-manifest.json','assets/art-v1/fort-202-manifest.json','assets/art-v1/gate-245/idle.png','assets/art-v1/gate-252/idle.png','assets/art-v1/stone-wall-construction-373/runtime.png']}}
dump(Q/'receipt.json',receipt);print(json.dumps(receipt))
