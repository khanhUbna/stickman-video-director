"""Meaningful kinematic checks for the creator's rejected robotic gait.
Not a substitute for watching the film at1x; outputs physical contact evidence.
"""
from pathlib import Path
import sys,math,json,hashlib
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P));import artwork as A,gait as G,locomotion_art as L,film
poly=[(-11,-2),(-4,-10),(13,-10),(25,-2),(24,5),(-10,5)]
max_chain_error=0.;max_floor_drift=0.;max_belt_error=0.;min_clearance=999;max_jump=0.;samples=0;last={}
for role,start,end in [('VALE',2.30,5.14),('MINA',9.45,10.814),('VALE',14.57,19.999)]:
 for j in range(round((end-start)*120)):
  t=start+j/120;state=G.pose(t,role)
  for i,f in enumerate(state['feet']):
   key=(role,start,i);old=last.get(key)
   pts=[(f['ankle'][0]+G.rotate(p,f['angle'],f['direction'])[0],f['ankle'][1]+G.rotate(p,f['angle'],f['direction'])[1]) for p in poly]
   clear=f['ground']-max(p[1] for p in pts);min_clearance=min(min_clearance,clear);assert clear>-.02,(role,t,clear)
   if old:
    jump=math.dist(f['ankle'],old[1]['ankle']);max_jump=max(max_jump,jump)
    if f['contact']!='air' and f['contact']==old[1]['contact']:
     dx=f['pivot'][0]-old[1]['pivot'][0]
     if start>=14.57:max_belt_error=max(max_belt_error,abs(dx+G.BELT_SPEED/120))
     else:max_floor_drift=max(max_floor_drift,abs(dx))
   last[key]=(t,f)
  # Actual emitted upper/lower chains, including held-rail endpoints.
  if j%4==0:
   c=A.C();r=L.render(c,t,role,hand=(770,456) if start>=14.57 else None,left=(710,456) if start>=14.57 else None)
   for chain,lengths in [(x,[68,68]) for x in r['legs']]+[(x,[72,68]) for x in r['arms']]:
    for a,b,n in zip(chain,chain[1:],lengths):max_chain_error=max(max_chain_error,abs(math.dist(a,b)-n))
  samples+=1
assert max_floor_drift<1e-6,max_floor_drift
assert max_belt_error<1e-6,max_belt_error
assert max_chain_error<1e-6,max_chain_error
assert max_jump<8,('unexpected ankle snap at120Hz',max_jump)
for i in range(600):film.frame(i/30)
old=P.parent/'gym-museum-preview-v1'
for name in ['dialogue20.flac','narrator-native.wav','vale-native.wav','mina-native.wav']:
 assert hashlib.sha256((P/'audio'/name).read_bytes()).hexdigest()==hashlib.sha256((old/'audio'/name).read_bytes()).hexdigest()
assert (P/'captions20.json').read_bytes()==(old/'captions20.json').read_bytes()
report={'samples_120hz':samples,'max_segment_length_error_px':max_chain_error,'max_planted_floor_pivot_drift_px':max_floor_drift,'max_belt_pivot_speed_error_px_per_120hz_step':max_belt_error,'minimum_shoe_clearance_px':min_clearance,'maximum_ankle_displacement_per_120hz_step_px':max_jump,'all_600_actual_frames_rendered':True,'saved_voice_hashes_identical':True,'captions_identical':True,'additional_paid_calls':0,'scope':'Physical continuity evidence only; naturalness is a creative/perceptual judgment.'}
(P/'reports/motion-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)
