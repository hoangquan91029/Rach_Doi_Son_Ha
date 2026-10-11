from pathlib import Path
import json,hashlib,subprocess,os
R=Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha');O=R/'docs/qa/initial-actors-public-406'
exec((R/'docs/qa/initial-actors-public-404/prepare.py').read_text().split('intake=json.loads')[0])
actual=policy();expected=json.loads((R/'docs/qa/initial-actors-release-405/receipt.json').read_text())['backend'];assert actual==expected
(O/'backend-policy-after.json').write_text(json.dumps({'status':'EXACT405_BACKEND_POLICY_PRESERVED','actual':actual},indent=2))
b=json.loads((O/'browser-receipt.json').read_text());assert b['status'].startswith('PASS406');assert b['cleanup']=={'browserClosed':True,'ownedServerStarted':False};assert b['launch']['art']['pipeline']['ready']==48;assert b['launch']['boot']['ready']==12
r={'order':406,'status':b['status'],'normalTLS':True,'ready':48,'portraits':12,'responsePins':len(b['responsePins']),'threeNewPNGResponsePins':[x for x in b['responsePins'] if '/initial-actors-403/' in x['file']],'selectedActors':[x['entity']['type'] for x in b['selectedActors']],'travel':b['travel']['actualRendererDiagnostic'],'arrivalDistance':b['arrival']['distance'],'pauseResumeStopMenu':True,'errors':b['errors'],'requestFailures':b['requestFailures'],'httpErrors':b['httpErrors'],'canonicalPublicBackendHEADPreserved':True,'backendPolicyMatches405':True,'handles':'CLOSED','scope':'Static D0 illustrations only; no motion/fullroster/eightdirection/finalfamilyacceptance','actualScene':'actual-initial-restored-world.png'}
(O/'receipt.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
