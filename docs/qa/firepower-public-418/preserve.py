exec(open('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha/docs/qa/initial-actors-runtime-403/prepare.py').read().split('p=preserve();')[0]);O=R/'docs/qa/firepower-public-418';S=Path('/tmp/rds-firepower412-stage');B=Path('/tmp/rds-firepower412-build')
import sys
mode=sys.argv[1];assert mode in ['before','after'];a=preserve();assert a['HEAD']=='7994fb044b7811d12bb498627c7d28cce8fa2fe7';assert a['health']=={'ok':True,'rooms':0};binding=json.loads((R/'docs/qa/firepower-runtime-412/binding.json').read_text());assert inv(S)=={k:v['sha256'] for k,v in binding['sourcePins'].items()};assert inv(B)=={k:v['sha256'] for k,v in binding['buildPins'].items()};assert a['public']=={k:v['sha256'] for k,v in binding['buildPins'].items()};assert len(a['public'])==206;assert len(json.loads((R/'public/assets/art-v1/fort-202-manifest.json').read_text())['assets'])==50
if mode=='after':assert a==json.loads((O/'preservation-before.json').read_text())
(O/('preservation-'+mode+'.json')).write_text(json.dumps(a,indent=2))
exec((R/'docs/qa/initial-actors-public-404/prepare.py').read_text().split('intake=json.loads')[0]);O=R/'docs/qa/firepower-public-418';pol=policy();assert pol==json.loads((R/'docs/qa/firepower-runtime-412/policy-before.json').read_text())
if mode=='after':assert pol==json.loads((O/'policy-before.json').read_text())
(O/('policy-'+mode+'.json')).write_text(json.dumps(pol,indent=2));print('418 '+mode+' exactpreservation/sealed412/fullpolicy PASS')
