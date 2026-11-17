# 3 Questions Even AI Can't Answer

An original English film for **AI Arrived Too Early**, built from the user's request to study a supplied TED-Ed transcript's question-led storytelling. Koa asks whether we are alone, whether a machine can feel and what a life should be for. The film separates missing evidence, contested tests for subjective experience and value-laden choices. It does not claim permanent AI incapacity or copy the reference's script.

## Delivery

- `3-questions-even-ai-cant-answer.mp4`: complete native 1280×720, 30 fps landscape film; Alloy narration, one-line burned-in captions, original score/Foley.
- `captions-en.srt` / `.vtt`: separately selectable English captions.
- `description-en.txt`, `chapters.txt`, `script.txt`: upload/editorial materials.
- `source.zip`: project source, generated paintings and props, saved speech, alignments and motion traces.
- `QA.json`, `visual-review.md`, `encoded-storyboard-*.jpg`: actual technical results, decoded evidence and review limits.
- `reference-study.md`: techniques studied, differences from the reference, scientific caveats and research-access limits.

The 35 shots are authored specifically for this story. None of the previous movie's footage or voice recording is reused. Existing Koa/Nim character packages, the AI stone and the established project-local articulated compositor retain channel identity. Five new painted settings cover the night ridge, space, a hypothetical tidal world, the cave and the dawn river fork. A sixth generated atlas supplies three planet illustrations, a butterfly, cup and flame. Planetary and neural-network graphics are conceptual illustrations, not observational data.

## Cost and provenance

Five newly saved `tts-1` / `alloy` requests at speed 1: estimated **USD 0.08724** using the recorded text count and working rate. Account billing was not verified. Six new image-generation calls; their billing is not exposed. No paid transcription call, voice audition or visual-correction revoice was made.

All music and Foley were synthesized locally for this film; no music recording or audio from the reference video was copied. See `rights.md`. No YouTube upload has been made.

## Rebuild

Python with `requirements.txt` plus FFmpeg/FFprobe. The saved speech is already present. Do not run `generate_voice.py` to correct animation.

1. `python timeline.py` rebuilds timing/captions from saved words and audio.
2. `python film.py` validates representative poses and saves source stills.
3. `python render_all.py` renders the five new chapters with four local worker processes.
4. `python sound.py` creates the original score/Foley after motion traces exist.
5. `python finish.py` checks every drawn actor frame, masters audio, muxes and fully decodes the film.
6. `python review.py` extracts frames and action-state sequences from the actual final MP4.

The archive includes original-rate narration and per-frame motion traces. Large assembled audio stems and intermediate chapter movies are reproducible and omitted. The installed trusted B6 runtime was not changed; this follows the established project-local B6-look extension. Strict primary-reference 35-subcheck acceptance and independent creative/listening approval are not claimed. Read the actual review record rather than interpreting an encode or geometry pass as an aesthetic certification.

`render_all.py` applies `scene_patch.py` to shot 04-08 only, so the spoken stone-placement action is literal in the final film. Its separate SHA is verified for chapter four by `finish.py`. Chapter five's first frame is clamped to its actual start to avoid a stale previous-shot sample after 30 fps boundary rounding. The shared `film.py` baseline and chapters one to three remain unchanged; call `render_all.py` for a complete faithful rebuild rather than rendering chapter four directly from the baseline module.
