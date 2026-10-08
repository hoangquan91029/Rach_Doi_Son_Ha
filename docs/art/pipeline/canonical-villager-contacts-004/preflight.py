from pathlib import Path
import importlib.util, json, hashlib
import numpy as np
ROOT=Path(__file__).resolve().parent
FROZEN=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha/docs/art/pipeline/deterministic-villager-003/model003.py')
REF=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha/docs/art/characters/villager-neutral-D07-screen-East-guided-007/raw.png')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
new=load('new_appearance',ROOT/'model-appearance-v1.py');old=load('frozen_003',FROZEN)
new.GEOMETRY_PREFLIGHT_ONLY=True
rows=[];bounds_ok=True;min_z=1e9;max_reach=0;pose_delta=0;motion_delta=0
for phase in np.linspace(0,1,501):
 p=new.pose(float(phase));q=old.pose(float(phase))
 for key,val in p['joints'].items():pose_delta=max(pose_delta,float(np.max(np.abs(val-q['joints'][key]))))
 for side in ('LEFT','RIGHT'):
  a=p['feet'][side];b=q['feet'][side]
  for key in ('toe','heel','ankle','worldToe'):
   motion_delta=max(motion_delta,float(np.max(np.abs(a[key]-b[key]))))
  if a['mode']!=b['mode'] or a['q']!=b['q']:motion_delta=1
 mesh=new.mesh_for(p);v=np.array(mesh.v);min_z=min(min_z,float(v[:,2].min()));world=np.array(v)@new.BASIS.T;proj=new.project_vertices(world);lo=proj[:,:2].min(axis=0);hi=proj[:,:2].max(axis=0);bounds_ok &= bool(np.all(lo>=0) and np.all(hi<256))
 for side in ('LEFT','RIGHT'):
  reach=float(np.linalg.norm(p['joints'][side+'_hip']-p['joints'][side+'_ankle']));max_reach=max(max_reach,reach)
 rows.append({'phase':float(phase),'meshMinZ':float(v[:,2].min()),'projectedBounds':lo.tolist()+hi.tolist()})
checks={'status':'READY_FOR_PARENT_PREFLIGHT_REVIEW' if min_z>=-1e-9 and max_reach<.85 and bounds_ok and pose_delta==0 and motion_delta==0 else 'FAILED_STOP_NO_RENDER','phaseSamples':501,'minMeshZ':min_z,'groundClearancePass':min_z>=-1e-9,'maxHipAnkleReach':max_reach,'wholeMeshCanvasBoundsPass':bounds_ok,'lockedJointPoseMaxDelta':pose_delta,'lockedFootLandmarkMaxDelta':motion_delta,'lockedMotionTracksEqual':pose_delta==0 and motion_delta==0,'clothSelfIntersection':'NOT SOLVED BY NUMERICAL PREFLIGHT; pending visual review at F0/F24 only','legOcclusion':'NOT SOLVED BY NUMERICAL PREFLIGHT; pending visual review at F0/F24 only','motionMetrics':'Pose/feet/mode/phase are byte-source-identical functions from frozen003; no cadence, gait, root, camera, pivot or scale edits.','inputs':{'frozenModel003':{'path':str(FROZEN),'sha256':sha(FROZEN)},'appearanceModel':{'path':str(ROOT/'model-appearance-v1.py'),'sha256':sha(ROOT/'model-appearance-v1.py')},'canonicalEastReference':{'path':str(REF),'sha256':sha(REF)},'animation003':{'path':str(Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha/docs/art/pipeline/deterministic-villager-003/animation.json')),'sha256':sha('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha/docs/art/pipeline/deterministic-villager-003/animation.json')}}}
(ROOT/'preflight.json').write_text(json.dumps(checks,indent=2)+'\n')
(ROOT/'preflight-501.csv').write_text('phase,minMeshZ,x0,y0,x1,y1\n'+'\n'.join(f"{r['phase']},{r['meshMinZ']},{','.join(map(str,r['projectedBounds']))}" for r in rows)+'\n')
print(json.dumps(checks,indent=2))
