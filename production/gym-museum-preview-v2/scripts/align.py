from pathlib import Path
import os
os.environ.update(HF_HUB_DISABLE_TELEMETRY='1',HF_HUB_DISABLE_IMPLICIT_TOKEN='1',HF_HOME='/workspace/models/huggingface-cache',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
import json,subprocess,re,difflib,math,hashlib
import numpy as np,soundfile as sf
from faster_whisper import WhisperModel
P=Path(__file__).resolve().parents[1];scenes=json.loads((P/'performance.json').read_text());roles=json.loads((P/'authorization.json').read_text())['voices'];model=WhisperModel('base.en',device='cpu',compute_type='int8',cpu_threads=4,download_root='/workspace/models/whisper')
normal=lambda w:re.sub('[^a-z0-9]','',w.lower());tracks={};aligned={};lines=[dict(x,scene=si,line=li,id=f's{si+1:02d}-l{li+1:02d}') for si,s in enumerate(scenes) for li,x in enumerate(s['lines'])]
for role in roles:
 target=P/'audio'/f'{role.lower()}.flac';subprocess.run(['ffmpeg','-v','error','-y','-i',str(P/'audio'/f'{role.lower()}-native.wav'),'-ar','48000','-ac','1',str(target)],check=True)
 samples,sr=sf.read(target,dtype='int16');tracks[role]=samples
 cache=P/'.cache'/f'{role}-{hashlib.sha256(target.read_bytes()).hexdigest()[:12]}-asr.json';tokens=' '.join(x['text'] for x in lines if x['speaker']==role).split()
 if cache.exists():raw=json.loads(cache.read_text())
 else:
  pcm=subprocess.run(['ffmpeg','-v','error','-i',str(target),'-ar','16000','-ac','1','-f','f32le','-'],capture_output=True,check=True).stdout
  seg,_=model.transcribe(np.frombuffer(pcm,dtype='<f4').copy(),language='en',beam_size=5,word_timestamps=True,condition_on_previous_text=False,vad_filter=False)
  raw=[{'text':w.word,'start':w.start,'end':w.end} for s in seg for w in (s.words or [])];cache.write_text(json.dumps(raw)+'\n')
 out=[None]*len(tokens);matches=0
 for b in difflib.SequenceMatcher(a=list(map(normal,tokens)),b=[normal(w['text']) for w in raw],autojunk=False).get_matching_blocks():
  for j in range(b.size):out[b.a+j]=dict(raw[b.b+j],text=tokens[b.a+j],basis='asr');matches+=1
 i=0
 while i<len(out):
  if out[i] is not None:i+=1;continue
  k=i
  while k<len(out) and out[k] is None:k+=1
  a=out[i-1]['end'] if i else 0;b=out[k]['start'] if k<len(out) else len(samples)/sr
  for j in range(i,k):out[j]={'text':tokens[j],'start':a+(b-a)*(j-i)/(k-i),'end':a+(b-a)*(j-i+1)/(k-i),'basis':'interpolated'}
  i=k
 assert matches/len(tokens)>.90,(role,matches,len(tokens));aligned[role]=out
 print(role,'anchors',matches,'/',len(tokens),'seconds',len(samples)/sr,flush=True)
index={r:0 for r in roles};assembled=[];words=[];turns=[];cursor=0;SR=48000
for i,line in enumerate(lines):
 role=line['speaker'];n=len(line['text'].split());a=index[role];b=a+n;ww=aligned[role][a:b];track=tracks[role]
 # Midpoint between role's adjacent utterances retains every word; trim excessive outside silence only.
 lo=max(0,ww[0]['start']-.10);hi=min(len(track)/SR,ww[-1]['end']+.16)
 if a:lo=max(lo,(aligned[role][a-1]['end']+ww[0]['start'])/2)
 if b<len(aligned[role]):hi=min(hi,(ww[-1]['end']+aligned[role][b]['start'])/2)
 aa=round(lo*SR);bb=round(hi*SR);clip=track[aa:bb];start=cursor/SR;end=(cursor+len(clip))/SR
 for w in ww:words.append(dict(w,start=start+w['start']-aa/SR,end=start+w['end']-aa/SR,role=role,turn=line['id']))
 turns.append(dict(line,start=start,end=end,native_role_start=aa/SR,native_role_end=bb/SR,voice=roles[role]))
 assembled.append(clip);cursor+=len(clip);index[role]=b
 # Action/reaction room, never speech tempo changes.
 gap=.30 if role=='NARRATOR' else .38
 if i+1<len(lines) and lines[i+1]['scene']!=line['scene']:gap=1.05
 if line['text'] in ['They paid?','When does the torture begin?','We need to change the sign.']:gap=.85
 assembled.append(np.zeros(round(gap*SR),np.int16));cursor+=round(gap*SR)
assembled.append(np.zeros(SR,np.int16));cursor+=SR
sf.write(P/'audio/dialogue.flac',np.concatenate(assembled),SR,subtype='PCM_16');duration=math.ceil(cursor/SR*30)/30
(P/'turns.json').write_text(json.dumps(turns,indent=2)+'\n');(P/'words.json').write_text(json.dumps(words,indent=2)+'\n');(P/'timing.json').write_text(json.dumps({'duration':duration,'fps':30,'speech_speed_changed':False,'word_count':len(words),'exact_asr_anchors':sum(w['basis']=='asr' for w in words),'voices':roles,'segmentation':'Word-aligned excerpts from each native role recording, original speech samples/rate retained; brief action gaps between turns.'},indent=2)+'\n');print('COMPLETE',duration,len(words),flush=True)
