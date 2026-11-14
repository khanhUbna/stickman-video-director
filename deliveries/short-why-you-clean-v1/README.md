# Why You Clean Instead of Starting — portrait Short

The rendered English Short is ready for user picture/sound review. No YouTube upload was made.

## Download

- `why-you-clean-instead-of-starting.mp4` — 1080×1920, 30 fps, about 27 seconds; alloy voice, original instrumental bed and action sounds, burned-in captions.
- `captions-en.srt` / `captions-en.vtt` — editable subtitle sidecars.
- `source-short-why-you-clean-v1.zip` — original WAV, actual acoustic word alignment, all original art/audio stems, project, renderer and QA sources.
- `encoded-contact-sheet.jpg` — one actual decoded middle frame per shot.
- `QA.json`, `paint-QA.json`, `rig-frame-QA.json`, `encoded-motion-QA.json`, `rights.json` — validation evidence and review limits.

The original requested scratch files were absent. After explicit user authorization, exactly one OpenAI `tts-1` / `alloy` request created the 26.575-second native-rate recording. It was saved and pushed immediately. No paid retry, paid transcription or image API was used. PocketSphinx acoustically aligned all 75 words offline. Estimated speech cost: USD 0.006495; account billing is not independently verified.

The story continues the channel's teal scarf and gold/sage/coral/blue accents. It shows hesitation, actual cleaning, a plate placed in a rack, a clean counter versus an empty draft, and a first typed sentence that remains unsent. It does not claim scientific proof or send an actual email.

## Verified and still pending

Full decode and video/audio stream checks passed. Native phone-size bounded visibility/safe-area and local motion diagnostics passed. Full-body rig lengths and hand/elbow/knee continuity were checked at frame times. A sampled encoded main-picture check, excluding captions/headings, found no low-change interval over 0.5 seconds. Every spoken word appears in semantic single-line captions. Final measured mix: -16.29 LUFS, -1.44 dBTP.

The production author inspected all 15 encoded middle frames and retained repairs. Independent creative review, continuous human playback/listening, and user acceptance are **pending**. Frame/pixel/geometry checks are not artistic acceptance or proof of sample equivalence. Caveat is the licensed portable handwritten font, not Apple's Chalkboard. The procedural score and effects are original local synthesis, not third-party recordings; see `rights.json`.

## Resume without spending

Reuse `voice.wav` and `words.json`. **Do not run TTS again.** The preserved `tts-attempt.json` prevents automatic retries. `create_voice_once.py` is historical provenance, not a required rebuild step.

Extract the source archive into `/workspace/scratch/short-email-v1` on a prepared cloud machine with this repository at `/workspace/stickman-video-director`. Reuse the existing checkout; no worktree is needed. The included `art/scarf.png` preserves the channel identity. The scripts use the installed Skill painter, project validation and portrait/motion checks with a project-local full-film finisher; they do not forge a Skill approval or independent-review record.

```bash
cd /workspace/stickman-video-director/skills/directing-stickman-videos
npm ci
/workspace/.venvs/stickman/bin/python -m pip install numpy==2.0.2 Pillow==11.3.0 pocketsphinx==5.0.4
cd /workspace/scratch/short-email-v1
# Existing WAV/words are sufficient; align_voice.py is optional and offline.
/workspace/.venvs/stickman/bin/python make_audio.py
node build-short.mjs
node check_rig.mjs
node render-short.mjs
/workspace/.venvs/stickman/bin/python finalize.py
```

`render-short.mjs` creates the original mix; run `finalize.py` once afterward to master it. Re-running only the mastering step processes an already-mastered mix. Rendered files go to `output/`. Playback processes do not persist across cloud tasks. No API keys, environment dump or credential files are included.
