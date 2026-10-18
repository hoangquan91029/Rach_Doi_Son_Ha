#!/usr/bin/env python3
"""Lossless native-pixel QA/packing. Never repairs or normalizes provider artwork."""
import argparse
import hashlib
import json
import subprocess
import re
from pathlib import Path
from PIL import Image, ImageOps

def fingerprint(image):
    return bytes(v for r,g,b,a in image.get_flattened_data() for v in ((r,g,b,a) if a else (0,0,0,0)))

DIRECTIONS = ['S','SW','W','NW','N','NE','E','SE']

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def load_png(path, size):
    with Image.open(path) as image:
        if image.format != 'PNG' or image.mode != 'RGBA' or image.size != size:
            raise ValueError(f'native RGBA PNG {size} required: {path}')
        image.load()
        return image.copy()

def check_frames(frames, palette=None):
    colors = set()
    seen = set()
    for i, frame in enumerate(frames):
        if frame.size != (128,128) or frame.mode != 'RGBA':
            raise ValueError('native128 RGBA frame required')
        pixels = list(frame.get_flattened_data())
        if any(a not in (0,255) for r,g,b,a in pixels):
            raise ValueError(f'nonbinary alpha frame{i}')
        if not any(a for r,g,b,a in pixels):
            raise ValueError(f'empty silhouette frame{i}')
        if any(pixels[y*128+x][3] for y in range(128) for x in range(128) if x<2 or x>=126 or y<2 or y>=126):
            raise ValueError(f'border frame{i}')
        colors.update((r,g,b) for r,g,b,a in pixels if a)
        digest = hashlib.sha256(fingerprint(frame)).hexdigest()
        if digest in seen:
            raise ValueError(f'duplicate frame{i}')
        seen.add(digest)
    if len(colors)>32:
        raise ValueError('palette exceeds32')
    if palette is not None:
        declared = {tuple(bytes.fromhex(c[1:])) for c in palette}
        if not colors <= declared:
            raise ValueError('undeclared palette color')
    return colors

def check_direction_rows(rows):
    fingerprints = [[hashlib.sha256(fingerprint(f)).digest() for f in row] for row in rows]
    mirrors = [[hashlib.sha256(fingerprint(ImageOps.mirror(f))).digest() for f in row] for row in rows]
    for r in range(len(rows)):
        for previous in range(r):
            for offset in range(8):
                for comparison in (fingerprints[previous], mirrors[previous]):
                    if all(fingerprints[r][f] == comparison[(f+offset)%8] for f in range(8)):
                        raise ValueError('duplicated/mirrored direction substitution (including shifted phases)')
    # Within-row mirror equality can also occur in a legitimately symmetric pose.
    # This check rejects whole direction substitution, not inferred authorship.


def strip_frames(path):
    strip = load_png(path, (1024,128))
    frames = [strip.crop((i*128,0,(i+1)*128,128)) for i in range(8)]
    check_frames(frames)
    return frames

def validate_provenance(provenance, root):
    if set(provenance) != {'sources','callTokens'} or not provenance['sources'] or not provenance['callTokens']:
        raise ValueError('source/call provenance required')
    if len(set(provenance['callTokens'])) != len(provenance['callTokens']) or any(not isinstance(t,str) or not t.strip() for t in provenance['callTokens']):
        raise ValueError('invalid call tokens')
    for pin in provenance['sources']:
        if set(pin) != {'path','sha256'}:
            raise ValueError('source pin fields')
        source = (root / pin['path']).resolve()
        declared = Path(pin['path']).as_posix()
        actual = source.relative_to(root.resolve()).as_posix() if source.is_relative_to(root.resolve()) else ''
        allowed = r'docs/art/pixel-[a-zA-Z0-9_-]+/(raw|raws)/[^.][^\\]*\.png'
        if not re.fullmatch(allowed,declared) or '..' in Path(declared).parts or not re.fullmatch(allowed,actual):
            raise ValueError('pixel sources must be new docs/art/pixel-*/raw[s] PNGs; legacy/reference pixels forbidden')
        if not source.is_relative_to(root.resolve()) or sha(source) != pin['sha256']:
            raise ValueError('source pin mismatch/outside root')
    # Hashes and tokens establish recorded bytes, never provider authenticity or visual approval.

def validate_atlas(path, metadata, root):
    validator = (Path(__file__).resolve().parents[1] / 'client/pixel-animation.js').as_uri()
    check = subprocess.run(['node','--input-type=module','-e',f'import {{validatePixelClip}} from {json.dumps(validator)}; let data="";for await (const part of process.stdin)data+=part;validatePixelClip(JSON.parse(data));'],input=json.dumps(metadata),text=True,capture_output=True)
    if check.returncode: raise ValueError('metadata schema invalid: '+check.stderr.strip())
    validate_provenance(metadata['provenance'], root)
    expected = f"{metadata['identity']}_{metadata['action']}.png"
    if Path(path).name != expected or Path(metadata['atlas']).name != expected:
        raise ValueError('identity/action filename binding')
    image = load_png(path,(1024,1024))
    rows = [[image.crop((f*128,r*128,(f+1)*128,(r+1)*128)) for f in range(8)] for r in range(8)]
    colors = set()
    for frames in rows:
        colors.update(check_frames(frames,metadata['palette']))
    if len(colors)>32:
        raise ValueError('identity palette exceeds32')
    check_direction_rows(rows)
    return image, rows

def pack(strips, destination, palette=None):
    if len(strips)!=8:
        raise ValueError('exact8 ordered direction strips required')
    rows = [strip_frames(p) for p in strips]
    colors = set()
    for row in rows:
        colors.update(check_frames(row,palette))
    if len(colors)>32:
        raise ValueError('identity palette exceeds32')
    check_direction_rows(rows)
    atlas = Image.new('RGBA',(1024,1024))
    for r,row in enumerate(rows):
        for f,frame in enumerate(row):
            atlas.paste(frame,(128*f,128*r))
    with open(destination,'xb') as output:
        atlas.save(output,format='PNG')
    return sha(destination)

def preview(frames, durations, destination, scale=1):
    if len(frames)!=8 or len(durations)!=8 or any(type(d)!=int or d<=0 or d%10 for d in durations):
        raise ValueError('GIF exact timing requires8 positive multiples of10ms')
    if scale not in (1,2,4):
        raise ValueError('nearest integer preview scale1/2/4')
    check_frames(frames)
    colors=sorted({(r,g,b) for f in frames for r,g,b,a in f.get_flattened_data() if a})
    lookup={color:i+1 for i,color in enumerate(colors)}
    palette=[0,0,0]+[v for c in colors for v in c]
    palette += [0]*(768-len(palette))
    indexed=[]
    for frame in frames:
        p=Image.new('P',(128,128));p.putpalette(palette)
        p.putdata([lookup[(r,g,b)] if a else 0 for r,g,b,a in frame.get_flattened_data()])
        if scale!=1:p=p.resize((128*scale,128*scale),Image.Resampling.NEAREST)
        indexed.append(p)
    with open(destination,'xb') as output:
        indexed[0].save(output,format='GIF',save_all=True,append_images=indexed[1:],duration=durations,loop=0,transparency=0,disposal=2,optimize=False)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['inspect-strip','pack','inspect-atlas','preview'])
    parser.add_argument('inputs',nargs='+')
    parser.add_argument('--output');parser.add_argument('--metadata');parser.add_argument('--root',default='.');parser.add_argument('--row',type=int,default=0)
    args=parser.parse_args()
    try:
        metadata=json.loads(Path(args.metadata).read_text()) if args.metadata else None
        if args.command=='inspect-strip':
            if len(args.inputs)!=1:raise ValueError('one strip required')
            frames=strip_frames(args.inputs[0]);result={'frames':len(frames),'sha256':sha(args.inputs[0])}
        elif args.command=='pack':
            if not args.output:raise ValueError('--output required')
            result={'sha256':pack(args.inputs,args.output,metadata['palette'] if metadata else None)}
        else:
            if not metadata or len(args.inputs)!=1:raise ValueError('one atlas and --metadata required')
            image,rows=validate_atlas(args.inputs[0],metadata,Path(args.root))
            if args.command=='preview':
                if not args.output or args.row not in range(8):raise ValueError('--output and row0..7 required')
                preview(rows[args.row],metadata['frameDurationsMs'],args.output)
            result={'sha256':sha(args.inputs[0])}
        print(json.dumps({'structural':'PASS','visual':'UNKNOWN','runtime':'UNKNOWN',**result}))
    except (ValueError,OSError,KeyError,TypeError) as error:
        print(json.dumps({'structural':'HELD','reason':str(error),'visual':'UNKNOWN','runtime':'UNKNOWN'}));raise SystemExit(1)
if __name__=='__main__':main()
