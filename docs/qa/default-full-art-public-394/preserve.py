from pathlib import Path
import json,hashlib,subprocess,urllib.request,sys
root=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');out=root/'docs/qa/default-full-art-public-394';runtime=Path('/home/kieu-hoang-quan/.local/share/rach-doi-son-ha/releases/230/runtime230')
def inv(base):return {str(p.relative_to(base)):{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'mode':oct(p.stat().st_mode&0o777)} for p in sorted(base.rglob('*')) if p.is_file() and not p.is_symlink()}
pins={'HEAD':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'canonical':{n:inv(root/n) for n in ['client','shared','server','public']},'publicDist':inv(root/'dist'),'runtime':{n:inv(runtime/n) for n in ['server','shared']},'pid3229':Path('/proc/3229/cmdline').read_bytes().decode().replace('\0',' '),'health':json.load(urllib.request.urlopen('http://127.0.0.1:3000/health'))}
assert pins['HEAD']=='2b16979393716bc056e205f8fc50eaea07db0593';assert pins['health']=={'ok':True,'rooms':0};assert len(pins['publicDist'])==201
binding=json.loads((root/'docs/qa/default-full-art-runtime-389/binding.json').read_text());assert pins['publicDist']==binding['buildPins']
mode=sys.argv[1];assert mode in ['before','after']
if mode=='after':assert pins==json.loads((out/'preservation-before.json').read_text())
(out/('preservation-'+mode+'.json')).write_text(json.dumps(pins,indent=2)+'\n');print('394 preservation '+mode+' PASS201/HEAD/PID3229/rooms0')
