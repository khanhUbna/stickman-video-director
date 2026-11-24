# Installation and local-use review

## Scope actually reviewed

- Upstream root LICENSE, npm manifests, CLI entrypoint and official Codex skill manifest.
- HyperFrames, CLI, registry and media-use skill entrypoints and relevant rendering, browser, 3D and character references.
- Plugin launcher process execution/version selection; CLI telemetry policy; browser path selection; cache directory behavior; Three.js deterministic seek adapter.
- Actual published `hyperframes@0.9.88` license/version/integrity and the package-lock used by the new engine.

This is a focused integration review, not an audit of every file in the 10,000+ file upstream repository.

## Installation choices

- Installed dependencies only in the separate engine directory using `npm install --ignore-scripts`; no package lifecycle hooks or monorepo prepare/Git hooks were executed.
- Preserved the inherited proxy and TLS verification. No token was extracted, displayed or written to tracked files.
- Original upstream skill files are unchanged and hash-pinned. Their paid-provider and telemetry advice is overridden explicitly in AGENTS.md, rather than silently rewritten as if it were upstream.
- The local gateway rejects account, billing, cloud rendering, provider-generation, share/publish and telemetry commands, and sets `HYPERFRAMES_NO_TELEMETRY=1` / `DO_NOT_TRACK=1`.
- Browser scene QA intercepts and blocks outbound requests. The actual scene uses local JS/audio and procedural content only. The gateway is a workflow guard, not a security sandbox for arbitrary untrusted compositions.
- Installed npm dependency audit returned zero reported vulnerabilities at installation time. This is a point-in-time tool report, not a guarantee of safety.

## Preservation and verification

Before installation, 763 tracked existing renderer/YouTube-skill/support files were SHA-256 recorded. After installation they were unchanged. YouTube's `check-install` passed for all 12 skills and their dependency imports. All 333 original HyperFrames skill files matched upstream hashes. The existing root license and old renderer package/lockfiles were not changed.

Host/runtime verification, actual browser motion checks, render execution and decoded video reports are copied into the delivery's `reports/` directory. Optional Whisper, Kokoro and MusicGen are not installed or needed, so the general doctor report's overall `ok` can be false while the required local renderer dependencies and actual MP4 render pass.

Chromium uses software WebGL on this host. Browser sandbox availability is constrained by the managed container; the checked scene is original project-local code, not an arbitrary external website. No host sandbox settings were changed.

Authored files and installed skills passed the Git whitespace check. The generated `assets/vendor/three.min.js` bundle retains upstream GLSL string indentation/trailing spaces and is excluded from that formatting-only check; shader strings were not rewritten to silence it. Its MIT license is retained, and the runtime/browser/video checks cover the actual bundled code.
