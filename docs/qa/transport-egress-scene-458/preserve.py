from pathlib import Path
import json,hashlib,subprocess,urllib.request,sys
r=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');p=r/'docs/qa/transport-egress-scene-458'
def inventory(q):return {str(f.relative_to(q)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(q.rglob('*')) if f.is_file() and not f.is_symlink()}
snap=dict(head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip(),source={n:inventory(r/n) for n in ['client','shared','server','public']},dist=inventory(r/'dist'),backend=inventory(Path('/home/kieu-hoang-quan/.local/share/rach-doi-son-ha/releases/230/runtime230')),sealed453Stage=inventory(Path('/tmp/rds-transport453-stage')),sealed453Build=inventory(Path('/tmp/rds-transport453-build')),sealed457Stage=inventory(Path('/tmp/rds-transport457-stage')),sealed457Build=inventory(Path('/tmp/rds-transport457-build')),productionPid=subprocess.check_output(['ps','-p','3229','-o','pid=,args='],text=True).strip(),productionHealth=json.load(urllib.request.urlopen('http://127.0.0.1:3000/health')))
(p/('preservation-'+sys.argv[1]+'.json')).write_text(json.dumps(snap,indent=2))
if sys.argv[1]=='after':assert snap==json.loads((p/'preservation-before.json').read_text())
print(json.dumps(dict(head=snap['head'],productionHealth=snap['productionHealth'],phase=sys.argv[1])))
