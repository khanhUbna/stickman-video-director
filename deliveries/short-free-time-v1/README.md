# Why Your Free Time Doesn't Feel Like Yours

Complete English Short: **32.533 seconds, 720 × 1280, 30 fps**, H.264/AAC. Narration is alloy. This is a finished viewing/export file, with creative acceptance awaiting the user's viewing. No YouTube publication was performed.

## What changed from the previous film

The protagonist now travels across a continuous living room with a stance/swing gait and opposing arm swing, lowers onto the sofa with fixed feet, uses the phone, notices the untouched guitar, rises with fixed feet, crosses back toward the guitar, bends and lifts it, then frets and strums. Head nods, hip support and an imperfect-note reaction accompany the playing. The room changes from evening to night, then resets for the following evening. Camera travel follows real world-space character travel; it is not the source of that travel.

The original painted gray-haired/green-vest identity and Archivo Black captions continue from the channel's B6 project. The new living-room set and guitar are original local artwork; the music and Foley are original synthesis without downloaded recordings or third-party melodies. The ending is an action and result rather than a lecture card.

## Action renderer scope

The installed B6 compositor is standing-only. It was **not modified**, and its old standing checks are **not claimed** to certify gait or sitting. `film.py` is a new, project-local articulated action extension reusing the established painted sprite assets and caption rasterizer. It solves fixed-length arms and two-bone legs, explicit planted feet, travel-driven stance/swing phases, garment layering and phone/instrument contacts. Its own per-frame geometry evidence and negative reach test appear in QA.json. These technical checks do not establish the installed 35-subcheck visual acceptance or universal human motion. The new fitting is specific to this character and story.

## Voice and sound

Exactly one new `tts-1`/`alloy` request at speed 1 generated 28.275 seconds of new speech. The voice is retained. The API's streamed WAV header was normalized locally without changing the samples; the original API response is preserved. Total estimated speech cost is **USD 0.00702**, based on the previously documented USD 15/million-character rate; the account bill was not independently checked. No new image request or paid transcription was made.

PocketSphinx aligned the actual speech offline. A 0.35-second opening offset and three explicit silent holds give the physical actions time; no narration was sped up or slowed down. Original footsteps are timed to rendered swing-to-stance transitions. The original guitar phrases coincide with visible string strokes. `prepare_audio.py` documents composition and all events; `finish.py` masters and muxes them.

## Verification and review limits

The final MP4 was fully decoded. All 976 frames are present; the 875 frames containing the actor have two arm and two leg control chains. Maximum fixed-bone error and consecutive planted-foot drift are below 1e-9 pixels. The fretting hand remains at the neck grip; the strumming hand traverses a bounded string area. Each caption fits the approved single-line raster geometry. Audio/video durations agree.

The author inspected source stills and the final encoded storyboard, plus native encoded frames around regret, phone placement and guitar playing. These show the new room, clear dark limbs, supported sitting/standing, phone on its table after release, and the same instrument lifted from its stand. See encoded-storyboard.jpg and the final-derived actions-with-sound.mp4. Independent creative review, real-time audiovisual listening by the agent and actual user acceptance are **not claimed**. The sound/decode measurements are technical checks.

## Reproduce locally

Requires Python 3.10+, Pillow, NumPy and FFmpeg/FFprobe. PocketSphinx is needed only to redo alignment. The saved voice is already included; **do not rerun paid generation**.

```bash
python film.py
python prepare_audio.py
python finish.py
```

Rendering first produces the exact motion trace used to time footsteps. `prepare_audio.py` then rebuilds original sound and the same speech-derived cues; `finish.py` exports `output/why-your-free-time-doesnt-feel-like-yours.mp4` and runs checks. No API is required by these commands. The source archive excludes intermediate MP4s but includes the saved narration, alignment, painted character assets, fonts, source and final technical reports.

Use the supplied SRT/VTT for editing. English captions are already burned into the MP4. Title and description are supplied separately. Review the actual video before publishing it yourself.
