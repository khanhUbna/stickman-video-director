"""Gym museum film. Preview timing is explicitly provisional until real speech is aligned."""
from pathlib import Path
import json,math,bisect
from PIL import ImageDraw
import artwork as A
P=Path(__file__).resolve().parent
PERFORMANCE=json.loads((P/'performance.json').read_text())
ACTUAL=(P/'timing.json').exists() and (P/'turns.json').exists()
if ACTUAL:T=json.loads((P/'timing.json').read_text());TURNS=json.loads((P/'turns.json').read_text())
else:
 TURNS=[];cursor=0
 for si,s in enumerate(PERFORMANCE):
  for li,r in enumerate(s['lines']):
   dur=max(.8,len(r['text'].split())/2.7);TURNS.append(dict(r,scene=si,line=li,id=f's{si+1:02d}-l{li+1:02d}',start=cursor,end=cursor+dur));cursor+=dur+(.9 if li==len(s['lines'])-1 else .32)
 T={'duration':cursor+1,'fps':30,'timing_basis':'provisional word-count planning, NOT actual speech'}
MODES=[
 ['opening','dig'],
 ['dig','vale','mina','bar','office','vale','banner','mina','vale'],
 ['bench','bench','vale','mina','handshake','vale','entry','mina','rewind'],
 ['receipt','receipt','mina','vale','mina','fineprint','banner','mina'],
 ['progress','mina','progress','mina','adaptation','vale','progress','painstop','mina'],
 ['belt','vale','mina','cardio','vale','mina','move_machine'],
 ['stage','stage','run','safety','clip','walk','walk','reaction'],
 ['vale','robot','mina','robot','stimulus','mina','screen'],
 ['outside','function','vale','mina','decision','correct'],
 ['correct','vale','mina','office','member','clerk','member','clerk','member','clerk','oldsign'],
 ['exhibit','reveal','mina','ending']]
assert [len(x) for x in MODES]==[len(x['lines']) for x in PERFORMANCE]
SHOTS=[]
for i,r in enumerate(TURNS):
 end=TURNS[i+1]['start'] if i+1<len(TURNS) else T['duration'];mode=MODES[r['scene']][r['line']];n=max(1,math.ceil((end-r['start'])/4.8))
 for j in range(n):SHOTS.append({'id':f'{r["id"]}-v{j+1}','turn':i,'scene':r['scene'],'mode':mode,'start':r['start']+(end-r['start'])*j/n,'end':r['start']+(end-r['start'])*(j+1)/n,'part':j,'parts':n})
STARTS=[s['start'] for s in SHOTS]
def tag(c,text,color=A.TEAL):c.rect((42,26,345,76),color,None,r=8);c.text(61,35,text,21,'#fff8e7')
def caption(im,text):
 d=ImageDraw.Draw(im);f=A.font(42);b=d.textbbox((0,0),text,font=f);w=b[2]-b[0]
 if w>1770:raise ValueError(('caption too wide',text,w))
 d.rounded_rectangle((960-w/2-24,968,960+w/2+24,1044),13,'#fff5dc',outline=A.INK,width=2);d.text((960-w/2,980),text,font=f,fill=A.INK)
def archive(c,text='RESTORED RECORDING'):
 tag(c,text,'#5c706d');c.line([(30,98),(30,650),(1245,650),(1245,99)],'#e0e7d3',2)
def card(c,tiny=False):
 c.rect((390,168,899,510),'#fff8dd',r=22,w=5)
 if tiny:
  c.text(644,205,'TERMS & CONDITIONS',30,anchor='mt')
  for i in range(10):c.line([(432,276+i*17),(846-(i%3)*28,276+i*17)],'#aa9c83',2)
 else:
  c.text(644,214,'MEMBERSHIP',40,anchor='mt');c.text(644,288,'PAID',60,A.TEAL,anchor='mt');c.text(644,393,'MONTHLY RENEWAL',22,anchor='mt')
def view(mode,t,u=0,speaking='',scene=0,line=0,part=0,local=0):
 # Every family has a contextual wide and an authored reaction/insert, not a camera-only replacement for acting.
 kind='dig';camera=(1,0,0)
 if mode in ['opening','banner','stage','run','safety','clip','walk','reaction','decision','screen']:kind='stage'
 if mode in ['correct','exhibit']:kind='museum'
 if mode in ['office','clerk','member','reveal','ending','oldsign']:kind='office'
 if mode in ['adaptation','cardio','robot','stimulus','function']:kind='diagram'
 if mode in ['receipt','fineprint']:kind='locker'
 if mode=='entry':kind='door'
 if mode in ['vale','mina']:
  if scene in [6,7,8]:kind='stage'
  if scene in [9,10]:kind='museum'
  target=410 if mode=='vale' else 880;camera=(1.4,max(0,target-430),120)
 if mode=='outside':kind=['steps','park','door'][part%3]
 if mode in ['progress','painstop','bench','handshake','rewind']:kind='archive'
 c=A.C(camera);A.background(c,kind,t,title='HUMANS PAID TO BE TORTURED' if scene in [3,6,8] and kind=='stage' else '')
 valeTalk=speaking=='VALE';minaTalk=speaking=='MINA'
 def vale(x=410,action='stand',mood='confident',**kw):return A.person(c,x=x,t=t,role='VALE',action=action,talk=valeTalk,mood=mood,u=u,**kw)
 def mina(x=880,action='hold',mood='neutral',**kw):return A.person(c,x=x,t=t,role='MINA',action=action,talk=minaTalk,mood=mood,u=u,**kw)
 if mode=='opening':
  if u<.45:
   A.treadmill(c,690,640,t);vale(625,'panic','worried');c.text(1080,379,'ON AIR',23,'#b35653',anchor='mt');c.text(1080,419,'02:00',44,anchor='mt')
  elif u<.72:vale(555,'panic','surprised');c.text(830,423,'REHEARSAL',27,anchor='mt')
  else:
   x=max(700,1200-135*local);mina(x,'run' if x>700 else 'stand','worried',walk_speed=-135);c.rect((x+60,475,x+138,523),'#fff6d8',r=4);c.text(x+66,482,'MANUAL',12)
 elif mode=='dig':
  A.treadmill(c,740,640,t);vale(450,'reach' if part%2 else 'point');mina(1080,'read',prop='tablet');tag(c,'3026 · EXCAVATION')
  if scene==0:tag(c,'TWO HOURS EARLIER')
 elif mode=='vale':
  A.weight(c,750,555,220);vale(410,'think' if line%3==0 else 'shrug' if line%3==1 else 'point','worried' if scene>=6 else 'confident');mina(1000,'read',prop='tablet')
 elif mode=='mina':
  vale(340,'think','worried' if scene>3 else 'confident');mina(880,'point' if line%2 else 'shrug','confident')
 elif mode=='bar':
  A.weight(c,650,480+30*math.sin(t*1.6),320);c.rect((435,520,870,542),'#b7a48a',r=5);c.line([(465,540),(445,650)],w=8);c.line([(839,540),(860,650)],w=8);vale(245,'point');tag(c,'NO PRODUCT?')
 elif mode in ['office','reveal','ending']:
  if mode=='office':
   c.text(644,255,'A DESK. TWO CHAIRS.',22,anchor='mt');A.person(c,1040,ground=646,t=t,role='CLERK',action='read',prop='card');c.rect((455,418,1146,449),'#c5aa83',r=6)
  else:
   c.rect((354,72,1106,166),'#e8ba73',r=10,w=5);c.text(730,91,'TORTURE CHAMBER',38,anchor='mt');vale(290,'stand','happy');mina(1110,'stand','happy');tag(c,'MUSEUM · OPENING DAY')
 elif mode=='banner':
  vale(440,'point');mina(980,'think','worried');c.text(640,208,'LIVE DEMONSTRATION TODAY',25,'#fff2cd',anchor='mt');c.line([(185,83),(185,39)],A.INK,5);c.line([(1111,83),(1111,39)],A.INK,5)
 elif mode in ['bench','handshake','rewind']:
  archive(c);A.bench(c,t,A.smooth((local%2.6)/2.6));A.person(c,1030,t=t,role='COACH',action='point',talk=speaking=='COACH',mood='confident')
  if mode=='rewind':c.text(1015,112,'◀◀',35,'#fff8df',anchor='mt')
  if mode=='handshake':
   # Following shot: secure bar and two people meet at a common hand endpoint.
   A.background(c,'archive',t);archive(c);A.weight(c,310,395,205)
   g=A.smooth(min(1,u/.25))*(1-A.smooth(max(0,(u-.8)/.2)));meet=(760,477+5*math.sin(local*8));h1=(A.lerp(698,meet[0],g),A.lerp(553,meet[1],g));h2=(A.lerp(822,meet[0],g),A.lerp(553,meet[1],g));A.person(c,645,t=t,role='MEMBER',action='stand',hand=h1,mood='happy');A.person(c,875,t=t,role='COACH',action='stand',left=h2,mood='happy')
 elif mode=='entry':
  speed=72 if part%2==0 else -72;x=(360 if part%2==0 else 800)+speed*(local%4.8);A.person(c,x,t=t,role='MEMBER',action='walk',walk_speed=speed,mood='happy');c.text(980,385,'ENTER · LEAVE · RETURN',19,anchor='mt');archive(c)
 elif mode in ['receipt','fineprint']:
  if part==0 and mode=='receipt':vale(420,'read','surprised',prop='card');mina(890,'point')
  else:card(c,mode=='fineprint')
  if mode=='fineprint':card(c,True)
 elif mode in ['progress','painstop','adaptation']:
  if mode=='adaptation':
   A.person(c,590,t=t,role='MEMBER',action='lift',u=.5+.45*math.sin(t*1.6));c.text(640,195,'TRAIN → RECOVER → ADAPT',27,anchor='mt');c.text(1028,428,'OVER TIME',23,anchor='mt');c.line([(867,495),(1012,495)],A.TEAL,7);c.poly([(1010,482),(1034,495),(1010,508)],A.TEAL,None)
  else:
   archive(c,'TRAINING RECORD');phase=(.5+.5*math.sin(t*1.8));A.bench(c,t,phase);A.person(c,1060,t=t,role='COACH',action='point' if mode=='progress' else 'panic',mood='worried' if mode=='painstop' else 'happy');c.text(570,125,'LATER · SAME EXERCISE' if part%2 else 'FIRST SESSION · START SMALL',22,anchor='mt')
   if mode=='painstop':c.rect((450,182,857,251),'#fff4db',r=7);c.text(654,194,'PAIN? STOP & ADJUST',24,'#a45749',anchor='mt')
 elif mode=='belt':
  archive(c);A.treadmill(c,685,640,t,True);A.person(c,610,ground=640,t=t,role='MEMBER',action='belt',mood='happy')
 elif mode=='move_machine':
  xx=510+min(3,local)*70;A.treadmill(c,xx,640,t,False);A.person(c,xx-190,t=t,role='COACH',action='walk' if local<3 else 'stand',walk_speed=70,hand=(xx-66,476));mina(1090,'read',prop='card');c.text(480,105,'TO THE STAGE',25,anchor='mt')
 elif mode=='cardio':
  A.treadmill(c,600,640,t,True);A.person(c,540,ground=640,t=t,role='MEMBER',action='belt')
  c.ell((848,270,960,382),'#d9816f');c.text(905,300,'HEART',19,'#fff8df',anchor='mt');c.text(1015,455,'BREATHING',20,anchor='mt');c.line([(822,390),(1030,390)],A.TEAL,5)
 elif mode in ['stage','run','safety','clip','walk','reaction','decision','screen']:
  walking=mode in ['walk','reaction','decision'];A.treadmill(c,675,640,t,walking)
  if mode in ['stage','walk','reaction','decision','screen']:
   if walking:
    vale(610,'belt','worried' if mode=='reaction' else 'neutral',ground=640,hand=(710,477) if mode=='walk' else None,left=(570,477) if mode=='walk' else None)
   else:vale(610,'panic' if mode=='stage' and line==1 else 'stand','confident',ground=640)
   mina(975,'point' if mode in ['screen','decision'] else 'hold',prop='tablet' if mode=='screen' else None)
  elif mode=='run':
   vale(610,'stand',ground=640);mina(max(810,1215-135*local),'run' if local<3 else 'stand','worried',walk_speed=-135)
  else:
   vale(610,'stand','worried',ground=640)
   # Clip reaches Vale's chest; then Mina releases it and touches the actual stop/start control.
   chest=(625,433);button=(795,419);alpha=A.smooth(min(1,u*2));endpoint=(A.lerp(745,chest[0],alpha),A.lerp(520,chest[1],alpha))
   if u>.68:endpoint=(A.lerp(chest[0],button[0],A.smooth((u-.68)/.32)),A.lerp(chest[1],button[1],A.smooth((u-.68)/.32)))
   if u>.4:c.line([chest,(700,505),button],'#b75d54',3);c.rect((chest[0]-5,chest[1]-5,chest[0]+5,chest[1]+5),'#d95b50',r=2,w=1)
   mina(780,'stand','neutral',left=endpoint)
  if mode=='decision':
   c.rect((1046,496,1153,535),'#b75b57',r=5);c.text(1100,503,'END LIVE',13,'#fff4e0',anchor='mt')
 elif mode in ['robot','stimulus']:
  vale(310,'think','surprised');A.robot(c,690,645,t,.5+.5*math.sin(local*2.1));mina(1080,'point');c.text(620,193,'WHO DOES THE WORK?',29,anchor='mt')
  if mode=='stimulus':c.line([(808,457),(1000,457)],A.TEAL,5);c.text(1050,330,'LOAD',22,anchor='mt');c.text(320,270,'OBSERVER',20,anchor='mt')
 elif mode=='outside':
  if part%3==0:
   # Walking up a shallow step sequence, with actual supported foot heights.
   A.person(c,640,ground=620,t=t,role='MEMBER',action='walk',walk_speed=65,prop=None);c.rect((703,550,744,602),'#bb9065',r=6);c.line([(712,551),(714,533),(735,533),(737,551)],w=3)
  elif part%3==1:
   xx=360+45*(local%4.8);A.person(c,xx,t=t,role='MEMBER',action='walk',walk_speed=45,mood='happy');A.person(c,xx+260,t=t,role='MINA',action='walk',walk_speed=45,mood='happy')
  else:A.person(c,810,t=t,role='COACH',action='point',mood='happy');A.person(c,300+65*(local%4.8),t=t,role='MEMBER',action='walk',walk_speed=65,mood='happy')
  archive(c,'LIFE OUTSIDE THE GYM')
 elif mode=='function':
  A.person(c,400,t=t,role='MEMBER',action='lift',u=.5+.45*math.sin(t*1.7));c.text(820,300,'HOME · OUTDOORS · GYM',25,anchor='mt');c.text(820,376,'DIFFERENT PEOPLE,',23,anchor='mt');c.text(820,412,'DIFFERENT NEEDS',23,anchor='mt')
 elif mode in ['correct','exhibit']:
  A.treadmill(c,675,640,t);vale(320,'hold','neutral',prop='card');mina(1015,'point','happy');c.text(640,210,'GYM',64,'#fff3d9',anchor='mt')
  if mode=='correct':c.text(641,284,'EVIDENCE FIRST',22,'#e2dcb8',anchor='mt')
 elif mode in ['clerk','member']:
  A.person(c,925,ground=644,t=t,role='CLERK',action='shrug' if line%2 else 'read',talk=speaking=='CLERK',prop='card' if line%2==0 else None)
  c.rect((455,418,1146,449),'#c5aa83',r=6);c.rect((478,449,1121,623),'#9d7e66',r=5)
  A.person(c,350,t=t,role='MEMBER',action='shrug' if line>5 else 'read',talk=speaking=='MEMBER',mood='worried',prop='card' if line<6 else None)
  archive(c,'FINAL RECOVERED RECORDING')
 elif mode=='oldsign':
  vale(330,'reach','surprised');c.rect((473,475,1040,570),'#e8ba73',r=10);c.text(751,493,'TORTURE CHAMBER',31,anchor='mt')
 return c.im
CUES=[]
if ACTUAL and (P/'captions.json').exists():CUES=json.loads((P/'captions.json').read_text())
CSTART=[x['start'] for x in CUES]
def frame(t,captions=True):
 s=SHOTS[max(0,bisect.bisect_right(STARTS,t)-1)];r=TURNS[s['turn']];u=max(0,min(1,(t-r['start'])/max(.1,r['end']-r['start'])));im=view(s['mode'],t,u,r['speaker'] if t<r['end'] else '',r['scene'],r['line'],s['part'],t-r['start'])
 if captions and CUES:
  k=bisect.bisect_right(CSTART,t)-1
  if k>=0 and t<CUES[k]['end']:caption(im,CUES[k]['text'])
 return im,s
if __name__=='__main__':
 name='timeline.json' if ACTUAL else 'preview-timeline.json';(P/name).write_text(json.dumps({'duration':T['duration'],'actual_audio_timing':ACTUAL,'width':1920,'height':1080,'fps':30,'shots':SHOTS},indent=2)+'\n');print(len(SHOTS),'shots',round(T['duration'],1),'seconds',name)
