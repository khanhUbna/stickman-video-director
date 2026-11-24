"""One authorized native OpenAI Alloy recording. No retries, key logging or revoice."""
from pathlib import Path
import json,os,urllib.request,urllib.error,hashlib,subprocess
P=Path(__file__).resolve().parents[1]
auth=json.loads((P/'authorization.json').read_text());text=(P/'script-en.txt').read_text()
estimate=len(text)*auth['pricing_usd_per_million_characters']/1e6
assert estimate<=auth['maximum_usd'] and auth['voice']=='alloy'
raw=P/'audio/openai-alloy-native.wav';record=P/'audio/tts-request.json'
if not raw.exists():
    assert not record.exists(),'Previous attempt recorded: do not automatically retry a billable request'
    assert os.environ.get('OPENAI_API_KEY'),'OpenAI key is unavailable; do not print it'
    record.write_text(json.dumps({'state':'attempted','model':auth['model'],'voice':'alloy','characters':len(text),'estimated_usd':estimate,'billing_verified':False,'speed':1,'automatic_retry':False},indent=2)+'\n')
    payload={'model':auth['model'],'voice':'alloy','input':text,'response_format':'wav','speed':1}
    request=urllib.request.Request('https://api.openai.com/v1/audio/speech',data=json.dumps(payload).encode(),headers={'Authorization':'Bearer '+os.environ['OPENAI_API_KEY'],'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(request,timeout=240) as response:raw.write_bytes(response.read())
    except urllib.error.HTTPError as error:raise SystemExit(f'OpenAI TTS HTTP {error.code}; no automatic retry; no key logged')
subprocess.run(['ffmpeg','-v','error','-y','-i',str(raw),'-ar','48000','-ac','1','-c:a','flac',str(P/'audio/voice.flac')],check=True)
info=json.loads(subprocess.run(['ffprobe','-v','error','-show_format','-of','json',str(P/'audio/voice.flac')],check=True,capture_output=True,text=True).stdout)
doc=json.loads(record.read_text());doc.update(state='saved',native_wav_sha256=hashlib.sha256(raw.read_bytes()).hexdigest(),duration_seconds=float(info['format']['duration']))
record.write_text(json.dumps(doc,indent=2)+'\n');print(json.dumps(doc))
