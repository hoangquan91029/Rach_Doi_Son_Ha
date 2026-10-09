#!/usr/bin/env python3
"""Read-only rejection contracts. No selected-eight fixture or image export."""
import copy,importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
here=Path(__file__).resolve().parent;spec=importlib.util.spec_from_file_location('export195',here/'export.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
keys=json.loads((here/'key-pins-192.json').read_text());base=keys['frames'][0];checks=[]
def rejected(label,fn,fragment):
 try:fn()
 except ValueError as error:assert fragment in str(error);checks.append({'contract':label,'result':'REJECTED_AS_REQUIRED','reason':str(error)})
 else:raise AssertionError(label+' incorrectly accepted')
rejected('actual current four keys cannot become eight-frame output',lambda:m.gate(here/'key-pins-192.json'),'Exactly8')
binding=m.source_binding(base,0);assert binding['source']['sha256']==base['sha256'];checks.append({'contract':'selected actual F0 custody read-only','result':'PINNED_ONLY_NOT_EXPORTED'})
f=copy.deepcopy(base);f['selection']='HELD';rejected('held selection',lambda:m.source_binding(f,0),'held')
f=copy.deepcopy(base);f['selectionStatus']='UNSELECTED';rejected('unselected status',lambda:m.source_binding(f,0),'Unselected')
f=copy.deepcopy(base);f['sha256']='0'*64;rejected('changed raw hash',lambda:m.source_binding(f,0),'Changed custody hash')
f=copy.deepcopy(base);f['offset']=[1,0];rejected('per-frame shift metadata',lambda:m.source_binding(f,0),'fitting forbidden')
ledger=json.loads((m.ROOT/'docs/art/pipeline/villager-walk-D0-contact-192/pilot-sequence-195.json').read_text())
for i in [1,5,7]:
 b=m.source_binding(ledger['frames'][i],i);checks.append({'contract':f'actual custom receipt roles F{i}', 'result':'VALIDATED_CLOSED_HASH_BOUND'})
f=ledger['frames'][5];p,h=m.pinned_file(f['source'],f['sha256'])
rejected('explicit open custom call overrides closed state',lambda:m.validate_tool_role('call-state.json',{'call_open':True,'state':'returned_closed'},5,p,h),'Open/')
data=json.loads((m.ROOT/f['toolReceipts'][2]['path']).read_text());data['slots'][0]['sha256']='0'*64
rejected('custom slot receipt wrong raw hash',lambda:m.validate_tool_role('receipt.json',data,5,p,h),'raw SHA mismatch')
print(json.dumps({'status':'PREPARATION_GATE_CONTRACTS_PASS_NO_LOOP_OUTPUT','checks':checks,'framesExported':0,'imageCalls':0},indent=2))
