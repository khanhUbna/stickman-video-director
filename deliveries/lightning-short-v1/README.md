# Where Does Lightning Go After It Hits the Ground?

Everyday, Explained — new 35-second native portrait animated science Short, 1080x1920, 30 fps. This is the everyday-science channel, not the green-vest psychology channel or the Koa/B6 story series.

## Current stage: animation preview, voice pending

The animation, original music/ambience/Foley and editorial English/Vietnamese caption drafts are ready for a viewing export. New OpenAI speech requests returned HTTP 401; no native speech response was saved. The user selected updating the credential in the environment, but has not yet confirmed completing that update. No automatic audio retry or substitute voice is used. A preview filename explicitly says `no-voice`; it is not represented as the finished narrated film. Estimated draft caption times must be acoustically aligned after actual speech exists.

## Story

Bolt thinks hitting the ground finishes the job. Ground replies that it is not a trash can. A cutaway shows current branching through and along the soil during a brief strike. Two foot contacts are marked A and B, not given invented numerical voltages. A neutral human diagram shows how a voltage difference can drive current through the legs/body. The closing advice is to get inside a substantial building when thunder is heard. The ending does not offer an outdoor safe distance or a risky outdoor exercise.

## Scientific scope

- Ground current and step voltage are conceptual principles, not a prediction of a specific strike. Shape, depth, duration, colors, arrows and relative placement are schematic; the ground is not assumed uniformly conductive in reality.
- The current is associated with a brief lightning pulse. The cutaway is explicitly marked **BRIEF PULSE / SLOWED DOWN**, and the body diagram **SIMPLIFIED / SLOWED DOWN**. It is not a claim that lightning flows underground for the full video's duration.
- Feet **can** be at different voltages; the diagram is one illustrative arrangement, not a claim that all foot positions always differ. A/B colors are identifiers, not measured positive/negative values.
- The animated lightning mascot and Ground are fictional presenters. The body is a diagram, not someone demonstrating this outside. No injury/gore, shoe-insulation claim, numerical safe-radius rule or advice to shelter under a tree is included.
- The occupied substantial building is shown enclosed, with the person inside and away from the exterior window/door. It is not an open picnic shelter or a promise of absolute immunity.

## Sources and access limits

Intended official reference pages:

- https://www.weather.gov/safety/lightning-struck — ground-current mechanism.
- https://www.weather.gov/safety/lightning-tips — indoor shelter guidance.
- https://www.cdc.gov/lightning/safety/index.html — general lightning safety.

Direct reads were denied by the environment's outbound proxy (`Tunnel connection failed: 403 Forbidden`). Those pages are **not** claimed as retrieved or checked on this production run. Evidence of the failed attempts is saved under `research/`. The script is limited to established ground-current, step-potential and indoor-shelter principles, with no statistics or new research claims.

## Art, motion and audio

One new transparent four-expression yellow Bolt atlas was generated. The mascot has separately animated two-bone arms/legs and pinned feet. Soil, branching current paths, voltage-contact diagrams, body silhouette, house and Ground face are original locally drawn animation, using the science channel's navy/teal/cream/yellow palette. The picture is a native portrait composition, not a crop of a landscape video. No rapid full-screen white flashes are used.

Music is an original locally composed plucked pattern; ambience, a restrained designed strike rumble and reveal cues are original local synthesis. No third-party recording, song or video is extracted. DejaVu Sans Bold is bundled with its license. New image billing is not exposed by the tool. No successful TTS response or verified TTS billing is claimed yet; rejected authentication attempts are recorded, not automatically replayed.

## Verification and rebuild

Technical checks cover full decoding, dimensions, frame count, stream duration agreement, caption text/order and fixed-bone lengths. Decoded before/after samples are inspected separately from source stills. Metrics do not establish semantic correctness or independent creative/AV acceptance. Independent review and real-time listening are not claimed. No YouTube upload or environment-configuration publication is performed.

Python 3, Pillow, NumPy, optional PocketSphinx for actual speech alignment, FFmpeg/FFprobe:

1. `python prepare.py` writes editorial preview timing while voice is absent; after real speech exists it uses offline acoustic alignment.
2. `python animate.py` renders the picture and local motion trace.
3. `python finish.py` produces a clearly named no-voice preview, or a narrated export only when real native audio is present.
4. `python review.py` extracts actual decoded evidence.

`voice.py` is not a picture-rebuild dependency. Do not remove saved files to force regeneration. Its authentication-failure records must be preserved; retry is only appropriate after the user confirms fixing the credential, and saved native responses must always be reused.
