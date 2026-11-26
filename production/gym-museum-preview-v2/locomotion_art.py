"""Side/three-quarter locomotion views, keeping the approved cast and palette.
Walk/run use heel-load/push-off, front-bending knees, shoulder/hip counter-motion,
FK arm pendulums and a head that follows the torso with restrained lag.
"""
import math
import artwork as A
import gait as G

def shoe(c,f,far=False):
 pts=[(-11,-2),(-4,-10),(13,-10),(25,-2),(24,5),(-10,5)]
 pts=[(f['ankle'][0]+G.rotate(p,f['angle'],f['direction'])[0],f['ankle'][1]+G.rotate(p,f['angle'],f['direction'])[1]) for p in pts]
 c.poly(pts,'#617184' if far else '#293c52',A.INK,2)
 heel=(f['ankle'][0]+G.rotate((-10,5),f['angle'],f['direction'])[0],f['ankle'][1]+G.rotate((-10,5),f['angle'],f['direction'])[1])
 toe=(f['ankle'][0]+G.rotate((24,5),f['angle'],f['direction'])[0],f['ankle'][1]+G.rotate((24,5),f['angle'],f['direction'])[1])
 c.line([heel,toe],'#a3adae',2)

def head(c,x,y,t,role,d,talk,mood,phase=0):
 skin='#e6bc94' if role=='MINA' else '#f5d3b2'
 def p(dx,dy):return(x+d*dx,y+dy)
 def poly(ps,fill,outline=A.INK,w=2):c.poly([p(*a) for a in ps],fill,outline,w)
 def ell(cx,cy,rx,ry,fill,outline=A.INK,w=2):
  xx,yy=p(cx,cy);c.ell((xx-rx,yy-ry,xx+rx,yy+ry),fill,outline,w)
 if role=='MINA':
  lag=8*math.sin(phase-.8);poly([(-25,-32),(-55,-9),(-65,38+lag),(-42,18),(-24,9)],'#263b4b')
 ell(1,-1,38,47,skin,w=3)
 # Nose gives a readable direction without changing the character's head shape.
 poly([(30,-3),(45,10),(31,15)],skin,w=2)
 if role=='VALE':
  poly([(-34,0),(-38,-37),(-18,-54),(13,-53),(34,-32),(30,-15),(13,-32),(-9,-27),(-20,-4)],'#d1d3cd')
 else:poly([(-36,0),(-36,-37),(-12,-51),(14,-48),(35,-30),(27,-9),(10,-27),(-5,-19)],'#263b4b')
 for ex,r in [(-3,7),(23,8)]:
  ell(ex,-1,r,10,'#fff8eb');ell(ex+2,0,2.4,5,A.INK,None)
  q=3 if mood in ['worried','surprised'] else -2;c.line([p(ex-8,-16-q),p(ex+8,-15+q)],w=2.4)
 if role=='VALE':
  for ex,r in [(-3,11),(23,12)]:ell(ex,-2,r,14,None,w=2)
  c.line([p(8,-3),p(12,-3)],w=2)
  poly([(-1,19),(9,13),(16,17),(24,15),(36,22),(22,25),(13,22),(4,26)],'#796151',None)
 mx,my=p(17,30)
 if talk:c.ell((mx-9,my-3,mx+9,my+4+9*float(talk)),'#683d42',w=2)
 elif mood in ['worried','surprised']:c.ell((mx-5,my,mx+5,my+8),'#70464a',w=2)
 else:c.arc((mx-9,my-6,mx+10,my+9),8,170,w=2)

def render(c,t,role,talk=False,mood='neutral',hand=None,left=None):
 state=G.pose(t,role);hx,hy=state['hip'];d=state['direction'];phase=state['arm_phase'];run=state['run'];lean=math.radians(state['lean']);ground=state['ground']
 chest=(hx+d*108*math.sin(lean),hy-108*math.cos(lean))
 # Upper torso counters the pelvis slightly; head stabilization is less than pelvis bob.
 chest=(chest[0]-d*1.8*math.sin(phase),chest[1]+1.1*math.cos(phase))
 shoulders=[(chest[0]-d*9,chest[1]+16-1.4*math.sin(phase)),(chest[0]+d*16,chest[1]+16+1.4*math.sin(phase))]
 joints=[]
 for i,f in enumerate(state['feet']):
  root=(hx+(-3 if i==0 else 3),hy+(-1.5 if i==0 else 1.5));chain=A.ik(root,f['ankle'],68,68,-d);joints.append(chain)
 c.shadow(hx,ground+6,49)
 # Far leg first, then near leg. Both knees bend in the travel direction, not outward.
 for i,chain in enumerate(joints):
  col='#607184' if i==0 else '#293e55';w=12 if i==0 else 15
  c.line(chain,col,w);kx,ky=chain[1];c.ell((kx-w/2,ky-w/2,kx+w/2,ky+w/2),col,None);shoe(c,state['feet'][i],i==0)
 arm_paths=[]
 for i,shoulder in enumerate(shoulders):
  sign=-1 if i==0 else 1
  amp=34 if run else 17
  theta=d*math.radians(amp*math.sin(phase+sign*.30)*sign)
  elbow_flex=78 if run else 24
  lower_theta=theta+d*math.radians(elbow_flex+4*math.sin(phase-.4))
  elbow=(shoulder[0]+72*math.sin(theta),shoulder[1]+72*math.cos(theta));wrist=(elbow[0]+68*math.sin(lower_theta),elbow[1]+68*math.cos(lower_theta))
  target=left if i==0 else hand
  if target is not None:chain=A.ik(shoulder,target,72,68,-d)
  else:chain=[shoulder,elbow,wrist]
  arm_paths.append(chain)
 def arm(i):
  chain=arm_paths[i];skin='#d8b294' if i==0 else '#f2cda7';c.line(chain,A.INK,13 if i==0 else 15);c.line(chain,skin,8 if i==0 else 10)
  ex,ey=chain[1];c.ell((ex-4,ey-4,ex+4,ey+4),skin,None)
  x,y=chain[-1];c.ell((x-7,y-7,x+8,y+7),skin,w=2)
 arm(0)
 col='#3c727f' if role=='VALE' else '#d67c47'
 # Sloping shoulders and a moving hip line avoid the old upright rectangle silhouette.
 c.poly([(chest[0]-26,chest[1]),(chest[0]+28,chest[1]+2),(hx+25,hy+7),(hx-23,hy+4)],col,w=3)
 if role=='VALE':
  c.poly([(chest[0]-10,chest[1]+2),(chest[0]+3,chest[1]+38),(chest[0]+17,chest[1]+3),(hx+15,hy+2),(hx-9,hy+2)],'#ddbe7c',w=2)
  for u in [.52,.70,.86]:
   x=G.mix(chest[0]+3,hx+3,u);y=G.mix(chest[1],hy,u);c.ell((x-2,y-2,x+2,y+2),A.INK,None)
  tie=2*math.sin(phase-.8);c.poly([(chest[0]-4,chest[1]+2),(chest[0]+8,chest[1]+2),(chest[0]+4+tie,chest[1]+23)],'#965055',None)
 else:
  c.line([(chest[0]-17,chest[1]+4),(hx+17,hy-1)],'#f3dfaa',7);c.rect((hx-17,hy-28,hx-3,hy-8),'#ab5734',r=2,w=2)
 neckx=chest[0]+d*2;c.poly([(neckx-8,chest[1]-19),(neckx+9,chest[1]-19),(chest[0]+10,chest[1]+4),(chest[0]-8,chest[1]+2)],'#eac39f',w=2)
 arm(1)
 # A small counter-lag keeps the head from following each knee compression rigidly.
 headx=chest[0]+d*(3-1.5*math.sin(phase-.45));heady=chest[1]-61-1.7*math.cos(phase-.4)
 head(c,headx,heady,t,role,d,talk,mood,phase)
 return dict(state,clip=(G.mix(chest[0],hx,.28)+d*9,G.mix(chest[1],hy,.28)),hands=[a[-1] for a in arm_paths],arms=arm_paths,legs=joints,head=(headx,heady))
