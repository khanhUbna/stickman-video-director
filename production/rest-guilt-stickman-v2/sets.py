"""Native 16:9 story-specific rooms and outdoor stages; no portrait movie crops."""
from pathlib import Path
from functools import lru_cache
import math
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from rig import line,poly,ip
B=Path(__file__).resolve().parent;FONT=str(B/'fonts/ArchivoBlack.ttf')
def label(g,xy,text,size=20,fill='#49514d'):g.text(xy,text,font=ImageFont.truetype(FONT,size),fill=fill)
def window(g,box,night=False):
 x,y,xx,yy=box;g.rounded_rectangle(box,5,fill='#8f7761',outline='#6d5a4b',width=5)
 g.rectangle((x+11,y+11,xx-11,yy-11),fill='#2b3f54' if night else '#bdd4d7')
 g.ellipse((xx-100,y+30,xx-60,y+70),fill='#eee2ac' if night else '#ecd0a0')
 for px,hh in [(x+12,70),(x+70,100),(x+145,58),(x+210,80)]:g.rectangle((px,yy-hh,px+55,yy-12),fill='#697c8a' if night else '#94aca8')
 g.rectangle(((x+xx)//2-4,y+8,(x+xx)//2+5,yy-8),fill='#9c8062');g.rectangle((x+8,(y+yy)//2-4,xx-8,(y+yy)//2+5),fill='#9c8062')
 poly(g,[(x-20,y-8),(x+25,y-8),(x+32,yy+13),(x-17,yy+24)],'#e2d2b4','#ad9779',2)
 poly(g,[(xx-25,y-8),(xx+22,y-8),(xx+20,yy+23),(xx-29,yy+14)],'#e2d2b4','#ad9779',2)
 for px in [x-10,x+8,xx-10,xx+8]:line(g,[(px,y+10),(px+3,yy-6)],'#c3af8f',2)
def plant(g,x,y,scale=1):
 def p(v):return [x+v[0]*scale,y+v[1]*scale]
 poly(g,[p(v) for v in [(-30,0),(31,0),(24,70),(-23,70)]],'#b0825a','#755b45',3)
 for dx,dy in [(-26,-45),(22,-72),(-18,-105),(29,-132)]:
  line(g,[p((0,5)),p((dx,dy))],'#5a7050',4)
  q=p((dx,dy));r=22*scale;g.ellipse((q[0]-r,q[1]-r,q[0]+r,q[1]+r),fill='#84996c',outline='#61784f',width=2)
def picture(g,x,y,w=170):
 poly(g,[(x,y),(x+w,y-2),(x+w+1,y+110),(x-2,y+112)],'#e9dfc5','#8a7258',5)
 poly(g,[(x+10,y+100),(x+60,y+40),(x+95,y+79),(x+w-10,y+29),(x+w-10,y+100)],'#85957b',None)
 g.ellipse((x+100,y+15,x+122,y+37),fill='#d4b16c')
def rug(g,box):
 g.ellipse(box,fill='#a1a38c',outline='#7d8877',width=3);x,y,xx,yy=box;g.ellipse((x+20,y+8,xx-20,yy-8),outline='#c3c0a5',width=2)
def table(g,x,y,width=230):
 for px in [x+15,x+width-20]:line(g,[(px,y),(px-8 if px<x+width/2 else px+8,590)],'#735b45',6)
 poly(g,[(x,y-10),(x+width,y-10),(x+width+14,y+10),(x-10,y+10)],'#c4a071','#735b45',3)

@lru_cache(maxsize=24)
def background(name,night=False):
 im=Image.new('RGBA',(1280,720),'#d9c9ad');g=ImageDraw.Draw(im)
 if name in ['street','park']:
  g.rectangle((0,0,1280,450),fill='#8ba4b4' if night else '#bfd5d5')
  g.ellipse((1080,40,1140,100),fill='#f0ddb0')
  if name=='street':
   for x,h,c in [(0,290,'#c6af96'),(220,350,'#b2b69f'),(450,250,'#d1b797'),(700,330,'#a8b5ac'),(970,300,'#c7b59d')]:
    poly(g,[(x,430-h),(x+200,425-h),(x+200,455),(x,455)],c,'#7a7e72',3)
    for xx in range(x+25,x+180,60):
     for yy in range(465-h,400,64):g.rectangle((xx,yy,xx+30,yy+42),fill='#637c88',outline='#8a8d7a',width=2)
   g.rectangle((0,435,1280,523),fill='#7e8b8b');g.line((0,482,1280,482),fill='#d2cdb5',width=3)
   for x in range(0,1280,140):g.rectangle((x,477,x+75,483),fill='#d8d1b6')
   g.rectangle((0,523,1280,720),fill='#b6ad98');g.line((0,524,1280,524),fill='#777d71',width=5)
   for x in range(-40,1300,180):g.line((x,530,x+55,720),fill='#a69f8d',width=2)
  else:
   g.rectangle((0,350,1280,720),fill='#9eae83');poly(g,[(0,610),(1280,510),(1280,720),(0,720)],'#c7b896',None)
   for x,y,sc in [(120,210,1.3),(430,250,.8),(1150,200,1.4)]:
    line(g,[(x,y+30),(x,y+260*sc)],'#77684d',round(15*sc))
    for dx,dy,r in [(-35,0,65),(35,5,65),(0,-50,75)]:g.ellipse((x+dx-r*sc,y+dy-r*sc,x+dx+r*sc,y+dy+r*sc),fill='#718d62',outline='#617d55',width=3)
   for xx in [850,1100]:line(g,[(xx,465),(xx,590)],'#6c6250',8)
   for yy in [380,415,450]:g.rounded_rectangle((825,yy,1132,yy+21),5,fill='#9c7d56',outline='#6e5b43',width=3)
   g.rounded_rectangle((815,475,1142,500),6,fill='#b69870',outline='#6e5b43',width=3)
   for x in [65,340,1230]:plant(g,x,530,.65)
 else:
  g.rectangle((0,520,1280,720),fill='#b88e68');g.rectangle((0,512,1280,527),fill='#8c7258')
  for y in [560,620,697]:g.line((0,y,1280,y+7),fill='#aa805f',width=2)
  for x in [100,390,750,1110]:g.line((x,525,x+40,720),fill='#ad8461',width=2)
  if name=='living':
   window(g,(65,75,415,340),night);picture(g,825,90);plant(g,1150,443,.8)
   poly(g,[(488,460),(493,365),(522,344),(823,347),(852,372),(857,502),(488,502)],'#bb856e','#78594a',4)
   for x in [515,675]:g.rounded_rectangle((x,365,x+144,467),20,fill='#c7937b',outline='#a77660',width=3)
   g.rounded_rectangle((487,458,857,503),16,fill='#d5aa8e',outline='#78594a',width=4)
   for x in [468,838]:g.rounded_rectangle((x,420,x+40,520),15,fill='#b78168',outline='#78594a',width=4)
   for x in [507,812]:line(g,[(x,504),(x,548)],'#705645',7)
   rug(g,(365,550,1080,698));table(g,915,440,130)
  elif name=='office':
   window(g,(70,65,405,330),False);plant(g,150,440,.9);picture(g,1050,90,140)
   table(g,660,430,490);g.rectangle((650,411,1140,426),fill='#957c60')
   g.rounded_rectangle((820,195,1070,365),9,fill='#606e70',outline='#3b4b50',width=4);g.rectangle((832,207,1058,353),fill='#d9e6df')
   g.rectangle((934,365,951,409),fill='#667873');g.ellipse((905,401,985,414),fill='#667873')
   for y in [234,265,301]:g.rounded_rectangle((850,y,1040,y+17),4,fill='#a3bcb3')
   label(g,(854,213),'INBOX',14,'#416156')
  elif name=='entry':
   poly(g,[(90,43),(355,39),(357,525),(91,525)],'#8e9d8f','#606d60',5)
   g.rounded_rectangle((115,70,332,340),8,outline='#71846e',width=3);g.ellipse((310,366,323,379),fill='#ccb470',outline='#655843',width=2)
   for x in [530,625,720]:line(g,[(x,115),(x,154),(x-18,164)],'#735e4b',6)
   picture(g,920,80,180);table(g,730,435,380);rug(g,(90,547,500,670));plant(g,1200,440,.7)
   poly(g,[(525,462),(708,460),(720,484),(515,484)],'#b99b74','#745b45',4)
   for x in [535,695]:line(g,[(x,480),(x,580)],'#745b45',7)
  elif name=='kitchen':
   window(g,(65,70,400,325),night)
   for x in [805,1020]:
    g.rounded_rectangle((x,74,x+197,238),7,fill='#9da48b',outline='#6c765f',width=4);g.line((x+100,82,x+100,233),fill='#7b856c',width=3)
    g.ellipse((x+80,154,x+89,163),fill='#d1b47b');g.ellipse((x+113,154,x+122,163),fill='#d1b47b')
   g.rectangle((795,250,1250,429),fill='#d8b99c')
   for y in range(254,430,44):g.line((795,y,1250,y),fill='#bd9f86',width=2)
   for x in range(800,1250,70):g.line((x,254,x,430),fill='#bd9f86',width=2)
   g.rectangle((797,439,1250,590),fill='#a1a68c',outline='#6a715c',width=4)
   poly(g,[(787,426),(1258,426),(1271,446),(782,446)],'#c8a172','#755c46',4)
   g.ellipse((1050,430,1150,445),fill='#758c8b');g.arc((1090,370,1125,435),180,360,fill='#777b6b',width=7)
   for x in [960,1160]:g.line((x,455,x,585),fill='#778267',width=3)
   plant(g,1190,366,.5)
  elif name=='hobby':
   window(g,(65,65,390,330),night);picture(g,1030,75,150);rug(g,(310,550,1080,695))
   for y in [230,370]:
    g.rectangle((930,y,1210,y+15),fill='#a17d57',outline='#755e43',width=3)
    for i,c in enumerate(['#819c8d','#b29b70','#a57e70','#768a98','#c3b389']):g.rectangle((955+i*42,y-76,987+i*42,y-3),fill=c,outline='#725f4f',width=2)
   table(g,900,440,220)
  elif name=='laundry':
   window(g,(65,60,400,270),False)
   g.rounded_rectangle((135,310,420,586),15,fill='#d7d7c8',outline='#7c867b',width=4);g.ellipse((188,370,370,552),fill='#829797',outline='#617876',width=6)
   g.rectangle((152,326,401,354),fill='#a6b7a9');g.ellipse((347,331,361,345),fill='#6b8075')
   table(g,730,440,420);g.rounded_rectangle((1050,480,1190,590),12,fill='#ba9d71',outline='#7b694f',width=3)
   for x in range(1065,1190,22):g.line((x,487,x,580),fill='#d4bc92',width=2)
  elif name=='bedroom':
   window(g,(65,65,395,330),True);picture(g,950,95,170)
   g.rounded_rectangle((850,335,1220,570),22,fill='#929b8b',outline='#687564',width=5)
   g.rounded_rectangle((832,410,1245,590),22,fill='#b4bb9e',outline='#687564',width=4)
   g.rounded_rectangle((875,354,1020,418),12,fill='#eee5cc',outline='#a7a78e',width=3)
   g.rectangle((1030,426,1225,580),fill='#8faaa0');table(g,730,438,125);rug(g,(380,550,830,692))
 # Static local pigment grain, cached with each native set, never swimming over actors.
 ar=np.asarray(im).copy();rng=np.random.default_rng(sum(map(ord,name))+(13 if night else 0));noise=rng.normal(0,.9,ar[:,:,:3].shape[:2]+(1,));ar[:,:,:3]=np.clip(ar[:,:,:3]+noise,0,255).astype('uint8');im=Image.fromarray(ar)
 if night and name not in ['street','park']:im=Image.alpha_composite(im,Image.new('RGBA',im.size,(24,37,55,25)))
 return im

def moving_world(im,name,elapsed,night=False):
 g=ImageDraw.Draw(im)
 if name=='street':
  x=-160+elapsed*165;y=477
  if -180<x<1400:
   poly(g,[(x-70,y-20),(x-46,y-62),(x+25,y-62),(x+64,y-25),(x+88,y-21),(x+88,y+2),(x-85,y+2),(x-85,y-20)],'#b58a6d','#5f655d',3)
   poly(g,[(x-40,y-55),(x+16,y-55),(x+47,y-28),(x-54,y-28)],'#a8c4c6','#5f655d',2)
   for xx in [x-48,x+53]:
    g.ellipse((xx-15,y-10,xx+15,y+20),fill='#3d4847');a=elapsed*165/15
    line(g,[(xx+11*math.cos(a),y+5+11*math.sin(a)),(xx-11*math.cos(a),y+5-11*math.sin(a))],'#bdc6ba',2)
 elif name=='park':
  for k in [0,1]:
   x=520+elapsed*30+k*50;y=110+k*35+6*math.sin(elapsed*2+k)
   line(g,[(x-9,y-3*math.sin(elapsed*5)),(x,y+4),(x+9,y-3*math.sin(elapsed*5))],'#6b7e7d',2)

def export_sets():
 for n in ['living','office','entry','kitchen','hobby','laundry','bedroom','street','park']:
  for night in ([False,True] if n in ['living','kitchen','hobby'] else [False]):background(n,night).save(B/f'art/set-{n}{"-night" if night else ""}.png')
if __name__=='__main__':export_sets();print('Native landscape sets saved.')
