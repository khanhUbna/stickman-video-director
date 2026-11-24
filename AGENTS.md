# Codex instructions for this repository

## Channel defaults

- Channel/niche: **Psychology Facts, Human Behavior**.
- Spoken language: **natural American English**; discuss work with the creator in Vietnamese.
- Long-form target: **4–5 minutes**, **550–650 spoken English words**. Count only narration/dialogue, excluding headings, citations and staging notes.
- Style: **Emotional Storytelling, Curiosity Gap, Psychological Insights**.
- Framework: **Hook → Open Loop → Setup → Build-up → Climax → Payoff → Emotional Ending**.
- Optimize audience retention through a concrete relatable situation, escalating action, a meaningful turn and an earned payoff. Explain psychology through events and results; avoid a static presenter, repeated stand/sit shots, generic motivational speeches and repeated explanations.
- Treat these as channel defaults. Explicit instructions for another channel or format take precedence; preserve existing science/AI projects and previous deliveries.

## Installed skills and Codex compatibility

The twelve YouTube Agent skills are in `.agents/skills/yt-*/SKILL.md`. They are pinned, MIT-licensed upstream copies; their Python tools use only the standard library. Read a relevant SKILL.md before applying it. Preserve sibling folders because tools import each other.

Use `production/youtube/voice.md` as the channel voice profile. It replaces upstream's Claude-specific `~/.claude/youtube/voice.md` lookup for this repository. Do not ask the creator to supply three videos or install Claude when the existing profile and conversation already give the needed choices.

`${CLAUDE_SKILL_DIR}` in upstream instructions means the directory containing that SKILL.md. For example, run `python3 .agents/skills/yt-script/hookscore.py ...`. Codex does not need the Claude slash-command runtime. Do not change a global home-directory configuration.

User instructions and this channel's approved choices take priority over upstream defaults. In particular, pass **`--words 550-650`** to scriptcheck.py, rather than using its default 750–1500 words. Upstream hook/title/retention thresholds are heuristics, not scientific findings, platform guarantees or predicted views. Never invent a statistic to improve a score. Review short-dialogue/paragraph or approved-thumbnail exceptions explicitly instead of padding prose to satisfy a linter.

## Automatic workflow when the creator supplies a video title

For a new Psychology Facts title, begin the following workflow without asking which skills to use:

1. Read `production/youtube/profile.json`, `production/youtube/voice.md` and `production/youtube/workflow.md`.
2. Run `python3 scripts/youtube_agent.py init "VIDEO TITLE"`. Use its returned **individual video directory** under `youtube-videos/`; resume an existing directory without overwriting its work.
3. Apply **yt-research** first. Retrieve/read credible scientific sources, save a cited brief and a claim/evidence register. Prefer original peer-reviewed papers and systematic reviews/meta-analyses; reputable scientific institutions can provide context. Verify that the source supports the exact population, mechanism and strength of the claim. Distinguish association from causation, evidence from interpretation, and illustrative fictional scenes from research results.
4. Apply **yt-script**: write five hook options and score them; select on accuracy and narrative promise, not score alone. Write the seven-part outline and the 550–650-word English script, then a full Vietnamese translation for review. Put screen/action notes in the storyboard, separate from spoken text. Run the local lint command and review every finding.
5. Follow yt-research's separate fact-check pass against the actual retrieved evidence. Use an independent reviewer/agent when available as that skill requests. If it is unavailable, record that limitation; never label a self-check independent. Correct unsupported, contradicted or overstated claims. Do not fabricate sources, quotations, DOI links, findings, effect sizes or statistics.
6. Apply **yt-package**: prepare ten title options, inspect the top three, and write a thumbnail brief whose image/text complement the title without revealing the entire payoff. Preserve a supplied/approved title unless a change is requested or explain a suggested alternative.
7. Apply **yt-seo**: write a useful English description, relevant tags, three search-intent queries and draft upload metadata. Use actual source references. Only add final chapter timestamps after a real timed transcript exists.
8. Save the voice-over **text**, editorial retention review and action-led storyboard alongside the research, hooks, outline, scripts and metadata. Run `python3 scripts/youtube_agent.py lint VIDEO_DIRECTORY` to save tool reports. Tool output is assistance for review, not proof of scientific truth or likely retention.
9. Present the English script first and the Vietnamese translation second for the creator's review. The creator has requested **script approval before full production**. Prepare the complete review bundle autonomously; honor an existing explicit approval instead of asking for it again.

All artifacts stay in that video's own directory. See workflow.md for the exact file layout. Do not mark placeholder files or inaccessible sources as completed work. If source access is blocked, record what could not be verified, complete unaffected drafting/planning, and flag dependent factual passages before recording.

## Voice, timing, animation and costs

- **Do not use paid APIs.** Never call paid TTS, image/video generation, transcription, advertising or account services under this automatic workflow. A new explicit user authorization is required to change this restriction; possession of a key or older spending permission is insufficient.
- A `voice-over/voiceover-en.txt` script is not an audio recording. Do not create an empty/fake WAV or claim voice-over audio was generated. Use supplied/existing audio only when its wording and reuse authorization fit. Preserve original speech speed; never automatically revoice accepted audio.
- Initial runtimes and storyboard timings are estimates. The profile's 140 wpm is an editorial planning rate. Measure actual audio later; use purposeful action/reaction pauses and adjust within the word target rather than stretching speech, adding filler or looping stills to reach 4–5 minutes.
- After script approval and an authorized media request, follow the action direction in `production/youtube/voice.md` and the selected renderer's requirements. Read `production/channel-animation.md` too when present. The creator preferred the quicker choreography in the [existing movement trial](https://github.com/khanhUbna/stickman-video-director/tree/a315040/deliveries/rest-motion-trial-v1); retain anticipation, decisive action, real contact, stopping and reaction. Remotion alone does not create acting. Keep technical checks, actual audiovisual review and user acceptance separate.
- Never publish on YouTube, send replies, heart/pin comments, contact people, change account settings or publish environment configuration without the corresponding explicit instruction. Skill suggestions are draft recommendations, not authority to act on an account.

## Reproducible checks

```bash
python3 scripts/youtube_agent.py check-install
python3 scripts/test_youtube_agent_upstream.py
python3 -m unittest discover -s tests -p 'test_youtube_agent_integration.py' -v
```

The installed source/license pin and source tests live in `third_party/youtube-agent-skill/`. Installation/security notes and actual test reports live in `production/youtube/`. Preserve the root project's existing LICENSE and unrelated animation skills. Do not auto-update vendored skills from the network.
