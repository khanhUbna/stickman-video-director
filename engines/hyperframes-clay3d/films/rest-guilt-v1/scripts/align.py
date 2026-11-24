"""Align the approved words to local Whisper recognition of the actual local narration."""
from pathlib import Path
import os
os.environ['HF_HUB_DISABLE_TELEMETRY']='1'
os.environ['HF_HUB_DISABLE_IMPLICIT_TOKEN']='1'
os.environ['HF_HUB_DISABLE_XET']='1'
os.environ['HF_HOME']='/workspace/models/huggingface-cache'
os.environ['ORT_DISABLE_TELEMETRY']='1'
import json,re,difflib,math,subprocess
import numpy as np
import onnxruntime as ort
ort.disable_telemetry_events()
from faster_whisper import WhisperModel

ROOT=Path(__file__).resolve().parents[1]
speech=json.loads((ROOT/'assets/speech.json').read_text())
model=WhisperModel('base.en',device='cpu',compute_type='int8',cpu_threads=4,num_workers=1,download_root='/workspace/models/whisper')
normalize=lambda s:re.sub(r'[^a-z0-9]','',s.lower())
all_words=[]; reports=[]
for p in speech['paragraphs']:
    cache=ROOT/f'.cache/asr-{p["id"]:02d}.json'
    if cache.exists(): raw=json.loads(cache.read_text())
    else:
        pcm=subprocess.run(['ffmpeg','-v','error','-i',str(ROOT/p['audio']),'-ac','1','-ar','16000','-f','f32le','-'],check=True,capture_output=True).stdout
        audio=np.frombuffer(pcm,dtype='<f4').copy()
        segments,_=model.transcribe(audio,language='en',beam_size=5,word_timestamps=True,vad_filter=False,condition_on_previous_text=False)
        raw=[{'word':w.word.strip(),'start':w.start,'end':w.end,'probability':w.probability} for s in segments for w in (s.words or [])]
        cache.write_text(json.dumps(raw,indent=2)+'\n')
    words=p['text'].split(); source=[normalize(w) for w in words]; recognized=[normalize(w['word']) for w in raw]
    matcher=difflib.SequenceMatcher(a=source,b=recognized,autojunk=False)
    aligned=[None]*len(words); matched=0
    for block in matcher.get_matching_blocks():
        for j in range(block.size):
            r=raw[block.b+j]; aligned[block.a+j]={'text':words[block.a+j],'start':p['start']+r['start'],'end':min(p['end'],p['start']+r['end']),'basis':'local-asr-anchor'}; matched+=1
    index=0
    while index<len(aligned):
        if aligned[index] is not None: index+=1;continue
        last=index
        while last<len(aligned) and aligned[last] is None:last+=1
        start=aligned[index-1]['end'] if index else p['start']; end=aligned[last]['start'] if last<len(aligned) else p['end']
        end=max(start+0.03*(last-index),end)
        for j in range(index,last):
            aligned[j]={'text':words[j],'start':start+(end-start)*(j-index)/(last-index),'end':start+(end-start)*(j-index+1)/(last-index),'basis':'interpolated-between-asr-anchors'}
        index=last
    previous=p['start']
    for w in aligned:
        w['start']=max(previous,min(p['end']-0.015,w['start'])); w['end']=min(p['end'],max(w['start']+0.015,w['end'])); previous=w['end'];w['paragraph']=p['id'];w['index']=len(all_words);all_words.append(w)
    reports.append({'paragraph':p['id'],'script_words':len(words),'recognized_words':len(raw),'exact_normalized_anchors':matched,'ratio':matched/len(words)})
    print(json.dumps(reports[-1]),flush=True)

cues=[];current=[]
for i,w in enumerate(all_words):
    candidate=' '.join(x['text'] for x in current+[w])
    boundary=current and (len(current)>=7 or len(candidate)>49 or w['paragraph']!=current[-1]['paragraph'] or w['start']-current[-1]['end']>0.6)
    if boundary:
        cues.append({'start':current[0]['start'],'end':current[-1]['end']+0.12,'text':' '.join(x['text'] for x in current)});current=[]
    current.append(w)
    if re.search(r'[.!?]$',w['text']) and len(current)>=3:
        cues.append({'start':current[0]['start'],'end':current[-1]['end']+0.12,'text':' '.join(x['text'] for x in current)});current=[]
if current:cues.append({'start':current[0]['start'],'end':current[-1]['end']+0.12,'text':' '.join(x['text'] for x in current)})
for i,cue in enumerate(cues):
    if i+1<len(cues):cue['end']=min(cue['end'],cues[i+1]['start']-0.01)
    cue['end']=max(cue['start']+0.10,cue['end']);cue['id']=i+1
def timestamp(t):
    ms=round(t*1000);return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'
(ROOT/'assets/words.json').write_text(json.dumps(all_words,ensure_ascii=False,indent=2)+'\n')
(ROOT/'assets/captions.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2)+'\n')
(ROOT/'script/subtitles-en.srt').write_text('\n\n'.join(f'{c["id"]}\n{timestamp(c["start"])} --> {timestamp(c["end"])}\n{c["text"]}' for c in cues)+'\n')
report={'method':'Local faster-whisper base.en on isolated paragraph recordings; exact script retained; unmatched words interpolated between recognized anchors.','word_count':len(all_words),'exact_anchors':sum(p['exact_normalized_anchors'] for p in reports),'paragraphs':reports,'caption_cues':len(cues),'paid_api_calls':0}
(ROOT/'assets/alignment-report.json').write_text(json.dumps(report,indent=2)+'\n')
assert ' '.join(w['text'] for w in all_words)==' '.join(speech_p['text'] for speech_p in speech['paragraphs'])
print(json.dumps({'complete':True,'words':len(all_words),'cues':len(cues),'anchor_ratio':report['exact_anchors']/len(all_words)}),flush=True)
