from pathlib import Path
import hashlib,json,os,stat,shutil,subprocess,tarfile
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha'); Q=R/'docs/qa/stone-construction-public-377'; B=Path('/tmp/rds-stone377-build'); S=Path('/tmp/rds-stone377-stage'); P=Path('/home/kieu-hoang-quan/.local/share/rach-doi-son-ha/releases/377'); RT=Path('/home/kieu-hoang-quan/.local/share/rach-doi-son-ha/releases/230/runtime230')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n')
def inv(base):return {str(p.relative_to(base)):{'sha256':sha(p),'mode':stat.S_IMODE(p.stat().st_mode)} for p in sorted(Path(base).rglob('*')) if p.is_file() and not p.is_symlink()}
def cmd(*args):return subprocess.check_output(args,text=True)
assert cmd('git','rev-parse','HEAD').strip()=='e95c46c811b6f6bdd06f935fae57744d3c3e4251'
assert not B.exists() and not S.exists() and not P.exists()
base=inv(R/'dist'); assert len(base)==196
seal=json.loads((R/'docs/qa/stone-raster-route-fix-368/seal.json').read_text())
chunk='assets/index-eaEH6Li-.js';assert base[chunk]['sha256']=='1dd1e2694658bcb797e17dccdd5686cdf68ccd75adc07f780ec580c92bebd2e0'
relevant=[x for x in seal['stage'] if x.startswith(('client/','shared/')) and x!='client/art-routes.js']
for rel in relevant:assert sha(R/rel)==seal['stage'][rel],rel
assert sha(R/'dist'/chunk)==seal['build'][chunk]
old370=json.loads((R/'docs/qa/stone-public-runtime-370/preservation-before.json').read_text())
paths={x['path'] for x in old370['pins'] if Path(x['path']).exists()}
for folder in ['client','shared','server','public']:
 paths.update(str(p) for p in (R/folder).rglob('*') if p.is_file())
paths.update(str(p) for p in (R/'dist').rglob('*') if p.is_file())
paths.add('/home/kieu-hoang-quan/.nvm/versions/node/v24.15.0/bin/node')
pins=[{'path':p,'sha256':sha(p),'mode':stat.S_IMODE(Path(p).stat().st_mode)} for p in sorted(paths)]
service=cmd('systemctl','--user','show','rach-doi-son-ha.service','-p','ActiveState','-p','MainPID','-p','WorkingDirectory'); assert 'MainPID=3229' in service and 'ActiveState=active' in service
health=json.loads(cmd('curl','-fsS','http://127.0.0.1:3000/health'));assert health['rooms']==0
policy={'service':service,'funnel':cmd('tailscale','serve','status','--json'),'health':health,'cmdlineSHA256':sha('/proc/3229/cmdline'),'environmentSHA256':sha('/proc/3229/environ'),'runtimeDistLink':os.readlink(RT/'dist')}
dump(Q/'preservation-before.json',{'sourceHEAD':cmd('git','rev-parse','HEAD').strip(),'pins':pins,'policy':policy})
P.mkdir(mode=0o700);os.chmod(P,0o700)
shutil.copytree(R/'dist',B,copy_function=shutil.copy2);os.chmod(B,0o755)
S.mkdir(mode=0o755);shutil.copy2(R/'package.json',S/'package.json')
for folder in ['client','shared']:shutil.copytree(R/folder,S/folder,copy_function=shutil.copy2)
(S/'public/assets/art-v1').mkdir(parents=True)
changed=['assets/art-v1/stone-361-manifest.json','assets/art-v1/fort-202-manifest.json']; added='assets/art-v1/stone-wall-construction-373/runtime.png'
for rel in changed+[added]:
 src=R/'public'/rel; dst=B/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
 dst2=S/'public'/rel;dst2.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst2)
 tested=R/'docs/qa/stone-construction-runtime-374/source-copies/public'/rel
 if tested.exists():assert sha(src)==sha(tested)
for rel,count,oldcount in zip(changed,[9,38],[8,37]):
 new=json.loads((B/rel).read_text());old=json.loads((R/'dist'/rel).read_text());assert len(new['assets'])==count and len(old['assets'])==oldcount
 assert new['assets'][:-1]==old['assets'];assert new['assets'][-1]['id']=='stone-wall-construction-373'
 newWithout=dict(new);newWithout['assets']=new['assets'][:-1];assert newWithout==old
candidate=inv(B);assert len(candidate)==197 and set(candidate)-set(base)=={added}
assert {x for x in base if base[x]!=candidate[x]}==set(changed)
assert not (B/'assets/art-v1/food-099-manifest.json').exists();assert not (B/'assets/art-v1/runtime/wall-collapse-321-atlas.png').exists()
# Safe paired archive stores current front, immutable runtime including its declared dist link, executable and policy files.
rollback=P/'rollback367.tar.gz'
with tarfile.open(rollback,'w:gz') as t:
 t.add(R/'dist',arcname='dist367');t.add(RT,arcname='runtime230');t.add('/home/kieu-hoang-quan/.nvm/versions/node/v24.15.0/bin/node',arcname='node/bin/node')
 t.add('/home/kieu-hoang-quan/.config/systemd/user/rach-doi-son-ha.service',arcname='policy/rach-doi-son-ha.service');t.add('/home/kieu-hoang-quan/.config/systemd/user/rach-doi-son-ha.service.d',arcname='policy/rach-doi-son-ha.service.d')
 (P/'policy.json').write_text(json.dumps(policy,indent=2)+'\n');t.add(P/'policy.json',arcname='policy/current.json')
# Permit only pinned runtime dist symlink; data-filter extraction excludes it and verifies link separately.
extract=P/'rollback-verified';extract.mkdir()
with tarfile.open(rollback) as t:
 members=t.getmembers(); links=[m for m in members if m.issym() or m.islnk()]
 assert len(links)==1 and links[0].name=='runtime230/dist' and links[0].linkname==str(R/'dist')
 for m in members:assert not m.name.startswith('/') and '..' not in Path(m.name).parts and (m.isfile() or m.isdir() or m in links)
 t.extractall(extract,members=[m for m in members if m not in links],filter='data')
assert inv(extract/'dist367')==base;assert inv(extract/'runtime230')==inv(RT);assert sha(extract/'node/bin/node')==sha('/home/kieu-hoang-quan/.nvm/versions/node/v24.15.0/bin/node')
archive=P/'dist377.tar.gz'
with tarfile.open(archive,'w:gz') as t:t.add(B,arcname='dist377')
verify=P/'candidate-verified';verify.mkdir()
with tarfile.open(archive) as t:
 for m in t.getmembers():assert not m.name.startswith('/') and '..' not in Path(m.name).parts and (m.isfile() or m.isdir())
 t.extractall(verify,filter='data')
assert inv(verify/'dist377')==candidate
binding={'order':377,'rootAuthorized':True,'sourceSelected':True,'root':str(R),'sourceHEAD':cmd('git','rev-parse','HEAD').strip(),'stage':str(S),'build':str(B),'stagePins':{x:v['sha256'] for x,v in inv(S).items()},'buildPins':{x:v['sha256'] for x,v in candidate.items()},'bundleSHA256':base[chunk]['sha256'],'constructionAssetId':'stone-wall-construction-373','completedAssetId':'stone-wall-X-362-mask0','preservationPins':pins,'policy':policy,'candidateInventory':candidate,'baseInventory':base}
dump(Q/'binding.json',binding)
dump(Q/'seal.json',{'status':'SEALED377_BEFORE_ONE_FIREFOX','build':candidate,'stage':inv(S),'rootMode':stat.S_IMODE(B.stat().st_mode),'dataOnlyChanges':changed,'added':[added],'published368RelevantSourcePinsEqualCanonical':relevant,'publicRoutesUnchangedPendingFoodExcluded':True,'noRebuild':True,'candidateArchive':str(archive),'candidateArchiveSHA256':sha(archive),'rollbackArchive':str(rollback),'rollbackArchiveSHA256':sha(rollback),'safeDataFilterExtractPASS':True,'rollbackSymlink':{'name':links[0].name,'target':links[0].linkname,'extractionExcludedAssertInstead':True}})
print(json.dumps({'status':'SEALED377','files':len(candidate),'rollbackSHA256':sha(rollback),'candidateSHA256':sha(archive),'preservationPins':len(pins)}))
