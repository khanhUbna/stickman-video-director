from pathlib import Path
import sys,subprocess,json,hashlib
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P));import film
out=P/'output/picture20.mp4';proc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','30','-i','-','-an','-c:v','libx264','-crf','19','-preset','fast','-threads','2','-pix_fmt','yuv420p',str(out)],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
try:
 for i in range(600):
  im,_=film.frame(i/30);proc.stdin.write(im.tobytes())
  if i%150==0:print('Frames',i,'/600',flush=True)
 proc.stdin.close();err=proc.stderr.read().decode();assert proc.wait()==0,err
except Exception:proc.kill();proc.wait();raise
names=['artwork.py','film.py','gait.py','locomotion_art.py','turns20.json','captions20.json','mouth-levels.json'];(P/'reports/render.json').write_text(json.dumps({'frames':600,'fps':30,'resolution':[1920,1080],'source_fingerprint':hashlib.sha256(b''.join((P/n).read_bytes() for n in names)).hexdigest(),'inputs':names,'speech_timing':'actual local alignment'},indent=2)+'\n');print('Picture done',flush=True)
