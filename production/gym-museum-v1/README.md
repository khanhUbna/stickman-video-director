# They Found a Gym. And Got It Wrong. — 2D production

User approved full English production using ChatGPT/OpenAI speech after V3 script and 2D format discussion. Approved 1,013-word script is preserved exactly in performance.json and script-en.txt. Six spoken roles, 11 scenes. New original clothed 2D cast and story-specific sets; applies directing-stickman-videos contact, semantic caption and audio QA principles. No claim of exact B6 painted-reference equivalence.

## Current checkpoint

- Native 1920×1080 body-action study encoded, silent and clearly labeled, 20 seconds at 30 fps. Four contact/acting sequences. It is a motion study, not the final film or timed voice-over.
- Editable artwork.py and film.py cover the 11 narrative scenes and 126 provisional shots. Actual shot lengths must follow recorded speech.
- Cast: Vale, gray hair/glasses/teal jacket/tan vest; Mina, dark ponytail/orange field outfit/tablet; distinct member, coach and clerk; robot.
- First pose checks exposed crossed legs; knee direction and stance height corrected. Review current decoded study, not stale test images. Final creative/playback and sound review remains pending.
- Voice plan: 7 requests, 5,957 characters, tts-1-hd, USD0.17871 estimated at the officially checked USD30/million characters. Proposed cap USD0.20. Narrator split below provider input limit, all six roles preserved. Requests have per-chunk hashes and an attempted-before-network ledger with no retry.
- **No paid TTS authorization has been recorded for this film. No speech request made.** Previous-film spending approvals are not reused. authorization.json remains false. Do not change that flag without the creator's explicit reply.

## Resume after voice-budget authorization

Record the actual new user reply and maximum_usd in authorization.json, then:

```bash
python3 production/gym-museum-v1/scripts/narrate.py
/workspace/.venvs/clay-narration/bin/python production/gym-museum-v1/scripts/align.py
python3 production/gym-museum-v1/scripts/captions.py
python3 production/gym-museum-v1/film.py
python3 production/gym-museum-v1/scripts/render.py
/workspace/.venvs/clay-narration/bin/python production/gym-museum-v1/scripts/mix.py
```

Reuse saved speech after initial generation. Do not rerun/retry failed or ambiguous requests automatically. No paid transcription: alignment uses cached local FasterWhisper. Do not alter accepted speech speed to hit provisional runtime. Final mux, full decode, loudness/caption/order verification and every-shot creative review are still required before a final-video claim. Preserve prior projects and keep YouTube publication disabled.

## Rights

Original code-drawn artwork, animation and locally synthesized music/Foley. No image, video or music API calls. Noto Sans uses the installed skill font; existing license remains at skills/directing-stickman-videos/assets/fonts. Voice rights/cost ledger will be updated only after actual generation.
