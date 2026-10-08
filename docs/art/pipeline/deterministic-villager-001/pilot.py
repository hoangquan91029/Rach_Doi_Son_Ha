"""Deterministic original 3D mesh/IK/cel pilot. CPU numpy/PIL, never source cutouts."""
import argparse,csv,hashlib,json,math,pathlib,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
BASE=pathlib.Path(__file__).resolve().parent
REFERENCE=pathlib.Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha/docs/art/characters/villager-neutral-D01-screen-South-007/raw.png')
REFERENCE_SHA='68a7fb9a71ae614f7c01432b1270e7a25071975667cfdf082ae02326d97678db'
ALPHA=math.atan(.5);C,S=math.cos(ALPHA),math.sin(ALPHA);STRIDE=.64;STANCE=.60;SOURCE_SCALE=128.;REFERENCE_HEIGHT=233.;GAME_PX_PER_MODEL=SOURCE_SCALE*80/REFERENCE_HEIGHT;WORLD_PX_PER_UNIT=54/math.sqrt(2)*1.08;WORLD_SPEED=2.1;SCREEN_SPEED=WORLD_SPEED*WORLD_PX_PER_UNIT;PERIOD=STRIDE*GAME_PX_PER_MODEL/SCREEN_SPEED
E=np.array([1,-1,0.])/math.sqrt(2);D=np.array([1,1,0.])/math.sqrt(2);Z=np.array([0.,0.,1.]);BASIS=np.stack([-D,E,Z],axis=1)
COLORS={'cloth':(214,195,158),'cloth_light':(230,211,174),'cloth_shadow':(179,157,123),'trousers':(91,75,61),'sash':(80,65,57),'sash_light':(104,85,71),'skin':(174,115,76),'skin_light':(198,139,91),'hat':(192,157,93),'hat_dark':(143,105,57),'hair':(37,31,25),'eye':(37,25,19),'eye_white':(216,195,152),'strap':(98,64,32),'sole':(111,79,38)}
IDS={'tunic':1,'hat':2,'head':3,'LEFT_thigh':4,'RIGHT_thigh':5,'LEFT_shin':6,'RIGHT_shin':7,'LEFT_foot':8,'RIGHT_foot':9,'LEFT_arm':10,'RIGHT_arm':11,'LEFT_hand':12,'RIGHT_hand':13,'sash':14}

def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def unit(v):v=np.array(v,dtype=float);return v/np.linalg.norm(v)
def smooth(x):x=float(np.clip(x,0,1));return x*x*(3-2*x)
def local_world(v):return np.array(v)@BASIS.T

def foot(t,side):
 offset=0 if side=='LEFT' else .5;unwrapped=t-offset;n=math.floor(unwrapped);q=unwrapped-n;sign=-1 if side=='LEFT' else 1;center=(n+offset)*STRIDE+STRIDE*STANCE/2
 if q<STANCE:
  u=0.;theta=math.radians(32)*smooth((q-.40)/.20);height=0.;toe_y=center+.13;contact='FLAT' if q<=.40 else 'TOE_ROLL'
 else:
  u=(q-STANCE)/(1-STANCE);theta=math.radians(32)*(1-smooth(u));height=.14*math.sin(math.pi*u)**2;toe_y=center+.13+STRIDE*smooth(u);contact='SWING'
 toe=np.array([sign*.105,toe_y-STRIDE*t,height])
 # Right-handed rotation Rx(-theta), toe fixed during flat/toe stance.
 R=np.array([[1,0,0],[0,math.cos(theta),math.sin(theta)],[0,-math.sin(theta),math.cos(theta)]])
 def transform(point):return toe+R@(np.array(point)-np.array([0.,.13,0.]))
 return {'q':q,'mode':contact,'pitchRad':theta,'toe':toe,'heel':transform([0,-.08,0]),'ankle':transform([0,-.015,.105]),'R':R,'transform':transform,'cycle':n,'worldToe':toe+np.array([0,STRIDE*t,0])}

def ik(H,A,L1=.43,L2=.42):
 v=A-H;dist=np.linalg.norm(v)
 if not abs(L1-L2)<dist<L1+L2:raise ValueError('unreachable leg')
 axis=v/dist;pole=np.array([0.,1.,0.]);bend=unit(pole-axis*np.dot(pole,axis));a=(L1*L1-L2*L2+dist*dist)/(2*dist);height=math.sqrt(max(0,L1*L1-a*a));K=H+axis*a+bend*height
 return K

def pose(t):
 bob=.014*(1-math.cos(4*math.pi*t));sway=-.016*math.cos(2*math.pi*t);p={'t':t,'bob':bob,'sway':sway,'feet':{},'joints':{}}
 for side,sign in [('LEFT',-1),('RIGHT',1)]:
  f=foot(t,side);H=np.array([sign*.105+sway,0.,.90+bob]);K=ik(H,f['ankle']);p['feet'][side]=f;p['joints'][side+'_hip']=H;p['joints'][side+'_knee']=K;p['joints'][side+'_ankle']=f['ankle']
  # Opposite arm to leading leg, with slightly bent constant-length elbow.
  phi=(-1 if side=='LEFT' else 1)*.32*math.cos(2*math.pi*t);shoulder=np.array([sign*.225+sway,0.,1.35+bob]);elbow=shoulder+.255*unit([sign*.08,math.sin(phi),-math.cos(phi)]);wrist=elbow+.235*unit([-sign*.03,math.sin(phi+.10),-math.cos(phi+.10)])
  p['joints'][side+'_shoulder']=shoulder;p['joints'][side+'_elbow']=elbow;p['joints'][side+'_wrist']=wrist
 return p

def measurements(t):
 p=pose(t);rows=[]
 for side in ('LEFT','RIGHT'):
  f=p['feet'][side];H=p['joints'][side+'_hip'];K=p['joints'][side+'_knee'];A=p['joints'][side+'_ankle'];dt=1e-7;prev=foot(t-dt,side);nxt=foot(t+dt,side);speed=np.linalg.norm(nxt['worldToe']-prev['worldToe'])/(2*dt)
  if f['mode']!='SWING':
   other=nxt if f['q']+dt<STANCE else prev;speed=np.linalg.norm(other['worldToe']-f['worldToe'])/dt
  rows.append({'phase':t,'side':side,'mode':f['mode'],'upperLength':float(np.linalg.norm(K-H)),'lowerLength':float(np.linalg.norm(A-K)),'upperError':abs(float(np.linalg.norm(K-H))-.43),'lowerError':abs(float(np.linalg.norm(A-K))-.42),'toeZ':float(f['toe'][2]),'heelZ':float(f['heel'][2]),'toeWorld':f['worldToe'].tolist(),'stanceWorldToeSpeedPerPhase':float(speed),'pitchDegrees':math.degrees(f['pitchRad'])})
 return rows

def freeze():
 if sha(REFERENCE)!=REFERENCE_SHA:raise ValueError('canonical South reference custody changed')
 spec={'status':'FROZEN_GEOMETRY_SPEC_PENDING_VISUAL_REVIEW','canonicalAppearanceReference':{'path':str(REFERENCE),'sha256':REFERENCE_SHA,'usage':'inspected identity only; no copied pixels/cutouts/textures'},'renderer':'deterministic original custom triangle meshes, numpy/PIL orthographic z-buffer','direction':{'screen':'East D07','world':'engineNE theta315','engineWorldX':[1,0,0],'engineWorldY':[0,1,0],'worldUp':[0,0,1],'cardinalMapping':'engineX=East; engineY=-North; camera+engineX/+engineY. Anatomical ownership follows explicit local rig axes, not reflected geographic labels.','screenRight':E.tolist(),'cameraGroundAxis':D.tolist(),'localActorRight':(-D).tolist(),'localActorForward':E.tolist(),'anatomicalLeftSash':'local x negative, camera-near side; fixed ownership/material'},'camera':{'type':'orthographic','elevationRad':ALPHA,'elevationDegrees':math.degrees(ALPHA),'projection':'screen=(128+128 dot(p,E),237+128[sin(alpha)dot(p,D)-cos(alpha)z]); depth=cos(alpha)dot(p,D)+sin(alpha)z','canvas':[256,256],'root':[128,237],'pixelsPerModelUnit':SOURCE_SCALE,'sourceReferenceCharacterHeight':REFERENCE_HEIGHT,'referenceScaleChoice':'F0 actualalphaheight233 measured once after originalmeshrender; reused for every frame, not bboxfitted perpose','scalePerPose':False,'runtimeCell':[128,128],'reviewCharacterTargets':[64,80,96]},'physicalScale':{'strideModelUnits':STRIDE,'gameplay80PixelsPerModelUnit':GAME_PX_PER_MODEL,'runtimeWorldPixelsPerUnit':WORLD_PX_PER_UNIT,'modelUnitInRuntimeWorldUnits':GAME_PX_PER_MODEL/WORLD_PX_PER_UNIT,'worldSpeed':WORLD_SPEED,'screenEastSpeedPxSec':SCREEN_SPEED,'periodSec':PERIOD,'eightFrameHoldMs':1000*PERIOD/8,'limitation':'physical orthographic camera elevationatan(.5) has sin(elevation) ground projection, whereas runtime2:1 grid convention uses .5; only screenEast foot/root speed is calibrated here.'},'rig':{'thigh':.43,'shin':.42,'upperArm':.255,'forearm':.235,'stanceFraction':STANCE,'heelRiseStartPhase':.4,'heelRiseMaxDegrees':32,'footLength':.21,'toeRest':[0,.13,0],'heelRest':[0,-.08,0],'ankleRest':[0,-.015,.105],'hipHeight':.90,'rootTravelPerPhase':STRIDE,'cadenceAccepted':False,'leftContactPhase':0,'rightContactPhase':.5,'sourceFootPitch':'rigid whole foot around toe; ankle derived then knee IK; no leg stretch or pivot correction'},'gates':{'boneLengthErrorMax':1e-8,'stanceToeZMax':1e-10,'stanceWorldToeSpeedPerPhaseMax':1e-7,'meshSourceCanvasMax':256,'sourceCharacterHeightRange':[192,256],'realHeldSpriteGroundSlipMaxPx':2.,'identityAccepted':False,'motionAccepted':False,'runtimeIntegrated':False}}
 rows=[r for t in np.linspace(.001,.999,501) for r in measurements(float(t))];gate=all(r['upperError']<1e-8 and r['lowerError']<1e-8 and r['heelZ']>=-1e-10 and (r['mode']=='SWING' or abs(r['toeZ'])<1e-10 and r['stanceWorldToeSpeedPerPhase']<1e-7) for r in rows)
 keys=[]
 for i in (0,2,4,6):
  pp=pose(i/8);keys.append({'frame':i,'phase':i/8,'jointsLocal':{k:v.tolist() for k,v in pp['joints'].items()},'feet':{s:{k:(v.tolist() if isinstance(v,np.ndarray) else v) for k,v in pp['feet'][s].items() if k not in ('transform','R')} for s in ('LEFT','RIGHT')}})
 (BASE/'spec.json').write_text(json.dumps(spec,indent=2)+'\n');(BASE/'key-geometry.json').write_text(json.dumps({'status':'NUMERICAL_PASS_NOT_VISUAL_ACCEPTANCE' if gate else 'NUMERICAL_FAIL','numericalGate':gate,'keys':keys,'checks':{'sampledPhases':501,'maxUpperError':max(r['upperError'] for r in rows),'maxLowerError':max(r['lowerError'] for r in rows),'maxStanceToeSpeedPerPhase':max(r['stanceWorldToeSpeedPerPhase'] for r in rows if r['mode']!='SWING')}},indent=2)+'\n')
 with (BASE/'geometry-measurements.csv').open('w') as fh:w=csv.DictWriter(fh,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 return gate

if __name__=="__main__" and len(sys.argv)>1 and sys.argv[1]=="freeze":print(json.dumps({"numericalGate":freeze()}))

class Mesh:
 def __init__(self):self.v=[];self.n=[];self.tri=[];self.color=[];self.ids=[]
 def add(self,verts,faces,material,limb,variations=None):
  verts=np.array(verts,dtype=float);normals=np.zeros_like(verts);faces=np.array(faces,dtype=int)
  for a,b,c in faces:
   normal=np.cross(verts[b]-verts[a],verts[c]-verts[a]);normals[a]+=normal;normals[b]+=normal;normals[c]+=normal
  lengths=np.linalg.norm(normals,axis=1);normals/=np.maximum(lengths[:,None],1e-15);offset=len(self.v);self.v.extend(verts);self.n.extend(normals);self.tri.extend(faces+offset)
  base=np.array(COLORS[material]);self.color.extend([np.clip(base*(variations[i] if variations else 1),0,255) for i in range(len(faces))]);self.ids.extend([IDS[limb]]*len(faces))
 def ring_form(self,rings,material,limb,N=16,fold=.0,front_open_below=None):
  verts=[];faces=[];variations=[]
  for j,(center,rx,ry) in enumerate(rings):
   for k in range(N):
    a=2*math.pi*k/N;f=1+fold*math.cos(6*a+.4*j);verts.append(np.array(center)+[rx*math.cos(a)*f,ry*math.sin(a)*f,0])
  for j in range(len(rings)-1):
   for k in range(N):
    # Actual slit topology below waist, not painted faux-leg cutouts.
    mid=2*math.pi*(k+.5)/N
    if front_open_below and rings[j][0][2]<front_open_below and abs(mid-math.pi/2)<.20:continue
    a=j*N+k;b=j*N+(k+1)%N;c=(j+1)*N+k;d=(j+1)*N+(k+1)%N;faces.extend([[a,b,c],[b,d,c]]);shade=1+.018*math.cos(3*mid+j);variations.extend([shade,shade])
  self.add(verts,faces,material,limb,variations)
 def tube(self,A,B,profile,material,limb,N=12,fold=0):
  A=np.array(A);B=np.array(B);axis=unit(B-A);width=unit(np.array([1.,0,0])-axis*axis[0]);other=np.cross(axis,width);verts=[];faces=[]
  for j,(t,rx,ry) in enumerate(profile):
   center=A+t*(B-A)
   for k in range(N):
    a=k*2*math.pi/N;f=1+fold*math.cos(5*a+.7*j);verts.append(center+f*(width*math.cos(a)*rx+other*math.sin(a)*ry))
  for j in range(len(profile)-1):
   for k in range(N):
    a=j*N+k;b=j*N+(k+1)%N;c=(j+1)*N+k;d=(j+1)*N+(k+1)%N;faces.extend([[a,b,c],[b,d,c]])
  self.add(verts,faces,material,limb)
 def strip(self,points,width,material,limb,widthaxis=None):
  points=np.array(points);axis=np.array([1.,0,0]) if widthaxis is None else unit(widthaxis);verts=[];faces=[]
  for p in points:verts.extend([p-axis*width/2,p+axis*width/2])
  for i in range(len(points)-1):faces.extend([[2*i,2*i+1,2*i+2],[2*i+1,2*i+3,2*i+2]])
  self.add(verts,faces,material,limb)
 def rod(self,points,r,material,limb):
  for a,b in zip(points,points[1:]):self.tube(a,b,[(0,r,r),(1,r,r)],material,limb,N=6)
 def world(self):return np.array(self.v)@BASIS.T,np.array(self.n)@BASIS.T,np.array(self.tri),np.array(self.color),np.array(self.ids)

def mesh_for(p):
 m=Mesh();b=p['bob'];sx=p['sway'];offset=np.array([sx,0,b]);shift=lambda v:np.array(v)+offset
 # Asymmetric wrap tunic, hand-shaped tapered torso/hem rings, visible front slit.
 m.ring_form([(shift([0,0,z]),rx,ry) for z,rx,ry in [(.65,.268,.170),(.72,.251,.155),(.84,.221,.145),(.96,.184,.122),(1.04,.207,.139),(1.22,.257,.146),(1.36,.262,.129),(1.40,.135,.097)]],'cloth','tunic',N=24,fold=.04,front_open_below=.77)
 # Wrapped front lapels and seam: layered geometry retains V neckline.
 m.strip([shift([-.13,.142,1.38]),shift([-.045,.160,1.22]),shift([.06,.154,1.08]),shift([.12,.133,.96])],.037,'cloth_light','tunic',widthaxis=[.82,0,.57])
 m.strip([shift([.13,.140,1.38]),shift([.04,.161,1.23])],.034,'cloth_light','tunic',widthaxis=[.84,0,-.55])
 # Hem folds, a few deliberate non-periodic cloth ridges, no photo texture.
 for x in [-.20,-.115,.09,.19]:m.strip([shift([x,.155, .70]),shift([x*.84,.148,.83]),shift([x*.71,.129,.96])],.010,'cloth_shadow','tunic')
 # Waist sash wraps actual body geometry; knot and hanging end on anatomical LEFT.
 m.ring_form([(shift([0,0,z]),rx,ry) for z,rx,ry in [(.949,.193,.135),(.966,.199,.144),(1.006,.196,.140),(1.017,.190,.132)]],'sash','sash',N=24,fold=.025)
 for z in [.967,.988,1.005]:m.ring_form([(shift([0,0,z]),.200,.144),(shift([0,0,z+.006]),.198,.143)],'sash_light','sash',N=24)
 m.ring_form([(shift([-.205,.085,z]),rx,ry) for z,rx,ry in [(.945,.008,.009),(.966,.035,.032),(.994,.036,.031),(1.010,.012,.012)]],'sash_light','sash',N=12)
 m.strip([shift([-.205,.087,.960]),shift([-.228,.108,.87]),shift([-.232,.135,.76]),shift([-.204,.152,.66])],.080,'sash','sash',widthaxis=[1,0,.2]);m.strip([shift([-.211,.104,.945]),shift([-.234,.127,.85]),shift([-.239,.151,.72])],.014,'sash_light','sash')
 # Neck and custom jaw/head profile, geometry facial features (no source pixels).
 m.ring_form([(shift([0,.013,z]),rx,ry) for z,rx,ry in [(1.34,.074,.068),(1.42,.076,.071),(1.49,.067,.061)]],'skin','head',N=14)
 m.ring_form([(shift([0,.021,z]),rx,ry) for z,rx,ry in [(1.45,.025,.04),(1.49,.067,.067),(1.55,.104,.092),(1.62,.116,.097),(1.69,.098,.083),(1.73,.070,.054),(1.75,.008,.009)]],'skin_light','head',N=20)
 m.ring_form([(shift([0,-.008,z]),rx,ry) for z,rx,ry in [(1.64,.11,.09),(1.70,.111,.087),(1.75,.081,.066),(1.78,.008,.008)]],'hair','head',N=20)
 for sign in (-1,1):
  m.ring_form([(shift([sign*.108,.011,z]),rx,ry) for z,rx,ry in [(1.551,.008,.013),(1.577,.024,.022),(1.61,.023,.019),(1.627,.005,.006)]],'skin','head',N=10)
  # Eyes and brows at front of the actual face; hat shadow is geometric occlusion.
  m.strip([shift([sign*.073,.109,1.621]),shift([sign*.037,.118,1.624])],.009,'eye','head',widthaxis=[0,0,1]);m.strip([shift([sign*.068,.108,1.646]),shift([sign*.031,.119,1.651])],.011,'hair','head',widthaxis=[0,0,1])
 nose=[shift(v) for v in [[-.021,.111,1.64],[.021,.111,1.64],[0,.171,1.592],[-.027,.119,1.582],[.027,.119,1.582]]];m.add(nose,[[0,1,2],[0,2,3],[1,4,2],[2,4,3]],'skin','head')
 m.strip([shift([-.047,.124,1.575]),shift([0,.144,1.580]),shift([.047,.124,1.575])],.014,'hair','head',widthaxis=[0,0,1]);m.strip([shift([-.028,.122,1.555]),shift([.028,.122,1.555])],.006,'eye','head',widthaxis=[0,0,1]);m.add([shift(v) for v in [[-.035,.120,1.542],[.035,.120,1.542],[0,.094,1.488]]],[[0,1,2]],'hair','head')
 # Original tilted conical woven hat; near brim lifted to keep profile face readable.
 hat_start=len(m.v)
 m.ring_form([(shift([0,0,z]),r,r) for z,r in [(1.694,.405),(1.710,.412),(1.740,.365),(1.785,.292),(1.834,.213),(1.885,.126),(1.935,.029),(1.947,.002)]],'hat','hat',N=36)
 m.ring_form([(shift([0,0,1.686]),.404,.404),(shift([0,0,1.693]),.414,.414)],'hat_dark','hat',N=36)
 for z in np.linspace(1.738,1.924,7):
  r=.412*(1.947-z)/(1.947-1.710)+.003;m.ring_form([(shift([0,0,z]),r,r),(shift([0,0,z+.003]),r-.005,r-.005)],'hat_dark','hat',N=36)
 for a in np.linspace(0,2*math.pi,18,endpoint=False):
  pts=[shift([r*math.cos(a),r*math.sin(a),z]) for z,r in [(1.716,.414),(1.784,.296),(1.855,.180),(1.930,.031)]];m.rod(pts,.0026,'hat_dark','hat')
 # Near-side brim lift is deterministic original geometry, not a source warp.
 for idx in range(hat_start,len(m.v)):
  v=np.array(m.v[idx]);relative=v-offset;v[:2]=offset[:2]+relative[:2]*.75;v[2]+=-.30*(v[0]-sx)+.12*v[1];m.v[idx]=v
 # Recompute hat normals after authored mesh tilt/shape (uniform across all poses).
 for i in range(hat_start,len(m.v)):m.n[i]=np.zeros(3)
 for tri in m.tri:
  if min(tri)<hat_start:continue
  a,bb,c=tri;normal=np.cross(np.array(m.v[bb])-m.v[a],np.array(m.v[c])-m.v[a]);
  for i in tri:m.n[i]+=normal
 for i in range(hat_start,len(m.v)):m.n[i]=unit(m.n[i]) if np.linalg.norm(m.n[i])>1e-15 else np.zeros(3)
 # Bone-driven original trouser/sleeve/skin meshes, stitched cuff rings.
 for side,sign in [('LEFT',-1),('RIGHT',1)]:
  j=p['joints'];H=j[side+'_hip'];K=j[side+'_knee'];A=j[side+'_ankle'];shoulder=j[side+'_shoulder'];elbow=j[side+'_elbow'];wrist=j[side+'_wrist'];thigh=side+'_thigh';shin=side+'_shin';arm=side+'_arm';hand=side+'_hand';footid=side+'_foot'
  m.tube(H,K,[(0,.095,.105),(.16,.133,.127),(.40,.134,.122),(.72,.123,.119),(.94,.097,.090),(1,.082,.083)],'trousers',thigh,N=18,fold=.07)
  m.tube(H,K,[(.91,.098,.094),(.96,.100,.095),(1,.086,.084)],'sash_light',thigh,N=18)
  m.tube(K,A,[(0,.078,.073),(.18,.087,.080),(.45,.070,.060),(.75,.055,.051),(.93,.046,.044),(1,.040,.042)],'cloth',shin,N=16,fold=.04)
  for t in [.20,.37,.57,.75,.88]:m.tube(K,A,[(t,.077*(1-t)+.041*t,.073*(1-t)+.041*t),(t+.018,.077*(1-t)+.041*t,.073*(1-t)+.041*t)],'cloth_shadow',shin,N=16)
  m.tube(shoulder,elbow,[(0,.109,.104),(.25,.120,.116),(.60,.111,.095),(.87,.102,.090),(1,.086,.078)],'cloth',arm,N=18,fold=.045)
  m.tube(shoulder,elbow,[(.86,.103,.098),(.90,.107,.101),(.96,.106,.095),(1.02,.085,.077)],'cloth_light',arm,N=18,fold=.06)
  m.tube(elbow,wrist,[(0,.064,.060),(.18,.070,.058),(.65,.051,.044),(1,.037,.035)],'skin',arm,N=14)
  axis=unit(wrist-elbow);end=wrist+.106*axis;m.tube(wrist,end,[(0,.037,.032),(.28,.055,.032),(.65,.049,.027),(1,.022,.018)],'skin',hand,N=12)
  for k in [-1.5,-.5,.5,1.5]:
   start=wrist+axis*.068+np.array([k*.016,0,0]);m.tube(start,start+axis*(.050-.005*abs(k)),[(0,.011,.010),(.7,.009,.009),(1,.004,.004)],'skin_light',hand,N=8)
  thumb=wrist+axis*.030+np.array([-sign*.04,0,0]);m.tube(thumb,thumb+axis*.044+np.array([-sign*.020,0,0]),[(0,.018,.017),(1,.006,.006)],'skin',hand,N=9)
  # Foot solids transformed as ONE rigid mesh around actual toe contact.
  fm=Mesh();fm.ring_form([([0,.025,z],rx,ry) for z,rx,ry in [(0,.051,.105),(.010,.055,.113),(.023,.052,.109)]],'sole',footid,N=24)
  # Toe contact bottom vertex is a declared original mesh landmark at y=.13,z=0.
  fm.ring_form([([0,y,z],rx,ry) for y,z,rx,ry in [(-.010,.019,.044,.069),(-.015,.040,.046,.073),(-.032,.075,.037,.055),(-.018,.102,.031,.030),(-.018,.110,.003,.005)]],'skin',footid,N=18)
  for k in range(5):
   x=(k-2)*.019;fm.ring_form([([x,.105,z],rx,ry) for z,rx,ry in [(.024,.008,.018),(.034,.010,.021),(.044,.006,.014),(.046,.001,.002)]],'skin_light',footid,N=10)
  fm.strip([[-.047,.078,.032],[-.030,.078,.052],[0,.078,.059],[.030,.078,.052],[.047,.078,.032]],.017,'strap',footid,widthaxis=[0,1,0]);fm.strip([[-.040,-.015,.07],[0,-.025,.108],[.04,-.015,.07]],.016,'strap',footid,widthaxis=[0,1,0])
  for sg in (-1,1):fm.rod([[sg*.038,-.01,.073],[sg*.021,.025,.064],[0,.079,.060]],.006,'strap',footid)
  transform=p['feet'][side]['transform'];fv=np.array([transform(v) for v in fm.v]);R=p['feet'][side]['R'];offsetlen=len(m.v);m.v.extend(fv);m.n.extend(np.array(fm.n)@R.T);m.tri.extend(np.array(fm.tri)+offsetlen);m.color.extend(fm.color);m.ids.extend(fm.ids)
 return m

def project_vertices(vertices):
 x=vertices@E;y=S*(vertices@D)-C*vertices[:,2];depth=C*(vertices@D)+S*vertices[:,2]
 return np.stack([128+SOURCE_SCALE*x,237+SOURCE_SCALE*y,depth],axis=1)

def render(p):
 mesh=mesh_for(p);v,n,tris,colors,ids=mesh.world();proj=project_vertices(v);zbuf=np.full((256,256),-np.inf);rgb=np.zeros((256,256,3),dtype=float);normalbuf=np.zeros((256,256,3));idbuf=np.zeros((256,256),dtype=np.uint8);light=unit(-.5*E+.3*D+Z)
 for i,tri in enumerate(tris):
  a,b,c=proj[tri];den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
  if abs(den)<1e-9:continue
  x0=max(0,math.floor(min(a[0],b[0],c[0])));x1=min(255,math.ceil(max(a[0],b[0],c[0])));y0=max(0,math.floor(min(a[1],b[1],c[1])));y1=min(255,math.ceil(max(a[1],b[1],c[1])))
  if x0>x1 or y0>y1:continue
  yy,xx=np.mgrid[y0:y1+1,x0:x1+1];xx=xx+.5;yy=yy+.5;wa=((b[1]-c[1])*(xx-c[0])+(c[0]-b[0])*(yy-c[1]))/den;wb=((c[1]-a[1])*(xx-c[0])+(a[0]-c[0])*(yy-c[1]))/den;wc=1-wa-wb;zz=wa*a[2]+wb*b[2]+wc*c[2];mask=(wa>=-1e-8)&(wb>=-1e-8)&(wc>=-1e-8)&(zz>zbuf[y0:y1+1,x0:x1+1])
  if not np.any(mask):continue
  normals=wa[...,None]*n[tri[0]]+wb[...,None]*n[tri[1]]+wc[...,None]*n[tri[2]];normals/=np.maximum(np.linalg.norm(normals,axis=2)[...,None],1e-15);diff=np.clip(normals@light,0,1);shade=np.select([diff<.18,diff<.48,diff<.78],[.55,.73,.88],default=1.03);col=np.clip(colors[i]*shade[...,None],0,255)
  zbuf[y0:y1+1,x0:x1+1][mask]=zz[mask];rgb[y0:y1+1,x0:x1+1][mask]=col[mask];normalbuf[y0:y1+1,x0:x1+1][mask]=normals[mask];idbuf[y0:y1+1,x0:x1+1][mask]=ids[i]
 mask=idbuf>0
 # Thin original sprite contour, material and geometry preserved; no reference image operations.
 adjacent=np.zeros_like(mask)
 for dy,dx in [(1,0),(-1,0),(0,1),(0,-1)]:adjacent|=np.roll(np.roll(mask,dy,0),dx,1)
 outline=adjacent&~mask;rgba=np.zeros((256,256,4),dtype=np.uint8);rgba[:,:,:3]=rgb.astype(np.uint8);rgba[:,:,3][mask]=255;rgba[:,:,:3][outline]=[57,45,31];rgba[:,:,3][outline]=230
 depth=np.zeros((256,256),dtype=np.uint16);depth[mask]=np.clip((zbuf[mask]+1)/3*65534+1,1,65535).astype(np.uint16);normals=np.zeros((256,256,4),dtype=np.uint8);normals[:,:,:3][mask]=np.clip((normalbuf[mask]+1)*127.5,0,255).astype(np.uint8);normals[:,:,3][mask]=255
 return Image.fromarray(rgba),Image.fromarray((mask*255).astype(np.uint8)),Image.fromarray(depth),Image.fromarray(normals),Image.fromarray(idbuf),{'vertices':len(v),'triangles':len(tris),'geometryBounds':proj[:,:2].min(axis=0).tolist()+proj[:,:2].max(axis=0).tolist()}

def grid(w,h,root_x=0):
 im=Image.new('RGBA',(w,h),(43,52,42,255));d=ImageDraw.Draw(im);step=54*1.08;half=step/2;hy=27*1.08/2;origin=w/2-root_x%step
 for i in range(-20,21):
  x=origin+i*half
  d.line([(x-6*step,190-6*hy*2),(x+6*step,190+6*hy*2)],fill=(72,86,65,255),width=1)
  d.line([(x-6*step,190+6*hy*2),(x+6*step,190-6*hy*2)],fill=(72,86,65,255),width=1)
 return im

def animsave(images,path,durations,loop=0):
 kwargs={'save_all':True,'append_images':images[1:],'duration':durations,'loop':loop}
 if path.suffix=='.gif':images[0].save(path,disposal=2,optimize=False,**kwargs)
 else:images[0].save(path,disposal=0,blend=0,**kwargs)

def create_previews(frames,meta):
 # Fixed whole-canvas scale from declared224 referenceheight, never per-frame bbox fit.
 sheets={};durations=meta['durationsMs'];sizes={height:round(256*height/REFERENCE_HEIGHT) for height in (64,80,96)}
 for height,size in sizes.items():
  sheet=Image.new('RGBA',(size*8, size+45),(63,66,60,255));d=ImageDraw.Draw(sheet);d.text((3,3),str(height)+'px declared-height / fixedcanvas scale / PENDING IDENTITY+MOTION',fill='white')
  for i,im in enumerate(frames):d.text((i*size+2,22),'F'+str(i),fill='white');sheet.alpha_composite(im.resize((size,size),Image.Resampling.LANCZOS),(i*size,45))
  sheet.save(BASE/('review-'+str(height)+'-contact-sheet.png'));sheets[height]=size
 size=sizes[80];root=np.array([128,237])*size/256;small=[im.resize((size,size),Image.Resampling.LANCZOS) for im in frames];inplace=[]
 for i,im in enumerate(small):
  canvas=grid(480,256);canvas.alpha_composite(im,(int(240-root[0]),int(190-root[1])));d=ImageDraw.Draw(canvas);d.text((8,8),'ACTUAL 8 CEL LOOP /80px reference scale /in place',fill='white');d.text((8,24),'Source pivot fixed; visible cadence/identity pending review',fill='white');d.text((8,40),'F'+str(i)+' '+str(durations[i])+'ms',fill='white');inplace.append(canvas)
 animsave(inplace,BASE/'gameplay80-inplace-eight.apng',durations);animsave(inplace,BASE/'gameplay80-inplace-eight.gif',durations)
 # Simulated renderer holds each cel while root moves at continuous engine speed60Hz.
 # Overlay is separate diagnostic; it never moves source pivot or corrects cel toes.
 hz=60;count=math.ceil(PERIOD*2*hz);travel=[];diagnostic=[];rows=[]
 for k in range(count):
  sec=k/hz;t=sec/PERIOD;phase=t%1;fi=min(7,math.floor(phase*8));held_phase=math.floor(t)+fi/8;root_x=100+SCREEN_SPEED*sec;canvas=grid(480,256);canvas.alpha_composite(small[fi],(round(root_x-root[0]),round(190-root[1])));d=ImageDraw.Draw(canvas);d.text((8,8),'80px /D07 East /continuous root86.604px/s /8 CEL HOLDS',fill='white');d.text((8,24),'Two-cycle traversal diagnostic; scene reset is not animation seam',fill='white');travel.append(canvas.copy());diag=canvas.copy();dd=ImageDraw.Draw(diag);dd.text((8,40),'RED=held cel toe GREEN=continuous rig toe; no pivot correction',fill='white')
  live=pose(t);sample=pose(held_phase)
  for side in ('LEFT','RIGHT'):
   lf=live['feet'][side];sf=sample['feet'][side];actual=project_vertices(local_world([sf['toe']]))[0,:2];desired=project_vertices(local_world([lf['toe']]))[0,:2];actual=actual*size/256+[round(root_x-root[0]),round(190-root[1])];desired=desired*size/256-root+[root_x,190];err=float(np.linalg.norm(actual-desired));mode=lf['mode'];same_contact=mode!='SWING' and sf['mode']!='SWING' and lf['cycle']==sf['cycle'];world_held=sf['toe']+np.array([0,STRIDE*t,0]);world_live=lf['worldToe'];ground_slip=abs(float(world_held[1]-world_live[1]))*SOURCE_SCALE*size/256
   for point,color in [(desired,(40,255,80,255)),(actual,(255,55,45,255))]:dd.ellipse((point[0]-2,point[1]-2,point[0]+2,point[1]+2),outline=color,width=1)
   dd.line([tuple(actual),tuple(desired)],fill=(255,160,60,255));rows.append({'timestampSec':sec,'phase':phase,'heldFrame':fi,'side':side,'mode':mode,'sameStanceContact':same_contact,'heldToeScreenErrorPx':err,'groundSlipPx':ground_slip,'actualPreviewHeldToeGroundSlipPx':abs(float(actual[0]-desired[0])),'sourcePivotCorrectionPx':0,'frameAgeMs':(phase-fi/8)*PERIOD*1000})
  diagnostic.append(diag)
 previewdur=[17 if i%3!=2 else 16 for i in range(count)];animsave(travel,BASE/'gameplay80-travel-eight-held-60hz.apng',previewdur,loop=1);animsave(travel,BASE/'gameplay80-travel-eight-held-60hz.gif',previewdur,loop=1);animsave(diagnostic,BASE/'continuous-groundphase-vs-held80.apng',previewdur,loop=1);animsave(diagnostic,BASE/'continuous-groundphase-vs-held80.gif',previewdur,loop=1)
 with (BASE/'held-ground-slip-60hz.csv').open('w') as fh:w=csv.DictWriter(fh,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 same=[r for r in rows if r['sameStanceContact']];measured=max(r['actualPreviewHeldToeGroundSlipPx'] for r in same);maxanalytic=SCREEN_SPEED*PERIOD/8;gate={'status':'FAILED_EIGHT_FRAME_HOLD_SLIP' if measured>2 else 'PASS_SAMPLED_HOLD_SLIP_NOT_VISUAL_ACCEPTANCE','thresholdPx':2,'actual60HzSameContactMaxSlipPx':measured,'analyticHeldPoseGroundSlipMaxPx':max(r['groundSlipPx'] for r in same),'measurementMethod':'Track originalmesh sole-toe landmark through actual held cel sample and integer APNG paste placement at60Hz; not opticalflow, no pivot compensation','worstContinuousHoldBoundPx':maxanalytic,'physicalScreenSpeedPxSec':SCREEN_SPEED,'simulationHz':hz,'celFrames':8,'testCycles':2,'previewWholeCanvasSize':size,'actualPreviewScalePxPerModelUnit':SOURCE_SCALE*size/256,'mathematicalStanceContactPass':True,'heldSpriteContactPass':measured<=2,'sourcePivotCorrection':False,'cadenceAccepted':False,'higherTemporalCelCountRecommended':24 if measured>2 else None,'recommendation':'Preserve8-frame failed hold pilot. Same eight phase keys need24/32 temporal cels and repeat real60Hz held-ground gate before motion acceptance. No other direction generated.'}
 (BASE/'held-ground-slip-gate.json').write_text(json.dumps(gate,indent=2)+'\n');return gate

def build():
 if not freeze():raise ValueError('numeric key geometry gate failed; no8frame export')
 side_reference=pathlib.Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha/docs/art/characters/villager-neutral-D07-screen-East-guided-007/raw.png');spec=json.loads((BASE/'spec.json').read_text());spec['sideAppearanceReference']={'path':str(side_reference),'sha256':sha(side_reference),'usage':'actually inspected side silhouette/colors only; no pixels copied'};spec['camera']['actualProjectionMatrixModelToScreenPerUnit']=[E.tolist(),(S*D-C*Z).tolist(),(C*D+S*Z).tolist()];spec['camera']['groundBasisScreenUnitVectors']={'engineX':[float(E[0]),float(S*D[0])],'engineY':[float(E[1]),float(S*D[1])]};spec['camera']['groundDiamondVerticalToHorizontalRatio']=S;spec['camera']['engine54x27ReconciliationAccepted']=False;(BASE/'spec.json').write_text(json.dumps(spec,indent=2)+'\n')
 target=BASE/'frames';target.mkdir(exist_ok=True);aux=BASE/'aux';aux.mkdir(exist_ok=True);runtime=BASE/'runtime128';runtime.mkdir(exist_ok=True);frames=[];records=[];cumulative=0
 exactms=PERIOD*1000/8;durations=[round((i+1)*exactms)-round(i*exactms) for i in range(8)]
 for i in range(8):
  p=pose(i/8);image,mask,depth,normal,limbid,geo=render(p);bounds=geo['geometryBounds'];alpha=image.getbbox();height=alpha[3]-alpha[1]
  if not (min(bounds)>=0 and bounds[2]<256 and bounds[3]<256 and 192<=height<=256):raise ValueError('wholemesh sourcecanvas/height gate failed')
  path=target/('F'+str(i)+'.png');image.save(path);mask.save(aux/('F'+str(i)+'-mask.png'));depth.save(aux/('F'+str(i)+'-depth.png'));normal.save(aux/('F'+str(i)+'-normal.png'));limbid.save(aux/('F'+str(i)+'-limbID.png'));image.resize((128,128),Image.Resampling.LANCZOS).save(runtime/('F'+str(i)+'.png'));frames.append(image)
  toes={};contacts={}
  for side in ('LEFT','RIGHT'):
   f=p['feet'][side];toes[side]=project_vertices(local_world([f['toe']]))[0,:2].tolist();contacts[side]={'mode':f['mode'],'toeLocal3D':f['toe'].tolist(),'toeWorld3D':f['worldToe'].tolist(),'heelLocal3D':f['heel'].tolist(),'ankleLocal3D':f['ankle'].tolist(),'pitchDegrees':math.degrees(f['pitchRad'])}
  records.append({'frame':i,'phase':i/8,'path':'frames/F'+str(i)+'.png','runtimePath':'runtime128/F'+str(i)+'.png','durationMs':durations[i],'startMs':cumulative,'sourceCanvas':[256,256],'sourcePivot':[128,237],'alphaBounds':list(alpha),'actualAlphaHeight':height,'declaredHeightForFixedReviewScale':REFERENCE_HEIGHT,'toeScreenSourceXY':toes,'contacts':contacts,'sha256':sha(path),'mesh':geo});cumulative+=durations[i]
 atlas=Image.new('RGBA',(128*4,128*2));atlas_source=Image.new('RGBA',(256*4,256*2))
 for i,im in enumerate(frames):atlas.alpha_composite(im.resize((128,128),Image.Resampling.LANCZOS),((i%4)*128,(i//4)*128));atlas_source.alpha_composite(im,((i%4)*256,(i//4)*256))
 atlas.save(BASE/'atlas-runtime128.png');atlas_source.save(BASE/'atlas-source256.png')
 meta={'status':'REAL_ORIGINAL_3D_EIGHT_FRAME_PILOT_PENDING_REVIEW','direction':'D07 screenEast/worldNEtheta315','sourceCanvas':[256,256],'sourcePivot':[128,237],'runtimeCell':[128,128],'runtimePivot':[64,118.5],'durationsMs':durations,'totalDurationMs':sum(durations),'exactModelPeriodMs':PERIOD*1000,'referenceCharacterHeight':REFERENCE_HEIGHT,'sourceCharacterHeight':REFERENCE_HEIGHT,'targetReviewHeights':[64,80,96],'fixedWholeCanvasReviewSizes':{str(h):round(256*h/REFERENCE_HEIGHT) for h in [64,80,96]},'reviewActualHeightRanges':{str(h):[min(r['actualAlphaHeight'] for r in records)*round(256*h/REFERENCE_HEIGHT)/256,max(r['actualAlphaHeight'] for r in records)*round(256*h/REFERENCE_HEIGHT)/256] for h in [64,80,96]},'rootTravelModelPerCycle':STRIDE,'rootTravelWorldPerCycle':STRIDE*GAME_PX_PER_MODEL/WORLD_PX_PER_UNIT,'groundSpeedScreenPxSec':SCREEN_SPEED,'frameRecords':records,'auxEncoding':{'mask':'binary actual geometry silhouette, excludes stylized outline','depth':'16bit same fixed near/far map: depthUnit=(-1+3*(pixel-1)/65534);0background','normal':'world unit normal encoded127.5*(n+1),alpha silhouette','limbID':IDS},'identityAccepted':False,'motionAccepted':False,'runtimeIntegrated':False,'sourceCutoutsUsed':False,'imageGenerationCalls':0}
 (BASE/'animation.json').write_text(json.dumps(meta,indent=2)+'\n');gate=create_previews(frames,meta)
 outputfiles=[p for p in BASE.rglob('*') if p.is_file() and p.suffix in ('.png','.apng','.gif','.json','.csv') and p.name!='receipt.json' and 'pre-scale-224' not in p.parts];receipt={'status':'PILOT_RENDERED_EIGHT_HOLD_CONTACT_GATE_FAILED' if not gate['heldSpriteContactPass'] else 'PILOT_RENDERED_PENDING_IDENTITY_MOTION_REVIEW','sourceReferenceSha256':REFERENCE_SHA,'sideReferenceSha256':sha(side_reference),'renderer':'actual articulated3D custommesh CPU numpy/PIL zbuffer','meshVertices':records[0]['mesh']['vertices'],'meshTriangles':records[0]['mesh']['triangles'],'frames':8,'sourceCanvas':[256,256],'sourceAlphaHeightRange':[min(r['actualAlphaHeight'] for r in records),max(r['actualAlphaHeight'] for r in records)],'footGeometryContact':'actual sole mesh bottom toe at local[0,.13,0]; toe-pivot transforms foot, ankle thenconstantlegIK','numericContactGate':True,'heldSpriteGate':gate,'identityAccepted':False,'motionAccepted':False,'cadenceAccepted':False,'camera54x27ReconciliationAccepted':False,'runtimeIntegrated':False,'sourceCutoutsUsed':False,'imageGenerationCalls':0,'scriptSha256':sha(__file__),'limitations':['Hand-authored toon reconstruction is visually different from painterly identity; likeness/style pendingparent review.','Fast337ms cadence is speed/stride hypothesis, not visual timing approval.','Eight held sprites have measured ground slip despite exact continuousrig contact.','Camera26.565 physical ortho ground ratio.4472 differs from2:1runtime grid.','No smooth cloth simulation, skinning deformation or shading-texture bake; bone-attached custommeshes and deterministic cloth shape.','A partial anatomy/tool assertion does not establish identity or motion qualification.'],'outputs':{str(p.relative_to(BASE)):sha(p) for p in outputfiles}}
 (BASE/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({'status':receipt['status'],'frames':8,'alphaHeightRange':receipt['sourceAlphaHeightRange'],'heldSlipMaxPx':gate['actual60HzSameContactMaxSlipPx']}))

if __name__=='__main__' and len(sys.argv)>1 and sys.argv[1]=='build':build()
