# Gym museum20s — motion revision V2

Creator rejected V1 walking as robotic. V1 delivery/source are preserved. This revision reuses every recorded English voice sample and the exact caption/timing files. Zero new TTS or other paid calls; original sample spend remains estimatedUSD0.0084, not another charge.

## Actual changes

- New side/three-quarter locomotion drawings preserve Vale/Mina colors, hair, glasses, vest and ponytail. Front dialogue views remain at explicit cuts.
- gait.py authors independent foot contact schedules, smooth start/brake trajectories, heel-load/toe-off pivoting, swing clearance and a belt gait. Both walking knees bend forward instead of the old front-view outward/X geometry.
- locomotion_art.py adds pelvis/shoulder counter-motion, knee compression, arm pendulums, head stabilization and ponytail lag. The belt uses equal alternating landing positions; the safety clip follows Vale's moving torso.
- Rubber-step Foley is re-spotted to actual new touchdown times. Speech content, native samples, rate, pauses and captions are unchanged.

## Deliverables

../../deliveries/gym-museum-preview-v2/gym-museum-20s-en-motion-v2-1080p.mp4 — native1920×1080,30fps, exact20.00s, English narration/dialogue, burned English captions and original soundtrack.

before-after-gait-20s.mp4 — matching-time side-by-side V1/V2 at reduced display scale, with the revised audio once; not the main native-resolution deliverable. Optional English/Vietnamese SRT sidecars included.

## Reproduce for free

Reuse saved voices. Never rerun speech generation. Run scripts/verify_motion.py, film.py, then the local narration venv's scripts/mix20.py, scripts/render20.py, mux output/picture20.mp4 with audio/mix20.flac to the delivery MP4, then scripts/verify20.py. CLI paths follow the V1 project with this V2 directory substituted.

Motion tests sample1156poses at120Hz, enforce fixed chains, check shoe-ground clearance, locked floor pivots and belt-carried pivots, render all600actual frames, and compare saved voice/caption hashes to V1. These are technical constraints, not proof of human-like naturalness. Current decoded MP4 evidence supports review; full-speed human perception/listening and creator acceptance are not falsely claimed.

Scope is this sample's authored paths. New characters, routes or speeds need new choreography and review; this is not a universal mocap system. Full-film production and YouTube publication remain pending. Source provenance/rights and native TTS recordings are retained from V1.
