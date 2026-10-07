"""Numerical MODEL_ONLY checks, never visual anatomy/contact qualification."""
import json,pathlib,math,hashlib
p=pathlib.Path(__file__).parent;j=json.loads((p/'coordinate-plan.json').read_text())
assert j['canvas']==[1254,1254] and j['root']==[654,1140]
assert j['direction']['anatomicalLeftAxis']==[1,0] and j['direction']['anatomicalLeftViewer']=='RIGHT'
assert j['eightStaticIdentityGate']=='INCOMPLETE_CLOSED_FOR_FINISHED_FRAME_CALLS'
assert not j['finishedArt'] and not j['motionQualified'] and not j['runtimeIntegrated'] and j['imageCalls']==0
for f in j['frames']:
 assert f['support']==('LEFT' if f['frame']<4 else 'RIGHT')
 for side,sign in [('LEFT',1),('RIGHT',-1)]:
  pts=f['points3D'];assert (f['points2D'][side+'_hip'][0]-654)*sign>0
  for a,b,size in [('hip','knee',260),('knee','ankle',240),('shoulder','elbow',200),('elbow','wrist',180)]:assert abs(math.dist(pts[side+'_'+a],pts[side+'_'+b])-size)<1e-8
  sole=f['soles'][side];assert sole['axis']==[0,160,0]
  assert sole['heightAboveGround']==(0 if side==f['support'] else 80 if f['passing'] else 12)
  for point in f['points2D'].values():assert 0<=point[0]<1254 and 0<=point[1]<1254
for first,second in [(j['frames'][0],j['frames'][1]),(j['frames'][2],j['frames'][3])]:
 side=first['support']
 for endpoint in ['worldHeel','worldToe']:assert math.dist(first['soles'][side][endpoint],second['soles'][side][endpoint])<1e-8
for row in j['contactTable']:assert abs(row['worldAnkleDepth']-row['expectedSupportWorldDepth'])<1e-8 and row['contactZ']==0
s=j['strideHypothesis'];assert abs(s['euclideanWorldStride']-s['fullCycleSourceProjectedPixels']*38/1254/(27/math.sqrt(2)))<1e-12
assert abs(s['distanceLockedBasePeriodMs']-s['euclideanWorldStride']/2.1*1000)<1e-10
assert s['euclideanWorldStride']<1 and s['nominalPreviewDoesNotMatchBaseSpeed']
r=j['sourceReference'];assert hashlib.sha256(pathlib.Path(r['path']).read_bytes()).hexdigest()==r['sha256']
print('PASS MODEL_ONLY: 4 keys, anatomical ownership, 16 fixed segment pairs, reachable IK, 8-phase+seam support counter-travel, source custody, honest cadence. NOT_ART/NOT_MOTION_QUALIFIED.')
