#!/usr/bin/env python3
"""Offline Codex YouTube workflow scaffolding, installation checks and editorial lint."""
import argparse
import ast
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents" / "skills"
UPSTREAM = ROOT / "third_party" / "youtube-agent-skill"
EXPECTED = ("yt-audit", "yt-chapters", "yt-comment", "yt-edit", "yt-package", "yt-plan",
            "yt-research", "yt-retention", "yt-script", "yt-seo", "yt-shorts", "yt-viral")
PENDING = "Status: pending."


def profile():
    return json.loads((ROOT / "production/youtube/profile.json").read_text(encoding="utf-8"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def within(path, base):
    try:
        path.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def check_install():
    pin = json.loads((UPSTREAM / "UPSTREAM.json").read_text(encoding="utf-8"))
    errors, references, tools = [], [], []
    for name in EXPECTED:
        directory = SKILLS / name
        md = directory / "SKILL.md"
        if directory.is_symlink() or not md.is_file():
            errors.append(f"Missing/nonlocal skill: {name}")
            continue
        text = md.read_text(encoding="utf-8")
        front = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
        if not front or not re.search(rf"^name: {re.escape(name)}$", front[1], re.M):
            errors.append(f"Invalid frontmatter/name: {name}")
        if not front or not re.search(r"^description:[ \t]*\S", front[1], re.M):
            errors.append(f"Missing description: {name}")
        license_file = directory / "LICENSE"
        if not license_file.is_file() or digest(license_file) != digest(UPSTREAM / "LICENSE"):
            errors.append(f"MIT notice mismatch: {name}")
        for relative in re.findall(r"\$\{CLAUDE_SKILL_DIR\}/([\w./-]+\.(?:py|json))", text):
            target = directory / relative
            if not within(target, SKILLS) or not target.is_file():
                errors.append(f"Broken/outside dependency: {name}/{relative}")
            references.append(f"{name}/{relative}")
        for script in sorted(directory.glob("*.py")):
            tree = ast.parse(script.read_text(encoding="utf-8"), filename=str(script))
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imports.extend(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom):
                    imports.append(node.module)
            tools.append({"path": str(script.relative_to(SKILLS)), "imports": sorted(set(imports))})
    for relative, expected_hash in pin["files"].items():
        path = SKILLS / relative
        if not within(path, SKILLS) or path.is_symlink() or not path.is_file() or digest(path) != expected_hash:
            errors.append(f"Upstream file missing/changed: {relative}")
    for relative, expected_hash in pin["support_files"].items():
        path = UPSTREAM / relative
        if not within(path, UPSTREAM) or not path.is_file() or digest(path) != expected_hash:
            errors.append(f"Upstream test/template changed: {relative}")
    formulas = json.loads((SKILLS / "yt-script/hooks.json").read_text(encoding="utf-8"))["hooks"]
    if len(tools) != 9 or len(formulas) != 21:
        errors.append("Unexpected tool/formula inventory")
    return {"ok": not errors, "source": pin["repository"], "commit": pin["commit"],
            "skills_checked": len(EXPECTED), "tools_checked": len(tools), "hook_formulas": len(formulas),
            "dependencies_checked": len(references), "upstream_files_unchanged": not errors,
            "tools": tools, "errors": errors, "paid_API_calls": 0}


def artifacts(title, channel):
    framework = "\n\n".join(f"## {part}\n\n{PENDING}" for part in channel["framework"])
    return {
        "research/brief.md": f"# Research brief: {title}\n\n{PENDING}\n\nRecord actual sources read, supported mechanisms, uncertainty and story implications.\n",
        "research/sources.json": [],
        "research/claims.json": [],
        "research/factcheck.md": f"# Evidence review\n\n{PENDING}\n\nRecord reviewer independence, claim verdicts, source locators and corrections. Do not imply a completed fact check.\n",
        "hooks/hooks.txt": "",
        "hooks/review.md": f"# Hook selection\n\n{PENDING}\n\nWrite five hooks, lint them, and select on truthful promise and curiosity rather than a score alone.\n",
        "outline.md": f"# {title}\n\n{framework}\n",
        "script/script-en.txt": "",
        "script/script-vi.txt": "",
        "script/script.json": {"title": title, "names": [], "text": "", "sources": []},
        "voice-over/voiceover-en.txt": "",
        "voice-over/README.md": "# Voice-over\n\nText only until approved and authorized media work. No audio has been generated. Paid APIs are disabled. Preserve exact reviewed wording and original speech speed.\n",
        "retention-review.md": f"# Editorial retention review\n\n{PENDING}\n\nAssess promise, open loops, escalation, midpoint turn, repeated ideas and payoff. No measured retention or view forecast exists for a draft. Record justified lint exceptions here.\n",
        "storyboard.md": f"# Storyboard\n\n{PENDING}\n\nTimings are estimates until actual audio exists.\n\n| Beat | Spoken passage | Goal/obstacle | Action and visible outcome | View/camera | Props/ownership | Estimated seconds |\n| --- | --- | --- | --- | --- | --- | --- |\n",
        "metadata/titles.txt": "",
        "metadata/package.md": f"# Title and thumbnail package\n\n{PENDING}\n\nEvaluate ten candidates, present the top three and explain the chosen complementary image/text. Honor an approved title.\n",
        "metadata/thumbnail-text.txt": "",
        "metadata/thumbnail-brief.md": f"# Thumbnail brief\n\n{PENDING}\n\nOne dominant subject/conflict, readable expression, contrast, short complementary text and an honest curiosity gap.\n",
        "metadata/description.txt": "",
        "metadata/tags.txt": "",
        "metadata/seo.json": {"status": "pending", "queries": [], "sources": [], "chapter_timing": "not available before timed transcript"},
        "metadata/upload.json": {"status": "draft", "title": title, "language": "en-US", "category_suggestion": "Education", "channel_audience": "general adults", "publication_authorized": False},
        "checks/.gitkeep": "",
    }


def init_video(title, slug=None, repo=ROOT):
    title = title.strip()
    if not title or len(title) > 500 or any(ord(c) < 32 for c in title):
        raise ValueError("Supply a nonempty title without control characters, at most 500 characters")
    channel = profile()
    normalized = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode().lower()
    readable = re.sub(r"[^a-z0-9]+", "-", normalized).strip("-")[:64].rstrip("-") or "video"
    identifier = hashlib.sha256(title.encode("utf-8")).hexdigest()[:10]
    slug = slug if slug is not None else f"{readable}-{identifier}"
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,90}", slug):
        raise ValueError("Slug must contain lowercase letters/digits/hyphens only, at most 91 characters")
    base = repo / channel["output_root"]
    destination = base / slug
    if base.is_symlink() or destination.is_symlink() or not within(destination, repo):
        raise ValueError("Video workspace must stay inside the repository without symlink redirection")
    if destination.exists():
        manifest = destination / "manifest.json"
        if manifest.is_symlink() or not manifest.is_file():
            raise ValueError("Existing directory has no safe workflow manifest; nothing overwritten")
        if json.loads(manifest.read_text(encoding="utf-8")).get("title") != title:
            raise ValueError("Existing slug belongs to a different title; nothing overwritten")
        return {"directory": str(destination), "created": False, "status": "resumed without overwriting"}
    base.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".init-", dir=base))
    try:
        for relative, content in artifacts(title, channel).items():
            path = staging / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(content, (dict, list)):
                write_json(path, content)
            else:
                path.write_text(content, encoding="utf-8")
        write_json(staging / "manifest.json", {"schema_version": 1, "title": title,
                   "status": "draft", "profile": channel, "stages": {skill: "pending" for skill in channel["automatic_skills"]},
                   "script_approved": False, "audio_generated": False, "published": False})
        staging.rename(destination)
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    return {"directory": str(destination), "created": True, "status": "draft; all four agent stages pending"}


def lint_video(directory):
    install = check_install()
    if not install["ok"]:
        raise ValueError("Installed skills failed integrity checks; do not execute changed tools")
    base = ROOT / profile()["output_root"]
    if directory.is_symlink() or base.is_symlink() or not within(base, ROOT):
        raise ValueError("Video workspace must not use a symlink outside the repository")
    directory = directory.resolve()
    if not within(directory, base) or not within(directory, ROOT) or directory == base.resolve():
        raise ValueError("Lint only an individual video workspace inside youtube-videos/")
    manifest_path = directory / "manifest.json"
    if manifest_path.is_symlink():
        raise ValueError("Workflow manifest must not be a symlink")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    channel = profile()
    blockers, warnings, reports = [], [], {}
    for relative in artifacts(manifest["title"], channel):
        path = directory / relative
        if path.is_symlink() or not within(path, directory):
            raise ValueError(f"Unsafe artifact path: {relative}")
        if not path.is_file():
            blockers.append(f"Missing artifact: {relative}")
    checks = directory / "checks"
    checks.mkdir(exist_ok=True)

    def tool(name, args, report_name):
        process = subprocess.run([sys.executable, str(SKILLS / name), *map(str, args), "--json"],
                                 capture_output=True, text=True, encoding="utf-8", timeout=30)
        try:
            payload = json.loads(process.stdout)
        except json.JSONDecodeError:
            payload = {"error": process.stderr or process.stdout}
        write_json(checks / report_name, payload)
        reports[report_name] = {"returncode": process.returncode, "result": payload}

    def read(relative):
        path = directory / relative
        return path.read_text(encoding="utf-8").strip() if path.is_file() else ""

    hooks = [x for x in read("hooks/hooks.txt").splitlines() if x.strip()]
    if hooks:
        tool("yt-script/hookscore.py", [directory / "hooks/hooks.txt"], "hooks.json")
    if len(hooks) != 5:
        warnings.append(f"Expected five hook candidates; found {len(hooks)}")
    text = read("script/script-en.txt")
    word_count = len(text.split())
    if not channel["spoken_words"]["min"] <= word_count <= channel["spoken_words"]["max"]:
        blockers.append(f"Spoken word count {word_count}; required 550–650")
    sources = json.loads(read("research/sources.json") or "[]")
    claims = json.loads(read("research/claims.json") or "[]")
    if not isinstance(sources, list) or not isinstance(claims, list):
        raise ValueError("Sources and claims must be JSON arrays")
    if any(not isinstance(item, dict) or not isinstance(item.get("id"), str) for item in sources + claims):
        raise ValueError("Each source/claim must be an object with a string id")
    read_sources = {s.get("id") for s in sources if s.get("access_status") == "read" and s.get("sections_read") and s.get("url")}
    if not read_sources:
        blockers.append("No scientific source is recorded as actually read with a section locator")
    if not claims:
        blockers.append("Claim/evidence register is empty")
    for claim in claims:
        ids = claim.get("source_ids", [])
        if not isinstance(ids, list) or any(not isinstance(item, str) for item in ids):
            raise ValueError("Claim source_ids must be an array of source identifiers")
        if (claim.get("verdict") != "SUPPORTED" or not ids
                or not set(claim["source_ids"]).issubset(read_sources)
                or not claim.get("evidence_locator") or not claim.get("evidence_excerpt")):
            blockers.append(f"Unresolved/incomplete evidence for claim {claim.get('id', '?')}")
    if text:
        extra = json.loads(read("script/script.json") or "{}")
        payload = {"title": manifest["title"], "text": text, "names": extra.get("names", []), "sources": sorted(x for x in read_sources if x)}
        write_json(checks / "scriptcheck-input.json", payload)
        tool("yt-script/scriptcheck.py", [checks / "scriptcheck-input.json", "--words", "550-650"], "scriptcheck.json")
        if reports["scriptcheck.json"]["returncode"]:
            warnings.append("Upstream scriptcheck findings require editorial review; scores are not acceptance")
    titles = [x for x in read("metadata/titles.txt").splitlines() if x.strip()]
    if titles:
        tool("yt-package/title.py", [directory / "metadata/titles.txt", "--thumb", read("metadata/thumbnail-text.txt")], "titles.json")
    if len(titles) != 10:
        warnings.append(f"Expected ten title candidates; found {len(titles)}")
    for relative in ["research/brief.md", "research/factcheck.md", "hooks/review.md", "outline.md", "script/script-vi.txt",
                     "retention-review.md", "storyboard.md", "metadata/package.md", "metadata/thumbnail-brief.md", "metadata/description.txt"]:
        content = read(relative)
        if not content or PENDING in content:
            blockers.append(f"Incomplete drafting/review artifact: {relative}")
    if text and " ".join(text.split()) != " ".join(read("voice-over/voiceover-en.txt").split()):
        blockers.append("Voice-over text does not match the English narration")
    outline = read("outline.md")
    for stage in channel["framework"]:
        if f"## {stage}" not in outline:
            blockers.append(f"Outline missing framework stage: {stage}")
    seo = json.loads(read("metadata/seo.json") or "{}")
    if len(seo.get("queries", [])) != 3:
        blockers.append("SEO needs three reviewed search-intent queries")
    result = {"directory": str(directory), "spoken_words": word_count,
              "estimated_spoken_seconds_at_planning_rate": round(word_count / channel["planning_words_per_minute"] * 60, 1),
              "blockers": blockers, "warnings": warnings, "tool_reports": reports,
              "draft_bundle_complete": not blockers, "scientific_truth_verified_by_cli": False,
              "script_approved": manifest.get("script_approved", False), "paid_API_calls": 0,
              "note": "Evidence-field checks and editorial lint only; actual source reading, fact-checking and creator review remain necessary."}
    write_json(checks / "workflow-lint.json", result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", help="Create/resume an isolated per-video draft bundle")
    init.add_argument("title")
    init.add_argument("--slug")
    check = commands.add_parser("check-install", help="Check all twelve SKILL.md files, imports, licenses and upstream hashes")
    check.add_argument("--report", help="Optional report path inside the repository")
    lint = commands.add_parser("lint", help="Save offline checks for a filled-in video draft")
    lint.add_argument("directory", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "init":
            result = init_video(args.title, args.slug)
        elif args.command == "check-install":
            result = check_install()
            if args.report:
                target = ROOT / args.report
                if not within(target, ROOT):
                    raise ValueError("Report must stay inside the repository")
                write_json(target, result)
        else:
            result = lint_video(args.directory)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("ok", result.get("draft_bundle_complete", True)) else 1
    except (ValueError, OSError, KeyError, subprocess.TimeoutExpired) as error:
        print(f"youtube_agent: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
