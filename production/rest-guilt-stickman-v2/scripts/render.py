"""Deterministic native 2D frames; local worker processes, not agents or API calls."""
from pathlib import Path
import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import sys,json,subprocess,math,time,hashlib
from concurrent.futures import ProcessPoolExecutor,as_completed
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P));import film
FPS=30;N=round(film.T['duration']*FPS)
FINGERPRINT=hashlib.sha256(b''.join((P/n).read_bytes() for n in ['film.py','rig.py','timeline.json','captions.json','caption-profile.json'])).hexdigest()
def encode(job):
 index,first,last,name=job;target=P/'output'/name;trace=target.with_suffix('.json')
 if target.exists() and trace.exists():
  cached=json.loads(trace.read_text())
  if cached.get('fingerprint')==FINGERPRINT:return cached
 cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','18','-threads','1','-pix_fmt','yuv420p',str(target)]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE);maxbone=0;maxgrip=0;maxdrift=0;landings=[];previous=None;start=time.monotonic()
 try:
  for frame in range(first,last):
   t=frame/FPS;image,rows,events,s=film.frame(t)
   for row in rows:maxbone=max(maxbone,row['bone_error']);maxgrip=max(maxgrip,max(row['contacts'].values(),default=0))
   if previous and previous[0]==s['id']:
    before={r['who']:r for r in previous[1]}
    for row in rows:
     if row['who'] in before:
      for side in ['left','right']:
       if not before[row['who']]['legs'][side]['planted'] and row['legs'][side]['planted']:landings.append({'time':t,'who':row['who'],'side':side,'shot':s['id']})
       if before[row['who']]['legs'][side]['planted'] and row['legs'][side]['planted']:
        import numpy as np
        maxdrift=max(maxdrift,float(np.linalg.norm(np.asarray(before[row['who']]['legs'][side]['joints'][-1])-row['legs'][side]['joints'][-1])))
   previous=(s['id'],rows);proc.stdin.write(image.tobytes())
   if (frame-first)%150==0:print(f'{name}: {frame-first}/{last-first}',flush=True)
  proc.stdin.close();error=proc.stderr.read().decode();code=proc.wait();assert code==0,error
 except Exception as error:
  proc.kill();proc.wait();raise RuntimeError(f'{name}: frame {frame}, time {t}, shot {s["id"]}: {error}') from error
 assert maxdrift<1e-6,(name,'World stance drift',maxdrift)
 report={'file':name,'fingerprint':FINGERPRINT,'first_frame':first,'last_frame_exclusive':last,'frames':last-first,'maximum_bone_error':maxbone,'maximum_grip_error':maxgrip,'maximum_world_stance_drift':maxdrift,'landings':landings,'seconds':time.monotonic()-start}
 trace.write_text(json.dumps(report,indent=2)+'\n');return report
if __name__=='__main__':
 if '--trial' in sys.argv:
  s=next(s for s in film.SHOTS if s['action']=='hurry');first=math.floor(s['start']*FPS);last=min(N,first+300);print(json.dumps(encode((0,first,last,'motion-trial-10s-silent.mp4'))));(P/'output/trial-span.json').write_text(json.dumps({'start':first/FPS,'duration':(last-first)/FPS})+'\n')
 else:
  jobs=[(i//600,i,min(N,i+600),f'part-{i//600:02d}.mp4') for i in range(0,N,600)];reports=[]
  with ProcessPoolExecutor(max_workers=4) as pool:
   for future in as_completed([pool.submit(encode,j) for j in jobs]):
    r=future.result();reports.append(r);print('COMPLETED',r['file'],flush=True)
  reports.sort(key=lambda r:r['first_frame']);(P/'output/render-report.json').write_text(json.dumps({'frames':N,'fps':FPS,'width':1280,'height':720,'parts':reports,'paid_render_calls':0},indent=2)+'\n')
  (P/'output/concat.txt').write_text(''.join(f"file '{r['file']}'\n" for r in reports))
  subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(P/'output/concat.txt'),'-c','copy',str(P/'output/picture.mp4')],check=True)
