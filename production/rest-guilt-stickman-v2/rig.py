"""Project-local articulated painted actor; inherited B6 standing runtime unchanged."""
from pathlib import Path
from functools import lru_cache
import json,math
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
B=Path(__file__).resolve().parent;S=1.10;FLOOR=590.;INK='#202936'
PACKS={k:json.loads((B/f'characters/{v}/package.json').read_text()) for k,v in [('hero','protagonist'),('friend','friend')]}
PATHS={'hero':B/'characters/protagonist','friend':B/'characters/friend'}
def ease(x):x=max(0.,min(1.,x));return x*x*(3-2*x)
def mix(a,b,u):return np.asarray(a,float)*(1-u)+np.asarray(b,float)*u
def rotate(p,a):
 a=math.radians(a);x,y=p;return np.array([math.cos(a)*x-math.sin(a)*y,math.sin(a)*x+math.cos(a)*y])
def ip(p):return tuple(round(float(v)) for v in p)
def line(g,p,fill=INK,width=6):g.line([ip(x) for x in p],fill=fill,width=round(width),joint='curve')
def poly(g,p,fill,outline='#695447',width=3):
 g.polygon([ip(x) for x in p],fill=fill)
 if outline:line(g,p+[p[0]],outline,width)
def ik(root,target,lengths,pole,name):
 root=np.asarray(root,float);target=np.asarray(target,float);v=target-root;d=float(np.linalg.norm(v));a,b=lengths
 if not abs(a-b)+.01<d<a+b-.01:raise ValueError(f'{name}: unreachable {d:.3f}/{a+b:.3f}')
 unit=v/d;along=(a*a-b*b+d*d)/(2*d);joint=root+unit*along+pole*np.array([-unit[1],unit[0]])*math.sqrt(max(0,a*a-along*along))
 return np.array([root,joint,target])
def transformed(im,center,pivot,scale=1.,angle=0):
 pivot=np.asarray(pivot)
 if scale!=1:im=im.resize((max(1,round(im.width*scale)),max(1,round(im.height*scale))),Image.Resampling.LANCZOS);pivot=pivot*scale
 mid=np.array(im.size)/2;rr=im.rotate(-angle,resample=Image.Resampling.BICUBIC,expand=True)
 pos=np.asarray(center)+rotate(mid-pivot,angle)-np.array(rr.size)/2
 return rr,ip(pos)
@lru_cache(maxsize=40)
def sprite(who,view,part,expression='normal'):
 v=PACKS[who]['views'][view];a=v['sprites'][part]
 if who=='hero' and part=='head' and expression=='worried':a=PACKS[who]['views']['front']['sprites']['heads']['worried']
 if who=='hero' and part=='head' and expression=='relieved':a={**PACKS[who]['views']['front']['sprites']['head'],'path':'front/head-relieved.png'}
 im=Image.open(PATHS[who]/a['path']).convert('RGBA');m=np.array(a['image_to_local']);scale=m[0,0]*S
 im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS);off=np.array([m[0,2],m[1,2]+92])*S
 return im,off
def paint_part(im,who,view,part,hip,angle,expression='normal'):
 spr,off=sprite(who,view,part,expression);rr,pos=transformed(spr,hip,-off,angle=angle);im.alpha_composite(rr,pos)
def gait(x,travel,side,direction=1):
 stride=125.;p=(abs(travel)/stride+(0 if side=='left' else .5))%1
 if p<.6:return np.array([x+direction*stride*(.3-p),FLOOR]),True
 u=(p-.6)/.4;dx=-stride*.3+stride*.6*ease(u)
 return np.array([x+direction*dx,FLOOR-22*math.sin(math.pi*u)]),False
def walking_hip_y(x,travel,direction=1,who='hero',view='front'):
 """Pendulum support: raise hips over stance instead of a constant crouch.

 The limiting leg stays just short of full extension; a swinging knee can
 flex naturally. This changes body support, never bone length or foot pins.
 """
 limits=[]
 for side,leg in PACKS[who]['views'][view]['legs'].items():
  foot,_=gait(x,travel,side,direction);dx=foot[0]-(x+leg['hip'][0]*S)
  reach=160*S-1.;assert abs(dx)<reach
  limits.append(foot[1]-math.sqrt(reach*reach-dx*dx))
 return max(limits)
def shadow(im,x):
 lay=Image.new('RGBA',(160,36));ImageDraw.Draw(lay).ellipse((15,9,145,24),fill=(25,30,30,62));lay=lay.filter(ImageFilter.GaussianBlur(6));im.alpha_composite(lay,(round(x-80),round(FLOOR-16)))

def limbline(g,points):
 # Stable actor-local pressure variation along the actual fixed control chain.
 # Geometry remains the drawn chain, rather than an unrelated hidden skeleton.
 points=[np.asarray(p,float) for p in points]
 # Supersample the actual painted contour. Tiny native-size line segments
 # produced visibly serrated edges in preview-v2 and were rejected.
 left=math.floor(min(p[0] for p in points))-10;top=math.floor(min(p[1] for p in points))-10
 width=math.ceil(max(p[0] for p in points))-left+11;height=math.ceil(max(p[1] for p in points))-top+11
 tile=Image.new('RGBA',(width*3,height*3));dg=ImageDraw.Draw(tile)
 def pp(p):return tuple(round(float(v)*3) for v in (np.asarray(p)-[left,top]))
 lengths=[np.linalg.norm(b-a) for a,b in zip(points,points[1:])];total=sum(lengths);done=0.
 for a,b,length in zip(points,points[1:],lengths):
  steps=max(1,round(length/3))
  for j in range(steps):
   q=(done+length*(j+.5)/steps)/max(total,1)
   width=round(7.5+1.3*math.sin(math.pi*q)+.5*math.sin(q*math.pi*3))
   dg.line([pp(mix(a,b,j/steps)),pp(mix(a,b,(j+1)/steps))],fill=INK,width=width*3)
  done+=length
 for p in points[1:-1]:
  x,y=pp(p);dg.ellipse((x-10.5,y-10.5,x+10.5,y+10.5),fill=INK)
 target=g._image;target.alpha_composite(tile.resize((tile.width//3,tile.height//3),Image.Resampling.LANCZOS),(left,top))

def actor(im,hip,view='front',angle=0,head_angle=0,expression='normal',feet=None,wrists=None,walk=None,who='hero',poles=None,prop_draw=None,held=None):
 hip=np.asarray(hip,float);torso=hip+[0,6];v=PACKS[who]['views'][view];wrists=wrists or {};poles=poles or {};arms={};legs={};plants={}
 def pt(p):return torso+rotate((np.asarray(p)+[0,92])*S,angle)
 for side,spec in v['legs'].items():
  root=hip+[spec['hip'][0]*S,0]
  if walk is not None:target,plant=gait(hip[0],walk[0],side,walk[1])
  else:target=np.asarray(feet[side] if feet is not None else [hip[0]+(-25 if side=='left' else 28),FLOOR]);plant=True
  legs[side]=ik(root,target,(80*S,80*S),1 if walk is not None and walk[1]<0 else -1,who+':leg:'+side);plants[side]=plant
 for side,spec in v['arms'].items():
  root=pt(spec['socket']);rest=pt([spec['socket'][0]+(-12 if side=='left' else 12),spec['socket'][1]+110])
  arms[side]=ik(root,wrists.get(side,rest),(64*S,62*S),poles.get(side,1 if side=='left' else -1),who+':arm:'+side)
 shadow(im,hip[0]);g=ImageDraw.Draw(im)
 for side,ch in legs.items():
  limbline(g,ch);toe=-1 if walk is not None and walk[1]<0 else 1;line(g,[ch[-1]+[-3*toe,0],ch[-1]+[13*toe,0]],width=7)
 for ch in arms.values():limbline(g,ch)
 paint_part(im,who,view,'body',torso,angle)
 for side,ch in arms.items():limbline(ImageDraw.Draw(im),[pt(v['arms'][side]['exit_center']),ch[1],ch[2]])
 if prop_draw is not None:prop_draw(im)
 g=ImageDraw.Draw(im)
 for side,ch in arms.items():
  limbline(g,[mix(ch[1],ch[2],.28),ch[2]]);x,y=ch[-1];g.ellipse((x-5,y-5,x+5,y+5),fill=INK)
 spr,off=sprite(who,view,'head',expression);neck_local=np.array([0.,-158.])*S;neck=torso+rotate(neck_local,angle)
 rr,pos=transformed(spr,neck,neck_local-off,angle=angle+head_angle);im.alpha_composite(rr,pos)
 # All checks use the geometry actually drawn above, rather than a shadow rig.
 errors=[]
 for side,ch in arms.items():errors.extend([abs(np.linalg.norm(ch[1]-ch[0])-64*S),abs(np.linalg.norm(ch[2]-ch[1])-62*S)])
 for side,ch in legs.items():errors.extend([abs(np.linalg.norm(ch[1]-ch[0])-80*S),abs(np.linalg.norm(ch[2]-ch[1])-80*S)])
 assert max(errors)<1e-8
 contact={}
 for name,info in (held or {}).items():
  target=np.asarray(info['point']);side=info['arm'];contact[name]=float(np.linalg.norm(arms[side][-1]-target));assert contact[name]<=info.get('tolerance',1e-6),(name,contact[name])
 return {'who':who,'hip':hip.tolist(),'view':view,'bone_error':float(max(errors)),'legs':{s:{'joints':ch.tolist(),'planted':plants[s]} for s,ch in legs.items()},'arms':{s:ch.tolist() for s,ch in arms.items()},'contacts':contact}
