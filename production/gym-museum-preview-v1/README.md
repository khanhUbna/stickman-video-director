# Gym museum — complete English 20-second review sample

Creator explicitly requested paid ChatGPT/OpenAI speech for a complete 20-second sample before deciding on the full film. Full film remains ungenerated. Original script excerpt: the live demonstration, Mina's warning, physical safety-clip attachment, then Vale's question and Mina's reply. The intervening narration about the attachment is represented visually rather than spoken so the sample fits naturally. No approved spoken line is rewritten.

## Deliverable

`deliveries/gym-museum-preview-v1/gym-museum-20s-en-1080p.mp4`: exact20.00s, native1920×1080,30fps, H.264/AAC, burned English captions, three native OpenAI voices, quiet original music and synchronized original Foley. English and Vietnamese SRT sidecars supplied; Vietnamese cues use English utterance anchors, not a Vietnamese spoken recording.

Alloy narrator, Onyx Vale, Nova Mina. Original speech samples/rate retained; silence between lines provides acting room. 49spoken words; 48exact local ASR anchors and one canonical interpolated token. Local FasterWhisper only; no paid transcription.

Five successful OpenAI requests: three initial role recordings and two new payoff lines, no retries or revoices. 280characters × USD30/million = estimatedUSD0.0084. Invoice not accessed. Official price saved in reports/tts-pricing.txt. authorization.json records the actual user reply; itsUSD0.02 ceiling is an assistant-imposed small-sample guard, not a numeric budget stated by the user. No other paid calls.

## Free reproduction using saved voice

Do NOT rerun narrate.py or extra_lines.py. Existing paid recordings are saved and must be reused.

```bash
/workspace/.venvs/clay-narration/bin/python production/gym-museum-preview-v1/scripts/align.py
/workspace/.venvs/clay-narration/bin/python production/gym-museum-preview-v1/scripts/assemble20.py
python3 production/gym-museum-preview-v1/film.py
/workspace/.venvs/clay-narration/bin/python production/gym-museum-preview-v1/scripts/mix20.py
python3 production/gym-museum-preview-v1/scripts/render20.py
```

Mux output/picture20.mp4 with audio/mix20.flac using video stream copy, AAC192k/48kHz stereo, `-t 20 -movflags +faststart`, then run scripts/verify20.py. Timing is exact recorded/aligned speech, not a word-count estimate. All600frames pass reachable fixed-length chain/caption-bound checks. Eleven authored shots cover the camera/banner, stepping, raised palm, speech, entrance, warning, hand-to-vest attachment, button touch, belt gait and deadpan reply.

Technical decode, exact duration, frame count, loudness, caption coverage/order, source fingerprint and cost checks are in reports/QA.json. Decoded frames reviewed for composition/contact; no independent aesthetic acceptance or full-speed human audition is claimed. User review is pending. No exact B6 sample-equivalence claim: original flat2D cartoon cast/sets, applying the installed skill's motion/contact/caption/audio principles. No YouTube publication.
