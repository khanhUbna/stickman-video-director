from pathlib import Path
import json,subprocess,re
import numpy as np,soundfile as sf
P=Path(__file__).resolve().parents[1];turns=json.loads((P/'turns.json').read_text());SR=48000;N=20*SR;audio=np.zeros(N,np.float32);new=[];words=json.loads((P/'words.json').read_text());result=[];cursor=0
for i,r in enumerate(turns):
 samples,sr=sf.read(P/'audio'/(r['speaker'].lower()+'.flac'),dtype='float32');assert sr==SR
 lo=round(r['native_role_start']*SR);hi=round(r['native_role_end']*SR);clip=samples[lo:hi];start=cursor/SR;shift=start-r['start'];end=start+len(clip)/SR
 assert cursor+len(clip)<=N,'Sample speech longer than20s; no automatic speed change'
 audio[cursor:cursor+len(clip)]=clip;cursor+=len(clip);new.append(dict(r,start=start,end=end))
 for w in words:
  if w['turn']==r['id']:result.append(dict(w,start=w['start']+shift,end=w['end']+shift))
 gap=.30 if r['speaker']=='NARRATOR' else .38
 if r['line']==3:gap=1.40 # Attach safety clip with a visible result before starting belt.
 if r['line']==4:gap=.85 # Vale waits for Mina's deadpan reply.
 cursor+=round(gap*SR)
assert new[-1]['end']<19.1
sf.write(P/'audio/dialogue20.flac',audio,SR,subtype='PCM_16');(P/'turns20.json').write_text(json.dumps(new,indent=2)+'\n');(P/'words20.json').write_text(json.dumps(result,indent=2)+'\n');(P/'timing20.json').write_text(json.dumps({'duration':20.0,'fps':30,'spoken_end':new[-1]['end'],'words':len(result),'speech_speed_changed':False,'post_dialogue_acting_seconds':20-new[-1]['end'],'source':'Exact native recording excerpts; only silence gaps adjusted'},indent=2)+'\n')
# Build sentence-level semantic cues. The longest line fits at fixed native42px.
byturn={r['id']:r for r in new};cues=[]
for turn in new:
 group=[]
 for w in result:
  if w['turn']!=turn['id']:continue
  group.append(w)
  if w['text'][-1:] in '.?!':
   cues.append({'text':' '.join(x['text'] for x in group),'start':group[0]['start'],'end':min(turn['end']+.10,group[-1]['end']+.17),'role':turn['speaker']});group=[]
 if group:cues.append({'text':' '.join(x['text'] for x in group),'start':group[0]['start'],'end':turn['end']+.10,'role':turn['speaker']})
for a,b in zip(cues,cues[1:]):a['end']=min(a['end'],b['start']-.002)
assert ' '.join(c['text'] for c in cues).split()==(P/'script-en.txt').read_text().split()
(P/'captions20.json').write_text(json.dumps(cues,indent=2)+'\n')
def stamp(t):
 n=round(t*1000);return f'{n//3600000:02d}:{n//60000%60:02d}:{n//1000%60:02d},{n%1000:03d}'
(P/'captions-en.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["text"]}' for i,c in enumerate(cues))+'\n')
vi=json.loads((P/'performance-vi.json').read_text())[0]['lines'];vc=[]
for turn,row in zip(new,vi):
 sentences=[s.strip() for s in re.findall(r'[^.!?]+[.!?]?',row['text']) if s.strip()];dt=(turn['end']-turn['start'])/len(sentences)
 for j,s in enumerate(sentences):vc.append({'text':s,'start':turn['start']+j*dt,'end':turn['start']+(j+1)*dt})
(P/'captions-vi.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["text"]}' for i,c in enumerate(vc))+'\n')
# RMS mouth tracking is amplitude driven, not phonetic lip sync.
levels=[]
for i in range(600):
 s=audio[i*1600:(i+1)*1600];levels.append(float(min(1,np.sqrt(np.mean(s*s))/.12)))
(P/'mouth-levels.json').write_text(json.dumps(levels)+'\n');print('20s assembly:',new[-1]['end'],'spoken end;',len(cues),'English cues')
