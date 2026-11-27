"""Full original2D science comedy, timed to actual accepted/native speech."""
from pathlib import Path
import json,bisect,math,re
from PIL import ImageDraw
import artwork as A
P=Path(__file__).resolve().parent
T=json.loads((P/'timing.json').read_text());TURNS=json.loads((P/'turns.json').read_text());WORDS=json.loads((P/'words.json').read_text());CUES=json.loads((P/'captions.json').read_text());LEVELS=json.loads((P/'mouth-levels.json').read_text())
BY={(r['scene'],r['line']):r for r in TURNS};WBY={r['id']:[w for w in WORDS if w['turn']==r['id']] for r in TURNS};SCENE_START={i:min(r['start'] for r in TURNS if r['scene']==i) for i in range(11)}
def mark(r,phrase):
 words=WBY[r['id']];a=[re.sub('[^a-z0-9]','',x['text'].lower()) for x in words];b=[re.sub('[^a-z0-9]','',x.lower()) for x in phrase.split()]
 for k in range(len(a)-len(b)+1):
  if a[k:k+len(b)]==b:return words[k]['start']
 raise ValueError(('missing cue phrase',r['id'],phrase))
# Each alternative is a meaningful principal-picture/action change, not a crop-only filler.
DIRECT={
(0,0):[('teaser-stage',None),('rehearsal','He has rehearsed'),('manual','He has not'),('teaser-run','Mina has')],(0,1):[('timejump',None)],
(1,0):[('dig-establish',None),('dig-room','Under an old'),('pull-machine','There are handles'),('bench','and benches')],(1,1):[('vale',None)],(1,2):[('mina',None)],(1,3):[('weight-task',None)],(1,4):[('empty-office',None),('office-detail','A desk')],(1,5):[('vale',None)],(1,6):[('phone',None),('banner-raise','A banner'),('banner','ANCIENT CRUELTY')],(1,7):[('mina',None)],(1,8):[('vale',None)],
(2,0):[('archive-console',None),('bench','A man lies'),('coach','Another man')],(2,1):[('coach',None)],(2,2):[('vale',None)],(2,3):[('mina',None)],(2,4):[('rack-bar',None),('handshake','The two men')],(2,5):[('vale',None)],(2,6):[('archive-console',None),('entry','People enter'),('exit','They leave'),('return-shoes','One comes back')],(2,7):[('mina',None)],(2,8):[('rewind',None)],
(3,0):[('locker-find',None),('receipt','Vale stops'),('read-price','He reads')],(3,1):[('paid-reaction',None)],(3,2):[('mina',None)],(3,3):[('vale',None)],(3,4):[('mina',None)],(3,5):[('card-flip',None),('fineprint','There is'),('photograph','Vale takes')],(3,6):[('headline',None)],(3,7):[('mina',None)],
(4,0):[('records',None),('remove-plate','On the first'),('progress-later','On a later')],(4,1):[('mina',None)],(4,2):[('progress-later',None)],(4,3):[('mina',None)],(4,4):[('resistance',None),('rest','Repeated training'),('add-plate','As capacity'),('calendar','Progress takes')],(4,5):[('weights',None)],(4,6):[('load-compare',None)],(4,7):[('pain-stop',None),('band-exercise','and changing')],(4,8):[('mina',None)],
(5,0):[('belt',None)],(5,1):[('vale',None)],(5,2):[('belt-control',None)],(5,3):[('cardio',None),('training-days','Regular aerobic'),('belt','Moving across')],(5,4):[('vehicle-paradox',None)],(5,5):[('mina',None)],(5,6):[('wheel-machine',None),('card-read','Mina stays')],
(6,0):[('stage-wide',None),('stage-banner','The banner'),('stage-step','Vale steps'),('stage-hand','He raises')],(6,1):[('stage-speech',None)],(6,2):[('stage-run',None)],(6,3):[('stage-warning',None)],(6,4):[('stage-stop',None),('stage-clip','attaches'),('stage-start','starts'),('stage-walk','Vale grips'),('stage-feet','He takes')],(6,5):[('stage-question',None)],(6,6):[('stage-reply',None)],(6,7):[('stage-reaction',None),('stage-headline','Behind him')],
(7,0):[('stage-question',None)],(7,1):[('robot-pickup',None),('robot-lift','A museum robot')],(7,2):[('mina',None)],(7,3):[('arm-look',None)],(7,4):[('robot-versus-body',None),('body-work','Exercise asks')],(7,5):[('mina',None)],(7,6):[('screen-switch',None)],
(8,0):[('groceries',None),('park','The woman'),('door-hold','The coach')],(8,1):[('everyday',None),('home-exercise','A gym is')],(8,2):[('vale',None)],(8,3):[('mina',None)],(8,4):[('live-evidence',None),('broadcast-hand','Vale reaches'),('stop-machine','Instead')],(8,5):[('correct',None)],
(9,0):[('correct',None),('card-exhibit','Mina puts')],(9,1):[('vale',None)],(9,2):[('fineprint',None)],(9,3):[('archive-console',None),('office-approach','The member')],(9,4):[('member',None)],(9,5):[('clerk',None)],(9,6):[('member',None)],(9,7):[('clerk',None)],(9,8):[('member',None)],(9,9):[('clerk',None)],(9,10):[('sign-pickup',None)],
(10,0):[('museum-visitors',None),('empty-office','At the back')],(10,1):[('sign-mount',None)],(10,2):[('ending-mina',None)],(10,3):[('ending',None)]}
SHOTS=[]
for index,r in enumerate(TURNS):
 end=TURNS[index+1]['start'] if index+1<len(TURNS) else T['duration'];entries=DIRECT[(r['scene'],r['line'])];points=[r['start'] if phrase is None else mark(r,phrase) for mode,phrase in entries]
 for k,(mode,_) in enumerate(entries):
  start=points[k];stop=points[k+1] if k+1<len(points) else end
  count=max(1,math.ceil((stop-start)/4.6))
  for part in range(count):SHOTS.append({'id':f'{r["id"]}-{k+1:02d}-{part+1:02d}','turn':index,'scene':r['scene'],'line':r['line'],'mode':mode,'start':start+(stop-start)*part/count,'end':start+(stop-start)*(part+1)/count,'part':part,'parts':count,'action_start':start,'action_end':stop})
STARTS=[s['start'] for s in SHOTS];CSTART=[c['start'] for c in CUES]
def energy(t,role):
 r=next((r for r in TURNS if r['start']<=t<=r['end']),None)
 return LEVELS[min(len(LEVELS)-1,int(t*30))] if r and r['speaker']==role else False

def frame(t,captions=True):
 import scenes
 s=SHOTS[max(0,bisect.bisect_right(STARTS,t)-1)];r=TURNS[s['turn']];im=scenes.draw(t,s,r)
 if captions:
  i=bisect.bisect_right(CSTART,t)-1
  if i>=0 and t<CUES[i]['end']:
   cue=CUES[i];d=ImageDraw.Draw(im);f=A.font(42);bb=d.textbbox((0,0),cue['text'],font=f);w=bb[2]-bb[0];assert w<1720,(cue['text'],w)
   box=(960-w/2-27,969,960+w/2+27,1045);d.rounded_rectangle(box,12,'#fff6e1',outline=A.INK,width=2);col={'NARRATOR':A.TEAL,'VALE':'#795a83','MINA':A.ORANGE}.get(cue['role'],'#526c84');d.rounded_rectangle((box[0]+5,976,box[0]+11,1038),3,col);d.text((960-w/2,981),cue['text'],font=f,fill=A.INK)
 return im,s
if __name__=='__main__':
 (P/'timeline.json').write_text(json.dumps({'duration':T['duration'],'resolution':[1920,1080],'fps':30,'shots':SHOTS},indent=2)+'\n');print('Native shots:',len(SHOTS),'duration',T['duration'])
