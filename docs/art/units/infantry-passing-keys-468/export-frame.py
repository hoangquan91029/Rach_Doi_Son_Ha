from pathlib import Path
import sys,json,hashlib,shutil
from PIL import Image
O=Path(__file__).resolve().parent;f=int(sys.argv[1]);source=Path(sys.argv[2]);raw=O/f"F{f}-raw.png"
assert f in [2,6] and source.exists() and not raw.exists()
shutil.copy2(source,raw);im=Image.open(raw).convert("RGBA");assert im.size==(1254,1254)
for size in [256,128]:im.resize((size,size),Image.Resampling.LANCZOS).save(O/f"F{f}-{size}.png")
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r={"state":"RETURNED_CLOSED","frame":f,"logicalCalls":1,"retries":0,"builtinOutput":str(source),"rawSHA":sha(raw),"dimensions":list(im.size),"uniformExportOnly":True,"pivot":[653,1057],"runtimeInstall":False,"motionApproval":False}
(O/f"F{f}-call.json").write_text(json.dumps(r,indent=2)+"\n");print(json.dumps(r))
