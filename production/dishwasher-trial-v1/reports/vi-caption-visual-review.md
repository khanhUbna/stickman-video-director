# Independent Vietnamese caption visual review

Reviewed 25 November 2026 by separate `/root/dishwasher_factcheck` reviewer, who did not author the captions or graphics. **No blocking caption issue found in this pass.**

Final `your-dishwasher-thinks-youre-the-problem-1080p-vi-sub.mp4` SHA-256 independently verified: `3e85395f7b53aaaea056774e65a6754dc10dc3916a372df5f176fe1a3dd2a10a`.

Inspected five actual decoded frames: `vi-decoded-10.5.jpg`, `61.5.jpg`, `98.6.jpg`, `108.7.jpg` and `173.jpg` (all under `reports/`). Vietnamese accents render clearly; the long courtroom caption fits horizontally; no right/bottom clipping or doubled English subtitles is visible. Captions leave the bowl/hand contact, spray-arm collision, water diagram and rack action visible. English lettering within the original scene artwork remains present.

Read all82 entries in `captions-vi.json` for gross translation meaning against the reviewed English script. Mechanism, scraping/pretreatment exceptions, model-specific filter care, detergent, fault uncertainty and the limited verdict for this load retain their meaning. No material reversal or omission found in that reading. `scripts/render_vi.py` calls the original frame with `captions=False`, consistent with the absence of English subtitle duplication.

Scope: one representative decoded-still pass, caption-text reading and renderer inspection. No human-auditioned playback, every-frame visual review, Vietnamese voice generation or new science review. The original audio is English; stream identity and full decode are documented by the primary technical checks, not independently re-auditioned here.
