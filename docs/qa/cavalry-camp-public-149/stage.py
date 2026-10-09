from pathlib import Path
import json,shutil,hashlib
out=Path(__file__).resolve().parent; root=out.parents[2]
a=json.loads((out/'dispatch.json').read_text()); assert a['status']=='AUTHORIZED_FINITE_PUBLIC149'
assert a['expectedCampAssets']==26; assert a['expectedOldSHA']=='7f85447da25868ab62a0a473e73d6f9a857c4faa0677c877738a7b2e20425676'
assert a['rootSceneIntakeStatus']=='ACCEPTED_TERMINAL148'
assert a['localProofStatus']=='PASS_ACTUAL_CAMP_BUILD_QUEUE_SPAWN_GROUP_STOP'
assert a['approvedSourcePins'] and a['approvedHelperPins']
for rel,h in a['approvedHelperPins'].items():
 assert hashlib.sha256((root/rel).read_bytes()).hexdigest()==h,rel
src=Path(a['approvedSourceStage']).resolve();
actual={str(f.relative_to(src)) for folder in ['client','shared','server','public'] for f in (src/folder).rglob('*') if f.is_file()}
assert actual==set(a['approvedSourcePins']), 'Incomplete frozen source inventory'
for rel,h in a['approvedSourcePins'].items(): assert hashlib.sha256((src/rel).read_bytes()).hexdigest()==h,rel
stage=out/'source-stage'; assert not stage.exists()
shutil.copytree(src,stage,ignore=shutil.ignore_patterns('node_modules','dist','.git'))
r=stage/'client/raster-slice.js'; before=r.read_text()
a1="['pilot','walk','work','food','terrain','iron','workshop','camp']"; a2="['pilot','walk','work','terrain','iron','workshop','camp']"
branch="new URLSearchParams(globalThis.location?.search||'').get('art')==='food'?'/assets/art-v1/food-099-manifest.json':"
assert before.count(a1)==1 and before.count(branch)==1
r.write_text(before.replace(a1,a2).replace(branch,''))
removed=[]
for rel in ['public/assets/art-v1/food-099-manifest.json','public/assets/art-v1/food-099/atlas.png']:
 q=stage/rel; assert q.is_file(); removed.append({'path':rel,'sha256':hashlib.sha256(q.read_bytes()).hexdigest()}); q.unlink()
rows=[]
for folder in ['client','shared','server','public']:
 for f in sorted((src/folder).rglob('*')):
  if f.is_file():
   rel=f.relative_to(src); q=stage/rel; rows.append({'path':str(rel),'approvedSHA':hashlib.sha256(f.read_bytes()).hexdigest(),'publicStageSHA':hashlib.sha256(q.read_bytes()).hexdigest() if q.exists() else None})
diff=[r for r in rows if r['approvedSHA']!=r['publicStageSHA']]
assert {r['path'] for r in diff}=={'client/raster-slice.js',*(r['path'] for r in removed)}
(out/'source-bindings.json').write_text(json.dumps({'status':'PUBLIC_SCOPE_EXCLUSIONS_EXPLICIT','source':str(src),'stage':str(stage),'changes':diff,'bindings':rows},indent=2)+'\n')
print(stage)
