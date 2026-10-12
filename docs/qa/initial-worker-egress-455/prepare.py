from pathlib import Path
import hashlib,json,shutil,subprocess,stat,urllib.request
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');O=R/'docs/qa/initial-worker-egress-455';S=Path('/tmp/rds-egress455-stage')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def inv(p):return {str(f.relative_to(p)):sha(f) for f in sorted(p.rglob('*')) if f.is_file() and not f.is_symlink()}
def preserve():return {'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'canonical':{n:inv(R/n) for n in ['client','shared','server','public']},'public451':inv(R/'dist'),'backend230':inv(Path.home()/'.local/share/rach-doi-son-ha/releases/230/runtime230'),'pid3229CmdlineSHA':sha('/proc/3229/cmdline'),'pid3229EnvironmentSHA':sha('/proc/3229/environ'),'health':json.load(urllib.request.urlopen('http://127.0.0.1:3000/health')),'baseline':sha(O/'baseline.json')}
before=preserve();assert before['head'].startswith('39e3eb0');assert not S.exists();(O/'preservation-before.json').write_text(json.dumps(before,indent=2)+'\n')
for n in ['shared','tests']:shutil.copytree(R/n,S/n)
shutil.copy2(R/'package.json',S/'package.json');f=S/'shared/sim.js';text=f.read_text();old='const goal=[...e.path].reverse().find(q=>dist(e,q)<=4&&dist(e,q)>1)||e.path[0];';new='const goal=[...e.path].reverse().find(q=>dist(e,q)<=4&&dist(e,q)>1&&(q===e.path.at(-1)||crowdSweep(s,e,q,q,true)))||e.path[0];';assert text.count(old)==1;f.write_text(text.replace(old,new));assert preserve()==before;print('Candidate only, single occupied nonterminal goal filter written')
