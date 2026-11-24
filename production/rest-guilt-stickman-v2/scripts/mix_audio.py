"""Creator-owned original score/Foley, synchronized to this new 2D performance."""
from pathlib import Path
import json,subprocess,hashlib
import numpy as np
import soundfile as sf
P=Path(__file__).resolve().parents[1];T=json.loads((P/'timeline.json').read_text());SR=48000;N=round(T['duration']*SR)
OLD=Path('/workspace/scratch/rest-guilt-long-v1/audio');OTHER=Path('/workspace/scratch/long-evenings-v1/audio')
def read(file):
 raw=subprocess.run(['ffmpeg','-v','error','-i',str(file),'-ar',str(SR),'-ac','1','-f','f32le','-'],check=True,capture_output=True).stdout;return np.frombuffer(raw,dtype='<f4').copy()
def pad(a):
 out=np.zeros(N,dtype=np.float32);out[:min(N,len(a))]=a[:N];return out
voice=pad(read(P/'audio/narration.flac'));music=pad(read(OLD/'music-original.wav'));room=np.resize(read(OLD/'room-original.wav'),N)*.65
rms=lambda a:float(np.sqrt(np.mean(a*a)))
music*=min(3,rms(voice)*.075/max(rms(music),1e-8));fade=np.minimum(1,np.arange(N)/(SR*.25))*np.minimum(1,(N-1-np.arange(N))/(SR*1.8));music*=fade;room*=fade
old=read(OLD/'foley-original.wav');events0=json.loads((OLD/'sound-events.json').read_text());other=read(OTHER/'foley-original.wav');events1=json.loads((OTHER/'sound-events.json').read_text())
def sample(kind,duration=.18,secondary=False):
 ledger=events1 if secondary else events0;stem=other if secondary else old;at=next(e['time'] for e in ledger if e['kind']==kind);a=stem[round(at*SR):round((at+duration)*SR)].copy();a*=np.minimum(1,np.arange(len(a))/(SR*.003))*np.minimum(1,(len(a)-1-np.arange(len(a)))/(SR*.018));return a
bank={'step':sample('step',.12),'seat':sample('seat'),'phone':sample('phone_on_wood',.12),'pen':sample('pen_on_paper',.25),'plate':sample('plate_on_counter'),'close':sample('laptop_close'),'key':sample('case_latch',.16,True),'water':sample('water_pour',1.4),'wash':sample('wash_contact',.2,True)}
t=np.arange(round(SR*.12))/SR;bank['alarm']=(.055*np.sin(2*np.pi*880*t)*np.sin(np.pi*np.minimum(1,t/.12))**2).astype(np.float32)
effects=np.zeros(N,dtype=np.float32);ledger=[]
def add(at,kind,gain=1,until=None):
 start=round(at*SR);a=bank[kind].copy();length=min(len(a),N-start)
 if until is not None:length=min(length,max(0,round((until-at)*SR)))
 if start<0 or length<=0:return
 a=a[:length];a*=np.minimum(1,(length-1-np.arange(length))/(SR*.012));effects[start:start+length]+=a*gain;ledger.append({'time':round(at,5),'kind':kind,'end':round(at+length/SR,5),'source':'Original designed Foley reused locally' if kind!='alarm' else 'Locally synthesized device-alarm effect'})
report=json.loads((P/'output/render-report.json').read_text());landings=[e for r in report['parts'] for e in r['landings']]
for e in landings:add(e['time'],'step',.7)
for s in T['shots']:
 start,end,a=s['start'],s['end'],s['action']
 if a=='keys':add(start+.18,'key',.8)
 if a=='timer_insert':add(start+.18,'alarm',.8);add(start+.42,'alarm',.7)
 if a in ['phone_reply','phone_question','unsent_insert']:add(start+.16,'phone',.3)
 if a=='set_snack':add(start+.5,'plate',.45)
 if a=='close_laptop':add(start+.85,'close',.7)
 if a=='write_note':
  for t in [.15,.4,.65,.9]:add(start+t,'pen',.4)
 if a=='sit_play':add(start+.45,'seat',.5);add(start+.8,'plate',.35);add(start+.94,'phone',.25)
 if a=='sit_back':add(start+.5,'seat',.5)
 if a=='startle':add(start+.35,'phone',.4);add(start+.9,'seat',.3)
 if a=='faucet_off':add(start+.5,'key',.3);add(start+1.22,'plate',.6)
 if a in ['wash','roommate_arrive','almost_excuse','faucet_off']:
  stop=min(end,start+.55) if a=='faucet_off' else end
  for at in np.arange(start,stop,1.3):add(float(at),'water',.26,stop)
 if a=='wash':
  for at in np.arange(start+.15,end,.6):add(float(at),'wash',.28,end)
effects*=fade
sf.write(P/'.cache/mix-raw.wav',voice+music+room+effects,SR,subtype='PCM_24')
def measurement(log):return json.JSONDecoder().raw_decode(log[log.rfind('{'):])[0]
base=['ffmpeg','-hide_banner','-nostats','-i',str(P/'.cache/mix-raw.wav')]
first=measurement(subprocess.run(base+['-af','loudnorm=I=-16:TP=-2:LRA=9:print_format=json','-f','null','-'],check=True,capture_output=True,text=True).stderr)
af=f'loudnorm=I=-16:TP=-2:LRA=9:measured_I={first["input_i"]}:measured_TP={first["input_tp"]}:measured_LRA={first["input_lra"]}:measured_thresh={first["input_thresh"]}:offset={first["target_offset"]}:linear=true:print_format=json'
second=measurement(subprocess.run(base+['-y','-af',af,'-ar',str(SR),'-c:a','flac',str(P/'.cache/master.flac')],check=True,capture_output=True,text=True).stderr);(P/'.cache/master.flac').replace(P/'audio/mix.flac')
(P/'audio/sound-events.json').write_text(json.dumps(ledger,indent=2)+'\n');(P/'audio/mix-measurements.json').write_text(json.dumps({'first_pass':first,'master':second,'footsteps_from_actual_animation':len(landings),'effects':len(ledger),'music_to_voice_rms_target':.075,'audio_review':'Measured, not human-auditioned','new_music_api_calls':0,'new_transcription_api_calls':0,'music_original_sha256':hashlib.sha256((OLD/'music-original.wav').read_bytes()).hexdigest()},indent=2)+'\n')
(P/'audio/rights.json').write_text(json.dumps({'voice':'OpenAI tts-1-hd/alloy; one user-authorized recording, native speed1. See tts-request.json and authorization.json.','music':'Creator-owned original instrumental from earlier rest-guilt-long-v1; reused, level balanced and faded to this ending.','foley':'Creator-owned original locally synthesized/designed Foley from rest-guilt-long-v1 and long-evenings-v1, resynchronized to actual body contacts.','alarm':'Original local synthesized device sound; no music-generation service.','new_paid_voice_calls':1,'new_paid_image_music_video_transcription_calls':0,'ai_voice_disclosure':'Narration is an AI-generated voice.'},indent=2)+'\n')
print(json.dumps({'duration':T['duration'],'footsteps':len(landings),'effects':len(ledger),'master':second}))
