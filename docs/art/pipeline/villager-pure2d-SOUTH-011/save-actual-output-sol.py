import pathlib,json,hashlib,sys
from PIL import Image
p=pathlib.Path(__file__).parent;k=sys.argv[1];src=pathlib.Path(sys.argv[2]);dst=p/(k+'-inbetween-01')/'raw.png';dst.parent.mkdir(exist_ok=True)
with dst.open('xb') as f:f.write(src.read_bytes())
im=Image.open(dst);rgba=im.convert('RGBA');a=rgba.getchannel('A');h=a.histogram();d={'sourcePath':str(src),'rawPath':str(dst),'dimensions':list(im.size),'mode':im.mode,'encodedSha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'rgbaSha256':hashlib.sha256(rgba.tobytes()).hexdigest(),'alphaExtrema':a.getextrema(),'alphaZeroPixels':h[0],'alphaPartialPixels':sum(h[1:255]),'alphaOpaquePixels':h[255],'sourceBytesIdentical':src.read_bytes()==dst.read_bytes(),'status':'CANDIDATE_PARENT_REVIEW_PENDING'}
(dst.parent/'diagnostics.json').write_text(json.dumps(d,indent=2));name='call-ledger-F1-F3-sol.json' if k in ['F1','F3'] else 'call-ledger-F5-F7-sol.json';l=json.loads((p/name).read_text());l['callsCompleted']+=1;l['jobs'][k].update(status='ACTUAL_OUTPUT_PRESERVED',sourcePath=str(src),diagnostics=d);(p/name).write_text(json.dumps(l,indent=2));print(json.dumps(d))
