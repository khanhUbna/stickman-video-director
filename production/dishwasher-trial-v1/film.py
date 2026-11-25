"""Native landscape film. Timing follows actual authorized role recordings."""
from pathlib import Path
import json,math,bisect
from PIL import Image,ImageDraw
import artwork as A
P=Path(__file__).resolve().parent;T=json.loads((P/'timing.json').read_text());TURNS=json.loads((P/'turns.json').read_text());WORDS=json.loads((P/'words.json').read_text());STARTS=[r['start'] for r in TURNS]
# Different contextual views per authored utterance, not a repeated talking presenter.
MODES={0:['bowl','court','court','judge','court','court'],1:['sink','sink','court','manual','manual','judge','court'],2:['water','water','court'],3:['load','nest','court','nest','nest'],4:['judge','arm','arm','court','filter'],5:['filter','court','court','judge','manual'],6:['care','arrange','judge'],7:['verdict','judge','court','court']}
SHOTS=[]
for k,r in enumerate(TURNS):
 end=TURNS[k+1]['start'] if k+1<len(TURNS) else T['duration'];n=max(1,math.ceil((end-r['start'])/4.8));mode=MODES[r['scene']][r['line']]
 for j in range(n):
  start=r['start']+(end-r['start'])*j/n;stop=r['start']+(end-r['start'])*(j+1)/n
  view=mode
  if mode=='care':view=['care','filter','load','manual'][j%4]
  if mode=='water' and r['line']==1 and j==n-1:view='sink'
  if mode=='manual' and r['scene']==5 and j%2:view='court'
  if mode=='sink' and j%2:view='sink'
  cam=(1.,0.,0.)
  if view=='court':
   cam=(1.58,220,220) if r['speaker'] in ['SAM','NARRATOR'] else (1.6,540,220)
   if r['scene']==0 and r['line']==1:cam=(2.05,255,255)
   if r['scene']==0 and r['line']==2:cam=(1.95,540,235)
  if view=='judge':cam=(1.9,735,255)
  if view=='sink' and j%2:cam=(1.5,210,230)
  if view=='verdict' and j:cam=(1.5,210,220)
  SHOTS.append({'id':f'{r["id"]}-{j+1:02d}','turn':k,'scene':r['scene'],'mode':view,'camera':cam,'start':start,'end':stop,'part':j,'parts':n})
SHOTSTART=[s['start'] for s in SHOTS]
# Semantic cues preserve full canonical text; phrase splits honor punctuation and grammatical units.
CUES=[]
def split_semantic(ww):
 text=' '.join(w['text'] for w in ww)
 if len(text)<=44:return [ww]
 options=[]
 for k in range(2,len(ww)-1):
  left=' '.join(w['text'] for w in ww[:k]);right=' '.join(w['text'] for w in ww[k:])
  if len(left)>44:continue
  balance=abs(len(left)-min(44,len(right)))
  bonus=12 if ww[k]['text'].lower().strip(',') in ['through','before','after','with','because','and','but','from','while','when','then','instead'] else 0
  penalty=25 if ww[k-1]['text'].lower() in ['a','an','the','of','to','with','at','for','by','and','or'] else 0
  options.append((balance+penalty-bonus,k))
 if not options:
  k=max(1,len(ww)//2)
 else:k=min(options)[1]
 return [ww[:k]]+split_semantic(ww[k:])
for turn in TURNS:
 ww=[w for w in WORDS if w['turn']==turn['id']];sentences=[];group=[]
 for w in ww:
  group.append(w)
  if w['text'][-1:] in ['.','?','!']:sentences.extend(split_semantic(group));group=[]
 if group:sentences.extend(split_semantic(group))
 for g in sentences:CUES.append({'text':' '.join(w['text'] for w in g),'start':g[0]['start'],'end':min(turn['end']+.07,g[-1]['end']+.17),'role':turn['speaker']})
for a,b in zip(CUES,CUES[1:]):a['end']=min(a['end'],b['start']-.002)
CSTART=[c['start'] for c in CUES]
def stamp(t):
 n=round(t*1000);return f'{n//3600000:02d}:{n//60000%60:02d}:{n//1000%60:02d},{n%1000:03d}'
def frame(t,captions=True):
 s=SHOTS[max(0,bisect.bisect_right(SHOTSTART,t)-1)];r=TURNS[s['turn']];u=(t-r['start'])/max(.1,r['end']-r['start']);u=max(0,min(1,u));local=t-r['start'];mode=s['mode'];cam=s['camera'];speaking=r['speaker'] if t<r['end'] else ''
 # Physical actions use decisive subsecond changes with time reserved for readable outcome.
 v=u
 if mode=='arm':
  if r['line']!=1:v=.92
  else:
   # Actual word timings: gently1.72s, bumps4.18s, moves7.50s, turns8.74s.
   if local<1.72:v=0
   elif local<4.18:v=.2*(local-1.72)/(4.18-1.72)
   elif local<7.50:v=.2
   elif local<8.74:v=.38+.35*(local-7.50)/(8.74-7.50)
   else:v=.74+.26*min(1,(local-8.74)/.66)
 if mode=='nest':v=max(0,min(1,(local-.3)/1.4)) if r['line']==4 else .1
 if mode=='filter':v=max(0,min(1,local/1.1))
 clean=r['scene']==7 or (r['scene']==6 and mode=='filter')
 phase=6
 if mode=='water':
  if r['line']==0:
   phase=0
   keys={'pump':1,'spray':2,'filtered':3,'hot':4,'later':5,'fresh':6}
   for w in WORDS:
    if w['turn']==r['id'] and w['start']<=t:
     key=w['text'].lower().strip('.,!?')
     if key in keys:phase=keys[key]
  else:phase=7
 im=A.scene_frame(mode,t,v,speaking,clean,camera=cam,beat=local,phase=phase)
 d=ImageDraw.Draw(im)
 # Caption transform is always native screen-space, independent of action camera.
 if captions:
  idx=bisect.bisect_right(CSTART,t)-1
  if idx>=0 and CUES[idx]['start']<=t<=CUES[idx]['end']:
   c=CUES[idx];f=A.font(40,1.5);bbox=d.textbbox((0,0),c['text'],font=f);width=bbox[2]-bbox[0];assert width<1790,(c['text'],width)
   y=993;pad=22;d.rounded_rectangle((960-width/2-pad,y-12,960+width/2+pad,y+75),radius=10,fill='#fff8e8',outline='#d3c4a7',width=2);d.text((960-width/2,y),c['text'],font=f,fill=A.INK)
 return im,s
if __name__=='__main__':
 (P/'timeline.json').write_text(json.dumps({'duration':T['duration'],'width':1920,'height':1080,'fps':30,'shots':SHOTS},indent=2)+'\n');(P/'captions.json').write_text(json.dumps(CUES,indent=2)+'\n');(P/'captions-en.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["text"]}' for i,c in enumerate(CUES))+'\n')
 print('shots',len(SHOTS),'captions',len(CUES),'duration',T['duration'])
