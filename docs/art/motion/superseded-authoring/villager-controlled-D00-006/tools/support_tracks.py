"""Persistent numeric IK helpers. No images/geometry previews or assumed bone lengths.
Use only after actual original segment landmarks and static calibrations are locked.
"""
import math
def solve_two_bone(root,target,upper,lower,pole_sign):
 if min(upper,lower)<=0 or pole_sign not in [-1,1]:raise ValueError('Measured positive lengths and persistent pole ownership required')
 dx,dy=target[0]-root[0],target[1]-root[1];distance=math.hypot(dx,dy)
 if not abs(upper-lower)+1e-6<distance<upper+lower-1e-6:raise ValueError('Target unreachable without stretching; revise contact/stride hypothesis')
 along=(upper*upper-lower*lower+distance*distance)/(2*distance);height=math.sqrt(max(0,upper*upper-along*along));ux,uy=dx/distance,dy/distance
 return [root[0]+ux*along-uy*height*pole_sign,root[1]+uy*along+ux*height*pole_sign]
def contact_track(phase,side,stride_source,lift_source,direction=(2/math.sqrt(5),1/math.sqrt(5))):
 if side not in ['near','far'] or stride_source<0 or lift_source<0:raise ValueError('Stable side and nonnegative calibrated stride/clearance required')
 q=(phase+(0 if side=='near' else .5))%1
 if q<.5:along=(.25-q)*stride_source;lift=0;support=True
 else:
  t=(q-.5)*2;h00=2*t**3-3*t**2+1;h10=t**3-2*t**2+t;h01=-2*t**3+3*t**2;h11=t**3-t**2
  # Match stance velocity at both swing/contact ends; no velocity jump at seam.
  along=stride_source*(-.25*h00-.5*h10+.25*h01-.5*h11);lift=lift_source*math.sin(math.pi*t)**2;support=False
 return {'offset':[direction[0]*along,direction[1]*along-lift],'support':support}
def reachable_stride(hips,feet,lengths,clearance,upper_bound,direction=(2/math.sqrt(5),1/math.sqrt(5)),samples=96):
 """Conservative source-space proposal capped by both real legs over the entire track.
 hips is a callable of side/phase returning actual core attachment (includes authored bob).
 No successful value constitutes contact or motion acceptance.
 """
 def reachable(stride):
  for side in ['near','far']:
   upper,lower=lengths[side]
   for n in range(samples):
    phase=n/samples;track=contact_track(phase,side,stride,clearance,direction);target=[feet[side][i]+track['offset'][i] for i in [0,1]];d=math.dist(hips(side,phase),target)
    if not abs(upper-lower)+1<d<(upper+lower)*.98:return False
  return True
 if not reachable(0):raise ValueError('Rest/support/clearance itself exceeds actual leg reach; calibrate static assembly first')
 low,high=0,upper_bound
 for _ in range(40):
  mid=(low+high)/2
  if reachable(mid):low=mid
  else:high=mid
 return low*.9
