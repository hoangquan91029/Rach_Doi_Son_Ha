"""Finite207 paired public deployment. No build or canonical source edits."""
from pathlib import Path
import ctypes, hashlib, json, os, re, shutil, subprocess, sys, tarfile, time, urllib.request

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
BASE = Path('/home/kieu-hoang-quan/.local/share/rach-doi-son-ha/releases/207')
DROP = Path('/home/kieu-hoang-quan/.config/systemd/user/rach-doi-son-ha.service.d/207-release.conf')
UNIT = 'rach-doi-son-ha.service'
NODE = Path('/home/kieu-hoang-quan/.nvm/versions/node/v24.15.0/bin/node')
URL = 'https://kieu-hoang-quan-loq-15iax9.tail5247a0.ts.net'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
read = lambda p: json.loads(p.read_text())
def inventory(root):
    return {str(p.relative_to(root)): sha(p) for p in sorted(root.rglob('*')) if p.is_file()}
def write(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2) + '\n')
def ctl(*args):
    return subprocess.check_output(['systemctl', '--user', *args], text=True)
def health():
    return json.loads(urllib.request.urlopen('http://127.0.0.1:3000/health', timeout=10).read())
def empty():
    assert health() == {'ok': True, 'rooms': 0}, 'Active rooms prohibit rollout/rollback'
def ready():
    deadline = time.monotonic() + 10
    while True:
        try:
            empty()
            return
        except (OSError, TimeoutError):
            if time.monotonic() >= deadline:
                raise
            time.sleep(.2)
def override(runtime):
    DROP.parent.mkdir(parents=True, exist_ok=True)
    tmp = DROP.with_suffix('.tmp')
    tmp.write_text(f'[Service]\nWorkingDirectory={runtime}\nExecStart=\nExecStart={NODE} {runtime}/server/index.js\n')
    tmp.replace(DROP)
def exchange(a, b):
    lib = ctypes.CDLL(None, use_errno=True)
    fn = lib.renameat2
    fn.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
    fn.restype = ctypes.c_int
    if fn(-100, os.fsencode(a), -100, os.fsencode(b), 2):
        raise OSError(ctypes.get_errno(), 'renameat2 exchange')
def freeze(runtime, source, expected_sim):
    runtime.mkdir()
    for folder in ['server', 'shared']:
        shutil.copytree(source / folder, runtime / folder)
    for name in ['package.json', 'package-lock.json']:
        shutil.copy2(source / name, runtime / name)
    shutil.copytree(ROOT / 'node_modules/ws', runtime / 'node_modules/ws')
    (runtime / 'dist').symlink_to(ROOT / 'dist', target_is_directory=True)
    assert sha(runtime / 'shared/sim.js') == expected_sim
    # Smoke the immutable module/dependency closure on an ephemeral private port.
    code = "const {createGameServer}=await import('./server/index.js');const g=await createGameServer({port:0});const h=await(await fetch('http://127.0.0.1:'+g.server.address().port+'/health')).json();if(!h.ok||h.rooms!==0)throw Error('health');await g.close();"
    subprocess.run([str(NODE), '--input-type=module', '-e', code], cwd=runtime, check=True, timeout=20)
    # Record source and dependencies separately; do not traverse the dist symlink.
    result = {'server': inventory(runtime / 'server'), 'shared': inventory(runtime / 'shared'), 'ws': inventory(runtime / 'node_modules/ws'), 'package': {n: sha(runtime/n) for n in ['package.json','package-lock.json']}}
    for p in runtime.rglob('*'):
        if p.is_symlink():
            continue
        p.chmod(0o555 if p.is_dir() else 0o444)
    runtime.chmod(0o555)
    return result
def prepare():
    binding = read(ROOT / 'docs/qa/public-candidate-206/source-build-binding.json')
    prior = read(ROOT / 'docs/qa/candidate-release-204/bindings.json')
    stage, build = Path(binding['stage']), Path(binding['outdir'])
    assert inventory(build) == binding['build']
    for rel, digest in binding['sources'].items():
        assert sha(stage / rel) == digest, rel
    assert not DROP.exists() and not BASE.exists(), 'Do not repeat prepared207'
    empty()
    assert 'MainPID=157023' in ctl('show', UNIT, '-p', 'MainPID', '-p', 'ActiveState')
    old = inventory(ROOT/'dist')
    expected = read(ROOT/'docs/qa/public-candidate-206/public149-before.json')
    assert all(k.startswith('dist/') for k in expected)
    assert old == {k.removeprefix('dist/'): v for k, v in expected.items()}
    old_source = Path(prior['rollback']['oldRunnableSource'])
    for rel, digest in prior['rollback']['moduleHashes'].items():
        assert sha(old_source / rel) == digest, rel
    BASE.mkdir(parents=True)
    old_runtime = freeze(BASE/'runtime149', old_source, prior['active']['loadedSimSHA256'])
    new_runtime = freeze(BASE/'runtime206', stage, binding['sources']['shared/sim.js'])
    shutil.copytree(ROOT/'dist', BASE/'dist149')
    shutil.copytree(build, BASE/'dist206')
    retained = []
    for rel, digest in old.items():
        if rel == 'index.html':
            continue
        dst = BASE/'dist206'/rel
        if dst.exists():
            assert sha(dst) == digest, f'Unexpected asset collision: {rel}'
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT/'dist'/rel, dst)
            retained.append(rel)
    for rel in ['assets/art-v1/food-099-manifest.json', 'assets/art-v1/food-099/atlas.png']:
        assert not (BASE/'dist206'/rel).exists()
    archive = BASE/'rollback149.tar.gz'
    with tarfile.open(archive, 'w:gz') as t:
        t.add(BASE/'dist149', arcname='dist')
        for folder in ['server', 'shared', 'node_modules']:
            t.add(BASE/'runtime149'/folder, arcname=folder)
        for name in ['package.json', 'package-lock.json']:
            t.add(BASE/'runtime149'/name, arcname=name)
        t.add(Path('/home/kieu-hoang-quan/.config/systemd/user')/UNIT, arcname='original-service')
    archive.chmod(0o444)
    empty()
    assert inventory(ROOT/'dist') == old
    write('prepared.json', {'status':'PREPARED_NOT_PROMOTED','base':str(BASE),'node':str(NODE),'nodeSHA256':sha(NODE),'oldInventory':old,'newInventory':inventory(BASE/'dist206'),'candidateInventory':binding['build'],'retained':retained,'oldRuntime':old_runtime,'newRuntime':new_runtime,'rollbackArchive':str(archive),'rollbackArchiveSHA256':sha(archive),'oldUnitSHA256':prior['active']['unitSHA256'],'foodCharacterExcluded':True,'defaultArtDisabled':True,'D0NotInstalled':True,'sourceUntouched':True,'dependencyLimit':'Both snapshots freeze current ws8.22.0; historical process dependency bytes are not claimed recovered'})
def promote():
    p = read(OUT/'prepared.json')
    assert p['status'] == 'PREPARED_NOT_PROMOTED'
    assert inventory(ROOT/'dist') == p['oldInventory']
    assert inventory(BASE/'dist206') == p['newInventory']
    assert sha(NODE) == p['nodeSHA256'] and sha(Path(p['rollbackArchive'])) == p['rollbackArchiveSHA256']
    assert sha(Path('/home/kieu-hoang-quan/.config/systemd/user')/UNIT) == p['oldUnitSHA256']
    assert not DROP.exists()
    assert ctl('show', UNIT, '-p', 'DropInPaths').strip() == 'DropInPaths='
    for name, key in [('runtime149','oldRuntime'), ('runtime206','newRuntime')]:
        for folder in ['server','shared']:
            assert inventory(BASE/name/folder) == p[key][folder]
        assert inventory(BASE/name/'node_modules/ws') == p[key]['ws']
        assert all(sha(BASE/name/f) == h for f,h in p[key]['package'].items())
    empty()
    before = ctl('show', UNIT, '-p', 'MainPID', '-p', 'ActiveState')
    assert 'MainPID=157023' in before
    ctl('stop', UNIT)
    exchange(ROOT/'dist', BASE/'dist206')
    override(BASE/'runtime206')
    ctl('daemon-reload')
    ctl('start', UNIT)
    ready()
    assert inventory(ROOT/'dist') == p['newInventory']
    index = urllib.request.urlopen(URL+'/', timeout=20).read()
    assert hashlib.sha256(index).hexdigest() == p['candidateInventory']['index.html']
    chunk = re.search(r'/assets/index-[^" ]+\.js', index.decode()).group()
    data = urllib.request.urlopen(URL+chunk, timeout=20).read()
    assert hashlib.sha256(data).hexdigest() == p['candidateInventory'][chunk.lstrip('/')]
    write('promotion.json', {'status':'PROMOTED_AWAIT_RELEVANT_TLS_UI','oldService':before,'service':ctl('show', UNIT, '-p','MainPID','-p','ActiveState','-p','WorkingDirectory','-p','ExecStart'),'runtime':str(BASE/'runtime206'),'simSHA256':sha(BASE/'runtime206/shared/sim.js'),'publicChunk':chunk,'bundleSHA256':hashlib.sha256(data).hexdigest(),'distFiles':len(p['newInventory']),'health':health(),'atomic':'renameat2 RENAME_EXCHANGE','rollbackReady':True,'canonicalSourceEdits':0,'foodCharacterExcluded':True,'D0MotionApproval':False})
def rollback():
    p = read(OUT/'prepared.json')
    empty()
    assert inventory(BASE/'dist206') == p['oldInventory']
    ctl('stop', UNIT)
    exchange(ROOT/'dist', BASE/'dist206')
    override(BASE/'runtime149')
    ctl('daemon-reload')
    ctl('start', UNIT)
    ready()
    assert inventory(ROOT/'dist') == p['oldInventory']
    write('rollback.json', {'status':'ROLLED_BACK_PAIRED149','runtime':str(BASE/'runtime149'),'simSHA256':sha(BASE/'runtime149/shared/sim.js'),'health':health(),'service':ctl('show', UNIT,'-p','MainPID','-p','ActiveState'),'canonicalSourceEdits':0})
if __name__ == '__main__':
    assert sys.argv[1:] in [['prepare'], ['promote'], ['rollback']]
    {'prepare':prepare,'promote':promote,'rollback':rollback}[sys.argv[1]]()
