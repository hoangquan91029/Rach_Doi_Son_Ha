"""Install only the accepted, byte-bound corner family; never build or deploy."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess

ROOT = Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha')
STAGE = Path('/tmp/rds-corners266-stage')
BUILD = Path('/tmp/rds-corners266-build')
QA = ROOT / 'docs/qa/wall-corners-install-268'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inventory(path):
    return {str(p.relative_to(path)): sha(p) for p in sorted(path.rglob('*')) if p.is_file()}

def read(path):
    return json.loads(path.read_text())

# The two actual UI scenes are independent gates. No prepared or technical-only
# receipt may satisfy these root intakes.
for folder in ['wall-corners-runtime-266b', 'wall-corners-firefox-267']:
    intake = read(ROOT / 'docs/qa' / folder / 'root-intake.json')
    assert intake['status'].startswith('ROOT_ACCEPTED_NARROW_')

binding = read(ROOT / 'docs/qa/wall-corners-runtime-266/binding.json')
assert binding['stage'] == str(STAGE) and binding['build'] == str(BUILD)
assert inventory(BUILD) == read(ROOT / 'docs/qa/wall-corners-runtime-266/build-pins.json')
assert {name: inventory(ROOT / name) for name in binding['canonical']} == binding['canonical']
assert {name: inventory(STAGE / name) for name in binding['stageInventories']} == binding['stageInventories']

manifest_rel = 'assets/art-v1/fort-202-manifest.json'
old = read(ROOT / 'public' / manifest_rel)
new = read(STAGE / 'public' / manifest_rel)
assert len(old['assets']) == 43 and len(new['assets']) == 46
assert new['assets'][:43] == old['assets']
assert {k: v for k, v in new.items() if k != 'assets'} == {k: v for k, v in old.items() if k != 'assets'}
assert sha(STAGE / 'public' / manifest_rel) == binding['manifestSHA256']

public_before = inventory(ROOT / 'dist')
source_before = {name: inventory(ROOT / name) for name in ['client', 'shared', 'server']}
before = inventory(ROOT / 'public')
added = []
for asset, mask, checkpoint in zip(new['assets'][43:], [6, 9, 10], [263, 264, 265]):
    assert asset['fortification'] == {'mask': mask}
    assert asset['pivot'] == {'x': 627, 'y': 900, 'space': 'source'}
    assert asset['render'] == {'width': 42.3225, 'height': 42.3225}
    source = ROOT / f'docs/art/buildings/wall-corner{mask}-idle-{checkpoint}'
    assert sha(source / 'raw.png') == asset['source']['sha256']
    assert sha(source / 'runtime.png') == asset['runtime']['sha256']
    rel = 'assets/art-v1/' + asset['runtime']['path']
    assert rel == f'assets/art-v1/corner-{checkpoint}/idle.png'
    staged = STAGE / 'public' / rel
    assert sha(staged) == asset['runtime']['sha256']
    target = ROOT / 'public' / rel
    assert not target.exists()
    target.parent.mkdir()
    shutil.copy2(staged, target)
    added.append(rel)
shutil.copy2(STAGE / 'public' / manifest_rel, ROOT / 'public' / manifest_rel)

after = inventory(ROOT / 'public')
assert set(after) - set(before) == set(added)
assert all(after[key] == value for key, value in before.items() if key != manifest_rel)
assert all(after[key] == binding['stageInventories']['public'][key] for key in after if key not in binding['removedPendingFood'])
assert inventory(ROOT / 'dist') == public_before
assert {name: inventory(ROOT / name) for name in source_before} == source_before
receipt = {
    'status': 'INSTALLED_EXACT_TESTED_WHOLE_CORNERS_46_LOCAL_ONLY',
    'sourceHEAD': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
    'addedPaths': added, 'manifestSHA256': sha(ROOT / 'public' / manifest_rel),
    'old43DescriptorsExact': True, 'wholeSourcesAndRuntimeBytesExact': True,
    'frozenBuildExact': True, 'public260Unchanged': True,
    'clientSharedServerUnchanged': True, 'builds': 0, 'productionMutations': 0,
    'scope': 'Only living completed idle corner masks6/9/10; no state/T/cross/mixed-gate or character motion acceptance.',
}
(QA / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(receipt['status'])
