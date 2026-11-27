"""Story-led world/actions for all eleven chapters. Geometry is native-output scale."""
import math
import artwork as A
import motion as M
import gait as G
import locomotion_art as L
from PIL import Image
import film as F
import staging as S

class Offset:
 def __init__(self,c,dx=0,dy=0):self.c=c;self.dx=dx;self.dy=dy
 def p(self,p):return(p[0]+self.dx,p[1]+self.dy)
 def line(self,ps,*a,**k):return self.c.line([self.p(p) for p in ps],*a,**k)
 def poly(self,ps,*a,**k):return self.c.poly([self.p(p) for p in ps],*a,**k)
 def rect(self,b,*a,**k):return self.c.rect((b[0]+self.dx,b[1]+self.dy,b[2]+self.dx,b[3]+self.dy),*a,**k)
 def ell(self,b,*a,**k):return self.c.ell((b[0]+self.dx,b[1]+self.dy,b[2]+self.dx,b[3]+self.dy),*a,**k)
 def arc(self,b,*a,**k):return self.c.arc((b[0]+self.dx,b[1]+self.dy,b[2]+self.dx,b[3]+self.dy),*a,**k)
 def text(self,x,y,*a,**k):return self.c.text(x+self.dx,y+self.dy,*a,**k)
 def shadow(self,x,y,*a,**k):return self.c.shadow(x+self.dx,y+self.dy,*a,**k)

def tag(c,text,color=A.TEAL):
 c.rect((38,25,398,73),color,None,r=7);c.text(55,34,text,20,'#fff8e7')
def archive(c,text='RESTORED RECORDING'):
 tag(c,text,'#5c706d');c.line([(28,94),(28,641),(1250,641),(1250,94)],'#dbe8df',2)
def front(c,role,x,t,pose='stand',u=.4,mood='neutral',**kw):return A.person(c,x,ground=626,t=t,role=role,action=pose,u=u,talk=F.energy(t,role),mood=mood,**kw)
def card(c,x=640,y=330,back=False,scale=1):
 w=220*scale;h=140*scale;c.rect((x-w,y-h,x+w,y+h),'#fff7df',r=12,w=3)
 if back:
  c.text(x,y-h+25*scale,'TERMS & CONDITIONS',20*scale,anchor='mt')
  for k in range(8):c.line([(x-w+26*scale,y-h+67*scale+k*18*scale),(x+w-26*scale-(k%3)*24*scale,y-h+67*scale+k*18*scale)],'#aa9c83',2)
 else:
  c.text(x,y-h+26*scale,'MEMBERSHIP',25*scale,anchor='mt');c.text(x,y-27*scale,'PAID',44*scale,A.TEAL,anchor='mt');c.text(x,y+55*scale,'MONTHLY RENEWAL',17*scale,anchor='mt')
def paper(c,x,y,text='RECORD',w=95,h=65):
 c.rect((x-w,y-h,x,y),'#fff8df',r=4,w=2);c.text(x-w+8,y-h+10,text,11)
 for j in range(3):c.line([(x-w+9,y-h+32+j*9),(x-12,y-h+32+j*9)],'#b9ad91',1)
def new_background(kind,t=0,cam=(1,0,0),title=''):
 c=A.C(cam);A.background(c,kind,t,title if title else ' ' if kind=='diagram' else '');return c

def base_kind(scene):return 'stage' if 6<=scene<=8 else 'museum' if scene>=9 else 'dig'

def draw(t,s,r):
 mode=s['mode'];scene=r['scene'];line=r['line'];dt=t-r['start'];at=t-s['action_start'];dur=max(.05,s['action_end']-s['action_start']);u=max(0,min(1,at/dur));part=s['part'];shotlocal=t-s['start'];talk=lambda role:F.energy(t,role)
 # The whole live sequence remains spatially and prop-state continuous.
 if mode.startswith('stage-') or (mode in ['vale','mina'] and 6<=scene<=8):
  cam=None
  if mode=='vale':cam=(2.0,420,225)
  if mode=='mina':cam=(2.0,550,215)
  return S.draw(t,mode,camera=cam).im
 if mode in ['teaser-stage','rehearsal','manual','teaser-run']:
  c=new_background('stage',t,title='ANCIENT CRUELTY')
  A.treadmill(c,675,620,t,False);c.rect((1054,25,1225,64),'#b6844c',None,r=6);c.text(1138,30,'UPCOMING',20,'#fff8ee',anchor='mt')
  if mode=='teaser-stage':
   if part==0:M.walk(c,min(at,2.84),'VALE',490,620,mood='confident')
   else:front(c,'VALE',690,t,hand=(770,456),left=(710,456),mood='confident')
   c.text(1005,390,'ON AIR IN',24,anchor='mt');c.text(1005,437,'02:00',46,anchor='mt')
  elif mode=='rehearsal':
   # Rehearsed agony is acting, not a second paid scream recording.
   front(c,'VALE',690,t,'shrug',u=.25+.45*math.sin(at*2)**2,mood='surprised');c.text(940,420,'REHEARSAL',22,anchor='mt')
  elif mode=='manual':
   front(c,'VALE',690,t,'point',u=u,mood='confident');c.rect((900,400,1110,555),'#fff6d8',r=10);c.text(1005,425,'INSTRUCTIONS',20,anchor='mt');c.text(1005,477,'UNREAD',25,'#a75b50',anchor='mt')
  else:
   front(c,'VALE',690,t,hand=(770,456),left=(710,456),mood='confident');out=M.run(c,min(1.414,at),'MINA',1152,626);x,y=out['hands'][1];paper(c,x,y,'MANUAL',70,52)
  return c.im
 if mode=='timejump':
  c=new_background('dig',t);tag(c,'TWO HOURS EARLIER');M.walk(c,min(at,2.8),'VALE',260,626,mood='confident');front(c,'MINA',1015,t,'read',prop='tablet');return c.im
 if mode in ['vale','mina','paid-reaction']:
  who='VALE' if mode!='mina' else 'MINA';x=410 if who=='VALE' else 880;cam=(1.65,max(0,x-385),238) if mode!='paid-reaction' else(2.1,160,240);c=new_background(base_kind(scene),t,cam,title='HUMANS PAID TO BE TORTURED' if scene>=3 else '')
  front(c,'VALE',410,t,'read' if mode=='paid-reaction' else 'think' if line%3==2 else 'point',u=u,mood='surprised' if mode=='paid-reaction' else 'confident' if scene<4 else 'worried',prop='card' if mode=='paid-reaction' else None)
  front(c,'MINA',880,t,'point' if line%2 else 'shrug',u=u if line%2 else min(.12,u),mood='confident');return c.im
 if mode in ['dig-establish','dig-room']:
  c=new_background('dig',t);tag(c,'3026 · EXCAVATION');A.treadmill(c,770,620,t);M.walk(c,min(at,2.84),'VALE',200,626,mood='confident');front(c,'MINA',1090,t,'read',prop='tablet');c.line([(100,100),(160,115)],'#e0b67b',5);return c.im
 if mode=='pull-machine':
  c=new_background('dig',t,(1.15,50,65));c.rect((420,120,450,614),'#75878f',r=5);c.line([(435,130),(705,130),(705,235)],A.INK,8);c.ell((682,111,723,152),'#b8c7c5',w=4)
  y=292+90*A.smooth((math.sin(at*2)+1)/2);c.line([(705,130),(705,y)],'#8b8e79',5);c.line([(620,y),(790,y)],A.INK,10);front(c,'MEMBER',705,t,hand=(790,y),left=(620,y),arm_bends=(-1,1),mood='worried');front(c,'MINA',1080,t,'point',u=u);return c.im
 if mode in ['bench','rack-bar','progress-later','remove-plate','pain-stop','weight-task']:
  c=new_background('archive',t,(1.16,180,100));archive(c,'TRAINING RECORD' if scene==4 else 'RESTORED RECORDING')
  if mode=='remove-plate':v=1
  elif mode=='weight-task':v=1-.8*math.sin(math.pi*u)
  elif mode=='rack-bar':v=.65+.35*A.smooth(at/.6)
  elif mode=='pain-stop':v=.44 if at>.8 else .44+.16*math.cos(at*3)
  elif mode=='progress-later':v=.5+.45*math.sin(at*1.9)
  else:v=.5+.38*math.sin(at*1.6)
  extra=(False,False) if mode=='progress-later' else (True,at<.65) if mode=='remove-plate' else (True,True)
  A.bench(Offset(c,dy=-40),t,v,effort=mode not in ['progress-later','rack-bar'],extra=extra)
  if mode!='remove-plate':front(c,'COACH',1040,t,'point' if mode!='pain-stop' else 'shrug',u=min(.12,u) if mode=='pain-stop' else u,mood='confident' if mode!='pain-stop' else 'worried')
  if mode=='progress-later':c.text(700,112,'WEEKS LATER · SAME EXERCISE',23,anchor='mt')
  if mode=='remove-plate':
   # Close-up insert gives the coach actual ownership of a removed plate.
   grab=A.smooth(at/.6);back=A.smooth((at-.65)/.6);hp=(A.lerp(873,920,back),A.lerp(387,500,back)) if at>=.65 else (A.lerp(887,873,grab),A.lerp(524,387,grab));out=front(c,'COACH',940,t,left=hp,arm_bends=(-1,-1),mood='neutral')
   if at>=.65:c.rect((hp[0]-5,hp[1]-28,hp[0]+5,hp[1]+28),'#62758b',r=3);c.ell((hp[0]-6,hp[1]-6,hp[0]+6,hp[1]+6),'#e6bc94',w=2)
   c.text(700,112,'FIRST SESSION · START SMALL',23,anchor='mt')
  if mode=='pain-stop':c.rect((450,170,880,230),'#fff5dc',r=7);c.text(666,184,'STOP · CHANGE THE EXERCISE',23,'#a45749',anchor='mt')
  return c.im
 if mode=='coach':
  c=new_background('archive',t,(1.65,620,210));archive(c);front(c,'COACH',1030,t,'point',u=u,mood='confident');A.bench(Offset(c,dy=-40),t,.8);return c.im
 if mode in ['empty-office','office-detail']:
  cam=(1,0,0) if mode=='empty-office' else(1.3,230,120);c=new_background('office',t,cam);tag(c,'BACK OFFICE' if scene<9 else 'RECONSTRUCTED OFFICE')
  if mode=='office-detail':
   c.rect((998,482,1030,514),'#68716f',r=4,w=2);c.ell((1009,493,1017,506),A.INK,None)
  return c.im
 if mode in ['phone','banner-raise','banner','headline']:
  c=new_background('museum',t,title='HUMANS PAID TO BE TORTURED' if mode=='headline' else 'ANCIENT CRUELTY')
  if mode=='phone':
   out=front(c,'VALE',420,t,'think',mood='confident');x,y=out['hands'][1];c.rect((x-10,y-30,x+14,y+10),'#547c8b',r=4);front(c,'MINA',1020,t,'read',prop='tablet')
  else:
   front(c,'VALE',420,t,'point',u=u,mood='confident');front(c,'MINA',1020,t,'think',mood='worried');c.text(640,211,'LIVE DEMONSTRATION TODAY',25,'#f9e8c1',anchor='mt')
   if mode=='banner-raise':
    # Workers pull the display into place; its top edge visibly settles.
    yy=88-30*(1-A.smooth(at/.9));c.line([(170,yy),(170,33)],'#8b968e',5);c.line([(1110,yy),(1110,33)],'#8b968e',5)
  return c.im
 if mode in ['archive-console','rewind','records','calendar','training-days']:
  c=new_background('dig',t);front(c,'MINA',1010,t,'read',prop='tablet');c.rect((110,140,850,545),'#42556b',r=12);c.rect((134,167,827,490),'#d5dfd1',r=6)
  if mode in ['records','calendar','training-days']:
   c.text(480,188,'TRAINING LOG',25,anchor='mt')
   for j,label in enumerate(['PRACTICE','REST','PRACTICE','REST']):
    c.rect((195+j*150,280,326+j*150,410),'#fff7df',r=5);c.text(260+j*150,324,label,14,A.TEAL if label=='REST' else A.INK,anchor='mt')
  else:
   off=A.C();A.background(off,'archive',t);A.bench(Offset(off,dy=-40),t,.5+.3*math.sin(at*1.7));b=c.p((134,190,827,490));hh=b[3]-b[1];ww=round(hh*16/9);im=off.im.resize((ww,hh),Image.Resampling.LANCZOS);c.im.paste(im,(b[0]+(b[2]-b[0]-ww)//2,b[1]));c.text(485,175,'REWIND' if mode=='rewind' else 'RECOVERED SECURITY VIDEO',20,anchor='mt')
  return c.im
 if mode=='handshake':
  c=new_background('archive',t);archive(c);A.weight(c,300,385,200);g=A.smooth(at/.45)*(1-A.smooth((u-.82)/.18));meet=(760,465+5*math.sin(at*8));a=(A.lerp(698,meet[0],g),A.lerp(524,meet[1],g));b=(A.lerp(822,meet[0],g),A.lerp(524,meet[1],g));front(c,'MEMBER',645,t,hand=a,mood='happy');front(c,'COACH',875,t,left=b,mood='happy');return c.im
 if mode in ['entry','exit','return-shoes','door-hold']:
  c=new_background('door',t);archive(c,'LIFE OUTSIDE THE GYM' if scene==8 else 'RESTORED RECORDING');direction=-1 if mode=='exit' else 1;start=780 if direction<0 else 330;out=M.walk(c,min(at,2.84),'MEMBER',start,626,direction,mood='happy')
  if mode=='return-shoes':
   x,y=out['hands'][1];c.line([(x,y),(x+5,y+28)],A.INK,2);c.rect((x-14,y+28,x+22,y+47),'#c37b65',r=7)
  if mode=='door-hold':front(c,'COACH',850,t,'point',u=.4,mood='happy',hand=(780,477))
  return c.im
 if mode in ['locker-find','receipt','read-price','card-flip','fineprint','photograph','card-read']:
  c=new_background('locker' if scene<4 else 'museum',t)
  if mode in ['receipt','fineprint']:
   card(c,640,345,mode=='fineprint',1.1)
  elif mode=='card-flip':
   out=front(c,'MINA',780,t,'hold');x,y=out['hands'][1];thin=max(.06,abs(math.cos(math.pi*A.smooth(at/.65))));card(c,x-25,y-25,at>.32,.25*thin);front(c,'VALE',380,t,'read',prop='card',mood='surprised')
  elif mode=='photograph':
   front(c,'MINA',780,t,'hold',prop='card');out=front(c,'VALE',480,t,'point',u=u,mood='confident');x,y=out['hands'][1];c.rect((x-21,y-16,x+8,y+25),'#536b7b',r=4)
   if .4<at%2<.48:c.poly([(x,y),(x+90,y-55),(x+90,y+55)],'#f9e9ad',None)
  elif mode=='locker-find':
   c.poly([(700,113),(750,136),(750,576),(700,598)],'#d9ddcb');out=front(c,'MINA',590,t,'reach',u=min(1,at/.7),mood='neutral');x,y=out['hands'][1];paper(c,x,y,'MEMBER')
  else:front(c,'MINA',840,t,'read',prop='card');front(c,'VALE',410,t,'read',prop='card',mood='surprised' if mode=='read-price' else 'neutral')
  return c.im
 if mode in ['resistance','rest','add-plate','weights','load-compare','band-exercise','home-exercise']:
  c=new_background('diagram' if mode in ['resistance','load-compare'] else 'archive',t);archive(c,'ILLUSTRATED TRAINING' if mode in ['resistance','load-compare'] else 'TRAINING RECORD')
  if mode=='rest':
   c.rect((390,390,520,544),'#aebcaf',r=10);c.rect((390,542,520,563),'#9aa99d',r=8);c.line([(403,563),(403,640)],A.INK,7);c.line([(504,563),(504,640)],A.INK,7);state={'hip':(455,544),'x':455,'root':455,'direction':1,'ground':640,'run':False,'moving':False,'lean':-5,'arm_phase':0,'feet':[G.planted(475,640,0,1,'flat'),G.planted(505,640,0,1,'flat')]};out=L.render(c,t,'MEMBER',False,'happy',hand=(500,507),state_override=state);x,y=out['hands'][1];c.rect((x-8,y-25,x+10,y+16),'#a9ced3',r=5);c.text(850,280,'RECOVERY IS PART',27,anchor='mt');c.text(850,321,'OF TRAINING',27,anchor='mt')
  elif mode in ['band-exercise','home-exercise']:
   yy=420+14*math.sin(at*1.8);front(c,'MEMBER',610,t,hand=(710,yy),left=(510,yy),mood='happy');c.line([(510,yy),(610,510),(710,yy)],A.TEAL,6);c.text(900,190,'HOME' if mode=='home-exercise' else 'ADJUST THE EXERCISE',25,anchor='mt')
  else:
   A.bench(Offset(c,-80,-40),t,.5+.35*math.sin(at*1.8),effort=mode=='resistance');c.text(730,132,'A MANAGEABLE CHALLENGE',26,anchor='mt')
   if mode=='resistance':c.line([(610,350),(610,402)],'#b36951',6);c.poly([(599,393),(610,415),(621,393)],'#b36951',None)
   if mode in ['add-plate','weights','load-compare']:A.weight(c,1030,480,100);c.text(1030,365,'GRADUALLY',21,anchor='mt')
  return c.im
 if mode in ['belt','belt-control','cardio']:
  c=new_background('diagram' if mode=='cardio' else 'archive',t);archive(c,'AEROBIC ACTIVITY' if mode=='cardio' else 'RESTORED RECORDING');A.treadmill(c,675,620,t,True);out=M.belt(c,at,'WALKER',690,620,mood='happy')
  if mode=='cardio':
   # Cutaway is anchored to the actor's real chest, not a floating decorative dashboard.
   hx,hy=out['hip'];cx=hx+8;cy=hy-83;pulse=1+.10*math.sin(t*8);rr=12*pulse;c.ell((cx-rr,cy-rr,cx+rr,cy+rr),'#c56a65',A.INK,w=2);c.line([(cx+rr,cy),(950,cy-22)],'#9a655b',3);c.text(1020,cy-50,'HEART & BREATHING',22,anchor='mt')
  if mode=='belt-control':c.rect((970,280,1160,360),'#f9f0da',r=7);c.text(1065,296,'SHE SETS THE SPEED',17,anchor='mt')
  return c.im
 if mode=='vehicle-paradox':
  c=new_background('park',t);x=170+(at*100)%850;c.rect((x,440,x+275,540),'#748f9b',r=18);c.rect((x+55,386,x+219,446),'#b8d1d1',r=15)
  for xx in [x+60,x+215]:c.ell((xx-29,513,xx+29,571),A.INK,None);c.line([(xx,542),(xx+20*math.cos(at*5),542+20*math.sin(at*5))],'#becaca',3)
  c.text(730,190,'THEN THEY BOUGHT WALKING?',28,anchor='mt');return c.im
 if mode=='wheel-machine':
  c=new_background('dig',t);coachx=240+96*at;x=coachx+210;A.treadmill(c,x,620,t,False);M.cruise(c,at,'COACH',240,626,hand_target=(x-66,456));M.cruise(c,at,'VALE',60,626,mood='confident');tag(c,'TO THE LIVE STAGE');return c.im
 # Remaining robot, outdoor and ending families are defined in the second part below.
 return tail(t,s,r)

def robot_scene(t,s,r):
 c=new_background('stage',t,(1.14,135,80),title='WHO DOES THE WORK?');dt=t-F.BY[(7,1)]['start'];r0=F.BY[(7,1)];pick=F.mark(r0,'picks');take=F.mark(r0,'takes');lift=F.mark(r0,'lifts');ret=F.mark(r0,'returns')
 stand=(950,500);exchange=(967,467);high=(1080,393)
 if t<pick:pos=stand
 elif t<take:
  u=A.smooth((t-pick)/max(.1,take-pick));pos=(A.lerp(stand[0],exchange[0],u),A.lerp(stand[1],exchange[1],u))
 elif t<lift+.5:
  u=A.smooth((t-take)/max(.3,lift+.5-take));pos=(A.lerp(exchange[0],high[0],u),A.lerp(exchange[1],high[1],u))
 elif t<ret:pos=high
 else:
  u=A.smooth((t-ret)/.8);pos=(A.lerp(high[0],stand[0],u),A.lerp(high[1],stand[1],u))
 c.rect((936,506,964,521),'#c8c3ae',r=5);c.line([(950,522),(950,626)],A.INK,8);c.line([(922,626),(978,626)],A.INK,7)
 mh=pos if t<take else(A.lerp(exchange[0],901,A.smooth((t-take)/.5)),A.lerp(exchange[1],524,A.smooth((t-take)/.5)))
 front(c,'MINA',848,t,hand=mh,mood='confident')
 x=1090;y=626;c.shadow(x,y+6,50);c.rect((x-37,y-220,x+37,y-145),'#b7cdd0',r=15);c.rect((x-45,y-142,x+45,y-68),'#839cae',r=12)
 for k in [-1,1]:c.ell((x+k*17-6,y-199,x+k*17+6,y-187),A.TEAL,None);c.line([(x+k*25,y-64),(x+k*30,y-8)],A.INK,14);c.line([(x+k*39,y),(x+k*8,y)],A.INK,12)
 rh=pos if take<=t<ret+.8 else(1035,514)
 # Robot reaches the SAME grip point for transfer, not a teleporting dumbbell.
 if t<take:
  u=A.smooth((t-take+.45)/.45);rh=(A.lerp(1035,exchange[0],u),A.lerp(514,exchange[1],u))
 chain=A.ik((1048,498),rh,72,68,1);c.line(chain,A.INK,12);c.line([(1130,498),(1160,545)],A.INK,12)
 A.weight(c,*pos,63)
 if t<take:c.ell((pos[0]-6,pos[1]-6,pos[0]+6,pos[1]+6),'#e6bc94',w=2)
 else:c.rect((pos[0]-8,pos[1]-6,pos[0]+8,pos[1]+6),'#93abb0',r=3,w=2)
 return c

def tail(t,s,r):
 mode=s['mode'];scene=r['scene'];line=r['line'];at=t-s['action_start'];dur=max(.05,s['action_end']-s['action_start']);u=max(0,min(1,at/dur));part=s['part']
 if mode in ['robot-pickup','robot-lift','robot-versus-body']:
  return robot_scene(t,s,r).im
 if mode=='arm-look':
  return S.draw(t,'stage-reaction',camera=(2.1,500,280)).im
 if mode=='body-work':
  c=new_background('diagram',t);A.bench(Offset(c,-60,-40),t,.5+.35*math.sin(at*1.8));c.text(815,181,'THE BODY ADAPTS OVER TIME',26,anchor='mt');return c.im
 if mode in ['screen-switch','live-evidence']:
  def screen(c):
   c.rect((265,91,1015,306),'#d6e1d6',r=8);c.text(640,112,'OUTSIDE THE GYM',26,anchor='mt');c.poly([(300,273),(385,191),(452,263),(537,175),(650,272)],'#87a891',None);c.line([(750,272),(875,198)],'#8c9a9f',18);c.rect((875,198,944,272),'#b7a185',r=4)
  return S.draw(t,'stage-wide',camera=(1,0,0),screen_layer=screen).im
 if mode=='groceries':
  c=new_background('steps',t);c.rect((0,500,1280,720),'#b7c4c5',None)
  for i in range(4):c.rect((650+i*55,612-i*28,1280,720),'#99aaad',w=3)
  M.stairs(c,min(at,2.59),'MEMBER');archive(c,'LIFE OUTSIDE THE GYM');return c.im
 if mode=='park':
  c=new_background('park',t);M.cruise(c,at,'WALKER',340,626,mood='happy');M.cruise(c,at,'MEMBER',650,626,mood='happy');archive(c,'LIFE OUTSIDE THE GYM');return c.im
 if mode=='everyday':
  c=new_background('park',t);M.cruise(c,at,'MEMBER',360,626,mood='happy',bag=True);c.text(880,270,'EVERYDAY FUNCTION',27,anchor='mt');return c.im
 if mode=='broadcast-hand':
  return S.draw(t,'stage-question',camera=(1.7,350,230)).im
 if mode=='stop-machine':
  c=S.draw(t,'stage-question',camera=(1.6,340,220));return c.im
 if mode in ['correct','card-exhibit']:
  c=new_background('museum',t,title='GYM');A.treadmill(c,675,620,t,False);front(c,'VALE',380,t,'read',prop='card',mood='neutral');front(c,'MINA',1020,t,'point',u=u,mood='happy')
  c.rect((390,380,880,502),'#fff8e2',r=9);c.text(640,392,'TORTURE CHAMBER',22,anchor='mt');c.line([(437,420),(844,404)],'#b76559',5);c.text(640,433,'GYM',34,A.TEAL,anchor='mt')
  if mode=='card-exhibit':
   c.rect((960,535,1140,552),'#c8d1c8',r=5);card(c,1050,490,False,.3)
  return c.im
 if mode in ['office-approach','member','clerk']:
  c=new_background('office',t,(1,0,0));archive(c,'FINAL RECOVERED RECORDING')
  # Draw clerk behind the counter; hands and forms stay above its actual top surface.
  out=front(c,'CLERK',930,t,'read' if line%2 else 'shrug',u=min(.12,u),mood='neutral',prop='card' if line%2 else None)
  c.rect((478,449,1121,623),'#9d7e66',r=5);c.rect((455,418,1146,449),'#c5aa83',r=6)
  if mode=='office-approach':M.walk(c,min(at,2.84),'MEMBER',110,626,mood='neutral')
  else:front(c,'MEMBER',350,t,'shrug' if line>=6 else 'read',u=min(.12,u),mood='worried',prop='card' if line<6 else None)
  # Keep the actual locked drawer legible as an early/late shared physical detail.
  c.rect((774,465,1066,524),'#ab8b6c',r=4,w=2);c.ell((1019,490,1025,496),A.INK,None)
  return c.im
 if mode=='sign-pickup':
  c=new_background('museum',t,title='GYM');lift=A.smooth((at-.3)/1.0);yy=A.lerp(558,467,lift);front(c,'VALE',845,t,'bend',u=1-lift,mood='surprised',hand=(910,yy),left=(780,yy));c.rect((690,yy-6,1000,yy+68),'#e8ba73',r=8);c.text(845,yy+10,'TORTURE CHAMBER',20,anchor='mt');return c.im
 if mode=='museum-visitors':
  c=new_background('museum',t,title='GYM');A.treadmill(c,835,620,t);A.weight(c,340,430,180);M.cruise(c,at,'VISITOR',170,626,mood='happy');c.rect((420,151,679,357),'#fff5dd',r=5);c.text(550,175,'TRAINING',24,anchor='mt');c.text(550,227,'EFFORT + RECOVERY',16,anchor='mt');return c.im
 if mode in ['sign-mount','ending-mina','ending']:
  c=new_background('office',t,(1.4,240,25) if mode=='ending' and part==0 else (1,0,0));tag(c,'MUSEUM · OPENING DAY');c.line([(390,120),(390,615),(1135,615),(1135,120)],'#6d828a',8)
  c.rect((585,75,895,149),'#e8ba73',r=8,w=4);c.text(740,93,'TORTURE CHAMBER',20,anchor='mt')
  front(c,'VALE',270,t,'stand',mood='happy');front(c,'MINA',1160,t,'shrug' if mode=='ending-mina' else 'stand',u=min(.12,u),mood='happy')
  if mode=='sign-mount':
   # The mounting view shows the label and its place, rather than another generic title card.
   c.line([(616,75),(616,58)],A.INK,3);c.line([(863,75),(863,58)],A.INK,3)
  return c.im
 raise ValueError(('unhandled picture mode',mode))
