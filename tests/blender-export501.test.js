import test from 'node:test';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
for (const scenario of ['background-reload','interactive-reject','wrong-file-reject']) {
  test(`Blender 5 saved state: ${scenario}`, () => {
    const code = String.raw`
import importlib.util,sys,tempfile
from pathlib import Path
from types import SimpleNamespace as N
spec=importlib.util.spec_from_file_location('m','scripts/blender/export_job.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
with tempfile.TemporaryDirectory() as d:
 p=Path(d)/'saved.blend'; calls=[]; case=sys.argv[1]
 def reopen(**kw):calls.append(kw)
 b=N(data=N(filepath=str(p),is_dirty=True),app=N(background=case!='interactive-reject'),ops=N(wm=N(open_mainfile=reopen)))
 if case=='wrong-file-reject':b.data.filepath=str(Path(d)/'other.blend')
 try:m.saved_background_state(b,p)
 except ValueError as e:
  assert case!='background-reload'; assert str(e)==('unsaved Blender data forbidden' if case=='interactive-reject' else 'opened blend mismatch');assert not calls
 else:assert case=='background-reload';assert calls==[{'filepath':str(p),'use_scripts':False}]
`;
    const result=spawnSync('python3',['-c',code,scenario],{encoding:'utf8'});
    assert.equal(result.status,0,result.stdout+result.stderr);
  });
}
