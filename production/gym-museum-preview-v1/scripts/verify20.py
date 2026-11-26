from pathlib import Path
import json,subprocess,hashlib,re
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parents[1];D=P.parents[1]/'deliveries/gym-museum-preview-v1';F=D/'gym-museum-20s-en-1080p.mp4'
def run(args):return subprocess.run(args,capture_output=True,text=True,check=True)
meta=json.loads(run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(F)]).stdout);v=next(x for x in meta['streams'] if x['codec_type']=='video');a=next(x for x in meta['streams'] if x['codec_type']=='audio')
assert(v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1920,1080,'30/1',600)
assert abs(float(meta['format']['duration'])-20)<.03
run(['ffmpeg','-v','error','-i',str(F),'-f','null','-'])
log=run(['ffmpeg','-hide_banner','-nostats','-i',str(F),'-af','loudnorm=I=-16:TP=-2:print_format=json','-f','null','-']).stderr;measure=json.JSONDecoder().raw_decode(log[log.rfind('{'):])[0];assert -18<float(measure['input_i'])<-14;assert float(measure['input_tp'])<-1
cues=json.loads((P/'captions20.json').read_text());words=json.loads((P/'words20.json').read_text());canon=(P/'script-en.txt').read_text().split();assert canon==' '.join(x['text'] for x in cues).split()==' '.join(x['text'] for x in words).split();assert len(canon)==49
assert all(c['end']>c['start']>=0 for c in cues);assert all(b['start']>=a['end'] for a,b in zip(cues,cues[1:]));assert max(c['end'] for c in cues)<20
render=json.loads((P/'reports/render.json').read_text());assert render['source_fingerprint']==hashlib.sha256(b''.join((P/n).read_bytes() for n in render['inputs'])).hexdigest()
ledger=json.loads((P/'audio/tts-ledger.json').read_text());assert len(ledger)==5 and all(x['state']=='saved' for x in ledger);cost=sum(x['estimated_usd'] for x in ledger);assert cost<=.02
sheet=Image.new('RGB',(1440,4*293),'white');draw=ImageDraw.Draw(sheet);evidence=[]
for i,t in enumerate([.4,1.8,3.5,5.8,7.5,10.2,11.4,13.5,14.2,15.4,17.2,18.9]):
 f=P/'reports'/f'encoded-{i+1:02d}.jpg';run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(F),'-frames:v','1','-q:v','2',str(f)]);im=Image.open(f);im.thumbnail((480,270));sheet.paste(im,(i%3*480,i//3*293));draw.text((i%3*480+8,i//3*293+274),f'{t:.2f}s',fill='black');evidence.append({'time':t,'file':f.name})
sheet.save(P/'reports/encoded-review.jpg')
qa={'file':F.name,'sha256':hashlib.sha256(F.read_bytes()).hexdigest(),'duration':float(meta['format']['duration']),'bytes':F.stat().st_size,'resolution':[1920,1080],'fps':'30/1','frames':600,'audio_codec':a['codec_name'],'audio_sample_rate':a['sample_rate'],'integrated_lufs':float(measure['input_i']),'true_peak_dbtp':float(measure['input_tp']),'decoded_without_errors':True,'paid_requests':5,'estimated_tts_usd':cost,'invoice_accessed':False,'other_paid_calls':0,'speech_speed_changed':False,'words':49,'ASR_exact_native_anchors':48,'ASR_canonical_interpolation':1,'caption_cues':len(cues),'source_fingerprint':render['source_fingerprint'],'visual_evidence':evidence,'quality_scope':'Original 2D sample; no B6 reference-equivalence claim','review_limits':'Technical checks and decoded-frame review; human audition/full-speed perceptual playback not claimed','full_film_rendered':False,'youtube_published':False}
(P/'reports/QA.json').write_text(json.dumps(qa,indent=2)+'\n');print(json.dumps({k:qa[k] for k in ['duration','bytes','words','estimated_tts_usd','integrated_lufs','true_peak_dbtp']}))
