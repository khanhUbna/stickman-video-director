from pathlib import Path
import subprocess,json,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;D=P.parents[1]/'deliveries/silver-jacket-motion-test-v2'
video=D/'silver-jacket-coffee-test-20s-v2.mp4'
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)]))
v=next(x for x in probe['streams'] if x['codec_type']=='video');a=next(x for x in probe['streams'] if x['codec_type']=='audio')
assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1280,720,'30/1',600)
assert abs(float(probe['format']['duration'])-20)<.04
subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(video),'-f','null','-'],check=True)
rows=json.loads((P/'reports/contact-log.json').read_text());slide=0;gap=1000;err=0
for prev,now in zip(rows,rows[1:]):
 gap=min(gap,now['feet'][1]['x']-now['feet'][0]['x'])
 for i in range(2):
  p,n=prev['feet'][i],now['feet'][i]
  if p['planted'] and n['planted']:slide=max(slide,abs(p['x']-n['x']))
 if now['held']:err=max(err,abs(now['cup'][0]-now['hand'][0]-26),abs(now['cup'][1]-now['hand'][1]+25))
assert gap>0 and slide<.001 and err<.001
minimum_joint_coverage=min(min(r['joint_core_coverage']) for r in rows)
maximum_detached=max(r['detached_large_components'] for r in rows)
assert minimum_joint_coverage>.95,minimum_joint_coverage
assert maximum_detached==0,maximum_detached
prior=P.parent/'silver-jacket-motion-test-v1/assets/demo-audio.wav'
assert (P/'assets/demo-audio.wav').read_bytes()==prior.read_bytes()

sheet=Image.new('RGB',(1280,720),'white')
for i,t in enumerate([1.5,5.7,7.0,10.8,14.,18.8]):
 f=P/'reports'/f'encoded-{i}.jpg'
 subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(video),'-frames:v','1','-q:v','2',str(f)],check=True)
 im=Image.open(f);im.thumbnail((426,240));sheet.paste(im,((i%3)*426,(i//3)*360))
sheet.save(P/'reports/encoded-contact-sheet.jpg')
old=P.parents[1]/'deliveries/silver-jacket-motion-test-v1/silver-jacket-coffee-test-20s.mp4'
oldframe=P/'reports/old-7s.jpg'
subprocess.run(['ffmpeg','-v','error','-y','-ss','7','-i',str(old),'-frames:v','1','-q:v','2',str(oldframe)],check=True)
compare=Image.new('RGB',(810,590),'white');dr=ImageDraw.Draw(compare)
for i,f in enumerate([oldframe,P/'reports/encoded-2.jpg']):
 crop=Image.open(f).crop((465,100,870,660));compare.paste(crop,(i*405,30))
 dr.text((i*405+15,8),'V1: rigid pieces' if i==0 else 'V2: continuous skin',fill='black')
compare.save(P/'reports/before-after-7s.jpg')

report=dict(duration_seconds=float(probe['format']['duration']),resolution=[v['width'],v['height']],fps=30,frames=600,video_codec=v['codec_name'],audio_codec=a['codec_name'],full_decode_passed=True,source_geometry_frames=len(rows),joint_core_checks=len(rows)*10,minimum_joint_core_coverage=minimum_joint_coverage,maximum_detached_components_over_50px=maximum_detached,original_audio_reused_exactly=True,minimum_feet_x_separation_px=gap,consecutive_planted_foot_drift_px=slide,held_cup_transform_error_px=err,voice='Kokoro am_michael (local synthetic demo, not voice impersonation)',paid_tts_calls=0,youtube_published=False,sha256=hashlib.sha256(video.read_bytes()).hexdigest(),bytes=video.stat().st_size,review_scope='Encoded stills and technical/contact checks, not independent full-speed human viewing/listening; prototype awaiting creator review.')
for f in [P/'reports/QA.json',D/'QA.json']:f.write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
