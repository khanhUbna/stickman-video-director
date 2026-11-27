from pathlib import Path
import json,subprocess,hashlib,sys
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P));import film
D=P.parents[1]/'deliveries/gym-museum-full-v1';F=D/'they-found-a-gym-and-got-it-wrong-en-1080p.mp4'
def run(a):return subprocess.run(a,capture_output=True,text=True,check=True)
meta=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(F)]).stdout);v=next(x for x in meta['streams'] if x['codec_type']=='video');a=next(x for x in meta['streams'] if x['codec_type']=='audio');assert(v['width'],v['height'],v['r_frame_rate'])==(1920,1080,'30/1');assert int(v['nb_frames'])==round(film.T['duration']*30);assert abs(float(meta['format']['duration'])-film.T['duration'])<.05
run(['ffmpeg','-v','error','-i',str(F),'-f','null','-'])
log=run(['ffmpeg','-hide_banner','-nostats','-i',str(F),'-af','loudnorm=I=-16:TP=-2:print_format=json','-f','null','-']).stderr;measure=json.JSONDecoder().raw_decode(log[log.rfind('{'):])[0];assert -18<float(measure['input_i'])<-14;assert float(measure['input_tp'])<-1
assert ' '.join(w['text'] for w in film.WORDS).split()==' '.join(c['text'] for c in film.CUES).split()==(P/'script-en.txt').read_text().split();assert all(c['end']>c['start']>=0 for c in film.CUES)
ledger=json.loads((P/'audio/tts-ledger.json').read_text());assert len(ledger)==7 and all(x['state']=='saved' for x in ledger);cost=sum(x['estimated_usd'] for x in ledger)+.0084;assert cost<=.2
rows=[]
for i,s in enumerate(film.SHOTS):
 t=(s['start']+s['end'])/2;f=P/'reports'/f'encoded-{i:03d}.jpg';run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(F),'-frames:v','1','-q:v','3',str(f)]);rows.append((s,f,t))
for j in range((len(rows)+23)//24):
 sheet=Image.new('RGB',(1536,1440),'white');dr=ImageDraw.Draw(sheet)
 for k,(s,f,t) in enumerate(rows[j*24:(j+1)*24]):
  im=Image.open(f);im.thumbnail((384,216));x=k%4*384;y=k//4*240;sheet.paste(im,(x,y));dr.text((x+4,y+219),f'{t:.1f} {s["mode"]}',fill='black')
 sheet.save(P/'reports'/f'encoded-sheet-{j+1}.jpg')
q={'file':F.name,'sha256':hashlib.sha256(F.read_bytes()).hexdigest(),'duration':float(meta['format']['duration']),'bytes':F.stat().st_size,'resolution':[1920,1080],'fps':30,'frames':int(v['nb_frames']),'shots':len(film.SHOTS),'scenes':11,'words':len(film.WORDS),'caption_cues':len(film.CUES),'integrated_lufs':float(measure['input_i']),'true_peak_dbtp':float(measure['input_tp']),'audio_codec':a['codec_name'],'full_decode_passed':True,'new_tts_requests':7,'approved_sample_utterances_reused':6,'estimated_total_tts_usd_including_sample':cost,'invoice_accessed':False,'other_paid_services':0,'native_speech_speed_preserved':True,'creative_review':'Encoded shot frames reviewed; not a claim of independent full-speed human viewing or audition.','youtube_published':False};(P/'reports/QA.json').write_text(json.dumps(q,indent=2)+'\n');print(json.dumps(q),flush=True)
