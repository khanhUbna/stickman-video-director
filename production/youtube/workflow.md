# Title-to-review workflow

This repository installs all twelve upstream skills, with a Codex entry point in the root AGENTS.md. The automatic drafting sequence is **yt-research → yt-script → yt-package → yt-seo**, with research fact-checking after the script and before recording. This is agent orchestration, not a claim that a Python CLI can write researched scripts by itself.

When the creator provides a new title, Codex reads the four SKILL.md files and the channel profile, creates/resumes its folder, then writes the actual deliverables there. The CLI creates a scaffold and runs local checks; placeholders are explicitly pending. It never fetches facts, calls an LLM/TTS API, renders a film, or publishes.

```bash
python3 scripts/youtube_agent.py init "Why You Feel Guilty When You Rest"
python3 scripts/youtube_agent.py lint youtube-videos/RETURNED-DIRECTORY
```

Each title maps to a safe readable slug plus a title hash. Repeating init resumes without overwriting existing files. Use an explicit different `--slug` for a separately commissioned video with the same title. Filenames supplied by a pasted title cannot escape the output directory or become shell commands.

## Each video's files

```text
youtube-videos/<slug>-<title-hash>/
  manifest.json
  research/
    brief.md
    sources.json
    claims.json
    factcheck.md
  hooks/
    hooks.txt
    review.md
  outline.md
  script/
    script-en.txt
    script-vi.txt
    script.json
  voice-over/
    voiceover-en.txt
    README.md
  retention-review.md
  storyboard.md
  metadata/
    titles.txt
    package.md
    thumbnail-text.txt
    thumbnail-brief.md
    description.txt
    tags.txt
    seo.json
    upload.json
  checks/
```

## Research and verification

Save the retrieved source identity, stable URL/DOI when actually established, access status and the sections read. Use peer-reviewed primary work, systematic reviews or meta-analyses where suitable; reputable institutional explanations can support context. A URL, a search snippet, a sourcekit keyword hit or an abstract alone does not establish every claim in a paper. Respect the environment's network policy; record blocked access instead of bypassing it or claiming a source was read.

Run sourcekit.py's `index` command only on a saved working copy in this video's research directory: it writes an adjacent `.index.json` file. Preserve the creator's original uploaded source. The tool locates text; it does not download papers or establish that an interpretation is scientifically valid.

`research/sources.json` is an array of source records, each with `id`, `title`, `url`, `kind`, `access_status`, `sections_read` and `limitations`. Use `access_status: "read"` only for material actually accessed/read. `research/claims.json` holds `id`, `paragraph`, `claim`, `verdict`, `source_ids`, `evidence_locator`, `evidence_excerpt` and `limitations`. Use SUPPORTED, NOT IN SOURCE, CONTRADICTED, OVERSTATED, FLAGGED or UNVERIFIED honestly. Do not insert example studies or fake DOI placeholders into a completed record.

Apply yt-research's independent check to the precise cited passages after drafting. Record who checked, source locators, verdict counts and corrections in factcheck.md. If independent checking is unavailable, say so. Unsupported/inaccessible claims must be removed, narrowed, explicitly framed as uncertainty, or left flagged before recording. The local CLI validates file structure and evidence fields, not scientific truth.

## Writing and retention

Write five hooks; save one per line in hooks.txt, rank with hookscore.py, and record the editorial selection in review.md. The opening must deliver the title's actual promise. A number or a high score is never a reason to invent research.

Use all seven stages in outline.md. Keep spoken English in script-en.txt and its Vietnamese reading translation in script-vi.txt. Keep staging notes and citations outside the counted 550–650 words. Record proper names/source identifiers in script.json. Prepare voiceover-en.txt from the same reviewed wording; it is text, not generated audio.

Run scriptcheck.py with the channel override `--words 550-650`; read both errors and warnings. Its 30–75-word paragraphs, minimum hook score and punctuation rules are editorial/provider defaults. Resolve genuine readability problems and record justified dialogue/style exceptions in retention-review.md. Do not invent numbers, remove useful dialogue or add filler merely to make a heuristic pass.

The retention review is an editorial assessment of likely weak moments, repeated ideas, unresolved promises, the midpoint turn and the ending's changed action. It is **not** measured audience retention. Use yt-retention/retention.py only with an actual supplied Studio CSV; do not generate analytics from a draft or claim its score predicts views.

The storyboard maps each narration section to a concrete action, outcome, view, prop ownership and camera intent. Estimate timings initially, then align to actual accepted speech later. Plan natural 4–5-minute delivery; do not claim word count proves final runtime or stretch voice to fit an estimate.

## Packaging and SEO

yt-package prepares ten title candidates and the three strongest complete packages. Run title.py and treat length/thumbnail-word suggestions as heuristics; honor a supplied/approved title. Thumbnail text complements the title without revealing the whole explanation. Preview at feed size.

yt-seo writes description.txt, tags.txt and three actual search-intent queries in seo.json. Put the useful promise in the first two description lines and cite actual sources. No invented view/CTR claims, keyword stuffing or fabricated chapter times. Verify current official YouTube documentation before relying on platform-limit claims in the upstream prose. upload.json is draft metadata, not an account change.

## Review and media

Present the English script, Vietnamese translation, selected hook/package, factual limitations and local lint findings. The creator reviews the script before full media work. Do not repeatedly ask to approve steps already authorized. No paid API or publication is part of this workflow; request-specific explicit authorization must change that policy before any paid service is used. A key in the environment is not authorization.

## Installation and tests

```bash
python3 scripts/youtube_agent.py check-install
python3 scripts/test_youtube_agent_upstream.py
python3 -m unittest discover -s tests -p 'test_youtube_agent_integration.py' -v
```

The upstream suite is retained byte-for-byte with fixtures under third_party/youtube-agent-skill. The runner builds an isolated temporary upstream layout using the **installed skill copies**, then executes the original tests. No dependencies, account, network or API calls are needed. The source pin/license/hash manifest is UPSTREAM.json in that folder. See SECURITY_REVIEW.md and reports/ for the actual installation results.
