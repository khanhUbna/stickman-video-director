"""Original 2D cast/sets. Jointed body animation at native 1920x1080."""
from PIL import Image, ImageDraw, ImageFont
from functools import lru_cache
import math
from pathlib import Path
W,H=1920,1080
INK='#26374b'; PAPER='#f8f2df'; TEAL='#377f88'; GOLD='#e4ab52'; ORANGE='#d87742'
FONT=str(Path(__file__).resolve().parents[2]/'skills/directing-stickman-videos/assets/fonts/NotoSans.ttf')
def smooth(u):u=max(0,min(1,u));return u*u*(3-2*u)
def lerp(a,b,u):return a+(b-a)*u
@lru_cache(None)
def font(size):return ImageFont.truetype(FONT,max(1,round(size)))
class C:
 def __init__(self,camera=(1,0,0)):
  self.im=Image.new('RGB',(W,H),PAPER);self.d=ImageDraw.Draw(self.im);self.z,self.ox,self.oy=camera;self.s=1.5*self.z
 def p(self,xy):return tuple(round((v-(self.ox if i%2==0 else self.oy))*self.s) for i,v in enumerate(xy))
 def line(self,ps,color=INK,w=3):self.d.line([self.p(p) for p in ps],fill=color,width=max(1,round(w*self.s)),joint='curve')
 def rect(self,b,fill,outline=INK,r=0,w=3):self.d.rounded_rectangle(self.p(b),round(r*self.s),fill,outline,max(1,round(w*self.s)))
 def ell(self,b,fill,outline=INK,w=3):self.d.ellipse(self.p(b),fill,outline,max(1,round(w*self.s)))
 def poly(self,ps,fill,outline=INK,w=3):
  self.d.polygon([self.p(p) for p in ps],fill)
  if outline:self.line(ps+[ps[0]],outline,w)
 def text(self,x,y,t,size=24,color=INK,anchor=None):self.d.text(self.p((x,y)),t,font=font(size*self.s),fill=color,anchor=anchor)
 def arc(self,b,a,e,color=INK,w=3):self.d.arc(self.p(b),a,e,fill=color,width=max(1,round(w*self.s)))
 def shadow(self,x,y,w=60):self.ell((x-w,y-7,x+w,y+7),'#b2a692',None)
def ik(a,b,l=72,m=68,side=1):
 dx=b[0]-a[0];dy=b[1]-a[1];d=math.hypot(dx,dy)
 if not abs(l-m)+.001<d<l+m-.001:raise ValueError(('unreachable IK',a,b,d,l,m))
 h=(l*l-m*m+d*d)/(2*d);q=math.sqrt(max(0,l*l-h*h));ux,uy=dx/d,dy/d
 e=(a[0]+ux*h-uy*q*side,a[1]+uy*h+ux*q*side)
 return [a,e,b]
def limb(c,points,skin=True,width=12):
 c.line(points,INK,width+4)
 if skin:c.line(points,'#f2cda7',width-2)
def weight(c,x,y,w=155):
 c.line([(x-w*.65,y),(x+w*.65,y)],'#8d9aa7',9)
 for k in [-1,1]:
  xx=x+k*w*.5;c.rect((xx-12,y-37,xx+12,y+37),'#465872',r=6);c.rect((xx-21,y-28,xx-12,y+28),'#62758b',r=3)
def face(c,x,y,t,role='VALE',talk=False,mood='neutral',gaze=0):
 skin='#e6bc94' if role in ['MINA','MEMBER','COACH'] else '#f5d3b2';r=43 if role=='MINA' else 46
 if role=='MINA':
  c.ell((x+24,y-18,x+70,y+38),'#263b4b');c.poly([(x+42,y+9),(x+77,y+54),(x+66,y+13)],'#263b4b')
 c.ell((x-r,y-r*1.13,x+r,y+r),skin)
 if role=='VALE':
  c.poly([(x-r,y-7),(x-r+4,y-43),(x-19,y-59),(x+20,y-56),(x+45,y-30),(x+44,y-3),(x+21,y-34),(x-15,y-34),(x-37,y-5)],'#d1d3cd')
 elif role=='MINA':c.poly([(x-r,y),(x-r,y-38),(x-19,y-54),(x+22,y-51),(x+44,y-24),(x+37,y+2),(x+21,y-29),(x-15,y-20)],'#263b4b')
 elif role=='CLERK':c.poly([(x-r,y-13),(x-39,y-44),(x+36,y-44),(x+45,y-10),(x+9,y-30)],'#684c46')
 else:c.poly([(x-r,y-9),(x-r+6,y-41),(x+13,y-51),(x+43,y-29),(x+40,y-4),(x+19,y-28)],'#624a40')
 for k in [-1,1]:
  ex=x+k*17;c.ell((ex-9,y-5,ex+9,y+10),'#fff8eb',w=2);c.ell((ex-3+gaze,y-2,ex+3+gaze,y+7),INK,None)
  brow=(6*k if mood in ['worried','surprised'] else -5*k if mood in ['confident','angry'] else 0)
  c.line([(ex-11,y-16-brow),(ex+10,y-16+brow)],w=3)
 if role=='VALE':
  for k in [-1,1]:c.ell((x+k*17-14,y-13,x+k*17+14,y+15),None,INK,w=2)
  c.line([(x-3,y),(x+3,y)],w=2);c.poly([(x-21,y+20),(x-7,y+13),(x,y+18),(x+7,y+13),(x+22,y+20),(x+8,y+25),(x,y+22),(x-8,y+25)],'#796151',None)
 if talk:
  h=4+12*min(1,float(talk));c.ell((x-12,y+26,x+12,y+26+h),'#683d42',w=2)
 elif mood in ['happy','confident']:c.arc((x-16,y+18,x+16,y+42),0,180,w=3)
 elif mood in ['worried','surprised']:c.ell((x-7,y+28,x+7,y+38),'#70464a',w=2)
 else:c.line([(x-12,y+32),(x+12,y+32)],w=3)
def person(c,x=400,ground=646,t=0,role='VALE',action='stand',talk=False,mood='neutral',u=0,hand=None,left=None,walk_speed=0,prop=None,scale=1,gaze=0,feet_override=None):
 # The body is not translated to fake a walk: stance feet stay fixed in world space.
 bob=0;hip_y=ground-132;feet=[(x-23,ground),(x+23,ground)]
 if action in ['walk','run','belt']:
  speed=walk_speed or (135 if action=='run' else 72);period=.62 if action=='run' else .90;v=speed;step=v*.6*period/2
  for i in range(2):
   q=(t/period+i*.5)%1
   if q<.6:dx=step-v*q*period;lift=0
   else:uu=(q-.6)/.4;dx=lerp(-step,step,smooth(uu));lift=math.sin(math.pi*uu)*(32 if action=='run' else 20)
   feet[i]=(x+dx+(i*2-1)*10,ground-lift)
  bob=1.5*math.sin(t/period*math.pi*4);hip_y=ground-130+bob
  span=max(abs(ft[0]-(x+(i*2-1)*15)) for i,ft in enumerate(feet));hip_y=max(hip_y,ground-math.sqrt(max(1,136**2-span**2))+2.5)
 if feet_override is not None:feet=feet_override
 if action in ['bend','lift']:
  bend=1-smooth(u) if action=='lift' else smooth(u);hip_y+=24*bend
 gesture=smooth(min(1,u/.22))*(1-smooth(max(0,(u-.72)/.28)))
 lean=((18 if walk_speed>=0 else -18) if action=='run' else 24*smooth(u) if action=='reach' else 9*gesture if action in ['point','shrug'] else 0)
 chest=(x+lean,hip_y-111);head=(chest[0],chest[1]-62)
 c.shadow(x,ground+6,52)
 for i,ft in enumerate(feet):
  chain=ik((x+(i*2-1)*15,hip_y),ft,68,68,1 if i==0 else -1);limb(c,chain,False,13);c.line([(ft[0]-9,ft[1]),(ft[0]+18,ft[1])],INK,10)
 color={'VALE':'#3c727f','MINA':'#d67c47','COACH':'#527c65','MEMBER':'#737fa6','CLERK':'#7d638b'}.get(role,TEAL)
 c.poly([(chest[0]-37,chest[1]),(chest[0]+37,chest[1]),(x+37,hip_y+5),(x-37,hip_y+5)],color)
 if role=='VALE':
  c.poly([(chest[0]-18,chest[1]+2),(chest[0],chest[1]+48),(chest[0]+19,chest[1]+2),(x+17,hip_y),(x-17,hip_y)],'#ddbe7c',w=2)
  c.poly([(chest[0]-9,chest[1]),(chest[0]+9,chest[1]),(chest[0],chest[1]+21)],'#965055',None)
  for yy in [60,78,95]:c.ell((chest[0]-2,chest[1]+yy,chest[0]+2,chest[1]+yy+4),INK,None)
 if role=='MINA':c.line([(chest[0]-26,chest[1]+3),(x+25,hip_y)],'#f3dfaa',9);c.rect((x-26,hip_y-28,x-8,hip_y-6),'#ab5734',r=3,w=2)
 c.rect((head[0]-10,chest[1]-21,head[0]+10,chest[1]+4),'#eac39f',r=5,w=2)
 shoulders=[(chest[0]-35,chest[1]+16),(chest[0]+35,chest[1]+16)];hands=[(x-53,hip_y+30),(x+53,hip_y+30)]
 if action in ['walk','run','belt']:
  sw=math.sin(t*(10 if action=='run' else 7))*25;hands=[(x-60,hip_y+4+sw),(x+60,hip_y+4-sw)]
 if action=='point':hands[1]=(lerp(x+53,chest[0]+151,gesture),lerp(hip_y+30,chest[1]+9,gesture))
 if action=='shrug':hands=[(lerp(x-53,chest[0]-105,gesture),lerp(hip_y+30,chest[1]-2,gesture)),(lerp(x+53,chest[0]+105,gesture),lerp(hip_y+30,chest[1]-2,gesture))]
 if action=='panic':hands=[(head[0]-67,head[1]+6),(head[0]+67,head[1]+6)]
 if action in ['read','hold']:hands=[(chest[0]-23,chest[1]+67),(chest[0]+78,chest[1]+53)]
 if action=='think':hands[1]=(head[0]+20,head[1]+39)
 if action=='reach':hands[1]=(lerp(x+53,x+145,smooth(u)),lerp(hip_y,chest[1]+60,smooth(u)))
 if action=='lift':hands=[(x-69,lerp(hip_y+6,chest[1]+61,smooth(u))),(x+69,lerp(hip_y+6,chest[1]+61,smooth(u)))]
 if hand:hands[1]=hand
 if left:hands[0]=left
 for i,(a,b) in enumerate(zip(shoulders,hands)):
  side=1 if i==0 else -1
  chain=ik(a,b,72,68,side);limb(c,chain,True,10);c.ell((b[0]-7,b[1]-7,b[0]+7,b[1]+7),'#edc49e',w=2)
 face(c,*head,t,role,talk,mood,gaze)
 if prop=='card':
  hx,hy=hands[1];c.rect((hx-86,hy-45,hx+1,hy+6),'#fff7df',r=5,w=2);c.text(hx-78,hy-38,'MEMBER',10);c.line([(hx-78,hy-19),(hx-13,hy-19)],'#c8945c',3)
 if prop=='tablet':
  hx,hy=hands[1];c.rect((hx-80,hy-48,hx+5,hy+7),INK,r=6,w=2);c.rect((hx-72,hy-40,hx-3,hy-1),'#80bfc2',r=3,w=1)
 if action=='lift':weight(c,(hands[0][0]+hands[1][0])/2,hands[0][1],138)
 return {'hands':hands,'feet':feet,'hip':(x,hip_y),'head':head}
def treadmill(c,x=675,y=640,t=0,on=False):
 c.poly([(x-180,y),(x+125,y),(x+160,y+32),(x-202,y+32)],'#607286');c.rect((x-162,y+2,x+105,y+17),'#303a49',r=4,w=2)
 if on:
  for k in range(10):
   xx=x-160+(k*34-t*72)%270;c.line([(xx,y+4),(xx+8,y+14)],'#9aa4ae',2)
 c.line([(x+115,y),(x+125,y-222),(x+58,y-222)],INK,13);c.line([(x-66,y-164),(x+121,y-166)],'#697c8b',10)
 c.rect((x+62,y-253,x+141,y-206),'#98c8c7',r=6);c.text(x+73,y-242,'START',13);c.rect((x+111,y-224,x+128,y-211),'#b85c57',r=3,w=1)
def bench(c,t=0,u=.5,talk=False):
 c.rect((460,568,850,594),'#b7a290',r=9);c.line([(500,594),(490,660)],w=10);c.line([(814,594),(830,660)],w=10)
 for xx in [580,845]:c.line([(xx,658),(xx,414),(xx+20,414)],'#7b8d9b',10)
 # Supine torso, grounded feet and elbow chains are authored for the bench view.
 c.line([(675,548),(782,562)],'#737fa6',51);face(c,618,548,t,'MEMBER',talk)
 for off in [-9,13]:limb(c,ik((780,560+off),(900+off,660),78,85,-1),False,12)
 by=lerp(496,427,smooth(u));weight(c,718,by,272)
 for sh,ha,side in [((668,535),(673,by),-1),((693,544),(761,by),1)]:limb(c,ik(sh,ha,72,68,side),True,10);c.ell((ha[0]-6,ha[1]-6,ha[0]+6,ha[1]+6),'#edc49e',w=2)
def robot(c,x=630,y=645,t=0,u=0):
 c.shadow(x,y+5,50);c.rect((x-37,y-220,x+37,y-145),'#b7cdd0',r=15);c.ell((x-22,y-199,x-9,y-186),TEAL,None);c.ell((x+9,y-199,x+22,y-186),TEAL,None)
 c.rect((x-45,y-142,x+45,y-68),'#839cae',r=12)
 for k in [-1,1]:c.line([(x+k*25,y-64),(x+k*30,y-8)],INK,14);c.line([(x+k*39,y),(x+k*8,y)],INK,12)
 hy=lerp(y-73,y-174,smooth(u));hx=x+105
 c.line([(x+43,y-128),(x+77,y-93),(hx,hy)],INK,13);weight(c,hx+19,hy,63)
 c.line([(x-44,y-124),(x-67,y-70)],INK,12)
def background(c,kind='dig',t=0,title=''):
 if kind in ['dig','archive','bench','locker']:
  c.rect((0,0,1280,720),'#e5c99d',None);c.rect((0,500,1280,720),'#c8a47b',None)
  c.poly([(0,0),(0,70),(140,42),(220,90),(380,34),(520,60),(680,15),(860,74),(1030,38),(1170,80),(1280,30),(1280,0)],'#806b60',None)
  for xx in [75,410,850,1210]:c.line([(xx,130),(xx,500)],'#ad9476',8)
  c.rect((90,155,360,390),'#acbbb7',r=12);c.rect((112,178,338,365),'#c6d4c9',r=7)
  for i in range(4):weight(c,155+i*49,310,30)
  c.line([(90,393),(90,495)],'#626d72',9);c.line([(356,392),(356,495)],'#626d72',9)
  c.rect((954,149,1163,498),'#6e7776',r=8);c.rect((974,167,1141,480),'#b7b6a1',r=4)
  c.text(1007,190,'OFFICE',22)
  for xx in [10,380,735,1190]:c.poly([(xx,678),(xx+30,633),(xx+70,652),(xx+99,691)],'#a38d76')
  if kind=='locker':
   for xx in range(70,1200,160):
    c.rect((xx,90,xx+145,615),'#879da0',r=6);c.rect((xx+10,105,xx+135,598),'#a6b8b3',r=4,w=2)
    for yy in [140,153,166]:c.line([(xx+26,yy),(xx+117,yy)],'#647d84',3)
    c.rect((xx+116,315,xx+125,360),GOLD,r=3,w=2)
 elif kind in ['stage','museum']:
  c.rect((0,0,1280,720),'#e4edf0',None);c.poly([(0,520),(1280,520),(1280,720),(0,720)],'#a5b8bf',None)
  for xx in [25,1225]:c.rect((xx,90,xx+26,566),'#809caa',None,r=8)
  c.rect((140,82,1140,329),'#2e4058',r=14);c.text(640,114,title or ('ANCIENT CRUELTY' if kind=='stage' else 'HOW HUMANS TRAINED'),37,'#fff1c9',anchor='mt')
  c.rect((1054,25,1225,64),'#b65652',None,r=6);c.text(1138,30,'LIVE' if kind=='stage' else 'MUSEUM',22,'#fff8ee',anchor='mt')
  c.rect((160,549,1124,675),'#c9d4d5',r=18)
  if kind=='stage':
   c.rect((24,450,137,523),INK,r=8);c.poly([(137,463),(174,444),(174,529),(137,510)],INK,None);c.line([(77,524),(77,620)],INK,7);c.line([(77,586),(34,658)],INK,7);c.line([(77,586),(123,658)],INK,7)
 elif kind=='office':
  c.rect((0,0,1280,720),'#ddd9cf',None);c.rect((0,530,1280,720),'#a5a99f',None)
  c.rect((215,57,1060,447),'#c6c6ba',r=8);c.rect((266,95,1022,406),'#eeeadd',r=4)
  c.rect((478,427,1121,623),'#9d7e66',r=8);c.rect((455,418,1146,449),'#c5aa83',r=6)
  c.rect((774,465,1066,524),'#ab8b6c',r=4,w=2);c.ell((1019,490,1025,496),INK,None)
  for xx in [165,340]:
   c.rect((xx,470,xx+105,554),'#818e91',r=12);c.line([(xx+8,551),(xx,660)],w=7);c.line([(xx+98,550),(xx+112,660)],w=7)
  c.text(645,140,'MEMBERSHIP OFFICE',30,anchor='mt');c.text(645,192,'PLEASE WAIT',22,'#82776e',anchor='mt')
 elif kind=='door':
  c.rect((0,0,1280,720),'#b9d5d5',None);c.rect((0,550,1280,720),'#9ca9a1',None)
  c.rect((427,80,846,603),'#6f8e94',r=12);c.rect((454,112,817,584),'#e4e5d1',r=8);c.rect((480,138,792,442),'#8fbac0',r=5)
  c.rect((766,457,780,508),GOLD,r=4);c.text(640,37,'FITNESS',30,anchor='mt')
 elif kind=='park':
  c.rect((0,0,1280,720),'#c4e1df',None);c.ell((1000,65,1115,180),'#f6dc8c',None)
  c.poly([(0,362),(230,230),(430,380),(690,220),(980,370),(1280,240),(1280,720),(0,720)],'#91b7a0',None)
  c.rect((0,484,1280,720),'#719876',None);c.poly([(0,651),(1280,517),(1280,624),(0,720)],'#ddc99d',None)
  for xx in [80,1120]:c.line([(xx,294),(xx,577)],'#6e7861',17);c.ell((xx-90,150,xx+95,363),'#608d78',None)
 elif kind=='steps':
  c.rect((0,0,1280,720),'#c8d9de',None);c.rect((740,90,1260,720),'#d6be9e',None);c.rect((966,140,1178,375),'#7a9da4',r=8)
  for i in range(5):c.rect((580+i*90,650-i*43,1280,720),'#9aabaf',w=3)
 elif kind=='diagram':
  c.rect((0,0,1280,720),'#f7efd9',None);c.rect((90,90,1190,606),'#e1eadc',r=25);c.text(640,117,title or 'THE BODY DOES THE WORK',31,anchor='mt')
 return c
