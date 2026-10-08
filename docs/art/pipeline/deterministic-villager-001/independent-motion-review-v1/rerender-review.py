import hashlib, importlib.util, json, pathlib, sys
from PIL import Image
src = pathlib.Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha-art-lease/deterministic-villager-001')
out = pathlib.Path(__file__).parent
sys.path.insert(0, str(src))
spec = importlib.util.spec_from_file_location('frozen_pilot', src/'pilot.py')
pilot = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pilot)
meta = json.loads((src/'animation.json').read_text())
records=[]
for rec in meta['frameRecords']:
    frame = int(rec['frame'])
    phase = float(rec['phase'])
    image, mask, depth, normal, limb_id, geo = pilot.render(pilot.pose(phase))
    target = out/'frames'/f"F{frame}.png"
    image.save(target)
    original = src/rec['path']
    original_img = Image.open(original).convert('RGBA')
    rendered_img = Image.open(target).convert('RGBA')
    records.append({
        'frame': frame, 'phase': phase,
        'original_path': str(original), 'rerender_path': str(target),
        'original_png_sha256': hashlib.sha256(original.read_bytes()).hexdigest(),
        'rerender_png_sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
        'png_bytes_equal': original.read_bytes() == target.read_bytes(),
        'original_rgba_sha256': hashlib.sha256(original_img.tobytes()).hexdigest(),
        'rerender_rgba_sha256': hashlib.sha256(rendered_img.tobytes()).hexdigest(),
        'rgba_equal': original_img.size == rendered_img.size and original_img.tobytes() == rendered_img.tobytes(),
        'size': list(rendered_img.size),
        'alpha_bounds': list(rendered_img.getbbox()),
        'alpha_height': rendered_img.getbbox()[3]-rendered_img.getbbox()[1],
    })
receipt={
  'status':'REVIEW_ONLY_RERENDER_COMPLETE',
  'source_dir':str(src),
  'pinned_hashes':{
    'pilot.py':hashlib.sha256((src/'pilot.py').read_bytes()).hexdigest(),
    'animation.json':hashlib.sha256((src/'animation.json').read_bytes()).hexdigest(),
    'receipt.json':hashlib.sha256((src/'receipt.json').read_bytes()).hexdigest(),
    'spec.json':hashlib.sha256((src/'spec.json').read_bytes()).hexdigest(),
  },
  'method':'Imported frozen pilot.py and called its original render(pose(phase)) once per the eight animation.json frame phases. No build/freeze/CLI paths; only this new review directory was written.',
  'frames':records,
  'all_png_bytes_equal':all(x['png_bytes_equal'] for x in records),
  'all_rgba_equal':all(x['rgba_equal'] for x in records),
}
(out/'rerender-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'status':receipt['status'],'all_png_bytes_equal':receipt['all_png_bytes_equal'],'all_rgba_equal':receipt['all_rgba_equal'],'frames':len(records)}))
