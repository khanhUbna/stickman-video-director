# Why You Feel Guilty When You Rest — full clay film

Standalone local HyperFrames/Three.js production. The approved 637-word English V2 and full Vietnamese translation are in `script/`; evidence and limitations in `research/`. `STORYBOARD.md` follows actual recorded narration, not estimated timing.

From the repository root (Node dependencies are in the parent engine):

```bash
node engines/hyperframes-clay3d/films/rest-guilt-v1/scripts/build.mjs
node engines/hyperframes-clay3d/films/rest-guilt-v1/scripts/browser-qa.mjs
node engines/hyperframes-clay3d/scripts/hf.mjs check "$PWD/engines/hyperframes-clay3d/films/rest-guilt-v1" --json --no-craft --samples 12
node engines/hyperframes-clay3d/films/rest-guilt-v1/scripts/render.mjs
```

Reuse committed narration and master mix; do not call TTS again to rerender. Python narration/alignment/mix scripts document how assets were produced with free local tools. Model/venv caches are intentionally untracked. Voice model is Apache-2.0; Three.js MIT; HyperFrames Apache-2.0; Nunito OFL. See `licenses/` and the engine's pinned third-party records.

Output and caches are ignored. The approved delivery belongs in `deliveries/rest-guilt-clay-v1/`. No account/cloud/media/paid API is required. The parent CLI gateway blocks those commands. Previous Stickman/B6 and YouTube skills remain installed unchanged.
