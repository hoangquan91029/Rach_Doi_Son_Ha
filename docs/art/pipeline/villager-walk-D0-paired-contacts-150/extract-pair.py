from pathlib import Path
from PIL import Image
import hashlib,json,shutil,datetime
p=Path(__file__).parent
source=Path('/home/kieu-hoang-quan/.codex/generated_images/01a1214b-3448-70b2-8a7a-f4df3b47097b/exec-b307587d-5273-4d0c-b5f7-5ea87c29e0a4.png')
shutil.copy2(source,p/'paired-raw.png')
im=Image.open(p/'paired-raw.png').convert('RGBA'); w,h=im.size
assert w%2==0
cw=w//2; s=128/max(cw,h); rw=round(cw*s); rh=round(h*s); ox=(128-rw)//2; oy=(128-rh)//2
frames=[]; sheet=Image.new('RGBA',(178,89),(0,0,0,0))
for i,name in enumerate(['A','B']):
 cell=im.crop((i*cw,0,(i+1)*cw,h)); cell.save(p/f'{name}-complete-cell.png')
 frame=Image.new('RGBA',(128,128)); frame.paste(cell.resize((rw,rh),Image.Resampling.LANCZOS),(ox,oy)); frame.save(p/f'{name}-uniform128.png')
 sheet.paste(frame.resize((89,89),Image.Resampling.LANCZOS),(i*89,0))
 frames.append({'name':name,'source':f'{name}-complete-cell.png','size':list(cell.size),'status':'HELD_SAME_LEADING_LEG','region':[i*cw,0,(i+1)*cw,h]})
sheet.save(p/'actual-pair89.png')
receipt={'rawReturnedPath':str(source),'rawCopy':'paired-raw.png','rawSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'size':[w,h],'mode':im.mode,'alphaExtrema':im.getchannel('A').getextrema(),'tool':'image_gen.imagegen','resultKeys':['image_url','output_hint'],'image_url':'data:image/png;base64,<binary payload preserved byte-for-byte as paired-raw.png and original returnedPath>','output_hint':'Generated images are saved to /home/kieu-hoang-quan/.codex/generated_images/01a1214b-3448-70b2-8a7a-f4df3b47097b as /home/kieu-hoang-quan/.codex/generated_images/01a1214b-3448-70b2-8a7a-f4df3b47097b/exec-b307587d-5273-4d0c-b5f7-5ea87c29e0a4.png by default.\nIf you need to use a generated image at another path, copy it and leave the original in place unless the user explicitly asks you to delete it.\nThe generated image is already displayed to the user. There is no need to render it in the final response as a Markdown image or file link.','request':'execution-call-request.json','calls':1,'retries':0}
(p/'tool-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
(p/'extraction-receipt.json').write_text(json.dumps({'size':[w,h],'equalCellSize':[cw,h],'scale':s,'resized':[rw,rh],'commonPadding':[ox,oy],'commonPivot128':[ox+s*cw*654/1254,oy+s*h*1140/1254],'bboxFit':False,'sourceRepair':False,'frames':frames,'original033Used':False,'newPairedFamilyOnly':True},indent=2)+'\n')
(p/'live-status.json').write_text(json.dumps({'status':'TERMINAL_HELD_SAME_LEADING_LEG','callsMade':1,'retries':0,'callOpen':False,'endedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'laterGate':'F2/F6/BIs/runtime/fanout CLOSED'},indent=2)+'\n')
(p/'execution-intake.json').write_text(json.dumps({'status':'HELD','review':'brief actual raw and fixed89 pair only','reason':'Both complete cells retain same forward/sash-side trouser/sandal and same trailing leg; required physical opposite contact is absent. Identity coherent but relational pose control failed.','selected':[],'parentActualIntake':'PENDING','retryAllowed':False},indent=2)+'\n')
