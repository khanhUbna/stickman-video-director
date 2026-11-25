from pathlib import Path
import os
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
import sys,json,bisect,hashlib,subprocess
from concurrent.futures import ProcessPoolExecutor,as_completed
from PIL import ImageDraw
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P));import film,artwork as A
sys.path.insert(0,str(P/'scripts'));import render as R
CUES=json.loads((P/'captions-vi.json').read_text());START=[c['start'] for c in CUES];original=film.frame
R.FP=hashlib.sha256(('vi:'+R.FP).encode()+(P/'captions-vi.json').read_bytes()+Path(__file__).read_bytes()).hexdigest()
def localized(t,captions=True):
 im,s=original(t,captions=False);idx=bisect.bisect_right(START,t)-1
 if idx>=0 and CUES[idx]['start']<=t<=CUES[idx]['end']:
  c=CUES[idx];d=ImageDraw.Draw(im);f=A.font(40,1.5);b=d.textbbox((0,0),c['text'],font=f);w=b[2]-b[0];assert w<1740
  y=978;d.rounded_rectangle((960-w/2-22,y-12,960+w/2+22,y+80),radius=10,fill='#fff8e8',outline='#d3c4a7',width=2);d.text((960-w/2,y),c['text'],font=f,fill=A.INK)
 return im,s
film.frame=localized
if __name__=='__main__':
 if '--stills' in sys.argv:
  for t in [1.5,8,10.5,61.5,98.6,108.7,152.5,173,193]:localized(t)[0].save(P/'reports'/f'vi-preview-{t}.jpg')
 else:
  jobs=[(a,min(R.N,a+600),f'vi-part-{a//600:02d}.mp4') for a in range(0,R.N,600)];rows=[]
  with ProcessPoolExecutor(max_workers=4) as pool:
   for f in as_completed([pool.submit(R.encode,j) for j in jobs]):rows.append(f.result());print('FINISHED',rows[-1]['file'],flush=True)
  rows.sort(key=lambda x:x['first']);(P/'output/vi-render-report.json').write_text(json.dumps({'frames':R.N,'fps':30,'parts':rows,'fingerprint':R.FP,'caption_language':'vi'},indent=2)+'\n');(P/'output/concat-vi.txt').write_text(''.join("file '"+x['file']+"'\n" for x in rows));subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(P/'output/concat-vi.txt'),'-c','copy',str(P/'output/picture-vi.mp4')],check=True)
