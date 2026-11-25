from pathlib import Path
import os
os.environ.update(HF_HUB_DISABLE_TELEMETRY='1',HF_HUB_DISABLE_IMPLICIT_TOKEN='1',HF_HOME='/workspace/models/huggingface-cache',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
import json,subprocess,re,difflib,hashlib
import numpy as np
from faster_whisper import WhisperModel
P=Path(__file__).resolve().parents[1];audio=P/'audio/dialogue.flac';cache=P/'.cache/assembled-asr.json';digest=hashlib.sha256(audio.read_bytes()).hexdigest()
if cache.exists() and json.loads(cache.read_text()).get('sha256')==digest:raw=json.loads(cache.read_text())['text']
else:
 pcm=subprocess.run(['ffmpeg','-v','error','-i',str(audio),'-ar','16000','-ac','1','-f','f32le','-'],capture_output=True,check=True).stdout
 m=WhisperModel('base.en',device='cpu',compute_type='int8',cpu_threads=2,download_root='/workspace/models/whisper');seg,_=m.transcribe(np.frombuffer(pcm,dtype='<f4').copy(),language='en',beam_size=5,condition_on_previous_text=False,vad_filter=False);raw=' '.join(s.text.strip() for s in seg);cache.write_text(json.dumps({'sha256':digest,'text':raw})+'\n')
normal=lambda x:re.sub('[^a-z0-9]','',x.lower());expected=(P/'script-en.txt').read_text().split();heard=raw.split();match=difflib.SequenceMatcher(a=list(map(normal,expected)),b=list(map(normal,heard)),autojunk=False);n=sum(b.size for b in match.get_matching_blocks());changes=[]
for tag,a,b,c,d in match.get_opcodes():
 if tag!='equal':changes.append({'kind':tag,'script':' '.join(expected[a:b]),'asr':' '.join(heard[c:d])})
r={'assembled_audio_sha256':digest,'local_model':'Whisperbase.en, CPU','canonical_words':len(expected),'asr_words':len(heard),'exact_normalized_word_matches':n,'exact_match_fraction':n/len(expected),'differences':changes,'scope':'Local ASR content check of assembled multi-role speech, not human listening or pronunciation certification.'};(P/'reports/speech-check.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r),flush=True);assert n/len(expected)>.94
