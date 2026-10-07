#!/usr/bin/env python3
"""Read-only raster custody/packaging validation. This does not grant visual approval."""
import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path
from PIL import Image

SHA = re.compile(r'^[a-fA-F0-9]{64}$')
KINDS = {'unit','building','prop','vfx','terrain','ui','portrait'}
STATUSES = {'CANDIDATE','APPROVED','REJECTED','PLACEHOLDER_ONLY'}


def check(condition, message):
    if not condition:
        raise ValueError(message)


def number(value):
    return isinstance(value,(int,float)) and not isinstance(value,bool) and math.isfinite(value)


def integer(value):
    return isinstance(value,int) and not isinstance(value,bool)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dimensions(meta, label):
    check(isinstance(meta,dict) and all(integer(meta.get(k)) and 1 <= meta[k] <= 16384 for k in ('width','height')) and meta['width']*meta['height'] <= 32*1024*1024, f'{label}: invalid dimensions')


def file_meta(meta, label):
    dimensions(meta,label)
    check(isinstance(meta.get('path'),str) and meta['path'],f'{label}: missing path')
    check(all(isinstance(meta.get(k),str) and SHA.fullmatch(meta[k]) for k in ('sha256','rgbaSha256')),f'{label}: encoded and decoded RGBA SHA256 required')


def check_candidate_fringe(alpha,label,allow_candidate_fringe):
    border_max=max(alpha.crop(rect).getextrema()[1] for rect in [(0,0,alpha.width,1),(0,alpha.height-1,alpha.width,alpha.height),(0,0,1,alpha.height),(alpha.width-1,0,alpha.width,alpha.height)])
    body=alpha.point(lambda value:255 if value>16 else 0).getbbox()
    check(allow_candidate_fringe and border_max<=16 and body is not None and body[0]>0 and body[1]>0 and body[2]<alpha.width and body[3]<alpha.height,f'{label}: clipped/opaque cutout or nontransparent canvas edge')
    return {'status':'CANDIDATE_WARNING','message':'Low-alpha border fringe retained exactly; strict margin fails, visual review and strict release margin still required','borderMax':border_max,'threshold16BBox':list(body)}


def image_file(meta, base, label, alpha_policy, allow_candidate_fringe=False):
    file_meta(meta,label)
    candidate = Path(meta['path'])
    path = candidate.resolve() if candidate.is_absolute() else (base/candidate).resolve()
    check(path.is_file(),f'{label}: missing file {path}')
    before = path.read_bytes()
    check(sha(before) == meta['sha256'].lower(),f'{label}: encoded SHA256 mismatch')
    with Image.open(path) as opened:
        check(opened.mode == 'RGBA' or alpha_policy=='opaque' and opened.mode=='RGB',f'{label}: genuine RGBA required (explicit opaque terrain RGB allowed), got {opened.mode}')
        check(opened.size == (meta['width'],meta['height']),f'{label}: dimension mismatch')
        image = opened.convert('RGBA')
    check(sha(image.tobytes()) == meta['rgbaSha256'].lower(),f'{label}: decoded RGBA SHA256 mismatch')
    alpha = image.getchannel('A')
    extrema = alpha.getextrema()
    bbox = alpha.getbbox()
    check(bbox is not None,f'{label}: empty alpha image')
    warnings=[]
    if alpha_policy == 'transparent':
        check(extrema[0] == 0 and extrema[1] > 0,f'{label}: transparent cutout requires actual alpha-zero pixels')
        strict_margin=bbox[0]>0 and bbox[1]>0 and bbox[2]<image.width and bbox[3]<image.height
        if not strict_margin:
            fringe=check_candidate_fringe(alpha,label,allow_candidate_fringe)
            warnings.append(fringe)
    elif alpha_policy == 'opaque':
        check(extrema == (255,255),f'{label}: declared opaque material has nonopaque alpha')
    else:
        raise ValueError(f'{label}: unknown alpha policy')
    if 'bbox' in meta:
        check(meta['bbox'] == list(bbox),f'{label}: declared alpha bbox mismatch')
    if 'alphaExtrema' in meta:
        check(meta['alphaExtrema'] == list(extrema),f'{label}: declared alpha extrema mismatch')
    # Reading/decoding cannot silently replace an immutable source file.
    check(sha(path.read_bytes()) == sha(before),f'{label}: file changed during validation')
    return image, {'path':str(path),'sha256':sha(before),'rgbaSha256':sha(image.tobytes()),'dimensions':list(image.size),'alphaExtrema':list(extrema),'bbox':list(bbox),'warnings':warnings}


def validate_asset(asset, base, source_base, require_approved):
    check(isinstance(asset,dict), 'asset must be an object')
    check(isinstance(asset.get('id'),str) and re.fullmatch(r'[A-Za-z0-9_.-]{1,120}',asset['id']), 'invalid asset ID')
    check(asset.get('kind') in KINDS,'invalid raster kind')
    policy = asset.get('alphaPolicy')
    check(policy in ('transparent','opaque') and (policy != 'opaque' or asset['kind'] == 'terrain'),'only terrain material may be opaque')
    source = asset.get('source'); runtime = asset.get('runtime')
    file_meta(source,'source'); file_meta(runtime,'runtime')
    check(Path(runtime['path']).suffix.lower() in ('.png','.webp'),'runtime must be PNG or WebP')
    runtime_path=Path(runtime['path'])
    check(not runtime_path.is_absolute() and not runtime_path.as_posix().startswith('/') and '..' not in runtime_path.parts,'runtime must remain inside manifest directory')
    check((base/runtime_path).resolve().is_relative_to(base.resolve()),'runtime symlink escapes manifest directory')
    check(asset.get('state') and isinstance(asset['state'],str),'explicit state required')
    direction=asset.get('direction','missing')
    check(direction is None or integer(direction) and 0 <= direction <= 7,'explicit direction required (null for nondirectional art)')
    review=asset.get('review',{})
    check(isinstance(review,dict),'review must be object')
    check(review.get('status') in STATUSES and isinstance(asset.get('candidate'),bool),'explicit review and candidate flag required')
    approved=review['status']=='APPROVED' and not asset['candidate']
    if review['status']=='APPROVED':
        check(approved and isinstance(review.get('reviewer'),str) and review['reviewer'] and isinstance(review.get('receipt'),str) and review['receipt'],'approval requires noncandidate flag, reviewer and review receipt')
    if require_approved:
        check(approved,'asset lacks explicit visual approval')
    cell=asset.get('cell');dimensions(cell,'cell')
    pivot=asset.get('pivot',{})
    check(isinstance(pivot,dict),'pivot must be object')
    check(pivot.get('space')=='source' and all(number(pivot.get(k)) for k in ('x','y')) and 0 <= pivot['x'] <= source['width'] and 0 <= pivot['y'] <= source['height'],'invalid fixed source-coordinate pivot')
    render=asset.get('render',{})
    check(isinstance(render,dict),'render must be object')
    check(all(number(render.get(k)) and render[k] > 0 for k in ('width','height')) and abs(render['width']/render['height']-cell['width']/cell['height']) < 1e-6,'invalid/distorted logical render size')
    shadow=asset.get('contactShadow',{})
    check(isinstance(shadow,dict),'shadow must be object')
    check(shadow.get('mode') in ('baked','separate','none'),'explicit contact shadow required')
    check(asset['kind'] not in ('unit','building','prop') or shadow['mode']!='none','grounded art requires contact shadow')
    check(shadow['mode']!='separate' or isinstance(shadow.get('assetId'),str),'separate shadow asset ID required')
    check('loop' not in asset or isinstance(asset['loop'],bool),'loop must be boolean')
    frames=asset.get('frames')
    check(isinstance(frames,list) and 1 <= len(frames) <= 256,'1–256 frames required')
    derivative=runtime.get('derivation',{})
    check(isinstance(derivative,dict),'derivation must be object')
    method=derivative.get('method')
    check(method in ('copy','resize','atlas') and derivative.get('sourceSha256')==source['sha256'],'runtime source derivation pin mismatch')
    check(method!='copy' or len(frames)==1 and cell['width']==source['width'] and cell['height']==source['height'],'copy requires original canvas dimensions')
    check(method!='resize' or len(frames)==1,'multi-frame derivative must declare atlas')
    check(method=='copy' or derivative.get('filter')=='lanczos','derivative requires declared common lanczos filter')
    check(cell['width']/source['width']==cell['height']/source['height'],'anisotropic per-frame camera fitting forbidden')
    allow_fringe=asset['candidate'] and review['status']=='CANDIDATE' and not require_approved
    original, source_receipt=image_file(source,source_base,'source',policy,allow_fringe)
    derivative_image,runtime_receipt=image_file(runtime,base,'runtime',policy,allow_fringe)
    check(source_receipt['path'] != runtime_receipt['path'] or method=='copy','runtime may not overwrite original source')
    expected=Image.new('RGBA',derivative_image.size,(0,0,0,0))
    frame_receipts=[]; occupied=[]
    for i,frame in enumerate(frames):
        check(isinstance(frame,dict) and all(integer(frame.get(k)) for k in ('x','y','width','height')),f'frame {i}: invalid integer cell bounds')
        x,y,w,h=(frame[k] for k in ('x','y','width','height'))
        check(x>=0 and y>=0 and w==cell['width'] and h==cell['height'] and x+w<=runtime['width'] and y+h<=runtime['height'],f'frame {i}: cell outside sheet or changes canvas')
        check(number(frame.get('durationMs')) and 0<frame['durationMs']<=60000,f'frame {i}: invalid duration')
        check('pivot' not in frame or frame['pivot']==pivot,f'frame {i}: per-frame pivot fitting forbidden')
        check(not any(x<r[2] and x+w>r[0] and y<r[3] and y+h>r[1] for r in occupied),f'frame {i}: overlapping cells')
        occupied.append((x,y,x+w,y+h))
        if len(frames)>1:
            frame_source=frame.get('source');file_meta(frame_source,f'frame {i} source')
            check((frame_source['width'],frame_source['height'])==original.size,f'frame {i}: source canvas drift')
            frame_image,frame_receipt=image_file(frame_source,source_base,f'frame {i} source',policy,allow_fringe)
            frame_receipts.append(frame_receipt)
        else:
            frame_image=original
        resized=frame_image if frame_image.size==(w,h) else frame_image.resize((w,h),Image.Resampling.LANCZOS)
        expected.paste(resized,(x,y))
        cell_alpha=derivative_image.crop((x,y,x+w,y+h)).getchannel('A')
        if policy=='transparent':
            b=cell_alpha.getbbox();check(b is not None,f'frame {i}: empty cutout cell');
            if not (b[0]>0 and b[1]>0 and b[2]<w and b[3]<h):
                check_candidate_fringe(cell_alpha,f'frame {i}',allow_fringe)
    check(expected.tobytes()==derivative_image.tobytes(),'runtime pixels differ from declared source-preserving copy/resize/atlas operation (use exact lossless WebP)')
    if method=='copy':
        check(runtime['rgbaSha256']==source['rgbaSha256'],'copy changed decoded source pixels')
    return {'id':asset['id'],'packaging':'PASS','visualReview':review['status'],'candidate':asset['candidate'],'source':source_receipt,'runtime':runtime_receipt,'frames':frame_receipts,'fixedPivot':pivot,'logicalRender':render,'warnings':source_receipt['warnings']+runtime_receipt['warnings']+[warning for frame in frame_receipts for warning in frame['warnings']]}


def validate_manifest(manifest_path, source_root=None, require_approved=False):
    base=manifest_path.resolve().parent
    source_base=Path(source_root).resolve() if source_root else base
    manifest=json.loads(manifest_path.read_text())
    check(isinstance(manifest,dict),'manifest must be object')
    check(manifest.get('schemaVersion')==1 and manifest.get('status') in ('CANDIDATE','APPROVED'),'unsupported manifest version/status')
    c=manifest.get('camera',{})
    check(isinstance(c,dict),'camera must be object')
    check(c.get('projection')=='dimetric' and c.get('ratio')==[2,1] and c.get('tile')==[54,27] and number(c.get('elevation')) and abs(c['elevation']-26.565)<=.001,'camera lock mismatch')
    assets=manifest.get('assets')
    check(isinstance(assets,list) and len(assets)<=4096,'invalid manifest assets')
    if require_approved:
        check(manifest['status']=='APPROVED' and len(assets)>0,'manifest is not approved release art')
    result={'manifest':str(manifest_path.resolve()),'packaging':'PASS','visualApprovalGranted':False,'manifestStatus':manifest['status'],'assets':[],'errors':[]}
    ids=set(); families={}
    for asset in assets:
        try:
            check(isinstance(asset,dict),'asset must be an object')
            check(asset.get('id') not in ids,'duplicate asset ID');ids.add(asset.get('id'))
            receipt=validate_asset(asset,base,source_base,require_approved)
            family=asset.get('family')
            if family:
                layout=(asset['source']['width'],asset['source']['height'],asset['cell']['width'],asset['cell']['height'],asset['pivot'],asset['render'])
                check(family not in families or families[family]==layout,'family changes fixed canvas, pivot or logical scale across states/directions')
                families[family]=layout
            if asset['contactShadow']['mode']=='separate':
                check(any(x.get('id')==asset['contactShadow']['assetId'] for x in assets),'separate contact shadow asset missing')
            result['assets'].append(receipt)
        except (ValueError,KeyError,TypeError,OSError) as exc:
            result['errors'].append({'id':asset.get('id','unknown') if isinstance(asset,dict) else 'unknown','message':str(exc)})
    if result['errors']:
        result['packaging']='FAIL'
    if not assets:
        result['packaging']='EMPTY_PLACEHOLDER_ONLY'
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest',type=Path)
    parser.add_argument('--source-root',type=Path,help='base directory for relative immutable source paths')
    parser.add_argument('--require-approved',action='store_true',help='require recorded visual approval; does not create approval')
    parser.add_argument('--output',type=Path,help='optional new receipt JSON file; never writes input rasters')
    args=parser.parse_args()
    try:
        result=validate_manifest(args.manifest,args.source_root,args.require_approved)
    except (ValueError,KeyError,TypeError,OSError) as exc:
        result={'packaging':'FAIL','visualApprovalGranted':False,'errors':[{'id':'manifest','message':str(exc)}]}
    text=json.dumps(result,indent=2)
    if args.output:
        check(args.output.resolve()!=args.manifest.resolve(),'receipt cannot overwrite manifest')
        check(not args.output.exists(),'receipt output must be a new file')
        args.output.write_text(text+'\n')
    print(text)
    return 0 if result['packaging']=='PASS' else 1


if __name__=='__main__':
    sys.exit(main())
