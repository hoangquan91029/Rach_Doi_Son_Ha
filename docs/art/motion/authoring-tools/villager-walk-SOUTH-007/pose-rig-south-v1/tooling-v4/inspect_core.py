"""One actual core rest diagnostic only; never a whole-character key or animation."""
import argparse,hashlib,json,pathlib,shutil,tempfile
from PIL import Image,ImageDraw,ImageFont
import bake_keys as b

def inspect(sidecar_path,output):
 out=pathlib.Path(output);b.require(not out.exists(),'refuse existing partial inspection output')
 contract,plan=b.locked_inputs();s,raw=b.validate_sidecar(sidecar_path,b.PARTS[0]);b.validate_approved_core(s)
 bounds=b.validate_pose_geometry(b.PARTS[0],s,plan);b.require(out.parent.exists(),'output parent must exist')
 original_sha=b.digest(s['raw']['path']);sidecar_sha=b.digest(sidecar_path)
 stage=pathlib.Path(tempfile.mkdtemp(prefix='.partial-core-stage-',dir=out.parent))
 try:
  neutral={'points3D':{},'lateralWeightShift':0,'pelvisZ':480};image=Image.new('RGBA',(1254,1254));b.draw_part(image,raw,s,neutral)
  qa=Image.new('RGBA',(1254,1254),(105,105,105,255));qa.alpha_composite(image);draw=ImageDraw.Draw(qa)
  try:font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
  except OSError:font=ImageFont.load_default()
  draw.text((20,15),'PARTIAL_REST_INSPECTION_ONLY / core1 of9 / no animation or finished-key approval',font=font,fill='white')
  draw.text((20,43),'Fixed1254 canvas +root6541140 / immutable uniform calibration / whole-canvas38px',font=font,fill='white')
  for name,t in b.core_targets().items():
   x,y=t['restScreenXY'];hip='hip' in name;color=(255,160,40,255) if hip else (20,220,255,255);radius=t['uncertaintySourcePx']*s['calibration']['scale']
   draw.ellipse((x-radius,y-radius,x+radius,y+radius),outline=color,width=2)
   draw.ellipse((x-3,y-3,x+3,y+3),fill=color)
   left='_left_' in name;tx=x+50 if left else x-340;ty=y-50 if hip else y-45
   label=('LEFT' if left else 'RIGHT')+(' hiddenhip hypothesis +/-45RAWpx' if hip else ' clothcap convention +/-14RAWpx')
   draw.line((x,y,tx+(0 if left else 305),ty+20),fill=color,width=2);draw.text((tx,ty),label,font=font,fill=color)
  draw.line((639,1140,669,1140),fill=(20,255,100,255),width=2);draw.line((654,1125,654,1155),fill=(20,255,100,255),width=2)
  draw.text((700,1123),'Fixed full-character root; all8 limb textures absent',font=font,fill='white')
  outputs=[]
  for name,im in [('partial-rest-core.png',image),('partial-rest-core-QA.png',qa),('partial-rest-core-whole38.png',image.resize((38,38),Image.Resampling.LANCZOS))]:
   p=stage/name;im.save(p);outputs.append({'path':name,'sha256':b.digest(p),'rgbaSha256':hashlib.sha256(im.tobytes()).hexdigest(),'width':im.width,'height':im.height})
  b.require(b.digest(s['raw']['path'])==original_sha and b.digest(sidecar_path)==sidecar_sha,'source/sidecar changed during partial inspection')
  b.locked_inputs()
  receipt={'status':'PARTIAL_REST_INSPECTION_ONLY','candidate':False,'fullCharacter':False,'animationKey':False,'motionQualified':False,'finalArtApproved':False,'imageCalls':0,'sourceByteSha256':original_sha,'sourceRgbaSha256':s['raw']['rgbaSha256'],'sidecarSha256':sidecar_sha,'contractSha256':b.CONTRACT_SHA,'posePlanSha256':b.PLAN_SHA,'staticCalibration':s['calibration'],'attachmentTargets':b.core_targets(),'allFourCorePoseGeometryChecked':True,'projectedMeshBounds':bounds,'sourceAlphaOutsideMesh':0,'missingOriginalParts':8,'outputs':outputs,'remainingFootGate':'Preserved F0/F4 trailing flat12px-lift geometry is a held hypothesis. Actual toe-grounded/heel-rise rigid foot plane must be authored from real lower-sandal landmarks and reviewed BEFORE four finished-key acceptance; no contact qualification.'}
  (stage/'inspection.json').write_text(json.dumps(receipt,indent=2)+'\n');b.publish_no_replace(stage,out);return receipt
 finally:
  if stage.exists():shutil.rmtree(stage)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('sidecar');p.add_argument('output');a=p.parse_args()
 try:r=inspect(a.sidecar,a.output);print(json.dumps({'status':r['status'],'candidate':False,'fullCharacter':False,'animationKey':False,'outputs':len(r['outputs'])}))
 except (b.Refusal,KeyError,OSError,ValueError,TypeError) as e:print(json.dumps({'status':'REFUSED_NO_PUBLISHED_OUTPUT','reason':str(e),'candidate':False}));raise SystemExit(2)
