"""Authoring prototype only: coherent whole-garment radial capsule clearance. NO rendering.
Frozen003 owns motion; frozen004 owns all mesh topology/materials. Realisticappearance unqualified.
"""
import sys
sys.dont_write_bytecode=True
import hashlib,importlib.util,json,pathlib
import numpy as np
BASE=pathlib.Path(__file__).resolve().parent
REPO=pathlib.Path('/home/kieu-hoang-quan/Videos/Rach_Doi_Son_Ha')
INPUTS=json.loads((BASE/'WORK_ORDER.json').read_text())['inputs']
CAPSULE_RADII={'thigh':.190,'trouser_shin':.140,'wrap':.094}
CLEARANCE=.012;CHORD_MARGIN=.014;MAX_RADIAL_STEP=.36;BINARY_STEPS=28
LOWER_FULL_REST_Z=.96;UPPER_ANCHOR_REST_Z=1.08

def sha(path):return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()
def verify_inputs():
 for rel,digest in INPUTS.items():
  if sha(REPO/rel)!=digest:raise ValueError('frozen input changed: '+rel)
 return {str(REPO/rel):digest for rel,digest in INPUTS.items()}
def load(rel,name):
 spec=importlib.util.spec_from_file_location(name,REPO/rel);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
verify_inputs()
MOTION=load('docs/art/pipeline/deterministic-villager-003/model003.py','binding005_frozen_motion003')
APPEARANCE=load('docs/art/pipeline/canonical-villager-contacts-004/model-appearance-v1.py','binding005_frozen_appearance004')

def capsules(p):
 result=[]
 for side in ('LEFT','RIGHT'):
  H=p['joints'][side+'_hip'];K=p['joints'][side+'_knee'];A=p['joints'][side+'_ankle'];cuff=K+.66*(A-K)
  for name,a,b in [('thigh',H,K),('trouser_shin',K,cuff),('wrap',cuff,A)]:result.append((side+'_'+name,np.asarray(a),np.asarray(b),CAPSULE_RADII[name]))
 return result

def signed_clearance(points,p):
 result=np.full(len(points),np.inf)
 for _,a,b,r in capsules(p):
  axis=b-a;t=np.clip((points-a)@axis/(axis@axis),0,1);nearest=a+t[:,None]*axis;result=np.minimum(result,np.linalg.norm(points-nearest,axis=1)-r)
 return result

def weight(rest_z):
 t=np.clip((rest_z-LOWER_FULL_REST_Z)/(UPPER_ANCHOR_REST_Z-LOWER_FULL_REST_Z),0,1)
 return 1-t*t*(3-2*t)

def warp(points,p):
 """One shared pose field for shell, panels and hem; keeps every vertex Z unchanged.
Outward garment-azimuth ray avoids side-dependent detached limb fitting. Uniform worst-radius
capsules deliberately overestimate hip/ankle regions; this may over-expand the garment silhouette.
Binary solve has fixed counts; no historicalframe state, fitting, renderer or source image.
 """
 points=np.asarray(points,dtype=float);result=points.copy();rest_z=points[:,2]-(p['bob']-.06);weights=weight(rest_z);active=weights>0
 if not np.any(active):return result
 q=points[active];direction=q[:,:2]-np.array([p['sway'],0]);length=np.linalg.norm(direction,axis=1);direction/=np.maximum(length[:,None],1e-15);direction[length<1e-12]=[0,1]
 need=signed_clearance(q,p)<CLEARANCE+CHORD_MARGIN;lo=np.zeros(len(q));hi=np.full(len(q),MAX_RADIAL_STEP)
 for _ in range(BINARY_STEPS):
  step=(lo+hi)/2;trial=q.copy();trial[:,:2]+=direction*step[:,None];outside=signed_clearance(trial,p)>=CLEARANCE+CHORD_MARGIN;hi=np.where(outside,step,hi);lo=np.where(outside,lo,step)
 step=np.where(need,hi,0)*weights[active];result[active,:2]+=direction*step[:,None]
 return result

def garment_indices(mesh):
 tri=np.asarray(mesh.tri,dtype=int);garment_faces=np.asarray(mesh.ids)==APPEARANCE.IDS['tunic'];return np.unique(tri[garment_faces]),garment_faces

def bind_pose(p):
 """Returns newfrozen004 mesh instance with coherent tunic deformation only. No module mutations."""
 mesh=APPEARANCE.mesh_for(p);original=np.asarray(mesh.v,dtype=float);vertices=original.copy();indices,faces=garment_indices(mesh);vertices[indices]=warp(original[indices],p)
 mesh.v=list(vertices);normals=np.asarray(mesh.n,dtype=float).copy();tri=np.asarray(mesh.tri,dtype=int)[faces];normals[indices]=0;face_normals=np.cross(vertices[tri[:,1]]-vertices[tri[:,0]],vertices[tri[:,2]]-vertices[tri[:,0]])
 for corner in range(3):np.add.at(normals,tri[:,corner],face_normals)
 lengths=np.linalg.norm(normals[indices],axis=1);normals[indices]/=np.maximum(lengths[:,None],1e-15);mesh.n=list(normals)
 return mesh,original,indices,faces

def mesh_for(p):return bind_pose(p)[0]
def pose(phase):return MOTION.pose(phase)
