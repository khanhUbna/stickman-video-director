# Cavemen Asked AI for More Food. It Gave Them Jobs.

An original English animated story for the new **AI Arrived Too Early** concept. Three clothed prehistoric stick characters discover a helpful machine, then build a food system around the wrong score. A storm forces them to choose between following the schedule and saving dinner.

## Files

- `cavemen-ai-food-jobs.mp4`: complete 16:9 film, English Alloy narration, original score/Foley and burned-in English captions.
- `captions-en.srt` / `.vtt`: optional separate English subtitles.
- `chapters.txt`, `description-en.txt`, `script.txt`: upload and editorial materials.
- `source.zip`: editable project, original generated art, cast bindings, saved narration, word timing and render scripts.
- `QA.json`, `visual-review.md`, `encoded-storyboard-*.jpg`: technical results and explicit limits of visual review.

The approved 18-second opening is included once. The remainder is newly authored; the opening is not looped. The new body has 56 shots across the grove, river, village, craft yard, food store and storm bank. Returns to a location serve the story; this does not mean 56 unique painted backgrounds. There are four painted environment plates, with independently composed native landscape cameras.

No YouTube upload has been made. This is fictional social satire, not a historical account or a factual prediction about AI.

## Thumbnail and publishing text

The requested cover is in [publishing/thumbnail.jpg](publishing/thumbnail.jpg), 1280×720 JPEG, below 2 MB. Recommended public title: **Cavemen Asked AI for Food. It Gave Them Jobs.** [Five title options, description, tags and a pinned comment](publishing/metadata.md) are saved separately. This packaging addition does not regenerate the movie or narration.

## Sound and rights

Seven additional `tts-1` / `alloy` requests, original speed 1. Estimated narration charge **USD 0.10086**, based on the recorded character count and working rate; account billing was not verified. The preview voice was reused. Four additional image-generation calls supplied three environments and one expression/AI sprite atlas; their billing amount is not exposed by the tool. No paid transcription was requested.

All music and Foley were synthesized locally for this film. No music recording or sound from the example channels was copied. Generated artwork and original script were created for this production. Archivo Black is included under its SIL Open Font License. Code is covered by the accompanying MIT license. See `rights.md` for provenance details.

## Rebuild from source

Use Python 3 with Pillow, NumPy, PocketSphinx, plus FFmpeg/FFprobe. Saved narration is already included. **Do not run `generate_voice.py` to fix pictures.** It is retained for provenance and skips existing chapter WAV files.

1. `python timeline.py` rebuilds shot/caption timing from saved words and speech.
2. `python film.py` checks representative poses and writes source stills.
3. `python render_all.py` renders seven new chapters using four local processes.
4. `python sound.py` creates the original score and contact-driven Foley after motion traces exist.
5. `python finish.py` verifies geometry, masters sound and exports the MP4.
6. `python review.py` extracts evidence from the final encoded movie.

`output/intro-approved.mp4` and `audio/intro-approved.wav` are the reused approved hook. To re-author that earlier opening, use the [saved preview source project](https://github.com/khanhUbna/stickman-video-director/raw/refs/heads/video-delivery-b1/deliveries/prehistoric-ai-preview-v1/source-project.zip). Per-frame motion traces for the new body are included. The source archive does not duplicate intermediate chapter movies or large assembled sound stems; regenerate these locally.

This uses the established **project-local articulated compositor** and painted B6 look. The installed trusted B6 runtime is unchanged. Geometry checks and decoded stills do not certify the installed reference's 35 creative subchecks. See the review notes for what was actually inspected.
