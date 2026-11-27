from pathlib import Path
import json,re,math
import numpy as np,subprocess
from PIL import ImageFont
P=Path(__file__).resolve().parents[1];ROOT=P.parents[1];font=ImageFont.truetype(str(ROOT/'skills/directing-stickman-videos/assets/fonts/NotoSans.ttf'),42)
ww=json.loads((P/'words.json').read_text());turns=json.loads((P/'turns.json').read_text());T=json.loads((P/'timing.json').read_text());out=[]
def width(words):return font.getlength(' '.join(w['text'] for w in words))
def split(words):
 if width(words)<1660:return [words]
 opts=[]
 for k in range(2,len(words)-1):
  if width(words[:k])>1660:continue
  tail=words[k-1]['text'].lower().strip(',.;:');nextword=words[k]['text'].lower().strip(',.;:')
  penalty=70 if tail in ['a','an','the','of','to','for','with','and','or','at','from','its','your','their'] else 0
  bonus=30 if words[k-1]['text'][-1:] in ',;:' else 0
  if nextword in ['and','but','because','although','when','while','instead','then']:bonus+=20
  opts.append((abs(width(words[:k])-min(1400,width(words[k:])))+penalty-bonus,k))
 k=min(opts)[1] if opts else len(words)//2
 return [words[:k]]+split(words[k:])
for r in turns:
 words=[w for w in ww if w['turn']==r['id']];group=[]
 def emit(group):
  for g in split(group):out.append({'text':' '.join(x['text'] for x in g),'start':g[0]['start'],'end':min(r['end']+.10,g[-1]['end']+.18),'role':r['speaker'],'turn':r['id']})
 for w in words:
  group.append(w)
  if w['text'][-1:] in '.?!' and w['text']!='Dr.':emit(group);group=[]
 if group:emit(group)
for a,b in zip(out,out[1:]):a['end']=min(a['end'],b['start']-.002)
assert all(x['end']>x['start']>=0 for x in out)
assert ' '.join(x['text'] for x in out).split()==(P/'script-en.txt').read_text().split()
def stamp(t):
 n=round(t*1000);return f'{n//3600000:02d}:{n//60000%60:02d}:{n//1000%60:02d},{n%1000:03d}'
def save(name,cues):
 (P/name).write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["text"]}' for i,c in enumerate(cues))+'\n')
(P/'captions.json').write_text(json.dumps(out,indent=2)+'\n');save('captions-en.srt',out)
vi=json.loads((P/'performance-vi.json').read_text());vc=[]
for r in turns:
 text=vi[r['scene']]['lines'][r['line']]['text'];clauses=[s.strip() for s in re.findall(r'[^.!?]+[.!?]?',text) if s.strip()];weight=sum(len(s) for s in clauses);cursor=r['start']
 for s in clauses:
  duration=(r['end']-r['start'])*len(s)/weight;vc.append({'text':s,'start':cursor,'end':cursor+duration});cursor+=duration
save('captions-vi.srt',vc)
sr=48000;raw=subprocess.run(['ffmpeg','-v','error','-i',str(P/'audio/dialogue.flac'),'-ar',str(sr),'-ac','1','-f','f32le','-'],capture_output=True,check=True).stdout;a=np.frombuffer(raw,dtype='<f4');levels=[]
for i in range(round(T['duration']*30)):
 x=a[round(i*sr/30):round((i+1)*sr/30)];levels.append(float(min(1,np.sqrt(np.mean(x*x))/.12)) if len(x) else 0.)
(P/'mouth-levels.json').write_text(json.dumps(levels)+'\n')
print(len(out),'English cues;',len(vc),'Vietnamese review cues;',len(levels),'mouth frames')
