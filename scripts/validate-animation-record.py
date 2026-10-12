#!/usr/bin/env python3
"""Validate candidate evidence custody. Never grants visual or production approval."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image
from jsonschema import Draft202012Validator

REPO = Path(__file__).resolve().parents[1]
SCHEMA = REPO / 'docs/art/pipeline/ASSET_MANIFEST_SCHEMA.json'

def require(condition, message):
    if not condition:
        raise ValueError(message)

def validate(record, root=REPO):
    Draft202012Validator(json.loads(SCHEMA.read_text())).validate(record)
    root = Path(root).resolve()
    def pinned(pin, base=root):
        path = Path(pin['path'])
        path = (base / path).resolve() if not path.is_absolute() else path.resolve()
        require(path.is_file(), f'Missing pinned file: {path}')
        require(hashlib.sha256(path.read_bytes()).hexdigest() == pin['sha256'], f'SHA mismatch: {path}')
        return path
    canonical = pinned(record['canonicalReference'])
    job_path, descriptor_path = pinned(record['job']), pinned(record['descriptor'])
    job, descriptor = json.loads(job_path.read_text()), json.loads(descriptor_path.read_text())
    geo = record['geometry']
    require(geo['cellWidth'] == geo['cellHeight'] == 128, 'Current compiler requires whole128 cells')
    require(geo['sourceWidth'] == geo['sourceHeight'], 'Source must be square')
    require(geo['renderWidth'] == geo['renderHeight'], 'Whole square render must remain undistorted')
    require(geo['pivotX'] < geo['sourceWidth'] and geo['pivotY'] < geo['sourceHeight'], 'Pivot outside source')
    def png(pin):
        path = pinned(pin)
        with Image.open(path) as image:
            require(image.format == 'PNG' and image.mode == 'RGBA', f'Expected RGBA PNG: {path}')
            require(image.size == (geo['sourceWidth'], geo['sourceHeight']), 'Source canvas mismatch')
            alpha = image.getchannel('A').getextrema()
            require(alpha[0] == 0 and alpha[1] > 0, 'Source needs transparent pixels and visible content')
            rgba = hashlib.sha256(image.tobytes()).hexdigest()
        return path, rgba
    png(record['canonicalReference'])
    sources = [png(source['pin']) for source in record['sources']]
    sequence = record['frameSequence']
    indices = [frame['sourceIndex'] for frame in sequence]
    require(indices == list(range(len(record['sources']))), 'Source indices must cover sources once in order')
    phases = [frame['phase'] for frame in sequence]
    require(phases[0] == 0 and phases == sorted(set(phases)), 'Phases must start zero and strictly increase')
    require(len(sequence) == len(job['frames']) == len(descriptor['frames']), 'Frame count mismatch')
    require(job.get('schemaVersion') == 2 and job['frameCount'] == len(sequence), 'Expected current explicit-loop job schema2')
    require(job['id'] == descriptor['id'] == record['assetId'], 'Asset identity mismatch')
    require(job['family'] == descriptor['family'], 'Family mismatch')
    require(job['action'] == descriptor['state'] == record['action'], 'Action mismatch')
    require(job['direction'] == descriptor['direction'] == record['direction'], 'Direction mismatch')
    require(job['loop'] == descriptor['loop'] == record['loop'], 'Loop mismatch')
    master = job.get('identityMaster', job['master'])
    require(descriptor.get('identityMasterSHA', master['sha256']) == master['sha256'], 'Descriptor identity master mismatch')
    require(pinned(master, job_path.parent) == canonical and master['sha256'] == record['canonicalReference']['sha256'], 'Canonical identity binding mismatch')
    for field, pair in [('fixedCanvas', ('sourceWidth','sourceHeight')), ('cell', ('cellWidth','cellHeight')), ('render', ('renderWidth','renderHeight'))]:
        require(job[field] == {'width':geo[pair[0]], 'height':geo[pair[1]]}, f'Job {field} mismatch')
        if field != 'fixedCanvas':
            require(descriptor[field] == job[field], f'Descriptor {field} mismatch')
    require(job['pivot'] == descriptor['pivot'] == {'x':geo['pivotX'],'y':geo['pivotY'],'space':'source'}, 'Pivot binding mismatch')
    columns = job.get('layout', {}).get('columns', min(15,len(sequence)))
    for index, (frame,jf,df) in enumerate(zip(sequence,job['frames'],descriptor['frames'])):
        source = record['sources'][index]
        for pin, base in ((jf['input'], job_path.parent), (df['source'], descriptor_path.parent)):
            require(pinned(pin, base) == sources[index][0] and pin['sha256'] == source['pin']['sha256'], 'Frame source binding mismatch')
            require(pin['rgbaSha256'] == sources[index][1], 'Source RGBA mismatch')
        require(source['status'] == jf['status'], 'Source status mismatch')
        require(frame['phase'] == jf['phase'], 'Phase mismatch')
        require(frame['durationMs'] == jf['durationMs'] == df['durationMs'], 'Duration mismatch')
        require((df['x'],df['y'],df['width'],df['height']) == ((index%columns)*132+2,(index//columns)*132+2,128,128), 'Atlas layout mismatch')
    runtime = descriptor['runtime']
    atlas = pinned(runtime, descriptor_path.parent)
    with Image.open(atlas) as image:
        require(image.mode == 'RGBA' and image.format == 'PNG', 'Atlas must be RGBA PNG')
        require(image.size == (runtime['width'],runtime['height']) == (columns*132, ((len(sequence)+columns-1)//columns)*132) and max(image.size)<=2048, 'Atlas dimensions mismatch')
        require(hashlib.sha256(image.tobytes()).hexdigest() == runtime['rgbaSha256'], 'Atlas RGBA mismatch')
    distance = job.get('locomotion', {}).get('distancePerCycle')
    require(record['distancePerCycle'] == distance == descriptor.get('locomotion', {}).get('distancePerCycle'), 'Distance metadata mismatch')
    for qualification in record['qualification'].values():
        for pin in qualification['evidence']:
            pinned(pin)
    if record['scope'] == 'production':
        require(all(source['status']=='selected' for source in record['sources']), 'Production rejects held/rejected/candidate sources')
        require(all(record['qualification'][stage]['status']=='PASS' for stage in ('technical','motion','runtime')), 'Production requires technical/motion/runtime evidence')
        if record['action']=='walk':
            require(record['distancePerCycle'] is not None, 'Production walk requires measured distance and bound evidence')
        raise ValueError('Production refused: trusted qualification/stride evidence adapter is not implemented; PASS labels are not approval')
    return {'status':'VALID_CANDIDATE_CUSTODY','visualApproval':False,'productionAuthorized':False,'frames':len(sequence)}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('record',type=Path)
    parser.add_argument('--root',type=Path,default=REPO)
    args=parser.parse_args()
    try:
        print(json.dumps(validate(json.loads(args.record.read_text()), args.root)))
    except Exception as error:
        parser.exit(1, f'INVALID: {error}\n')

if __name__ == '__main__':
    main()
