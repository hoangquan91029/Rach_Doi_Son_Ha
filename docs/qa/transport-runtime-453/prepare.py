from pathlib import Path
import json,hashlib,shutil,subprocess,urllib.request,stat
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');O=R/'docs/qa/transport-runtime-453';S=Path('/tmp/rds-transport453-stage');B=Path('/tmp/rds-transport453-build')
O.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def inv(p):return {str(f.relative_to(p)):{'sha256':sha(f),'bytes':f.stat().st_size,'mode':stat.S_IMODE(f.stat().st_mode)} for f in sorted(p.rglob('*')) if f.is_file() and not f.is_symlink()}
def preserve():return {'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'canonical':{n:inv(R/n) for n in ['client','shared','server','public']},'public451':inv(R/'dist'),'backend230':inv(Path.home()/'.local/share/rach-doi-son-ha/releases/230/runtime230'),'pid3229CmdlineSHA':sha('/proc/3229/cmdline'),'pid3229EnvironmentSHA':sha('/proc/3229/environ'),'health':json.load(urllib.request.urlopen('http://127.0.0.1:3000/health'))}
def dump(n,v):(O/n).write_text(json.dumps(v,indent=2)+'\n')
before=preserve();assert before['head']=='39e3eb08a18479ffce671a4b3e8994ba4159bee2';assert len(before['public451'])==209;assert before['health']['ok'];assert not S.exists() and not B.exists();dump('preservation-before.json',before)
for n in ['client','shared','server','public','tests']:shutil.copytree(R/n,S/n)
for n in ['index.html','vite.config.js','package.json','package-lock.json']:shutil.copy2(R/n,S/n)
(S/'node_modules').symlink_to(R/'node_modules',target_is_directory=True)
routes=S/'client/art-routes.js';oldroutes=routes.read_text();foodline=" food:Object.freeze({manifestUrl:'/assets/art-v1/food-099-manifest.json',world:false}),\n";assert oldroutes.count(foodline)==1;routes.write_text(oldroutes.replace(foodline,''))
for f in ['assets/art-v1/food-099-manifest.json','assets/art-v1/food-099/atlas.png']:(S/'public'/f).unlink()
fort='assets/art-v1/fort-202-manifest.json';f=S/'public'/fort;text=f.read_text();original=json.loads(text);assert len(original['assets'])==50;assert original==json.loads((R/'dist'/fort).read_text());a=json.loads((R/'docs/art/units/transport-identity-447/descriptor.json').read_text());assert a['family']=='unit.transport' and a['runtime']['sha256']=='d3cbc022df157c74d9d6cad5051cdc2836fa1b68bac3a65764b443e4d2755eba';assert a['render']=={'width':78,'height':78} and a['pivot']=={'x':128,'y':166.4,'space':'source'}
# Locate assets closing bracket without rewriting any old row bytes.
pos=text.index('[',text.index('"assets"'))+1;decoder=json.JSONDecoder();ranges=[]
while True:
 while text[pos].isspace() or text[pos]==',':pos+=1
 if text[pos]==']':break
 start=pos;row,end=decoder.raw_decode(text,pos);ranges.append([start,end]);pos=end
assert len(ranges)==50
insertion=',\n'+json.dumps(a,indent=2)+'\n';newtext=text[:pos].rstrip()+insertion+text[pos:];f.write_text(newtext);new=json.loads(newtext);assert new['assets'][:50]==original['assets'];assert len(new['assets'])==51
# rstrip removes only whitespace immediately before closing assets bracket, never old asset objects.
assert all(newtext[s:e]==text[s:e] for s,e in ranges)
runtime=S/'public/assets/art-v1'/a['runtime']['path'];runtime.parent.mkdir(exist_ok=False);shutil.copy2(R/'docs/art/units/transport-identity-447/runtime-128.png',runtime);assert sha(runtime)==a['runtime']['sha256']
for rel,pin in before['public451'].items():
 if rel in ['index.html',fort]:continue
 target=S/'public'/rel
 if target.exists():assert sha(target)==pin['sha256'],rel
 else:target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/'dist'/rel,target)
assert not any('food-099' in str(f.relative_to(S/'public')) for f in (S/'public').rglob('*') if f.is_file())
for n in ['shared','server']:assert inv(S/n)==before['canonical'][n]
after=preserve();assert after==before;dump('preservation-after.json',after);dump('stage-inventory.json',inv(S));dump('old50-row-byte-ranges.json',{'source':str(R/'public'/fort),'sourceSHA':sha(R/'public'/fort),'byteRanges':ranges,'unchanged':True});dump('source-binding.json',{'stage':str(S),'build':str(B),'head':before['head'],'boatDescriptorSHA':sha(R/'docs/art/units/transport-identity-447/descriptor.json'),'boatRuntimeSHA':sha(runtime),'fortManifestSHA':sha(f),'sourcePins':{n:inv(S/n) for n in ['client','shared','server','public']},'oldPublic451':before['public451']})
pre={'status':'PREPARED_WAIT_FOCUSED_CONTRACTS','cwd':str(S),'outDir':str(B),'config':str(S/'vite.config.js'),'configSHA256':sha(S/'vite.config.js'),'stageFortSHA256':sha(f),'assets':51,'old50JSONAndRowBytesUnchanged':True,'retained209Public451ExceptIndexFort':True,'sourcePixelChanges':False,'simulationChanges':False,'soleStageCodeDifference':'Remove only LOCALfood route line as public451; all other canonical code bytes copied unchanged','stageOnlyRemoved':['food recipe','food099 manifest','food099 atlas'],'addedRuntime':str(runtime),'buildOutputMustNotExist':not B.exists(),'buildCalls':0,'browserCalls':0,'installationCalls':0,'guards':'CLOSED'};dump('preflight.json',pre);shutil.copy2('/tmp/transport453_prepare.py',O/'prepare.py');print(json.dumps(pre))
