from pathlib import Path
import shutil,json,hashlib,subprocess,urllib.request,re
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');O=R/'docs/qa/unit-scale-runtime-426';S=Path('/tmp/rds-unit-scale426-stage');B=Path('/tmp/rds-unit-scale426-build')
def inv(p):return {str(f.relative_to(p)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(p.rglob('*')) if f.is_file() and not f.is_symlink()}
def preserve():return {'HEAD':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'canonical':{n:inv(R/n) for n in ['client','shared','server','public']},'public':inv(R/'dist'),'backend':inv(Path('/home/kieu-hoang-quan/.local/share/rach-doi-son-ha/releases/230/runtime230')),'pid':Path('/proc/3229/cmdline').read_bytes().hex(),'health':json.load(urllib.request.urlopen('http://127.0.0.1:3000/health'))}
p=preserve();assert p['HEAD']=='3a2ab48917d7fb7f3b50858e983037f4dbd44d5f';assert p['health']=={'ok':True,'rooms':0};assert len(p['public'])==207;assert not S.exists() and not B.exists();(O/'preservation-before.json').write_text(json.dumps(p,indent=2));S.mkdir()
for n in ['client','shared','server','public','tests']:shutil.copytree(R/n,S/n)
for n in ['index.html','vite.config.js','package.json','package-lock.json']:shutil.copy2(R/n,S/n)
(S/'node_modules').symlink_to(R/'node_modules',target_is_directory=True)
routes=S/'client/art-routes.js';routeSource=routes.read_text();manifestPaths=re.findall("manifestUrl:'([^']+)'",routeSource);assert len(set(manifestPaths))==11
changes=[];modified=[]
for rel in manifestPaths:
 f=S/'public'/rel.lstrip('/');m=json.loads(f.read_text());old=json.loads(f.read_text());updates=[]
 for a in m['assets']:
  if a.get('family') in ['villager','unit.villager']:
   before=a['render'].copy();a['render']={'width':42,'height':42};updates.append({'id':a['id'],'family':a['family'],'state':a['state'],'before':before,'after':a['render']})
  if rel.endswith('fort-202-manifest.json') and a['id']=='supply-wagon-horse-idle-d0-415':
   before=a['render'].copy();assert before=={'width':112,'height':112};a['render']={'width':84,'height':84};updates.append({'id':a['id'],'family':a['family'],'state':a['state'],'before':before,'after':a['render']})
 # Only render dimensions differ.
 for a,b in zip(m['assets'],old['assets']):assert {k:v for k,v in a.items() if k!='render'}=={k:v for k,v in b.items() if k!='render'}
 if updates:f.write_text(json.dumps(m,indent=2)+'\n');modified.append(rel.lstrip('/'));changes.append({'manifest':rel,'updates':updates})
 if 'food-099' in rel:(O/'local-food099-patched-custody.json').write_text(json.dumps(m,indent=2))
line=" food:Object.freeze({manifestUrl:'/assets/art-v1/food-099-manifest.json',world:false}),\n";assert line in routeSource;routes.write_text(routeSource.replace(line,''))
for n in ['assets/art-v1/food-099-manifest.json','assets/art-v1/food-099/atlas.png']:(S/'public'/n).unlink()
f=S/'client/world-presentation.js';text=f.read_text();assert text.count('NORMAL_ZOOM = 1.08')==1;f.write_text(text.replace('NORMAL_ZOOM = 1.08','NORMAL_ZOOM = 1.68'))
for rel,pin in p['public'].items():
 if rel=='index.html' or rel in modified:continue
 t=S/'public'/rel
 if t.exists():assert hashlib.sha256(t.read_bytes()).hexdigest()==pin,rel
 else:t.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/'dist'/rel,t)
assert preserve()==p
pre={'status':'PASS_PREBUILD426_WAIT_ROOT_BUILD','cwd':str(S),'outDir':str(B),'config':str(S/'vite.config.js'),'configSHA':hashlib.sha256((S/'vite.config.js').read_bytes()).hexdigest(),'activeManifestRenderChanges':changes,'solePresentationCodeChange':'NORMAL_ZOOM1.08→1.68','retainedPublic207':True,'expectedBuild208NewJS':True,'allPixelSourceRuntimePivotsTimingStrideUnchanged':True,'simulationUnchanged':True,'food099':'Patchedlocalmetadata retainedQA custody; publicrecipe/manifest/atlas excludedstageonly','modifiedPublicManifests':modified}
(O/'preflight.json').write_text(json.dumps(pre,indent=2));(O/'stage-inventory.json').write_text(json.dumps(inv(S),indent=2));print(json.dumps({'status':pre['status'],'cwd':str(S),'outDir':str(B),'configSHA':pre['configSHA'],'activeManifests':len(changes),'updatedRows':sum(len(x['updates']) for x in changes),'public207Retained':True}))
