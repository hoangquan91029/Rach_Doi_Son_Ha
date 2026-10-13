#!/usr/bin/env python3
"""Whole-frame packaging only: no generation, visual approval, or runtime install."""
import argparse
import hashlib
import json
import math
import os
import re
import shutil
import tempfile
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw

BUDGET = 128 * 1024 * 1024

def require(ok, message):
    if not ok:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def number(value):
    return type(value) in (int, float) and math.isfinite(value)

def pinned_image(pin, base, canvas):
    require(isinstance(pin, dict), 'missing input pin')
    path = (base / pin['path']).resolve()
    data = path.read_bytes()
    require(digest(data) == pin['sha256'], 'encoded SHA256 mismatch')
    with Image.open(path) as opened:
        require(opened.mode == 'RGBA', 'genuine RGBA required')
        image = opened.copy()
    require(image.size == canvas, 'fixed canvas mismatch')
    require(digest(image.tobytes()) == pin['rgbaSha256'], 'decoded RGBA SHA256 mismatch')
    return image, dict(path=str(path), width=image.width, height=image.height,
                       sha256=digest(data), rgbaSha256=digest(image.tobytes()))

def compile_job(job_path, mode):
    job_path = Path(job_path).resolve()
    job = json.loads(job_path.read_text())
    base = job_path.parent
    require(job.get('schemaVersion') in (1, 2, 3), 'unsupported job schema')
    building = job.get('schemaVersion') == 3
    canonical = None
    if building:
        require(job.get('kind') == 'building' and job.get('direction') is None, 'schema3 requires building/null direction')
        definitions = json.loads(subprocess.check_output(['node', '--input-type=module', '-e', f"import {{BUILDINGS}} from {json.dumps((Path(__file__).resolve().parents[1] / 'shared/data.js').as_uri())}; process.stdout.write(JSON.stringify(BUILDINGS));"], text=True))
        kind = job.get('buildingType')
        require(kind in definitions and job.get('family') in (kind, 'building.' + kind), 'known building family/type required')
        require(job.get('action') in ('construction', 'hit', 'death', 'attack') and (job.get('action') != 'attack' or definitions[kind].get('damage', 0) > 0), 'invalid building state/attack')
        require('locomotion' not in job and not job.get('previewBank'), 'building locomotion/directional bank forbidden')
        pin = job.get('canonicalDescriptor', {})
        raw = (base / pin.get('path', '')).resolve().read_bytes()
        require(digest(raw) == pin.get('sha256'), 'canonical building descriptor SHA mismatch')
        canonical = json.loads(raw)
        require(canonical.get('kind') == 'building' and canonical.get('direction') is None and canonical.get('family') in (kind, 'building.' + kind), 'canonical building type/direction mismatch')
        require(all(job.get(k) == canonical.get(k) for k in ('cell', 'pivot', 'render', 'contactShadow')), 'building canonical layout mismatch')
        require(job.get('fixedCanvas') == {k: canonical['source'][k] for k in ('width', 'height')}, 'building canonical source canvas mismatch')
        require(job.get('originalMaster', {}).get('sha256') == canonical['source']['sha256'] == job.get('masterSHA') and job.get('master') == job.get('originalMaster'), 'building original master binding mismatch')
        require(job.get('loop') is True if job.get('action') == 'construction' else type(job.get('loop')) is bool, 'building explicit construction loop required')
    require(not any(k in job for k in ('transform', 'mirror', 'warp', 'fit')), 'whole-frame transforms forbidden')
    require(mode in ('diagnostic', 'selected', 'production'), 'invalid mode')
    require(re.fullmatch(r'[A-Za-z0-9_.-]{1,120}', job['id']), 'invalid ID')
    require(isinstance(job['family'], str) and job['family'], 'family required')
    require(isinstance(job['action'], str) and job['action'], 'action required')
    require(building or type(job['direction']) is int and 0 <= job['direction'] <= 7, 'invalid direction')
    canvas = tuple(job['fixedCanvas'][k] for k in ('width', 'height'))
    require(all(type(n) is int and 1 <= n <= 16384 for n in canvas), 'invalid canvas')
    require(canvas[0] == canvas[1] and canvas[0] * canvas[1] <= 32 * 1024 * 1024, 'square fixed canvas required within 32 megapixels')
    require(building or job['cell'] == {'width': 128, 'height': 128}, 'runtime cell must be 128 square')
    cell = job['cell']['width']
    require(type(cell) is int and cell > 0 and job['cell']['height'] == cell, 'square runtime cell required')
    pivot = job['pivot']; render = job['render']
    require(pivot.get('space') == 'source' and all(number(pivot.get(k)) and 0 <= pivot[k] <= canvas[i] for i, k in enumerate(('x', 'y'))), 'invalid fixed pivot')
    require(all(number(render.get(k)) and render[k] > 0 for k in ('width', 'height')) and render['width'] == render['height'], 'invalid fixed logical scale')
    shadow = job['contactShadow']
    require(shadow.get('mode') in ('baked', 'separate') and (shadow['mode'] != 'separate' or isinstance(shadow.get('assetId'), str) and bool(shadow['assetId'])), 'grounded baked or separate shadow required')
    calls = job['callBudget']
    require(all(type(calls.get(k)) is int and calls[k] >= 0 for k in ('limit', 'used')) and calls['used'] <= calls['limit'], 'invalid call budget')
    frames = job['frames']
    require(isinstance(frames, list) and 1 <= len(frames) <= 256, 'missing frames')
    require(job.get('frameCount') == len(frames), 'missing frame or frameCount mismatch')
    require(job['schemaVersion'] == 1 or 'loop' in job, 'schema 2 requires explicit loop')
    loop = job.get('loop', job['action'] in ('idle', 'walk', 'gather', 'build', 'carry', 'work'))
    require(type(loop) is bool, 'loop must be boolean')
    if job['action'] == 'death':
        require(not loop and sum(f.get('durationMs', 0) for f in frames) <= 4000, 'death must be nonlooping and at most 4000ms')
    for f in frames:
        require(f.get('status') in ('candidate', 'held', 'selected'), 'explicit frame status required')
        require(number(f.get('phase')) and 0 <= f['phase'] < 1, 'invalid frame phase')
        require(number(f.get('durationMs')) and 0 < f['durationMs'] <= 60000, 'invalid frame duration')
        events = f.get('events', [])
        require(isinstance(events, list) and len(events) <= 32, 'invalid frame events')
        for event in events:
            require(isinstance(event, dict) and re.fullmatch(r'[A-Z][A-Z0-9_]{0,63}', event.get('name', '')) and type(event.get('offsetMs')) is int and 0 <= event['offsetMs'] < f['durationMs'], 'invalid frame event marker')
        require('pivot' not in f and 'render' not in f and 'transform' not in f, 'per-frame pivot/scale/transform forbidden')
        if mode != 'diagnostic':
            require(f['status'] == 'selected' and isinstance(f.get('custody'), str) and f['custody'], 'selected frame and custody required')
    require(len({f['phase'] for f in frames}) == len(frames) and [f['phase'] for f in frames] == sorted(f['phase'] for f in frames), 'phases must be unique and ordered')
    require('identityMaster' not in job or job['schemaVersion'] == 2, 'identityMaster requires schema 2')
    identity_pin = None
    identity_master = None
    if 'identityMaster' in job:
        identity_master, identity_pin = pinned_image(job['identityMaster'], base, canvas)
    if mode == 'production':
        q = job.get('qualification', {})
        require(q.get('status') == 'qualified' and isinstance(q.get('record'), str) and q['record'], 'qualified record required')
        record = (base / q['record']).resolve().read_bytes()
        require(digest(record) == q.get('sha256'), 'qualification record SHA256 mismatch')
        qualification = json.loads(record)
        if building:
            require(qualification.get('kind') == 'building' and qualification.get('buildingType') == job['buildingType'] and qualification.get('direction') is None and qualification.get('canonicalDescriptorSHA') == job['canonicalDescriptor']['sha256'] and all(qualification.get(k) == job[k] for k in ('fixedCanvas', 'cell', 'pivot', 'render', 'contactShadow')), 'building qualification does not bind canonical kind/layout')
        require(qualification.get('status') == 'qualified' and all(qualification.get(k) == job[k] for k in ('masterSHA', 'family', 'action', 'direction')) and qualification.get('frameSHAs') == [f['input']['sha256'] for f in frames], 'qualification does not bind this cycle')
        if identity_pin is not None:
            require(qualification.get('identityMasterSHA') == identity_pin['sha256'], 'qualification does not bind identity master')
        if job['action'] == 'attack':
            require(sum(e['name'] in ('WEAPON_CONTACT', 'FIRE_PROJECTILE', 'DEAL_DAMAGE') for f in frames for e in f.get('events', [])) == 1, 'production attack requires one WEAPON_CONTACT, FIRE_PROJECTILE or DEAL_DAMAGE event')
        if job['action'] == 'walk':
            motion = job.get('locomotion', {})
            require(number(motion.get('distancePerCycle')) and motion['distancePerCycle'] > 0 and motion.get('measurementRecord') == q['record'] and motion.get('distancePerCycle') == qualification.get('distancePerCycle'), 'walk measured distance metadata required')
    columns = job.get('layout', {}).get('columns', min(15, len(frames)))
    require(type(columns) is int and 1 <= columns <= 15, 'invalid layout columns')
    rows = math.ceil(len(frames) / columns)
    stride = cell + 4
    size = (columns * stride, rows * stride)
    require(max(size) <= 2048, 'atlas exceeds 2048px; split into independently qualified jobs')
    pages = job.get('otherDecodedPages', [])
    unique = {}
    for page in pages:
        require(isinstance(page.get('path'), str) and re.fullmatch(r'[a-f0-9]{64}', page.get('sha256', '')), 'invalid decoded page pin')
        key = (page['path'], page['sha256'])
        require(all(type(page.get(k)) is int and page[k] > 0 for k in ('width', 'height')), 'invalid decoded page')
        require(key not in unique or unique[key] == page['width'] * page['height'] * 4, 'inconsistent duplicate page')
        unique[key] = page['width'] * page['height'] * 4
    memory = sum(unique.values()) + size[0] * size[1] * 4
    require(memory <= BUDGET, 'decoded unique-page memory exceeds 128 MiB')
    master, master_pin = pinned_image(job['master'], base, canvas)
    require(job['masterSHA'] == master_pin['sha256'], 'master SHA mismatch')
    identity_pin = identity_pin or master_pin
    identity_master = identity_master if identity_master is not None else master
    images = [pinned_image(f['input'], base, canvas) for f in frames]
    target = (base / job['output']['directory']).resolve()
    require(not target.exists(), 'refuse overwrite output')
    require(job['output']['runtimePath'] == 'atlas.png', 'runtime path must be atlas.png relative to descriptor')
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix='.sprite471-', dir=target.parent))
    try:
        (temporary / 'working').mkdir()
        atlas = Image.new('RGBA', size)
        descriptor_frames = []
        for i, (image, pin) in enumerate(images):
            image.resize((256, 256), Image.Resampling.LANCZOS).save(temporary / 'working' / f'{i:03}.png')
            x, y = (i % columns) * stride + 2, (i // columns) * stride + 2
            atlas.paste(image.resize((cell, cell), Image.Resampling.LANCZOS), (x, y))
            descriptor_frames.append(dict(x=x, y=y, width=cell, height=cell, durationMs=frames[i]['durationMs'], source=pin, events=frames[i].get('events', [])))
        atlas.save(temporary / 'atlas.png')
        runtime = dict(path='atlas.png', width=size[0], height=size[1], sha256=digest((temporary / 'atlas.png').read_bytes()), rgbaSha256=digest(atlas.tobytes()), derivation=dict(method='atlas', filter='lanczos', sourceSha256=images[0][1]['sha256']))
        descriptor = dict(identityMasterSHA=identity_pin['sha256'], directionalMasterSHA=master_pin['sha256'], id=job['id'], family=job['family'], kind='unit', state=job['action'], direction=job['direction'], source=images[0][1], runtime=runtime, cell=job['cell'], pivot=pivot, render=render, contactShadow=job['contactShadow'], alphaPolicy='transparent', frames=descriptor_frames, candidate=True, review=dict(status='CANDIDATE'), loop=loop)
        if building:
            descriptor.update(kind='building', direction=None, loadPolicy='on-demand', canonicalDescriptorSHA=job['canonicalDescriptor']['sha256'])
        if job['action'] == 'walk' and 'locomotion' in job:
            require(number(job['locomotion'].get('distancePerCycle')) and job['locomotion']['distancePerCycle'] > 0, 'invalid provisional locomotion distance')
            descriptor['locomotion'] = {**job['locomotion'], 'status': 'MEASURED' if mode == 'production' else 'PROVISIONAL'}
        (temporary / 'asset.json').write_text(json.dumps(descriptor, indent=2) + '\n')
        zoom = job.get('previewZoom', 1.68)
        require(number(zoom) and 0 < zoom <= 8, 'invalid preview zoom')
        preview_size = max(1, round(render['width'] * zoom))
        require(preview_size <= 1024, 'preview exceeds 1024px')
        # Whole canvases only; these previews do not qualify identity or contact.
        thumbs = [image.resize((128, 128), Image.Resampling.LANCZOS) for image, pin in images]
        contact = Image.new('RGBA', (columns * 144, rows * 160), (34, 38, 43, 255))
        draw = ImageDraw.Draw(contact)
        for i, thumb in enumerate(thumbs):
            x, y = (i % columns) * 144 + 8, (i // columns) * 160 + 8
            contact.alpha_composite(thumb, (x, y))
            draw.text((x, y + 130), f"F{i} {frames[i]['status']}", fill='white')
        contact.save(temporary / 'contact-sheet.png')
        identity_master.resize((128, 128), Image.Resampling.LANCZOS).save(temporary / 'master-preview.png')
        previews = [image.resize((preview_size, preview_size), Image.Resampling.LANCZOS) for image, pin in images]
        previews[0].save(temporary / 'game-size.png', save_all=True, append_images=previews[1:], duration=[f['durationMs'] for f in frames], loop=0 if loop else 1, disposal=0, blend=0)
        (temporary / 'preview.html').write_text(Path(__file__).with_name('sprite-preview.html').read_text())
        bank = []
        directions = set()
        for entry in job.get('previewBank', []):
            path = (base / entry['path']).resolve()
            raw = path.read_bytes()
            require(digest(raw) == entry['sha256'], 'bank descriptor SHA mismatch')
            asset = json.loads(raw)
            require(asset.get('identityMasterSHA') == identity_pin['sha256'], 'bank identity master SHA mismatch')
            require(asset['family'] == job['family'] and asset['state'] == job['action'] and asset['pivot'] == pivot and asset['render'] == render and (asset['source']['width'], asset['source']['height']) == canvas, 'bank changes identity layout/action')
            require(type(asset['direction']) is int and 0 <= asset['direction'] <= 7 and asset['direction'] not in directions, 'invalid or repeated bank direction')
            directions.add(asset['direction'])
            runtime_path = Path(asset['runtime']['path'])
            require(not runtime_path.is_absolute() and '..' not in runtime_path.parts, 'bank runtime must be descriptor relative')
            require(digest((path.parent / runtime_path).read_bytes()) == asset['runtime']['sha256'], 'bank runtime SHA mismatch')
            bank.append({'direction': asset['direction'], 'path': os.path.relpath(path, target)})
        require(len(bank) <= 8, 'bank allows at most eight directions')
        (temporary / 'preview-config.json').write_text(json.dumps({'zoom': zoom, 'mode': mode, 'bank': bank}) + '\n')
        receipt = dict(schemaVersion=1, mode=mode, visualApproval=False, installAuthorized=False, master=master_pin, identityMaster=identity_pin, inputJobSHA256=digest(job_path.read_bytes()), decodedUniquePageBytes=memory, decodedBudgetBytes=BUDGET, frameStatuses=[f['status'] for f in frames], outputPins={p.relative_to(temporary).as_posix():digest(p.read_bytes()) for p in temporary.rglob('*') if p.is_file()})
        (temporary / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
        require(not target.exists(), 'refuse overwrite output')
        os.rename(temporary, target)
    except BaseException:
        shutil.rmtree(temporary, ignore_errors=True)
        raise
    return receipt

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('job'); parser.add_argument('--mode', choices=['diagnostic', 'selected', 'production'], default='diagnostic')
    args = parser.parse_args()
    try:
        print(json.dumps(compile_job(args.job, args.mode)))
    except (ValueError, KeyError, OSError, TypeError) as error:
        parser.exit(1, f'{error}\n')
