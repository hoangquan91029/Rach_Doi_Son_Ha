#!/usr/bin/env python3
"""195 root-selected whole PNG gate; reuse017 atlas +014/012 APNG packaging only."""
import argparse,hashlib,importlib.util,json,sys,copy
from pathlib import Path
from PIL import Image
sys.dont_write_bytecode=True
ROOT=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');PACKAGE=Path(__file__).resolve().parent
ATLAS=ROOT/'docs/art/pipeline/pure2d-action-adapter-017/export-v3.py'
APNG=ROOT/'docs/art/pipeline/pure2d-loop-preview-012/export-apng.py'
sha=lambda b:hashlib.sha256(b).hexdigest()
def require(ok,msg):
 if not ok:raise ValueError(msg)
def pinned_file(value,expected=None):
 p=(ROOT/value).resolve() if not Path(value).is_absolute() else Path(value).resolve()
 require(p.is_relative_to(ROOT/'docs/art') and p.is_file(),'Missing/outside art custody file: '+str(p))
 h=sha(p.read_bytes());require(expected is None or h==expected,'Changed custody hash: '+str(p));return p,h
def validate_tool_role(role,data,index,source_path,source_hash):
 if role=='call-state.json':
  require(data.get('call_open') is not True,'Open/unfinished tool call forbidden')
  slot=data.get('F'+str(index))
  closed=data.get('state')=='returned_closed' or data.get('call_open') is False or (isinstance(slot,str) and slot.startswith('returned_closed'))
  require(closed,'Open/unfinished tool call forbidden')
 if role=='receipt.json':
  raw=data.get('raw_sha256',data.get('rawSha256'))
  slots=data.get('slots')
  if slots is not None:
   matches=[s for s in slots if s.get('slot') in ['F'+str(index),f'F{index:02d}']]
   require(len(matches)==1,'Missing/ambiguous tool receipt slot')
   slot=matches[0];raw=slot.get('sha256')
   require(pinned_file(slot['raw'])[0]==source_path,'Tool receipt slot source mismatch')
  require(raw is not None and raw==source_hash,'Tool receipt raw SHA mismatch')
def source_binding(frame,index):
 selection=frame.get('selection','');status=frame.get('selectionStatus')
 require(isinstance(selection,str) and selection.strip() and not any(x in selection.lower() for x in ['held','unselected','rejected','pending','missing']),'Missing/held/unselected frame selection: F'+str(index))
 desired='SELECTED_KEY_CANDIDATE' if index%2==0 else 'SELECTED_INBETWEEN_CANDIDATE'
 require(status is None or status==desired,'Unselected/held slot status: F'+str(index))
 require(not any(k in frame for k in ['crop','trim','offset','transform','scale','mirror','warp','pivot']),'Per-frame fitting forbidden')
 p,h=pinned_file(frame['source'],frame['sha256']);require(p.suffix.lower()=='.png','Actual whole PNG required')
 with Image.open(p) as im:
  require(im.size==(1254,1254) and im.mode=='RGBA','Exact1254 RGBA whole original required');rgba=sha(im.tobytes())
 supplied=frame.get('toolReceipts')
 if supplied is None:
  supplied=[{'path':str(p.parent/name)} for name in ['tool-request.json','call-state.json','receipt.json']]
 require(isinstance(supplied,list) and len(supplied)>=3,'Actual request/call-state/receipt custody required')
 tools=[];roles=set()
 for record in supplied:
  tp,th=pinned_file(record['path'],record.get('sha256'));data=json.loads(tp.read_text());role=record.get('role',tp.name);roles.add(role);tools.append({'path':str(tp),'sha256':th,'role':role});validate_tool_role(role,data,index,p,h)
 require({'tool-request.json','call-state.json','receipt.json'}.issubset(roles),'Missing request/call-state/receipt roles')
 return {'frame':index,'source':{'path':str(p),'sha256':h,'rgbaSha256':rgba,'width':1254,'height':1254},'selectionStatus':desired,'selection':selection,'toolReceipts':tools}
def gate(ledger_path):
 lp=Path(ledger_path).resolve();j=json.loads(lp.read_text());frames=j.get('frames',[])
 require(len(frames)==8 and [f.get('frame') for f in frames]==list(range(8)),'Exactly8 ordered actual root-selected sources required; no partial preview')
 require(j.get('status')=='ROOT_SELECTED_ACTUAL_EIGHT_SOURCES_FOR_PREVIEW_ONLY' and j.get('selectedBy')=='root','Explicit root selected-eight ledger required')
 require(j.get('sourceCanvas')==[1254,1254] and j.get('pivotSource')==[654,1140] and j.get('runtimeCell')==[128,128] and j.get('previewCell')==[89,89] and j.get('durationMs')==600 and j.get('frameMs')==[75]*8,'Fixed canvas/pivot/cell/timing mismatch')
 keys=json.loads((PACKAGE/'key-pins-192.json').read_text());by_index={f['frame']:f for f in keys['frames']}
 bindings=[];seen=set()
 for i,f in enumerate(frames):
  if i in by_index:require(pinned_file(f.get('source'))[0]==pinned_file(by_index[i]['source'])[0] and f.get('sha256')==by_index[i]['sha256'],'Changed selected192 key: F'+str(i))
  b=source_binding(f,i);require(b['source']['rgbaSha256'] not in seen,'Duplicate whole frame forbidden');seen.add(b['source']['rgbaSha256']);bindings.append(b)
 return {'path':str(lp),'sha256':sha(lp.read_bytes()),'declaration':j,'bindings':bindings}
def load_helper(name,p):
 spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def build(ledger_path,out):
 g=gate(ledger_path);pins=json.loads((PACKAGE/'helper-pins.json').read_text());require(all(sha((ROOT/name).read_bytes())==h for name,h in pins.items()),'Frozen packaging helper changed');out=Path(out).resolve();require(out.is_relative_to(PACKAGE) and not out.exists(),'New output only inside213 package');a=load_helper('atlas017',ATLAS);p=load_helper('apng012',APNG)
 # Existing014 shadow contract; no new texture, pixels or body fitting.
 legacy=json.loads((ROOT/'docs/art/pipeline/pure2d-loop-preview-014/atlas-job.json').read_text());job={k:copy.deepcopy(legacy[k]) for k in ['camera','contactShadow','shadowDependency','wholeCanvasTransform','sourceMethod']}
 job.update(id='villager-walk-D0-pilot-213',family='unit.villager',state='walk',direction=0,sourceCanvas=[1254,1254],runtimeCell=[128,128],renderSize=[89,89],pivot=[654,1140],columns=8,gutter=0,loop=True,technicalFixture=False,frames=[])
 # Gate completes BEFORE creating even normalized selection metadata or outputs.
 out.mkdir();(out/'root-selected-ledger.json').write_bytes(Path(ledger_path).read_bytes());(out/'selection').mkdir()
 for b in g['bindings']:
  i=b['frame'];receipt={'status':b['selectionStatus'],'frameIndex':i,'sourceSha256':b['source']['sha256'],'rgbaSha256':b['source']['rgbaSha256'],'rootLedgerSha256':g['sha256'],'rootLedgerPath':g['path'],'rootSelection':b['selection'],'limits':'Derived custody record from explicit root ledger; not motion/owner/release approval'}
  rp=out/'selection'/f'F{i}.json';rp.write_text(json.dumps(receipt,indent=2)+'\n');job['frames'].append({'index':i,'phase':f'F{i}','durationMs':75,'events':[],'source':b['source'],'selectionStatus':b['selectionStatus'],'selectionReceipt':{'path':str(rp),'sha256':sha(rp.read_bytes())}})
 jp=out/'atlas-job.json';jp.write_text(json.dumps(job,indent=2)+'\n');a.export(jp,out/'compiled');compiled=out/'compiled';apng_job={'compiledDirectory':str(compiled),'manifestSha256':sha((compiled/'manifest.json').read_bytes()),'previewSha256':sha((compiled/'preview.json').read_bytes()),'nominalHeight':80,'referenceHeight':1130};ap=out/'apng-job.json';ap.write_text(json.dumps(apng_job,indent=2)+'\n');p.build(ap,out/'playback')
 for b in g['bindings']:
  pinned_file(b['source']['path'],b['source']['sha256'])
  for t in b['toolReceipts']:pinned_file(t['path'],t['sha256'])
 require(sha(Path(ledger_path).read_bytes())==g['sha256'],'Root ledger changed during export')
 r={'status':'ACTUAL_SELECTED_EIGHT_TECHNICAL_PREVIEW_ONLY','rootLedger':{'path':g['path'],'sha256':g['sha256']},'sourceBindings':g['bindings'],'helpers':{str(ATLAS):sha(ATLAS.read_bytes()),str(APNG):sha(APNG.read_bytes())},'sourceCanvas':[1254,1254],'pivotSource':[654,1140],'runtimeCell':[128,128],'presentationCell':[89,89],'atlasSize':[1024,128],'durationsMs':[75]*8,'cycleMs':600,'events':[],'outputs':{str(f.relative_to(out)):sha(f.read_bytes()) for f in out.rglob('*') if f.is_file()},'imageCalls':0,'limits':'Packing/uniform whole exports only; local stationary preview, no ordinary gameplay/world foot-lock/runtime/motion/owner/continuous visual approval'};(out/'receipt.json').write_text(json.dumps(r,indent=2)+'\n');return r
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('ledger');parser.add_argument('--output');args=parser.parse_args()
 if args.output:print(json.dumps(build(args.ledger,args.output),indent=2))
 else:print(json.dumps(gate(args.ledger),indent=2))
