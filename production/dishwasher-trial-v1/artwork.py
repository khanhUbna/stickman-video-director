"""Original editable 2D artwork. Native1080 rasterized from design-space geometry."""
from PIL import Image,ImageDraw,ImageFont
from functools import lru_cache
import math,numpy as np
W,H=1920,1080;S=1.5;INK='#263c46';PAPER='#faf2df';TEAL='#548d89';BLUE='#527eab';GOLD='#dfaa55'
CAM=(1.,0.,0.)
FONT='/workspace/stickman-video-director/skills/directing-stickman-videos/assets/fonts/NotoSans.ttf'
@lru_cache(None)
def font(n,scale=1.5):return ImageFont.truetype(FONT,round(n*scale))
def ease(x):x=max(0,min(1,x));return x*x*(3-2*x)
def mix(a,b,u):return a+(b-a)*u
def pt(p):
 z,ox,oy=CAM
 return tuple(round((v-([ox,oy][i%2]))*S) for i,v in enumerate(p))
class Canvas:
 def __init__(self,im=None):self.im=im if im is not None else Image.new('RGB',(W,H),PAPER);self.d=ImageDraw.Draw(self.im)
 def line(self,p,fill=INK,w=3):self.d.line([pt(x) for x in p],fill=fill,width=max(1,round(w*S)),joint='curve')
 def rect(self,b,fill,outline=INK,w=3,r=0):self.d.rounded_rectangle(pt(b),round(r*S),fill=fill,outline=outline,width=round(w*S))
 def ellipse(self,b,fill,outline=INK,w=3):self.d.ellipse(pt(b),fill=fill,outline=outline,width=round(w*S))
 def poly(self,p,fill,outline=INK,w=3):self.d.polygon([pt(x) for x in p],fill=fill);self.line(p+[p[0]],outline,w) if outline else None
 def text(self,p,t,n=24,fill=INK,anchor=None):self.d.text(pt(p),t,font=font(n,S),fill=fill,anchor=anchor)
 def arc(self,b,a,z,fill=INK,w=3):self.d.arc(pt(b),a,z,fill=fill,width=round(w*S))
 def shadow(self,x,y,rx=60,ry=9):self.ellipse((x-rx,y-ry,x+rx,y+ry),'#cbbda5',None)
def ik(a,b,l1,l2,side):
 a=np.array(a,float);b=np.array(b,float);v=b-a;d=float(np.linalg.norm(v));assert abs(l1-l2)+.01<d<l1+l2-.01,(a,b,d)
 u=v/d;h=(l1*l1-l2*l2+d*d)/(2*d);q=math.sqrt(max(0,l1*l1-h*h));e=a+u*h+np.array([-u[1],u[0]])*q*side
 return [tuple(a),tuple(e),tuple(b)]
def face(c,x,y,r,talk=0,mood='neutral',skin='#f5d5ad',hair=True,judge=False,gaze=0):
 c.ellipse((x-r,y-r*1.06,x+r,y+r),skin,w=3)
 if hair:
  c.poly([(x-r*.96,y-r*.2),(x-r*.87,y-r*.88),(x-r*.35,y-r*1.13),(x+r*.4,y-r*1.05),(x+r*.91,y-r*.6),(x+r*.91,y-r*.15),(x+r*.55,y-r*.67),(x-r*.2,y-r*.62),(x-r*.65,y-r*.25)],'#6e493a')
 ey=y-r*.05;dx=r*.36
 for k in [-1,1]:
  xx=x+k*dx;c.ellipse((xx-r*.105+gaze,ey-r*.12,xx+r*.105+gaze,ey+r*.12),INK,None)
  tilt= -.09*r*k if mood in ['angry','confident'] else .08*r*k if mood in ['worried','surprised'] else 0
  c.line([(xx-r*.19,ey-r*.28-tilt),(xx+r*.19,ey-r*.28+tilt)],w=3)
 if judge:
  for k in [-1,1]:c.ellipse((x+k*dx-r*.28,ey-r*.25,x+k*dx+r*.28,ey+r*.25),None,w=2)
  c.line([(x-r*.08,ey),(x+r*.08,ey)],w=2)
 if talk>.15:c.ellipse((x-r*.25,y+r*.28,x+r*.25,y+r*(.37+.21*talk)),'#6e3935',w=2)
 elif mood in ['happy','confident']:c.arc((x-r*.27,y+r*.12,x+r*.27,y+r*.56),5,175,w=3)
 elif mood=='worried':c.arc((x-r*.25,y+r*.35,x+r*.25,y+r*.67),190,350,w=3)
 else:c.line([(x-r*.2,y+r*.42),(x+r*.2,y+r*.42)],w=3)
def bowl(c,x,y,scale=1,dirty=True,tilt=0):
 w=58*scale;h=27*scale
 if tilt:
  c.poly([(x-w*.37,y),(x+w*.37,y),(x+w/2,y+h),(x-w/2,y+h)],'#f8eedc',w=3)
  yy=y+h;c.ellipse((x-w/2,yy-8*scale,x+w/2,yy+8*scale),'#faf8ee',w=3)
 else:
  c.poly([(x-w/2,y),(x-w*.37,y+h),(x+w*.37,y+h),(x+w/2,y)],'#f8eedc',w=3)
  yy=y;c.ellipse((x-w/2,yy-8*scale,x+w/2,yy+8*scale),'#faf8ee',w=3)
 if dirty:
  for dx,dy in [(-12,-1),(3,2),(17,-1)]:c.ellipse((x+(dx-4)*scale,yy+(dy-2)*scale,x+(dx+4)*scale,yy+(dy+2)*scale),'#ac5d3b',None)

def person(c,x=310,hip=537,t=0,pose='stand',talk=False,prop=None,hand=None,judge=False,walk=0,mood='neutral',left_hand=None,beat=0):
 """Fixed-length chains. Held bowl is anchored to actual hand endpoint."""
 skin='#bd896d' if judge else '#f5d5ad';shirt='#795773' if judge else BLUE
 # planted legs for bends; walking step interpolates foot placement, separately traced
 feet=[(x-22,635),(x+24,635)]
 if walk:
  phase=t*5.5;feet=[(x-25+22*math.sin(phase),635-11*max(0,math.cos(phase))),(x+25-22*math.sin(phase),635-11*max(0,-math.cos(phase)))]
 c.shadow(x,640,55)
 for k,f in zip([-1,1],feet):
  joints=ik((x+k*14,hip),f,51,51,-k);c.line(joints,'#344b5b',15);c.line([(f[0]-7,f[1]),(f[0]+15,f[1])],INK,9)
 chest=hip-104;head=(x,hip-161)
 c.poly([(x-37,chest),(x+37,chest),(x+36,hip+5),(x-36,hip+5)],shirt,w=3)
 c.line([(x-24,chest+6),(x+24,chest+6)],'#9bb9ca',3)
 c.rect((x-12,chest-18,x+12,chest+3),skin,w=2,r=4)
 face(c,*head,39,talk=(.3+.7*abs(math.sin(t*14))) if talk else 0,mood=mood,skin=skin,judge=judge)
 shoulders=[(x-35,chest+17),(x+35,chest+17)];hands=[(x-48,chest+100),(x+47,chest+99)]
 if pose=='point':hands[1]=(x+121,chest+1)
 if pose in ['hold','offer']:hands[1]=(x+100,chest+55);hands[0]=(x+15,chest+65)
 if pose=='shrug':hands=[(x-100,chest+18),(x+102,chest+15)]
 if pose=='inspect':hands[1]=(x+112,chest+68)
 if hand: hands[1]=tuple(hand)
 if left_hand:hands[0]=tuple(left_hand)
 elif pose=='hold' and talk:
  u=ease(min(1,beat/.4));hands[0]=(mix(x+15,x-94,u),mix(chest+65,chest+21,u))
 rows=[]
 for k,a,b in zip([-1,1],shoulders,hands):
  chain=ik(a,b,66,66,-k);c.line(chain,INK,15);c.line(chain,skin,10);c.ellipse((b[0]-7,b[1]-7,b[0]+7,b[1]+7),skin,w=2);rows.append(chain)
 if prop=='bowl':
  bowl(c,hands[1][0]-29,hands[1][1]-15,1,dirty=mood!='happy');b=hands[1];c.ellipse((b[0]-6,b[1]-6,b[0]+6,b[1]+6),skin,w=2)
 return {'hands':hands,'arms':rows,'feet':feet}
def dishwasher(c,x=790,y=300,w=250,h=327,t=0,open=0,talk=False,mood='neutral',gesture=False):
 c.shadow(x+w/2,y+h+10,w*.6)
 c.rect((x,y,x+w,y+h),'#bed0c9',r=11);c.rect((x+12,y+57,x+w-12,y+h-15),'#dbe1d4',r=4)
 c.rect((x+8,y+8,x+w-8,y+59),TEAL,r=5)
 for i in range(4):c.ellipse((x+18+i*12,y+24,x+23+i*12,y+29),'#e8e8c5',None)
 # eyes in upper panel
 for k in [-1,1]:
  xx=x+w*.5+k*21;c.ellipse((xx-7,y+19,xx+7,y+36),'#f9f4de',None);c.ellipse((xx-2,y+23,xx+3,y+33),INK,None)
  c.line([(xx-10,y+13+(3*k if mood=='worried' else -3*k)),(xx+9,y+13-(3*k if mood=='worried' else -3*k))],w=3)
 if talk:c.ellipse((x+w/2-13,y+38,x+w/2+13,y+43+8*abs(math.sin(t*14))),'#654b43',w=2)
 else:c.arc((x+w/2-14,y+29,x+w/2+14,y+49),10,170,w=2)
 if open:
  c.rect((x+16,y+70,x+w-16,y+h-20),'#526c70',r=3)
  # open door is a horizontal supported flap
  c.poly([(x+8,y+h-18),(x+w-8,y+h-18),(x+w+34,y+h+12),(x-34,y+h+12)],'#c6d5ce',w=3)
  rack(c,x+23,y+h-115+open*28,w-46,75)
 else:
  c.rect((x+37,y+77,x+w-37,y+89),'#91a9a1',w=2,r=5)
  c.line([(x+30,y+h-42),(x+w-30,y+h-42)],'#a8bab1',3)
 if gesture:
  a=(x+w-2,y+95);b=(x+w+49,y+56+6*math.sin(t*2));c.line([a,(x+w+30,y+105),b],INK,6);c.ellipse((b[0]-7,b[1]-7,b[0]+7,b[1]+7),'#f5d5ad',w=2)
def rack(c,x,y,w=200,h=70):
 c.poly([(x,y),(x+w,y),(x+w+15,y+h),(x-15,y+h)],'#afbbb4',w=3)
 for i in range(1,9):
  u=i/9;c.line([(x+w*u,y),(x-15+(w+30)*u,y+h)],'#627d7d',2)
 for u in [.25,.5,.75]:c.line([(x-15*u,y+h*u),(x+w+15*u,y+h*u)],'#627d7d',2)
def room(kind='court'):
 c=Canvas();c.rect((0,0,1280,720),PAPER,None,0)
 c.rect((0,0,1280,420),'#f3e4ca',None,0)
 for x in range(0,1280,128):c.line([(x,140),(x,420)],'#e6d3b8',1)
 for y in [140,210,280,350,420]:c.line([(0,y),(1280,y)],'#e6d3b8',1)
 c.rect((0,630,1280,720),'#dbc6a5',None,0);c.line([(0,630),(1280,630)],'#947f68',3)
 for x in range(-300,1300,160):c.line([(x,720),(x+100,630)],'#cbb18c',2)
 # window with outdoor light
 c.rect((60,80,320,300),'#84b4b7',r=5);c.rect((73,93,307,286),'#c9dddd',w=2);c.line([(190,93),(190,286)],'#f7f1df',8);c.line([(73,185),(307,185)],'#f7f1df',8)
 for x in [90,130,230,270]:c.ellipse((x,213,x+45,269),'#8da485',None)
 # counter run, sink
 c.rect((10,405,600,625),'#b4c5b6',r=4);c.rect((0,394,610,420),'#dcc5a4',r=5)
 for x in [30,220,410]:c.rect((x,436,x+169,604),'#c2cfbf',w=2,r=5);c.line([(x+50,452),(x+115,452)],'#6b8580',4)
 if kind!='court':
  c.ellipse((310,391,500,416),'#6f9290',w=3);c.arc((391,337,456,402),185,355,w=6);c.line([(453,367),(453,392)],w=6)
 c.rect((1015,90,1210,295),'#b4c5b6',r=7);c.line([(1112,95),(1112,290)],'#77918c',2)
 # pendant lamp
 c.line([(910,0),(910,80)],w=3);c.poly([(876,82),(944,82),(964,120),(856,120)],GOLD,w=3)
 if kind=='court':
  c.rect((465,65,890,125),'#ead39a',r=7);c.text((677,95),'HOUSEHOLD COURT',25,anchor='mm')
 return c.im
@lru_cache(None)
def background(kind,z=1,ox=0,oy=0):return room(kind)
def gavel(c,x,y,rot=0):
 c.line([(x-10,y+25),(x+21,y-11)],'#8a5a42',8);c.rect((x+4,y-28,x+43,y-7),'#b17c52',r=3)
def judge(c,t,talk=False,hit=False,beat=0):
 gy=450+17*ease(min(1,beat/.28)) if hit else 467
 hand=(997,gy+25)
 row=person(c,1090,537,t,judge=True,talk=talk,mood='neutral',left_hand=hand)
 c.rect((988,474,1244,630),'#ac8260',r=5);c.rect((972,460,1253,481),'#d1a572',r=4)
 c.rect((1032,506,1202,545),PAPER,w=2,r=3);c.text((1117,525),'THE JUDGE',20,anchor='mm')
 chain=row['arms'][0];c.line(chain,INK,15);c.line(chain,'#bd896d',10)
 gavel(c,1007,gy);c.ellipse((hand[0]-7,hand[1]-7,hand[0]+7,hand[1]+7),'#bd896d',w=2)

def stamp(c,text,color='#a86043'):
 c.rect((500,161,829,222),PAPER,color,4,r=6);c.text((665,191),text,25,color,anchor='mm')
def scene_frame(mode,t=0,u=0,speaker='NARRATOR',clean=False,camera=(1.,0.,0.),pose=None,beat=0,phase=6):
 global CAM,S
 CAM=camera;S=1.5*camera[0]
 c=Canvas(background('court' if mode in ['court','judge','bowl','verdict'] else 'kitchen',*camera).copy());talk=speaker
 if mode in ['court','judge','bowl','verdict']:
  # dishwasher at center, owner in foreground, bench right
  dishwasher(c,625,295,252,330,t,open=.6 if mode=='verdict' else 0,talk=talk=='DISHWASHER',gesture=talk=='DISHWASHER')
  person(c,405,537,t,pose=pose or 'hold',talk=talk=='SAM',prop='bowl',mood='happy' if clean else 'worried',beat=beat)
  judge(c,t,talk=='JUDGE',hit=mode=='judge',beat=beat)
  if mode=='bowl':
   c.rect((60,65,360,290),'#faf7e9',r=8);c.text((210,94),'EXHIBIT A',23,anchor='mm');bowl(c,210,178,3.6,not clean)
  if mode=='verdict' and clean:stamp(c,'CASE DISMISSED',TEAL)
 elif mode=='sink':
  # owner stands near sink, bowl follows contacting hands
  person(c,275,537,t,pose='hold',hand=(373+6*math.sin(t*4),497+3*math.cos(t*4)),talk=talk=='SAM',prop='bowl',mood='neutral')
  c.rect((300,508,555,626),'#b4c5b6',None,0);c.ellipse((318,506,510,530),'#6f9290',w=3)
  c.line([(453,390),(453+2*math.sin(t*15),516)],'#86b9bf',8)
  for j in range(4):c.ellipse((450+j*6,520+4*math.sin(t*9+j),455+j*6,525+4*math.sin(t*9+j)),'#a3cbcc',None)
  dishwasher(c,735,298,255,330,t,talk=talk=='DISHWASHER',gesture=True)
 elif mode in ['rack','nest']:
  dishwasher(c,735,255,300,367,t,open=1,talk=talk=='DISHWASHER')
  # isolated enlarged loading view, actual separation happens as hands lift inner bowl
  c.rect((70,80,675,394),'#e5e8d7',r=12);c.text((370,115),'LET THE WATER REACH',25,anchor='mm')
  rack(c,160,229,410,115)
  lift=100*ease((u-.15)/.55) if mode!='load' else 100
  bowl(c,330,251,2.2,False,tilt=1);bowl(c,330,238-lift,1.95,True,tilt=1)
  c.line([(562,168),(457,168),(374,240-lift)],INK,10);c.ellipse((364,231-lift,383,250-lift),'#f5d5ad',w=2)
  if lift>60:
   for j in range(4):
    yy=321-j*12;c.line([(198,yy),(286,232+j*3)],'#83b9bf',3)
  person(c,500,537,t,pose='point',talk=talk=='SAM',mood='neutral')
 elif mode in ['load','arrange']:
  dishwasher(c,735,255,300,367,t,open=1,talk=talk=='DISHWASHER')
  pull=ease(min(1,u*2.5));rx=758-108*pull
  # Owner grips the front-left rack, then visibly separates a bowl on the rack.
  hip=537+8*math.sin(pull*math.pi)
  if mode=='load':hand=(rx,525)
  else:
   rx=650;v=ease(max(0,min(1,(u-.1)/.75)));bx=695+65*v;by=492-55*math.sin(v*math.pi);hand=(bx+29,by+15)
  row=person(c,680,hip,t,hand=hand,mood='neutral',talk=talk=='SAM')
  rack(c,rx,510,254,80)
  bowl(c,rx+45,493,1,True,tilt=1)
  if mode=='load':bowl(c,rx+45,483,1,True,tilt=1)
  else:bowl(c,bx,by,1,True,tilt=1)
  hx,hy=hand;c.ellipse((hx-7,hy-7,hx+7,hy+7),'#f5d5ad',w=2)
  c.text((460,155),'MAKE ROOM FOR WATER',24,anchor='mm')
 elif mode=='arm':
  c.rect((112,73,1145,593),'#5e7c7c',r=20);c.text((630,110),'WITH THE MACHINE OFF',24,'#f9f1d9',anchor='mm')
  c.ellipse((345,150,902,577),'#acbcb0',w=4)
  spin=(.55+(u-.73)*15) if u>.73 else min(u*3,.55)
  cx,cy=622,367;dx=200*math.cos(spin);dy=140*math.sin(spin)
  c.line([(cx-dx,cy-dy),(cx+dx,cy+dy)],'#dfbd79',32);c.ellipse((cx-25,cy-25,cx+25,cy+25),TEAL,w=4)
  for side in [-1,1]:
   for q in [.3,.6,.85]:c.ellipse((cx+side*dx*q-5,cy+side*dy*q-5,cx+side*dx*q+5,cy+side*dy*q+5),'#647b79',None)
  ux=781+330*ease((u-.38)/.37)
  c.line([(ux,155),(ux,453)],'#ba8971',17);c.rect((ux-27,431,ux+26,488),'#ccb6a0',r=7)
  c.line([(1180,200),(ux+60,185),(ux+4,180)],INK,12);c.ellipse((ux-7,170,ux+14,192),'#f5d5ad',w=2)
  c.text((946,516),'CLEAR' if u>.73 else 'BLOCKED',25,'#f3dcc0',anchor='mm')
 elif mode=='filter':
  c.rect((78,75,1195,605),'#e2ddc9',r=14);c.text((636,115),'INSPECT THE FILTER',27,anchor='mm')
  lift=75*ease(u/.45);x,y=608,330-lift
  c.ellipse((421,417,811,535),'#8b9b90',w=4)
  c.rect((x-84,y,x+84,y+166),'#d1d5c1',r=15)
  for a in range(-65,70,13):c.line([(x+a,y+10),(x+a,y+145)],'#899e90',2)
  for a in range(20,150,15):c.line([(x-75,y+a),(x+75,y+a)],'#899e90',2)
  c.ellipse((x-97,y-20,x+97,y+22),'#b9c8b7',w=4)
  for a,b in [(-30,40),(22,91),(-17,124),(45,58)]:
   if not clean or u<.7:c.ellipse((x+a-12,y+b-7,x+a+12,y+b+7),'#b46b43',None)
  if clean:
   # Serviceable filter removed for cleaning, water and brush visibly meet mesh.
   c.line([(388,155),(492,155),(492,y+40)],'#719ca2',12)
   for j in range(4):c.line([(492+j*7,y+35),(535+j*7,y+105+5*math.sin(t*9+j))],'#80b7c2',4)
   by=y+72+20*math.sin(t*5);c.line([(389,by),(518,by)],'#a77c54',14)
   for j in range(5):c.line([(516,by-14+j*7),(538,by-14+j*7)],'#6c7971',3)

  c.line([(953,187),(842,182),(x+52,y-6)],INK,13);c.ellipse((x+33,y-16,x+65,y+7),'#f5d5ad',w=3)
 elif mode in ['water','wash']:
  c.rect((115,72,1148,598),'#e2e9df',r=18);c.text((632,109),'FOLLOW THE WATER',27,anchor='mm')
  c.rect((325,161,938,553),'#c7d5ca',w=5,r=8)
  rack(c,370,247,510,49);rack(c,370,382,510,49)
  for x in [440,578,717,825]:bowl(c,x,248,1,False,tilt=1);bowl(c,x-10,385,1,False,tilt=1)
  depth=33*ease(beat/2.8) if phase==0 else 6 if phase==5 else 33
  c.rect((345,537-depth,919,537),'#a3ccd0' if phase==6 else '#85b6bd',None,0)
  if phase>=1:
   c.ellipse((222,440,314,532),TEAL,w=3);c.text((268,485),'PUMP',14,'#fff2d8',anchor='mm')
   c.line([(360,518),(315,518),(315,484)],'#5e9fa9',8);c.line([(270,439),(270,337),(410,337)],'#5e9fa9',8)
  for yy in [328,454]:
   shift=20*math.sin(t*2);c.line([(408+shift,yy),(858-shift,yy)],GOLD,12)
   if phase>=2 and phase not in [5,7]:
    for j in range(7):
     x=435+j*62+shift;end=(x+22*math.sin(t*3+j),yy-69);c.line([(x,yy),end],'#62a7b4',3)
     q=(t*2+j*.17)%1;c.ellipse((mix(x,end[0],q)-3,mix(yy,end[1],q)-3,mix(x,end[0],q)+3,mix(yy,end[1],q)+3),'#2e8b9c',None)
  if phase>=3:
   c.rect((330,490,390,541),'#b8ccb7',w=2,r=3)
   for j in range(5):c.line([(338+j*10,495),(338+j*10,536)],'#77998a',1)
   c.text((360,474),'FILTER',12,anchor='mm')
  if phase==4:
   c.rect((989,187,1093,245),'#dfbf79',r=6);c.text((1041,214),'DETERGENT',13,anchor='mm')
   for j in range(7):
    xx=510+j*48;yy=518-5*math.sin(t*3+j);c.ellipse((xx,yy,xx+7,yy+7),'#f6f1da',None)
  if phase==5:
   c.line([(919,526),(1034,526),(1034,557)],'#6a9eaa',8);c.text((1033,579),'DRAIN',15,anchor='mm')
   for j in range(5):xx=930+(t*60+j*20)%90;c.ellipse((xx,522,xx+5,529),'#2e8b9c',None)
  if phase==7:
   c.rect((471,174,806,219),'#fcf4e0',r=5);c.text((638,196),'NOT A FULL TUB',22,anchor='mm')
  c.text((627,572),'FILL  /  WASH  /  DRAIN  /  RINSE',20,anchor='mm')
 elif mode=='manual':
  person(c,360,537,t,pose='point',talk=talk=='SAM',mood='surprised');dishwasher(c,830,299,250,328,t,talk=talk=='DISHWASHER')
  c.rect((520,180,785,453),'#fffae9',r=5);c.rect((530,191,775,229),TEAL,None,0);c.text((650,210),'OWNER MANUAL',20,'#fffae9',anchor='mm')
  for j,txt in enumerate(['SCRAPE SCRAPS','SPACE BOWLS','CLEAR SPRAY ARMS','FILTER CARE']):c.text((549,270+j*40),txt,18)
 elif mode=='care':
  c.rect((120,110,1160,580),'#e4dfc9',r=12);c.text((640,145),'A FAIR TEST',27,anchor='mm')
  # visible three stage transformations rather than a static list
  for j,title in enumerate(['SCRAPE','SPACE','CHECK']):
   x=302+j*330;c.ellipse((x-110,250,x+110,470),'#f7f1df',w=3);c.text((x,505),title,24,anchor='mm')
   if j==0:
    bowl(c,x,325,2,True);c.line([(x+120,255),(x+22+12*math.sin(t*6),323)],'#a57751',12)
   elif j==1:
    bowl(c,x-35,345,1.35,False,tilt=1);bowl(c,x+30,320-10*math.sin(t*2),1.3,False,tilt=1)
   else:
    ang=t*2;c.line([(x-65*math.cos(ang),360-50*math.sin(ang)),(x+65*math.cos(ang),360+50*math.sin(ang))],GOLD,16);c.ellipse((x-12,348,x+12,372),TEAL,w=3)
 return c.im
