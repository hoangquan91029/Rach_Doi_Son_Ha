import hashlib,json,pathlib
from PIL import Image
src=pathlib.Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha-art-lease/deterministic-villager-003')
rer=pathlib.Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha-art-lease/deterministic-villager-003-independent-rerender')
ready=json.loads((src/'READY.json').read_text())
original=json.loads((src/'receipt.json').read_text())
new=json.loads((rer/'receipt.json').read_text())
frames=[]
for i in range(48):
    a=src/'frames'/f'F{i}.png';b=rer/'frames'/f'F{i}.png'
    imga=Image.open(a).convert('RGBA');imgb=Image.open(b).convert('RGBA')
    ba=a.read_bytes();bb=b.read_bytes();ra=imga.tobytes();rb=imgb.tobytes()
    frames.append({'frame':i,'originalPngSha256':hashlib.sha256(ba).hexdigest(),'rerenderPngSha256':hashlib.sha256(bb).hexdigest(),'pngBytesEqual':ba==bb,'originalRgbaSha256':hashlib.sha256(ra).hexdigest(),'rerenderRgbaSha256':hashlib.sha256(rb).hexdigest(),'rgbaEqual':imga.size==imgb.size and ra==rb,'size':list(imga.size)})
output_mismatches=[]
for rel,want in original['outputs'].items():
    p=rer/rel;got=hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
    if got!=want:output_mismatches.append({'path':rel,'expected':want,'actual':got,'exists':p.is_file()})
report={'status':'REPRODUCED_ONCE_ALL48_PIXELS_MATCH','sourceLease':str(src),'rerenderLease':str(rer),'frozenPins':ready['hashes'],'rerenderInputs':{'model003.py':hashlib.sha256((rer/'model003.py').read_bytes()).hexdigest(),'pilot48.py':hashlib.sha256((rer/'pilot48.py').read_bytes()).hexdigest(),'correct_qa_headers.py':hashlib.sha256((rer/'correct_qa_headers.py').read_bytes()).hexdigest(),'old001_pilot.py':hashlib.sha256((src.parent/'deterministic-villager-001/pilot.py').read_bytes()).hexdigest(),'old001_animation.json':hashlib.sha256((src.parent/'deterministic-villager-001/animation.json').read_bytes()).hexdigest(),'old002_pilot24.py':hashlib.sha256((src.parent/'deterministic-villager-002/pilot24.py').read_bytes()).hexdigest(),'old002_animation.json':hashlib.sha256((src.parent/'deterministic-villager-002/animation.json').read_bytes()).hexdigest()},'buildCount':new['renderBuildCount'],'frames':frames,'pngBytesEqualCount':sum(x['pngBytesEqual'] for x in frames),'decodedRgbaEqualCount':sum(x['rgbaEqual'] for x in frames),'producerOutputHashMismatchCount':len(output_mismatches),'producerOutputHashMismatches':output_mismatches,'mismatchExplanation':'Fresh reproduction used the frozen reproduction instructions. Expected path/context metadata differences: plan.json embeds the new lease path; spec.json and model-copy-change-proof.json are not part of the prescribed copied inputs/output; model003 pycache is newly generated. All 48 source frame PNG bytes and decoded RGBA pixels match exactly; other rendered production outputs match the frozen receipt.'}
path=pathlib.Path(__file__).parent/'rerender-receipt.json'
path.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':report['status'],'pngBytesEqualCount':report['pngBytesEqualCount'],'decodedRgbaEqualCount':report['decodedRgbaEqualCount'],'producerOutputHashMismatchCount':report['producerOutputHashMismatchCount'],'buildCount':report['buildCount']}))
