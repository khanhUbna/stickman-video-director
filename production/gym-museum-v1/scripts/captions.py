from pathlib import Path
import json,re
P=Path(__file__).resolve().parents[1]
words=json.loads((P/'words.json').read_text());turns=json.loads((P/'turns.json').read_text());out=[]
def split(ww):
 if len(' '.join(w['text'] for w in ww))<=44:return [ww]
 options=[]
 for i in range(2,len(ww)-1):
  left=' '.join(w['text'] for w in ww[:i]);right=' '.join(w['text'] for w in ww[i:])
  if len(left)>44:continue
  penalty=22 if ww[i-1]['text'].lower().strip(',') in ['the','a','an','to','of','for','with','and','or'] else 0
  bonus=12 if ww[i]['text'].lower().strip(',') in ['but','and','because','while','when','then','before','after','instead','with'] else 0
  options.append((abs(len(left)-min(44,len(right)))+penalty-bonus,i))
 k=min(options)[1] if options else max(1,len(ww)//2)
 return [ww[:k]]+split(ww[k:])
for r in turns:
 ww=[w for w in words if w['turn']==r['id']];sent=[]
 for w in ww:
  sent.append(w)
  if w['text'][-1:] in ['.','?','!']:
   # Dr. is part of a name, not the end of a sentence.
   if w['text']=='Dr.':continue
   for a in split(sent):out.append({'text':' '.join(x['text'] for x in a),'start':a[0]['start'],'end':min(r['end']+.07,a[-1]['end']+.17),'role':r['speaker']})
   sent=[]
 if sent:
  for a in split(sent):out.append({'text':' '.join(x['text'] for x in a),'start':a[0]['start'],'end':min(r['end']+.07,a[-1]['end']+.17),'role':r['speaker']})
for a,b in zip(out,out[1:]):a['end']=min(a['end'],b['start']-.002)
assert all(x['end']>x['start']>=0 for x in out)
assert ' '.join(x['text'] for x in out).split()==(P/'script-en.txt').read_text().split()
def stamp(t):
 n=round(t*1000);return f'{n//3600000:02d}:{n//60000%60:02d}:{n//1000%60:02d},{n%1000:03d}'
(P/'captions.json').write_text(json.dumps(out,indent=2)+'\n');(P/'captions-en.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["text"]}' for i,c in enumerate(out))+'\n');print('Cues',len(out))
