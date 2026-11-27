from pathlib import Path
import os
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
import sys,json,subprocess,hashlib,math,time
from concurrent.futures import ProcessPoolExecutor,as_completed
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P));import film
assert film.TURNS and film.WORDS
N=round(film.T['duration']*30);FP=hashlib.sha256(b''.join((P/n).read_bytes() for n in ['artwork.py','film.py','scenes.py','staging.py','motion.py','gait.py','locomotion_art.py','turns.json','captions.json'])).hexdigest()
def encode(job):
 a,b,name=job;out=P/'output'/name;report=out.with_suffix('.json')
 if report.exists() and out.exists():
  r=json.loads(report.read_text())
  if r.get('fingerprint')==FP:return r
 proc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','30','-i','-','-an','-c:v','libx264','-crf','20','-preset','fast','-threads','1','-pix_fmt','yuv420p',str(out)],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
 try:
  for f in range(a,b):
   im,_=film.frame(f/30);proc.stdin.write(im.tobytes())
  proc.stdin.close();err=proc.stderr.read().decode();assert proc.wait()==0,err
 except Exception:
  proc.kill();proc.wait();raise
 r={'file':name,'fingerprint':FP,'first':a,'last_exclusive':b,'frames':b-a};report.write_text(json.dumps(r)+'\n');return r
if __name__=='__main__':
 jobs=[(a,min(N,a+600),f'part-{a//600:02d}.mp4') for a in range(0,N,600)];rows=[]
 with ProcessPoolExecutor(max_workers=4) as pool:
  for f in as_completed([pool.submit(encode,j) for j in jobs]):rows.append(f.result());print('FINISHED',rows[-1]['file'],flush=True)
 rows.sort(key=lambda r:r['first']);(P/'output/render-report.json').write_text(json.dumps({'frames':N,'fps':30,'parts':rows,'fingerprint':FP},indent=2)+'\n');(P/'output/concat.txt').write_text(''.join("file '"+r['file']+"'\n" for r in rows));subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(P/'output/concat.txt'),'-c','copy',str(P/'output/picture.mp4')],check=True)
