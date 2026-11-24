# Why You Feel Guilty When You Rest

Complete original English animated story for **Psychology Facts**. Native **1280 x 720, 16:9, 30fps**, approximately **4 minutes 10 seconds**. The authoritative encoded duration and checksum are in QA.json.

## Upload files

- `why-you-feel-guilty-when-you-rest.mp4`: H.264/AAC, English narration, burned English captions, original score and Foley.
- `thumbnail.jpg`: separately authored 1280 x 720 JPEG, below 2MB.
- `captions-en.srt` / `.vtt`: complete English captions, acoustically aligned offline to the saved native speech.
- `captions-vi.srt`: Vietnamese reading translation; phrase times interpolate inside the corresponding narrated story beat. These are translated reading timings, not Vietnamese speech alignment.
- `script-en.txt`, `script-vi.txt`: scripts to read/edit.
- `upload-title.txt`, `upload-description.txt`, `chapters.txt`: ready to copy.
- `source-project.zip`: portable authoring files, existing fitted identity, new art, fonts and six saved native chapter recordings. Do not rerun paid speech generation to rebuild pictures.

## Story and production

Six chapters and 39 separately timed narrative shots. The protagonist sits, perceives a shirt, rises with planted feet, bends/acquires/lifts it, folds, wipes, handles dishes, types, writes, closes a laptop, walks, uses/places a phone, pauses on a park bench, stirs, pours, reads, reaches then returns to the book. Principal-picture changes, action details and reaction shots serve the story. Quiet holds are intentional for this rest story. Eight new painted room/park plates include one alternate kitchen plate reserved in the art package; seven new plates appear in the film, alongside the existing street stage.

The existing painted gray-haired green-waistcoat identity and Archivo Black subtitle renderer continue from the channel. One new fitted reading expression changes the ending's emotional state. This project extends the previously delivered local articulated action renderer; it does not modify or claim certification by the installed standing-only B6 engine. Fixed geometry, grip/stance checks and technical encoding do not establish the entire installed Sample 1 visual acceptance.

## Voice, costs and rights

Six new `tts-1` / `alloy` chapter requests, speed 1. The saved native responses and normalized sample-preserving WAVs are included. No voice speed/pitch manipulation, revoicing, paid transcription or downloaded music. Estimated speech cost **USD 0.06045**, based on the previously documented USD15/million-character rate; actual account billing is not exposed. Four image-generation requests: two four-panel environment atlases, one reading-expression cutout, one thumbnail. Image pricing/billing is not exposed.

Music, room tone and contact Foley are original local synthesis in sound.py. Footstep events derive from actual rendered stance transitions. Font/source notices are included. No third-party song recording or stock video is used. See rights.json.

## Verification and limits

See QA.json for final stream/frame/duration/full-decode results, every actual actor chain, grip contacts, fixed foot support and stop checks. Final-frame samples, caption coverage/readability checks and encoded speech-presence checks are recorded separately. These are author and technical checks. Independent creative review, continuous human viewing, real-time audiovisual listening by the agent, and actual user approval are not claimed. Source retrieval limits and scientific scope are in editorial-notes.md. No YouTube upload has been made.

## Rebuild offline

Python 3.10+, Pillow, NumPy and FFmpeg/FFprobe; PocketSphinx only for redoing offline alignment. Saved word files are included.

```bash
python timeline.py
python render_all.py
python sound.py
python finish.py
python review.py
```

The renderer uses four ordinary local encoder workers. Original saved narration is reused; no API calls occur in these rebuild commands. The script author and generate_voice.py are provenance/explicit-generation tools, not required rebuild steps. Never delete their saved checkpoint files to force a paid retry.
