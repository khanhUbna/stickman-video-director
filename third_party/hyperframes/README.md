# HyperFrames upstream source and license

Source: https://github.com/heygen-com/hyperframes

Inspected commit: `aefca2baff396213711b59fcce5ec357896529c6`, version `0.9.88`, retrieved on 2026-11-24. The root source license and published CLI metadata identify **Apache-2.0**. `LICENSE` preserves the upstream copyright and license. `UPSTREAM.json` records all copied original skill-file hashes.

Nine source skill directories were copied into `.agents/skills/` without changing their original files: `hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use`, `figma`, `slideshow`, `remotion-to-hyperframes`, `reverse-any-video` and `style-sampling`. An Apache license copy was added to each installed directory. The source repository was inspected in a temporary checkout; no nested Git repository or automatic upstream updater was added.

The installed runtime is the separately pinned `hyperframes@0.9.88` npm release with lockfile integrity, not the entire upstream monorepo. It runs only through `engines/hyperframes-clay3d/scripts/hf.mjs`. This repository intentionally overrides upstream account, credit, telemetry, hosted rendering and automatic-latest instructions. Those workflows were not invoked and are not enabled by the installation.

Three.js is a distinct MIT-licensed dependency, Puppeteer/esbuild and transitive dependencies retain their own notices, and the existing project's MIT license is unchanged. The Apache license describes HyperFrames; it does not relicense every dependency or the existing application. The demo's procedural models, textures, posing and sound were authored locally for this project.
