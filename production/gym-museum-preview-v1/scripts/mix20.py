from pathlib import Path
import json,subprocess,hashlib
import numpy as np,soundfile as sf
P=Path(__file__).resolve().parents[1];SR=48000;N=20*SR;rng=np.random.default_rng(3026)
voice,sr=sf.read(P/'audio/dialogue20.flac',dtype='float32');assert sr==SR and len(voice)==N
music=np.zeros(N,np.float32);fx=np.zeros(N,np.float32);events=[]
def add(stem,at,sound,gain):
 i=round(at*SR);n=min(len(sound),N-i)
 if i>=0 and n>0:stem[i:i+n]+=sound[:n]*gain
# Original sparse pizzicato cue. Pull the music out for Mina's safety interruption.
for i,at in enumerate(np.arange(.15,19,.60)):
 if 10.9<at<14.4:continue
 f=[196,246.94,293.66,246.94,174.61,220,261.63,220][i%8];tt=np.arange(round(.38*SR))/SR;note=(np.sin(2*np.pi*f*tt)+.22*np.sin(2*np.pi*f*2*tt))*np.exp(-tt*14)*np.minimum(1,tt/.004)
 add(music,float(at),note.astype(np.float32),.007 if at<10.9 else .004)
def event(at,kind,gain):
 dur=.13 if kind=='step' else .08;tt=np.arange(round(dur*SR))/SR;noise=rng.normal(0,1,len(tt));env=np.minimum(1,tt/.003)*np.exp(-tt*(42 if kind=='clip' else 24))
 if kind=='step':sound=(np.sin(2*np.pi*95*tt)*.65+np.convolve(noise,np.ones(8)/8,mode='same')*.4)*env
 else:sound=(noise*.6+np.sin(2*np.pi*1400*tt)*.25)*env
 add(fx,at,sound.astype(np.float32),gain);events.append({'time':at,'kind':kind,'gain':gain,'source':'original local procedural Foley','purpose':'visible foot contact' if kind=='step' else 'visible clip or button contact'})
for t in np.arange(2.3,4.8,.45):event(float(t),'step',.028)
for t in np.arange(9.45,10.82,.31):event(float(t),'step',.023)
event(13.88,'clip',.035);event(14.55,'button',.024)
for t in np.arange(14.57,20,.45):event(float(t),'step',.018)
# Low mechanical belt motor, only after explicit start; no suspense alarm.
tt=np.arange(N)/SR;env=np.clip((tt-14.57)/.35,0,1)*np.clip((20-tt)/.2,0,1);fx+=(np.sin(2*np.pi*86*tt)+.2*np.sin(2*np.pi*172*tt))*env*.0015
music*=np.minimum(1,np.arange(N)/(SR*.08))*np.minimum(1,(N-1-np.arange(N))/(SR*.25))
raw=voice+music+fx;sf.write(P/'.cache/pre-master.wav',raw,SR,subtype='PCM_24')
def metric(log):return json.JSONDecoder().raw_decode(log[log.rfind('{'):])[0]
base=['ffmpeg','-hide_banner','-nostats','-i',str(P/'.cache/pre-master.wav')]
a=metric(subprocess.run(base+['-af','loudnorm=I=-16:TP=-2:LRA=8:print_format=json','-f','null','-'],capture_output=True,text=True,check=True).stderr)
filt=f'loudnorm=I=-16:TP=-2:LRA=8:measured_I={a["input_i"]}:measured_TP={a["input_tp"]}:measured_LRA={a["input_lra"]}:measured_thresh={a["input_thresh"]}:offset={a["target_offset"]}:linear=true:print_format=json'
b=metric(subprocess.run(base+['-y','-af',filt,'-ar','48000','-c:a','flac',str(P/'audio/mix20.flac')],capture_output=True,text=True,check=True).stderr)
(P/'reports/mix.json').write_text(json.dumps({'source':a,'master':b,'speech_speed_changed':False,'human_auditioned':False,'events':events},indent=2)+'\n')
(P/'audio/rights.json').write_text(json.dumps({'voices':'User-authorized paid OpenAI tts-1-hd for 20-second sample only: Alloy narrator, Onyx Vale, Nova Mina. Native speed1; no revoice or speech tempo changes.','music':'Original locally authored procedural pizzicato cue, scripts/mix20.py; no third-party music or paid generation.','effects':'Original locally synthesized rubber steps, clip/button and motor; no stock recording licenses needed.','artwork':'Original local 2D cast and sets, copied from this project own gym-museum-v1 and refined for this sample.','font':'Noto Sans, installed skill font; upstream font license retained in repository.'},indent=2)+'\n');print('Mix complete',b['output_i'],b['output_tp'])
