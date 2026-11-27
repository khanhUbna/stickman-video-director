from pathlib import Path
import subprocess,json,hashlib,math
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;D=P.parents[1]/'deliveries/silver-face-stickman-test-v1'
video=D/'cartoon-stickman-coffee-20s.mp4'
data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)]))
v=next(x for x in data['streams'] if x['codec_type']=='video');a=next(x for x in data['streams'] if x['codec_type']=='audio')
assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1280,720,'30/1',600)
assert abs(float(data['format']['duration'])-20)<.01
subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(video),'-f','null','-'],check=True)
rows=json.loads((P/'reports/motion-log.json').read_text());drift=0;prop_error=0;bone_error=0
expected=[100,113,84,88]*2
for row in rows:
 bone_error=max(bone_error,max(abs(x-y) for x,y in zip(row['bone_lengths'],expected)))
 if row['held']:
  prop_error=max(prop_error,abs(row['cup'][0]-row['hands'][1][0]-26),abs(row['cup'][1]-row['hands'][1][1]+25))
for before,after in zip(rows,rows[1:]):
 for i in range(2):
  p,n=before['feet'][i],after['feet'][i]
  if p[2] and n[2]:drift=max(drift,abs(p[0][0]-n[0][0]))
assert bone_error<.001 and prop_error<.001 and drift<.001
old=P.parent/'silver-jacket-motion-test-v1/assets/demo-audio.wav'
assert (P/'assets/demo-audio.wav').read_bytes()==old.read_bytes()
sheet=Image.new('RGB',(1280,540),'white');draw=ImageDraw.Draw(sheet)
for i,t in enumerate([1.5,4.8,5.7,7.,10.8,18.8]):
 f=P/'reports'/f'encoded-{i}.jpg'
 subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(video),'-frames:v','1','-q:v','2',str(f)],check=True)
 im=Image.open(f);im.thumbnail((426,240));sheet.paste(im,((i%3)*426,(i//3)*270));draw.text(((i%3)*426+5,(i//3)*270+244),f'{t:.1f}s',fill='black')
sheet.save(P/'reports/encoded-contact-sheet.jpg')
report=dict(duration_seconds=20,resolution=[1280,720],fps=30,frames=600,video_codec=v['codec_name'],audio_codec=a['codec_name'],full_decode_passed=True,source_frames_checked=len(rows),maximum_bone_length_error_px=bone_error,planted_foot_drift_px=drift,held_cup_transform_error_px=prop_error,original_audio_reused_exactly=True,face='Original simple cartoon, silver hair and glasses; no portrait texture',body='Procedural connected rounded vector limbs; no mesh-warped clothing',paid_service_calls=0,youtube_published=False,bytes=video.stat().st_size,sha256=hashlib.sha256(video.read_bytes()).hexdigest(),review_scope='Encoded frame sampling and source geometry, not independent full-speed human viewing/listening. Awaiting creator review.')
for f in [D/'QA.json',P/'reports/QA.json']:f.write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
