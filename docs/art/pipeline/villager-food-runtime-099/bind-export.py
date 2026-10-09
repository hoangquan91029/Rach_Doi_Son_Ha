#!/usr/bin/env python3
"""Bind a complete parent-reviewed actual food export into an isolated stage only."""
import argparse,json,hashlib,shutil
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('export');p.add_argument('sequence');p.add_argument('stage');p.add_argument('--parent-reviewed',action='store_true',required=True);a=p.parse_args()
export=Path(a.export).resolve();stage=Path(a.stage).resolve();root=Path(__file__).resolve().parents[4]
assert stage.is_relative_to(Path('/tmp')) and stage!=root,'Owned isolated /tmp stage required'
sequence=json.loads(Path(a.sequence).read_text());keys=sequence['selectedKeys'];assert sorted(k['frame'] for k in keys)==list(range(8)),'Eight actual selected source frames required'
assert not sequence.get('uncalled') and not sequence.get('callOpen'),'Incomplete/open source order; historical held receipts remain preserved'
for k in keys:assert hashlib.sha256(Path(k['path']).read_bytes()).hexdigest()==k['sha256'],'Selected source custody mismatch'
m=json.loads((export/'manifest.json').read_text());food=[x for x in m['assets'] if x['state']=='gather_food'];assert len(food)==1;food=food[0];assert food['direction']==1 and food['kind']=='unit' and food['family']=='unit.villager' and len(food['frames'])==8
base=json.loads((stage/'public/assets/art-v1/gather-026-manifest.json').read_text());assert len(base['assets'])==17
shadow=food.get('contactShadow',{});assert shadow.get('mode')=='separate';old=next(x for x in base['assets'] if x['id']==shadow['assetId']);new=next(x for x in m['assets'] if x['id']==shadow['assetId']);assert old['runtime']['sha256']==new['runtime']['sha256'],'Shadow must reuse existing original raster'
src=export/food['runtime']['path'];assert hashlib.sha256(src.read_bytes()).hexdigest()==food['runtime']['sha256'];assert food['id'] not in {x['id'] for x in base['assets']}
dest=stage/'public/assets/art-v1/food-099';dest.mkdir(exist_ok=False);shutil.copy2(src,dest/'atlas.png');food['runtime']['path']='food-099/atlas.png';base['assets'].append(food);base['notes']+='; optional LOCAL food099 actual parent-reviewed source; no public/final approval';(stage/'public/assets/art-v1/food-099-manifest.json').write_text(json.dumps(base,indent=2))
print(json.dumps({'status':'BOUND_ACTUAL_EXPORT_ONLY','assets':len(base['assets']),'atlasSHA':food['runtime']['sha256'],'export':str(export),'stage':str(stage)}))
