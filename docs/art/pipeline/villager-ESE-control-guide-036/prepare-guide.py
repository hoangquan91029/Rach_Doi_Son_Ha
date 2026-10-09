from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,hashlib,json
root=Path.cwd();out=Path(__file__).resolve().parent
src=root/'docs/art/pipeline/villager-walk-ESE-033/F00-raw.png';ref=root/'docs/art/pipeline/villager-walk-ESE-033/F04-model-guide.png'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(src)=='4a7d287bc844b02d00b38074f1b59e3ce41e109b30891c20b3026a8965c6041c'
# Approximate clothed landmarks from the whole source; identity ownership follows hip roots.
controls=[('RIGHT_NEAR_hip',(550,750),(550,750)),('RIGHT_NEAR_knee',(510,870),(640,950)),('RIGHT_NEAR_ankle',(450,1000),(675,1140)),('RIGHT_NEAR_toe',(485,1080),(725,1190)),('LEFT_FAR_hip',(690,750),(690,750)),('LEFT_FAR_knee',(680,930),(645,880)),('LEFT_FAR_ankle',(740,1080),(580,1020)),('LEFT_FAR_toe',(830,1130),(625,1080))]
anchors=[(x,y) for y in [0,300,600,720] for x in [0,300,600,900,1253]]+[(0,950),(1253,950),(0,1253),(1253,1253),(654,1140)]
# Thin plate spline inverse map over one RGBA canvas; no part extraction or donor assembly.
a=np.array([t for _,s,t in controls]+anchors,float);b=np.array([s for _,s,t in controls]+anchors,float);n=len(a)
def kernel(r2):return r2*np.log(np.maximum(r2,1e-12))
k=kernel(((a[:,None]-a[None,:])**2).sum(2));p=np.c_[np.ones(n),a];m=np.block([[k,p],[p.T,np.zeros((3,3))]])
coef=np.linalg.solve(m,np.vstack([b-a,np.zeros((3,2))]))
im=np.array(Image.open(src).convert('RGBA'),dtype=float)/255;assert im.shape==(1254,1254,4);im[:,:,:3]*=im[:,:,3:4]
result=np.zeros_like(im)
for y0 in range(0,1254,32):
 yy,xx=np.mgrid[y0:min(1254,y0+32),0:1254];points=np.c_[xx.ravel(),yy.ravel()].astype(float)
 displacement=kernel(((points[:,None]-a[None,:])**2).sum(2))@coef[:n]+np.c_[np.ones(len(points)),points]@coef[n:]
 # Preserve full head/torso/arms above730 exactly; smooth lower-garment transition.
 fade=np.clip((points[:,1]-730)/90,0,1);fade=fade*fade*(3-2*fade);mapped=points+displacement*fade[:,None]
 x=mapped[:,0];y=mapped[:,1];x0=np.floor(x).astype(int);y1=np.floor(y).astype(int);dx=x-x0;dy=y-y1;values=np.zeros((len(x),4))
 for ox,oy,w in [(0,0,(1-dx)*(1-dy)),(1,0,dx*(1-dy)),(0,1,(1-dx)*dy),(1,1,dx*dy)]:
  sx=x0+ox;sy=y1+oy;valid=(sx>=0)&(sy>=0)&(sx<1254)&(sy<1254);values[valid]+=im[sy[valid],sx[valid]]*w[valid,None]
 result[y0:y0+len(yy)]=values.reshape(len(yy),1254,4)
result[:,:,:3]=np.divide(result[:,:,:3],result[:,:,3:4],out=np.zeros_like(result[:,:,:3]),where=result[:,:,3:4]>1e-8)
rgba=np.uint8(np.clip(np.rint(result*255),0,255));rgba[:730]=np.array(Image.open(src).convert('RGBA'))[:730]
guide=out/'F04-wholecanvas-warp-MODEL_ONLY.png';Image.fromarray(rgba).save(guide)
sheet=Image.new('RGB',(218,125),(45,55,48));d=ImageDraw.Draw(sheet)
for i,pth in enumerate([src,guide]):
 small=Image.open(pth).convert('RGBA').resize((89,89),Image.Resampling.LANCZOS);sheet.paste(small,(i*109+10,15),small);d.text((i*109+4,108),['033F00','036GUIDE'][i],fill='white')
sheet.save(out/'fixed89-comparison.png')
receipt={'status':'MODEL_ONLY_NOT_FINAL_ART_NOT_SELECTED_FRAME','source':{'path':str(src),'sha256':sha(src)},'targetReference':{'path':str(ref),'sha256':sha(ref),'role':'MODEL_ONLY approximate target'},'method':'One full-canvas inverse TPS premultiplied RGBA resample; exact upper730 anchor, lower transition; no extracted parts','controls':[{'ownership':name,'source':s,'target':t} for name,s,t in controls],'identityAnchors':anchors,'pivot':[654,1140],'canvas':[1254,1254],'counts':{'aiCalls':0,'candidateGuideExports':1,'fixed89Comparisons':1},'outputs':{guide.name:sha(guide),'fixed89-comparison.png':sha(out/'fixed89-comparison.png')},'sourceUnmodified':True,'upper730ByteIdentical':bool(np.array_equal(rgba[:730],np.array(Image.open(src).convert('RGBA'))[:730])),'limits':'Guide deformation artifacts accepted as guide only. No selected art, animation, cadence, foot lock or visual approval.'}
(out/'control-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
