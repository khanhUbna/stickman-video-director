from pathlib import Path
import sys,json,subprocess,hashlib,math,shutil
from PIL import Image,ImageDraw,ImageStat,ImageChops
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P));import film
D=P.parents[1]/'deliveries/dishwasher-trial-v1';F=D/'your-dishwasher-thinks-youre-the-problem-1080p.mp4';R=P/'reports';raw=P/'output/decoded';raw.mkdir(exist_ok=True)
def run(a):return subprocess.run(a,check=True,capture_output=True,text=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
info=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(F)]).stdout);v=next(x for x in info['streams'] if x['codec_type']=='video');a=next(x for x in info['streams'] if x['codec_type']=='audio');assert (v['width'],v['height'],v['r_frame_rate'])==(1920,1080,'30/1');assert int(v['nb_frames'])==round(film.T['duration']*30);assert abs(float(info['format']['duration'])-film.T['duration'])<.05
rr=json.loads((P/'output/render-report.json').read_text());current=hashlib.sha256(b''.join((P/n).read_bytes() for n in ['artwork.py','film.py','turns.json','words.json'])).hexdigest();assert rr['fingerprint']==current;assert all(p['fingerprint']==current for p in rr['parts'])
decode=run(['ffmpeg','-v','error','-i',str(F),'-f','null','-']);assert not decode.stderr.strip(),decode.stderr
log=run(['ffmpeg','-hide_banner','-nostats','-i',str(F),'-af','loudnorm=I=-16:TP=-2:print_format=json','-f','null','-']).stderr;measure=json.JSONDecoder().raw_decode(log[log.rfind('{'):])[0];assert -18<float(measure['input_i'])<-14;assert float(measure['input_tp'])<-1
assert ' '.join(w['text'] for w in film.WORDS).split()==(P/'script-en.txt').read_text().split();assert ' '.join(c['text'] for c in film.CUES).split()==(P/'script-en.txt').read_text().split();assert all(c['end']>c['start']>=0 for c in film.CUES)
frames=[];comparisons=[]
for i,s in enumerate(film.SHOTS):
 t=round((s['start']+.63*(s['end']-s['start']))*30)/30;out=raw/f'{i+1:02d}-{s["mode"]}.jpg';run(['ffmpeg','-v','error','-y','-ss',f'{t:.9f}','-i',str(F),'-frames:v','1','-q:v','2',str(out)]);im=Image.open(out).convert('RGB');assert sum(ImageStat.Stat(im).stddev)>30
 frames.append({'shot':s['id'],'mode':s['mode'],'time':t,'file':out.name})
 if i%9==0 or s['mode']=='arrange':
  ref,_=film.frame(t);err=sum(ImageStat.Stat(ImageChops.difference(im,ref)).mean)/3;assert err<8,(s,err);comparisons.append({'shot':s['id'],'rgb_mean_absolute_error':err})
for n in range(math.ceil(len(frames)/32)):
 group=frames[n*32:(n+1)*32];sheet=Image.new('RGB',(1600,math.ceil(len(group)/4)*250),'#efe4ce');d=ImageDraw.Draw(sheet)
 for i,r in enumerate(group):x=i%4*400;y=i//4*250;sheet.paste(Image.open(raw/r['file']).resize((400,225)),(x,y));d.text((x+4,y+229),f'{r["shot"]} {r["time"]:.2f} {r["mode"]}',fill='black')
 sheet.save(R/f'decoded-sheet-{n+1}.jpg',quality=93)
for mode in ['load','arm','filter','arrange','verdict','water','judge']:
 r=next(r for r in frames if r['mode']==mode);shutil.copy2(raw/r['file'],R/f'detail-{mode}.jpg')
start=next(t['start'] for t in film.TURNS if t['scene']==3);run(['ffmpeg','-v','error','-y','-ss',str(start),'-i',str(F),'-t','20','-c:v','libx264','-crf','18','-preset','fast','-c:a','aac','-b:a','192k','-movflags','+faststart',str(R/'motion-trial-20s.mp4')])
ledger=json.loads((P/'audio/tts-ledger.json').read_text());qa={'ok':True,'sha256':sha(F),'bytes':F.stat().st_size,'duration':float(info['format']['duration']),'resolution':[v['width'],v['height']],'fps':v['r_frame_rate'],'frames':int(v['nb_frames']),'audio_codec':a['codec_name'],'audio_sample_rate':a['sample_rate'],'integrated_lufs':float(measure['input_i']),'true_peak_dbtp':float(measure['input_tp']),'decode_errors':decode.stderr,'native_artwork':True,'shots':len(film.SHOTS),'caption_cues':len(film.CUES),'words':len(film.WORDS),'script_sha256':sha(P/'script-en.txt'),'reference_comparisons':comparisons,'decoded_shots':frames,'source_fingerprint':current,'tts_requests':len(ledger),'voices':{r['role']:r['voice'] for r in ledger},'estimated_voice_usd':sum(r['estimated_usd'] for r in ledger),'budget_usd':.20,'invoice_accessed':False,'other_paid_calls':0,'speech_speed_changed':False,'visual_review':'Pending independent final decoded-frame review','audio_review':'Measured, not human-auditioned','style_scope':'Original channel-specific2D cartoon; no exact B2/B6 sample-equivalence claim','youtube_published':False}
(R/'QA.json').write_text(json.dumps(qa,indent=2)+'\n');assert qa['bytes']<100_000_000;print(json.dumps({k:qa[k] for k in ['ok','duration','bytes','integrated_lufs','true_peak_dbtp','shots','words','estimated_voice_usd']}),flush=True)
