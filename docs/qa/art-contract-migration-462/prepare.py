from pathlib import Path
import hashlib,json,shutil,subprocess,urllib.request
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');O=R/'docs/qa/art-contract-migration-462';S=Path('/tmp/rds-art-contract462-stage');sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def inv(p):return {str(f.relative_to(p)):sha(f) for f in sorted(p.rglob('*')) if f.is_file() and not f.is_symlink()}
def preserve():return {'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'canonical':{n:inv(R/n) for n in ['client','shared','server','public','tests']},'public451':inv(R/'dist'),'backend230':inv(Path.home()/'.local/share/rach-doi-son-ha/releases/230/runtime230'),'456custody':inv(R/'docs/qa/egress-semantic-456'),'original177fixture':inv(R/'docs/qa/navigation-cache-177/baseline'),'reference340SHA':sha(R/'docs/qa/terrain-install-340/before/public/assets/art-v1/fort-202-manifest.json'),'pidSHA':sha('/proc/3229/cmdline'),'health':json.load(urllib.request.urlopen('http://127.0.0.1:3000/health'))}
before=preserve();assert before['head']=='0bfefd60a1db811a451554fea3ff83238886f73b';assert not S.exists();(O/'preservation-before.json').write_text(json.dumps(before,indent=2)+'\n')
for n in ['client','shared','server','public','scripts','tests']:shutil.copytree(R/n,S/n)
for n in ['package.json','package-lock.json','index.html','vite.config.js']:shutil.copy2(R/n,S/n)
for n in ['docs','node_modules','dist']:(S/n).symlink_to(R/n,target_is_directory=True)
files=json.loads((R/'docs/qa/egress-semantic-456/failing-control-files.json').read_text());assert len(files)==12
for rel in files:
 d=O/'original'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,d)
(O/'input-pins.json').write_text(json.dumps({'files':{f:sha(R/f) for f in files},'historical340ManifestSHA':before['reference340SHA'],'rationaleSHA':sha(O/'migration-rationale.md')},indent=2)+'\n');assert preserve()==before;print(S)
