"""Deliver the actual native 2D movie and verifiable sidecars. No API calls."""
from pathlib import Path
import sys,json,subprocess,hashlib,math,shutil
from PIL import Image,ImageDraw,ImageStat,ImageChops
P=Path(__file__).resolve().parents[1];REPO=P.parents[1];sys.path.insert(0,str(P));import film
D=REPO/'deliveries/rest-guilt-stickman-v2';R=D/'reports';R.mkdir(parents=True,exist_ok=True)
OUT=P/'output';FINAL=D/'why-you-feel-guilty-when-you-rest-2d-alloy-720p.mp4'
def run(args):return subprocess.run(args,check=True,capture_output=True,text=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def probe(p):return json.loads(run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(p)]).stdout)
report=json.loads((OUT/'render-report.json').read_text());assert report['frames']==round(film.T['duration']*30)
assert len(report['parts'])==13 and sum(r['frames'] for r in report['parts'])==report['frames']
assert max(r['maximum_bone_error'] for r in report['parts'])<1e-8
assert max(r['maximum_grip_error'] for r in report['parts'])<1e-6
assert max(r['maximum_world_stance_drift'] for r in report['parts'])<1e-6
run(['ffmpeg','-v','error','-y','-i',str(OUT/'picture.mp4'),'-i',str(P/'audio/mix.flac'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-t',str(film.T['duration']),'-movflags','+faststart',str(FINAL)])
info=probe(FINAL);video=next(s for s in info['streams'] if s['codec_type']=='video');audio=next(s for s in info['streams'] if s['codec_type']=='audio')
assert (video['width'],video['height'],video['r_frame_rate'],video['codec_name'])==(1280,720,'30/1','h264')
assert int(video['nb_frames'])==report['frames'];assert abs(float(info['format']['duration'])-film.T['duration'])<.08
assert audio['codec_name']=='aac' and int(audio['sample_rate'])==48000
decode=run(['ffmpeg','-v','error','-i',str(FINAL),'-f','null','-']);assert not decode.stderr.strip(),decode.stderr
log=run(['ffmpeg','-hide_banner','-nostats','-i',str(FINAL),'-vn','-af','loudnorm=I=-16:TP=-2:LRA=9:print_format=json','-f','null','-']).stderr
audio_metrics=json.JSONDecoder().raw_decode(log[log.rfind('{'):])[0];assert -18<float(audio_metrics['input_i'])<-14;assert float(audio_metrics['input_tp'])<-1
norm=lambda t:''.join(c.lower() for c in t if c.isalnum())
assert norm((P/'script-en.txt').read_text())==norm(' '.join(c['text'] for c in film.CUES))
assert sha(P/'script-en.txt')==film.T['script_sha256']
assert all(c['start']<c['end']<=film.T['duration'] for c in film.CUES)
assert all(a['end']<=b['start']+.001 for a,b in zip(film.CUES,film.CUES[1:]))
decoded=OUT/'decoded';decoded.mkdir(exist_ok=True);frames=[];cast={'hero':set(),'friend':set()};differences=[]
for s in film.SHOTS:
 frame=round((s['start']+.63*s['duration'])*30);t=frame/30;target=decoded/f"{s['id']}.jpg"
 run(['ffmpeg','-v','error','-y','-ss',f'{t:.9f}','-i',str(FINAL),'-frames:v','1','-q:v','2',str(target)])
 image=Image.open(target).convert('RGB');deviation=sum(ImageStat.Stat(image).stddev)/3;assert deviation>10,(s['id'],deviation)
 reference,rows,_,_=film.frame(t)
 for row in rows:cast[row['who']].add(s['id'])
 if s['action'] in ['keys','phone_movie','phone_question','unsent_insert','thumb_stop','timer_insert']:cast['hero'].add(s['id'])
 if s['id'] in ['p01-s01','p07-s02','p11-s03','p11-s06','p12-s04','p14-s03','p15-s04']:
  difference=sum(ImageStat.Stat(ImageChops.difference(image,reference)).mean)/3;differences.append({'shot':s['id'],'mean_absolute_rgb_error':difference});assert difference<10,(s['id'],difference)
 frames.append({'shot':s['id'],'action':s['action'],'time':t,'rgb_stddev':deviation})
for part in range(3):
 group=frames[part*22:(part+1)*22];sheet=Image.new('RGB',(1600,math.ceil(len(group)/4)*252),'#f0e5d4');draw=ImageDraw.Draw(sheet)
 for i,f in enumerate(group):
  x,y=i%4*400,i//4*252;sheet.paste(Image.open(decoded/f"{f['shot']}.jpg").resize((400,225)),(x,y));draw.text((x+5,y+230),f"{f['shot']} {f['time']:.2f}s {f['action']}",fill='black')
 sheet.save(R/f'decoded-sheet-{part+1}.jpg',quality=90)
for source,target in [('script-en.txt','script-en.txt'),('script-vi.txt','script-vi.txt'),('captions-en.srt','captions-en.srt'),('authorization.json','tts-authorization.json'),('audio/tts-request.json','tts-request.json'),('audio/rights.json','audio-rights.json')]:shutil.copy2(P/source,D/target)
shutil.copy2(OUT/'render-report.json',R/'render-report.json');shutil.copy2(P/'speech.json',R/'voice-alignment.json');shutil.copy2(P/'audio/mix-measurements.json',R/'mix-measurements.json')
chapters=[('couch_guilt','Why rest feels like getting caught'),('email_insert','Just one email'),('timer_insert','The break you never took'),('friend_rest','A different rule for your friend'),('useful_pause','When unfinished work feels personal'),('boss','When the pressure comes from outside'),('document_insert','Closing the laptop'),('keys','The clean plate'),('roommate_question','No inspection')]
times=[]
for action,label in chapters:
 candidates=[s for s in film.SHOTS if s['action']==action]
 if action=='document_insert':s=next(s for s in candidates if s['paragraph']==11)
 elif action=='keys':s=candidates[-1]
 else:s=candidates[0]
 n=int(s['start']);times.append(f'{n//60:02d}:{n%60:02d} {label}')
description='''Why do you feel guilty when you rest—even after the urgent work is done? This animated story explores rest guilt, productivity guilt, and why it can feel so hard to relax.

One email turns into another. Your break ends before it begins. Then you hear keys at the door… and suddenly you are washing a plate that was already clean.

Through one fictional evening, we explore the pressure to earn a break, the kindness you offer a friend but struggle to give yourself, and one small choice that changes the ending.

'''+ '\n'.join(times)+'''

Sources:
Ohio State University — leisure beliefs and enjoyment:
https://news.osu.edu/think-leisure-is-a-waste-that-may-not-bode-well-for-your-mental-health/
Crocker & Wolfe (2001), Contingencies of self-worth:
https://pubmed.ncbi.nlm.nih.gov/11488379/
Masicampo & Baumeister (2011), Plan making and unfulfilled goals:
https://pubmed.ncbi.nlm.nih.gov/21688924/

The story is a fictional illustration, not a diagnosis or a claim that guilt has one universal cause. Research access and interpretation limits are documented in the production source.

Narration uses an AI-generated OpenAI Alloy voice. Original instrumental music and designed sound effects are reused with the creator's permission.

Have you ever started cleaning just because someone came home?

#Psychology #HumanBehavior #RestGuilt
'''
(D/'description-en.txt').write_text(description)
metadata={'title':film.T['title'],'description':description,'tags':['rest guilt','productivity guilt','why you feel guilty when you rest','feeling guilty for resting','psychology facts','human behavior','self worth','animated psychology'],'language':'en-US','category_id':'27','category':'Education','audience':'General adult audience, not specifically made for children','publish':False}
(D/'youtube-metadata.json').write_text(json.dumps(metadata,indent=2,ensure_ascii=False)+'\n')
span=json.loads((OUT/'trial-span.json').read_text());run(['ffmpeg','-v','error','-y','-ss',str(span['start']),'-i',str(FINAL),'-t',str(span['duration']),'-c:v','libx264','-preset','fast','-crf','18','-c:a','aac','-b:a','192k','-movflags','+faststart',str(R/'motion-trial-10s.mp4')])
run(['ffmpeg','-v','error','-y','-i',str(FINAL),'-frames:v','1','-q:v','2',str(D/'poster.jpg')])
request=json.loads((P/'audio/tts-request.json').read_text())
qa={'ok':True,'file':FINAL.name,'sha256':sha(FINAL),'bytes':FINAL.stat().st_size,'duration_seconds':float(info['format']['duration']),'width':1280,'height':720,'native_layout':'16:9; no upscale from the 3D movie','fps':video['r_frame_rate'],'frames':int(video['nb_frames']),'audio_codec':audio['codec_name'],'audio_sample_rate':audio['sample_rate'],'integrated_lufs':float(audio_metrics['input_i']),'true_peak_dbtp':float(audio_metrics['input_tp']),'full_decode_errors':decode.stderr,'shot_samples':frames,'reference_comparisons':differences,'caption_cues':len(film.CUES),'approved_words':637,'script_sha256':sha(P/'script-en.txt'),'new_paid_tts_calls':1,'model':request['model'],'voice':request['voice'],'estimated_voice_usd':request['estimated_usd'],'budget_usd':.20,'invoice_accessed':False,'other_paid_api_calls':0,'voice_time_stretch':False,'maximum_bone_error':max(r['maximum_bone_error'] for r in report['parts']),'maximum_grip_error':max(r['maximum_grip_error'] for r in report['parts']),'maximum_world_stance_drift':max(r['maximum_world_stance_drift'] for r in report['parts']),'cast_inventory':{who:sorted(ids) for who,ids in cast.items()},'youtube_published':False,'visual_status':'Decoded sheets generated; final visual inspection remains to be recorded','audio_review':'Measured, not human-auditioned','reference_scope':'Accepted channel-specific painted articulated extension; no claim of strict V44/35-subcheck equivalence'}
(R/'QA.json').write_text(json.dumps(qa,indent=2)+'\n');(D/'README.md').write_text('''# Why You Feel Guilty When You Rest — 2D / Alloy

Complete native 1280×720, 30fps painted stickman film, approximately 4:04. The established gray-haired green-waistcoat character acts through the approved 637-word story. New OpenAI Alloy narration, single-line English captions, original instrumental music and synchronized designed Foley.

Upload the MP4. English SRT and English/Vietnamese reading scripts are separate files; description and metadata are drafts for the creator. poster.jpg is an actual frame, not a newly illustrated thumbnail.

The exact approved speech is preserved at native speed1. Purposeful silent gaps allow physical actions and reactions. One authorized tts-1-hd request is estimated at USD0.11208, within the USD0.20 cap; invoice was not accessed. No other paid API was called. Previous 3D and 2D deliveries remain intact. No YouTube publication.

Source, saved native recording, alignment and reproducible rendering scripts are in production/rest-guilt-stickman-v2. Do not call TTS again for rerenders. Reports separate geometry, actual decoded frames and visual review. Sound was measured, not human-auditioned; no claim of full Eiffel V44 reference equivalence or independent human audiovisual acceptance.
''')
assert FINAL.stat().st_size<100_000_000
print(json.dumps({k:qa[k] for k in ['ok','bytes','duration_seconds','frames','integrated_lufs','true_peak_dbtp','estimated_voice_usd']}))
