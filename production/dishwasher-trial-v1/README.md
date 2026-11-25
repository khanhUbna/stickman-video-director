# Your Dishwasher Thinks You're the Problem — Objects on Trial

Complete new native landscape2D cartoon project. Approved556-word script, four OpenAI roles and original local artwork. Actual recording/edit timing is194.9seconds (about3:15), not the earlier4:00–4:30 planning estimate. No speech slowdown or filler to hit that estimate. Output1920×1080 at30fps, captions in one semantic line, original quiet instrumental score and designed Foley.

## Reproduce without paying again

Run from repository root:

```bash
/workspace/.venvs/clay-narration/bin/python production/dishwasher-trial-v1/scripts/align.py
python3 production/dishwasher-trial-v1/film.py
python3 production/dishwasher-trial-v1/scripts/render.py
/workspace/.venvs/clay-narration/bin/python production/dishwasher-trial-v1/scripts/mix.py
```

Use the saved recordings. Do NOT rerun narrate.py to render again. The saved ledger prevents automatic retry/revoice. OpenAI was explicitly authorized for this new film up toUSD0.20. Four successful requests totalUSD0.09558 estimated from3,186characters at officialUSD30/million characters; invoice not accessed. No image, music, video or transcription service was paid.

Local dependencies: Python3, Pillow, NumPy, FFmpeg; alignment/mix environment additionally SoundFile and FasterWhisper with already cached base.en. Mux command and technical checks are documented in scripts/check.py and final reports. All source graphics are editable in artwork.py; camera views rasterize geometry/fonts at native output pixel scale. No previous720p video was enlarged. Existing Stickman/YouTube/HyperFrames engines and previous deliveries remain unchanged.

## Direction and scope

Sam, a personified dishwasher and judge are a new original cast. This is a channel-specific colored2D courtroom cartoon, applying the directing-stickman-videos action/contact, semantic caption, original-speed voice and QA workflow. No exact B2/B6 public-sample equivalence is claimed. User requested full production after approving the script; no sample approval was fabricated or added through an approve command.

Recorded voices: Nova narrator, Echo Sam, Alloy dishwasher, Onyx judge. The four source recordings were locally word-aligned and assembled by actor turns. Their actual speech samples and rate remain unchanged; small action/reaction gaps are added between turns.553/556 word anchors matched exactly; three alignment tokens interpolated. Audio is technically measured, not human-auditioned.

All59shots are specified in timeline.json. Physics diagrams are illustrative. Script and factual review remain at youtube-videos/your-dishwasher-thinks-you-re-the-problem-9012e9e5e1. Example appliance instructions are based on Bosch SHEM63W55N/11, not every model. The clean retest is fictional and makes several corrections together, not an isolated causal experiment. No YouTube publication.

## Vietnamese caption edition

Run `python3 production/dishwasher-trial-v1/scripts/localize_vi.py`, then `python3 production/dishwasher-trial-v1/scripts/render_vi.py` from repo root. This uses the approved Vietnamese performance translation and real English sentence/turn anchors. Long Vietnamese sentences are split for reading within the same source interval; this is display timing, not forced alignment to a Vietnamese voice. The Vietnamese render calls the original frame renderer with English captions disabled and draws only Vietnamese captions. It caches `vi-part-*` separately; run only one render_vi process at a time. Mux its `output/picture-vi.mp4` with a stream copy of the original English MP4 audio.
