"""Local demo voice only. No impersonation or paid API."""
from pathlib import Path
import os,json
os.environ['ORT_DISABLE_TELEMETRY']='1'
os.environ['DO_NOT_TRACK']='1'
import numpy as np
import soundfile as sf
import onnxruntime as ort
import espeakng_loader
from kokoro_onnx import Kokoro
from kokoro_onnx.config import EspeakConfig
P=Path(__file__).resolve().parent
opts=ort.SessionOptions();opts.intra_op_num_threads=4;opts.inter_op_num_threads=1
ort.disable_telemetry_events()
m=Kokoro.from_session(ort.InferenceSession('/workspace/models/kokoro-v1/kokoro-v1.0.onnx',sess_options=opts,providers=['CPUExecutionProvider']),'/workspace/models/kokoro-v1/voices-v1.0.bin',espeak_config=EspeakConfig(lib_path=espeakng_loader.get_library_path(),data_path=espeakng_loader.get_data_path()))
lines=[(6.2,'Now, the important part: keep the coffee in the cup.'),(12.2,'Walking is easy. Walking with coffee? That takes confidence.')]
mix=np.zeros(480000,dtype=np.float32); cues=[]
for i,(start,text) in enumerate(lines):
 f=P/'assets'/f'line-{i}.wav'
 if f.exists():a,sr=sf.read(f,dtype='float32')
 else:
  a,sr=m.create(text,voice='am_michael',speed=1.02,lang='en-us');sf.write(f,a,sr)
 assert sr==24000
 assert start+len(a)/sr<18
 mix[round(start*sr):round(start*sr)+len(a)]+=a
 cues.append(dict(start=start,end=start+len(a)/sr,text=text))
 print(cues[-1],flush=True)
# Low-key original room tone and procedural foot/cup Foley, not licensed music.
rng=np.random.default_rng(24)
for t in [0.8,1.25,1.7,2.15,2.6,3.05,3.5,3.95,10.5,10.95,11.4,16.5,16.95,17.4]:
 n=2400;x=np.arange(n)/24000;hit=.018*rng.normal(size=n)*np.exp(-x*55)
 i=round(t*24000);mix[i:i+n]+=hit
for t in [5.1,18.4]:
 x=np.arange(3600)/24000;hit=.02*(np.sin(2*np.pi*1700*x)+.5*np.sin(2*np.pi*2400*x))*np.exp(-x*35)
 i=round(t*24000);mix[i:i+len(hit)]+=hit
mix*=min(1.,.82/max(.001,float(np.max(np.abs(mix)))))
sf.write(P/'assets'/'demo-audio.wav',mix,24000,subtype='PCM_16')
(P/'assets'/'speech.json').write_text(json.dumps(dict(provider='Local Kokoro ONNX',voice='am_michael',impersonation=False,paid_api_calls=0,cues=cues),indent=2))
