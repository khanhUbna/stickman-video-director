from pathlib import Path
import os
os.environ.update(HF_HUB_DISABLE_TELEMETRY='1',HF_HUB_DISABLE_IMPLICIT_TOKEN='1',HF_HOME='/workspace/models/huggingface-cache',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
import json,subprocess,re,difflib,math,hashlib
import numpy as np,soundfile as sf
from faster_whisper import WhisperModel
P=Path(__file__).resolve().parents[1];V=P.parent/'gym-museum-preview-v2';SR=48000
scenes=json.loads((P/'performance.json').read_text());plan=json.loads((P/'audio/record-plan.json').read_text());reuse=json.loads((P/'audio/reuse-map.json').read_text())
model=WhisperModel('base.en',device='cpu',compute_type='int8',cpu_threads=4,download_root='/workspace/models/whisper')
lines=[dict(r,scene=si,line=li,id=f's{si+1:02d}-l{li+1:02d}') for si,s in enumerate(scenes) for li,r in enumerate(s['lines'])];byid={x['id']:x for x in lines};clips={};aligned={};origins={}
def norm(w):
 w=re.sub('[^a-z0-9]','',w.lower());return {'1':'one','2':'two','3':'three','4':'four'}.get(w,w)
for req in plan['missing_requests']:
 wav=P/'audio'/(req['id']+'.wav');target=P/'audio'/(req['id']+'.flac');subprocess.run(['ffmpeg','-v','error','-y','-i',str(wav),'-ar',str(SR),'-ac','1',str(target)],check=True);samples,sr=sf.read(target,dtype='int16');tokens=req['input'].split();key=hashlib.sha256(wav.read_bytes()).hexdigest()[:12];cache=P/'.cache'/(req['id']+'-'+key+'-asr.json')
 if cache.exists():raw=json.loads(cache.read_text())
 else:
  pcm=subprocess.run(['ffmpeg','-v','error','-i',str(target),'-ar','16000','-ac','1','-f','f32le','-'],capture_output=True,check=True).stdout
  seg,_=model.transcribe(np.frombuffer(pcm,dtype='<f4').copy(),language='en',beam_size=5,word_timestamps=True,condition_on_previous_text=False,vad_filter=False)
  raw=[{'text':w.word,'start':w.start,'end':w.end} for s in seg for w in(s.words or[])];cache.write_text(json.dumps(raw)+'\n')
 out=[None]*len(tokens);matches=0
 for b in difflib.SequenceMatcher(a=list(map(norm,tokens)),b=[norm(w['text']) for w in raw],autojunk=False).get_matching_blocks():
  for j in range(b.size):out[b.a+j]=dict(raw[b.b+j],text=tokens[b.a+j],basis='asr');matches+=1
 i=0
 while i<len(out):
  if out[i] is not None:i+=1;continue
  k=i
  while k<len(out) and out[k] is None:k+=1
  lo=out[i-1]['end'] if i else 0;hi=out[k]['start'] if k<len(out) else len(samples)/SR
  for j in range(i,k):out[j]={'text':tokens[j],'start':lo+(hi-lo)*(j-i)/(k-i),'end':lo+(hi-lo)*(j-i+1)/(k-i),'basis':'interpolated'}
  i=k
 assert matches/len(tokens)>=.90,(req['id'],matches,len(tokens),'No paid retry; inspect local ASR')
 offset=0
 for ident in req['turn_ids']:
  r=byid[ident];n=len(r['text'].split());ww=out[offset:offset+n];lo=max(0,ww[0]['start']-.10);hi=min(len(samples)/SR,ww[-1]['end']+.16)
  if offset:lo=max(lo,(out[offset-1]['end']+ww[0]['start'])/2)
  if offset+n<len(out):hi=min(hi,(ww[-1]['end']+out[offset+n]['start'])/2)
  a=round(lo*SR);b=round(hi*SR);clips[ident]=samples[a:b];aligned[ident]=[dict(w,start=w['start']-a/SR,end=w['end']-a/SR) for w in ww];origins[ident]={'kind':'new missing speech','file':target.name,'start_sample':a,'end_sample':b};offset+=n
 print(req['id'],'anchors',matches,'/',len(tokens),'seconds',len(samples)/SR,flush=True)
# Reuse exact accepted dialogue samples and their word locations.
prior,sr=sf.read(V/'audio/dialogue20.flac',dtype='int16');oldwords=json.loads((V/'words20.json').read_text())
for ident,info in reuse.items():
 r=info['source_turn'];a=round(r['start']*SR);b=round(r['end']*SR);clips[ident]=prior[a:b];aligned[ident]=[dict(w,start=w['start']-a/SR,end=w['end']-a/SR) for w in oldwords if w['turn']==r['id']];origins[ident]={'kind':'approved V2 voice reused unchanged','source_project':str(V),'source_turn':r['id'],'start_sample':a,'end_sample':b,'pcm_sha256':hashlib.sha256(prior[a:b].tobytes()).hexdigest()}
assembled=[];cursor=0;turns=[];words=[]
for i,r in enumerate(lines):
 ident=r['id'];clip=clips[ident];start=cursor/SR;end=start+len(clip)/SR;assembled.append(clip);cursor+=len(clip)
 turns.append(dict(r,start=start,end=end,voice=json.loads((P/'authorization.json').read_text())['voices'][r['speaker']],origin=origins[ident]))
 for w in aligned[ident]:words.append(dict(w,start=start+w['start'],end=start+w['end'],role=r['speaker'],turn=ident))
 sf.write(P/'audio/reused'/(ident+'.flac'),clip,SR,subtype='PCM_16') if ident in reuse else None
 gap=.30 if r['speaker']=='NARRATOR' else .38
 if r['text'] in ['They paid?','Complicated society.','Online.']:gap=.80
 if r['text']=='When does the torture begin?':gap=.85
 if i+1<len(lines) and lines[i+1]['scene']!=r['scene']:gap=1.05
 if i==len(lines)-1:gap=1.8
 assembled.append(np.zeros(round(gap*SR),np.int16));cursor+=round(gap*SR)
sf.write(P/'audio/dialogue.flac',np.concatenate(assembled),SR,subtype='PCM_16');duration=math.ceil(cursor/SR*30)/30
(P/'turns.json').write_text(json.dumps(turns,indent=2)+'\n');(P/'words.json').write_text(json.dumps(words,indent=2)+'\n');(P/'timing.json').write_text(json.dumps({'duration':duration,'fps':30,'word_count':len(words),'native_speech_speed_preserved':True,'reused_turns':list(reuse),'exact_asr_anchors':sum(w['basis']=='asr' for w in words),'source':'New missing-role recordings + exact approved V2 PCM excerpts, no tempo change'},indent=2)+'\n')
assert ' '.join(w['text'] for w in words).split()==(P/'script-en.txt').read_text().split()
print('FULL AUDIO',duration,'seconds;',len(words),'words;',len(turns),'turns;',len(reuse),'reused unchanged',flush=True)
