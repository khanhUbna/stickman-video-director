"""Shared-vertex texture skinning. One continuous suit silhouette, no joint caps.
Artwork is warped only as part of rendering video frames. No generative service.
"""
import sys,math
from pathlib import Path
sys.path.insert(0,'/workspace/.cache/silver-jacket-mesh-deps')
import cv2
import numpy as np
from PIL import Image
S=.36
def smooth(x):x=np.clip(x,0,1);return x*x*(3-2*x)
def affine(points,a,b,c,d):
 a,b,c,d=map(lambda p:np.asarray(p,dtype=float),(a,b,c,d))
 q=b-a;r=d-c;angle=math.atan2(r[1],r[0])-math.atan2(q[1],q[0])
 co,si=math.cos(angle),math.sin(angle);rot=np.array([[co,-si],[si,co]])
 return (points-a)@rot.T*S+c
class Skin:
 def __init__(self,path):
  im=Image.open(path).convert('RGB');a=np.asarray(im).astype(np.float32)
  alpha=np.clip((253-a.min(axis=2))/10,0,1)
  # Keep the head/neck separate to preserve its authored facial animation.
  yy=np.arange(a.shape[0])[:,None];alpha*=smooth((yy-326)/25)
  premul=np.concatenate((a*alpha[:,:,None],alpha[:,:,None]*255),axis=2)
  self.texture=cv2.resize(premul,None,fx=S,fy=S,interpolation=cv2.INTER_AREA)
  xs=np.unique(np.r_[np.arange(0,1024,24),1023]);ys=np.unique(np.r_[np.arange(312,1536,24),1535])
  xx,yy=np.meshgrid(xs,ys);self.points=np.c_[xx.ravel(),yy.ravel()].astype(float)
  tris=[];ny,nx=xx.shape
  for j in range(ny-1):
   for i in range(nx-1):
    n=j*nx+i
    for tr in [(n,n+1,n+nx),(n+1,n+nx+1,n+nx)]:
     pp=self.points[list(tr)]*S;lo=np.floor(pp.min(axis=0)).astype(int);hi=np.ceil(pp.max(axis=0)).astype(int)
     block=self.texture[max(0,lo[1]):hi[1]+1,max(0,lo[0]):hi[0]+1,3]
     if block.size and block.max()>4:tris.append(tr)
  def z(tr):
   x,y=self.points[list(tr)].mean(axis=0)
   if y>775 and 300<x<740:return 0 if x<512 else 1
   if y>350 and x<350:return 3
   if y>350 and x>675:return 4
   return 2
  self.triangles=np.array(sorted(tris,key=z));self.bind=self.points*S
  self.x=self.points[:,0];self.y=self.points[:,1]
 def deform(self,root,hy,arms,legs):
  p=self.points;x=self.x;y=self.y
  body=(p-np.array([512,802]))*S+np.array([root,hy]);out=body.copy()
  for side,chain in enumerate(arms):
   a,b,c=chain
   src=([(333,408),(267,586),(174,779)] if side==0 else [(691,408),(757,586),(850,779)])
   up=affine(p,src[0],src[1],a,b);low=affine(p,src[1],src[2],b,c)
   bend=smooth((y-530)/110)
   cut=385-30*smooth((y-420)/100) if side==0 else 639+30*smooth((y-420)/100)
   branch=smooth(((cut-x) if side==0 else (x-cut))/45)*smooth((y-330)/75)
   branch*=1-smooth((y-960)/40)
   result=up*(1-bend[:,None])+low*bend[:,None]
   out=out*(1-branch[:,None])+result*branch[:,None]
  for side,chain in enumerate(legs):
   a,b,c,angle=chain
   src=([(427,802),(391,1081),(354,1400)] if side==0 else [(590,802),(633,1081),(674,1400)])
   up=affine(p,src[0],src[1],a,b);low=affine(p,src[1],src[2],b,c)
   bend=smooth((y-1025)/112);result=up*(1-bend[:,None])+low*bend[:,None]
   r=math.radians(angle);co,si=math.cos(r),math.sin(r);rot=np.array([[co,-si],[si,co]])
   shoe=(p-np.array(src[2]))@rot.T*S+np.array(c)
   ankle=smooth((y-1350)/70);result=result*(1-ankle[:,None])+shoe*ankle[:,None]
   lower=smooth((y-950)/60)
   lateral=smooth((x-300)/30)*smooth((730-x)/30)
   region=((x<512) if side==0 else (x>=512))*(lateral*(1-lower)+lower)
   branch=smooth((y-760)/85)*region
   out=out*(1-branch[:,None])+result*branch[:,None]
  return out
 def render(self,vertices,hide_right_hand=False):
  texture=self.texture
  if hide_right_hand:
   texture=texture.copy();yy,xx=np.indices(texture.shape[:2]);fade=1-smooth((yy/S-786)/16)*smooth((xx/S-790)/25)
   texture*=fade[:,:,None]
  low=np.floor(vertices[self.triangles].min(axis=(0,1))).astype(int)-2
  high=np.ceil(vertices[self.triangles].max(axis=(0,1))).astype(int)+2
  # Source vertices far outside the silhouette do not enlarge the canvas.
  width,height=(high-low+1).tolist();canvas=np.zeros((height,width,4),np.float32)
  for tri in self.triangles:
   src=self.bind[tri].astype(np.float32);dst=(vertices[tri]-low).astype(np.float32)
   x0,y0=np.floor(dst.min(axis=0)).astype(int);x1,y1=np.ceil(dst.max(axis=0)).astype(int)+1
   if x1<=x0 or y1<=y0:continue
   relative=dst-np.array([x0,y0],np.float32)
   mat=cv2.getAffineTransform(src,relative)
   patch=cv2.warpAffine(texture,mat,(x1-x0,y1-y0),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT)
   mask=np.zeros(patch.shape[:2],np.uint8);cv2.fillConvexPoly(mask,np.round(relative).astype(np.int32),255)
   area=canvas[y0:y1,x0:x1];alpha=patch[:,:,3:4]/255
   use=mask>0
   composed=patch+area*(1-alpha)
   area[use]=composed[use]
  alpha=canvas[:,:,3:4]/255
  rgb=np.divide(canvas[:,:,:3],np.maximum(alpha,1e-6))
  rgba=np.concatenate((rgb,canvas[:,:,3:4]),axis=2).clip(0,255).astype(np.uint8)
  return Image.fromarray(rgba),tuple(low.tolist())
