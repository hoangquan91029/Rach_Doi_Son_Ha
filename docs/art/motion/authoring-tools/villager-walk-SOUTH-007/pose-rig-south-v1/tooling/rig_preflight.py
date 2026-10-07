"""Preparation-only geometry/custody gate. Raster baking is NOT implemented."""
import hashlib,json,math,pathlib,sys
BASE=pathlib.Path(__file__).resolve().parents[1]
CONTRACT_SHA='52202bc716ce0d82bc3cdef3c2e18c4cdba094f7a58dc5b6c75e5c7ccf883421'
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(pathlib.Path(p).read_text())
def project(p):return [654+p[0],1140+.5*p[1]-p[2]]
def bone_plane(a,b,L):
 v=[(b[i]-a[i])/L for i in range(3)]
 if abs(sum(x*x for x in v)-1)>1e-8:raise ValueError('bone length changed')
 w=[(1 if i==0 else 0)-v[0]*v[i] for i in range(3)]; n=math.sqrt(sum(x*x for x in w))
 if n<1e-6:raise ValueError('singular bone plane')
 w=[x/n for x in w]
 return [w[0],.5*w[1]-w[2],v[0],.5*v[1]-v[2],*project(a)]
def geometry(plan):
 if plan['canvas']!=[1254,1254] or plan['root']!=[654,1140]:raise ValueError('camera mismatch')
 fs={f['frame']:f for f in plan['frames']}
 if set(fs)!={0,2,4,6}:raise ValueError('four keys required')
 result={}
 for k,f in fs.items():
  if f['support']!=('LEFT' if k<4 else 'RIGHT'):raise ValueError('support ownership')
  result[k]={};p=f['points3D']
  for side in ('LEFT','RIGHT'):
   for name,a,b,L in [('thigh','hip','knee',260),('shin','knee','ankle',240),('upperArm','shoulder','elbow',200),('forearm','elbow','wrist',180)]:result[k][side+'_'+name]=bone_plane(p[side+'_'+a],p[side+'_'+b],L)
   if abs(math.dist(p[side+'_heel'],p[side+'_toe'])-160)>1e-8:raise ValueError('foot length changed')
   result[k][side+'_foot']={x:project(p[side+'_'+x]) for x in ('heel','toe','ankle')}
 for a,b,side in [(0,2,'LEFT'),(4,6,'RIGHT')]:
  for e in ('worldHeel','worldToe'):
   if math.dist(fs[a]['soles'][side][e],fs[b]['soles'][side][e])>1e-8:raise ValueError('world support slides')
 return result

def inputs(contract,manifest):
 from PIL import Image
 required={p['id'] for p in contract['parts']};parts=manifest.get('parts',{})
 if set(parts)!=required:raise ValueError('missing real parts: '+','.join(sorted(required-set(parts))))
 for name,r in parts.items():
  if sha(r['sidecarPath'])!=r['sidecarSha256']:raise ValueError('sidecar custody mismatch')
  s=load(r['sidecarPath']);raw=s['raw']
  if s.get('status')!='SEALED_ORIGINAL_CALIBRATION':raise ValueError('unsealed calibration')
  if sha(raw['path'])!=raw['sha256']:raise ValueError('raw byte custody mismatch')
  with Image.open(raw['path']) as im:
   if im.mode!='RGBA' or list(im.size)!=[1254,1254]:raise ValueError('original canvas/mode')
   if hashlib.sha256(im.tobytes()).hexdigest()!=raw['rgbaSha256']:raise ValueError('RGBA custody mismatch')
  c=s['uniformRawToRest']
  if c['scale']<=0 or not all(math.isfinite(c[x]) for x in ('scale','rotationRad')) or len(c['translation'])!=2:raise ValueError('invalid uniform calibration')
  if not s.get('landmarks'):raise ValueError('missing landmarks')
  for v in s['landmarks'].values():
   if v.get('method') not in ('observed_original','authored_hidden_hypothesis') or len(v.get('xy',[]))!=2 or v.get('uncertaintyPx',-1)<0:raise ValueError('unresolved landmark')
  if 'lower_sandal' in name:
   for field,n in [('shinPolygon',3),('footPolygon',3),('sharedAnkleSeam',2)]:
    if len(s.get('mesh',{}).get(field,[]))<n:raise ValueError('unresolved independent shin/foot seam')
   if not {'knee','ankle','heel','toe','solePlane'}<=s['landmarks'].keys():raise ValueError('missing independent foot landmarks')
 for k in (0,2,4,6):
  order=manifest.get('layerOrderByKey',{}).get('F'+str(k),[])
  if len(order)!=9 or set(order)!=required:raise ValueError('per-pose layer order required')
def preflight(manifest_path,output):
 if pathlib.Path(output).exists():raise ValueError('refuse overwrite')
 cp=BASE/'part-contract-v2.json'
 if sha(cp)!=CONTRACT_SHA:raise ValueError('contract custody mismatch')
 c=load(cp);i=c['identity_lock']
 if sha(i['lock_path'])!=i['lock_sha256']:raise ValueError('identity custody mismatch')
 plan=BASE.parent/'pose-guides/walk-south-keys-v2/coordinate-plan.json'
 if sha(plan)!='c6499aebde1287abe2066de1dfcc3f6fc74bae9b0952452a34024e3da27c87bf':raise ValueError('sealed geometry custody mismatch')
 geometry(load(plan))
 inputs(c,load(manifest_path))
 raise ValueError('BAKER_NOT_IMPLEMENTED: independent foot-plane/seam rendering and illustration review pending')
if __name__=='__main__':
 try:preflight(sys.argv[1],sys.argv[2])
 except (ValueError,KeyError,FileNotFoundError,IndexError) as e:
  print(json.dumps({'status':'PREPARATION_ONLY_REFUSED','candidate':False,'reason':str(e),'outputsWritten':0,'imageCalls':0}));sys.exit(2)
