#!/usr/bin/env python3
"""Static complete-frame diagnostic; never fits/crops/repairs source art."""
import argparse, hashlib, json, shutil
from pathlib import Path
from PIL import Image
STATUS = 'STATIC_CONTACT_DIAGNOSTIC_NOT_MOTION_APPROVAL'
def sha(data): return hashlib.sha256(data).hexdigest()
def describe(path, im):
    alpha = im.getchannel('A')
    hist = alpha.histogram()
    return dict(path=str(path), encodedSha256=sha(path.read_bytes()), rgbaSha256=sha(im.tobytes()), dimensions=list(im.size), alphaBounds=alpha.getbbox(), alphaExtrema=list(alpha.getextrema()), transparentPixels=hist[0], partialAlphaPixels=sum(hist[1:255]), opaquePixels=hist[255])
def main():
    parser=argparse.ArgumentParser(); parser.add_argument('job'); parser.add_argument('output'); args=parser.parse_args()
    job_path=Path(args.job).resolve(); job=json.loads(job_path.read_text()); out=Path(args.output).resolve()
    if out.exists(): raise SystemExit('Refusing existing output')
    if set(job['sources']) != {'canonicalSouth','oldSelectedF0','newF4ActualRaw'}: raise SystemExit('Exactly three declared source roles required')
    sources=[]
    for role in ['canonicalSouth','oldSelectedF0','newF4ActualRaw']:
        item=job['sources'][role]; path=Path(item['path'])
        if not path.is_absolute(): raise SystemExit('Source paths must be absolute')
        with Image.open(path) as raw:
            if raw.format != 'PNG' or 'A' not in raw.getbands(): raise SystemExit(f'{role}: genuine PNG alpha channel required')
            im=raw.convert('RGBA')
        receipt=describe(path, im)
        for key in ['encodedSha256','rgbaSha256']:
            if receipt[key] != item[key]: raise SystemExit(f'{role}: {key} mismatch')
        sources.append((role,im,receipt))
    out.mkdir(parents=False)
    metadata=dict(status=STATUS, jobSha256=sha(job_path.read_bytes()), sourceCanvas=[1254,1254], referenceHeight=1130, pivot=[654,1140], runtimeCanvas=[128,128], scale=128/1254, runtimeReferenceHeight=1130*128/1254, runtimePivot=[654*128/1254,1140*128/1254], resampling='Pillow LANCZOS whole canvas, no crop/shift/alpha threshold', subjects=[])
    if any(im.size != (1254,1254) for _,im,_ in sources):
        metadata['status']='HELD_CANVAS'; metadata['sources']=[dict(role=r,**d) for r,_,d in sources]
        (out/'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n'); raise SystemExit('HELD_CANVAS: no derivatives or repairs produced')
    for role,im,receipt in sources:
        dest=out/(role+'.png'); derivative=im.resize((128,128),Image.Resampling.LANCZOS); derivative.save(dest)
        metadata['subjects'].append(dict(role=role,path=dest.name,source=receipt,runtime=describe(dest,derivative)))
    (out/'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
    shutil.copyfile(Path(__file__).with_name('preview.html'),out/'preview.html')
    print(f'{STATUS}: {out}')
if __name__=='__main__': main()
