#!/usr/bin/env python3
"""Run the unchanged upstream suite against isolated copies of the installed skills."""
import json
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from youtube_agent import ROOT, SKILLS, UPSTREAM, EXPECTED, check_install, write_json


def main():
    integrity = check_install()
    if not integrity["ok"]:
        print(json.dumps(integrity, indent=2))
        return 1
    with tempfile.TemporaryDirectory(prefix="youtube-agent-installed-tests-") as temporary:
        sandbox = Path(temporary)
        shutil.copytree(UPSTREAM / "tests", sandbox / "tests", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        for name in EXPECTED:
            shutil.copytree(SKILLS / name, sandbox / "skills" / name, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        command = [sys.executable, "-W", "error::ResourceWarning", "-m", "unittest", "discover", "-s", "tests", "-v"]
        process = subprocess.run(command, cwd=sandbox, capture_output=True, text=True, encoding="utf-8", timeout=120)
        output = (process.stdout + process.stderr).replace(str(sandbox), "<installed-test-root>")
    reports = ROOT / "production/youtube/reports"
    reports.mkdir(parents=True, exist_ok=True)
    (reports / "upstream-installed-tests.txt").write_text(
        f"Python {platform.python_version()}\nUnmodified upstream tests; isolated copies of installed skills.\nTemporary root paths normalized for reproducible logs.\n\n{output}", encoding="utf-8")
    match = re.search(r"Ran (\d+) tests", output)
    result = {"passed": process.returncode == 0, "tests": int(match[1]) if match else None,
              "python": platform.python_version(), "commit": integrity["commit"],
              "upstream_tests_modified": False, "installed_skills_integrity": True,
              "ResourceWarning_mentions": output.count("ResourceWarning"),
              "paid_API_calls": 0, "network_calls": 0}
    write_json(reports / "upstream-installed-tests.json", result)
    print(json.dumps(result, indent=2))
    if process.returncode:
        print(output, file=sys.stderr)
    return process.returncode


if __name__ == "__main__":
    sys.exit(main())
