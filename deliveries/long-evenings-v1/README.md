# Why Your Evenings Keep Disappearing — long film

Original English long-form film, **native 1280 × 720 landscape, 30 fps**. Eight chapters and 80 separately directed shots expand the Short's subject into work spillover, endless chores, starting friction, chosen leisure and realistic constraints. This is a new film; no Short footage was slowed, stretched or looped to fill the runtime.

## Cast, sets and action

The established gray-haired, green-vest channel protagonist returns. A second painted character appears as a friend in the park. Both use their actual per-view garment/head assets and sleeve fitting. Nine native landscape stages cover the workplace, journey home, entry, living room, kitchen, laundry, bedroom, hobby corner and park. Scenes include travel-driven walking, seated phone use, supported sitting/rising, bag handling, writing, closing a laptop, pouring, stirring, washing, wiping, folding, page turning, painting, bending to lace a shoe, guitar pickup/playing, a phone call and meeting/walking with a friend. Prop/environment inserts are distinguished from actor shots in the inventory.

`rig.py`, `film.py`, `props.py` and `sets.py` extend the previous Short's **project-local** articulated renderer. They do not alter or certify the installed standing-only B6 runtime. Existing painted B6 identity assets and Archivo Black typography are retained. New motion has its own fixed-bone/contact/stance evidence; it is not represented as the installed 35-subcheck reference acceptance or a universal human animation system.

## Voice, music and rights

Exactly eight new `tts-1`/`alloy` chapter recordings were generated at native speed 1 and saved immediately. They total approximately **615.21 seconds** of source speech. Chapter pauses, an opening offset and a final sound/action tail produce the final runtime reported in QA.json. No speech was sped up or slowed down. Offline PocketSphinx aligned all 1,785 words; no paid transcription was used.

Estimated speech cost: **USD 0.151095**, based on the previously documented USD 15/million-character rate, announced before execution. This is an estimate, not verified account billing. No image-generation or paid sound-effects requests were made for this long film. The continuous score, room bed, material Foley and guitar gestures are original seeded local synthesis in `sound.py`; no third-party song or recording was downloaded. Footsteps use the actual rendered swing-to-stance transitions. Font and source license notices are included.

## Verification and review

QA.json contains actual exported frame count, native dimensions, source fingerprint, full decode, loudness, audio/video durations, actor/shot inventory, four control chains per actor frame, fixed lengths, contact-point errors, planted-foot drift and every landed walk stop. Caption coverage matches the normalized script exactly, with semantic one-line breaks, a fixed Archivo Black size and independently authored landscape placement below the principal action field.

The author inspected native action stills, decoded final-film frames and contact/stop details. `visual-review.md` states what was observed. Independent creative review, real-time audiovisual listening by the agent and user acceptance are **not claimed**. Sound measurements do not substitute for listening, and numeric geometry does not certify natural performance or reference equivalence. The complete exported MP4 is supplied for the user's viewing, with these review limits retained.

No YouTube publication was performed. The MP4 contains burned English subtitles; SRT/VTT, chapters, description and source are also provided.

## Reproduce without paid calls

Install Python 3.10+, NumPy, Pillow and FFmpeg/FFprobe. PocketSphinx is needed only to redo offline alignment; the saved word files are provided. Extract the source archive, which includes the eight saved native recordings. Do not regenerate them.

```bash
python timeline.py
python render_all.py
python sound.py
python finish.py
```

Four local encoder processes render independent chapters; these are ordinary local workers, not external agents or API requests. Matching source fingerprints allow chapter reuse. Sound waits for actual motion traces. The finished MP4 is in `output/why-your-evenings-keep-disappearing.mp4`. Large reproducible music/mix/intermediate WAVs and chapter MP4s are omitted from the source archive; the original chapter voice files, actual aligned words, artwork, font, source and technical evidence are retained.
