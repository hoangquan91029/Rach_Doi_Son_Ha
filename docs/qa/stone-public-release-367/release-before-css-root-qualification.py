#!/usr/bin/env python3
"""Uncalled finite stone release tooling. No build or backend mutation capability."""
from pathlib import Path,PurePosixPath
import argparse,ctypes,datetime,hashlib,json,os,re,shutil,stat,subprocess,tarfile,urllib.request
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');Q=R/'docs/qa/stone-public-release-367';TRIAL=R/'docs/qa/stone-fortification-runtime-361';PRIVATE=Path('/home/kieu-hoang-quan/.local/share/rach-doi-son-ha/releases/367');RB=Path('/home/kieu-hoang-quan/.local/share/rach-doi-son-ha/releases/353');L=Path('/home/kieu-hoang-quan/.local/share/rach-doi-son-ha/releases/230/runtime230');NEXT=R.parent/'rds-public367-next-dist';U='rach-doi-son-ha.service';ROLLBACK_SHA='c0d2133d8559b8115f7160621db4290b015fcfac789ac97d3350746539c62552'
def require(ok,message):
 if not ok:raise ValueError(message)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def write(name,value):(Q/name).write_text(json.dumps(value,indent=2)+'\n')
def tree(root):
 root=Path(root);result={}
 for p in [root,*sorted(root.rglob('*'))]:
  s=p.lstat();record={'mode':stat.S_IMODE(s.st_mode)}
  if p.is_symlink():record.update(type='symlink',target=os.readlink(p))
  elif p.is_dir():record.update(type='directory')
  elif p.is_file():record.update(type='file',sha256=sha(p),bytes=s.st_size)
  else:raise ValueError('Special file: '+str(p))
  result[str(p.relative_to(root))]=record
 return result
def inv(root):return {str(p.relative_to(root)):sha(p) for p in sorted(Path(root).rglob('*')) if p.is_file() and 'node_modules' not in p.parts}
def ctl(*args):return subprocess.check_output(['systemctl','--user',*args],text=True)
def service():return ctl('show',U,'-p','MainPID','-p','WorkingDirectory','-p','ActiveState')
def health():return json.load(urllib.request.urlopen('http://127.0.0.1:3000/health',timeout=5))
def verify_archive(path,rootname,expected,extract=None):
 with tarfile.open(path) as archive:
  members=archive.getmembers();entries={}
  for member in members:
   name=PurePosixPath(member.name);require(not name.is_absolute() and '..' not in name.parts and name.parts[0]==rootname,'Unsafe archive name')
   key=str(Path(member.name).relative_to(rootname));require(key not in entries,'Duplicate archive entry');entries[key]=member
   require(member.isfile() or member.isdir() or member.issym(),'Special or hardlinked archive entry')
   if member.issym():
    target=PurePosixPath(member.linkname);resolved=os.path.normpath(str(name.parent/target));require(not target.is_absolute() and (resolved==rootname or resolved.startswith(rootname+'/')),'Escaping symlink')
  require(set(entries)==set(expected),'Archive entry inventory differs')
  for key,record in expected.items():
   member=entries[key];require(member.mode==record['mode'],'Archive modes differ')
   if record['type']=='file':require(member.isfile() and hashlib.sha256(archive.extractfile(member).read()).hexdigest()==record['sha256'],'Archive file differs')
   elif record['type']=='directory':require(member.isdir(),'Archive directory differs')
   else:require(member.issym() and member.linkname==record['target'],'Archive symlink differs')
  if extract is not None:
   extract=Path(extract);require(not extract.exists(),'Extraction path already exists');extract.mkdir(mode=0o700);archive.extractall(extract,filter='data')
   for member in members:
    if member.isfile():(extract/member.name).chmod(member.mode)
   for member in sorted(members,key=lambda m:len(Path(m.name).parts),reverse=True):
    if member.isdir():(extract/member.name).chmod(member.mode)
   require(tree(extract/rootname)==expected,'Extracted bytes/modes differ')
def paired_guard(public=True):
 receipt=read(R/'docs/qa/mixed-gate-rollback-353/receipt.json');inventory=read(R/'docs/qa/mixed-gate-rollback-353/source-inventories.json')
 require(receipt['archiveSHA256']==ROLLBACK_SHA and sha(RB/'rollback345.tar.gz')==ROLLBACK_SHA,'Current345 rollback353 pin mismatch')
 require(tree(L)==inventory['immutableRuntime230'],'Immutable230 changed')
 if public:require(tree(R/'dist')==inventory['public345'],'Current public345 changed')
 require(sha(Path.home()/'.config/systemd/user'/U)==inventory['unitSHA256'],'Unit changed');require(tree(Path.home()/('.config/systemd/user/'+U+'.d'))==inventory['dropins'],'Dropins changed')
 state=service();pid=int(re.search(r'MainPID=(\d+)',state).group(1));require(pid==3229 and 'ActiveState=active' in state and str(L) in state,'Service identity changed')
 require(str(L/'server/index.js') in Path(f'/proc/{pid}/cmdline').read_bytes().decode().replace('\x00',' '),'Service runtime command changed')
 require(sha(Path(os.readlink(f'/proc/{pid}/exe')))==inventory['node']['sha256'],'Node changed')
 policy=ctl('show',U,'-p','FragmentPath','-p','DropInPaths','-p','EnvironmentFiles','-p','Environment','-p','ExecStart','-p','WorkingDirectory');require(hashlib.sha256(policy.encode()).hexdigest()==inventory['policySHA256'],'Service policy changed')
 require(hashlib.sha256(subprocess.check_output(['tailscale','serve','status','--json'])).hexdigest()==inventory['funnelSHA256'],'Funnel changed')
 require(all(sha(e['reference'])==e['sha256'] for e in read(RB/'rollback345/service-metadata/environment-references.json')),'Environment changed')
 require(health()=={'ok':True,'rooms':0},'Active rooms HOLD; never kick or restart')
 return {'service':state,'PID':pid,'rollbackSHA256':ROLLBACK_SHA}
def binding():
 b=read(Q/'binding.json');require(b['order']==367,'Wrong binding order')
 require(b['sourceBuildOrder']==368,'Only rootqualified368 source/build can release')
 require(all(Path(b[k]).is_absolute() and str(Path(b[k])).startswith('/tmp/rds-') and Path(b[k]).resolve()==Path(b[k]) and Path(b[k])!=R/'dist' for k in ['stage','build']),'Literal isolated source/build paths required')
 require(b['stage']!=b['build'],'Source and build must differ')
 require(sha(b['sealPath'])==b['sealSHA256'] and sha(b['rootIntakePath'])==b['rootIntakeSHA256'],'Seal/intake pin changed')
 require(b['rootActualSceneAccepted'] is True and b['trialClosed'] is True,'Actual scene intake/CLOSED required')
 seal=read(b['sealPath']);require(inv(Path(b['stage']))==seal['stage'] and inv(Path(b['build']))==seal['build'],'Sealed source/build changed')
 require(sha(b['actualReceiptPath'])==b['actualReceiptSHA256'] and sha(b['preservationReceiptPath'])==b['preservationReceiptSHA256'],'Actual368 receipts changed')
 require(read(b['preservationReceiptPath'])['preservationPASS'] is True,'Actual368 preservation failed')
 require(b['actualStoneEntityDrawsPASS'] is True and b['defaultStoneSampleEntityContractPASS'] is True,'Real defaultStone routeeligible sampleEntity/entityDraw proof required')
 require('368' in read(b['actualReceiptPath'])['status'] and read(b['actualReceiptPath'])['status'].startswith('PASS'),'Actual368 call must PASS and beclosed')
 require(sha(R/'docs/art/buildings/stone-wall-production-366/selected-bindings.json')==b['selected366SHA256'],'Three-source selection changed')
 require(b['normalTLSBase'].startswith('https://'),'Normal TLS base required');return b,seal

def material_guard(b,seal):
 build=Path(b['build']);old=read(R/'docs/qa/public-terrain-release-345/current-public-pins.json');new=seal['build'];ret=read(TRIAL/'retired-payload-removal.json')
 retired={v['stageRelativePath'].removeprefix('public/') for v in ret['files']};require(len(retired)==15,'Exact15 retired wood files required')
 extra=set(b['exactNonArtRemovedPaths']);require(extra=={'assets/index-Ct9S0o8d.css'},'Only exact sealed368 old CSS removal allowed');require(set(old)-set(new)==retired|extra,'Unexpected payload removal')
 for v in ret['files']:
  require(v['referencedByRetainedManifest'] is False and sha(TRIAL/v['custodyRelativePath'])==v['sha256'],'Retired wood custody mismatch')
  require(not (build/v['stageRelativePath'].removeprefix('public/')).exists(),'Retired wood payload still public')
 fort_path=b['fortManifestPath'];default_path=b['defaultStoneManifestPath'];fort=read(build/fort_path);default=read(build/default_path)
 require(len(fort['assets'])==37 and len(default['assets'])==8,'Expected fullfort37/defaultStone8')
 oldassets=read(R/'dist'/fort_path)['assets'];retained=[a for a in oldassets if a['family'] not in ('wall','gate','building.wall','building.gate')];require(len(retained)==29 and fort['assets'][:29]==retained,'Unrelated29 descriptors changed')
 stone=fort['assets'][29:];require(stone==default['assets'],'Default8 must equal exact fullfort stone8')
 require(all(a['material']=='stone' and a['kind']=='building' and a['family']=='building.wall' and a['state']=='idle' for a in stone),'Unexpected stone descriptor material/state')
 runtime={a['runtime']['path'] for a in stone};require(len(runtime)==3,'Only three authored stone images')
 selected=read(R/'docs/art/buildings/stone-wall-production-366/selected-bindings.json')['bindings'];selectedPins={x['runtime']['sha256'] for x in selected}
 require({a['runtime']['sha256'] for a in stone}==selectedPins,'Unselected source/runtime substitution')
 for a in stone:require(sha(build/'assets/art-v1'/a['runtime']['path'])==a['runtime']['sha256'],'Stone runtime bytes changed')
 newfiles=set(new)-set(old);expected={b['bundlePath'],default_path,*('assets/art-v1/'+p for p in runtime)};require(newfiles==expected,'Unexpected new public files')
 changed={p for p in set(old)&set(new) if old[p]!=new[p]};require(changed=={'index.html',fort_path},'Unexpected retained file change')
 for p in old:
  if p.startswith('assets/index-') and p.endswith('.js'):require(new.get(p)==old[p],'Old JS chunk retention policy violated')
 pending=set(read(R/'docs/qa/terrain-publicscope-342/source-bindings.json')['removedPending']);require(set(b['exactPendingExcludedPaths'])==pending,'Exact pending099/321 inventory required')
 require(all(not (build/p).exists() for p in pending),'Pending099/321 payload present')
 require(not any(a.get('fortification',{}).get('deathSite')=='completed' for a in fort['assets']),'Pending completedcollapse metadata present')
 require(b['pending099RecipeAbsentPASS'] is True,'Exact099 recipe exclusion contract required')
 require(b['defaultRouteContractPASS'] is True and b['unknownExplicitArtDisabledPASS'] is True,'DefaultStone/worldfalse and unknownroute contracts required')
 require(b['worldDefault'] is False,'BareURL stone route must not load world extras')
 return {'old':old,'new':new,'retired':sorted(retired),'tlsPins':['index.html',b['bundlePath'],fort_path,default_path,*sorted('assets/art-v1/'+p for p in runtime)]}
def tls(base,path):return hashlib.sha256(urllib.request.urlopen(base+'/'+('' if path=='index.html' else path),timeout=20).read()).hexdigest()
def go(kind):
 g=read(Q/('archive-go.json' if kind=='archive' else 'promotion-go.json'));require(g['order']==367 and g['status']==('PREPARE_STONE367_ROOT_GO' if kind=='archive' else 'PROMOTE_STONE367_ROOT_GO'),'Explicit finite rootGO missing');require(g['retries']==0,'No retry authorized')
 return g

def archive_candidate():
 go('archive');b,seal=binding();material=material_guard(b,seal);backend=paired_guard();require(not PRIVATE.exists(),'Private367 exists; no overwrite/replay')
 verify_archive(RB/'rollback345.tar.gz','rollback345',read(R/'docs/qa/mixed-gate-rollback-353/archive-inventory.json'))
 require(tree(RB/'verify-rollback345/rollback345')==read(R/'docs/qa/mixed-gate-rollback-353/archive-inventory.json'),'Retained paired rollback extraction differs')
 PRIVATE.mkdir(mode=0o700);dist=PRIVATE/'dist367';shutil.copytree(b['build'],dist,copy_function=shutil.copy2);require(inv(dist)==seal['build'],'Candidate clone differs')
 expected=tree(dist);archive=PRIVATE/'dist367.tar.gz'
 with tarfile.open(archive,'w:gz') as tar:tar.add(dist,arcname='dist367',recursive=True)
 archive.chmod(0o400);verify_archive(archive,'dist367',expected,PRIVATE/'verify-candidate')
 paired_guard();require(inv(Path(b['build']))==seal['build'] and inv(Path(b['stage']))==seal['stage'],'Seal changed during archive')
 write('candidate-tree.json',expected);write('build-pins.json',seal['build']);write('ready.json',{'status':'READY367_SAME_SEALED368_STONE_SEPARATE_PROMOTION_UNCALLED','candidateArchive':str(archive),'candidateArchiveSHA256':sha(archive),'rollbackArchive':str(RB/'rollback345.tar.gz'),'rollbackSHA256':ROLLBACK_SHA,'bindingSHA256':sha(Q/'binding.json'),'candidateFiles':len(seal['build']),'fortDescriptors':37,'defaultStoneDescriptors':8,'retiredWoodPayloads':15,'retainedLegacyJSChunks':True,'normalTLSPaths':material['tlsPins'],'backend':backend,'builds':0,'browsers':0,'promotions':0,'safeArchiveBytesModesExtractionVerified':True})
 print('READY367 same368 build, paired353 rollback verified; promotion uncalled')
def promote():
 go('promote');b,seal=binding();material=material_guard(b,seal);ready=read(Q/'ready.json');require(ready['bindingSHA256']==sha(Q/'binding.json'),'Ready binding drift');backend=paired_guard();require(backend==ready['backend'],'Service identity drift')
 dist=PRIVATE/'dist367';require(inv(dist)==seal['build'] and sha(ready['candidateArchive'])==ready['candidateArchiveSHA256'],'Prepared candidate changed')
 require(not NEXT.exists() and not (Q/'attempt.json').exists(),'Oneexchange already prepared/attempted; no replay')
 old=material['old'];beforePaths=['index.html',b['oldBundlePath'],b['fortManifestPath']];before={p:tls(b['normalTLSBase'],p) for p in beforePaths};require(all(before[p]==old[p] for p in before),'BeforeTLS does not match345');write('tls-before.json',before)
 shutil.copytree(dist,NEXT,copy_function=shutil.copy2);NEXT.chmod(0o755);require(stat.S_IMODE(NEXT.stat().st_mode)==0o755 and NEXT.stat().st_dev==(R/'dist').stat().st_dev,'Owned nextroot755/samefilesystem required');require(inv(NEXT)==seal['build'],'Nextclone bytes differ');write('nextclone.json',{'path':str(NEXT),'rootMode':'755','exactBuildBytes':True})
 paired_guard();binding();require(inv(NEXT)==seal['build'],'Nextclone drift');write('attempt.json',{'status':'ONE_AUTHORIZED_CLIENT_EXCHANGE_START','timeUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PID':backend['PID'],'health':health()})
 libc=ctypes.CDLL(None,use_errno=True);exchange=libc.renameat2;exchange.argtypes=[ctypes.c_int,ctypes.c_char_p,ctypes.c_int,ctypes.c_char_p,ctypes.c_uint];exchange.restype=ctypes.c_int
 if exchange(-100,os.fsencode(R/'dist'),-100,os.fsencode(NEXT),2):raise OSError(ctypes.get_errno(),'renameat2 exchange failed')
 require(inv(R/'dist')==seal['build'],'Promoted public bytes differ');require(tree(NEXT)==read(R/'docs/qa/mixed-gate-rollback-353/source-inventories.json')['public345'],'Old345 tree not retainedexactly')
 after={p:tls(b['normalTLSBase'],p) for p in ready['normalTLSPaths']};write('tls-after.json',after);require(all(after[p]==seal['build'][p] for p in after),'AfterTLS response pin mismatch');paired_guard(public=False);binding()
 write('promotion.json',{'status':'PROMOTED_PUBLIC367_STONE37_DEFAULT8_BACKEND230_UNCHANGED','candidateArchiveSHA256':ready['candidateArchiveSHA256'],'pairedRollback353SHA256':ROLLBACK_SHA,'normalTLSPins':after,'retiredWoodPayloads':15,'old345Tree':str(NEXT),'backend':backend,'backendRestarted':False,'exchanges':1,'builds':0,'browsers':0,'pending':'Separate ONE actualnormalTLS changedstone/defaultscene intake; no finalmap/fullgoal inference'})
 print('PROMOTED367 clientexchange only; backend230 unchanged')
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('action',choices=['archive','promote']);args=parser.parse_args();archive_candidate() if args.action=='archive' else promote()
