from pathlib import Path
import os
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
import sys,json,subprocess,hashlib,math,time
from concurrent.futures import ProcessPoolExecutor,as_completed
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P));import film
N=round(film.T['duration']*30);FP=hashlib.sha256(b''.join((P/n).read_bytes() for n in ['artwork.py','film.py','turns.json','words.json'])).hexdigest()
def encode(job):
 a,b,name=job;out=P/'output'/name;report=out.with_suffix('.json')
 if report.exists() and out.exists():
  r=json.loads(report.read_text())
  if r.get('fingerprint')==FP:return r
 proc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','30','-i','-','-an','-c:v','libx264','-crf','19','-preset','fast','-threads','1','-pix_fmt','yuv420p',str(out)],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
 start=time.monotonic()
 try:
  for f in range(a,b):
   im,shot=film.frame(f/30);proc.stdin.write(im.tobytes())
   if (f-a)%180==0:print(name,f-a,'/',b-a,flush=True)
  proc.stdin.close();err=proc.stderr.read().decode();assert proc.wait()==0,err
 except Exception:
  proc.kill();proc.wait();raise
 r={'file':name,'fingerprint':FP,'first':a,'last_exclusive':b,'frames':b-a,'seconds':time.monotonic()-start,'resolution':[1920,1080],'native_artwork':'All geometry and type rasterized at output pixel scale, including camera views; no720p raster upscaling.'};report.write_text(json.dumps(r,indent=2)+'\n');return r
if __name__=='__main__':
 if '--trial' in sys.argv:
  turn=next(x for x in film.TURNS if x['scene']==3);first=round(turn['start']*30);last=min(N,first+600);print(json.dumps(encode((first,last,'motion-trial-20s-silent.mp4'))));(P/'output/trial-span.json').write_text(json.dumps({'start':first/30,'duration':(last-first)/30})+'\n')
 else:
  jobs=[(a,min(N,a+600),f'part-{a//600:02d}.mp4') for a in range(0,N,600)];rows=[]
  with ProcessPoolExecutor(max_workers=4) as pool:
   for f in as_completed([pool.submit(encode,j) for j in jobs]):rows.append(f.result());print('FINISHED',rows[-1]['file'],flush=True)
  rows.sort(key=lambda r:r['first']);(P/'output/render-report.json').write_text(json.dumps({'frames':N,'fps':30,'parts':rows,'fingerprint':FP},indent=2)+'\n');(P/'output/concat.txt').write_text(''.join("file '"+r['file']+"'\n" for r in rows));subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(P/'output/concat.txt'),'-c','copy',str(P/'output/picture.mp4')],check=True)
