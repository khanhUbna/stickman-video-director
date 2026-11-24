from pathlib import Path
import os
os.environ['HF_HUB_DISABLE_TELEMETRY']='1';os.environ['HF_HUB_DISABLE_IMPLICIT_TOKEN']='1';os.environ['HF_HUB_DISABLE_XET']='1';os.environ['HF_HOME']='/workspace/models/huggingface-cache';os.environ['ORT_DISABLE_TELEMETRY']='1'
import json,re,difflib,subprocess,math
import numpy as np
import soundfile as sf
import onnxruntime as ort
ort.disable_telemetry_events()
from faster_whisper import WhisperModel
P=Path(__file__).resolve().parents[1];text=(P/'script-en.txt').read_text();paras=text.strip().split('\n\n');tokens=text.split()
rawfile=P/'.cache/native-asr.json'
if rawfile.exists():raw=json.loads(rawfile.read_text())
else:
 pcm=subprocess.run(['ffmpeg','-v','error','-i',str(P/'audio/voice.flac'),'-ar','16000','-ac','1','-f','f32le','-'],capture_output=True,check=True).stdout
 model=WhisperModel('base.en',device='cpu',compute_type='int8',cpu_threads=4,download_root='/workspace/models/whisper')
 seg,_=model.transcribe(np.frombuffer(pcm,dtype='<f4').copy(),language='en',beam_size=5,word_timestamps=True,condition_on_previous_text=False,vad_filter=False)
 raw=[{'word':w.word,'start':w.start,'end':w.end} for s in seg for w in (s.words or [])];rawfile.write_text(json.dumps(raw)+'\n')
normal=lambda w:re.sub('[^a-z0-9]','',w.lower());aligned=[None]*len(tokens);matched=0
for b in difflib.SequenceMatcher(a=list(map(normal,tokens)),b=[normal(w['word']) for w in raw],autojunk=False).get_matching_blocks():
 for j in range(b.size):r=raw[b.b+j];aligned[b.a+j]={'text':tokens[b.a+j],'start':r['start'],'end':r['end'],'basis':'local-asr'};matched+=1
voice,sr=sf.read(P/'audio/voice.flac',dtype='int16');native_duration=len(voice)/sr
i=0
while i<len(aligned):
 if aligned[i] is not None:i+=1;continue
 end=i
 while end<len(aligned) and aligned[end] is None:end+=1
 a=aligned[i-1]['end'] if i else 0;b=aligned[end]['start'] if end<len(aligned) else native_duration
 for j in range(i,end):aligned[j]={'text':tokens[j],'start':a+(b-a)*(j-i)/(end-i),'end':a+(b-a)*(j-i+1)/(end-i),'basis':'interpolated'}
 i=end
assert matched/len(tokens)>.95,(matched,len(tokens))
pauses=[1.1,.65,1.25,.6,1.0,.8,1.5,.6,1.1,.6,1.4,1.8,1.3,1.0]
ends=[];offset=0
for p in paras:offset+=len(p.split());ends.append(offset)
cuts=[]
for j,index in enumerate(ends[:-1]):
 a=aligned[index-1]['end'];b=aligned[index]['start'];assert b>=a,(j,a,b);cuts.append((round((a+b)/2*sr),pauses[j]))
chunks=[];last=0;inserted=0
for cut,pause in cuts:chunks.extend([voice[last:cut],np.zeros(round(pause*sr),dtype=voice.dtype)]);last=cut;inserted+=round(pause*sr)
chunks.extend([voice[last:],np.zeros(round(1.2*sr),dtype=voice.dtype)])
final=np.concatenate(chunks);sf.write(P/'audio/narration.flac',final,sr,subtype='PCM_16')
for i,w in enumerate(aligned):
 native=w['start'];shift=sum(pause for cut,pause in cuts if cut/sr<=native);w['start']+=shift;w['end']+=shift;w['index']=i;w['paragraph']=next(j+1 for j,e in enumerate(ends) if i<e)
speech=[];start=0
for j,(p,index) in enumerate(zip(paras,ends)):
 words=aligned[start:index];speech.append({'id':j+1,'text':p,'start':words[0]['start'],'end':words[-1]['end']});start=index
duration=math.ceil((len(final)/sr)*30)/30
(P/'speech.json').write_text(json.dumps({'paragraphs':speech,'duration':duration,'native_duration':native_duration,'silence_inserted_seconds':inserted/sr+1.2,'speech_speed_changed':False,'exact_anchors':matched,'words':len(tokens)},indent=2)+'\n')
(P/'words.json').write_text(json.dumps(aligned,indent=2)+'\n')
cues=[];group=[]
for w in aligned:
 if group and (len(' '.join(t['text'] for t in group+[w]))>48 or len(group)>=7 or w['paragraph']!=group[-1]['paragraph'] or w['start']-group[-1]['end']>.5):cues.append({'start':group[0]['start'],'end':group[-1]['end']+.10,'text':' '.join(t['text'] for t in group)});group=[]
 group.append(w)
 if re.search('[.!?]$',w['text']) and len(group)>=3:cues.append({'start':group[0]['start'],'end':group[-1]['end']+.1,'text':' '.join(t['text'] for t in group)});group=[]
if group:cues.append({'start':group[0]['start'],'end':group[-1]['end']+.1,'text':' '.join(t['text'] for t in group)})
for i,c in enumerate(cues):
 if i+1<len(cues):c['end']=min(c['end'],cues[i+1]['start']-.005)
def stamp(t):
 n=round(t*1000);return f'{n//3600000:02d}:{n//60000%60:02d}:{n//1000%60:02d},{n%1000:03d}'
(P/'captions.json').write_text(json.dumps(cues,indent=2)+'\n');(P/'captions-en.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["text"]}' for i,c in enumerate(cues))+'\n')
print(json.dumps({'words':len(tokens),'exact_anchors':matched,'duration':duration,'cues':len(cues),'native_voice_preserved':True}))
