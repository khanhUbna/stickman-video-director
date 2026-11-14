# Why You Clean Instead of Starting — production checkpoint

**Incomplete.** The user approved the replacement script and one new OpenAI
`tts-1` / `alloy` recording at native speed, within a total new fee of USD 0.02.
No paid API request has been made. `OPENAI_API_KEY` is absent in this environment.
Never paste a key in chat or commit it. Configure it securely in the runtime.

## Preserved work

- Exact approved narration: `script.txt` (75 words, 433 submitted characters).
- Channel identity/color and shot/sound plan: `creative-direction.md`.
- Draft title and description: `title.txt`, `description.txt`.
- Resumable state: `checkpoint.json`.
- Safe project-local TTS adapter: `create_voice_once.py`.

The official model page, checked 2026-11-14, lists USD 15 / 1M characters:
https://developers.openai.com/api/docs/models/tts-1
Estimated single-call cost is **USD 0.006495**, within the authorized USD 0.02.
The Speech API documents `alloy`, WAV output and speed 1.0:
https://platform.openai.com/docs/api-reference/audio/createSpeech
No paid transcription is planned; timestamps must come from actual audio and a
local aligner. Proportional/guessed timing must not be labeled aligned words.

## Resume

From a checkout of `video-delivery-b1`, run the adapter with no arguments for a
nonbillable dry run. Once credentials are securely available, the authorized
single call is `python create_voice_once.py --execute-once`. It saves and pushes
a persistent attempt latch **before** the request and the original voice plus
checkpoint immediately afterward. No paid retry is implemented. On an error,
timeout or unverified response, inspect the saved status and provider usage;
do not delete the latch or call again automatically.

After voice generation, align actual words locally, time the planned action,
render original animation with the installed `directing-stickman-videos`
runtime, mix the rights-cleared soundtrack, review the actual encoded 9:16 MP4,
and upload MP4, sidecar captions and source archive to this same branch.
Do not report technical encoding as independent picture/sound acceptance.
Do not publish to YouTube.

## Verified local tools

FFmpeg/FFprobe and Node are available. The Skill's dependencies were installed
with a workspace-local npm cache. Its `doctor` subsequently passed Node,
FFmpeg, FFprobe, canvas, sharp and font checks. TTS access, returned speech,
alignment and final MP4 review remain pending.
