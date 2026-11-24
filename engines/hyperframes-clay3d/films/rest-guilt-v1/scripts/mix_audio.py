"""Reuse the creator's original score/Foley and synchronize it to this film's actual motion."""
from pathlib import Path
import json,subprocess,hashlib
import numpy as np
import soundfile as sf
ROOT=Path(__file__).resolve().parents[1]
T=json.loads((ROOT/'assets/timeline.json').read_text()); SR=48000;N=round(T['duration']*SR)
OLD=Path('/workspace/scratch/rest-guilt-long-v1/audio')
EVENINGS=Path('/workspace/scratch/long-evenings-v1/audio')
def read(file):
    pcm=subprocess.run(['ffmpeg','-v','error','-i',str(file),'-ar',str(SR),'-ac','1','-f','f32le','-'],check=True,capture_output=True).stdout
    return np.frombuffer(pcm,dtype='<f4').copy()
def pad(a):
    out=np.zeros(N,dtype=np.float32);out[:min(N,len(a))]=a[:N];return out
voice=pad(read(ROOT/'assets/voice/narration.flac'))
music_source=OLD/'music-original.wav';music=pad(read(music_source))
voice_rms=float(np.sqrt(np.mean(voice**2)));music_rms=float(np.sqrt(np.mean(music**2)))
music*=min(3.0,voice_rms*.085/max(music_rms,1e-9))
room=np.resize(read(OLD/'room-original.wav'),N)*.85
foley=np.zeros(N,dtype=np.float32);events=[]
old_events=json.loads((OLD/'sound-events.json').read_text());old_foley=read(OLD/'foley-original.wav')
evening_events=json.loads((EVENINGS/'sound-events.json').read_text());evening_foley=read(EVENINGS/'foley-original.wav')
def sample(kind,seconds=.18,evening=False):
    source=evening_foley if evening else old_foley;ledger=evening_events if evening else old_events
    event=next(e for e in ledger if e['kind']==kind);start=max(0,round(event['time']*SR));a=source[start:start+round(seconds*SR)].copy()
    if len(a):a*=np.minimum(1,np.arange(len(a))/(SR*.003))*np.minimum(1,(len(a)-1-np.arange(len(a)))/(SR*.02))
    return a
bank={'step':sample('step',.12),'seat':sample('seat',.18),'phone':sample('phone_on_wood',.12),'paper':sample('pen_on_paper',.30),'plate':sample('plate_on_counter',.18),'close':sample('laptop_close',.18),'key':sample('case_latch',.16,True),'water':sample('water_pour',1.40),'wash':sample('wash_contact',.24,True)}
def add(at,kind,gain=1):
    a=bank[kind];start=round(at*SR);length=min(len(a),N-start)
    if start>=0 and length>0:foley[start:start+length]+=a[:length]*gain;events.append({'time':round(at,5),'kind':kind,'source':'Creator-owned original Foley stem, reused and resynchronized'})
motion_path=ROOT/'output/motion-audit.json'
assert motion_path.exists(),'Use the actual motion audit before placing footsteps'
motion=json.loads(motion_path.read_text());assert not motion['errors']
for landing in motion['landings']:add(landing['time'],'step',.7)
for s in T['shots']:
    start=s['start'];d=s['duration'];a=s['action'];at=lambda u:start+d*u
    if a=='keys':add(at(.18),'key',.8);add(at(.48),'key',.5)
    if a in ('phone_movie','phone_question','phone_reply','unsent_insert','timer_insert'):add(at(.10),'phone',.35)
    if a in ('sit_play','sit_back','startle'):add(at(.67),'seat',.6)
    if a=='write_note':
        for time in np.arange(at(.1),at(.60),.4):add(float(time),'paper',.45)
    if a=='close_laptop':add(at(.78),'close',.8)
    if a=='faucet_off':add(at(.36),'key',.35);add(at(.74),'plate',.65)
    if a in ('wash','roommate_arrive','almost_excuse'):
        for time in np.arange(start,s['end'],1.35):add(float(time),'water',.30)
    if a=='wash':
        for time in np.arange(at(.12),at(.85),.72):add(float(time),'wash',.35)
    if a=='set_snack':add(at(.73),'plate',.5)
    if a=='snack_grab':add(at(.30),'plate',.3)
fade=np.minimum(1,np.arange(N)/(SR*.18))*np.minimum(1,(N-1-np.arange(N))/(SR*1.5));foley*=fade.astype(np.float32);room*=fade.astype(np.float32)
raw=voice+music+room+foley
sf.write(ROOT/'.cache/mix-unmastered.wav',raw,SR,subtype='PCM_24')
command=['ffmpeg','-hide_banner','-nostats','-i',str(ROOT/'.cache/mix-unmastered.wav'),'-af','loudnorm=I=-16:TP=-2:LRA=9:print_format=json','-f','null','-']
probe=subprocess.run(command,capture_output=True,text=True,check=True).stderr
measure=json.JSONDecoder().raw_decode(probe[probe.rfind('{'):])[0]
filter=f'loudnorm=I=-16:TP=-2:LRA=9:measured_I={measure["input_i"]}:measured_TP={measure["input_tp"]}:measured_LRA={measure["input_lra"]}:measured_thresh={measure["input_thresh"]}:offset={measure["target_offset"]}:linear=true:print_format=json'
result=subprocess.run(['ffmpeg','-hide_banner','-nostats','-y','-i',str(ROOT/'.cache/mix-unmastered.wav'),'-af',filter,'-ar',str(SR),'-c:a','flac',str(ROOT/'.cache/mix-mastered.flac')],capture_output=True,text=True,check=True)
master=json.JSONDecoder().raw_decode(result.stderr[result.stderr.rfind('{'):])[0]
(ROOT/'.cache/mix-mastered.flac').replace(ROOT/'assets/mix.flac')
(ROOT/'assets/sound-events.json').write_text(json.dumps(events,indent=2)+'\n')
(ROOT/'assets/audio-measurements.json').write_text(json.dumps({'pre_master':measure,'master':master,'voice_rms':voice_rms,'music_ratio_target':.085,'motion_landings':len(motion['landings']),'effects':len(events),'music_original_sha256':hashlib.sha256(music_source.read_bytes()).hexdigest(),'measurement_only_not_human_audition':True,'paid_api_calls':0},indent=2)+'\n')
print(json.dumps({'duration':T['duration'],'motion_landings':len(motion['landings']),'effects':len(events),'master_I':master.get('output_i'),'master_TP':master.get('output_tp')}))
