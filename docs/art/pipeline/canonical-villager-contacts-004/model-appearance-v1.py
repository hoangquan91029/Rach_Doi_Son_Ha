"""Copied frozen001 geometry: ONLYstride.64->1.28,hip.90->.84,upperbody/head/hat/arms carrieddown.06. No cutouts or style changes."""
import argparse,csv,hashlib,json,math,pathlib,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
BASE=pathlib.Path(__file__).resolve().parent
REFERENCE=pathlib.Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha/docs/art/characters/villager-neutral-D01-screen-South-007/raw.png')
REFERENCE_SHA='68a7fb9a71ae614f7c01432b1270e7a25071975667cfdf082ae02326d97678db'
ALPHA=math.atan(.5);C,S=math.cos(ALPHA),math.sin(ALPHA);STRIDE=1.28;STANCE=.60;SOURCE_SCALE=128.;REFERENCE_HEIGHT=233.;GAME_PX_PER_MODEL=SOURCE_SCALE*80/REFERENCE_HEIGHT;WORLD_PX_PER_UNIT=54/math.sqrt(2)*1.08;WORLD_SPEED=2.1;SCREEN_SPEED=WORLD_SPEED*WORLD_PX_PER_UNIT;PERIOD=STRIDE*GAME_PX_PER_MODEL/SCREEN_SPEED
E=np.array([1,-1,0.])/math.sqrt(2);D=np.array([1,1,0.])/math.sqrt(2);Z=np.array([0.,0.,1.]);BASIS=np.stack([-D,E,Z],axis=1)
COLORS={'cloth':(214,195,158),'cloth_light':(230,211,174),'cloth_shadow':(179,157,123),'trousers':(91,75,61),'sash':(80,65,57),'sash_light':(104,85,71),'skin':(174,115,76),'skin_light':(198,139,91),'hat':(192,157,93),'hat_dark':(143,105,57),'hair':(37,31,25),'eye':(37,25,19),'eye_white':(216,195,152),'strap':(98,64,32),'sole':(111,79,38)}
IDS={'tunic':1,'hat':2,'head':3,'LEFT_thigh':4,'RIGHT_thigh':5,'LEFT_shin':6,'RIGHT_shin':7,'LEFT_foot':8,'RIGHT_foot':9,'LEFT_arm':10,'RIGHT_arm':11,'LEFT_hand':12,'RIGHT_hand':13,'sash':14}
GEOMETRY_PREFLIGHT_ONLY=False

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
  f=foot(t,side);H=np.array([sign*.105+sway,0.,.84+bob]);K=ik(H,f['ankle']);p['feet'][side]=f;p['joints'][side+'_hip']=H;p['joints'][side+'_knee']=K;p['joints'][side+'_ankle']=f['ankle']
  # Opposite arm to leading leg, with slightly bent constant-length elbow.
  phi=(-1 if side=='LEFT' else 1)*.32*math.cos(2*math.pi*t);shoulder=np.array([sign*.225+sway,0.,1.29+bob]);elbow=shoulder+.255*unit([sign*.08,math.sin(phi),-math.cos(phi)]);wrist=elbow+.235*unit([-sign*.03,math.sin(phi+.10),-math.cos(phi+.10)])
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

class Mesh:
 def __init__(self):self.v=[];self.n=[];self.tri=[];self.color=[];self.ids=[]
 def add(self,verts,faces,material,limb,variations=None):
  verts=np.array(verts,dtype=float);normals=np.zeros_like(verts);faces=np.array(faces,dtype=int)
  if not GEOMETRY_PREFLIGHT_ONLY:
   for a,b,c in faces:
    normal=np.cross(verts[b]-verts[a],verts[c]-verts[a]);normals[a]+=normal;normals[b]+=normal;normals[c]+=normal
   lengths=np.linalg.norm(normals,axis=1);normals/=np.maximum(lengths[:,None],1e-15)
  offset=len(self.v);self.v.extend(verts);self.n.extend(normals);self.tri.extend(faces+offset)
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
 m=Mesh();b=p['bob'];sx=p['sway'];offset=np.array([sx,0,b-.06]);shift=lambda v:np.array(v)+offset
 # Complete wrapped tunic: a longer, low-frequency drape reaches the knee line.
 # The pelvis-following shell is continuous across phases; legs keep their locked tracks.
 skirt_rings=[(.44,.328,.218),(.49,.333,.224),(.57,.318,.216),(.68,.285,.195),(.79,.251,.174),(.84,.232,.157),(.96,.184,.122),(1.04,.207,.139),(1.22,.257,.146),(1.36,.262,.129),(1.40,.135,.097)]
 m.ring_form([(shift([0,0,z]),rx,ry) for z,rx,ry in skirt_rings],'cloth','tunic',N=32,fold=.075,front_open_below=.70)
 # Wrapped front lapels and seam: layered geometry retains V neckline.
 m.strip([shift([-.13,.142,1.38]),shift([-.045,.160,1.22]),shift([.06,.154,1.08]),shift([.12,.133,.96])],.037,'cloth_light','tunic',widthaxis=[.82,0,.57])
 m.strip([shift([.13,.140,1.38]),shift([.04,.161,1.23])],.034,'cloth_light','tunic',widthaxis=[.84,0,-.55])
 # Long overlapping wrap panels and broad seams. Keep the folds low-frequency at game size.
 for points,width,material in [
  ([[-.18,.194,.96],[-.19,.210,.82],[-.17,.222,.66],[-.15,.230,.50],[-.13,.224,.45]],.118,'cloth_light'),
  ([[.10,.190,.96],[.13,.203,.82],[.16,.214,.66],[.18,.218,.51],[.19,.210,.47]],.105,'cloth_shadow'),
  ([[-.04,.222,.94],[.00,.229,.78],[.025,.236,.62],[.05,.235,.49]],.080,'cloth_light')]:
  m.strip([shift(v) for v in points],width,material,'tunic',widthaxis=[0,1,0])
 # Sculpted broad hem folds (not a repeated fine texture).
 for x in [-.23,-.12,.04,.17,.25]:m.strip([shift([x,.205,.49]),shift([x*.92,.197,.63]),shift([x*.82,.174,.77])],.016,'cloth_shadow','tunic')
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
 # Layered woven brim with a readable dark underside lip, rather than a single flat rim.
 m.ring_form([(shift([0,0,1.671]),.391,.391),(shift([0,0,1.681]),.410,.410),(shift([0,0,1.693]),.414,.414)],'hat_dark','hat',N=36)
 for z in np.linspace(1.738,1.924,7):
  r=.412*(1.947-z)/(1.947-1.710)+.003;m.ring_form([(shift([0,0,z]),r,r),(shift([0,0,z+.003]),r-.005,r-.005)],'hat_dark','hat',N=36)
 for a in np.linspace(0,2*math.pi,18,endpoint=False):
  pts=[shift([r*math.cos(a),r*math.sin(a),z]) for z,r in [(1.716,.414),(1.784,.296),(1.855,.180),(1.930,.031)]];m.rod(pts,.0026,'hat_dark','hat')
 # Near-side brim lift is deterministic original geometry, not a source warp.
 for idx in range(hat_start,len(m.v)):
  v=np.array(m.v[idx]);relative=v-offset;v[0]=offset[0]+relative[0]*.75;v[1]=offset[1]+relative[1]*.86;v[2]+=-.42*(v[0]-sx)+.16*v[1];m.v[idx]=v
 # Recompute hat normals after authored mesh tilt/shape (uniform across all poses).
 if not GEOMETRY_PREFLIGHT_ONLY:
  for i in range(hat_start,len(m.v)):m.n[i]=np.zeros(3)
  for tri in m.tri:
   if min(tri)<hat_start:continue
   a,bb,c=tri;normal=np.cross(np.array(m.v[bb])-m.v[a],np.array(m.v[c])-m.v[a]);
   for i in tri:m.n[i]+=normal
  for i in range(hat_start,len(m.v)):m.n[i]=unit(m.n[i]) if np.linalg.norm(m.n[i])>1e-15 else np.zeros(3)
 # Bone-driven original trouser/sleeve/skin meshes, stitched cuff rings.
 for side,sign in [('LEFT',-1),('RIGHT',1)]:
  j=p['joints'];H=j[side+'_hip'];K=j[side+'_knee'];A=j[side+'_ankle'];shoulder=j[side+'_shoulder'];elbow=j[side+'_elbow'];wrist=j[side+'_wrist'];thigh=side+'_thigh';shin=side+'_shin';arm=side+'_arm';hand=side+'_hand';footid=side+'_foot'
  # Loose brown trousers continue below the knee and gather into a soft cuff.
  m.tube(H,K,[(0,.115,.117),(.14,.158,.145),(.38,.168,.150),(.67,.153,.142),(.91,.123,.116),(1,.104,.103)],'trousers',thigh,N=20,fold=.095)
  m.tube(H,K,[(.92,.125,.118),(.96,.130,.120),(1,.108,.108)],'sash_light',thigh,N=20)
  cuff=K+.66*(A-K)
  m.tube(K,cuff,[(0,.092,.088),(.18,.111,.103),(.40,.119,.108),(.66,.102,.096),(.90,.083,.080),(1,.078,.077)],'trousers',shin,N=18,fold=.075)
  m.tube(K,cuff,[(.90,.084,.081),(.95,.093,.089),(1,.081,.079)],'sash_light',shin,N=18)
  # Pale gathered leg wraps begin below the trousers; broad folds echo the reference.
  m.tube(cuff,A,[(0,.080,.078),(.10,.084,.081),(.34,.073,.069),(.62,.065,.061),(.86,.058,.055),(1,.052,.051)],'cloth',shin,N=18,fold=.065)
  for t in [.12,.31,.51,.72,.89]:
   center=cuff+t*(A-cuff);m.tube(center,A,[(0,.073*(1-t)+.052*t,.069*(1-t)+.051*t),(.035,.073*(1-t)+.052*t,.069*(1-t)+.051*t)],'cloth_shadow',shin,N=18)
  m.tube(cuff+.04*(A-cuff),cuff+.09*(A-cuff),[(0,.086,.083),(.55,.088,.084),(1,.082,.080)],'sash_light',shin,N=18)
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
  normals=wa[...,None]*n[tri[0]]+wb[...,None]*n[tri[1]]+wc[...,None]*n[tri[2]];normals/=np.maximum(np.linalg.norm(normals,axis=2)[...,None],1e-15);diff=np.clip(normals@light,0,1)
  # Continuous diffuse response replaces the pilot's four hard normal-light bands.
  # A small broad fill keeps cream cloth and warm skin legible in a side-view silhouette.
  shade=.54+.49*diff
  col=np.clip(colors[i]*shade[...,None],0,255)
  zbuf[y0:y1+1,x0:x1+1][mask]=zz[mask];rgb[y0:y1+1,x0:x1+1][mask]=col[mask];normalbuf[y0:y1+1,x0:x1+1][mask]=normals[mask];idbuf[y0:y1+1,x0:x1+1][mask]=ids[i]
 mask=idbuf>0
 # Thin original sprite contour, material and geometry preserved; no reference image operations.
 adjacent=np.zeros_like(mask)
 for dy,dx in [(1,0),(-1,0),(0,1),(0,-1)]:adjacent|=np.roll(np.roll(mask,dy,0),dx,1)
 outline=adjacent&~mask;rgba=np.zeros((256,256,4),dtype=np.uint8);rgba[:,:,:3]=rgb.astype(np.uint8);rgba[:,:,3][mask]=255;rgba[:,:,:3][outline]=[57,45,31];rgba[:,:,3][outline]=230
 depth=np.zeros((256,256),dtype=np.uint16);depth[mask]=np.clip((zbuf[mask]+1)/3*65534+1,1,65535).astype(np.uint16);normals=np.zeros((256,256,4),dtype=np.uint8);normals[:,:,:3][mask]=np.clip((normalbuf[mask]+1)*127.5,0,255).astype(np.uint8);normals[:,:,3][mask]=255
 return Image.fromarray(rgba),Image.fromarray((mask*255).astype(np.uint8)),Image.fromarray(depth),Image.fromarray(normals),Image.fromarray(idbuf),{'vertices':len(v),'triangles':len(tris),'geometryBounds':proj[:,:2].min(axis=0).tolist()+proj[:,:2].max(axis=0).tolist()}
