# Where Your Tap Water Comes From

Finished English ensemble-comedy explainer, custom bright 2D cutaway style continuing the approved water preview. This is not a B6/Koa production and does not claim B6 sample equivalence.

## Delivery

- `where-your-tap-water-comes-from.mp4`: native 1280x720, 16:9, 30 fps; approximately 3 minutes 46 seconds. English dialogue, burned-in English captions, original music and designed Foley/ambience.
- `captions-en.srt`: English subtitles without speaker labels.
- `captions-vi.srt`: separate Vietnamese reading translation, matching the spoken dialogue cues.
- `script-with-speakers.txt`: readable English dialogue script.
- `decoded-review-1.jpg`, `decoded-review-2.jpg`, `decoded-review-3.jpg`: chronological samples decoded from the delivered MP4, three phases of all 31 main scenes.
- `QA.json`, `decoded-motion-checks.json`, `sound-rights.json`, `shots.json`: technical results, sampled local motion, sound provenance, shot timeline.
- `source.zip`: animation/finishing code, saved native dialogue, timing, existing generated mascot, font and license. No API key is included.

## Story and motion

Pump takes all the credit while switched off. Drop asks why the tap still runs. A rewind follows one reservoir-fed town through intake screening, particle aggregation, settling, filtration, disinfection, pumping, elevated storage, buried distribution and the household tap. The final toothbrush joke cuts to Drain: “Next department.”

There are 31 main scenes, plus the settling-to-filtration insert. Layouts alternate bathroom wide shot, pump close-up, lake, underwater intake, source comparison, intake screen, inspection station, microscopic particles, aggregation, settling tank, filter cross-section, disinfection chamber, stairs gag, impeller, network diagram, tower, three-appliance split screen, gravity/head diagram, underground street, house connection, occupied supply pipe, valve cutaway and gray drain.

Local action includes articulated Drop arms/legs, walking, recoil and falling; rotating impeller; moving flow markers; detached debris stopping at screen; particles gathering and sinking; water moving through filter media; sequential showers/washer activation; rotating washer contents; tank-level decline while the pump is stopped and tap continues; physical brush/drain progression. This is code animation of original mechanisms and a generated character asset, not video-generation-model footage or a still-image slideshow.

## Science scope

This is a simplified, time-compressed example, not a claim that every home's supply uses a reservoir or elevated tank. Rivers and groundwater and direct pumped networks are acknowledged. Treatment stages are distinct: intake screen, particle aggregation, settling, filtration, controlled chlorine disinfection. Looking clean does not establish safety. Treatment is not depicted as an instantaneous universal guarantee.

In the gravity demonstration, stored water was pumped up earlier; the pump remains off, the tank surface declines and remains above the open tap outlet. Pipes are normally full; a tap does not restart the whole journey. Schematic geometry/level changes are not to scale, CFD or an engineering prediction. Supply is blue; wastewater/drain is gray. The drain ending previews a separate process; wastewater is not routed back into the drinking supply.

## Voice, audio rights and cost

The 15-second preview's voice does not contain the new script. One saved native `tts-1`, speed 1 request per new dialogue cue was made, with no paid retries, transcription or revoicing. Drop uses Alloy; Pump Echo; Tank Onyx; Filter Nova; Tap Shimmer; Drain Fable. Native responses and normalizations are retained. Estimated new TTS cost is USD 0.034995 for 2,333 characters at USD 15 per million characters; account billing was not independently verified. No new image-generation request was made.

The mascot expressions reuse the generated assets from `water-motion-preview-v1`. Mechanisms and scenery are original drawing code. Music is an original locally composed plucked progression; ambience and Foley are original local synthesis. No third-party song, recording, YouTube soundtrack or uncleared library sample is used. This describes provenance and reuse; it does not guarantee platform Content ID outcomes. The font is DejaVu Sans Bold, distributed with its license.

## Verification and limits

Full video/audio decoding, frame count, dimensions, stream-duration agreement, subtitle ordering/coverage, encoded loudness/true peak and final file hash are checked. Picture-only pixel samples exclude the subtitle band; changes alone do not establish artistic quality. The author reviews the source storyboard and chronological decoded samples across all 31 scenes. A height-head issue found during review is repaired in the final version; the earlier audit is retained locally and not presented as the final file's QA.

No independent creative review or real-time audiovisual listening review was performed. Technical success and sampled picture inspection are separate from the creator's viewing approval. No YouTube upload or environment-configuration publication is performed.

## Rebuild

Python 3 with Pillow and NumPy; FFmpeg/FFprobe. Working directory is the extracted source folder.

1. `python animate.py` renders picture from the saved timeline and images.
2. `python finish.py` builds original stems, masters the mix, muxes the MP4 and writes English subtitles and QA.
3. `python review.py` decodes review sheets, checks sampled local changes and writes Vietnamese subtitles.

`voice.py` is supplied for provenance, not needed for picture/audio edits. Saved audio must be reused; never remove files merely to regenerate a line. Requests with a saved attempt but no response stop instead of automatically retrying a paid call.
