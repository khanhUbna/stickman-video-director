# The Pump Is Off. Why Is Water Still Flowing?

32-second English Short for Everyday, Explained. Native 1080x1920 portrait composition at 30 fps, with eight story-specific scenes. This is separately authored portrait animation, not a crop or stretch of the landscape episode.

The hook immediately shows an OFF pump and flowing faucet. A brief flashback shows filling an elevated vented tank. The main mechanism shows stored water above a lower tap, declining tank level and continued outlet flow while the pump is off. Drop then operates the switch, the pump starts and the tank refills. Tank says “Teamwork”; Pump returns to “I'm supervising.”

## Media

- `pump-off-water-still-flows-short.mp4`: finished picture, saved native English dialogue, original music/ambience/Foley, burned-in single-line English captions.
- `captions-en.srt`: semantic single-line captions acoustically aligned offline to the saved voices.
- `captions-vi.srt`: separate Vietnamese translation for reading/review, at dialogue-line times.
- `cover.jpg`: decoded opening-frame cover; no extra generated thumbnail.
- `decoded-review-1.jpg`, `decoded-review-2.jpg`: decoded samples across all eight scenes, before and after the principal local action.
- `QA.json`, `decoded-motion-checks.json`, `sound-rights.json`, `shots.json`: technical and provenance records.
- `source.zip`: portable source, saved dialogue, artwork, font/license and timings.

## Reuse, cost and rights

All nine dialogue clips reuse native saved files from `water-full-v1`, preserving voices, speed and wording. No new paid TTS, transcription, image or video-generation call was made. Offline PocketSphinx aligns known spoken text. Original blue hardhat droplet assets and DejaVu Sans Bold/font license are reused; machinery/scenery are original drawing code. New music and stylized Foley/ambience are original local synthesis, not a library song or another channel's soundtrack. Voice, music, ambience and Foley stems remain separate in the working folder. Billing of this Short's new external generation is zero; local computation not priced here.

## Scientific scope and review

This is one simplified reservoir-supply/elevated-storage mechanism, not a universal description of all home water supplies. Pipes are normally full. Tank headspace is vented; in the gravity proof its water surface stays above the tap. The geometry, water-level rates and time jumps are illustrative, not CFD, scale or a claim of instantaneous real-world refilling. Inlet flow and rotor state follow the switch; water does not gain energy from an off pump.

Technical checks cover full decoding, 960 frames, dimensions, duration agreement, subtitle text/ordering, loudness/true peak and file hashes. Author inspection covers source poses and actual decoded picture samples, including both sides of cuts and switch contact. Pixel differences support motion checking but do not establish semantic or artistic quality. No independent reviewer or full real-time audiovisual listening review is claimed. Creator viewing approval is separate. No YouTube upload and no environment configuration publishing occurred.

## Rebuild

Python 3, Pillow, NumPy, PocketSphinx, FFmpeg and FFprobe. Run `python short.py` from the extracted folder. It reuses the saved WAVs; there is no API generation code in this Short project. `drawing.py` retains the prior drawing helpers; only the portrait staging in `short.py` is used. `python review.py` writes decoded evidence. Exclude caches and large intermediate stems when bundling source.
