import test from 'node:test';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
// Fixtures are synthetic validation records, never actual selected artwork or Blender proof.
const python = String.raw`
import importlib.util,tempfile,json,hashlib,copy,sys
from pathlib import Path
spec=importlib.util.spec_from_file_location('exporter','scripts/blender/export_job.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
with tempfile.TemporaryDirectory() as d:
 root=Path(d)
 def pin(name):
  (root/name).write_bytes(name.encode());return {'path':name,'sha256':m.digest(root/name)}
 j={'schema':'rds-blender-job/v1','id':'synthetic-test','identity':'villager','action':'idle','direction':1,'original':pin('original.png'),'view':pin('view.png'),'blend':pin('asset.blend'),'selection':{'scene':'Scene','model':'Model','rig':'Rig','camera':'Camera','action':'Idle','renderCollection':'Character','renderMeshes':['Model','Hat']},'layout':{'fixedCanvas':{'width':256,'height':256},'cell':{'width':128,'height':128},'pivot':{'space':'source','x':128,'y':232},'render':{'width':42,'height':42},'contactShadow':{'mode':'baked'},'camera':{'projection':'dimetric','ratio':[2,1],'tile':[54,27],'elevation':26.565}},'frames':[{'slot':i,'blenderFrame':i+1,'phase':i/4,'durationMs':100,'status':'candidate'} for i in range(4)],'loop':True,'output':'new-output','candidate':True}
 q={'schema':'rds-blender-selection/v1','status':'qualified','bindings':{k:j[k] for k in ('identity','action','direction','original','view','blend','selection','layout','frames','loop')},**{k:'VERIFIED' for k in ('identityReview','modelReview','rigReview','cameraReview')}}
 (root/'qualification.json').write_text(json.dumps(q));j['qualification']={'path':'qualification.json','sha256':m.digest(root/'qualification.json')}
 plan=m.validate(j,root)
 case=sys.argv[1]
 if case=='valid':
  assert plan['acceptance']['blenderExecution']=='UNKNOWN' and len(plan['mapping'])==4
 elif case=='projection':
  b=plan['orthographicBasis'];scale=b['worldPixelScale']
  for x,y in ((1,0),(0,1),(1,1),(-1,1)):
   sx=scale*(b['right'][0]*x+b['right'][1]*y);sy=-scale*(b['up'][0]*x+b['up'][1]*y)
   assert abs(sx-27*(x-y))<1e-10 and abs(sy-13.5*(x+y))<1e-10
 elif case=='world':
  ident=[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
  assert m.world_signature(ident)==(1,1,1)
  m.fixed_world_signature(ident,(1,1,1))
 elif case in ('worldmirror','worldscale','extramesh','outsidecollection'):
  ident=[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
  try:
   if case=='worldmirror':ident[0][0]=-1;m.world_signature(ident)
   elif case=='worldscale':ident[0][0]=2;m.fixed_world_signature(ident,(1,1,1))
   elif case=='extramesh':m.render_members(['Model','Hat','Foreign'],['Model','Hat'],['Model','Hat'])
   else:m.render_members(['Model','Hat'],['Model','Hat'],['Model'])
  except ValueError as e:
   assert str(e)=={'worldmirror':'mirrored or singular evaluated world transform','worldscale':'animated evaluated world scale forbidden','extramesh':'render-visible mesh allowlist mismatch','outsidecollection':'allowlisted mesh outside selected collection'}[case]
  else:raise AssertionError('invalid matrix/allowlist accepted')
 else:
  mutations={
   'pin':lambda: j['blend'].update(sha256='0'*64),
   'escape':lambda:j.update(output='../escape'),
   'absolute':lambda:j.update(output='/tmp/escape'),
   'action':lambda:j.update(action='run'),
   'direction':lambda:j.update(direction=True),
   'frame':lambda:j['frames'][1].update(slot=0),
   'fit':lambda:j['frames'][0].update(pivot={'x':1}),
   'phase':lambda:j['frames'][1].update(phase=.9),
   'status':lambda:j['frames'][0].update(status='selected'),
   'qualification':lambda:j['selection'].update(rig='Other'),
   'unknown':lambda:j.update(eval='arbitrary'),
   'overwrite':lambda:(root/'new-output').mkdir(),
   'symlink':lambda:((root/'link').symlink_to(root.parent),j.update(output='link/escape')),
   'timing':lambda:j['frames'][0].update(durationMs=float('nan')),
   'canvas':lambda:j['layout']['fixedCanvas'].update(width=1024,height=1024),
   'continuousloop':lambda:j.update(loop=False),
   'finiteloop':lambda:(j.update(action='hit',loop=True),j['selection'].update(action='Hit')),
   'duplicateallowlist':lambda:j['selection'].update(renderMeshes=['Model','Model'])}
  expected={'pin':'input pin mismatch','escape':'path escape','absolute':'relative path required','action':'known canonical applicable action required','direction':'engine direction required','frame':'exact candidate frame slot/timing required','fit':'exact candidate frame slot/timing required','phase':'exact candidate frame slot/timing required','status':'exact candidate frame slot/timing required','qualification':'source-bound selected model/rig/camera qualification required','unknown':'exact job schema required','overwrite':'output exists or overlaps input','symlink':'path escape','timing':'exact candidate frame slot/timing required','canvas':'v1 fixed source canvas must be 256 square','continuousloop':'action loop policy mismatch','finiteloop':'action loop policy mismatch','duplicateallowlist':'exact selected Blender names required'}
  mutations[case]()
  # Refresh fixture qualification for malformed job tests so intended guard is reached.
  if case != 'qualification':
   q['bindings']={k:j[k] for k in ('identity','action','direction','original','view','blend','selection','layout','frames','loop')}
   (root/'qualification.json').write_text(json.dumps(q));j['qualification']['sha256']=m.digest(root/'qualification.json')
  try:m.validate(j,root)
  except ValueError as e:assert str(e)==expected[case],str(e)
  else:raise AssertionError('invalid input accepted: '+case)
`;
for(const name of ['valid','projection','pin','escape','absolute','action','direction','frame','fit','phase','status','qualification','unknown','overwrite','symlink','timing','canvas','continuousloop','finiteloop','duplicateallowlist','world','worldmirror','worldscale','extramesh','outsidecollection']){
 test(`Blender candidate validation: ${name}`,()=>{const r=spawnSync('python3',['-c',python,name],{encoding:'utf8'});assert.equal(r.status,0,r.stderr);});
}
