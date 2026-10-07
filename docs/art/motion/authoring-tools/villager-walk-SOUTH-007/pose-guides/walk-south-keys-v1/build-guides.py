"""MODEL_ONLY numerical pose hypotheses. No reference pixels, art edits or animation export."""
import math,json,pathlib,hashlib
P=pathlib.Path(__file__).parent
REFERENCE=pathlib.Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha/docs/art/characters/villager-neutral-D01-screen-South-007/raw.png')
assert hashlib.sha256(REFERENCE.read_bytes()).hexdigest()=='68a7fb9a71ae614f7c01432b1270e7a25071975667cfdf082ae02326d97678db'
ROOT=(654,1140); BASE_D=-100; THIGH=260; SHIN=240; ARM=200; FOREARM=180
# Metric authoring coordinates x (viewer right), d (forward camera depth), z (up).
# South forward=(0,+1); anatomical LEFT=(forward.d,-forward.x)=(+1,0).
# Affine game ground projection, NOT a calibrated physical perspective camera.
def project(q):x,d,z=q;return [ROOT[0]+x,ROOT[1]+.5*d-z]
def ik(hip,ankle,a,b,pole=1):
 x,d,z=hip;_,ad,az=ankle;dd=ad-d;dz=az-z;r=math.hypot(dd,dz)
 assert abs(a-b)<r<a+b,('unreachable',r)
 u=(dd/r,dz/r);along=(a*a-b*b+r*r)/(2*r);height=math.sqrt(a*a-along*along)
 # Perpendicular oriented toward +depth for readable knee flexion.
 n=(-u[1]*pole,u[0]*pole)
 return [x,d+u[0]*along+n[0]*height,z+u[1]*along+n[1]*height]
def distance(a,b):return math.dist(a,b)
# Reach envelope first: max hip-to-ankle vertical separation is440; safe forward excursion160.
# This is deliberately below sqrt(500^2-440^2)=237.49; choose160 with margin.
EXCURSION=160; TRAVEL_D=EXCURSION*4; PERIOD=600
frames=[]
for index,time,support,passing in [(0,0,'LEFT',False),(2,150,'LEFT',True),(4,300,'RIGHT',False),(6,450,'RIGHT',True)]:
 phase=(time%300)/300;pelvis_z=500 if passing else 480;pts={};soles={};lengths={}
 for side,x in [('LEFT',100),('RIGHT',-100)]:
  planted=side==support;local_d=BASE_D+EXCURSION-TRAVEL_D*phase*.5 if planted else (BASE_D if passing else BASE_D-EXCURSION)
  ankle_z=60 if planted else (140 if passing else 72)
  hip=[x,BASE_D,pelvis_z];ankle=[x,local_d,ankle_z];knee=ik(hip,ankle,THIGH,SHIN)
  # Foot is a fixed160-depth-long sole, groundoffset60 below ankle. No per-frame scaling.
  heel=[x,local_d-50,ankle_z-60];toe=[x,local_d+110,ankle_z-60]
  pts.update({side+'_hip':hip,side+'_knee':knee,side+'_ankle':ankle,side+'_heel':heel,side+'_toe':toe})
  arm_sign=-1 if side==support else 1;arm_swing=0 if passing else arm_sign*110
  shoulder=[x*1.8,BASE_D,pelvis_z+310];wrist=[x*1.9,BASE_D+arm_swing,pelvis_z-20]
  elbow=ik(shoulder,[shoulder[0],wrist[1],wrist[2]],ARM,FOREARM,pole=-arm_sign)
  wrist[0]=shoulder[0] # Arm constraints are solved in a constant x sagittal plane.
  pts.update({side+'_shoulder':shoulder,side+'_elbow':elbow,side+'_wrist':wrist})
  lengths[side]={'thigh':distance(hip,knee),'shin':distance(knee,ankle),'upperArm':distance(shoulder,elbow),'forearm':distance(elbow,wrist)}
  soles[side]={'planted':planted,'heightAboveGround':ankle_z-60,'axis':[0,160,0],'worldHeel':[heel[0],heel[1]+TRAVEL_D*time/PERIOD,heel[2]],'worldToe':[toe[0],toe[1]+TRAVEL_D*time/PERIOD,toe[2]]}
 for side in ['LEFT','RIGHT']:
  for name,expected in [('thigh',THIGH),('shin',SHIN),('upperArm',ARM),('forearm',FOREARM)]:assert abs(lengths[side][name]-expected)<1e-8
  assert soles[side]['planted']==(side==support)
  assert soles[side]['heightAboveGround']==0 if side==support else soles[side]['heightAboveGround']>0
 frames.append({'frame':index,'timeMs':time,'support':support,'swing':'RIGHT' if support=='LEFT' else 'LEFT','passing':passing,'pelvisZ':pelvis_z,'bodyTravelDepth':TRAVEL_D*time/PERIOD,'points3D':pts,'points2D':{k:project(v) for k,v in pts.items()},'soles':soles,'lengths':lengths})
# Full eight-phase contact diagnostic, not authored frames. Each support sole remains stationary inworld.
contact=[]
for frame,time in enumerate([0,80,150,230,300,380,450,530,600]):
 support='LEFT' if time%600<300 else 'RIGHT';half=math.floor(time/300);local=BASE_D+EXCURSION-TRAVEL_D*((time%300)/PERIOD);world=local+TRAVEL_D*time/PERIOD
 contact.append({'frame':frame if frame<8 else 'SEAM_F0','timeMs':time,'support':support,'rootWorldDepth':TRAVEL_D*time/PERIOD,'localAnkleDepth':local,'worldAnkleDepth':world,'contactZ':0,'expectedSupportWorldDepth':BASE_D+EXCURSION+TRAVEL_D*half*.5})
 for_check=BASE_D+EXCURSION+TRAVEL_D*half*.5;assert abs(world-for_check)<1e-8
source_stride=TRAVEL_D*.5;logical_stride=source_stride*38/1254;world_stride=logical_stride/(27/math.sqrt(2));base_period=world_stride/2.1*1000
plan={'status':'MODEL_ONLY_NON_ART_NO_ANIMATION_QUALIFICATION','canvas':[1254,1254],'root':list(ROOT),'wholeCanvasLogicalSize':38,'direction':{'screen':'South','engine':1,'world':'SE','forwardLocal':[0,1],'anatomicalLeftAxis':[1,0],'anatomicalLeftViewer':'RIGHT'},'projection':'screen=(654+x,1140+0.5*depth-z); locked game2:1 affine ground;26.565deg ground-slope convention, not physically calibrated camera','sourceReference':{'path':'/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha/docs/art/characters/villager-neutral-D01-screen-South-007/raw.png','sha256':'68a7fb9a71ae614f7c01432b1270e7a25071975667cfdf082ae02326d97678db','usage':'inspected gross proportions only; no tracing/copied pixels/extraction'},'hiddenJoints':{'status':'AUTHORED_HYPOTHESES_NOT_MEASURED_ANATOMY','hipSourceApprox':[554,610,754,610],'uncertaintySourcePx':60,'kneePole':'forward depth','segmentLengths3D':{'thigh':THIGH,'shin':SHIN,'upperArm':ARM,'forearm':FOREARM},'feet':{'soleDepth':160,'soleWidth':64,'ankleToSoleHeight':60}},'reach':{'maxVerticalSeparation':440,'theoreticalMaxDepthExcursion':math.sqrt(500**2-440**2),'selectedDepthExcursion':EXCURSION,'maxSelectedHipAnkleDistance':math.hypot(440,160),'legMaxReach':500},'strideHypothesis':{'fullCycleModelDepth':TRAVEL_D,'fullCycleSourceProjectedPixels':source_stride,'fullCycleLogicalPixels':logical_stride,'euclideanWorldStride':world_stride,'nominalReviewPeriodMs':600,'nominalReviewWorldSpeed':world_stride/.6,'baseVillagerWorldSpeed':2.1,'distanceLockedBasePeriodMs':base_period,'nominalPreviewDoesNotMatchBaseSpeed':True,'modifiers':'eventual cycle rate uses actual traversed Euclidean distance including terrain/supply speed effects; no runtime integration','calibrationGate':'This reachable model stride is a hypothesis only; real illustrated contact tracks and grid playback must be judged before cadence is sealed.'},'clothOcclusionHypothesis':'Front tunic/skirt covers pelvis and proximal upper thighs; knee/shin and both feet remain readable. Anatomical axes never swap behind cloth. Arm order can change by depth but not identity. No per-frame whole-image fit, body bob derives from support hip height.','frames':frames,'contactTable':contact,'eightStaticIdentityGate':'INCOMPLETE_CLOSED_FOR_FINISHED_FRAME_CALLS','imageCalls':0,'finishedArt':False,'motionQualified':False,'runtimeIntegrated':False}
(P/'coordinate-plan.json').write_text(json.dumps(plan,indent=2)+'\n')
(P/'contact-table.json').write_text(json.dumps(contact,indent=2)+'\n')

def svg(frame,qa=False):
 p=frame['points2D'];bob=frame['pelvisZ']-480;e=['<rect width="1254" height="1254" fill="#f2efe5"/>',f'<text x="30" y="30" font-family="sans-serif" font-size="20" fill="#294b42">MODEL_ONLY / NON_ART — SOUTH F{frame["frame"]} — {frame["timeMs"]}ms</text>','<path d="M430 1140L654 1028L878 1140L654 1252Z" fill="none" stroke="#bcc7ba" stroke-dasharray="8 8"/>','<path d="M644 1140h20M654 1130v20" stroke="#667c69" stroke-width="2"/>']
 # Coarse mannequin capsules, not illustration/identity pixels.
 colors={'LEFT':'#64877b','RIGHT':'#a0aca1'}
 def limb(side,a,b,width):
  pa,pb=p[side+'_'+a],p[side+'_'+b];return f'<path d="M{pa[0]} {pa[1]}L{pb[0]} {pb[1]}" stroke="{colors[side]}" stroke-width="{width}" stroke-linecap="round"/>'
 for side in ['RIGHT','LEFT']:
  e.extend([limb(side,'hip','knee',85),limb(side,'knee','ankle',52)])
  heel,toe=p[side+'_heel'],p[side+'_toe'];x=heel[0];e.append(f'<path d="M{x-32} {heel[1]}L{x-29} {heel[1]-23}L{x+29} {heel[1]-23}L{x+32} {toe[1]-15}Q{x} {toe[1]} {x-32} {toe[1]-15}Z" fill="{colors[side]}" stroke="#3f5b50" stroke-width="3"/>')
  e.append(f'<path d="M{x} {heel[1]}L{x} {toe[1]}" stroke="#435f4c" stroke-width="2"/>')
 # Front silhouette with coat skirt blocks proximal legs, not the actual reference costume.
 e.extend([f'<path d="M490 {300-bob}Q654 {245-bob} 818 {300-bob}L799 {520-bob}L764 {610-bob}L830 {795-bob}Q740 {835-bob} 654 {805-bob}Q565 {835-bob} 478 {795-bob}L544 {610-bob}L509 {520-bob}Z" fill="#ccd1bf" stroke="#466352" stroke-width="4"/>',f'<path d="M544 {595-bob}Q654 {620-bob} 764 {595-bob} M654 {622-bob}L654 {805-bob}" stroke="#6e7c65" stroke-width="11" fill="none"/>'])
 for side in ['RIGHT','LEFT']:e.extend([limb(side,'shoulder','elbow',60),limb(side,'elbow','wrist',35)])
 # Explicit front head, no identity reconstruction.
 e.extend([f'<ellipse cx="654" cy="{210-bob}" rx="88" ry="105" fill="#adbfae" stroke="#466352" stroke-width="4"/>',f'<path d="M486 {145-bob}L654 {50-bob}L822 {145-bob}Q654 {190-bob} 486 {145-bob}Z" fill="#cad0b7" stroke="#466352" stroke-width="4"/>',f'<circle cx="619" cy="{207-bob}" r="5" fill="#466352"/><circle cx="689" cy="{207-bob}" r="5" fill="#466352"/>',f'<path d="M654 {213-bob}v27m-22 20h44" stroke="#466352" stroke-width="4" fill="none"/>'])
 e.append(f'<text x="30" y="75" font-family="sans-serif" font-size="18" fill="#294b42">SUPPORT {frame["support"]} (viewer {"RIGHT" if frame["support"]=="LEFT" else "LEFT"}) / SWING {frame["swing"]}</text>')
 e.append('<text x="30" y="103" font-family="sans-serif" font-size="16" fill="#294b42">Root654,1140 • fixed geometry • hidden-joint hypotheses • no art/motion qualification</text>')
 if qa:
  for side,x in [('RIGHT',180),('LEFT',980)]:
   ankle=p[side+'_ankle'];gap=frame['soles'][side]['heightAboveGround'];label=side+(' SUPPORT z0' if side==frame['support'] else f' SWING gap{gap}px')
   e.append(f'<text x="{x-100}" y="960" font-family="sans-serif" font-size="22" fill="#873e39">{label}</text><path d="M{x} 970L{ankle[0]} {ankle[1]}" stroke="#873e39" stroke-width="2"/>')
   # Numerical joints appear only on QA output; never a finished-art guide promise.
   for joint in ['hip','knee','ankle']:
    q=p[side+'_'+joint];e.append(f'<circle cx="{q[0]}" cy="{q[1]}" r="6" fill="#873e39"/>')
 return '<svg xmlns="http://www.w3.org/2000/svg" width="1254" height="1254" viewBox="0 0 1254 1254">'+''.join(e)+'</svg>'
for f in frames:
 for qa in [False,True]:(P/f'F{f["frame"]}{"-qa" if qa else ""}.svg').write_text(svg(f,qa))
print(json.dumps(plan['strideHypothesis'],indent=2));print('PASS fixed bone lengths / support contact / stance counter-travel / eight-phase numerical table; NON_ART only')
