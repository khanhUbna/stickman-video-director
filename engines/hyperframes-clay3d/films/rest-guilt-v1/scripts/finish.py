"""Export and verify the actual full-film render; never call a media service."""
from pathlib import Path
import hashlib, json, math, re, shutil, subprocess
from PIL import Image, ImageDraw, ImageStat

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[3]
OUT = ROOT / 'output'
DELIVERY = REPO / 'deliveries/rest-guilt-clay-v1'
REPORTS = DELIVERY / 'reports'
REPORTS.mkdir(parents=True, exist_ok=True)
T = json.loads((ROOT / 'assets/timeline.json').read_text())
DURATION = T['duration']
FINAL = DELIVERY / 'why-you-feel-guilty-when-you-rest-1080p.mp4'

def run(args):
    return subprocess.run(args, check=True, capture_output=True, text=True)

def sha(file):
    h = hashlib.sha256()
    with file.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def probe(file):
    return json.loads(run(['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(file)]).stdout)

execution = json.loads((OUT / 'render-execution.json').read_text())
assert execution['exitCode'] == 0, 'Complete the actual HyperFrames render first'
base = OUT / 'base-12fps.mp4'
base_probe = probe(base)
base_video = next(s for s in base_probe['streams'] if s['codec_type'] == 'video')
assert int(base_video['nb_frames']) == round(DURATION * 12)
assert (base_video['width'], base_video['height']) == (1920, 1080)

# Duplicate the authored clay poses into a broadly compatible 30fps file.
# This changes neither speech speed nor the duration of the native animation.
run(['ffmpeg', '-hide_banner', '-nostats', '-y', '-i', str(base), '-i', str(ROOT / 'assets/mix.flac'),
     '-map', '0:v:0', '-map', '1:a:0', '-vf', 'fps=30', '-c:v', 'libx264', '-preset', 'medium',
     '-crf', '18', '-threads', '4', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
     '-ar', '48000', '-t', f'{DURATION:.9f}', '-movflags', '+faststart', str(FINAL)])
assert FINAL.stat().st_size < 100_000_000, 'Check GitHub individual-file size before staging'
info = probe(FINAL)
video = next(s for s in info['streams'] if s['codec_type'] == 'video')
audio = next(s for s in info['streams'] if s['codec_type'] == 'audio')
assert (video['width'], video['height'], video['codec_name'], video['pix_fmt']) == (1920, 1080, 'h264', 'yuv420p')
assert video['r_frame_rate'] == '30/1' and int(video['nb_frames']) == round(DURATION * 30)
assert audio['codec_name'] == 'aac' and int(audio['sample_rate']) == 48000
assert abs(float(info['format']['duration']) - DURATION) < .1
decode = run(['ffmpeg', '-v', 'error', '-i', str(FINAL), '-f', 'null', '-'])
assert not decode.stderr.strip(), decode.stderr
analysis = run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(FINAL), '-vn', '-af',
                'loudnorm=I=-16:TP=-2:LRA=9:print_format=json', '-f', 'null', '-']).stderr
loudness = json.JSONDecoder().raw_decode(analysis[analysis.rfind('{'):])[0]
assert -18 < float(loudness['input_i']) < -14, loudness
assert float(loudness['input_tp']) < -1, loudness

captions = json.loads((ROOT / 'assets/captions.json').read_text())
script = (ROOT / 'script/script-en.txt').read_text()
normalize = lambda text: ''.join(c.lower() for c in text if c.isalnum())
assert normalize(script) == normalize(' '.join(c['text'] for c in captions))
for index, cue in enumerate(captions):
    assert 0 <= cue['start'] < cue['end'] <= DURATION
    if index:
        assert cue['start'] >= captions[index - 1]['end'] - .001
assert sha(ROOT / 'script/script-en.txt') == T['script_sha256']

decoded = OUT / 'decoded'
decoded.mkdir(exist_ok=True)
browser = json.loads((OUT / 'browser-qa-combined.json').read_text())
assert browser['ok'] and len(browser['frames']) == len(T['shots'])
frame_checks = []
for shot in browser['frames']:
    # Select a delivery frame corresponding to the same 12Hz source pose.
    time = round(math.floor((shot['time'] + 1e-7) * 12) / 12 * 30) / 30
    file = decoded / f"{shot['shot']}.jpg"
    run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{time:.9f}', '-i', str(FINAL),
         '-frames:v', '1', '-q:v', '2', str(file)])
    image = Image.open(file).convert('RGB')
    deviation = sum(ImageStat.Stat(image).stddev) / 3
    assert deviation > 10, (shot['shot'], 'Blank or near-solid frame', deviation)
    frame_checks.append({'shot': shot['shot'], 'time': time, 'rgb_stddev': deviation})

for part in range(math.ceil(len(frame_checks) / 22)):
    group = frame_checks[part * 22:(part + 1) * 22]
    sheet = Image.new('RGB', (1920, math.ceil(len(group) / 4) * 302), '#eee6dd')
    draw = ImageDraw.Draw(sheet)
    for index, entry in enumerate(group):
        x, y = index % 4 * 480, index // 4 * 302
        image = Image.open(decoded / f"{entry['shot']}.jpg").resize((480, 270))
        sheet.paste(image, (x, y))
        draw.text((x + 8, y + 274), f"{entry['shot']} {entry['time']:.2f}s — decoded MP4", fill='black')
    sheet.save(REPORTS / f'decoded-sheet-{part + 1}.jpg', quality=90)

copies = {
    'script/subtitles-en.srt': 'captions-en.srt',
    'script/script-en.txt': 'script-en.txt',
    'script/script-vi.txt': 'script-vi.txt',
    'metadata/description-en.txt': 'description-en.txt',
    'metadata/youtube.json': 'youtube-metadata.json',
    'licenses/audio-rights.json': 'audio-rights.json',
}
for source, target in copies.items():
    shutil.copy2(ROOT / source, DELIVERY / target)
for name in ['render-execution.json', 'browser-qa-combined.json', 'motion-audit.json',
             'hyperframes-check-stable.json', 'hyperframes-lint-final.json']:
    shutil.copy2(OUT / name, REPORTS / name)
for name in ['alignment-report.json', 'audio-measurements.json']:
    shutil.copy2(ROOT / 'assets' / name, REPORTS / name)
run(['ffmpeg', '-v', 'error', '-y', '-i', str(FINAL), '-frames:v', '1', '-q:v', '2', str(DELIVERY / 'poster.jpg')])

report = {
    'ok': True, 'file': FINAL.name, 'bytes': FINAL.stat().st_size, 'sha256': sha(FINAL),
    'duration_seconds': float(info['format']['duration']), 'width': video['width'], 'height': video['height'],
    'codec': video['codec_name'], 'pixel_format': video['pix_fmt'], 'fps': video['r_frame_rate'],
    'frames': int(video['nb_frames']), 'native_clay_pose_hz': 12,
    'audio_codec': audio['codec_name'], 'audio_sample_rate': audio['sample_rate'], 'audio_channels': audio['channels'],
    'integrated_lufs': float(loudness['input_i']), 'true_peak_dbtp': float(loudness['input_tp']),
    'full_decode_errors': decode.stderr, 'decoded_shots': frame_checks, 'caption_cues': len(captions),
    'caption_text_equals_approved_script': True, 'script_sha256': sha(ROOT / 'script/script-en.txt'),
    'voice_sha256': sha(ROOT / 'assets/voice/narration.flac'), 'mix_sha256': sha(ROOT / 'assets/mix.flac'),
    'no_post_production_speech_time_stretch': True, 'motion_samples': browser['motion']['samples'],
    'motion_contact_errors': len(browser['motion']['errors']), 'paid_api_calls': 0, 'youtube_published': False,
    'sound_review_scope': 'Measured, not human-auditioned',
    'craft_scope': 'HyperFrames craft heuristic disabled; full local pose audit and separate visual review are documented in REVIEW.md',
    'visual_inspection_status': 'Encoded sheets generated; record actual inspection separately before delivery',
}
(REPORTS / 'QA.json').write_text(json.dumps(report, indent=2) + '\n')
manifest = json.loads((ROOT / 'manifest.json').read_text())
manifest.update(status='rendered-awaiting-final-visual-inspection', delivery=str(DELIVERY.relative_to(REPO)), mp4_sha256=report['sha256'])
(ROOT / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
(DELIVERY / 'README.md').write_text('''# Why You Feel Guilty When You Rest

Full English 3D clay film, native 1920×1080, approximately 4:37. 63 story shots, English narration, burned-in single-line captions, original instrumental music and synchronized Foley. A 30fps H.264/AAC MP4 carries the deliberately authored 12Hz clay poses.

Use `why-you-feel-guilty-when-you-rest-1080p.mp4` for upload. `captions-en.srt` is a separate caption track; script-en.txt and script-vi.txt are reading copies. The description and metadata are drafts for the creator to copy. poster.jpg is an actual first frame, not a separately illustrated thumbnail.

Source, committed narration/master audio, evidence, rights and rerender commands are in `engines/hyperframes-clay3d/films/rest-guilt-v1/`. No paid APIs or HeyGen account/credits were used. This delivery was not published to YouTube.

Reports distinguish all-pose geometry tests, actual decoded MP4 samples and independent still-frame review. Sound was measured, not human-auditioned. The film uses expression and gaze without phoneme lip sync. See the source REVIEW.md for creative choices and limits.
''')
(DELIVERY / 'SHA256SUMS').write_text(''.join(f'{sha(file)}  {file.name}\n' for file in sorted(DELIVERY.iterdir()) if file.is_file() and file.name != 'SHA256SUMS'))
print(json.dumps({k: report[k] for k in ['ok', 'bytes', 'duration_seconds', 'frames', 'integrated_lufs', 'true_peak_dbtp', 'caption_cues']}))
