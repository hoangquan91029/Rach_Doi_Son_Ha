exec(open('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha/docs/qa/initial-actors-runtime-403/prepare.py').read().split('p=preserve();')[0]);O=R/'docs/qa/unit-scale-public-434';S=Path('/tmp/rds-unit-scale426-stage');B=Path('/tmp/rds-unit-scale426-build')
import sys
mode=sys.argv[1];assert mode in ['before','after'];a=preserve();assert a['HEAD']=='3a2ab48917d7fb7f3b50858e983037f4dbd44d5f';assert a['health']=={'ok':True,'rooms':0};binding=json.loads((R/'docs/qa/unit-scale-runtime-426/binding.json').read_text());assert inv(S)=={k:v['sha256'] for k,v in binding['sourcePins'].items()};assert inv(B)=={k:v['sha256'] for k,v in binding['buildPins'].items()};assert a['public']=={k:v['sha256'] for k,v in binding['buildPins'].items()};assert len(a['public'])==208
if mode=='after':assert a==json.loads((O/'preservation-before.json').read_text())
(O/('preservation-'+mode+'.json')).write_text(json.dumps(a,indent=2))
exec((R/'docs/qa/initial-actors-public-404/prepare.py').read_text().split('intake=json.loads')[0]);O=R/'docs/qa/unit-scale-public-434';pol=policy();assert pol==json.loads((R/'docs/qa/unit-scale-runtime-426/policy-before.json').read_text())
if mode=='after':assert pol==json.loads((O/'policy-before.json').read_text())
(O/('policy-'+mode+'.json')).write_text(json.dumps(pol,indent=2));print('434 '+mode+' exactpreservation/sealed426/fullpolicy PASS')
