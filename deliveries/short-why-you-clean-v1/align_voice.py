"""Offline acoustic forced alignment; never calls a speech API."""
from pathlib import Path
import hashlib,json,re,subprocess,wave
from pocketsphinx import Decoder

B=Path(__file__).resolve().parent
source=Path('/workspace/stickman-video-director/deliveries/short-why-you-clean-v1/voice.wav')
if not (B/'voice.wav').exists():
    (B/'voice.wav').write_bytes(source.read_bytes())
subprocess.run(['ffmpeg','-v','error','-i',str(B/'voice.wav'),'-ar','16000','-ac','1','-c:a','pcm_s16le','-y',str(B/'alignment-16k.wav')],check=True)
text=(B/'script.txt').read_text().strip()
tokens=re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?",text)
decoder=Decoder(samprate=16000,loglevel='ERROR')
missing=[w for w in tokens if not decoder.lookup_word(w.lower())]
if missing: raise RuntimeError('Dictionary missing words: '+str(missing))
decoder.set_align_text(' '.join(w.lower() for w in tokens))
with wave.open(str(B/'alignment-16k.wav'),'rb') as f: data=f.readframes(f.getnframes())
decoder.start_utt();decoder.process_raw(data,full_utt=True);decoder.end_utt()
segments=[s for s in decoder.seg() if s.word not in ('<sil>','<s>','</s>','[SPEECH]','[NOISE]')]
if len(segments)!=len(tokens): raise RuntimeError((len(segments),len(tokens)))
words=[]
for token,s in zip(tokens,segments):
    assert re.sub(r'\(\d+\)$','',s.word)==token.lower(),(token,s.word)
    words.append(dict(word=token,start=round(s.start_frame/100,3),end=round((s.end_frame+1)/100,3)))
result=dict(method='PocketSphinx 5.0.4 offline acoustic forced alignment',source_sha256=hashlib.sha256((B/'voice.wav').read_bytes()).hexdigest(),words=words,review='automatic alignment; caption boundaries require playback review')
(B/'words.json').write_text(json.dumps(result,indent=2)+'\n')
for w in words: print(f"{w['start']:5.2f} {w['end']:5.2f} {w['word']}")
