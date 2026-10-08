"""ONE bounded24 temporal experiment; pinned original001 mesh/rig/style/scale unchanged."""
import csv,hashlib,importlib.util,json,math,pathlib,sys
import numpy as np
from PIL import Image,ImageDraw
BASE=pathlib.Path(__file__).resolve().parent
OLD=BASE.parent/'deterministic-villager-001'
MODEL_SHA='b5c1472cce875cec649e8331b4f91da2bef64a7f57b910109a360ad727fb62e4'
META_SHA='ec9951436196c0f6208df8f2f20589531f0a216e482e06499369f6d08b88d530'
N=24;TARGETS=(64,80,96)
def sha(path):return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()
def model():
 if sha(OLD/'pilot.py')!=MODEL_SHA or sha(OLD/'animation.json')!=META_SHA:raise ValueError('frozen001 dependency changed')
 spec=importlib.util.spec_from_file_location('frozen_mesh_pilot001',OLD/'pilot.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

def phase_from_time(sec,m):
 # Distance phase and elapsed phase agree because stride/modelworldconversion/period are locked.
 traveled_world=m.WORLD_SPEED*sec;world_stride=m.STRIDE*m.GAME_PX_PER_MODEL/m.WORLD_PX_PER_UNIT
 return traveled_world/world_stride

def tracked_hold(sec,height,m):
 t=phase_from_time(sec,m);phase=t%1;fi=min(N-1,int(math.floor(phase*N)));sample=math.floor(t)+fi/N;live=m.pose(t);held=m.pose(sample);scale=height/m.REFERENCE_HEIGHT;zoom=height/80.;root=np.array([100+m.SCREEN_SPEED*zoom*sec,190.]);source_root=np.array([128.,237.])*scale;paste=np.round(root-source_root);rows=[]
 for side in ('LEFT','RIGHT'):
  lf=live['feet'][side];sf=held['feet'][side];target=m.project_vertices(m.local_world([lf['toe']]))[0,:2]*scale-source_root+root;actual=m.project_vertices(m.local_world([sf['toe']]))[0,:2]*scale+paste;coherent=lf['mode']!='SWING' and sf['mode']!='SWING' and lf['cycle']==sf['cycle'];analytic=abs(float((sf['toe'][1]+m.STRIDE*t)-lf['worldToe'][1]))*m.SOURCE_SCALE*scale
  rows.append({'timestampSec':sec,'targetHeight':height,'sceneZoom':zoom,'phase':phase,'distancePhase':t,'heldFrame':fi,'side':side,'mode':lf['mode'],'sameStanceContact':coherent,'analyticGroundSlipPx':analytic,'actualIntegerPasteGroundSlipPx':abs(float(actual[0]-target[0])),'floatEngineHeldToeErrorPx':abs(float(actual[0]-target[0]-(paste[0]-(root-source_root)[0]))),'frameAgeMs':(phase-fi/N)*m.PERIOD*1000,'rootScreenVelocityPxSec':m.SCREEN_SPEED*zoom,'sourcePivotCorrectionPx':0,'actualToeXY':actual.tolist(),'continuousToeXY':target.tolist()})
 return rows

def hold_gate(m,cycles=4):
 rows=[]
 for height in TARGETS:
  for k in range(math.ceil(m.PERIOD*cycles*60)):rows.extend(tracked_hold(k/60,height,m))
 records={}
 for height in TARGETS:
  selected=[r for r in rows if r['targetHeight']==height and r['sameStanceContact']];worst=m.STRIDE*m.SOURCE_SCALE*height/m.REFERENCE_HEIGHT/N
  records[str(height)]={'thresholdPx':2.,'floatEngine60HzMaxPx':max(r['floatEngineHeldToeErrorPx'] for r in selected),'integerPaste60HzMaxPx':max(r['actualIntegerPasteGroundSlipPx'] for r in selected),'worstContinuousFloatHoldBoundPx':worst,'integerPasteUpperBoundPx':worst+.5,'pass':max(r['actualIntegerPasteGroundSlipPx'] for r in selected)<=2 and worst+.5<=2,'sourcePivotCorrection':False}
 return {'status':'PREBUILD_CONTACT_PASS_NOT_VISUAL_ACCEPTANCE' if all(x['pass'] for x in records.values()) else 'PREBUILD_CONTACT_FAIL','pass':all(x['pass'] for x in records.values()),'method':'60Hz held exact24 phase cel, track original3D soletoe through source projection+fixed scale+actualintegerpaste; floatengine error separately. Not opticalflow.','cycles':cycles,'simulationHz':60,'precisePeriodMs':m.PERIOD*1000,'samplePhaseRule':'distance_world/world_stride; frame=floor(frac(distancephase)*24)','sceneZoomConvention':'64/80/96 are entire-scene camera zooms64/80,1,96/80: sameworld2.1; sprite,rootvelocity andgridscale together. Sprite-only resize at fixedworldpixelmapping is a different physicalscale and is notqualified.','thresholdsByHeight':records},rows

def prepare():
 if (BASE/'receipt.json').exists():raise ValueError('one completed renderbuild exists; no revision')
 m=model();gate,rows=hold_gate(m);numeric=[]
 for phase in np.linspace(.001,.999,501):numeric.extend(m.measurements(float(phase)))
 bones=max(max(r['upperError'],r['lowerError']) for r in numeric);stance=max(r['stanceWorldToeSpeedPerPhase'] for r in numeric if r['mode']!='SWING');numericpass=bones<=1e-8 and stance<=1e-7 and all(r['toeZ']>=-1e-10 and r['heelZ']>=-1e-10 for r in numeric)
 # Separate phase seam invariant; same localgeometry at phase0 and1, whole world advancesonestride.
 p0=m.pose(0);p1=m.pose(1);seam=max(float(np.linalg.norm(p0['joints'][k]-p1['joints'][k])) for k in p0['joints']);toeseam=max(float(np.linalg.norm(p0['feet'][s]['toe']-p1['feet'][s]['toe'])) for s in ('LEFT','RIGHT'))
 plan={'schema':'deterministic-villager-24-temporal-plan/v1','status':'FROZEN_ONE_BUILD_EXPERIMENT','frozenModelScript':{'path':str(OLD/'pilot.py'),'sha256':MODEL_SHA},'frozenEightMetadata':{'path':str(OLD/'animation.json'),'sha256':META_SHA},'changes':'Temporal sampling8->24 only. Exact same custommesh, material, gait, stride, camera, sourcegeometry, wholecanvas scale233 and physicalperiod. No style/detail/gait changes.','direction':'D07 screenEast/worldNEtheta315 ONLY','sourceCanvas':[256,256],'sourcePivot':[128,237],'runtimeCell':[128,128],'sourceCharacterHeight':233,'phaseSamples':[i/N for i in range(N)],'oldPhaseKeyMapping':{str(i):i*3 for i in range(8)},'contactKeys':{'F0':'oldF0 LEFTcontact','F12':'oldF4 RIGHTcontact'},'durationsMsExactEngine':[m.PERIOD*1000/N]*N,'precisePeriodMs':m.PERIOD*1000,'apngDurationsMs':[round((i+1)*m.PERIOD*1000/N)-round(i*m.PERIOD*1000/N) for i in range(N)],'gifDurationsMs':[10*(round((i+1)*m.PERIOD*100/N)-round(i*m.PERIOD*100/N)) for i in range(N)],'numericalRigGate':{'pass':numericpass,'maxBoneLengthError':bones,'maxStanceToeWorldVelocity':stance,'phaseSeamJointResidual':seam,'phaseSeamToeResidual':toeseam,'worldSeamStrideModel':m.STRIDE},'prebuildHeldContactGate':gate,'cadenceAccepted':False,'identityAccepted':False,'cameraReconciliationAccepted':False,'motionAccepted':False,'runtimeIntegrated':False,'oneRenderBuildOnly':True}
 (BASE/'plan.json').write_text(json.dumps(plan,indent=2)+'\n');(BASE/'prebuild-contact-gate.json').write_text(json.dumps(gate,indent=2)+'\n')
 with (BASE/'prebuild-contact-60hz.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 print(json.dumps({'prebuildContactPass':gate['pass'],'rigPass':numericpass,'seamJointResidual':seam,'at64_80_96':gate['thresholdsByHeight']},indent=2));return plan

def static_grid(w,h,zoom=1):
 # Camera fixed. Grid remains static; only character root translates. NEVER double motion.
 im=Image.new('RGBA',(w,h),(43,52,42,255));d=ImageDraw.Draw(im);step=54*1.08*zoom;half=step/2;hy=27*1.08/2*zoom
 for i in range(-20,21):
  x=w/2+i*half;d.line([(x-6*step,190-12*hy),(x+6*step,190+12*hy)],fill=(72,86,65,255));d.line([(x-6*step,190+12*hy),(x+6*step,190-12*hy)],fill=(72,86,65,255))
 return im

def anim(images,path,durations,loop=0):
 images[0].save(path,save_all=True,append_images=images[1:],duration=durations,loop=loop,**({'disposal':2,'optimize':False} if path.suffix=='.gif' else {'disposal':0,'blend':0}))

def reviews(frames,plan,m):
 for height in TARGETS:
  # PIL buffer rounds only storage width; drawing uses the exactheight233 physicalscale.
  canvas_size=round(256*height/233);images=[im.resize((canvas_size,canvas_size),Image.Resampling.LANCZOS) for im in frames];root=np.array([128.,237.])*canvas_size/256;sheet=Image.new('RGBA',(canvas_size*8,canvas_size*3+56),(63,66,60,255));d=ImageDraw.Draw(sheet);d.text((3,3),str(height)+'px target /24 samples same model+gait /CADENCE UNAPPROVED',fill='white')
  for i,im in enumerate(images):x=(i%8)*canvas_size;y=(i//8)*canvas_size+56;sheet.alpha_composite(im,(x,y));d.text((x+2,y-14),'F'+str(i),fill='white')
  sheet.save(BASE/('review-'+str(height)+'-contact-sheet.png'))
  inplace=[]
  for i,im in enumerate(images):
   canvas=static_grid(480,256,height/80);canvas.alpha_composite(im,(round(240-root[0]),round(190-root[1])));dd=ImageDraw.Draw(canvas);dd.text((8,8),str(height)+'px /24 CEL LOOP /same324.790ms cadence /PENDING REVIEW',fill='white');dd.text((8,24),'F'+str(i)+' /fixedsourcepivot /no contact compensation',fill='white');inplace.append(canvas)
  anim(inplace,BASE/('gameplay'+str(height)+'-inplace24.apng'),plan['apngDurationsMs']);anim(inplace,BASE/('gameplay'+str(height)+'-inplace24.gif'),plan['gifDurationsMs'])
 # Actual60Hz held cel against continuousdistancephase; staticgrid + roottravel only.
 rows=[];travel=[];diag=[];size=round(256*80/233);scaled=[im.resize((size,size),Image.Resampling.LANCZOS) for im in frames];root=np.array([128.,237.])*size/256
 for k in range(math.ceil(m.PERIOD*2*60)):
  sec=k/60;current=tracked_hold(sec,80,m);rows.extend(current);fi=current[0]['heldFrame'];root_x=100+m.SCREEN_SPEED*sec;canvas=static_grid(480,256);canvas.alpha_composite(scaled[fi],(round(root_x-root[0]),round(190-root[1])));dd=ImageDraw.Draw(canvas);dd.text((8,8),'80px /24 CEL HOLDS /60Hz root '+format(m.SCREEN_SPEED,'.3f')+'px/s',fill='white');dd.text((8,24),'STATIC GRID+MOVING ROOT ONLY /two-cycle diagnostic',fill='white');travel.append(canvas.copy());overlay=canvas.copy();od=ImageDraw.Draw(overlay);od.text((8,40),'RED heldsoletoe /GREEN continuousrigtoe /no pivotfix',fill='white')
  for r in current:
   for point,color in [(r['continuousToeXY'],(30,255,70,255)),(r['actualToeXY'],(255,55,40,255))]:od.ellipse((point[0]-2,point[1]-2,point[0]+2,point[1]+2),outline=color,width=1)
   od.line([tuple(r['continuousToeXY']),tuple(r['actualToeXY'])],fill=(255,175,60,255))
  diag.append(overlay)
 apng_d=[round((k+1)*1000/60)-round(k*1000/60) for k in range(len(travel))];gif_d=[10*(round((k+1)*100/60)-round(k*100/60)) for k in range(len(travel))]
 for name,ims in [('gameplay80-travel24-held60hz',travel),('continuous-groundphase-vs-held24',diag)]:anim(ims,BASE/(name+'.apng'),apng_d,loop=1);anim(ims,BASE/(name+'.gif'),gif_d,loop=1)
 return {'gridScreenVelocityPxSec':0,'spriteRootScreenVelocityPxSec':m.SCREEN_SPEED,'relativeGroundVelocityPxSec':m.SCREEN_SPEED,'rootAndGroundBothMoving':False,'renderedAtHz':60,'previewIntegerImageStorageSize':size,'exactPhysicalSpriteCanvasWidth':256*80/233,'storageRoundingDifferencePx':size-256*80/233,'exactEnginePeriodMs':m.PERIOD*1000,'apngPeriodMs':sum(plan['apngDurationsMs']),'gifPeriodMs':sum(plan['gifDurationsMs']),'gifIsTimingOracle':False,'previewTimingQuantization':'APNG integer1ms; GIF integer10ms. Engine uses exactfloat duration/distancephase. Traversal animation temporaldisplay rounded to16/17ms, root sampledexact60Hz.'}

def build():
 if (BASE/'frames').exists() or (BASE/'receipt.json').exists():raise ValueError('one build only; existing frames/receipt refusal')
 m=model();plan=json.loads((BASE/'plan.json').read_text());gate,measurements=hold_gate(m)
 if not(plan['numericalRigGate']['pass'] and gate['pass']):raise ValueError('prebuild gates failed; no celrender')
 for directory in ('frames','runtime128','aux'):(BASE/directory).mkdir()
 oldmeta=json.loads((OLD/'animation.json').read_text());frames=[];records=[];samekeys={};sourceheights=[];exactdur=m.PERIOD*1000/N
 for i in range(N):
  phase=i/N;pp=m.pose(phase);im,mask,depth,normals,limbid,geo=m.render(pp);bounds=geo['geometryBounds'];alpha=im.getbbox();height=alpha[3]-alpha[1]
  if not(min(bounds)>=0 and bounds[2]<256 and bounds[3]<256 and 192<=height<=256):raise ValueError('mesh bounds/size failed; stop no retry')
  path=BASE/'frames'/('F'+str(i)+'.png');im.save(path);im.resize((128,128),Image.Resampling.LANCZOS).save(BASE/'runtime128'/('F'+str(i)+'.png'))
  for suffix,image in [('mask',mask),('depth',depth),('normal',normals),('limbID',limbid)]:image.save(BASE/'aux'/('F'+str(i)+'-'+suffix+'.png'))
  if i%3==0:
   oldi=i//3;matching=sha(path)==oldmeta['frameRecords'][oldi]['sha256'];samekeys[str(oldi)]={'newFrame':i,'exactSourcePngByteMatch':matching}
   if not matching:raise ValueError('frozen8 key source changed; stop no retry')
  contacts={};toes={}
  for side in ('LEFT','RIGHT'):
   f=pp['feet'][side];toes[side]=m.project_vertices(m.local_world([f['toe']]))[0,:2].tolist();contacts[side]={'mode':f['mode'],'toeLocal3D':f['toe'].tolist(),'toeWorld3D':f['worldToe'].tolist(),'heelLocal3D':f['heel'].tolist(),'ankleLocal3D':f['ankle'].tolist(),'pitchDegrees':math.degrees(f['pitchRad'])}
  records.append({'frame':i,'phase':phase,'path':'frames/F'+str(i)+'.png','runtimePath':'runtime128/F'+str(i)+'.png','durationMs':exactdur,'startMs':i*exactdur,'sourceCanvas':[256,256],'sourcePivot':[128,237],'alphaBounds':list(alpha),'actualAlphaHeight':height,'toeScreenSourceXY':toes,'contacts':contacts,'jointsLocal3D':{k:v.tolist() for k,v in pp['joints'].items()},'sha256':sha(path),'mesh':geo});frames.append(im);sourceheights.append(height)
 atlas=Image.new('RGBA',(128*6,128*4));sourceatlas=Image.new('RGBA',(256*6,256*4))
 for i,im in enumerate(frames):atlas.alpha_composite(im.resize((128,128),Image.Resampling.LANCZOS),((i%6)*128,(i//6)*128));sourceatlas.alpha_composite(im,((i%6)*256,(i//6)*256))
 atlas.save(BASE/'atlas-runtime128.png');sourceatlas.save(BASE/'atlas-source256.png');movieinfo=reviews(frames,plan,m)
 # Preserve exactphase seam without storing duplicateframe24 as a misleading newphase.
 first=frames[0];seamimage,*_=m.render(m.pose(1));seam_rgba=first.tobytes()==seamimage.tobytes()
 if not seam_rgba:raise ValueError('pose1 image differs frompose0; stop no retry')
 meta={'schema':'deterministic-villager-animation/v2','status':'REAL_24_TEMPORAL_CEL_EXPERIMENT_PENDING_INDEPENDENT_REVIEW','direction':'D07 screenEast/worldNEtheta315','sourceCanvas':[256,256],'sourcePivot':[128,237],'runtimeCell':[128,128],'runtimePivot':[64,118.5],'sourceCharacterHeight':233,'referenceCharacterHeight':233,'durationsMs':[exactdur]*N,'totalDurationMs':m.PERIOD*1000,'exactModelPeriodMs':m.PERIOD*1000,'encodedApngDurationsMs':plan['apngDurationsMs'],'encodedGifDurationsMs':plan['gifDurationsMs'],'frameRecords':records,'targetReviewHeights':[64,80,96],'fixedWholeCanvasReviewSizes':{str(h):round(256*h/233) for h in TARGETS},'rootTravelModelPerCycle':m.STRIDE,'rootTravelWorldPerCycle':m.STRIDE*m.GAME_PX_PER_MODEL/m.WORLD_PX_PER_UNIT,'groundSpeedScreenPxSec':m.SCREEN_SPEED,'phaseSelection':'distancephase=worlddistance/worldstride, equivalentseconds/preciseperiod; floor(fracphase*24)','sceneZoomConvention':gate['sceneZoomConvention'],'frozenOldPhaseKeys':samekeys,'phaseSeamImageExactlyMatchesF0':seam_rgba,'auxEncoding':oldmeta['auxEncoding'],'identityAccepted':False,'cadenceAccepted':False,'cameraReconciliationAccepted':False,'motionAccepted':False,'runtimeIntegrated':False,'sourceCutoutsUsed':False,'imageGenerationCalls':0,'movieTiming':movieinfo}
 (BASE/'animation.json').write_text(json.dumps(meta,indent=2)+'\n');gate['status']='NUMERICAL_24_HELD_CONTACT_PASS_PENDING_ACTUAL_BROWSER_REVIEW';(BASE/'held-ground-slip-gate.json').write_text(json.dumps(gate,indent=2)+'\n')
 with (BASE/'held-ground-slip-60hz.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(measurements[0]));w.writeheader();w.writerows(measurements)
 files=[p for p in BASE.rglob('*') if p.is_file() and p.name!='receipt.json'];receipt={'schema':'deterministic-villager-24-temporal-receipt/v1','status':'ONE_24_TEMPORAL_EXPERIMENT_RENDERED_CONTACT_NUMERIC_PASS_REVIEW_PENDING','frames':24,'sourceAlphaHeightRange':[min(sourceheights),max(sourceheights)],'modelDependencySha256':MODEL_SHA,'frozen001Untouched':sha(OLD/'pilot.py')==MODEL_SHA,'modelMotionStyleScaleUnchanged':True,'old8SourceKeysExactlyMatch':all(x['exactSourcePngByteMatch'] for x in samekeys.values()),'phaseSeamExactRgbaMatch':seam_rgba,'heldContactGate':gate,'movieGroundMotion':movieinfo,'cadenceChanged':False,'cadenceAccepted':False,'identityAccepted':False,'cameraReconciliationAccepted':False,'motionAccepted':False,'runtimeIntegrated':False,'fanoutDirections':0,'imageGenerationCalls':0,'renderBuildCount':1,'scriptSha256':sha(__file__),'outputs':{str(p.relative_to(BASE)):sha(p) for p in files},'limitations':['Numerical heldtoe landmark comparison is not independent visiblemotion or opticalflow assessment.','Same brisk324.79ms cadence/style asfailed8pilot; denser samples alone do notfixidentity or timing.','64/80/96 consistency requires entirescenezoom, not resizing onlysprite atfixedgroundspeed.','PIL wholecanvas image buffers rounded tointegerpixels; browserexactfloatcanvasperiod is timingoracle.','Physicalortho26.565 groundratio.4472vsruntime2:1 remainsopen.']}
 (BASE/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({'status':receipt['status'],'alphaHeightRange':receipt['sourceAlphaHeightRange'],'old8KeysExact':receipt['old8SourceKeysExactlyMatch'],'phaseSeamExact':seam_rgba,'held64_80_96':gate['thresholdsByHeight']},indent=2))

if __name__=='__main__':
 if len(sys.argv)!=2 or sys.argv[1] not in ('prepare','build'):raise SystemExit('usage: pilot24.py prepare|build')
 if sys.argv[1]=='prepare':prepare()
 else:build()
