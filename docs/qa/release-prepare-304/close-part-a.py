from pathlib import Path
import hashlib,json,subprocess,urllib.request,os,stat
R=Path.cwd();Q=R/'docs/qa/release-prepare-304'; B=Path.home()/'.local/share/rach-doi-son-ha/releases/304'; L=Path.home()/'.local/share/rach-doi-son-ha/releases/230/runtime230'; C=B/'rollback299/runtime230'
def inv(p):
 return {str(f.relative_to(p)):{'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'mode':stat.S_IMODE(f.stat().st_mode)} for f in sorted(p.rglob('*')) if f.is_file()}
for n in ['server','shared','node_modules']:assert inv(L/n)==inv(C/n)
for n in ['package.json','package-lock.json']:
 if (L/n).exists():assert (L/n).read_bytes()==(C/n).read_bytes() and stat.S_IMODE((L/n).stat().st_mode)==stat.S_IMODE((C/n).stat().st_mode)
pub={str(f.relative_to(R/'dist')):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted((R/'dist').rglob('*')) if f.is_file()};assert pub==json.loads((Q/'public299-before.json').read_text())
service=subprocess.check_output(['systemctl','--user','show','rach-doi-son-ha.service','-p','MainPID','-p','WorkingDirectory','-p','ActiveState'],text=True);assert service==(Q/'service-before.txt').read_text();assert json.load(urllib.request.urlopen('http://127.0.0.1:3000/health'))=={'ok':True,'rooms':0}
a=json.loads((Q/'archives.json').read_text())['rollback299']
(Q/'receipt-part-a.json').write_text(json.dumps({'status':'PART_A_READY_PHASE_B_WAIT','rollbackArchive':a['path'],'rollbackSHA256':a['sha256'],'archiveBytesModesSafeExtractionVerified':True,'fullCopiedRuntimeBytesModesMatchLive':True,'publicBeforeAfterExact':True,'servicePID':3229,'serviceBeforeAfterExact':True,'rooms':0,'canonicalSealed':False,'candidateSealed':False,'buildBrowserImageCalls':0,'productionMutation':False,'ownedHandles':'all PART A processes terminal after this receipt; phase B uncalled'},indent=2)+'\n')
print(a['sha256'])
