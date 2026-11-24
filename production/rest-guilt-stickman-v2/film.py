"""New 2D performance of the approved story. Native seconds, physical props, planted feet."""
from pathlib import Path
from functools import lru_cache
import json,math,bisect
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import rig,props,sets_new as sets
from rig import actor,rotate,mix,line,poly,ip,ease
from caption_renderer import CaptionRenderer
P=Path(__file__).resolve().parent
T=json.loads((P/'timeline.json').read_text());SHOTS=T['shots'];STARTS=[s['start'] for s in SHOTS]
CUES=json.loads((P/'captions.json').read_text());CSTARTS=[s['start'] for s in CUES]
CR=CaptionRenderer(P,'16:9',1280,720,T['caption_profile']);FONT=str(P/'fonts/ArchivoBlack.ttf')
INK='#202936';REMOTE=np.array([762.,466.]);BOWL=np.array([575.,500.])
def on(t,a,b):return ease((t-a)/max(.001,b-a))
def txt(g,xy,text,size=23,color='#304f47'):g.text(ip(xy),text,font=ImageFont.truetype(FONT,size),fill=color)
def wrap(g,text,xy,width,size=23,color='#304f47'):
 f=ImageFont.truetype(FONT,size);out='';y=xy[1]
 for word in text.split():
  candidate=(out+' '+word).strip()
  if g.textlength(candidate,font=f)>width and out:g.text((xy[0],y),out,font=f,fill=color);y+=size*1.4;out=word
  else:out=candidate
 if out:g.text((xy[0],y),out,font=f,fill=color)
def remote(im,c,angle=0):
 tile=Image.new('RGBA',(42,84));g=ImageDraw.Draw(tile);g.rounded_rectangle((7,3,35,79),8,fill='#424c4c',outline=INK,width=2)
 for i,col in enumerate(['#c9876c','#e2d9bb','#e2d9bb']):g.ellipse((17,14+i*17,25,22+i*17),fill=col)
 rr,pos=rig.transformed(tile,c,[21,42],.7,angle);im.alpha_composite(rr,pos)
def bowl(im,c):
 x,y=c;g=ImageDraw.Draw(im);g.ellipse((x-32,y-17,x+32,y+14),fill='#f1e0ae',outline='#6d7464',width=3)
 g.pieslice((x-32,y-26,x+32,y+25),0,180,fill='#a2b7a0',outline='#5a7568',width=3)
 for i in range(9):
  xx=x-22+(i%5)*11;yy=y-12-(i//5)*8;g.ellipse((xx-5,yy-6,xx+6,yy+5),fill='#f5e3b1',outline='#b2a16f')
def phone_insert(im,mode,l):
 g=ImageDraw.Draw(im);g.rounded_rectangle((465,98,815,589),27,fill='#344841',outline='#202936',width=7);g.rounded_rectangle((483,121,797,563),12,fill='#f7ecd3')
 g.rectangle((483,121,797,186),fill='#587e6e');txt(g,(505,139),'TIMER' if mode=='timer' else 'MESSAGES',24,'#fff2d8')
 if mode=='timer':txt(g,(525,285),'00:00',64);txt(g,(533,381),'Break over',26)
 else:
  message='Finally, movie time.' if mode=='movie' else "How's the movie?";g.rounded_rectangle((502,212,777,310),10,fill='#dbe2ca');wrap(g,message,(520,232),242,27)
  if mode=='draft':
   g.rounded_rectangle((502,345,777,494),10,fill='#fff9e6');draft="Haven't earned it yet.";shown=draft[:round(len(draft)*on(l,.10,.85))];wrap(g,shown,(521,366),242,27);txt(g,(520,515),'UNSENT',20,'#a16b4b')
 # Cropped hands hold the bezel below the meaningful text.
 for x in [470,810]:g.ellipse((x-18,498,x+18,582),fill=INK)
 if mode=='draft' and l<.8:g.ellipse((755,544,775,570),fill=INK)
def laptop(im,mode='email',progress=0,lid=0,foreground=False):
 g=ImageDraw.Draw(im);top=280+144*lid
 poly(g,[(730,top),(950,top+5),(950,423),(730,419)],'#829b86','#4c6559',4)
 if lid<.8:
  poly(g,[(741,top+12),(939,top+17),(939,405),(741,403)],'#f1e7ca',None)
  if lid<.4:
   txt(g,(754,top+24),'Document' if mode=='document' else 'Inbox',19)
   if mode=='document':wrap(g,'One correction. It can wait until tomorrow.',(754,top+55),167,15)
   elif mode=='overflow':
    for i in range(3):
     if progress>i*.45:g.rounded_rectangle((751,top+62+i*26,930,top+85+i*26),3,fill='#ccdac0');txt(g,(759,top+66+i*26),['Another message','A document','One small change'][i],13)
   else:wrap(g,'Quick question about the document.',(754,top+55),166,15)
 poly(g,[(586,423),(949,423),(977,446),(570,446)],'#b0bda1','#536f5f',3)
 for y in [429,437]:
  for x in range(598,934,22):g.rectangle((x,y,x+14,y+4),fill='#e9e2c4')
 if lid>.72:
  yy=423+23*on(lid,.72,1.)
  poly(g,[(730,423),(950,423),(977,yy),(570,yy)],'#829b86','#4c6559',4)
  if lid>.98:poly(g,[(586,423),(949,423),(977,446),(570,446)],'#829b86','#4c6559',4)
def sink(im,x,water):
 g=ImageDraw.Draw(im);poly(g,[(x-150,440),(x+220,440),(x+245,470),(x-170,470)],'#ddc49b','#755f45',4)
 poly(g,[(x-165,470),(x+240,470),(x+230,594),(x-158,594)],'#8da18a','#5f735f',4)
 g.ellipse((x-4,426,x+149,454),fill='#8eaaa3',outline='#526f65',width=3)
 g.arc((x+40,317,x+114,398),170,360,fill='#475d55',width=8);line(g,[(x+114,356),(x+114,431)],'#475d55',8)
 line(g,[(x+118,404),(x+141,395)],'#6e6852',7)
 if water:line(g,[(x+41,358),(x+41,428)],'#c5e7e5',4)
 # Drying rack remains distinct from the held clean plate.
 g.rounded_rectangle((x-145,422,x-35,439),3,fill='#94745a',outline='#4a5e54',width=3)
 for i in range(5):line(g,[(x-135+i*22,429),(x-131+i*22,391)],'#4a5e54',5)
def stand_pose(x=650):return {'hip':np.array([float(x),418.]),'feet':{'left':np.array([x-25.,590.]),'right':np.array([x+28.,590.])},'view':'front','angle':0.,'head':0.,'expr':'normal','wr':{},'held':{},'draws':[],'plants':{'left':True,'right':True}}
def sit_pose(x=650):
 a=stand_pose(x);a['hip']=[x,480.];a['feet']={'left':np.array([x-25.,590.]),'right':np.array([x+28.,590.])};return a
def hand(a,side,local):a['wr'][side]=np.asarray(a['hip'])+rotate(local,a['angle']);return a['wr'][side]
def rest(a):
 for side in ['left','right']:hand(a,side,[-68 if side=='left' else 72,-6])
def carry(a,name,side,draw,offset=(0,0)):
 grip=a['wr'][side].copy();center=grip+offset;a['draws'].append(lambda im,c=center:draw(im,c));a['held'][name]={'arm':side,'point':grip}
def walk_pose(start,end,t,duration=1.35):
 n=max(4,math.ceil(abs(end-start)/115));n+=n%2;dt=duration/n;feet={};plants={}
 for side in ['left','right']:
  offset=-25 if side=='left' else 28;x=start+offset;moving=False
  for i in range(n):
   if ('left' if i%2==0 else 'right')!=side:continue
   target=start+(end-start)*min(1,(i+1)/(n-1))+offset;begin=i*dt
   if t>=begin+dt:x=target
   elif t>=begin:u=(t-begin)/dt;feet[side]=np.array([x+(target-x)*ease(u),590-24*math.sin(math.pi*u)]);moving=True;break
   else:break
  if not moving:feet[side]=np.array([float(x),590.])
  plants[side]=not moving
 x=(feet['left'][0]+feet['right'][0])/2;a=stand_pose(x);a['feet']=feet;a['plants']=plants
 view='three_quarter' if end>=start else 'front'
 a['hip'][1]=max(418.,max(feet[side][1]-math.sqrt(174**2-(feet[side][0]-(x+spec['hip'][0]*rig.S))**2) for package in rig.PACKS.values() for side,spec in package['views'][view]['legs'].items()))
 a['view']='three_quarter' if end>=start else 'front';a['angle']=4*math.sin(math.pi*min(1,t/duration));swing=math.sin(t/dt*math.pi)
 for side in ['left','right']:hand(a,side,[-68+16*swing if side=='left' else 72-16*swing,-6+4*swing])
 return a
def show_actor(im,a,who='hero'):
 def draw(m):
  for d in a['draws']:d(m)
 row=actor(im,a['hip'],view=a['view'],angle=a['angle'],head_angle=a['head'],expression=a['expr'],feet=a['feet'],wrists=a['wr'],who=who,prop_draw=draw,held=a['held'])
 for side in row['legs']:row['legs'][side]['planted']=a['plants'][side]
 return row
@lru_cache(maxsize=12)
def background(name):
 mapped={'work':'office','friend':'bedroom','inspection':'office'}.get(name,name)
 return sets.background(mapped,True).copy()
def scene(t,s):
 l=max(0,t-s['start']);dur=s['duration'];a=s['action'];p=s['paragraph'];im=background(s['set']).copy();g=ImageDraw.Draw(im);rows=[];events=[]
 hero=None;buddy=None;post=[];water=False;lid=0;desk=s['set']=='work';kitchen=s['set']=='kitchen';living=s['set']=='living'
 if living:
  sets.table(g,890,440,150)
  # A television on its own stand makes the movie action visible.
  tv=Image.new('RGBA',(1280,720));tg=ImageDraw.Draw(tv)
  tg.rounded_rectangle((1000,254,1253,420),8,fill='#344641',outline=INK,width=5);tg.rectangle((1012,267,1240,405),fill='#8dabb0')
  poly(tg,[(1013,405),(1070,321),(1130,373),(1200,310),(1240,405)],'#657e76',None);playing=p==1 or p>=12 or (p==11 and a=='sit_play' and l>.94);sunx=1170+(5*math.sin(t*.2) if playing else 0);tg.ellipse((sunx,281,sunx+24,305),fill='#eac787')

  if not playing:poly(tg,[(1118,316),(1118,357),(1152,336)],'#eee1b9','#536c61',2)
  line(tg,[(1120,422),(1120,486)],'#48594b',7);line(tg,[(1074,489),(1162,489)],'#48594b',7)

  im.alpha_composite(tv,(0,0))
  if a in ['remote_insert','empty_movie','walk_snack','sit_back','snack_grab'] or a=='sit_play' and l<.8 or a=='startle' and l>=.36:remote(im,REMOTE)

 if desk:
  g.rounded_rectangle((563,352,684,493),10,fill='#9a9f82',outline='#62715c',width=4);g.rounded_rectangle((553,487,698,508),7,fill='#b2ac88',outline='#596e5e',width=4)
  for xx in [569,683]:line(g,[(xx,506),(xx,590)],'#5e6e59',6)
  sets.table(g,565,447,420)
 if s['set']=='friend':
  g.rounded_rectangle((411,477,853,548),18,fill='#a3ad91',outline='#6e735c',width=5);g.rounded_rectangle((736,434,846,489),15,fill='#e2d6b7',outline='#91866e',width=3)
 if a=='keys':
  # Native physical detail, not a floating key icon.
  g.rectangle((0,0,1280,720),fill='#b58a58');g.rectangle((1045,0,1080,720),fill='#70563e');g.ellipse((715,220,833,338),fill='#c0ae80',outline='#786847',width=5)
  g.ellipse((768,268,782,296),fill=INK);ang=35*math.sin(math.pi*on(l,.1,.75));c=np.array([674.,282.]);v=rotate([110,0],ang)
  line(g,[c,c+v],'#725f37',15);g.ellipse((c[0]-45,c[1]-45,c[0]+45,c[1]+45),outline='#cfad57',width=13)
  for f in [.67,.83]:line(g,[c+v*f,c+v*f+rotate([0,20],ang)],'#cfad57',11)
  line(g,[c+[-20,27],c+[-165,76]],INK,12);g.ellipse((c[0]-40,c[1]+10,c[0]-1,c[1]+48),fill=INK)
  return im,rows,[{'kind':'keys','phase':l}]
 if a in ['phone_movie','phone_question','unsent_insert','thumb_stop','timer_insert']:
  phone_insert(im,'timer' if a=='timer_insert' else 'movie' if a=='phone_movie' else 'draft' if a in ['unsent_insert','thumb_stop'] else 'question',l if a!='thumb_stop' else 2.)
  return im,rows,events
 if a in ['email_insert','document_insert','inbox_overflow']:
  laptop(im,'document' if a=='document_insert' else 'overflow' if a=='inbox_overflow' else 'email',l)

  if not (a=='email_insert' and p==2):im=im.crop((554,246,994,493)).resize((1280,720),Image.Resampling.LANCZOS)
  return im,rows,events
 if a in ['remote_insert','snack_cooling']:
  if a=='remote_insert':remote(im,REMOTE);box=(635,370,945,544)
  else:sets.table(g,585,445,360);bowl(im,[746,427]);props.plate(im,[870,431]);box=(565,300,1085,592)
  return im.crop(box).resize((1280,720),Image.Resampling.LANCZOS),rows,events
 if a=='empty_movie':return im,rows,events
 if a in ['inspection','receipt']:
  if a=='receipt':
   poly(g,[(324,131),(914,145),(959,552),(292,543)],'#e8dec2','#7c6a50',5);txt(g,(400,215),'PERMISSION TO REST',35);txt(g,(411,330),'Receipt required.',32);txt(g,(414,421),'Not found.',30)
   return im,rows,events
  hero=stand_pose(574);rest(hero);hand(hero,'right',[110,-80]);hero['expr']='worried';hero['head']=-5
  buddy=sit_pose(920);rest(buddy);hand(buddy,'left',[-90,-75]);rows.append(show_actor(im,hero));rows.append(show_actor(im,buddy,'friend'));sets.table(ImageDraw.Draw(im),810,430,330)
  g=ImageDraw.Draw(im);g.rectangle((850,444,1075,518),fill='#e3d4ae',outline='#756e54',width=3);txt(g,(873,465),'REST DESK',26);txt(g,(40,40),'IMAGINED',19)
  return im,rows,events
 if a=='write_note':
  poly(g,[(370,130),(904,147),(943,553),(328,539)],'#f0e3c3','#7d674c',5)
  full=['FIX PARAGRAPH','Tomorrow','After breakfast'];q=on(l,.10,1.1)
  for i,text in enumerate(full):txt(g,(415,210+i*110),text[:round(len(text)*max(0,min(1,q*3-i)))],35)
  if l<1.55:
   pt=np.array([430+340*((q*3)%1),247+110*min(2,int(q*3))]);withdraw=on(l,1.15,1.55);pt=mix(pt,[1030,100],withdraw);line(g,[pt+[100,-120],pt],INK,12);line(g,[pt,pt+[-12,35]],'#5a7163',6)
  return im,rows,[{'kind':'pen','phase':l}]
 if a in ['friend_rest','friend_kindness','leisure','boss','laundry','care']:
  if a=='laundry':
   buddy=walk_pose(370,710,l,1.6);rest(buddy);hand(buddy,'left',[-57,-25]);hand(buddy,'right',[57,-25]);center=np.asarray(buddy['hip'])+[0,0]
   def basket(m,c=center):
    q=ImageDraw.Draw(m);q.rounded_rectangle((c[0]-58,c[1]-22,c[0]+58,c[1]+48),8,fill='#a5b39c',outline='#596e61',width=4)
    for j in range(4):q.ellipse((c[0]-48+j*26,c[1]-35,c[0]-10+j*26,c[1]+5),fill=['#c18f76','#dbcb9f','#a5a1b5'][j%3])
   buddy['draws'].append(basket)
  elif a=='care':
   hero=sit_pose(790);rest(hero);hand(hero,'left',[-132,-70]);buddy=stand_pose(500);rest(buddy);hand(buddy,'right',mix([72,-6],[111,-24],on(l,.1,.6)));carry(buddy,'cup','right',props.mug,[0,17])
  else:
   buddy=sit_pose(620);buddy['view']='three_quarter';buddy['angle']=9 if a=='friend_rest' else 0;rest(buddy);hand(buddy,'right',[70,-85]);hand(buddy,'left',[-14,-48]);carry(buddy,'phone','right',props.phone,[0,-16]);buddy['head']=6*on(l,.1,.6)
  if a=='leisure':
   buddy['draws']=[];buddy['held']={};center=np.asarray(buddy['hip'])+[0,-33];buddy['wr']['left']=center+[-48,17];buddy['wr']['right']=center+[48,17];buddy['draws'].append(lambda m,c=center:props.book(m,c,1,on(l,.55,1.15)));buddy['held']={'book-left':{'arm':'left','point':buddy['wr']['left']},'book-right':{'arm':'right','point':buddy['wr']['right']}}
  if hero:rows.append(show_actor(im,hero))
  rows.append(show_actor(im,buddy,'friend'))
  if a=='boss':laptop(im)
  return im,rows,events
 if kitchen:
  x=650.;hero=stand_pose(x);rest(hero)
  if a=='hurry':hero=walk_pose(320,x,l,1.25);rest(hero)
  hero['head']=5;hero['expr']='worried' if a in ['almost_excuse','hurry','wash'] else 'normal';hero['angle']=5
  platecenter=np.array([x+22,388.]);leftgrip=platecenter+[-30,0]
  if a in ['wash','roommate_arrive','almost_excuse','faucet_off','honest','roommate_question'] or a=='hurry' and l>1.28:
   hand(hero,'left',leftgrip-np.asarray(hero['hip']));hand(hero,'right',[38,-30+4*math.sin(l*11)]);carry(hero,'plate','left',props.plate,[30,0]);water=True
   if a=='hurry':
    hero['wr']['left']=mix(np.asarray(hero['hip'])+[-68,-6],[x-80,412],on(l,1.28,1.6));hero['draws']=[];hero['held']={}
    if l<1.62:post.append(lambda m:props.plate(m,[x-50,412]))
    else:
     hero['wr']['left']=mix([x-80,412],leftgrip,on(l,1.65,2.15));carry(hero,'plate','left',props.plate,[30,0])
   if a=='faucet_off':
    hero['wr']['right']=mix(np.asarray(hero['hip'])+[38,-30],[x+125,398],on(l,.08,.48));water=l<.55
    hero['wr']['left']=mix(leftgrip,[x-75,421],on(l,.75,1.2));hero['draws']=[];hero['held']={}
    if l<1.22:carry(hero,'plate','left',props.plate,[30,0])
    else:post.append(lambda m:props.plate(m,[x-45,421]))
   if a in ['honest','roommate_question']:
    water=False;hero['draws']=[];hero['held']={};rest(hero);hero['expr']='relieved';hero['head']=-4+7*on(l,.1,.6);post.append(lambda m:props.plate(m,[x-45,421]))
  elif a!='hurry':
   hero['angle']=4;hand(hero,'left',[-52,-27]);hand(hero,'right',[60,-30]);center=np.asarray(hero['hip'])+[-35,-13]
   if a=='set_snack':
    hero['wr']['left']=mix(np.asarray(hero['hip'])+[-52,-27],[x-98,420],on(l,.05,.48))
    if l<.50:carry(hero,'bowl','left',bowl,[0,14])
    else:post.append(lambda m:bowl(m,[x-98,434]))
   else:
    hero['wr']['left']=mix([x-98,420],np.asarray(hero['hip'])+[-52,-27],on(l,.12,.58))
    if a=='dinner_done':carry(hero,'plate','left',props.plate,[30,0])
    else:carry(hero,'bowl','left',bowl,[0,14])
  if a in ['roommate_arrive','almost_excuse','faucet_off','honest','roommate_question']:
   buddy=walk_pose(1100,950,l,1.) if a=='roommate_arrive' else stand_pose(950);rest(buddy);buddy['head']=-5
   if a=='roommate_question':hand(buddy,'left',[-105,-74]);buddy['head']=-6+5*math.sin(min(l,1.2)*3)
   rows.append(show_actor(im,buddy,'friend'))
  rows.append(show_actor(im,hero));sink(im,x,water)
  # Repaint hand-owned props and distal forearms above the physical counter.
  for draw in hero['draws']:draw(im)
  for side in ['left','right']:
   ch=np.asarray(rows[-1]['arms'][side]);rig.limbline(ImageDraw.Draw(im),[mix(ch[1],ch[2],.55),ch[2]])
  for draw in post:draw(im)
  return im,rows,[{'kind':'water','active':water}]
 if desk:
  hero=sit_pose(620);rest(hero);hero['head']=5
  hand(hero,'left',[-14,-64]);hand(hero,'right',[83,-64])
  if a=='walk_pull':
   hero=walk_pose(300,620,l,1.35);rest(hero);hero['head']=4
   if l>1.4:hero['hip'][1]=418+62*on(l,1.4,1.85);hero['wr']={};rest(hero)
  elif a in ['typing_reply','file_check','inbox_overflow','reach_work']:
   hero['wr']['left']+=np.array([0,3*math.sin(l*15)]);hero['wr']['right']+=np.array([0,-3*math.sin(l*18)]);hero['head']=4+2*on(l,.1,.5)
  elif a=='close_laptop':
   lid=on(l,.18,.85);hero['angle']=4*math.sin(math.pi*lid);hero['wr']['right']=[750,280+166*lid];hero['head']=7
   if l>1.:hand(hero,'right',mix([130,-34],[72,-6],on(l,1.,1.4)))
  elif a in ['phone_reply','realize']:
   hand(hero,'right',[70,-85]);hand(hero,'left',[-14,-48]);carry(hero,'phone','right',props.phone,[0,-16]);hero['expr']='worried' if a=='realize' else 'normal';hero['head']=7-11*on(l,.5,1.1)
  elif a=='alarm_off':
   hero['wr']['right']=mix(np.asarray(hero['hip'])+[83,-64],[750,421],on(l,.1,.48));props.phone(im,[750,425],90)
  elif a in ['leave_desk','hover_couch']:
   rise=on(l,.15,.65);hero['hip'][1]=480-62*rise;hero['wr']={};rest(hero);hero['head']=-8*on(l,.1,.6)
  else:
   hero['expr']='worried';hero['head']=6-10*on(l,.4,.95);hero['angle']=-4*math.sin(math.pi*on(l,.2,.8))
   hand(hero,'right',mix([83,-64],[110,-100],on(l,.2,.55)*(1-on(l,1.,1.45))))
   if a=='useful_pause':hand(hero,'right',mix([90,-70],[72,-6],on(l,.4,1.0)))
  rows.append(show_actor(im,hero));laptop(im,'document' if a in ['file_check','urgent_done','close_laptop'] else 'email',l,lid)
  return im,rows,events
 # Living-room body performance, including explicit quick sit/rise and carried snack.
 hero=sit_pose();rest(hero);hero['head']=-3
 if a=='walk_snack':
  hero=walk_pose(350,850,l,1.5);rest(hero);hand(hero,'left',[-52,-27]);carry(hero,'bowl','left',bowl,[0,14])
 elif a=='sit_play':
  hero=stand_pose();hero['hip'][1]=418+62*on(l,.05,.45);rest(hero);hero['expr']='relieved'
  hand(hero,'left',[-52,-27]);hand(hero,'right',[70,-20])
  if l<.45:carry(hero,'bowl','left',bowl,[0,14])
  elif l<.8:
   hero['wr']['left']=mix(np.asarray(hero['hip'])+[-52,-27],BOWL-[0,14],on(l,.45,.78));carry(hero,'bowl','left',bowl,[0,14])
  else:hand(hero,'left',mix([-75,6],[-90,-4],on(l,.8,1.2)))
  if l>.45:
   hero['wr']['right']=mix(np.asarray(hero['hip'])+[70,-20],REMOTE+[0,10],on(l,.45,.78))
   if l>=.8:
    hero['wr']['right']=mix(REMOTE+[0,10],np.asarray(hero['hip'])+[70,-20],on(l,.8,1.));carry(hero,'remote','right',remote,[0,-10])
 elif a=='startle':
  hero['expr']='worried';hero['wr']['right']=mix(np.asarray(hero['hip'])+[70,-20],REMOTE+[0,10],on(l,.05,.35));hero['hip'][1]=480-62*on(l,.4,.9);hero['head']=-12*on(l,.05,.28)
  if l<.36:carry(hero,'remote','right',remote,[0,-10])
  if l>.4:rest(hero)
 elif a=='sit_back':
  hero=stand_pose();hero['hip'][1]=418+62*on(l,.05,.5);rest(hero);hero['expr']='relieved'
 elif a=='snack_grab':
  buddy=stand_pose(480);buddy['hip'][1]=418+62*on(l,.08,.35)*(1-on(l,.65,1.05));rest(buddy)
  hand(buddy,'right',mix([72,-6],[95,6],on(l,.1,.35)))
  if l>.45:
   hand(buddy,'right',mix([95,6],[73,-25],on(l,.5,.9)))
   if l>1.1:buddy=walk_pose(480,100,l-1.1,1.3);rest(buddy);hand(buddy,'right',[73,-25])
   c=buddy['wr']['right']+[0,-6];buddy['draws'].append(lambda m,c=c:ImageDraw.Draw(m).ellipse((c[0]-7,c[1]-7,c[0]+7,c[1]+7),fill='#e1c18b',outline='#6e6954'))
  rows.append(show_actor(im,buddy,'friend'))
 else:
  hand(hero,'right',[70,-20]);carry(hero,'remote','right',remote,[0,-10]);hero['expr']='worried' if a in ['couch_guilt','uneasy_movie','still_guilty'] else 'relieved' if a in ['watch','rest_end','stay'] else 'normal'
  if a in ['couch_guilt','uneasy_movie','still_guilty']:hand(hero,'left',mix([-68,-6],[-106,-80],on(l,.2,.55)*(1-on(l,1.2,1.6))))
  elif a=='find_place':
   hero['wr']['right']=mix(REMOTE+[0,10],np.asarray(hero['hip'])+[70,-20],on(l,.1,.55));hero['draws']=[];carry(hero,'remote','right',remote,[0,-10])
  else:hand(hero,'left',[-90,-4]);hero['head']=-2+3*on(l,.1,.7)
 if a in ['rest_end','stay','watch']:hero['hip'][1]+=.8*math.sin(l*2)
 rows.append(show_actor(im,hero))
 g=ImageDraw.Draw(im);poly(g,[(460,514),(710,514),(730,534),(444,534)],'#c7ad85','#6f6650',3)
 for xx in [466,704]:line(g,[(xx,533),(xx,644)],'#75674d',6)
 if (p>=11 and a!='walk_snack' and not(a=='sit_play' and l<.8)) or a=='uneasy_movie':bowl(im,BOWL)
 return im,rows,events
def frame(t,caption=True):
 i=max(0,min(len(SHOTS)-1,bisect.bisect_right(STARTS,t)-1));s=SHOTS[i];im,rows,events=scene(t,s)
 # Stable authored camera cuts preserve hand/foot geometry; no zoom-loop animation.
 if s['camera'] in ['face','buddy_face']:
  cx=950 if s['camera']=='buddy_face' else 650
  width,height,top=(768,432,30) if s['set']=='kitchen' else (672,378,120)
  left=max(0,min(1280-width,cx-width//2));box=(left,top,left+width,top+height)
  im=im.crop(box).resize((1280,720),Image.Resampling.LANCZOS)
 elif s['camera']=='plate':im=im.crop((470,240,1000,538)).resize((1280,720),Image.Resampling.LANCZOS)
 if s['paragraph']==2 and s['action']=='dinner_done':
  g=ImageDraw.Draw(im);g.rounded_rectangle((35,27,370,73),6,fill='#f1e3c5');txt(g,(49,36),'ONE HOUR EARLIER',23)
 if caption:
  j=bisect.bisect_right(CSTARTS,t)-1
  if j>=0 and t<CUES[j]['end']:
   if len(CR.cache)>12:CR.cache.clear()
   im=Image.alpha_composite(im,CR.raster(CUES[j]['text'])[0])
 return im.convert('RGB'),rows,events,s
