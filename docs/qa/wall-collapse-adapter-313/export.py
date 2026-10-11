#!/usr/bin/env python3
"""Four selected whole illustrated wall keys; technical packaging only."""
import argparse, hashlib, importlib.util, json, re, shutil, sys
from pathlib import Path
from PIL import Image, ImageDraw
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('contract', ROOT/'scripts/validate-art-assets.py')
contract = importlib.util.module_from_spec(spec); spec.loader.exec_module(contract)
CAMERA = {'projection':'dimetric','ratio':[2,1],'tile':[54,27],'elevation':26.565}
def sha(data): return hashlib.sha256(data).hexdigest()
def require(ok, message):
    if not ok: raise ValueError(message)
def pinned(record, base):
    path = Path(record['path']); path = path.resolve() if path.is_absolute() else (base/path).resolve()
    require(path.is_file(), 'Missing custody file: '+str(path))
    require(record.get('sha256') == sha(path.read_bytes()), 'Custody hash mismatch: '+str(path))
    return path

def preflight(job_path):
    job_path = Path(job_path).resolve(); job = json.loads(job_path.read_text()); base = job_path.parent
    require(job.get('family') == 'building.wall' and job.get('state') == 'death' and job.get('direction', 'missing') is None and job.get('fortification') == {'mask':0}, 'Exact standalone Wall death contract required')
    require(job.get('loop') is False, 'Death must be nonloop terminal hold')
    require(job.get('sourceCanvas') == [1254,1254] and job.get('runtimeCell') == [128,128] and job.get('pivot') == [627,900] and job.get('renderSize') == [42.3225,42.3225], 'Fixed whole family layout required')
    require(job.get('sourceMethod') == 'FINISHED_WHOLE_2D_FRAMES' and job.get('wholeCanvasTransform') == 'UNIFORM_LANCZOS_NO_CROP_SHIFT_FIT', 'Finished whole illustrations required')
    require(isinstance(job.get('id'),str) and re.fullmatch(r'[A-Za-z0-9_.-]{1,120}',job['id']), 'Invalid asset ID')
    frames = job.get('frames'); require(isinstance(frames,list) and len(frames)==4, 'Require actual F0 onset/F1 fall/F2 impact/F3 settle; missing keys cannot be filled')
    images=[]; records=[]; seen=set()
    for i,f in enumerate(frames):
        require(f.get('index')==i and f.get('phase')==f'F{i}' and f.get('selectionStatus')=='SELECTED_FRAME_CANDIDATE', 'Exact ordered selected keys required')
        require(not any(k in f for k in ['crop','trim','scale','transform','offset','pivot','runtimeCell','renderSize']), 'Per-frame adjustment forbidden')
        duration=f.get('durationMs'); require(isinstance(duration,int) and not isinstance(duration,bool) and 0<duration<=60000, 'Positive finite integer duration required')
        source=dict(f['source']); require((source.get('width'),source.get('height'))==(1254,1254), 'Source family dimensions drift')
        path=pinned(source,base); source['path']=str(path)
        require(path.suffix.lower()=='.png', 'Returned whole PNG required')
        im,_=contract.image_file(source,base,f'F{i}','transparent',True)
        require(source['rgbaSha256'] not in seen,'Duplicated phase cannot supply missing illustration'); seen.add(source['rgbaSha256'])
        raw_path=pinned(f['originalRaw'],base); tool_path=pinned(f['toolReceipt'],base)
        require(raw_path==path and f['originalRaw']['sha256']==source['sha256'], 'Selected source must preserve actual original raw bytes')
        selected=pinned(f['selectionReceipt'],base); receipt=json.loads(selected.read_text())
        require(receipt.get('status')=='SELECTED_FRAME_CANDIDATE' and receipt.get('frameIndex')==i and receipt.get('sourceSha256')==source['sha256'] and receipt.get('rgbaSha256')==source['rgbaSha256'], 'Selection receipt must bind exact phase/source')
        records.append(dict(source=source,originalRaw={'path':str(raw_path),'sha256':source['sha256']},toolReceipt={'path':str(tool_path),'sha256':f['toolReceipt']['sha256']},selectionReceipt={'path':str(selected),'sha256':f['selectionReceipt']['sha256']})); images.append(im)
    return job,images,records

def export(job_path, output):
    output=Path(output).resolve(); require(not output.exists(),'Refusing existing output')
    job,images,records=preflight(job_path)
    require(not any(output==Path(r['source']['path']).parent or output in Path(r['source']['path']).parents for r in records),'Output overlaps source custody')
    output.mkdir(parents=True); atlas=Image.new('RGBA',(512,128)); frames=[]; runtime_frames=[]; sources=output/'sources'; sources.mkdir()
    for i,(im,r) in enumerate(zip(images,records)):
        destination=sources/f'F{i}.png'; shutil.copyfile(r['source']['path'],destination)
        source=dict(r['source'],path=str(destination)); runtime=im.resize((128,128),Image.Resampling.LANCZOS); runtime_frames.append(runtime); atlas.paste(runtime,(i*128,0))
        frames.append(dict(x=i*128,y=0,width=128,height=128,durationMs=job['frames'][i]['durationMs'],source=source,events=[]))
    atlas.save(output/'atlas.png')
    asset=dict(id=job['id'],family='building.wall',kind='building',state='death',direction=None,fortification={'mask':0},source=frames[0]['source'],runtime=dict(path='atlas.png',sha256=sha((output/'atlas.png').read_bytes()),rgbaSha256=sha(atlas.tobytes()),width=512,height=128,derivation=dict(method='atlas',filter='lanczos',sourceSha256=frames[0]['source']['sha256'])),cell=dict(width=128,height=128),pivot=dict(x=627,y=900,space='source'),render=dict(width=42.3225,height=42.3225),alphaPolicy='transparent',contactShadow={'mode':'baked'},candidate=True,review={'status':'CANDIDATE'},frames=frames,loop=False)
    manifest=dict(schemaVersion=1,status='CANDIDATE',camera=CAMERA,assets=[asset],notes='Technical custody only; no motion/scene/install approval')
    (output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    validation=contract.validate_manifest(output/'manifest.json'); require(validation['packaging']=='PASS','Packaging validator failed: '+json.dumps(validation))
    durations=[f['durationMs'] for f in frames]
    previews=[im.resize((42,42),Image.Resampling.LANCZOS) for im in images]
    previews[0].save(output/'preview42-once.png',save_all=True,append_images=previews[1:],duration=durations,loop=1,disposal=0,blend=0)
    runtime_frames[0].save(output/'preview128-once.png',save_all=True,append_images=runtime_frames[1:],duration=durations,loop=1,disposal=0,blend=0)
    sheet=Image.new('RGBA',(4*160,78),(45,55,48,255)); draw=ImageDraw.Draw(sheet)
    for i,im in enumerate(previews):
        sheet.alpha_composite(im,(i*160+59,0)); draw.text((i*160,48),f'F{i}: {durations[i]}ms',fill='white')
    sheet.save(output/'contact-sheet42.png')
    ledger=dict(status='CANDIDATE_TECHNICAL_CUSTODY_ONLY',jobSha256=sha(Path(job_path).read_bytes()),frames=records,timingMs=durations,totalDurationMs=sum(durations),terminal=dict(frame=3,loop=False,hold='Persists after total duration until ordinary simulation corpse removal'),packagingValidation=validation,limits='One brief actual-size preview and real relevant scene remain required; no missing phase substitution')
    (output/'frame-source-ledger.json').write_text(json.dumps(ledger,indent=2)+'\n'); return ledger
if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('job',type=Path); parser.add_argument('output',type=Path); args=parser.parse_args(); print(json.dumps(export(args.job,args.output),indent=2))
