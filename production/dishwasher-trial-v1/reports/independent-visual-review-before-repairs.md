# Independent visual review — repair required

Reviewer: separate `/root/dishwasher_factcheck` agent, who did not author the graphics. Reviewed 25 November 2026. Output reviewed: `deliveries/dishwasher-trial-v1/your-dishwasher-thinks-youre-the-problem-1080p.mp4`, SHA-256 `55526ac5a08f51a6d3ba27c6a30553343fb45d0abb060cbd334a306f86a0e870`.

Scope: inspected both actual decoded contact sheets, all seven supplied detail frames, and independently extracted final-MP4 frames at98.566s,105.3s and108.6s; correlated implementation and word timings. This is still-frame/code review, not human-auditioned playback or exact B2/B6 reference acceptance.

| Priority | Finding | Evidence | Required repair |
|---|---|---|---|
| P1 | Arm clears before narration describes the collision. | `detail-arm.jpg` at106.533s has already moved the utensil out of reach while caption says “turns the lower spray arm”; at108.6s the actual MP4 says “It bumps into a long utensil” over a clear arm and CLEAR label. `film.py:61` uses local/3.6 for a9.56s utterance. | Hold visible collision through “bumps” (108.55s); move utensil at “Sam moves it” (111.73–112.29s); begin unobstructed rotation/CLEAR around “turns freely” (113.11–113.77s). |
| P1 | The inset lifting hand does not touch the bowl. | Independently decoded98.566s frame: hand center approximately(570,182); bowl upper-right approximately(558,208), leaving about14px clear after the hand radius. `artwork.py:172–173` separates the bowl top and hand endpoint. | Anchor the hand/arm endpoint to a visible bowl edge with persistent overlap throughout the lift; inspect a decoded mid-lift and final-lift frame. |

No P0 found. Sampled caption phrases fit the frame and remain readable, loading bowl openings face downward toward the illustrated spray, the corrected rack has separated bowls, the final cleared arm has no obstruction, and rack/arrange/filter/gavel grips visibly meet their props. Character limbs remain coherent in the inspected frames. These findings do not establish every animation frame's contact or full audio synchronization.

The water-panel separator glyph renders as a missing-glyph box in `detail-water.jpg`; the primary reviewer already identified it and queued an ASCII replacement. It is a readability repair, not an additional factual issue.

Status: two P1 repairs pending. Preserve this rejected-version record; review the replacement MP4 and its decoded repair frames before marking visual review complete.
