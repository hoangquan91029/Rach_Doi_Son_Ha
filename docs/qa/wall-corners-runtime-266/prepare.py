from pathlib import Path
import json,hashlib,shutil,subprocess,urllib.request
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');Q=R/'docs/qa/wall-corners-runtime-266';S=Path('/tmp/rds-corners266-stage');B=Path('/tmp/rds-corners266-build')
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def inv(p):return {str(f.relative_to(p)):h(f) for f in sorted(p.rglob('*')) if f.is_file()}
def write(n,v):(Q/n).write_text(json.dumps(v,indent=2)+'\n')
assert not S.exists() and not B.exists();S.mkdir()
svc=subprocess.check_output(['systemctl','--user','show','rach-doi-son-ha.service','-p','MainPID','-p','WorkingDirectory','-p','ActiveState'],text=True);assert 'MainPID=575363' in svc;(Q/'service-before.txt').write_text(svc)
assert json.load(urllib.request.urlopen('http://127.0.0.1:3000/health'))=={'ok':True,'rooms':0}
canonical={n:inv(R/n) for n in ['client','shared','server','public']};public=inv(R/'dist');assert len(public)==192
write('preservation-before.json',{'canonical':canonical,'public':public,'sourceHEAD':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()})
for n in canonical:shutil.copytree(R/n,S/n)
for n in ['index.html','package.json','package-lock.json','vite.config.js']:shutil.copy2(R/n,S/n)
(S/'node_modules').symlink_to(R/'node_modules',target_is_directory=True)
route=S/'client/art-routes.js';text=route.read_text();food=" food:Object.freeze({manifestUrl:'/assets/art-v1/food-099-manifest.json',world:false}),\n";assert text.count(food)==1;route.write_text(text.replace(food,''))
removed={}
for n in ['assets/art-v1/food-099-manifest.json','assets/art-v1/food-099/atlas.png']:f=S/'public'/n;removed[n]=h(f);f.unlink()
mp=S/'public/assets/art-v1/fort-202-manifest.json';m=json.loads(mp.read_text());assert len(m['assets'])==43;prior=json.loads(mp.read_text());write('prior43.json',prior)
for mask,cp in [(6,263),(9,264),(10,265)]:
 p=R/f'docs/art/buildings/wall-corner{mask}-idle-{cp}';a=json.loads((p/'candidate.json').read_text());assert a['fortification']=={'mask':mask};assert a['pivot']=={'x':627,'y':900,'space':'source'};assert a['render']=={'width':42.3225,'height':42.3225};assert h(p/'raw.png')==a['source']['sha256'];assert h(p/'runtime.png')==a['runtime']['sha256']
 a['source']['path']=str((p/'raw.png').relative_to(R));a['runtime']['path']=f'corner-{cp}/idle.png';dest=S/'public/assets/art-v1'/a['runtime']['path'];dest.parent.mkdir();shutil.copy2(p/'runtime.png',dest);m['assets'].append(a)
assert m['assets'][:43]==prior['assets'];assert len(m['assets'])==46;mp.write_text(json.dumps(m,indent=2)+'\n')
write('binding.json',{'rootAuthorized':True,'stage':str(S),'build':str(B),'config':str(S/'vite.config.js'),'sourceHEAD':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'canonical':canonical,'stageInventories':{n:inv(S/n) for n in canonical},'removedPendingFood':removed,'manifestSHA256':h(mp),'assets':46,'bundleSHA256':'add2b4e819d43aff69360158ef7d0b867a078730a4c53135d1a5f5d8ced49e64'})
assert S.resolve()==Path('/tmp/rds-corners266-stage');assert B.resolve()==Path('/tmp/rds-corners266-build');assert (S/'vite.config.js').read_bytes()==(R/'vite.config.js').read_bytes()
print('Prepared isolated46 candidate; path/config assertions passed')
