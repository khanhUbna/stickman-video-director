"""Channel/workspace regression tests; all generated videos are temporary test drafts."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import youtube_agent as workflow

REAL_ROOT = workflow.ROOT


class YouTubeAgentIntegration(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="youtube-agent-integration-")
        self.addCleanup(self.temporary.cleanup)
        self.repo = Path(self.temporary.name)
        config = self.repo / "production/youtube/profile.json"
        config.parent.mkdir(parents=True)
        shutil.copy2(REAL_ROOT / "production/youtube/profile.json", config)
        patcher = mock.patch.object(workflow, "ROOT", self.repo)
        patcher.start()
        self.addCleanup(patcher.stop)

    def make_video(self, title="Fixture: a fictional video for installation testing"):
        return Path(workflow.init_video(title, repo=self.repo)["directory"])

    def test_installed_files_and_all_skill_dependencies_are_intact(self):
        report = workflow.check_install()
        self.assertTrue(report["ok"], report["errors"])
        self.assertEqual(report["skills_checked"], 12)
        self.assertEqual(report["tools_checked"], 9)
        self.assertEqual(report["hook_formulas"], 21)

    def test_channel_constraints_and_no_paid_api_defaults(self):
        config = workflow.profile()
        self.assertEqual(config["spoken_words"], {"min": 550, "max": 650})
        self.assertEqual(config["duration_seconds"], {"min": 240, "max": 300})
        self.assertEqual(config["automatic_skills"], ["yt-research", "yt-script", "yt-package", "yt-seo"])
        self.assertEqual(config["framework"], ["Hook", "Open Loop", "Setup", "Build-up", "Climax", "Payoff", "Emotional Ending"])
        self.assertFalse(config["paid_apis_allowed"])
        self.assertFalse(config["publication_allowed"])

    def test_modified_installed_code_is_detected_before_running_tools(self):
        copied_skills = self.repo / "copied-skills"
        for name in workflow.EXPECTED:
            shutil.copytree(workflow.SKILLS / name, copied_skills / name,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        script = copied_skills / "yt-package/title.py"
        script.write_text(script.read_text() + "\n# test-only changed copy\n")
        with mock.patch.object(workflow, "SKILLS", copied_skills):
            report = workflow.check_install()
        self.assertFalse(report["ok"])
        self.assertTrue(any("yt-package/title.py" in item for item in report["errors"]))

    def test_each_video_has_the_complete_pending_artifact_layout(self):
        directory = self.make_video()
        for relative in workflow.artifacts("fixture", workflow.profile()):
            self.assertTrue((directory / relative).is_file(), relative)
        manifest = json.loads((directory / "manifest.json").read_text())
        self.assertEqual(set(manifest["stages"].values()), {"pending"})
        self.assertFalse(manifest["audio_generated"])
        self.assertFalse(manifest["script_approved"])
        self.assertFalse(list(directory.rglob("*.wav")))

    def test_resume_preserves_existing_script_and_manifest(self):
        title = "Fixture: preserve my existing review"
        directory = self.make_video(title)
        script = directory / "script/script-en.txt"
        script.write_text("Creator edits must survive initialization.")
        old_manifest = (directory / "manifest.json").read_bytes()
        result = workflow.init_video(title, repo=self.repo)
        self.assertFalse(result["created"])
        self.assertEqual(script.read_text(), "Creator edits must survive initialization.")
        self.assertEqual((directory / "manifest.json").read_bytes(), old_manifest)

    def test_same_slug_cannot_overwrite_a_different_video(self):
        workflow.init_video("Fixture one", slug="same-slug", repo=self.repo)
        with self.assertRaisesRegex(ValueError, "different title"):
            workflow.init_video("Fixture two", slug="same-slug", repo=self.repo)

    def test_path_traversal_and_control_characters_are_rejected(self):
        for slug in ["../outside", "/tmp/outside", "nested/path", "a;touch-b"]:
            with self.subTest(slug=slug), self.assertRaises(ValueError):
                workflow.init_video("Fixture", slug=slug, repo=self.repo)
        for title in ["", "   ", "bad\ntitle", "bad\x00title"]:
            with self.subTest(title=title), self.assertRaises(ValueError):
                workflow.init_video(title, repo=self.repo)

    def test_output_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as outside:
            try:
                (self.repo / "youtube-videos").symlink_to(outside, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("Platform does not permit creating a symlink")
            with self.assertRaises(ValueError):
                self.make_video()
            self.assertEqual(list(Path(outside).iterdir()), [])

    def test_title_is_data_not_a_shell_command_in_the_real_cli(self):
        scripts = self.repo / "scripts"
        scripts.mkdir()
        shutil.copy2(REAL_ROOT / "scripts/youtube_agent.py", scripts / "youtube_agent.py")
        sentinel = self.repo / "must-not-exist"
        title = f"Fixture $(touch {sentinel}); a quoted title"
        process = subprocess.run([sys.executable, str(scripts / "youtube_agent.py"), "init", title],
                                 cwd=self.repo, capture_output=True, text=True, timeout=20)
        self.assertEqual(process.returncode, 0, process.stderr)
        directory = Path(json.loads(process.stdout)["directory"])
        self.assertEqual(json.loads((directory / "manifest.json").read_text())["title"], title)
        self.assertFalse(sentinel.exists())

    def test_empty_scaffold_cannot_pass_as_completed_research_or_script(self):
        directory = self.make_video()
        result = workflow.lint_video(directory)
        self.assertFalse(result["draft_bundle_complete"])
        self.assertFalse(result["scientific_truth_verified_by_cli"])
        self.assertEqual(result["paid_API_calls"], 0)
        self.assertTrue(any("source" in item for item in result["blockers"]))
        self.assertTrue(any("word count 0" in item for item in result["blockers"]))

    def test_word_limits_are_the_channel_limits_not_upstream_defaults(self):
        directory = self.make_video()
        for count, should_block in [(549, True), (550, False), (650, False), (651, True)]:
            with self.subTest(count=count):
                (directory / "script/script-en.txt").write_text(("fixture " * count).strip() + ".")
                result = workflow.lint_video(directory)
                count_blocked = any(item.startswith("Spoken word count") for item in result["blockers"])
                self.assertEqual(count_blocked, should_block)
                actual = result["tool_reports"]["scriptcheck.json"]["result"]
                self.assertEqual(actual["words"], count)

    def test_unread_source_cannot_support_a_claim_by_label_alone(self):
        directory = self.make_video()
        workflow.write_json(directory / "research/sources.json", [
            {"id": "fixture", "title": "Test fixture, not research", "url": "https://example.invalid/fixture",
             "access_status": "unavailable", "sections_read": []}])
        workflow.write_json(directory / "research/claims.json", [
            {"id": "test-claim", "claim": "Test fixture only", "verdict": "SUPPORTED", "source_ids": ["fixture"],
             "evidence_locator": "fixture line", "evidence_excerpt": "fixture text"}])
        result = workflow.lint_video(directory)
        self.assertTrue(any("test-claim" in item for item in result["blockers"]))

    def test_lint_refuses_to_read_an_external_manifest_symlink(self):
        directory = self.make_video()
        manifest = directory / "manifest.json"
        manifest.unlink()
        outside = self.repo / "outside.json"
        outside.write_text('{"private": "test sentinel"}')
        try:
            manifest.symlink_to(outside)
        except (OSError, NotImplementedError):
            self.skipTest("Platform does not permit creating a symlink")
        with self.assertRaisesRegex(ValueError, "manifest"):
            workflow.lint_video(directory)


if __name__ == "__main__":
    unittest.main()
