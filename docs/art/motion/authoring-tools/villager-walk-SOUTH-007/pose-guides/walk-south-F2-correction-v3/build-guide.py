"""Single MODEL_ONLY F2 correction. Reuses immutable numeric geometry, never character pixels."""
import pathlib,json,hashlib,math
P=pathlib.Path(__file__).parent;V2=P.parent/'walk-south-keys-v2';V1=P.parent/'walk-south-keys-v1';LEASE=P.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for folder in [V1,V2]:
 for name,digest in json.loads((folder/'SHA256SUMS.json').read_text()).items():assert sha(folder/name)==digest
F0=LEASE/'walk/keys/F00-left-contact-01/raw.png';F2=LEASE/'walk/keys/F02-right-passing-01/raw.png'
assert sha(F0)=='803163981d41540f237ac3b53652e73eab82f8a35a8ffa68c5db7d4f57019001'
assert sha(F2)=='1c41fdda017b5f64dd7bb03deb5c0c72a24c0d18cacbbbf1f79b2e1c2a274366'
plan=json.loads((V2/'coordinate-plan.json').read_text());f0=plan['frames'][0];f2=plan['frames'][1];pts=f2['points2D']
# The SVG foot cap is a quadratic fromtoeY-15 via toeY to toeY-15: maximumtoeY-7.5.
def contour_extent(frame,side):return frame['points2D'][side+'_toe'][1]-7.5
source_model=contour_extent(f0,'LEFT');target=contour_extent(f2,'LEFT');passing=contour_extent(f2,'RIGHT')
assert source_model-target==80 and target==1137.5 and passing==1057.5
assert f2['soles']['LEFT']['heightAboveGround']==0 and f2['soles']['RIGHT']['heightAboveGround']==80
assert f2['points3D']['LEFT_ankle'][1]==f2['points3D']['RIGHT_ankle'][1]==-100
for endpoint in ['worldHeel','worldToe']:assert f0['soles']['LEFT'][endpoint]==f2['soles']['LEFT'][endpoint]
for side in ['LEFT','RIGHT']:
 for a,b,length in [('hip','knee',260),('knee','ankle',240),('shoulder','elbow',200),('elbow','wrist',180)]:assert abs(math.dist(f2['points3D'][side+'_'+a],f2['points3D'][side+'_'+b])-length)<1e-8
contract={'status':'MODEL_ONLY_SINGLE_F2_CORRECTION_PARENT_AUDIT_PENDING','canvas':[1254,1254],'root':[654,1140],'geometrySource':{'path':str(V2/'coordinate-plan.json'),'sha256':sha(V2/'coordinate-plan.json')},'characterReferences':[{'role':'accepted F0 inspected only','path':str(F0),'sha256':sha(F0)},{'role':'held F2 inspected only; not selected','path':str(F2),'sha256':sha(F2)}],'frame':2,'timeMs':150,'support':'LEFT / viewer RIGHT','passing':'RIGHT / viewer LEFT','unchangedF2Geometry':f2,'targetExtents':{'supportModelOutlineBottomY':target,'passingModelOutlineBottomY':passing,'F0ModelOutlineBottomY':source_model,'exactModelBackwardLocalDisplacementY':-80,'observedF0ApproxBottomY':1208,'observedHeldF2ApproxBottomY':1206,'observedF0GhostApproxY':1210,'observedReferenceIsNotExactModelTrack':True},'stablePlanes':{'hatApexY':30,'shoulderY':280,'hipY':590,'rootY':1140,'anatomicalLeftSoleCenterX':754,'anatomicalRightSoleCenterX':554},'bodyShift':{'sourcePx':55,'meaning':'authored shift toward support, not measured exact COM'},'closedGates':['Finished source frame authoring requires parent direction/identity gate authorization','No motion/loop/art/runtime qualification from geometry'], 'sourcePixelOperations':False,'imageCalls':0,'finishedArt':False,'motionQualified':False}
(P/'coordinate-contract.json').write_text(json.dumps(contract,indent=2)+'\n')
plain=(V2/'F2.svg').read_text().replace('SOUTH F2 — 150ms','SOUTH F2 CORRECTION TARGET — 150ms')
(P/'guide.svg').write_text(plain)
qa=(V2/'F2-qa.svg').read_text().replace('SOUTH F2 — 150ms','SOUTH F2 CORRECTION TARGET — 150ms')
marks=[]
# Geometry ghost only, not traced/reference pixels. Its footer differentiates approximateobservedreference from contractual ghost.
def foot_outline(side,dy,color,dash=''):
 heel,toe=pts[side+'_heel'],pts[side+'_toe'];x=heel[0];hy=heel[1]+dy;ty=toe[1]+dy
 return f'<path d="M{x-32} {hy}L{x-29} {hy-23}L{x+29} {hy-23}L{x+32} {ty-15}Q{x} {ty} {x-32} {ty-15}Z" fill="none" stroke="{color}" stroke-width="4" stroke-dasharray="{dash}"/>'
marks.extend([foot_outline('LEFT',0,'#146d91'),foot_outline('RIGHT',0,'#146d91'),foot_outline('LEFT',80,'#bf6b2c','8 7'),foot_outline('LEFT',1210-target,'#9a8b72','3 8')])
for y,color in [(target,'#146d91'),(passing,'#146d91'),(source_model,'#bf6b2c')]:marks.append(f'<path d="M680 {y}H842" stroke="{color}" stroke-width="2" stroke-dasharray="6 4"/>')
marks.append(f'<path d="M825 {target}V{source_model}m-6 -6l6 6l6 -6M819 {target+6}l6 -6l6 6" stroke="#bf6b2c" stroke-width="3" fill="none"/>')
for x,y,label,color in [(868,1068,'LEFT SUPPORT target bottom≈1138','#146d91'),(868,1095,'LOCAL STANCE retreat −80px','#146d91'),(868,1122,'Foot stays planted; do not leave atF0','#146d91'),(868,1180,'Orange F0 model ghost≈1218','#bf6b2c'),(868,1207,'Grey observed F0 ghost≈1210','#756951'),(30,1140,'RIGHT airborne PASSING: sole≈1058','#146d91'),(30,1165,'Same ground depth as LEFT, gap80','#146d91'),(30,1190,'Observed F0≈1208 / held F2≈1206','#756951'),(30,1215,'Those approximate source values are NOT the model80px track.','#756951')]:marks.append(f'<text x="{x}" y="{y}" font-family="sans-serif" font-size="17" fill="{color}">{label}</text>')
# Stable source planes, small segments outside character. No fullimage translation or fitting.
for y,label in [(30,'HAT30'),(280,'SHOULDER280'),(590,'HIP590')]:marks.append(f'<path d="M{1020 if y==30 else 20} {y}H{1105 if y==30 else 85}" stroke="#8c9584" stroke-width="2"/><text x="{1024 if y==30 else 24}" y="{y+20}" font-size="14" fill="#697260">{label}</text>')
qa=qa.replace('</svg>',''.join(marks)+'</svg>');(P/'guide-qa.svg').write_text(qa)
print('PASS singleF2 contract: fixed geometry/bones/canvas/root, exact80px local retreat, passing80px above same grounddepth, immutablev1/v2 and originalF0/F2 hashes preserved. NON_ART only.')
