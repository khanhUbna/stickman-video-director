# HyperFrames + Three.js clay animation engine

A separate local renderer for this repository. It preserves Stickman Video Director, its B6 assets/dependency lockfile, and all twelve YouTube Agent skills.

- HyperFrames **0.9.88**, Apache-2.0, pinned in `package-lock.json`.
- Three.js **0.187.0**, MIT, with its license distributed beside the local browser bundle.
- Node.js **22+**, Chromium with WebGL 2, Python 3 standard library, FFmpeg and FFprobe.
- No HeyGen API, paid service, login, credits, hosted rendering or generated stock assets.

## Run

From this directory:

```bash
npm ci --ignore-scripts --cache .cache/npm
npm run build
npm test
node scripts/browser-qa.mjs
npm run check
npm run preview
# In another terminal, or after stopping preview:
npm run render
npm run verify
```

The output is `output/clay-animation-15s.mp4`. The checked delivery copy is under [`../../deliveries/hyperframes-clay3d-15s-v1/`](../../deliveries/hyperframes-clay3d-15s-v1/). A first install needs the free npm registry; the authored composition and render assets are local.

`npm run doctor` checks the host. Its overall `ok` can be false when optional voice/transcription/music tools are absent. Those optional tools are not needed for this demo. Check Node, Chrome, FFmpeg and FFprobe individually, then use the real browser/render reports as evidence.

Codex Cloud uses `/usr/bin/chromium`, `/usr/bin/ffmpeg` and `/usr/bin/ffprobe` by default. Override `HYPERFRAMES_BROWSER_PATH`, `HYPERFRAMES_FFMPEG_PATH` and `HYPERFRAMES_FFPROBE_PATH` for another host. The renderer uses **software WebGL and screenshot capture** on this CPU-only host; rendering is slower than playback. No paid GPU is required.

## What is animated

The clothed gray-haired character walks into the room, notices a ball, squats, reaches and lifts it, inspects it, tosses and catches it, walks to the sofa, then sits and relaxes. The motion includes hips, torso, shoulders, elbows, knees, wrists, head, eyes and expression changes. Two-bone inverse kinematics preserves limb lengths. Stance feet remain at authored world-space anchors. A held ball follows the hand; a released ball follows an authored ballistic arc with head clearance.

The file is **1920×1080, 30 fps, 15 seconds, 450 frames**. Poses advance at **12 Hz** for an intentional clay stop-motion cadence. Three camera setups cut between views; there is no animated camera zoom disguising a static character. The sound is original local synthesis, with no samples, third-party music or voice API.

## Files to change for a new scene

- `src/motion.mjs`: deterministic actions, foot anchors, timings and prop ownership.
- `src/scene.mjs`: reusable rig, clay materials, environment, lighting and cameras.
- `src/main.mjs`: HyperFrames `hf-seek` integration, setup readiness and GPU readback.
- `index.html`: duration, canvas resolution and local audio track.
- `scripts/make_sound.py`: original procedural foley/notes.
- `SPEC.md`: intended acting and timing. `output/` contains actual QA, not acceptance by the creator.

For longer films, plan distinct action-led shots and reuse the rig across compositions. This engine does not automatically convert a B6 still into a rig or create acting from a script. The existing script-approval workflow remains in place.

## Local-only gateway and skills

Use `node scripts/hf.mjs <command>` or the npm scripts above. The gateway validates the pinned Apache-2.0 package and allows local preview, checks, rendering and read-only project utilities. It rejects remote media generation, cloud rendering, auth/login, billing, usage checks, telemetry events, sharing and publishing. Telemetry and update notices are disabled. All runtime caches use ignored project-local directories; no HOME or global Codex settings are changed.

Nine original HyperFrames skills live in `.agents/skills/`. Their provider/credit suggestions are upstream documentation, **not authorization** to use those services. The repository's root `AGENTS.md` states the local-only overrides. See [`../../third_party/hyperframes/`](../../third_party/hyperframes/) for source pin, licensing and installation review.

## Quality evidence

`browser-qa.mjs` blocks outbound composition requests, checks page errors, samples visible poses and audits all 450 frame states for limb reach and framing. It also checks repeat-seek image/joint determinism. `verify.mjs` fully decodes the MP4, checks duration/codec/resolution/frame count/audio and compares decoded frames with independent browser captures. Inspect the actual decoded contact sheet too. Neither these checks nor a linter guarantees artistic approval.
