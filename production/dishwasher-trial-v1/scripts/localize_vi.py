"""Vietnamese captions from approved translation, anchored to real English sentence/turn times.
Within a long translated sentence, display subphrases divide the same source interval for reading;
this is translation display timing, not a claim of Vietnamese word forced alignment.
"""
from pathlib import Path
import json,re,sys
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P));import artwork as A
from PIL import ImageDraw,Image
VI=P.parents[1]/'youtube-videos/your-dishwasher-thinks-you-re-the-problem-9012e9e5e1/script/performance-vi.json'
en=json.loads((P/'performance.json').read_text());vi=json.loads(VI.read_text());turns=json.loads((P/'turns.json').read_text());words=json.loads((P/'words.json').read_text());font=A.font(40,1.5);draw=ImageDraw.Draw(Image.new('RGB',(1920,1080)))
def sentences(t):return [s.replace('<ELLIPSIS>','...') for s in re.split(r'(?<=[.!?])\s+',t.replace('...','<ELLIPSIS>'))]
def width(t):b=draw.textbbox((0,0),t,font=font);return b[2]-b[0]
def split(t):
 if width(t)<=1700:return [t]
 tokens=t.split();options=[]
 for k in range(2,len(tokens)-1):
  a=' '.join(tokens[:k]);b=' '.join(tokens[k:])
  if width(a)>1700:continue
  score=abs(width(a)-min(1700,width(b)))
  if tokens[k-1].endswith(','):score-=1000
  elif tokens[k].lower() in ['rồi','nhưng','và','trước','sau','để','khi','theo','với','mà','như','bằng']:score-=250
  if (tokens[k-1].lower(),tokens[k].lower().strip('.,!?')) in [('bộ','lọc'),('máy','rửa'),('rửa','bát'),('tay','phun'),('tia','nước'),('thức','ăn'),('thẩm','phán'),('chất','tẩy'),('tinh','bột'),('bát','đĩa')]:score+=2000
  if tokens[k-1].lower() in ['của','một','những','các','và','hoặc','trong','theo']:score+=300
  options.append((score,k))
 assert options,t
 k=min(options)[1];return [' '.join(tokens[:k])]+split(' '.join(tokens[k:]))
units=[];counter=0
for si,(a,b) in enumerate(zip(en,vi)):
 for li,(x,y) in enumerate(zip(a['lines'],b['lines'])):
  turn=turns[counter];counter+=1;ww=[w for w in words if w['turn']==turn['id']];aa=sentences(x['text']);bb=sentences(y['text'])
  if si==7 and li==0:bb=['Khi chương trình kết thúc, Sam mở cửa máy.']+bb[2:]
  assert len(aa)==len(bb),(si,li);offset=0
  for english,vietnamese in zip(aa,bb):
   n=len(english.split());part=ww[offset:offset+n];offset+=n;assert len(part)==n
   units.append({'start':part[0]['start'],'end':min(turn['end']+.08,part[-1]['end']+.25),'text':vietnamese,'source_text':english,'turn':turn['id'],'role':turn['speaker']})
  assert offset==len(ww),(si,li)
# Merge very short adjacent sentences in the same utterance when they fit one line.
merged=[]
for u in units:
 if merged and merged[-1]['turn']==u['turn'] and width(merged[-1]['text']+' '+u['text'])<=1700 and u['end']-merged[-1]['start']<=5:
  merged[-1]['text']+=' '+u['text'];merged[-1]['source_text']+=' '+u['source_text'];merged[-1]['end']=u['end']
 else:merged.append(dict(u))
cues=[]
for u in merged:
 pieces=split(u['text']);weights=[len(t) for t in pieces];total=sum(weights);elapsed=0
 for t,k in zip(pieces,weights):
  a=u['start']+(u['end']-u['start'])*elapsed/total;elapsed+=k;b=u['start']+(u['end']-u['start'])*elapsed/total
  cues.append(dict(u,text=t,start=a,end=b))
for a,b in zip(cues,cues[1:]):a['end']=min(a['end'],b['start']-.005)
assert all(c['end']>c['start']>=0 and width(c['text'])<=1700 for c in cues)
def stamp(t,comma=True):
 n=round(t*1000);return f'{n//3600000:02d}:{n//60000%60:02d}:{n//1000%60:02d}{"," if comma else "."}{n%1000:03d}'
(P/'captions-vi.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2)+'\n');(P/'captions-vi.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["text"]}' for i,c in enumerate(cues))+'\n');(P/'captions-vi.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f'{stamp(c["start"],False)} --> {stamp(c["end"],False)}\n{c["text"]}' for c in cues)+'\n')
report={'language':'vi','cues':len(cues),'source_utterances':counter,'source_sentences':len(units),'complete_source_sentence_coverage':True,'new_paid_calls':0,'timing':'Actual English word/sentence/turn anchors; Vietnamese long-sentence display subphrases divide the same interval for reading. No Vietnamese speech generated or word-for-word forced-alignment claim.','maximum_native_pixel_width':max(width(c['text']) for c in cues),'font_native_pixels':60,'single_line':True,'duration_seconds':194.9,'last_cue_end':cues[-1]['end']};(P/'reports/vietnamese-caption-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
