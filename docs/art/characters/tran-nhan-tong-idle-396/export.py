from pathlib import Path
from PIL import Image
import json,shutil,hashlib
p=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha/docs/art/characters/tran-nhan-tong-idle-396')
tool=Path('/home/kieu-hoang-quan/.codex/generated_images/01a1159b-f20c-75d2-8030-3f4d27119543/exec-2ace1f7c-b802-4bd9-bd9f-13470a53aa68.png')
shutil.copy2(tool,p/'raw.png');im=Image.open(p/'raw.png');assert im.mode=='RGBA' and im.width==im.height
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
def rec(f):
 i=Image.open(p/f);return dict(path=f,sha256=sha(p/f),rgbaSha256=hashlib.sha256(i.tobytes()).hexdigest(),width=i.width,height=i.height)
for f,n in [('working256.png',256),('runtime.png',128),('preview42.png',42)]:im.resize((n,n),Image.Resampling.LANCZOS).save(p/f)
s=rec('working256.png');s['path']='docs/art/characters/tran-nhan-tong-idle-396/working256.png';rr=rec('runtime.png');rr['path']='characters-396/tran-nhan-tong-idle.png';rr['derivation']=dict(method='uniform-full-canvas-resize',filter='lanczos',sourceSha256=s['sha256'])
a=dict(id='tran-nhan-tong-idle-396-D0',family='unit.tran_nhan_tong',kind='unit',state='idle',direction=0,candidate=True,review={'status':'CANDIDATE'},source=s,runtime=rr,cell={'width':128,'height':128},pivot={'x':654/1254*256,'y':1140/1254*256,'space':'source'},render={'width':42,'height':42},alphaPolicy='transparent',contactShadow={'mode':'baked'},frames=[{'x':0,'y':0,'width':128,'height':128,'durationMs':1000}],loop=True,notes='Whole builtin2D King identity396; one D0 idle only. All original leadership references preserved. Provisional current-general scale; no animation/8direction/finalfamily scale acceptance.')
(p/'candidate.json').write_text(json.dumps(a,indent=2)+'\n')
alpha=im.getchannel('A');edges=[alpha.crop((0,0,im.width,1)),alpha.crop((0,im.height-1,im.width,im.height)),alpha.crop((0,0,1,im.height)),alpha.crop((im.width-1,0,im.width,im.height))]
receipt=dict(status='RETURNED_CLOSED_CANDIDATE_AWAIT_ACTUAL_SCENE',builtinCalls=1,retries=0,toolOriginal=str(tool),raw=rec('raw.png'),source=s,runtime=rr,preview=rec('preview42.png'),alphaExtrema=alpha.getextrema(),edgeAlphaMax=max(e.getextrema()[1] for e in edges),derivation='Whole uniform resizes only; no crop/fit/shift/alpha repair/mirror/warp/source splicing',resolutionReason='Production source256 and runtime128 preserve useful detail without large browser sprites; larger built-in raw retained as original custody. Provisional logical42 matches existing same-scene general; final 64–96px family-scale target remains open.')
(p/'receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n');j=json.loads((p/'work-order.json').read_text());j.update(status='RETURNED_CLOSED',callsCompleted=1,toolOriginal=str(tool));(p/'work-order.json').write_text(json.dumps(j,indent=2)+'\n')
for f in j['refs']:assert sha(Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha')/f['path'])==f['sha256']
print(json.dumps({'source':s['sha256'],'runtime':rr['sha256'],'alpha':receipt['alphaExtrema'],'edgeAlphaMax':receipt['edgeAlphaMax']}))
