# YouTube Agent Skill installation review

Reviewed on **2026-11-24** for `khanhUbna/stickman-video-director`.

## Source and scope

- Cloned source into `/tmp/youtube-agent-skill-review-20261124` from `https://github.com/utillayer/youtube-agent-skill.git`.
- Pinned revision: `e0ac1e7476e71bed780a6e2ae19a929e40146c87`.
- Read all twelve SKILL.md files, all nine Python tools (1,002 source lines in this revision), hooks.json, the original test suite, voice template, README, MIT license and CI workflow before running the source tests.
- Checked file inventory, symlinks, Python imports, subprocess/filesystem operations, network/credential/code-execution patterns and sibling dependencies.
- All 22 upstream skill files are installed unchanged. Each skill additionally carries the original MIT LICENSE. The root animation project's existing license and skills are preserved. Hashes and attribution are in third_party/youtube-agent-skill/UPSTREAM.json and NOTICE.md.

This is a source review of the pinned revision and exercised local paths, not a security certification of arbitrary future commits or arbitrary hostile input files. No automatic upstream updates are configured.

## Findings

The tools use Python's standard library and sibling modules only. No requests/urllib/socket client, credential lookup, secret-file reader, shell execution, dynamic eval/exec/pickle loading, installer or paid-API client was found in the reviewed tool code. No upstream symlinks or submodule bootstrap were present. No pip/npm dependencies were installed for this integration.

The tools read supplied local text/JSON/CSV/subtitle files. sourcekit.py's `index` command writes a derived sibling `.index.json`; the workflow restricts that operation to a research working copy. The other tools emit reports rather than editing video, logging into YouTube, posting comments or uploading content.

The upstream tests launch known local Python tools through argument arrays without `shell=True`. Their unlink operations target their own temporary fixtures. They were reviewed before execution. The installed-suite runner executes the original tests in an isolated temporary layout copied from the installed skills, so relative imports and fixtures are exercised without modifying channel work.

The local integration likewise uses no network/API service. Titles are data, slugs are validated, workspace output is confined to the repository, symlink redirection is rejected, existing work is resumed without overwriting, and a temporary initialized folder is renamed into place. Regression tests cover these boundaries, the 550–650-word override and incomplete/unread evidence.

## Codex and editorial adaptations

Upstream Claude paths and `${CLAUDE_SKILL_DIR}` are mapped in AGENTS.md to the local skill directory and production/youtube/voice.md. No global Claude profile, plugin installation, account or API key is required. Profile/template adaptations are separate from upstream files.

The title-triggered workflow applies yt-research, yt-script, yt-package and yt-seo and saves each video's actual work in a separate folder. A scaffold is explicitly pending; empty scripts/evidence cannot pass the integration lint as a completed draft. Voice-over output initially means reviewed narration text, not generated audio. Paid APIs and publication are disabled.

Hook/title scores are handcrafted editorial checks, not validated view/CTR/retention predictors. Numbers must not be invented to satisfy a score. Upstream title/thumbnail lengths and retention thresholds are heuristics. swipe.py infers Shorts from duration at most 180 seconds; verify actual format before comparing competitor groups. Upstream prose about platform limits should be checked against current official documentation when relied on. No scientific claim is validated just because a linter or source search passes.

## Test results and known warning

- Original source command: `python3 -W error::ResourceWarning -m unittest discover -s tests -v` — **42 tests passed**, Python **3.12.14**. Original output is retained in reports/upstream-source-tests.txt.
- The same unchanged suite against isolated copies of the installed folders — **42 tests passed**. See reports/upstream-installed-tests.json and .txt.
- **13 local integration tests passed**; results are retained in reports/integration-tests.txt. Installation inventory/hash/frontmatter/dependency checks are in reports/installation.json.
- With ResourceWarning promoted, upstream hookscore.py line 24 reports one unclosed `hooks.json` file at module import (`json.load(open(...))`). Python reports it as an ignored finalizer exception; the 42-test suite still returns success. It is a file-handle hygiene warning, not evidence of a network call or a failed assertion. The original file is retained unchanged so the pin/hashes remain reproducible. A future reviewed upstream fix can replace it with a `with open(...)` block; do not silently hide the warning or claim warning-free tests.

Only Python 3.12.14 was exercised in this environment; the upstream CI matrix was inspected, not rerun on every Python version. No paid API was used, no channel/account action was performed, and no environment configuration was published.
