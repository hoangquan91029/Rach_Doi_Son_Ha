exec(open('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha/docs/qa/firepower-runtime-410/prepare.py').read().split('p=preserve();')[0])
assert inv(S)==json.loads((O/'stage-inventory.json').read_text());before=json.loads((O/'preservation-before.json').read_text());assert preserve()==before
bp=inv(B)
for rel,pin in before['public'].items():
 if rel!='assets/art-v1/fort-202-manifest.json':assert bp[rel]==pin,rel
assert len(bp)==206
binding={'stage':str(S),'build':str(B),'sourcePins':{k:{'sha256':v} for k,v in inv(S).items()},'buildPins':{k:{'sha256':v} for k,v in bp.items()},'immutableSealed':True,'bundleSHA256':bp['assets/index-8telBS7h.js']}
(O/'binding.json').write_text(json.dumps(binding,indent=2));print(json.dumps({'status':'SEALED410','files':len(bp),'JS':binding['bundleSHA256']}))
