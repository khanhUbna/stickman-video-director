# Water motion preview — 15 seconds

Requested deliverable: one 15-second animated proof so the creator can judge the new everyday-science channel's motion before commissioning a full episode. This is a custom bright 2D cutaway, not a continuation of the Koa/AI films.

- `water-motion-preview-15s.mp4`: 1280×720, 30 fps, exactly 450 frames, English Alloy narration, burned-in English captions, original music and causal Foley.
- `captions-en.srt` / `captions-vi.srt`: separate English and Vietnamese subtitles.
- `decoded-review.jpg`: four frames from this final encoded MP4.
- `QA.json`: media and model checks, including local decoded-pixel comparisons.
- `source.zip`: editable component animation, generated mascot layers, saved speech, word timings, fonts and state trace.

## What actually moves

The camera remains fixed for the full 15 seconds. The mascot's arms/body/knees move to touch the motor switch, react and gesture. The impeller accelerates, rotates, decelerates and stops. Intake arrows stop with it. The tank's surface rises with inlet volume, then falls as the tap continues drawing water. The attached faucet lever rotates, the downstream flow markers move, and the water stream/splash animate independently of the pump.

At approximately 3.6 seconds the impeller is fully stopped; the tap remains open and water continues to flow. This is the main movement/causality proof, rather than a sequence of panned or zoomed stills. The mascot's face is generated artwork with separately animated limbs, not a video-generation-model clip.

## Scientific scope

This is a simplified example of an **elevated, vented storage tank** supplied with already-treated water. Distribution pipes are already full. The water surface stays above the tap outlet. The model uses a qualitative gravity-head flow relationship and a conserved tank-volume update; it is not CFD, a scale drawing or a prediction of a particular building's pressure. A non-return valve is shown on the inlet branch. The gray drain is separate from the blue supply. The faucet stem connects to the supply, separately from the falling stream.

Not every home or municipal system uses this configuration. The complete water-treatment journey is outside this short sample. Humorous water-droplet personification is illustrative.

## Audio, art and cost

One new `tts-1` / `alloy` request at speed 1, saved before picture timing. Native speech duration: 9.26 seconds, offset by 0.18 seconds; the complete picture lasts 15 seconds so the mechanism remains observable. Estimated speech cost: USD 0.00228, not account-verified. No revoice and no paid transcription.

One new image-generation call supplied a four-expression limb-free water-worker atlas: `exec-471f1a7d-4125-4fbf-a5f7-4d88d1529fd8.png`. Image billing is not exposed. The complete original atlas and extracted cells are retained. The mechanism, paths, impeller, tank, valve, water stream and environment are original animated drawing code. Music, motor, switch and water sounds are original local synthesis; no third-party audio recording is used.

DejaVu Sans Bold is bundled with its license in `fonts/DejaVu-LICENSE.txt`; that bundled font is byte-identical to the system file used for the reviewed render. The unused inherited Archivo Black font is retained with its SIL OFL in the source bundle.

## Checks and review limits

Full MP4 decoding passed. All 450 frames, stream dimensions, frame rate and durations were checked. The tank model conserves its illustrative volume update; level rises during pumping and declines after pumping stops. Sampled mascot switch contact and fixed limb lengths are checked, with feet pinned in world space. Decoded local-pixel checks show the running impeller changes, the stopped impeller region remains unchanged, and downstream water continues changing after the pump stops.

The author inspected full-size source samples and the decoded final MP4 review sheet for connections, water height, pipe routing, captions and pose states. Independent creative review and real-time audiovisual listening by the agent were not performed. Technical checks do not replace the creator's actual viewing decision.

Only this 15-second sample is produced. A full episode remains pending the user's decision. No YouTube upload was made.

## Rebuild

Python with Pillow, NumPy and optional PocketSphinx for re-alignment; FFmpeg/FFprobe are required. Saved narration, alignment and mascot PNGs are included. Do not run `generate_voice.py` for picture corrections.

1. `python animate.py stills` writes representative state/pose samples.
2. `python animate.py` renders all 450 new frames and the mechanism trace.
3. `python finish.py` creates original sound, masters the mix, exports subtitles and validates the MP4.

The delivery's final JPEG review sheet and decoded local-pixel measurements were extracted from the actual exported movie separately. No full-film production or user approval is inferred.
