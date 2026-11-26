from pathlib import Path
import sys,subprocess,json,hashlib,time
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P));import film
from PIL import ImageDraw
out=P/'reports/motion-study-20s-silent.mp4'
proc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','30','-i','-','-an','-c:v','libx264','-crf','20','-preset','fast','-threads','2','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],stdin=subprocess.PIPE)
shots=[('bench',2,0),('clip',6,4),('walk',6,5),('handshake',2,4)]
for i in range(600):
 t=i/30;k=min(3,i//150);local=t-k*5;mode,scene,line=shots[k];u=min(1,local/3.4)
 im=film.view(mode,t,u,'',scene,line,0,local);d=ImageDraw.Draw(im);d.rounded_rectangle((20,1000,835,1055),8,'#fff4d9');d.text((39,1009),'MOTION STUDY · SILENT · TIMING NOT FINAL',font=film.A.font(25),fill=film.A.INK);proc.stdin.write(im.tobytes())
 if i%150==0:print('Preview',i,'/ 600',flush=True)
proc.stdin.close();assert proc.wait()==0
subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True)
info=json.loads(subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out)],capture_output=True,text=True,check=True).stdout)
(P/'reports/preview-technical.json').write_text(json.dumps({'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'duration':info['format']['duration'],'width':1920,'height':1080,'fps':30,'frames':600,'source_fingerprint':hashlib.sha256((P/'artwork.py').read_bytes()+(P/'film.py').read_bytes()).hexdigest(),'audio':'intentionally absent; budget approval pending','scope':'Four body/contact motion studies, NOT complete film or final timing','decode_errors':0},indent=2)+'\n');print('Preview saved:',out,flush=True)
