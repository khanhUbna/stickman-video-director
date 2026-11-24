"""Free local Kokoro narration. Public model files are downloaded separately, never via an API."""
from pathlib import Path
import os
os.environ['ORT_DISABLE_TELEMETRY'] = '1'
os.environ['HF_HUB_DISABLE_TELEMETRY'] = '1'
os.environ['DO_NOT_TRACK'] = '1'
import json
import hashlib
import numpy as np
import soundfile as sf
import onnxruntime as ort
ort.disable_telemetry_events()
import espeakng_loader
from kokoro_onnx import Kokoro
from kokoro_onnx.config import EspeakConfig

ROOT = Path(__file__).resolve().parents[1]
MODELS = Path(os.environ.get('CLAY_TTS_MODELS', '/workspace/models/kokoro-v1'))
TEXT = (ROOT / 'script/script-en.txt').read_text()
VOICE = 'am_michael'
SPEED = 0.86
EXPECTED = '30f4fbc4dc8da1f6d4c4b99e42882a7da065e15018f4edd21e7b66a7196fa27d'
assert hashlib.sha256(TEXT.encode()).hexdigest() == EXPECTED, 'Approved narration changed'
options = ort.SessionOptions()
options.intra_op_num_threads = 4
options.inter_op_num_threads = 1
options.log_severity_level = 3
session = ort.InferenceSession(str(MODELS / 'kokoro-v1.0.onnx'), sess_options=options, providers=['CPUExecutionProvider'])
model = Kokoro.from_session(session, str(MODELS / 'voices-v1.0.bin'), espeak_config=EspeakConfig(lib_path=espeakng_loader.get_library_path(), data_path=espeakng_loader.get_data_path()))
rate = 24000
parts = []
paragraphs = []
cursor = 0.0

def silence(seconds):
    global cursor
    parts.append(np.zeros(round(seconds * rate), dtype=np.float32))
    cursor += seconds

silence(0.25)
for i, paragraph in enumerate(TEXT.strip().split('\n\n'), 1):
    cache = ROOT / f'.cache/paragraph-{i:02d}-{VOICE}-{SPEED}.wav'
    if cache.exists():
        audio, sample_rate = sf.read(cache, dtype='float32')
    else:
        audio, sample_rate = model.create(paragraph, voice=VOICE, speed=SPEED, lang='en-us')
        sf.write(cache, audio, sample_rate, subtype='PCM_16')
    assert sample_rate == rate
    start = cursor
    parts.append(audio)
    cursor += len(audio) / rate
    paragraphs.append({'id':i, 'start':round(start,6), 'end':round(cursor,6), 'text':paragraph, 'audio':str(cache.relative_to(ROOT))})
    print(json.dumps({'paragraph':i, 'seconds':round(len(audio)/rate,2), 'timeline_end':round(cursor,2)}), flush=True)
    silence(0.70 if i in (1,5,7,12,13) else 0.42)
silence(1.8)
audio = np.concatenate(parts)
sf.write(ROOT / 'assets/voice/narration.flac', audio, rate, subtype='PCM_16')
ledger = {'script_sha256':EXPECTED,'word_count':len(TEXT.split()),'provider':'Kokoro ONNX, local CPU','voice':VOICE,'native_synthesis_speed':SPEED,'sample_rate':rate,'duration':len(audio)/rate,'paragraphs':paragraphs,'paid_api_calls':0,'model_license':'Apache-2.0','model_card':'https://huggingface.co/hexgrad/Kokoro-82M','model_sha256':hashlib.sha256((MODELS/'kokoro-v1.0.onnx').read_bytes()).hexdigest(),'voices_sha256':hashlib.sha256((MODELS/'voices-v1.0.bin').read_bytes()).hexdigest(),'telemetry_disabled':True}
(ROOT / 'assets/speech.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'complete':True,'duration':len(audio)/rate,'words':len(TEXT.split())}),flush=True)
