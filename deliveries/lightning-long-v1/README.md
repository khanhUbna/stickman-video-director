# Lightning Hits the Ground. Then What?

Finished English landscape film for Everyday, Explained, approximately **5 minutes 52 seconds**, native **1280x720 / 16:9 / 30 fps**. This is a newly authored long story, not the Short slowed down, looped or cropped into landscape.

## Delivery

- `lightning-hits-the-ground-then-what.mp4`: narrated H.264/AAC export with original music/ambience/Foley and burned-in English captions.
- `captions-en.srt`: semantic single-line subtitles acoustically aligned offline to saved speech.
- `captions-vi.srt`: Vietnamese reading translation at dialogue-block times.
- `script-en.txt`, `script-vi.txt`: final edited scripts.
- `chapters.txt`: actual chapter starts for the upload description.
- `decoded-review-*.jpg`, `cover.jpg`: actual decoded movie samples and cover frame.
- `QA.json`, `voice-presence-checks.json`, `decoded-review.json`, `supporting-binding-checks.json`, `sound-rights.json`, `shots.json`, `manifest.json`: media, source, contact and review evidence.
- `source.zip`: portable editable code, saved native voices, timing, artwork, fonts/licenses and research-access record. No API key is included.

## Story and production

The opening introduces a field, a cow, a parked car and something hidden beneath the grass. Bolt's confidence and Ground's dry replies connect ground-current paths, energy/charge, fulgurites, contact voltage, animal contact span, conducting vehicle shells, thunder and shelter. Sand and Car are new supporting voices. The ending is one short exchange rather than several conclusions.

There are 47 active speech/scene blocks across six chapters, with local staged builds and close/detail inserts. Actions include a planted four-leg cow gait, branching current, changing contact markers, a growing glassy fulgurite diagram, inspection inset, finger-free educational silhouettes, a vehicle arrival with wheels stopping at rest, current paths around an occupied conducting shell, a closing window and expanding-air/pressure-wave diagrams. Scene changes are authored from meaning; a comparison card or macro inspection is not claimed as a moving camera in 3D. All detailed mechanisms are schematic, not CFD or a field reconstruction.

The main Bolt artwork/identity continues from the Short. One new generated transparent atlas supplies limb-free cow bodies and sand-grain expressions; the legs/arms and all scenery, vehicle and diagrams are locally animated. Visible-alpha tests verify supporting character roots are inside the body at the actual rendered sizes. The initial cow travel-to-foot phase mismatch was corrected before final export; the earlier picture is retained locally as `picture-pre-gait-repair.mp4`. The final gait uses the same eased travel for body and leg phase, with four attached fixed-length chains.

## Speech and sound rights

The cast uses native `tts-1` speed 1: Alloy narration, Echo Bolt, Onyx Ground, Shimmer Cow, Nova Sand, Fable Car. Eight exact dialogue clips reuse the Short's saved native audio. Forty-one new responses were saved once; no successful media was revoiced for picture repairs. Two newly recorded explanatory blocks were removed in editing to avoid repetition; their original files remain in the source archive and their cost is still included.

Estimated new speech cost is **USD 0.08202**, based on the previously documented USD 15/million characters rate. Billing is not account-verified. One new image-generation call produced the supporting atlas; its charge is not exposed. No new generation was used for the existing Bolt or the scenery.

Music is an original locally composed six-chapter plucked arrangement, with changing notes, rests, timbre and level. Room/outdoor beds, hoof contacts, a restrained strike/thunder rumble, diagram/reveal accents and window cue are original local synthesis. They are stylized cartoon sound, not real weather/material recordings or a physical distance simulation. No third-party song, soundtrack, footage or recording is extracted. Separate stems and native dialogue remain in the working project. DejaVu Sans Bold and its license are bundled.

## Science and access limits

See `science-notes.md` for the claim/qualification ledger. The account of charge, pulse duration, multiple paths, energy transfer, fulgurites and conditional contact voltage is conceptual. Colors, geometry, distances, current directions and times are schematic. No numerical safe radius, universal voltage difference, shoe-insulation claim or guarantee of vehicle/indoor invulnerability is given. The 30-minute instruction is standard thunderstorm shelter guidance after the **last** thunder, not a calculated property of the cartoon's field.

Direct reads of intended NWS and USGS pages were denied by the environment proxy with HTTP CONNECT 403. Those pages are not claimed as retrieved or freshly verified during this run. `research/sources.json` retains failed requests; a failed URL request does not establish that an article path exists. The script uses established concepts and standard shelter guidance, without new research claims, precise lightning temperatures, mortality statistics or numerical ground-current range. Further-reading URLs are identified as unverified this run.

## Checks and review limits

Checks cover full MP4 decoding, frame count, dimensions, A/V duration match, encoded loudness/true peak, caption coverage/order/width, saved speech presence, fixed bone lengths and the cow's stance-foot behavior. Source pose checks, decoded before/after frames and neighboring scene/cue evidence support the author's visual review. Pixel differences, successful encoding or geometry do not establish artistic quality, exact physical simulation or independent acceptance. Independent creative review and full real-time audiovisual listening were not performed. Creator approval is separate.

No YouTube upload or environment-configuration publication was performed. Delivery is on the previously authorized `video-delivery-b1` branch.

## Rebuild without paid generation

Python 3, Pillow, NumPy, PocketSphinx, FFmpeg and FFprobe:

1. `python prepare.py` uses saved native speech/offline alignment caches to build semantic captions.
2. `python animate.py` renders the native landscape picture and local motion traces.
3. `python finish.py` rebuilds original sound, masters/muxes the MP4 and runs technical QA.
4. `python review.py` decodes the final movie and checks speech/motion evidence.

`voice.py` is supplied for provenance, not needed for picture or sound edits. Do not delete saved media to force new calls. Recorded attempts with no response stop instead of automatically retrying. A missing reused clip must be restored from this archive rather than silently revoiced. The archive contains all required voices/images and reads no external prior project during ordinary rebuild.
