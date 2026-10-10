from pathlib import Path
import json,hashlib,shutil,subprocess,urllib.request
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');Q=R/'docs/qa/wall-t-runtime-277';S=Path('/tmp/rds-wall-t277-stage');B=Path('/tmp/rds-wall-t277-build')
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def inv(p):return {str(f.relative_to(p)):h(f) for f in sorted(p.rglob('*')) if f.is_file()}
def write(n,v):(Q/n).write_text(json.dumps(v,indent=2)+'\n')
go=json.loads((Q/'root-go.json').read_text());assert go['runGO'] is True and go['275IntakeAccepted'] is True
assert not S.exists() and not B.exists();assert S.resolve()==Path('/tmp/rds-wall-t277-stage') and B.resolve()==Path('/tmp/rds-wall-t277-build')
svc=subprocess.check_output(['systemctl','--user','show','rach-doi-son-ha.service','-p','MainPID','-p','WorkingDirectory','-p','ActiveState'],text=True);(Q/'service-before.txt').write_text(svc)
health=json.load(urllib.request.urlopen('http://127.0.0.1:3000/health'));assert health=={'ok':True,'rooms':0}
canonical={n:inv(R/n) for n in ['client','shared','server','public']};public=inv(R/'dist');assert len(public)==195
write('preservation-before.json',{'canonical':canonical,'public':public,'sourceHEAD':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'health':health})
S.mkdir()
for n in canonical:shutil.copytree(R/n,S/n)
for n in ['index.html','package.json','package-lock.json','vite.config.js']:shutil.copy2(R/n,S/n)
(S/'node_modules').symlink_to(R/'node_modules',target_is_directory=True)
route=S/'client/art-routes.js';text=route.read_text();food=" food:Object.freeze({manifestUrl:'/assets/art-v1/food-099-manifest.json',world:false}),\n";assert text.count(food)==1;route.write_text(text.replace(food,''))
removed={}
for n in ['assets/art-v1/food-099-manifest.json','assets/art-v1/food-099/atlas.png']:f=S/'public'/n;removed[n]=h(f);f.unlink()
mp=S/'public/assets/art-v1/fort-202-manifest.json';prior=json.loads(mp.read_text());assert len(prior['assets'])==46;m=json.loads(mp.read_text());write('prior46.json',prior)
for mask,cp in [(7,274),(11,275)]:
 p=R/f'docs/art/buildings/wall-t{mask}-idle-{cp}';a=json.loads((p/'candidate.json').read_text());assert a['fortification']=={'mask':mask};assert a['pivot']=={'x':627,'y':900,'space':'source'};assert a['render']=={'width':42.3225,'height':42.3225};assert h(p/'raw.png')==a['source']['sha256'];assert h(p/'runtime.png')==a['runtime']['sha256']
 a['source']['path']=str((p/'raw.png').relative_to(R));a['runtime']['path']=f'wall-t{mask}-{cp}/idle.png';dest=S/'public/assets/art-v1'/a['runtime']['path'];dest.parent.mkdir();shutil.copy2(p/'runtime.png',dest);m['assets'].append(a)
assert m['assets'][:46]==prior['assets'];assert len(m['assets'])==48;mp.write_text(json.dumps(m,indent=2)+'\n')
assert (S/'vite.config.js').read_bytes()==(R/'vite.config.js').read_bytes()
write('binding.json',{'rootAuthorized':True,'runGO':True,'stage':str(S),'build':str(B),'config':str(S/'vite.config.js'),'sourceHEAD':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'canonical':canonical,'stageInventories':{n:inv(S/n) for n in canonical},'removedPendingFood':removed,'manifestSHA256':h(mp),'descriptors':48,'bundleSHA256':'add2b4e819d43aff69360158ef7d0b867a078730a4c53135d1a5f5d8ced49e64'})
print('Prepared isolated48; NO build performed')
