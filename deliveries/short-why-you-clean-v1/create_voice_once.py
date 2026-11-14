"""One authorized OpenAI speech request; persistent latch prevents paid retries.

Dry run is the default. Credentials are read only from OPENAI_API_KEY and never
written, logged, passed on a command line, or included in checkpoints.
"""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import urllib.error
import urllib.request
import wave
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
CEILING_USD = 0.02
RATE_PER_MILLION = 15.0
PRICE_SOURCE = 'https://developers.openai.com/api/docs/models/tts-1'


def save(name, value):
    target = ROOT / name
    temporary = target.with_suffix(target.suffix + '.tmp')
    temporary.write_text(json.dumps(value, indent=2) + '\n')
    temporary.replace(target)


def checkpoint(stage, **fields):
    state = json.loads((ROOT / 'checkpoint.json').read_text())
    state.update(stage=stage, **fields)
    save('checkpoint.json', state)


def persist(message):
    # Only this delivery directory is staged. No environment/credential files.
    repo = ROOT.parents[1]
    relative = str(ROOT.relative_to(repo))
    subprocess.run(['git', 'add', '--', relative], cwd=repo, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['git', '-c', 'user.name=Codex', '-c',
                    'user.email=codex@users.noreply.github.com', 'commit',
                    '-m', message], cwd=repo, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['git', 'push', 'origin', 'HEAD:video-delivery-b1'], cwd=repo,
                   check=True, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute-once', action='store_true')
    args = parser.parse_args()
    text = (ROOT / 'script.txt').read_text().strip()
    estimate = len(text) * RATE_PER_MILLION / 1_000_000
    summary = dict(model='tts-1', voice='alloy', speed=1.0,
                   input_characters=len(text), estimated_usd=estimate,
                   ceiling_usd=CEILING_USD, pricing_source=PRICE_SOURCE,
                   pricing_checked_utc='2026-11-14', automatic_retries=0)
    if estimate > CEILING_USD:
        sys.exit('Budget guard: no request made.')
    if not args.execute_once:
        print(json.dumps(dict(summary, dry_run=True,
                              credential_configured=bool(os.getenv('OPENAI_API_KEY'))),
                         indent=2))
        return
    key = os.getenv('OPENAI_API_KEY')
    if not key:
        sys.exit('Missing OPENAI_API_KEY. No request made.')
    if (ROOT / 'voice.wav').exists():
        sys.exit('Voice already exists. Reuse it; no request made.')
    attempt = ROOT / 'tts-attempt.json'
    state = dict(summary, status='armed_do_not_retry',
                 input_sha256=hashlib.sha256(text.encode()).hexdigest(),
                 time_utc=datetime.now(timezone.utc).isoformat())
    try:
        with attempt.open('x') as f:
            json.dump(state, f, indent=2)
    except FileExistsError:
        sys.exit('A prior attempt is recorded. Inspect it; never auto-retry.')
    # Persist the guard before a network request. If this fails, no paid call.
    try:
        persist('Arm single authorized Short TTS call; disable paid retries')
    except subprocess.CalledProcessError:
        sys.exit('Could not persist pre-call guard. No request made; inspect checkpoint.')
    request = urllib.request.Request(
        'https://api.openai.com/v1/audio/speech',
        data=json.dumps(dict(model='tts-1', voice='alloy', input=text,
                             response_format='wav', speed=1.0)).encode(),
        headers={'Authorization': 'Bearer ' + key,
                 'Content-Type': 'application/json'}, method='POST')
    # Do not follow redirects carrying Authorization; urllib has no paid retry loop.
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *args, **kwargs):
            return None
    opener = urllib.request.build_opener(NoRedirect)
    try:
        with opener.open(request, timeout=120) as response:
            payload = response.read()
            state['http_status'] = response.status
    except urllib.error.HTTPError as e:
        state.update(status='http_error_do_not_retry', http_status=e.code,
                     billing='unverified; inspect provider usage before any new authorization')
        save('tts-attempt.json', state)
        checkpoint('tts_http_error_do_not_retry', tts_attempt=state)
        try:
            persist('Preserve failed TTS status without retrying or logging response bodies')
        except subprocess.CalledProcessError:
            pass
        sys.exit('TTS returned an HTTP error. Sanitized status saved; no retry.')
    except Exception as e:
        state.update(status='uncertain_do_not_retry', error_category=type(e).__name__,
                     billing='unknown; potentially billable')
        save('tts-attempt.json', state)
        checkpoint('tts_uncertain_do_not_retry', tts_attempt=state)
        try:
            persist('Preserve uncertain TTS attempt; do not retry')
        except subprocess.CalledProcessError:
            pass
        sys.exit('TTS result uncertain. No retry; inspect provider usage/artifacts.')
    try:
        with wave.open(io.BytesIO(payload), 'rb') as audio:
            duration = audio.getnframes() / audio.getframerate()
            if duration <= 0:
                raise ValueError('empty audio')
            state.update(duration_seconds=duration, sample_rate=audio.getframerate(),
                         channels=audio.getnchannels())
    except Exception:
        (ROOT / 'voice-unverified-response.bin').write_bytes(payload)
        state.update(status='unverified_response_do_not_retry')
        save('tts-attempt.json', state)
        checkpoint('tts_unverified_response_do_not_retry', tts_attempt=state)
        persist('Preserve unverified TTS output without retrying')
        sys.exit('Unverified audio response preserved. No retry.')
    (ROOT / 'voice.wav').write_bytes(payload)
    state.update(status='audio_preserved', audio_sha256=hashlib.sha256(payload).hexdigest(),
                 billing='character-rate estimate; account invoice not independently verified')
    save('tts-attempt.json', state)
    checkpoint('voice_preserved_alignment_pending', tts_attempt=state,
               narration=dict(provider='OpenAI', model='tts-1', voice='alloy',
                              speed=1.0, calls_attempted=1, retry=False),
               cost=dict(new_total_ceiling_usd=CEILING_USD,
                         new_calls_estimated_usd=estimate, alignment='local'))
    persist('Preserve original alloy Short voice and checkpoint immediately after synthesis')
    print('Original voice and checkpoint saved to repository. No further API calls.')


if __name__ == '__main__':
    main()
