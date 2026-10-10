from pathlib import Path
from PIL import Image
import json,math,hashlib
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');Q=R/'docs/qa/wall-corner-pick-diagnosis-273';B=Path('/tmp/rds-corners266-build')
r=json.loads((R/'docs/qa/wall-corners-firefox-267/browser-receipt.json').read_text());c=r['failure']['camera'];m=json.loads((B/'assets/art-v1/fort-202-manifest.json').read_text());ents=r['failure']['visibleBuildings'];z=c['zoom'];assets={};images={}
for e in ents:
 if e['type']=='wall':
  mask=next(t['mask'] for t in r['topology'] if t['id']==e['id']);a=next(a for a in m['assets'] if a['family']=='building.wall' and a.get('fortification',{}).get('mask')==mask)
 else:a=next(a for a in m['assets'] if a['kind']=='building' and a['family'] in [e['type'],'building.'+e['type']])
 path=B/'assets/art-v1'/a['runtime']['path'];assert hashlib.sha256(path.read_bytes()).hexdigest()==a['runtime']['sha256'];assets[e['id']]=a;images[e['id']]=Image.open(path).getchannel('A')
def project(e):return (640+(e['x']-e['y'])*54*z/2-(c['x']-c['y'])*54*z/2,400+(e['x']+e['y']-c['x']-c['y'])*27*z/2)
def sample(x,y):
 out=[]
 for e in sorted(ents,key=lambda e:(-(e['x']+e['y']),-e['id'])):
  a=assets[e['id']];w=a['render']['width']*z;h=a['render']['height']*z;px,py=project(e);left=px-a['pivot']['x']/a['source']['width']*w;top=py-a['pivot']['y']/a['source']['height']*h;u=math.floor((x-left)/w*a['cell']['width']);v=math.floor((y-top)/h*a['cell']['height']);alpha=images[e['id']].getpixel((u,v)) if 0<=u<images[e['id']].width and 0<=v<images[e['id']].height else 0
  out.append({'id':e['id'],'type':e['type'],'runtimePixel':[u,v],'alpha':alpha})
 return out
def pick(x,y):return next((s['id'] for s in sample(x,y) if s['alpha']>=80),None)
e=next(e for e in ents if e['id']==51);px,py=project(e);probes=[];first=None
for dy in [-15,-24,-8,-32,0]:
 for dx in [0,-4,4]:
  x,y=px+dx*z,py+dy*z;p={'offset':[dx,dy],'point':[x,y],'fractionalPick':pick(x,y),'FirefoxFloorPoint':[math.floor(x),math.floor(y)],'FirefoxFloorPick':pick(math.floor(x),math.floor(y))};probes.append(p)
  if first is None and p['fractionalPick']==51:first={**p,'fractionalSamples':sample(x,y),'FirefoxFloorSamples':sample(math.floor(x),math.floor(y))}
data={'method':'Read-only pinned PNG alpha sampling and recorded buildings/camera; no browser/game state injection','camera':c,'canvasAssumed':[1280,800],'recordedTarget':51,'recordedFailureSelection':r['failure']['selection'],'project':project(e),'firstSuccessfulFractionalProbe':first,'probes':probes,'limits':['267 did not persist attempted thirdpoint or actual event clientcoordinates','Failure snapshot has buildings+builder only; other units and precise click-time rendererframe not retained','Pillow source alpha should agree with canvas same128RGBA decoding, exact JavaScript arithmetic separately checked']};(Q/'reconstruction.json').write_text(json.dumps(data,indent=2));print(json.dumps(data,indent=2)[:4500])
